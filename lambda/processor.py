# This class centralizes the data transformation logic. 
# By encapsulating these steps, we ensure that the same cleaning rules 
# can be applied in both the production Lambda environment and during 
# local development or testing.

import pandas as pd
from config import COLUMNS_TO_DROP, CRITICAL_ATTRIBUTES, BRAND_CORRECTION
from helpers import parse_word_to_number

class CarDataProcessor:
    """
    PURPOSE:
        Encapsulate all car-related data cleaning and normalization logic.
    
    WHY:
        Data originating from S3 landing zones is often "raw" and contains 
        typos, missing values, or PII. This processor transforms it into 
        a "curated" format ready for ML consumption.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def run_preprocessing(self) -> pd.DataFrame:
        """
        PURPOSE:
            Execute the full pipeline of cleaning steps in a specific order.
        
        WHY:
            Ordering matters: e.g., we must drop invalid records before 
            attempting to normalize brand names to avoid processing nulls.
        """
        self._drop_non_ml_features()
        self._filter_invalid_records()
        self._normalize_brand_names()
        self._convert_numeric_strings()
        return self.df

    def _drop_non_ml_features(self):
        """
        PURPOSE:
            Remove columns that are irrelevant for modeling or contain PII.
        
        WHY:
            Reducing the feature set decreases memory usage and prevents 
            the model from over-fitting on noise like 'car_ID'.
        """
        self.df = self.df.drop(columns=[c for c in COLUMNS_TO_DROP if c in self.df.columns])

    def _filter_invalid_records(self):
        """
        PURPOSE:
            Remove rows missing essential data.
        
        WHY:
            Models cannot reliably learn from records where the target variable 
            (Price) or primary categories are missing.
        """
        self.df = self.df.dropna(subset=[c for c in CRITICAL_ATTRIBUTES if c in self.df.columns])

    def _normalize_brand_names(self):
        """
        PURPOSE:
            Extract and fix the car brand from the 'CarName' string.
        
        WHY:
            'CarName' usually includes the model (e.g., "toyota corolla"). 
            We only need the brand for high-level categorization, and 
            we must correct frequent manual entry typos (e.g., "maxda").
        """
        if 'CarName' in self.df.columns:
            # Splits the string and takes the first word as the brand.
            self.df['brand'] = self.df['CarName'].str.split(' ').str[0].str.lower().replace(BRAND_CORRECTION)
            # Records without a valid brand extraction are useless for this analysis.
            self.df = self.df.dropna(subset=['brand']).drop(columns=['CarName'])

    def _convert_numeric_strings(self):
        """
        PURPOSE:
            Iterate through object columns to find and convert word-based numbers.
        
        WHY:
            Ensures columns like 'doornumber' or 'cylindernumber' are 
            strictly numeric for the ML pipeline.
        """
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            self.df[col] = self.df[col].apply(parse_word_to_number)
