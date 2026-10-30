import io
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://{os.environ['PG_USER']}:{os.environ['PG_PASSWORD']}"
    f"@{os.environ['PG_HOST']}:{os.environ['PG_PORT']}/{os.environ['PG_DATABASE']}"
)
RAW_DIR = Path("data/raw")
MONTH = "2026-07"

engine = create_engine(DB_URL)


def copy_df(conn, df, table):
    buf = io.StringIO()
    df.to_csv(buf, index=False, header=False)
    buf.seek(0)
    cols = ", ".join(f'"{c}"' for c in df.columns)
    cur = conn.connection.cursor()
    cur.copy_expert(f"COPY raw.{table} ({cols}) FROM STDIN WITH (FORMAT csv)", buf)


def load_lookup(conn, name):
    df = pd.read_parquet(RAW_DIR / f"{name}.parquet")
    df.head(0).to_sql(name, conn, schema="raw", if_exists="replace", index=False)
    copy_df(conn, df, name)
    print(f"loaded raw.{name}: {len(df)} rows")


def load_prices(conn, month):
    df = pd.read_parquet(RAW_DIR / f"pricecatcher_{month}.parquet")
    df["source_month"] = month
    df.head(0).to_sql("pricecatcher", conn, schema="raw", if_exists="append", index=False)
    conn.execute(text("DELETE FROM raw.pricecatcher WHERE source_month = :m"), {"m": month})
    copy_df(conn, df, "pricecatcher")
    print(f"loaded raw.pricecatcher for {month}: {len(df)} rows")


with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    load_lookup(conn, "lookup_item")
    load_lookup(conn, "lookup_premise")
    load_prices(conn, MONTH)