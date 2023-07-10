import pytest
import pandas as pd

@pytest.fixture
def mock_extract_data():
    return pd.DataFrame(
        {
            "YEAR_MONTH": [201901],
            "PRACTICE_NAME": ["BALHAM PARK SURGERY"],
            "POSTCODE": ["SW17 7AW"],
            "CHEMICAL_SUBSTANCE_BNF_DESCR": ["Lidocaine hydrochloride"],
            "BNF_DESCRIPTION": ["Lidocaine 5% medicated plasters"],
            "BNF_CHAPTER_PLUS_CODE": ["15: Anaesthesia"],
            "QUANTITY": [30.0],
            "ITEMS": [5],
            "TOTAL_QUANTITY": [150.0],
            "ADQUSAGE": [0.0],
            "NIC": [362.00],
            "ACTUAL_COST": [336.05147]
        }
    )