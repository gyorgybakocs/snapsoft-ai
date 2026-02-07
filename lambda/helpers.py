from config import NUMERIC_MAPPING

def parse_word_to_number(value):
    if not isinstance(value, str):
        return value
        
    lower_val = value.lower().strip()
    return NUMERIC_MAPPING.get(lower_val, value)
