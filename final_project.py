import requests
from pydantic import BaseModel, RootModel, Field
from typing import Dict
import requests
from datetime import date
import pandas as pd
import sqlite3
import os

# Pydantic Models
class Observation(BaseModel):
    open: float = Field(alias="1. open")
    high: float = Field(alias="2. high")
    low: float = Field(alias="3. low")
    close: float = Field(alias="4. close")
    volume: int = Field(alias="5. volume")

class TimeSeries(RootModel[Dict[str, Observation]]):
    pass

class MetaDataIntraday(BaseModel):
    Information: str = Field(alias="1. Information")
    Symbol: str = Field(alias="2. Symbol")
    Last_Refreshed: str = Field(alias="3. Last Refreshed")
    Interval: str = Field(alias="4. Interval")
    Output_Size: str = Field(alias="5. Output Size")
    Time_Zone: str = Field(alias="6. Time Zone")

class ApiResponse(BaseModel):
    meta_data: MetaDataIntraday = Field(alias="Meta Data")
    time_series: TimeSeries = Field(alias="Time Series (5min)")


# Extract
api_key = "TTKOHGL05DM097G0"
companies = ["AAPL", "GOOG", "MSFT"]

for company in companies:
  response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={company}&interval=5min&apikey={api_key}").json()
  
  validated = ApiResponse.model_validate(response)
  df_from_api = pd.DataFrame(validated.time_series.model_dump()).T
  df_from_api.reset_index(inplace=True)
  df_from_api.rename(columns={"index": "date"}, inplace=True)

  df_from_api.to_json(f'./raw_data/{company}_{date.today()}.json')
  print(f"{company} - DONE")


# Transform and Load
def transform_load(file):
    # Reading json files
    df = pd.read_json(f"raw_data/{file}")

    # adding new columns
    df["daily_change_percentage"] = ((df["close"] - df["open"]) / df["open"]) * 100
    df["symbol"] = file.split("_")[0]

    # Changing timestamp to add it into sqlite database
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Changing order of the columns
    df = df[["symbol", "date", "open", "high", "low", "close", "volume", "daily_change_percentage"]]

    conn = sqlite3.connect("./db/stocks.db")
    cursor = conn.cursor()

    # Primary key is symbol and date to "Make sure no duplicate records are inserted for the same stock/date"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_daily_data (
            symbol TEXT NOT NULL,
            date DATE NOT NULL,
            open_price REAL,
            high_price REAL,
            low_price REAL,
            close_price REAL,
            volume INTEGER,
            daily_change_percentage REAL,
            extraction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (symbol, date)
        );
    """)

    sql_command = """
        INSERT OR IGNORE INTO stock_daily_data (symbol, date, open_price, high_price, low_price, close_price, volume, daily_change_percentage)
        VALUES (?,?,?,?,?,?,?,?) 
    """
    data_into_table = df.values.tolist()
    print(data_into_table)

    cursor.executemany(sql_command, data_into_table)

    conn.commit()
    conn.close()

    return df

for file in os.listdir("./raw_data"):
    transform_load(file)