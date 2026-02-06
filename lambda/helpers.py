from config import NUMERIC_MAPPING

def parse_word_to_number(value):
    """
    Converts string-based numbers to integers using config.NUMERIC_MAPPING.
    Returns original value if it's already a number or not in the map.
    """
    if not isinstance(value, str):
        return value
        
    lower_val = value.lower().strip()
    return NUMERIC_MAPPING.get(lower_val, value)
