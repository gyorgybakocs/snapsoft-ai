# The choice of a centralized config module ensures consistency across the 
# ingestion pipeline and allows for quick adjustments to PII handling without 
# modifying core processing logic.

# PURPOSE:
#   Define fields to be removed to ensure the curated dataset is compliant 
#   with privacy standards and free from non-predictive noise.
# WHY:
#   'car_ID' is a database artifact, while 'ownername', 'owneremail', and 
#   'dealershipaddress' contain sensitive PII not required for ML modeling.
COLUMNS_TO_DROP = [
    'car_ID', 
    'ownername', 
    'owneremail', 
    'dealershipaddress', 
    'iban', 
    'saledate'
]

# PURPOSE:
#   Identify columns that must contain data for a record to be considered valid.
# WHY:
#   Records missing 'Price' or core categorical data (body, fuel) cannot 
#   be used for training or accurate analysis, so they are dropped early.
CRITICAL_ATTRIBUTES = [
    'Price',
    'carbody',
    'fueltype'
]

# PURPOSE:
#   Map known variations and typos in manufacturer names to a canonical form.
# WHY:
#   The source data is often manual entry or sourced from legacy systems with 
#   inconsistent naming (e.g., 'vw' vs 'volkswagen'). Normalization is 
#   required for correct categorical grouping in downstream models.
BRAND_CORRECTION = {
    'maxda': 'mazda', 
    'porcshce': 'porsche', 
    'toyouta': 'toyota', 
    'vokswagen': 'volkswagen', 
    'vw': 'volkswagen', 
    'alfa-romero': 'alfa-romeo'
}

# PURPOSE:
#   Provide a translation layer for alphanumeric representations of integers.
# WHY:
#   Certain features (like door numbers) may arrive as strings ('four'). 
#   Converting these to numeric types is essential for mathematical 
#   operations and model compatibility.
NUMERIC_MAPPING = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5, 
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12
}
