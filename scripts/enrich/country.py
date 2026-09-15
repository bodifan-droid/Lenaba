
import pandas as pd

COUNTRY_MAP = {
    "Ukrainian": "Ukraine",
    "English": "United Kingdom",
    "Scottish": "Scotland",
    "Irish": "Ireland",
    "Welsh": "Wales",
    "French": "France",
    "German": "Germany",
    "Spanish": "Spain",
    "Italian": "Italy",
    "Portuguese": "Portugal",
    "Dutch": "Netherlands",
    "Greek": "Greece",
    "Hebrew": "Israel",
    "Arabic": "Saudi Arabia",
    "Persian": "Iran",
    "Turkish": "Türkiye",
    "Japanese": "Japan",
    "Chinese": "China",
    "Korean": "South Korea",
    "Hindi": "India",
    "Sanskrit": "India",
    "Russian": "Russia",
    "Polish": "Poland",
    "Czech": "Czech Republic",
    "Slovak": "Slovakia",
    "Croatian": "Croatia",
    "Serbian": "Serbia",
    "Bosnian": "Bosnia and Herzegovina",
    "Icelandic": "Iceland",
    "Norwegian": "Norway",
    "Swedish": "Sweden",
    "Finnish": "Finland",
}


def enrich_country(df: pd.DataFrame):

    print("Country...")

    if "country" not in df.columns:
        df["country"] = None

    if "language" not in df.columns:
        return df

    before = df["country"].isna().sum()

    mask = (
        df["country"].isna()
        & df["language"].notna()
    )

    df.loc[mask, "country"] = (
        df.loc[mask, "language"]
        .map(COUNTRY_MAP)
    )

    after = df["country"].isna().sum()

    print(f"  Filled: {before-after:,}")

    return df
