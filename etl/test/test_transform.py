import pandas as pd
from code.func import transform

def test_transform(mock_extract_data):
    frames = transform(mock_extract_data)
    expected = {
        "date_dim": pd.DataFrame(
            {
                "YearMonth": [201901],
                "Year": ["2019"],
                "Month": ["01"],
            }
        ),
        "practice_dim": pd.DataFrame(
            {
                "Practice_Name": ["BALHAM PARK SURGERY"],
                "Postcode": ["SW17 7AW"]
            }
        ),
        "chemical_dim": pd.DataFrame(
            {
                "Bnf_Description": ["Lidocaine 5% medicated plasters"],
                "Chemical_Substance_Bnf_Descr": ["Lidocaine hydrochloride"],
                "Bnf_Chapter_Plus_Code": ["15: Anaesthesia"]
            }
        ),
        "fact_table": pd.DataFrame(
            {
                "YearMonth": [201901],
                "Practice_Name": ["BALHAM PARK SURGERY"],
                "Bnf_Description": ["Lidocaine 5% medicated plasters"],
                "Quantity": [30.0],
                "Items": [5],
                "Total_Quantity": [150.0],
                "Adqusage": [0.0],
                "Nic": [362.0],
                "Actual_Cost": [336.05147]
            }
        ),
    }
    for key in frames.keys():
        pd.testing.assert_frame_equal(frames[key], expected[key])