import pandas as pd
from config import COLUMNS_TO_DROP, CRITICAL_ATTRIBUTES, BRAND_CORRECTION
from helpers import parse_word_to_number

class CarDataProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def run_preprocessing(self) -> pd.DataFrame:
        self._drop_non_ml_features()
        self._filter_invalid_records()
        self._normalize_brand_names()
        self._convert_numeric_strings()
        return self.df

    def _drop_non_ml_features(self):
        self.df = self.df.drop(columns=[c for c in COLUMNS_TO_DROP if c in self.df.columns])

    def _filter_invalid_records(self):
        self.df = self.df.dropna(subset=[c for c in CRITICAL_ATTRIBUTES if c in self.df.columns])

    def _normalize_brand_names(self):
        if 'CarName' in self.df.columns:
            # Extract brand (first word) and fix typos
            self.df['brand'] = self.df['CarName'].str.split(' ').str[0].str.lower().replace(BRAND_CORRECTION)
            self.df = self.df.dropna(subset=['brand']).drop(columns=['CarName'])

    def _convert_numeric_strings(self):
        string_cols = self.df.select_dtypes(include=['object']).columns
        for col in string_cols:
            self.df[col] = self.df[col].apply(parse_word_to_number)
