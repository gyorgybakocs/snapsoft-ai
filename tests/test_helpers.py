import sys
import os
# Hozzáadjuk a lambda mappát az elérési úthoz, hogy importálni tudjuk
sys.path.append(os.path.join(os.path.dirname(__file__), '../lambda'))

from helpers import parse_word_to_number

def test_parse_word_to_number():
    # Happy path
    assert parse_word_to_number("four") == 4
    assert parse_word_to_number("One") == 1  # Nagybetű kezelése
    
    # Edge cases (ami nem változik)
    assert parse_word_to_number("100") == "100"
    assert parse_word_to_number(None) is None
