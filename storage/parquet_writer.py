# Parquet writer
import pandas as pd


def write_parquet(records, path):
    df = pd.DataFrame(records)
    df.to_parquet(
        path,
        engine="pyarrow",
        compression="snappy"
    )
