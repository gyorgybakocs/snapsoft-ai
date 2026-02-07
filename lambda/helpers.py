# This helper module provides reusable logic for data cleaning that is 
# independent of the Pandas DataFrame structure, making it easier to 
# unit test without mocking large data structures.

from config import NUMERIC_MAPPING

def parse_word_to_number(value):
    """
    PURPOSE:
        Converts string-based numbers (e.g., "four") to actual integers (4).
    
    WHY:
        Input data often represents counts or dimensions as words. 
        Numerical representation is required for any statistical analysis 
        or machine learning feature engineering.

    TRADE-OFF:
        The function returns the original value if no mapping is found. 
        This prevents data loss for values that are already numeric or 
        unrecognized, but might require further cleaning if the input 
        contains unexpected noise.

    RISKS:
        If the 'NUMERIC_MAPPING' in config.py is incomplete, certain 
        string-based numbers will remain as strings, potentially causing 
        type errors in downstream mathematical operations.
    """
    if not isinstance(value, str):
        return value
        
    lower_val = value.lower().strip()
    return NUMERIC_MAPPING.get(lower_val, value)
