# Manual Testing Guide - Game Generation Engine

This document provides step-by-step manual testing procedures for features that benefit from human validation.

## Prerequisites

1. Virtual environment activated
2. All dependencies installed: `pip install -r requirements.txt`
3. Server running: `python ./server-side/web_server.py`
4. Browser open to: `http://localhost:5000`

## Test Scenarios

### Section 1: User Interface Testing

#### Test 1.1: Chat Interface Layout
**Objective:** Verify the chat interface displays correctly

**Steps:**
1. Open `http://localhost:5000` in browser
2. Check that the chat interface is visible
3. Verify the chat input field is present
4. Verify the chat history display area exists
5. Check that buttons/controls are accessible

**Expected Results:**
- ✓ Chat interface loads without errors
- ✓ All UI elements are visible and properly aligned
- ✓ Input field is ready for user interaction
- ✓ Chat history is displayed clearly

---

#### Test 1.2: Responsive Design
**Objective:** Verify UI adapts to different screen sizes

**Steps:**
1. Open the app in browser
2. Resize browser window to smaller size (mobile-like)
3. Verify layout adapts properly
4. Resize to tablet size
5. Resize to desktop size

**Expected Results:**
- ✓ Layout is responsive
- ✓ No horizontal scrolling on mobile
- ✓ Text remains readable
- ✓ Buttons remain clickable

---

### Section 2: Conversation Flow Testing

#### Test 2.1: Complete Happy Path - Collecting Goals
**Objective:** Test the complete conversation flow for collecting goals game

**Steps:**

| Step | User Input | Expected Response |
|------|------------|------------------|
| 1 | (Load page) | "What is your name?" |
| 2 | "Alice" | "Describe your main hero..." |
| 3 | "Brave warrior" | "Where does the game take place?" |
| 4 | "Mountain kingdom" | "What is the hero's goal?" + options |
| 5 | "collecting goals" | "What object does the hero want to collect?" |
| 6 | "Golden treasure" | "What obstacles do you want to have?" |
| 7 | "Lava pits and dragons" | Game generated + game URL appears |

**Expected Results:**
- ✓ Each step progresses to the next question
- ✓ User input is acknowledged
- ✓ Final game is generated with correct theme
- ✓ Game URL is playable

---

#### Test 2.2: Complete Happy Path - Rescue Mission
**Objective:** Test rescue mission game generation flow

**Steps:**

| Step | User Input | Expected Response |
|------|------------|------------------|
| 1 | (Load page) | "What is your name?" |
| 2 | "Bob" | "Describe your main hero..." |
| 3 | "Space ranger" | "Where does the game take place?" |
| 4 | "Alien planet" | "What is the hero's goal?" + options |
| 5 | "rescue mission" | "What character does the hero want to rescue?" |
| 6 | "Lost astronaut" | "What obstacles do you want to have?" |
| 7 | "Asteroid field" | Game generated successfully |

**Expected Results:**
- ✓ Flow completes successfully
- ✓ Game includes rescue mission elements
- ✓ Generated game is playable

---

#### Test 2.3: Complete Happy Path - Escape
**Objective:** Test escape game generation flow

**Steps:**

| Step | User Input | Expected Response |
|------|------------|------------------|
| 1 | (Load page) | "What is your name?" |
| 2 | "Charlie" | "Describe your main hero..." |
| 3 | "Ninja" | "Where does the game take place?" |
| 4 | "Ancient temple" | "What is the hero's goal?" + options |
| 5 | "escape" | "How do you describe the enemy?" |
| 6 | "Ghost guardian" | Game generated successfully |

**Expected Results:**
- ✓ Flow completes without extra questions
- ✓ Game generated with escape mechanics
- ✓ Enemy appears as obstacle

---

#### Test 2.4: Invalid Choice Error Handling
**Objective:** Verify invalid choices are rejected properly

**Steps:**
1. Follow conversation until "What is the hero's goal?" question
2. Enter invalid option: "invalid choice"
3. Verify error message appears
4. Try entering correct option: "collecting goals"

**Expected Results:**
- ✓ Invalid choice rejected with error message
- ✓ Question repeated for valid input
- ✓ Correct choice accepted and flow continues

---

#### Test 2.5: Case-Insensitive Input
**Objective:** Verify system accepts input regardless of case

**Steps:**
1. When prompted for goal, try: "COLLECTING GOALS"
2. Try: "Rescue Mission"
3. Try: "time trial"
4. Try: "ESCAPE"

**Expected Results:**
- ✓ All variations accepted
- ✓ Flow continues normally
- ✓ No errors for different cases

---

### Section 3: Image Upload Testing (if applicable)

#### Test 3.1: Upload Hero Image
**Objective:** Test uploading custom hero image

**Steps:**
1. When asked to describe hero, look for image upload option
2. Select an image file (PNG, JPG, etc.)
3. Upload the image
4. Verify image is accepted and processed

**Expected Results:**
- ✓ Image uploads successfully
- ✓ File size validates
- ✓ System processes image
- ✓ Conversation continues

---

### Section 4: Game Generation Testing

#### Test 4.1: Generated Game Loads
**Objective:** Verify generated game HTML loads and runs

**Steps:**
1. Complete a full conversation flow
2. Click on the generated game URL/link
3. Wait for game to load
4. Verify game canvas appears
5. Look for game elements (hero, obstacles)

**Expected Results:**
- ✓ Game HTML loads in browser
- ✓ Canvas element renders
- ✓ Game information displayed
- ✓ Animations run smoothly

---

#### Test 4.2: Game Controls Work
**Objective:** Test game is interactive

**Steps:**
1. Load generated game
2. Try arrow keys: Left, Right
3. Try spacebar for jumping (if applicable)
4. Verify character responds

**Expected Results:**
- ✓ Character moves with arrow keys
- ✓ Character jumps with spacebar
- ✓ Controls are responsive
- ✓ No lag in responsiveness

---

#### Test 4.3: Different Game Types Vary
**Objective:** Verify different game types generate different games

**Steps:**
1. Generate a "collecting goals" game
2. Generate a "rescue mission" game
3. Generate an "obstacle run" game
4. Compare the three games

**Expected Results:**
- ✓ Each game has unique goals
- ✓ Game UI reflects the goal type
- ✓ Different obstacles/mechanics

---

### Section 5: Session Management Testing

#### Test 5.1: Multiple Sessions Independent
**Objective:** Verify multiple sessions don't interfere

**Steps:**
1. Open two browser tabs/windows
2. In Tab 1: Start conversation, enter name "Alice"
3. In Tab 2: Start conversation, enter name "Bob"
4. In Tab 1: Complete game generation
5. In Tab 2: Complete different game generation
6. Verify both games are different

**Expected Results:**
- ✓ Sessions are independent
- ✓ No data mixing between sessions
- ✓ Both games generated correctly

---

#### Test 5.2: Session Persistence
**Objective:** Verify session state is maintained

**Steps:**
1. Start conversation, enter name "David"
2. Go to next question, enter hero description
3. Close browser tab (don't exit app)
4. Open new tab and refresh
5. Check if conversation resumes or restarts

**Expected Results:**
- ✓ System either maintains state or gracefully restarts
- ✓ No errors occur
- ✓ User experience is consistent

---

### Section 6: Error Recovery Testing

#### Test 6.1: Network Error Recovery
**Objective:** Test recovery from network interruptions (if applicable)

**Steps:**
1. Start conversation
2. Simulate network issue (disable WiFi/network)
3. Try to continue
4. Re-enable network
5. Try to proceed

**Expected Results:**
- ✓ Graceful error message appears
- ✓ Can retry operation
- ✓ No stuck states

---

#### Test 6.2: Invalid Input Recovery
**Objective:** Test system recovery from various invalid inputs

**Steps:**
1. When asked for name, enter: `<script>alert('xss')</script>`
2. Verify no script execution
3. Try entering very long text (10000 characters)
4. Verify system handles it

**Expected Results:**
- ✓ No security issues (XSS, injection)
- ✓ System handles long input gracefully
- ✓ Flow continues normally

---

#### Test 6.3: Rapid Input Testing
**Objective:** Test system with rapid user input

**Steps:**
1. Quickly enter responses without waiting
2. Send multiple messages in quick succession
3. Verify system queues or handles properly

**Expected Results:**
- ✓ System doesn't crash
- ✓ Input is processed in order
- ✓ Responses are accurate

---

### Section 7: Performance Testing

#### Test 7.1: Page Load Time
**Objective:** Verify acceptable page load time

**Steps:**
1. Clear browser cache
2. Open `http://localhost:5000`
3. Measure time from request to fully loaded page
4. Record time

**Expected Results:**
- ✓ Page loads within 2-3 seconds
- ✓ All elements visible within 3 seconds

---

#### Test 7.2: Chat Response Time
**Objective:** Test response time for chat interactions

**Steps:**
1. Enter message
2. Measure time to receive response
3. Repeat 5 times
4. Calculate average

**Expected Results:**
- ✓ Response time under 2 seconds on average
- ✓ Consistent response times

---

#### Test 7.3: Game Generation Time
**Objective:** Test game generation performance

**Steps:**
1. Complete conversation flow
2. Note time when "generating" message appears
3. Time until game appears
4. Record total time

**Expected Results:**
- ✓ Game generation under 30 seconds (with API)
- ✓ Mock games instant (< 1 second)

---

### Section 8: Browser Compatibility Testing

#### Test 8.1: Chrome Browser
**Steps:**
1. Open app in Chrome
2. Test conversation flow
3. Generate game
4. Play game

**Expected:** ✓ All features work

#### Test 8.2: Firefox Browser
**Steps:**
1. Open app in Firefox
2. Test conversation flow
3. Generate game
4. Play game

**Expected:** ✓ All features work

#### Test 8.3: Safari Browser (Mac)
**Steps:**
1. Open app in Safari
2. Test conversation flow
3. Generate game
4. Play game

**Expected:** ✓ All features work

#### Test 8.4: Edge Browser
**Steps:**
1. Open app in Edge
2. Test conversation flow
3. Generate game
4. Play game

**Expected:** ✓ All features work

---

### Section 9: Accessibility Testing

#### Test 9.1: Keyboard Navigation
**Steps:**
1. Unplug mouse/trackpad
2. Use only Tab key to navigate
3. Use only arrow keys where applicable
4. Complete a game setup

**Expected Results:**
- ✓ All interactive elements accessible via keyboard
- ✓ Tab order is logical
- ✓ Can complete flow without mouse

---

#### Test 9.2: Screen Reader Compatibility
**Steps:**
1. Enable screen reader (e.g., Windows Narrator)
2. Navigate the interface
3. Verify text is read correctly
4. Check chat messages are readable

**Expected Results:**
- ✓ Text is properly announced
- ✓ No missing labels
- ✓ Navigation is clear

---

### Section 10: Data Input Testing

#### Test 10.1: Special Characters
**Steps:**
1. Enter name: `José García`
2. Enter hero: `Café warrior`
3. Enter location: `Tokyo, Japan (城)`
4. Enter obstacles: `Fire & ice @ Level 5`

**Expected Results:**
- ✓ All special characters accepted
- ✓ Game generated correctly
- ✓ Characters displayed in game

---

#### Test 10.2: Different Languages
**Steps:**
1. Enter name in Hebrew: `דוד`
2. Enter hero in Arabic: `الفارس`
3. Enter location in Spanish: `Castillo mágico`

**Expected Results:**
- ✓ Non-English characters accepted
- ✓ RTL text handled correctly
- ✓ Game generated with proper characters

---

#### Test 10.3: Maximum Input Length
**Steps:**
1. Enter very long name (100+ characters)
2. Enter very long hero description
3. Enter very long location
4. Enter very long obstacles description

**Expected Results:**
- ✓ All inputs accepted
- ✓ Game generated (possibly truncated)
- ✓ No system errors

---

## Test Data Sets

### Valid Test Data
```
Names: Alice, Bob, Charlie, Diana, 日本人
Heroes: Brave Knight, Space Ranger, Ninja, Wizard, Dragon
Locations: Castle, Space Station, Temple, Forest, City
Goals: collecting goals, rescue mission, time trial, escape, obstacle run
Objects: Golden treasure, Lost princess, Finish line, Exit, Victory flag
Obstacles: Dragons, Lava pits, Ghosts, Spikes, Rocks
```

### Edge Case Test Data
```
Empty strings: ""
Very long strings: "a" * 1000
Special characters: @#$%^&*()
Unicode: 中文, العربية, עברית
HTML: <script>alert('test')</script>
SQL: ' OR 1=1; --
```

---

## Test Execution Checklist

### Before Testing
- [ ] Virtual environment activated
- [ ] Server running
- [ ] Browser cache cleared
- [ ] Network connection stable
- [ ] No other apps using port 5000

### During Testing
- [ ] Document any issues found
- [ ] Take screenshots of errors
- [ ] Note response times
- [ ] Record browser/device info

### After Testing
- [ ] Summarize findings
- [ ] File bugs for issues
- [ ] Suggest improvements
- [ ] Update documentation

---

## Known Limitations & Workarounds

### Limitation 1: Long Game Generation
**Issue:** Game generation takes 20+ seconds
**Workaround:** Use mock mode for testing (currently active)

### Limitation 2: Image Processing
**Issue:** Large image uploads may timeout
**Workaround:** Use images under 2MB for testing

### Limitation 3: Multiple Rapid Requests
**Issue:** Rapid requests may queue
**Workaround:** Wait 1-2 seconds between requests

---

## Bug Report Template

When you find an issue, please report it with:

```
### Title
Brief description of the issue

### Steps to Reproduce
1. Step one
2. Step two
3. Step three

### Expected Behavior
What should happen

### Actual Behavior
What actually happened

### Screenshots/Logs
Attach relevant images or error logs

### Environment
- Browser: Chrome/Firefox/Safari/Edge
- OS: Windows/Mac/Linux
- App Version: x.x.x
```

---

## Test Report Template

After completing testing, fill in:

```
# Test Report - [Date]

## Summary
- Total Tests Run: X
- Passed: X
- Failed: X
- Success Rate: X%

## Critical Issues
- Issue 1
- Issue 2

## Minor Issues
- Issue 1
- Issue 2

## Recommendations
- Recommendation 1
- Recommendation 2

## Sign-off
Tester: _______________
Date: _______________
```

---

**Last Updated:** 2024
**Version:** 1.0
