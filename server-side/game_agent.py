from google import genai
import os
import time

# הגדרת המפתח והלקוח
API_KEY = "AIzaSyDrd_FzseeDTj5PMaQrBuJ7LBiFjOv10r4"
client = genai.Client(api_key=API_KEY)


# =====================================================================
# 1. גרסת ה-MOCK (פעילה כרגע)
# מחזירה משחק דמה מיידי כדי שנוכל לבדוק את האתר בלי לחכות לשרתים
# =====================================================================
def generate_game_html(hero_desc, environment_desc, goal_desc, obstacle_desc):
    print(f"מתחיל לתכנן משחק עם: {hero_desc} ב-{environment_desc}...")
    print("🤖 מזהה עומס בשרתים: עובר למצב Mock (משחק מדומה לצורך בדיקות תוכנה)...")

    mock_game_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{hero_desc}'s Adventure</title>
        <style>
            body {{ margin: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #222; color: white; font-family: sans-serif; }}
            #gameCanvas {{ background-color: #87CEEB; border: 4px solid #fff; border-radius: 10px; margin-top: 20px; }}
            .info-box {{ background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="info-box">
            <h1 style="margin:0; color: #00C9FF;">🎮 THE {hero_desc.upper()} GAME</h1>
            <p style="font-size: 18px; margin: 5px 0;"><strong>Location:</strong> {environment_desc}</p>
            <p style="font-size: 18px; margin: 5px 0;"><strong>Mission:</strong> {goal_desc}</p>
            <p style="font-size: 18px; margin: 5px 0; color: #FF512F;"><strong>Watch out for:</strong> {obstacle_desc}</p>
        </div>

        <canvas id="gameCanvas" width="800" height="400"></canvas>

        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            let x = 50;

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#228B22';
                ctx.fillRect(0, 350, canvas.width, 50);

                ctx.fillStyle = '#FF512F';
                ctx.fillRect(x, 300, 50, 50); 

                x += 3;
                if(x > canvas.width) x = -50;

                requestAnimationFrame(draw);
            }}
            draw();
        </script>
    </body>
    </html>
    """
    return mock_game_html.strip()


# =====================================================================
# 2. הגרסה האמיתית (מכובה כרגע בהערה)
# כשהשרתים של גוגל יחזרו לעבוד, פשוט תמחקי את ה-Mock שלמעלה,
# ותמחקי את הגרשיים ( """) שעוטפים את הפונקציה הזו למטה!
# =====================================================================
"""
def generate_game_html(hero_desc, environment_desc, goal_desc, obstacle_desc):
    print(f"מתחיל לתכנן משחק עם: {hero_desc} ב-{environment_desc}...")

    prompt = f'''
    You are an expert game developer. Write a complete, single-file HTML5 canvas game.
    Do NOT include any markdown formatting (like ```html), explanations, or text outside the HTML. Output ONLY the raw HTML code.

    Game Elements:
    - Hero: {hero_desc} 
    - Environment: {environment_desc}
    - Goal: {goal_desc}
    - Obstacles: {obstacle_desc}

    Graphics & Proportions (CRITICAL):
    - Use JavaScript's Image() to load: 'static/bg.png', 'static/hero.png', 'static/taxi.png', 'static/princess.png'.
    - Background: Draw to completely fill the canvas.
    - Hero & Obstacles: You MUST maintain their original aspect ratio. Scale the hero to be roughly 15% of the canvas height. Scale obstacles proportionally. 

    Mechanics & Physics (STRICT RULES):
    1. Movement: Smooth left/right movement using Arrow keys. Do NOT make the movement too fast.
    2. Jumping: You MUST implement an 'isGrounded' check. The hero CANNOT double jump. They can only jump if they are touching the ground or a platform. Gravity should feel natural.
    3. Obstacles: Obstacles MUST spawn continuously on the right side of the screen and move leftwards towards the hero.
    4. Platforms: Generate 3-4 floating platforms (draw them as simple colored rectangles for now) that the hero can jump onto and stand on.
    5. Win/Loss: Collision with moving obstacles = Game Over. Reaching the Goal (placed at the far right or top) = Win.
    '''

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )

            html_content = response.text.strip()

            if html_content.startswith("```html"):
                html_content = html_content[7:]
            if html_content.endswith("```"):
                html_content = html_content[:-3]

            return html_content.strip()

        except Exception as e:
            print(f"⚠️ השרת עמוס (ניסיון {attempt + 1} מתוך {max_retries}). ממתין 15 שניות ומנסה שוב אוטומטית...")
            time.sleep(15)

    return "Error"
"""