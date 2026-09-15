
import pandas as pd
from slugify import slugify


def enrich_slug(df: pd.DataFrame):

    print("Slug...")

    if "slug" not in df.columns:
        df["slug"] = None

    for i, name in df["name"].items():

        if pd.isna(df.at[i, "slug"]) or df.at[i, "slug"] == "":

            df.at[i, "slug"] = slugify(str(name))

    return df
