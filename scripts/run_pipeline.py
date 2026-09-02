
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("Data Audit", "01_audit.py"),
    ("Data Clean", "02_clean.py"),
    ("Normalization", "02b_normalize.py"),
]

EXPECTED = [
    ROOT / "data" / "reports" / "audit_report.html",
    ROOT / "data" / "cleaned" / "names_cleaned.parquet",
    ROOT / "data" / "cleaned" / "names.parquet",
    ROOT / "data" / "cleaned" / "name_variants.parquet",
    ROOT / "data" / "cleaned" / "phonetics.parquet",
    ROOT / "data" / "cleaned" / "name_stats.parquet",
]


def run_step(title, script):
    print(f"\n{'='*50}")
    print(f"Running: {title}")
    print(f"{'='*50}")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script)],
        cwd=ROOT
    )

    if result.returncode != 0:
        print(f"\n❌ Pipeline stopped on: {script}")
        sys.exit(result.returncode)

    print(f"✅ {title} completed.")


def verify_outputs():
    print("\nVerifying outputs...")

    missing = []

    for file in EXPECTED:
        if not file.exists():
            missing.append(file)

    if missing:
        print("\n❌ Missing files:")
        for file in missing:
            print("-", file)
        sys.exit(1)

    print("✅ All expected files exist.")


def main():
    start = time.time()

    print("🚀 Lenaba Build Dataset v0.1")

    for title, script in STEPS:
        run_step(title, script)

    verify_outputs()

    elapsed = round(time.time() - start, 2)

    print(f"\n{'='*50}")
    print("🎉 PIPELINE COMPLETED")
    print(f"{'='*50}")
    print(f"Time: {elapsed} sec")
    print("Status: SUCCESS")
    print("Output: data/cleaned/")
    print("Report: data/reports/audit_report.html")


if __name__ == "__main__":
    main()