import polars as pl
import os

def save_logging_errors(logs_df, path):
    try:
        logs_df.write_csv(path)
        print(f"Saved LOG info to {path}")
    except Exception as e:
        print(f"Error saving LOG CSV: {e}")

