"""
Storyboard Generation Engine

Responsible for:
- Converting structured game data into visual storyboard prompts
- Generating images using Hugging Face inference
- Creating a 2x2 storyboard collage
"""
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
load_dotenv(os.path.join(BASE_DIR, ".env"))


import json
import os
import re
import logging
from typing import List, Optional, Tuple

from PIL import Image
from google import genai
from huggingface_hub import InferenceClient

import storyboard_config

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

HF_MODEL = os.getenv("HF_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is missing from environment variables.")

USE_GEMINI = bool(GEMINI_API_KEY)

hf_client = InferenceClient(token=HF_TOKEN)
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if USE_GEMINI else None


def create_storyboard_collage(images: List[Optional[Image.Image]]) -> Optional[Image.Image]:
    """
    Combine up to four images into a 2x2 storyboard collage.
    If fewer than four images are available, the last valid image is duplicated.
    """
    valid_images = [img for img in images if img is not None]
    if not valid_images:
        return None

    while len(valid_images) < 4:
        valid_images.append(valid_images[-1].copy())

    width, height = valid_images[0].size
    collage = Image.new("RGB", (width * 2, height * 2), color=(30, 30, 30))

    positions = [(0, 0), (width, 0), (0, height), (width, height)]
    for img, pos in zip(valid_images[:4], positions):
        collage.paste(img, pos)

    return collage


def extract_json_array(text: str) -> List[str]:
    """
    Extract the first JSON array found in a text response.
    Gemini may return additional text around the JSON.
    """
    match = re.search(r"\[[\s\S]*\]", text or "")
    if not match:
        raise ValueError("No JSON array found in Gemini response.")

    data = json.loads(match.group(0))
    if not isinstance(data, list):
        raise ValueError("Parsed JSON is not a list.")

    return [str(x) for x in data]


def generate_optimized_storyboard(
    json_path: str,
    output_dir: str,
    file_prefix: str = "storyboard",
) -> Tuple[Optional[str], Optional[str]]:
    """
    Generate a 4-frame storyboard collage from structured game data.

    Returns:
        (image_url, filename) on success
        (None, None) on failure
    """
    with open(json_path, "r", encoding="utf-8") as f:
        game_data = json.load(f)

    goal_type = game_data.get("goal_type", "Rescue mission")
    character = game_data.get("character", "main character")
    background = game_data.get("background", "game level")
    obstacles = game_data.get("obstacles", "obstacles")
    target = game_data.get("target", "goal")

    scenario_steps = storyboard_config.GAME_SCENARIOS.get(
        goal_type,
        storyboard_config.GAME_SCENARIOS["Rescue mission"],
    )

    prompts: List[str] = []

    if USE_GEMINI and gemini_client is not None:
        system_prompt = f"""
You are a professional storyboard artist.

Return ONLY a JSON array with EXACTLY 4 image prompts.
No markdown. No explanations.

Rules:
- Replace [character] with: {character}
- Replace [target] with: {target}
- Replace [obstacles] with: {obstacles}
- Use this style consistently: {storyboard_config.BASE_STYLE}
- Setting: {background}
- All movement should be left-to-right
- Pure 2D side-view (no perspective)

Scenario steps:
{json.dumps(scenario_steps, ensure_ascii=False)}
"""
        try:
            response = gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=system_prompt,
            )
            prompts = extract_json_array(response.text)
        except Exception as exc:
            logger.warning("Gemini prompt generation failed, falling back: %s", exc)

    if not prompts:
        for step in scenario_steps:
            prompt = (
                step.replace("[character]", character)
                .replace("[target]", target)
                .replace("[obstacles]", obstacles)
            )
            prompt += f" Style: {storyboard_config.BASE_STYLE}. Setting: {background}. {storyboard_config.HARD_RULES}"
            prompts.append(prompt)

    prompts = prompts[:4]
    while len(prompts) < 4:
        prompts.append(prompts[-1])

    frames: List[Optional[Image.Image]] = []
    for prompt in prompts:
        try:
            image = hf_client.text_to_image(
                prompt=prompt,
                model=HF_MODEL,
                negative_prompt=storyboard_config.NEGATIVE_PROMPT,
            )
            frames.append(image)
        except Exception as exc:
            logger.error("Image generation failed: %s", exc)
            frames.append(None)

    collage = create_storyboard_collage(frames)
    if not collage:
        return None, None

    os.makedirs(output_dir, exist_ok=True)
    safe_goal = goal_type.lower().replace(" ", "_")
    filename = f"{file_prefix}_{safe_goal}.png"
    output_path = os.path.join(output_dir, filename)
    collage.save(output_path)

    return f"/static/storyboards/{filename}", filename
