"""
Gemini AI Assistant for Game Design.

Uses the Google GenAI SDK (google-genai) to:
- Extract a structured game JSON from user instructions
- Generate the next best question based on the current JSON
"""

from __future__ import annotations

import copy
import json
import logging
import re
from typing import Any, Dict, Optional

from google import genai

logger = logging.getLogger(__name__)


class GameStructure:
    """Holds the canonical game JSON template and prompt builders."""

    TEMPLATE: Dict[str, Any] = {
        "game": {
            "title": "",
            "description": "",
            "difficulty": "medium",  # easy, medium, hard
            "theme": "default",      # default, space, castle, etc.
        },
        "player": {
            "width": 32,
            "height": 32,
            "speed": 5,
            "jump_power": 15,
            "jump_height": 100,
            "color": "#00FF00",
        },
        "levels": [
            {
                "id": 1,
                "name": "Level 1",
                "width": 800,
                "height": 600,
                "platforms": [
                    {"x": 0, "y": 550, "width": 800, "height": 50, "type": "solid"}
                ],
                "enemies": [
                    {
                        "type": "patroller",
                        "x": 200,
                        "y": 500,
                        "width": 32,
                        "height": 32,
                        "speed": 3,
                        "patrol_range": 200,
                    }
                ],
                "collectibles": [{"type": "coin", "x": 100, "y": 480, "value": 10}],
                "goal": {"x": 700, "y": 480, "type": "flag"},
            }
        ],
        "mechanics": {
            "has_double_jump": False,
            "has_dash": False,
            "has_wall_slide": False,
            "gravity": 0.6,
        },
    }

    @staticmethod
    def get_extraction_prompt(current_json: Dict[str, Any]) -> str:
        """
        Build a prompt that instructs the model to return a full JSON object
        matching the exact TEMPLATE structure, updated based on user instruction.
        """
        template_json = json.dumps(GameStructure.TEMPLATE, indent=2, ensure_ascii=False)
        current_json_str = json.dumps(current_json or {}, indent=2, ensure_ascii=False)

        return f"""
You are a game design AI assistant.
Your job: update/complete the game JSON based on the user's instruction.

Return ONLY a valid JSON object matching this exact template structure:

TEMPLATE:
{template_json}

CURRENT JSON (may be empty/incomplete):
{current_json_str}

RULES:
1. Return ONLY valid JSON (no markdown, no explanations)
2. Keep the structure exactly like the template
3. Fill in what the user specifies
4. Use reasonable defaults for missing info
5. All numeric fields must be valid numbers
6. Keep descriptions concise
""".strip()

    @staticmethod
    def get_chat_user_response(current_json: Dict[str, Any]) -> str:
        """
        Build a prompt that asks the model to produce ONE short next question
        to fill the most important missing detail.
        """
        template_json = json.dumps(GameStructure.TEMPLATE, indent=2, ensure_ascii=False)
        current_json_str = json.dumps(current_json or {}, indent=2, ensure_ascii=False)

        return f"""
You are a game design AI assistant.

Here is the CURRENT game JSON:
{current_json_str}

Here is the TEMPLATE:
{template_json}

Task:
- Ask the user ONE short, interactive question that helps fill the most important missing detail.
- Don't ask for everything at once.
- Don't repeat the JSON.
- Be engaging and concise.
Return ONLY the user question text.
""".strip()


class GeminiGameAssistant:
    """Communicates with the Gemini API using the google-genai SDK."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        demo_mode: bool = False,
        model_name: str = "gemini-2.5-flash",
    ):
        self.demo_mode = demo_mode or not api_key
        self.model_name = model_name
        self.client = None

        # Use a deep copy to avoid accidental shared mutations.
        self.game_structure: Dict[str, Any] = copy.deepcopy(GameStructure.TEMPLATE)

        if not self.demo_mode:
            try:
                self.client = genai.Client(api_key=api_key)
                logger.info("Gemini AI initialized in Live Mode (google-genai)")
            except Exception as exc:
                logger.error(
                    "Failed to initialize Gemini client: %s. Falling back to Demo Mode.",
                    exc,
                )
                self.demo_mode = True
        else:
            logger.info("Gemini AI initialized in Demo Mode")

    def extract_game_structure(self, user_instruction: str) -> Dict[str, Any]:
        """
        Extract/update game structure from a user instruction using Gemini.

        Returns a dict with:
        - success (bool)
        - game_structure (dict)
        - message (str)
        """
        if self.demo_mode:
            return self._demo_extraction(user_instruction)

        try:
            system_prompt = GameStructure.get_extraction_prompt(self.game_structure)

            resp = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{system_prompt}\n\nUSER INSTRUCTION:\n{user_instruction}",
            )

            updated = self._parse_json_response((resp.text or "").strip())
            if updated:
                self.game_structure = updated

            return {
                "success": True,
                "game_structure": self.game_structure,
                "message": "Game structure updated.",
            }

        except Exception as exc:
            logger.error("Error extracting game structure: %s", exc)
            return {
                "success": False,
                "game_structure": self.game_structure,
                "message": f"Extraction failed: {exc}",
            }

    def get_chat_response(self, user_message: str) -> str:
        """
        Generate the next best question/response based on the current JSON state.
        """
        if self.demo_mode:
            return self._demo_chat_response(user_message)

        try:
            prompt = GameStructure.get_chat_user_response(self.game_structure)
            resp = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return (resp.text or "").strip()

        except Exception as exc:
            logger.error("Error getting chat response: %s", exc)
            return "Something went wrong. Can you tell me one more detail about your game?"

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from a model response.
        If parsing fails, return a deep copy of the template.
        """
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", response_text)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass

        logger.warning("Could not parse JSON response. Using template fallback.")
        return copy.deepcopy(GameStructure.TEMPLATE)

    def _demo_extraction(self, instruction: str) -> Dict[str, Any]:
        game_structure = copy.deepcopy(GameStructure.TEMPLATE)
        game_structure["game"]["title"] = "My Platform Game"
        game_structure["game"]["description"] = f"A platformer based on: {instruction}"
        self.game_structure = game_structure

        return {
            "success": True,
            "game_structure": game_structure,
            "message": "Game design extracted! (Demo Mode)",
        }

    def _demo_chat_response(self, _message: str) -> str:
        return "Tell me: what is the main goal of your hero (collect / rescue / escape / time trial / obstacle run)?"
