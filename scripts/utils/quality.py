
import pandas as pd


def fill_if_empty(df, column, values, source_name=None):

    if column not in df.columns:
        df[column] = None

    mask = df[column].isna() | (df[column].astype(str).str.strip() == "")

    df.loc[mask, column] = values[mask]

    if source_name:
        src = f"{column}_source"
        conf = f"{column}_confidence"

        if src not in df.columns:
            df[src] = None

        if conf not in df.columns:
            df[conf] = None

        df.loc[mask, src] = source_name
        df.loc[mask, conf] = 1.0

    return df
