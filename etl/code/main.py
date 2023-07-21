from func import extract, transform, load
import sqlite3

resource_name = 'EPD_201901' # For EPD resources are named EPD_YYYYMM
postcode = '%SW17%'
# Create a connection to the SQLite database
conn = sqlite3.connect('sqlite/transformed_data.db')

def run_etl(resource_name: str, postcode: str, conn):
    raw_df = extract(resource_name, postcode)
    frames = transform(raw_df)
    load(frames, conn)

if __name__ == "__main__":
    run_etl(resource_name, postcode, conn)