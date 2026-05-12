# Software Testing Plan

This document lists the exact tests that should be performed for the current Game Generation Engine project.
It covers the project core: backend chat API, AI-assisted game generation, file upload, and client-side chat interface.
Storyboard-specific behavior is intentionally excluded because it is no longer relevant to the current project.

## 1. Unit Tests

1. `_normalize_obstacles` function
   - Input: `None`
     - Call: `_normalize_obstacles(None)`
     - Expected output: `No obstacles specified (default)`
   - Input: `""`
     - Call: `_normalize_obstacles("")`
     - Expected output: `No obstacles specified (default)`
   - Input: `"none"`
     - Call: `_normalize_obstacles("none")`
     - Expected output: `No obstacles specified (default)`
   - Input: `"No"`
     - Call: `_normalize_obstacles("No")`
     - Expected output: `No obstacles specified (default)`
   - Input: `"n/a"`
     - Call: `_normalize_obstacles("n/a")`
     - Expected output: `No obstacles specified (default)`
   - Input: `"spikes and pits"`
     - Call: `_normalize_obstacles("spikes and pits")`
     - Expected output: `spikes and pits`

2. `_map_answers_to_game_json` function
   - Input: `{"hero_goal": "collecting goals", "hero_description": "Brave knight", "game_location": "haunted forest", "collecting_goals_object": "magic gems", "collecting_goals_obstacles": "spikes"}`
     - Expected output:
       - `goal_type`: `Collecting goals`
       - `character`: `Brave knight`
       - `background`: `haunted forest`
       - `target`: `magic gems`
       - `obstacles`: `spikes`
   - Input: `{"hero_goal": "rescue mission", "hero_description": "Space ranger", "game_location": "outer space", "rescue_mission_character": "lost alien", "rescue_mission_obstacles": "asteroid field"}`
     - Expected output:
       - `goal_type`: `Rescue mission`
       - `target`: `lost alien`
       - `obstacles`: `asteroid field`
   - Input: `{"hero_goal": "time trial", "hero_description": "Speed runner", "game_location": "city streets", "time_trial_obstacles": "traffic"}`
     - Expected output:
       - `goal_type`: `Time trial`
       - `target`: `Finish line`
       - `obstacles`: `traffic`
   - Input: `{"hero_goal": "escape", "hero_description": "Ninja", "game_location": "ancient temple", "escape_enemy_description": "ghost guardian"}`
     - Expected output:
       - `goal_type`: `Escape`
       - `target`: `Exit gate`
       - `obstacles`: `ghost guardian`
   - Input: `{"hero_goal": "obstacle run", "hero_description": "Runner", "game_location": "lava canyon", "obstacle_run_obstacles": "falling rocks"}`
     - Expected output:
       - `goal_type`: `Obstacle run`
       - `target`: `Victory flag`
       - `obstacles`: `falling rocks`
   - Input: `{"hero_goal": "unknown", "hero_description": "Hero", "game_location": "world"}`
     - Expected output:
       - `goal_type`: `Rescue mission`
       - `target`: `Goal`
       - `obstacles`: `Obstacles`

3. `handle_user_text` function
   - Start new session when session id is missing
     - Call: `handle_user_text("", "session1")`
     - Expected output: `{"message": "What is your name?", "type": "text", "options": []}`
   - Accept user name and move to hero description
     - Input state: `{"current_question": "name", "answers": {}}`
     - Call: `handle_user_text("Alice", "session1")`
     - Expected output: `{"message": "Describe your main hero (you can use text or an image):", "type": "text_or_image", "options": []}`
   - Accept hero description and move to game location
     - Call: `handle_user_text("A brave wizard", "session1")`
     - Expected output: `{"message": "Where does the game take place?", "type": "text", "options": []}`
   - Accept game location and move to hero goal
     - Call: `handle_user_text("A floating castle", "session1")`
     - Expected output: `{"message": "What is the hero's goal?", "type": "choice", "options": ["collecting goals", "rescue mission", "time trial", "escape", "obstacle run"]}`
   - Accept valid hero goal choice and move to mapped next question
     - Call: `handle_user_text("rescue mission", "session1")`
     - Expected output: `{"message": "What character does the hero want to rescue (text or image)?", "type": "text_or_image", "options": []}`
   - Reject invalid hero goal choice
     - Input: `handle_user_text("wrong option", "session1")` while current question is `hero_goal`
     - Expected output:
       - `message`: `Invalid choice. Please choose from collecting goals, rescue mission, time trial, escape, obstacle run`
       - `type`: `choice`
       - `options`: `["collecting goals", "rescue mission", "time trial", "escape", "obstacle run"]`
   - Complete conversation after the final answer and produce game-ready response
     - Call: `handle_user_text("robot friend", "session1")` after rescue mission path
     - Expected output contains `type`: `game_ready` and a non-empty `game_url`

4. `finalize_structured_conversation` function
   - When `generate_game_html` returns valid HTML
     - Input answers:
       - `name`: `Alice`
       - `hero_description`: `Brave knight`
       - `game_location`: `Dark castle`
       - `hero_goal`: `escape`
       - `escape_enemy_description`: `dragon`
     - Mock `generate_game_html("Brave knight", "Dark castle", "Exit gate", "dragon")` to return `"<html>game</html>"`
     - Expected output:
       - `type`: `game_ready`
       - `game_url`: string matching `/static/games/game_[a-f0-9]{6}.html`
       - saved file exists under `static/games`
   - When `generate_game_html` returns `Error`
     - Mock `generate_game_html(...)` to return `"Error"`
     - Expected output:
       - `type`: `text`
       - `message`: includes `Sorry` and mentions game generation servers are busy

5. `GeminiGameAssistant` fallback behavior
   - Input: `handle_user_text` raises an exception for a given message
     - Expected: call `assistant.get_chat_response(user_message)` and return that string
   - Input: both `handle_user_text` and fallback `assistant.get_chat_response` raise exceptions
     - Expected output: `{"error": "Sorry, an internal error occurred while processing your message."}` or equivalent server error response
   - Test `assistant.demo_mode` when `GEMINI_API_KEY` is not set
     - Expected output: `mode` in `/api/health` contains `Demo Mode`

## 2. API Tests

1. `/api/chat`
   - POST valid JSON with `message`
     - Request body: `{"message": "Hello"}`
     - Expected response:
       - `success`: `true`
       - `response`: string
       - `type`: `text` or `choice` or `text_or_image` or `game_ready`
       - `options`: array
   - POST missing `message`
     - Request body: `{}`
     - Expected HTTP 400
     - Expected JSON error: `Missing 'message' field`
   - POST empty `message`
     - Request body: `{"message": ""}`
     - Expected HTTP 400
     - Expected JSON error: `Message cannot be empty`
   - Send messages through the full conversation sequence
     - Example sequence:
       1. `{"message": "Alice"}` → `What is your name?` branch start
       2. `{"message": "Brave wizard"}` → `hero_description`
       3. `{"message": "Ancient tower"}` → `game_location`
       4. `{"message": "time trial"}` → `time_trial_type`
       5. `{"message": "stopwatch"}` → `time_trial_obstacles`
       6. `{"message": "lava pits"}` → final `game_ready`
     - Expected transitions across questions
   - Final message completes the flow and returns `game_ready` + `game_url`
     - Expected response contains `type`: `game_ready`
     - Expected `game_url`: non-empty string beginning with `/static/games/`
   - Invalid `hero_goal` choice returns the same question type and options list
     - Request body: `{"message": "invalid choice"}` at hero_goal step
     - Expected response:
       - `type`: `choice`
       - `options`: `["collecting goals", "rescue mission", "time trial", "escape", "obstacle run"]`

2. `/api/upload`
   - POST valid file upload with `file`
     - Upload file: `hero.png`
     - Expected HTTP 200
     - Expected response: `{"url": "/static/uploads/<filename>"}`
   - POST request without `file`
     - Expected HTTP 400
     - Expected response: `{"error": "No file part in the request"}`
   - POST request with empty filename
     - Use an empty file name in form data
     - Expected HTTP 400
     - Expected response: `{"error": "No selected file"}`
   - Ensure uploaded filename uses `secure_filename` and unique suffix
     - Uploaded file name should not contain path segments
     - Expected returned URL contains a unique file name value

3. `/api/health`
   - GET request
     - Expected HTTP 200
     - Expected response:
       - `status`: `ok`
       - `message`: `Game Maker Chat Server is running`
       - `mode`: contains `Demo Mode` or `Live Mode`

## 3. Integration Tests

1. Full game creation conversation
   - Use repeated `/api/chat` requests with the same `X-Session-ID`
   - Example flow:
     1. `{"message": "Alice"}`
     2. `{"message": "A brave knight"}`
     3. `{"message": "Haunted castle"}`
     4. `{"message": "collecting goals"}`
     5. `{"message": "gold coins"}`
     6. `{"message": "lava pits"}`
   - Expected final response:
     - `type`: `game_ready`
     - `game_url`: valid `/static/games/...` value
   - Expected side effect: a new game HTML file exists in `static/games`

2. Upload flow
   - Upload an image during a `text_or_image` question
     - Request file: sample image file
     - Expected response: `{"url": "/static/uploads/<unique-name>"}`
     - Expected side effect: file exists in `static/uploads`

3. Session persistence
   - Use the same `X-Session-ID` across multiple `/api/chat` calls
   - Expected: conversation state persists and questions advance correctly
   - When using a different `X-Session-ID`, expected: a new conversation starts at `What is your name?`

4. Fallback interaction
   - Simulate `handle_user_text` raising an unexpected exception
   - Expected: `/api/chat` returns a fallback assistant response from `assistant.get_chat_response`
   - If fallback also fails, expected: server error message with `Sorry, an internal error occurred while processing your message.`

## 4. UI / Frontend Test Cases

1. Chat page loads
   - Open `/`
   - Expected: `index.html` loads with `script_v2.js`
   - Expected: welcome message appears in the chat panel

2. Sending a message
   - Enter `Hello` in the text area and click send
   - Expected: user message appears in chat
   - Expected: send button is disabled while request is pending
   - Expected: assistant response appears after the request returns

3. Option rendering
   - When `/api/chat` returns `options`, expected: option controls are displayed in the UI
   - When `/api/chat` returns `type: text_or_image`, expected: file upload UI is displayed

4. Game-ready flow
   - When server returns `type: game_ready` and `game_url`
     - Expected: the UI renders a play button or link to the generated game
     - Expected: assistant message confirms that the game is ready

5. Message personalization logic
   - Provide a name when the assistant asks for it
   - Expected: assistant responses include the user name in the first few replies

## 5. Regression Tests

1. Verify game creation still works after any change to conversation logic
   - Expected: full conversation still reaches `game_ready` when given valid inputs
2. Verify upload endpoint still accepts files and returns URLs
   - Expected: `/api/upload` returns `200` and valid upload paths
3. Verify health endpoint remains available
   - Expected: `/api/health` returns `status: ok`
4. Verify no storyboard-related behavior is present in current UI or API
   - Expected: no `type: storyboard` responses
   - Expected: no storyboard references displayed in the chat UI

## 6. Execution Notes

- Use `pytest` for Python backend unit and integration tests.
- Use `requests` or Postman for `/api/chat`, `/api/upload`, and `/api/health` verification.
- Use browser manual testing or simple DOM assertions for the frontend.
- Mock `generate_game_html` and Gemini assistant behavior during unit tests to isolate backend logic.
''' ; path.write_text(text, encoding='utf-8')"