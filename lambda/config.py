# Attributes to be dropped (PII and non-predictive data)
COLUMNS_TO_DROP = [
    'car_ID', 
    'ownername', 
    'owneremail', 
    'dealershipaddress', 
    'iban', 
    'saledate'
]

# Critical attributes for row filtering
CRITICAL_ATTRIBUTES = [
    'Price',
    'carbody',
    'fueltype'
]

# Correction map for common brand typos
BRAND_CORRECTION = {
    'maxda': 'mazda', 
    'porcshce': 'porsche', 
    'toyouta': 'toyota', 
    'vokswagen': 'volkswagen', 
    'vw': 'volkswagen', 
    'alfa-romero': 'alfa-romeo'
}

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
