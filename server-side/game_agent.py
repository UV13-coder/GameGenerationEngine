import os
import time

import anthropic
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-haiku-4-5-20251001"


def _build_prompt(hero_desc, environment_desc, goal_desc, obstacle_desc):
    return f"""You are an expert game developer. Write a complete, single-file HTML5 canvas game.
Output ONLY raw HTML — no markdown, no code fences, no explanations.

Game details:
- Hero: {hero_desc}
- Environment: {environment_desc}
- Goal: {goal_desc}
- Obstacles: {obstacle_desc}

PIXEL ART CHARACTER SYSTEM (critical — read carefully):
All characters must be drawn as pixel art using canvas rectangles. Use this exact technique:

1. Define each character as a 2D array of color strings. Empty string means transparent.
   Example for a simple character:
   const heroSprite = [
     ['', '#FF0000', '#FF0000', ''],
     ['#FF0000', '#FFAA00', '#FFAA00', '#FF0000'],
     ['', '#FF0000', '#FF0000', ''],
   ];

2. Draw sprites using this function:
   function drawSprite(sprite, x, y, scale) {{
     sprite.forEach((row, r) => {{
       row.forEach((color, c) => {{
         if (color) {{
           ctx.fillStyle = color;
           ctx.fillRect(x + c * scale, y + r * scale, scale, scale);
         }}
       }});
     }});
   }}

3. Use scale=8 for characters (each pixel = 8x8 canvas pixels), giving large ~128x128 sprites on screen.

4. Design pixel art sprites that actually look like the character described:
   - {hero_desc}: design a 16x16 pixel art sprite with colors and shape matching this character. Think about their iconic colors, outfit, and silhouette.
   - Obstacles ({obstacle_desc}): design a different 16x16 pixel art sprite that fits the obstacle description.
   - Goal object: design a small 8x8 pixel art sprite (scale=3) for what the hero is trying to reach.

CANVAS & BACKGROUND:
5. Use a <canvas> sized 1400x550. Center it on the page with a black background.
6. Draw a themed scrolling background matching "{environment_desc}":
   - City/New York: dark blue sky, 6-8 gray building rectangles of varied heights, yellow window rectangles
   - Jungle: dark green sky, brown tree trunks, large green canopy rectangles
   - Space: black background, many small white star dots
   - Desert: orange sky, sand dunes, cacti shapes
   - For any environment: use at least 4 distinct background elements with fitting colors
7. Draw a thick ground rectangle at y=490, colored to match the environment.

GAMEPLAY:
8. Arrow keys move the hero left/right. Up arrow or Space to jump.
9. Gravity must feel natural (add a gravity constant ~0.5 each frame, reset on landing).
10. No double jump — only jump when touching the ground.
11. Implement a scrolling camera: as the hero moves right past x=700, scroll the background left so the level feels very long.
12. The full level is 5000px wide. Place 15-20 obstacles spread across the level.
13. Place 4-5 elevated platforms the hero can jump onto across the level.
14. Collision with an obstacle = Game Over with a Restart button.
15. Reaching the end of the level (x > 4800) = Win screen with a Play Again button.
16. Score counter top-left, increases as the hero moves right.
17. Use requestAnimationFrame for the game loop.
18. Single HTML file, no external dependencies."""


def _build_repair_prompt(broken_html, reason):
    return f"""The following HTML game has a problem: {reason}

Fix it and return ONLY the corrected raw HTML. No markdown, no explanations.

BROKEN CODE:
{broken_html}"""


def _clean_html(text):
    text = text.strip()
    if "```html" in text:
        text = text.split("```html", 1)[1]
        if "```" in text:
            text = text.split("```")[0]
    elif "```" in text:
        text = text.split("```", 1)[1]
        if "```" in text:
            text = text.split("```")[0]
    return text.strip()


def _is_valid_game(html):
    return (
        "<canvas" in html
        and "<script" in html
        and "requestAnimationFrame" in html
    )


def generate_game_html(hero_desc, environment_desc, goal_desc, obstacle_desc):
    print(f"Generating game: {hero_desc} in {environment_desc}...")

    prompt = _build_prompt(hero_desc, environment_desc, goal_desc, obstacle_desc)

    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}/3...")
            message = client.messages.create(
                model=MODEL,
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}],
            )
            html = _clean_html(message.content[0].text)

            if _is_valid_game(html):
                print("Game generated successfully.")
                return html

            print(f"Attempt {attempt + 1}: output missing required elements, retrying...")
            prompt = _build_repair_prompt(html, "missing <canvas>, <script>, or requestAnimationFrame")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(5)

    return "Error"
