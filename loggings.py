import polars as pl
import os

def save_logging_errors(logs_df, path):
    try:
        logs_df.write_csv(path)
        print(f"Saved LOG info to {path}")
    except Exception as e:
        print(f"Error saving LOG CSV: {e}")

def create_logging_errors(name, path):
    log_path = os.path.join(path, name)
    if os.path.exists(log_path):
        logs_df = pl.read_csv(log_path)
        # Ensure consistent schema
        logs_df = logs_df.with_columns([
            pl.col("name").cast(pl.Utf8)
        ])
    else:
        # Initialize empty DataFrame with proper schema
        logs_df = pl.DataFrame(schema={'name': pl.Utf8})
        if not os.path.exists(path):
            os.mkdir(path)
        save_logging_errors(logs_df, log_path)
    
    return logs_df
      
if __name__ == "__main__":
    # Test the function
    loggin_df = create_logging_errors("logging_errors", os.path.join(os.getcwd(), "logs"))
