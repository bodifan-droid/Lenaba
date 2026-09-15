from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
OUT = DOCS / "DATA_SCHEMA.md"

EXTENSIONS = {".parquet", ".csv"}

PRIMARY_KEY_CANDIDATES = [
    "name",
    "name_id",
    "slug",
    "family_id",
    "alias",
    "canonical_name",
]


def read_table(path: Path):
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def detect_primary_key(df):
    for col in PRIMARY_KEY_CANDIDATES:
        if col in df.columns:
            return col
    return "Unknown"


def md_table(df, rows=5):
    sample = df.head(rows).fillna("")

    headers = list(sample.columns)

    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for _, row in sample.iterrows():
        values = [str(v).replace("\n", " ") for v in row]
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)


def main():

    DOCS.mkdir(exist_ok=True)

    files = sorted(
        p for p in DATA.rglob("*")
        if p.suffix in EXTENSIONS
    )

    lines = []

    lines.append("# Lenaba Data Schema")
    lines.append("")
    lines.append("> Auto-generated. Do not edit manually.")
    lines.append("")
    lines.append(f"Files scanned: **{len(files)}**")
    lines.append("")

    summary = []

    details = []

    for path in files:

        try:
            df = read_table(path)

            pk = detect_primary_key(df)

            summary.append(
                (
                    path.relative_to(ROOT).as_posix(),
                    len(df),
                    len(df.columns),
                    pk,
                )
            )

            details.append(f"## {path.relative_to(ROOT).as_posix()}")
            details.append("")
            details.append(f"- **Rows:** {len(df):,}")
            details.append(f"- **Columns:** {len(df.columns)}")
            details.append(f"- **Primary key:** `{pk}`")
            details.append("")

            details.append("### Columns")
            details.append("")
            details.append("| Column | Type |")
            details.append("|---|---|")

            for col, dtype in df.dtypes.items():
                details.append(f"| `{col}` | `{dtype}` |")

            details.append("")
            details.append("### Sample")
            details.append("")
            details.append(md_table(df))
            details.append("")
            details.append("---")
            details.append("")

        except Exception as e:

            summary.append(
                (
                    path.relative_to(ROOT).as_posix(),
                    "ERROR",
                    "-",
                    "-",
                )
            )

            details.append(f"## {path.relative_to(ROOT).as_posix()}")
            details.append("")
            details.append(f"**Error:** `{e}`")
            details.append("")
            details.append("---")
            details.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| File | Rows | Columns | Primary key |")
    lines.append("|---|---:|---:|---|")

    for file, rows, cols, pk in summary:
        lines.append(f"| `{file}` | {rows} | {cols} | `{pk}` |")

    lines.append("")
    lines.extend(details)

    OUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Generated: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
