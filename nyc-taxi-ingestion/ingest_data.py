import argparse
import os
import pandas as pd
from sqlalchemy import create_engine

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5433"))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_NAME = os.getenv("DB_NAME", "ny_taxi")


def ingest_file(url: str, table_name: str):
    print(f"Downloading {url}")

    if url.endswith(".parquet"):
        df = pd.read_parquet(url)
    elif url.endswith(".csv"):
        df = pd.read_csv(url)
    else:
        raise ValueError("Unsupported file type")

    print("Connecting to Postgres...")
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print(f"Ingesting into table: {table_name}")
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print("Done.")


def parse_args():
    parser = argparse.ArgumentParser(description="Ingest dataset into Postgres")
    parser.add_argument("--url", required=True)
    parser.add_argument("--table", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ingest_file(url=args.url, table_name=args.table)
