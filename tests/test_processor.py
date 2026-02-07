import sys
import os
import pandas as pd
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../lambda'))

from processor import CarDataProcessor

@pytest.fixture
def raw_data():
    # Create in-memory test dataframe
    data = {
        'car_ID': [1, 2],
        'CarName': ['toyouta corolla', 'vokswagen golf'], # Contains TYPOS
        'Price': [10000, 20000],
        'doornumber': ['four', '2'],
        'carbody': ['sedan', 'hatchback'],
        'fueltype': ['gas', 'diesel'],
        'ownername': ['PII Data', 'PII Data'] # PII to be dropped
    }
    return pd.DataFrame(data)

def test_processor_cleaning(raw_data):
    # Initialize processor
    processor = CarDataProcessor(raw_data)
    
    # Execute preprocessing
    cleaned_df = processor.run_preprocessing()
    
    # 1. Test: Brand Typo Correction ('toyouta' -> 'toyota')
    assert cleaned_df.iloc[0]['brand'] == 'toyota'
    assert cleaned_df.iloc[1]['brand'] == 'volkswagen'
    
    # 2. Test: PII Column Removal
    assert 'ownername' not in cleaned_df.columns
    
    # 3. Test: Word-to-Number Conversion
    assert cleaned_df.iloc[0]['doornumber'] == 4
