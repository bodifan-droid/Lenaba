
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

EXTENSIONS = {".parquet", ".csv"}


def inspect_file(path: Path):
    print("=" * 80)
    print(path.relative_to(ROOT))
    print("=" * 80)

    try:
        if path.suffix == ".parquet":
            df = pd.read_parquet(path)
        else:
            df = pd.read_csv(path)

        print(f"Rows: {len(df):,}")
        print(f"Columns ({len(df.columns)}):")
        print(df.columns.tolist())
        print("\nDtypes:")
        print(df.dtypes.to_string())
        print("\nSample:")
        print(df.head(5).to_string())

    except Exception as e:
        print("ERROR:", e)

    print()


def main():
    files = sorted(
        p for p in DATA.rglob("*")
        if p.suffix in EXTENSIONS
    )

    print(f"Found {len(files)} data files.\n")

    for f in files:
        inspect_file(f)


if __name__ == "__main__":
    main()
