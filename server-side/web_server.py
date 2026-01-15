# server-side/web_server.py
"""
Web-based Game Maker Chat Application Server

- Flask server
- Conversation flow (structured Q&A)
- Optional Gemini assistant fallback
- Storyboard generation (Hugging Face + optional Gemini prompt generation)
"""

import json
import logging
import os
import time
import uuid

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from gemini_assistant import GeminiGameAssistant
from storyboard_engine import generate_optimized_storyboard

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "client-side", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "client-side", "static"),
)
CORS(app)

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

STORYBOARD_FOLDER = os.path.join(app.static_folder, "storyboards")
os.makedirs(STORYBOARD_FOLDER, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
assistant = GeminiGameAssistant(api_key=GEMINI_API_KEY)

conversation_questions = {
    "name": {"question": "What is your name?", "type": "text", "next_question": "hero_description"},
    "hero_description": {"question": "Describe your main hero (you can use text or an image):", "type": "text_or_image", "next_question": "game_location"},
    "game_location": {"question": "Where does the game take place?", "type": "text", "next_question": "hero_goal"},
    "hero_goal": {
        "question": "What is the hero's goal?",
        "type": "choice",
        "options": ["collecting goals", "rescue mission", "time trial", "escape", "obstacle run"],
        "next_question_map": {
            "collecting goals": "collecting_goals_object",
            "rescue mission": "rescue_mission_character",
            "time trial": "time_trial_type",
            "escape": "escape_enemy_description",
            "obstacle run": "obstacle_run_obstacles",
        },
    },
    "collecting_goals_object": {"question": "What object does the hero want to collect?", "type": "text", "next_question": "collecting_goals_obstacles"},
    "collecting_goals_obstacles": {"question": "What obstacles do you want to have?", "type": "text"},
    "rescue_mission_character": {"question": "What character does the hero want to rescue (text or image)?", "type": "text_or_image", "next_question": "rescue_mission_obstacles"},
    "rescue_mission_obstacles": {"question": "What obstacles do you want to have?", "type": "text"},
    "time_trial_type": {"question": "Is the game a stopwatch or stay-in-frame kind of game?", "type": "choice", "options": ["stopwatch", "stay in frame"], "next_question": "time_trial_obstacles"},
    "time_trial_obstacles": {"question": "What obstacles do you want to have?", "type": "text"},
    "escape_enemy_description": {"question": "How do you describe the enemy (text or image)?", "type": "text_or_image"},
    "obstacle_run_obstacles": {"question": "What are the obstacles you want to have?", "type": "text"},
}

user_states = {}


def _normalize_obstacles(val: str) -> str:
    if val is None:
        return "No obstacles specified (default)"
    v = str(val).strip()
    if v == "" or v.lower() in ("none", "no", "n/a", "no obstacles"):
        return "No obstacles specified (default)"
    return v


def _map_answers_to_storyboard_json(answers: dict) -> dict:
    goal_map = {
        "collecting goals": "Collecting goals",
        "rescue mission": "Rescue mission",
        "time trial": "Time trial",
        "escape": "Escape",
        "obstacle run": "Obstacle run",
    }

    hero_goal_raw = (answers.get("hero_goal") or "").strip().lower()
    goal_type = goal_map.get(hero_goal_raw, "Rescue mission")

    character = answers.get("hero_description", "main character")
    background = answers.get("game_location", "game level")

    if hero_goal_raw == "collecting goals":
        target = answers.get("collecting_goals_object", "collectible")
        obstacles = _normalize_obstacles(answers.get("collecting_goals_obstacles"))
    elif hero_goal_raw == "rescue mission":
        target = answers.get("rescue_mission_character", "rescued character")
        obstacles = _normalize_obstacles(answers.get("rescue_mission_obstacles"))
    elif hero_goal_raw == "time trial":
        target = "Finish line"
        obstacles = _normalize_obstacles(answers.get("time_trial_obstacles"))
    elif hero_goal_raw == "escape":
        target = "Exit gate"
        obstacles = answers.get("escape_enemy_description", "enemy")
    elif hero_goal_raw == "obstacle run":
        target = "Victory flag"
        obstacles = _normalize_obstacles(answers.get("obstacle_run_obstacles"))
    else:
        target = "Goal"
        obstacles = "Obstacles"

    return {
        "goal_type": goal_type,
        "character": character,
        "background": background,
        "obstacles": obstacles,
        "target": target,
    }


def handle_user_text(user_message: str, session_id: str) -> dict:
    if session_id not in user_states or user_states[session_id].get("current_question") == "complete":
        user_states[session_id] = {"current_question": "name", "answers": {}}
        first_q = conversation_questions["name"]

        if user_message:
            user_states[session_id]["answers"]["name"] = user_message
            next_key = first_q.get("next_question")
            if next_key:
                user_states[session_id]["current_question"] = next_key
                next_q = conversation_questions[next_key]
                return {"message": next_q["question"], "type": next_q.get("type", "text"), "options": next_q.get("options", [])}

            user_states[session_id]["current_question"] = "complete"
            return finalize_structured_conversation(session_id)

        return {"message": first_q["question"], "type": first_q.get("type", "text"), "options": first_q.get("options", [])}

    current_key = user_states[session_id]["current_question"]
    current_data = conversation_questions[current_key]

    user_states[session_id]["answers"][current_key] = user_message

    next_key = None
    if "next_question_map" in current_data:
        chosen = user_message.lower()
        if chosen in current_data["next_question_map"]:
            next_key = current_data["next_question_map"][chosen]
        else:
            return {
                "message": f"Invalid choice. Please choose from {', '.join(current_data['options'])}",
                "type": "choice",
                "options": current_data["options"],
            }
    elif "next_question" in current_data:
        next_key = current_data["next_question"]

    if next_key:
        user_states[session_id]["current_question"] = next_key
        next_q = conversation_questions[next_key]
        return {"message": next_q["question"], "type": next_q.get("type", "text"), "options": next_q.get("options", [])}

    user_states[session_id]["current_question"] = "complete"
    return finalize_structured_conversation(session_id)


def finalize_structured_conversation(session_id: str) -> dict:
    answers = user_states[session_id]["answers"]

    storyboard_json = _map_answers_to_storyboard_json(answers)

    temp_dir = os.path.join(os.path.dirname(__file__), "tmp_storyboards")
    os.makedirs(temp_dir, exist_ok=True)
    temp_json_path = os.path.join(temp_dir, f"storyboard_{session_id}.json")

    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(storyboard_json, f, ensure_ascii=False, indent=2)

    file_prefix = f"storyboard_{uuid.uuid4().hex[:6]}"
    image_url = None

    try:
        image_url, _filename = generate_optimized_storyboard(
            json_path=temp_json_path,
            output_dir=STORYBOARD_FOLDER,
            file_prefix=file_prefix,
        )
    except Exception as e:
        logger.error("Storyboard generation failed: %s", e)

    user_name = (answers.get("name") or "").strip()

    if not image_url:
        msg = f"Okay{', ' + user_name if user_name else ''}! I saved your game details, but storyboard generation failed."
        return {"message": msg, "type": "text", "options": []}

    msg = f"Done{', ' + user_name if user_name else ''}! Here’s your storyboard 👇"
    return {"message": msg, "type": "storyboard", "image_url": image_url, "options": []}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field", "success": False}), 400

        user_message = (data.get("message") or "").strip()
        if not user_message:
            return jsonify({"error": "Message cannot be empty", "success": False}), 400

        session_id = request.headers.get("X-Session-ID", "default_session")
        logger.info("Received message from session %s: %s", session_id, user_message)

        try:
            message = handle_user_text(user_message, session_id)
        except Exception as err:
            logger.debug("handle_user_text error: %s", err)
            try:
                message = assistant.get_chat_response(user_message)
            except Exception as assistant_err:
                logger.error("Assistant fallback failed: %s", assistant_err)
                message = "Sorry, an internal error occurred while processing your message."

        if isinstance(message, dict):
            return jsonify(
                {
                    "response": message.get("message"),
                    "type": message.get("type"),
                    "options": message.get("options", []),
                    "image_url": message.get("image_url"),
                    "success": True,
                }
            ), 200

        return jsonify({"response": message, "success": True}), 200

    except Exception as e:
        logger.error("Error processing request: %s", e)
        return jsonify({"error": f"Server error: {str(e)}", "success": False}), 500


@app.route("/api/health", methods=["GET"])
def health():
    mode = "Demo Mode (No API Key)" if assistant.demo_mode else "Live Mode (Gemini API)"
    return jsonify({"status": "ok", "message": "Game Maker Chat Server is running", "mode": mode}), 200


@app.route("/api/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = secure_filename(file.filename)
        base, ext = os.path.splitext(filename)
        unique = f"{base}_{int(time.time())}_{uuid.uuid4().hex[:6]}{ext}"
        save_path = os.path.join(UPLOAD_FOLDER, unique)
        file.save(save_path)

        url = f"/static/uploads/{unique}"
        return jsonify({"url": url}), 200

    except Exception as e:
        logger.error("Upload failed: %s", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Game Maker Chat Server...")
    print(f"Mode: {'Demo Mode (No API Key)' if assistant.demo_mode else 'Live Mode (Gemini API)'}")
    if assistant.demo_mode:
        print("To enable Gemini AI: Set GEMINI_API_KEY environment variable")
    print("Access the server at: http://localhost:5000")

    app.run(host="127.0.0.1", port=5000, debug=True)
