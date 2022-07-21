import pandas as pd


if __name__ == "__main__":
    df = pd.read_parquet("~/flask-webapp/Data-Exploration-Tool/data/flights/final/combined_flights.parquet")
    # print(df.head)
    print(df.index)
    # print(len(df.index))