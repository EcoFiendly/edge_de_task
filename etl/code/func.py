import requests
import pandas as pd
import warnings
import urllib.parse

warnings.simplefilter("ignore", category=UserWarning)

# extract.py
def extract(resource_name: str, postcode: str) -> pd.DataFrame:
    single_month_query = "SELECT YEAR_MONTH, PRACTICE_NAME, POSTCODE, "\
                         "CHEMICAL_SUBSTANCE_BNF_DESCR, BNF_DESCRIPTION, "\
                         "BNF_CHAPTER_PLUS_CODE, QUANTITY, ITEMS, TOTAL_QUANTITY, "\
                         "ADQUSAGE, NIC, ACTUAL_COST " \
                         f"FROM `{resource_name}` "\
                         f"WHERE postcode LIKE '{postcode}' "

    single_month_api_call = f"https://opendata.nhsbsa.net/api/3/action/"\
                            f"datastore_search_sql?"\
                            "resource_id="\
                            f"{resource_name}"\
                            "&"\
                            "sql="\
                            f"{urllib.parse.quote(single_month_query)}" # Encode spaces in the url

    single_month_resp = requests.get(single_month_api_call).json()
    if not single_month_resp["success"]:
        print("Error extracting the data, check queries and api call")
        return
    single_month_df = pd.json_normalize(single_month_resp['result']['result']['records'])
    return single_month_df

def create_sql_schema(conn) -> None:
    # Create the necessary tables in the SQLite database
    # sqlite does not have datetime dtype
    conn.execute('''
        CREATE TABLE IF NOT EXISTS DateDimension (
            YearMonth INTEGER PRIMARY KEY,
            Year INTEGER,
            Month INTEGER
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS PracticeDimension (
            Practice_Name TEXT PRIMARY KEY,
            Postcode TEXT
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ChemicalSubstanceDimension (
            Bnf_Description TEXT PRIMARY KEY,
            Chemical_Substance_Bnf_Descr TEXT,
            Bnf_Chapter_Plus_Code TEXT
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS MonthDataFact (
            YearMonth INTEGER,
            Practice_Name TEXT,
            Bnf_Description TEXT,
            Quantity REAL,
            Items INTEGER,
            Total_Quantity REAL,
            Adqusage REAL,
            Nic REAL,
            Actual_Cost REAL,
            FOREIGN KEY (YearMonth) REFERENCES DateDimension(YearMonth),
            FOREIGN KEY (Practice_Name) REFERENCES PracticeDimension(Practice_Name),
            FOREIGN KEY (Bnf_Description) REFERENCES ChemicalSubstanceDimension(Bnf_Description)
        )
    ''')

def transform(frame) -> dict[str, pd.DataFrame]:
    frame.columns = [x.title() for x in frame.columns]

    frame.rename(columns={"Year_Month": "YearMonth"}, inplace=True)
    # Create the Date dimension table
    date_dim = frame[['YearMonth']].drop_duplicates().reset_index(drop=True)
    date_dim['Year'] = date_dim['YearMonth'].astype(str).str[:4]
    date_dim['Month'] = date_dim['YearMonth'].astype(str).str[4:]
    
    # Create the Practice dimension table
    practice_dim = frame[['Practice_Name', 'Postcode']].drop_duplicates().reset_index(drop=True)
    
    # Create the Chemical dimension table
    chemical_dim = frame[["Bnf_Description", "Chemical_Substance_Bnf_Descr", "Bnf_Chapter_Plus_Code"]].drop_duplicates().reset_index(drop=True)
    
    # Insert records into the Medication fact table
    fact_table = frame[['YearMonth', 'Practice_Name', 'Bnf_Description',
                            'Quantity', 'Items', 'Total_Quantity', 'Adqusage', 'Nic', 'Actual_Cost']]
    fact_table.drop_duplicates().reset_index(drop=True, inplace=True)
    
    frames = {
        "date_dim": date_dim,
        "practice_dim": practice_dim,
        "chemical_dim": chemical_dim,
        "fact_table": fact_table
    }

    return frames

def load(frames: dict, conn) -> None:
    create_sql_schema(conn)

    frames["date_dim"].to_sql('DateDimension', conn, if_exists='append', index=False)

    frames["practice_dim"].to_sql('PracticeDimension', conn, if_exists='append', index=False)

    frames["chemical_dim"].to_sql('ChemicalSubstanceDimension', conn, if_exists='append', index=False)
    
    frames["fact_table"].to_sql('MonthDataFact', conn, if_exists='append', index=False)

    # Close the database connection
    conn.close()

