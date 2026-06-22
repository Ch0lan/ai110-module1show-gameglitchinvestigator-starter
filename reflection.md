# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the app, several things were immediately wrong. The "Developer Debug Info" expander let me see the secret number, yet I still couldn't win — even guessing the exact secret returned a "Too Low" or "Too High" hint. Hints were also clearly backwards: guessing a number larger than the secret told me to go *higher*, not lower. On top of that, the game seemed to give different results for the same guess depending on which attempt number it was, because the secret was silently converted to a string on even-numbered turns.

**Concrete bugs noticed at first run:**
- Hints were inverted — "Go HIGHER!" appeared when my guess exceeded the secret.
- On even attempts, the game converted the secret to a `str` before comparing, causing alphabetical ("99" > "9") instead of numeric comparison.
- Hard difficulty (range 1–50) was *easier* than Normal (1–100), which is backwards.
- Attempts counter started at 1, so the first render showed one fewer attempt than allowed.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, secret is 50 | Hint: "Too High — Go LOWER!" | Hint: "Go HIGHER!" (inverted) | none |
| Guess 50 on attempt 2, secret is 50 | Win | "Too Low" — string comparison "50" vs 50 failed | none |
| Select Hard difficulty | Harder to guess (range 1–200) | Easier (range 1–50, smaller than Normal) | none |
| Open app fresh, 8 attempts allowed (Normal) | "Attempts left: 8" | "Attempts left: 7" (off by one) | none |

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic) as my AI assistant throughout this project — both for understanding the buggy logic and for generating the refactored code and test suite.

**Correct AI suggestion:** I asked Claude to explain why the hints were inverted. It correctly identified that `check_guess` had the messages swapped — `guess > secret` was labeled "Too High" but displayed "Go HIGHER!", which contradicts itself. Claude's fix (swap the hint strings so "Too High" maps to "Go LOWER!") was exactly right. I verified by running `pytest` and by manually tracing the condition: if my guess is bigger than the secret, I need to guess lower.

**Incorrect/misleading AI suggestion:** When I first asked about the secret-type bug, Claude initially suggested adding a type-check inside `check_guess` to handle both `int` and `str` secrets gracefully — essentially keeping the toggling logic and patching around it. That was misleading: it treated a symptom rather than eliminating the root cause. The actual fix was to remove the even/odd `str()` conversion entirely in `app.py` and always pass the integer secret to `check_guess`. I rejected the type-patch because it made the code more complex and left the intentional bug in place; instead I deleted the three lines that caused the toggle.

---

## 3. Debugging and testing your fixes

For each bug I followed a three-step verification loop: read the code to confirm where the fault was, apply the fix, then run `pytest` and manually trace an example in my head to make sure the logic was now correct.

For the inverted hints, the key test was `test_hint_message_too_high_says_lower` — it asserts that the message returned for a too-high guess contains the word "LOWER". Before the fix, that test failed; after the fix it passed. I also added `test_hint_message_too_low_says_higher` as a symmetric check.

For the secret-type bug, I traced attempt number 2: before the fix, `secret = str(50)` → `check_guess(50, "50")` triggered the `TypeError` branch, then compared `"50" > "50"` which is `False`, returning "Too Low" even for a correct guess. After removing the str-cast, `check_guess(50, 50)` hits the `guess == secret` branch and returns "Win" immediately. The test `test_winning_guess` confirms this.

Claude helped me design the edge-case tests (`test_parse_negative_number`, `test_parse_decimal_truncates`) by suggesting common boundary inputs. I verified each by reading the `parse_guess` implementation and confirming the expected return value matched the code path.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time a user interacts with the page — clicking a button, typing in a text box, or changing a select widget all trigger a full re-execution. Without `st.session_state`, any variable assigned at the top of the script would reset to its initial value on every rerun. `st.session_state` is a dictionary-like object that persists across these reruns, so values stored in it (like `secret`, `attempts`, and `score`) survive each interaction.

Think of it like this: the script is a recipe that gets read aloud from start to finish every time someone touches a control. `st.session_state` is a sticky note attached to the clipboard — it carries information from one reading to the next, so the cook doesn't have to start from scratch every time.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is marking suspected bug locations with `# FIXME:` before touching any code. Having a labeled "crime scene" made it easy to jump back to the exact line in a conversation with the AI and get focused help, rather than pasting the entire file and asking "what's wrong?"

Next time I work with AI on a debugging task, I would reject any suggestion that adds complexity to work around a bug rather than removing the cause. The type-patching suggestion for the secret-toggle bug was a red flag I should have spotted faster — if the AI's fix makes the code *longer*, it is probably masking the real problem.

This project changed how I read AI-generated code: I now assume there are intentional-looking mistakes embedded in plausible logic, and I read every condition and return value with the question "does this actually match what the name says it does?" AI tools can produce code that *looks* correct at a glance but embeds subtle inversions or type coercions that only surface at runtime.
