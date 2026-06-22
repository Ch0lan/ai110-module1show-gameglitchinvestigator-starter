# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Bugs Found and Fixed

| Bug | Root Cause | Fix Applied |
|-----|-----------|-------------|
| Inverted hints ("Go HIGHER!" when guess was too high) | `check_guess` had the hint strings swapped — `guess > secret` printed "Go HIGHER!" | Swapped messages so "Too High" → "Go LOWER!" and "Too Low" → "Go HIGHER!" |
| Secret alternated between `int` and `str` | `app.py` cast `secret` to `str` on even attempts, causing string/numeric comparison mismatch | Removed the `str()` conversion; secret is always passed as `int` to `check_guess` |
| Hard difficulty easier than Normal | Hard used range 1–50 (smaller = easier), Normal used 1–100 | Changed Hard range to 1–200 |
| Attempts counter off by one on first render | `st.session_state.attempts` initialized to `1` instead of `0` | Changed initialization to `0` |
| `logic_utils.py` raised `NotImplementedError` | Functions were stubs, never refactored from `app.py` | Moved all four logic functions into `logic_utils.py`; `app.py` now imports from it |

## 📝 Document Your Experience

The game is a number-guessing game where you try to find a secret number within a limited number of attempts. Each wrong guess costs 5 points; a correct guess awards up to 90 points (decreasing by 10 per attempt, floored at 10). Three difficulty levels change the number range and attempt limit.

The bugs above made the game unwinnable: inverted hints sent players in the wrong direction, and the secret-type toggle corrupted comparisons every other turn. After the fixes, hints are correct, comparisons are always numeric, and Hard is genuinely harder than Normal.

## 📸 Demo Walkthrough

1. Launch the app with `python -m streamlit run app.py`. The sidebar shows "Normal" difficulty with range 1–100 and 8 attempts.
2. User enters a guess of **40**. The game returns "📉 Go LOWER!" — the secret is below 40.
3. User enters a guess of **20**. The game returns "📈 Go HIGHER!" — the secret is above 20.
4. User enters a guess of **30**. The game returns "📉 Go LOWER!" — secret is between 20 and 29.
5. User enters a guess of **25**. The game returns "🎉 Correct!" — balloons appear, score is displayed, and the game stops accepting further guesses until "New Game" is clicked.
6. Score updates correctly each turn: each wrong guess deducts 5 points; the win awards points proportional to how few attempts were used.

## 🧪 Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/mukunth/ai110-module1show-gameglitchinvestigator-starter
collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests/test_game_logic.py::test_hint_message_too_high_says_lower PASSED   [ 28%]
tests/test_game_logic.py::test_hint_message_too_low_says_higher PASSED   [ 35%]
tests/test_game_logic.py::test_parse_valid_integer PASSED                [ 42%]
tests/test_game_logic.py::test_parse_empty_string PASSED                 [ 50%]
tests/test_game_logic.py::test_parse_non_numeric PASSED                  [ 57%]
tests/test_game_logic.py::test_parse_decimal_truncates PASSED            [ 64%]
tests/test_game_logic.py::test_parse_negative_number PASSED              [ 71%]
tests/test_game_logic.py::test_parse_very_large_number PASSED            [ 78%]
tests/test_game_logic.py::test_win_score_increases PASSED                [ 85%]
tests/test_game_logic.py::test_wrong_guess_decreases_score PASSED        [ 92%]
tests/test_game_logic.py::test_score_floors_at_ten_for_late_win PASSED   [100%]

============================== 14 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
