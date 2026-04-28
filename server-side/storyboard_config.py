# server-side/storyboard_config.py

BASE_STYLE = (
    "flat 2D side-scrolling platformer, 16-bit pixel art, SNES sprite style, "
    "pure profile view, facing right, 16:9 ratio, clean crisp sprites, "
    "simple background, no text, no watermark"
)

HARD_RULES = (
    "IMPORTANT: Only the hero and (if specified) the target may appear as characters. "
    "No extra characters, no crowd, no NPCs, no civilians, no sidekicks, no enemies unless explicitly stated. "
    "Background buildings/props only. Pure side view."
)

NEGATIVE_PROMPT = (
    "3d, realistic, perspective, depth, vanishing point, photorealistic, high poly, "
    "crowd, group, multiple people, extra characters, NPCs, civilians, bystanders, side characters, companions, team, "
    "face closeup, portrait, looking at camera, back view, walking away, "
    "text, captions, subtitles, watermark, logo, signature, "
    "helmet removed, face revealed"
)

GAME_SCENARIOS = {
    "Collecting goals": [
        "Frame 1: ONLY ONE character (the hero): [character] stands on the far left of a flat 2D level, facing right.",
        "Frame 2: ONLY ONE character (the hero): [character] jumps right to touch ONE floating [target]. No other characters.",
        "Frame 3: ONLY ONE character (the hero): [character] jumps over ONE [obstacles] in the center. No other characters.",
        "Frame 4: ONLY ONE character (the hero): [character] stands on the far right, pure side view, arms forward, clearly holding the collected [target] in both hands. The [target] is visible and centered. Victory pose. No piles. No other characters. No NPCs. No crowd."
    ],

    "Rescue mission": [
        "Frame 1: ONLY ONE character (the hero): [character] on the far left, facing right toward the goal. The rescued character is NOT visible.",
        "Frame 2: ONLY ONE character (the hero): [character] runs right across a 2D floor. No other characters.",
        "Frame 3: ONLY ONE character (the hero): [character] clashes against [obstacles] in the center. The rescued [target] is NOT visible.",
        "Frame 4: ONLY TWO characters: [character] and ONE rescued [target]. They stand side-by-side on the far right, safe and victorious. NO other characters anywhere.",
    ],

    "Time trial": [
        "Frame 1: ONLY ONE character (the hero): [character] at the far left, facing right. A 2D digital timer is visible at the top. No other characters.",
        "Frame 2: ONLY ONE character (the hero): [character] sprinting right with motion lines. No other characters.",
        "Frame 3: ONLY ONE character (the hero): [character] dashes right to bypass ONE [obstacles]. No other characters.",
        "Frame 4: ONLY ONE character (the hero): [character] crosses a glowing vertical finish line on the far right, timer stopped. No other characters.",
    ],

    "Escape": [
        "Frame 1: ONLY ONE character (the hero): [character] on the left, facing right, alarmed. [obstacles] is visible as the threat on the far left. No extra characters.",
        "Frame 2: ONLY ONE character (the hero): [character] sprinting right; [obstacles] chasing from far left. No other characters.",
        "Frame 3: ONLY ONE character (the hero): [character] sliding right under a low [obstacles]. No other characters.",
        "Frame 4: ONLY ONE character (the hero): [character] safe on the far right behind a closed 2D vertical gate. No other characters.",
    ],

    "Obstacle run": [
        "Frame 1: ONLY ONE character (the hero): [character] on the far left looking right at a series of 2D platforms. No other characters.",
        "Frame 2: ONLY ONE character (the hero): [character] balancing on a thin ledge moving right. No other characters.",
        "Frame 3: ONLY ONE character (the hero): [character] jumps right to avoid ONE swinging [obstacles]. No other characters.",
        "Frame 4: ONLY ONE character (the hero): [character] touches a victory flag on the far right platform. No other characters.",
    ],
}
