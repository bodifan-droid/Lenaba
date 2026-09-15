import pandas as pd

REQUIRED = [
    "name",
    "gender",
    "origin",
    "meaning",
    "language",
    "country",
    "slug",
    "ipa",
    "tags",
]


def validate_database(df: pd.DataFrame):

    print("Validation...")

    total = len(df)

    lines = []
    lines.append("=" * 32)
    lines.append("COVERAGE REPORT")
    lines.append("=" * 32)
    lines.append(f"Total names: {total:,}")
    lines.append("")

    for col in REQUIRED:

        if col not in df.columns:
            lines.append(f"{col:<12} MISSING COLUMN")
            continue

        series = df[col]

        if series.dtype == "object":
            missing = (
                series.isna()
                | (series.astype(str).str.strip() == "")
            ).sum()
        else:
            missing = series.isna().sum()

        filled = total - missing
        pct = filled / total * 100

        lines.append(
            f"{col:<12} {filled:>6,}/{total:,} ({pct:5.1f}%)"
        )

    dup = df["slug"].duplicated().sum()

    lines.append("")
    lines.append(f"Duplicate slugs: {dup:,}")

    return "\n".join(lines)
