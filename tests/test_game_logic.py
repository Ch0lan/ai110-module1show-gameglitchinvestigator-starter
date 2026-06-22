import pytest
from logic_utils import check_guess, parse_guess, update_score


# --- check_guess ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # Guess of 60 against secret 50 should say Too High (go lower)
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # Guess of 40 against secret 50 should say Too Low (go higher)
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_message_too_high_says_lower():
    # The message for Too High must tell the player to go LOWER, not higher
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_hint_message_too_low_says_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- parse_guess ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False

def test_parse_decimal_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok is True
    assert value == 7

def test_parse_negative_number():
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5

def test_parse_very_large_number():
    ok, value, err = parse_guess("999999")
    assert ok is True
    assert value == 999999


# --- update_score ---

def test_win_score_increases():
    new_score = update_score(0, "Win", 1)
    assert new_score > 0

def test_wrong_guess_decreases_score():
    new_score = update_score(50, "Too High", 1)
    assert new_score < 50

def test_score_floors_at_ten_for_late_win():
    # Many attempts in — points should floor at 10, not go negative
    new_score = update_score(0, "Win", 20)
    assert new_score >= 10
