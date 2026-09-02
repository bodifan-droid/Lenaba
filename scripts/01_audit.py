
from pathlib import Path
import pandas as pd

from lib.validation import quality_metrics, gender_counts, missing_values
from lib.reports import timestamp

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "all-names.csv"
REPORT = ROOT / "data" / "reports" / "audit_report.html"

df = pd.read_csv(RAW)

# Тимчасово перейменовуємо для єдиного стандарту
df = df.rename(columns={"sex": "gender"})

quality = quality_metrics(df)
gender = gender_counts(df)
missing = missing_values(df)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Lenaba Audit Report</title>
<style>
body {{
font-family: Arial,sans-serif;
background:#F8F6F3;
padding:40px;
color:#1F2937;
}}
.card {{
background:white;
padding:20px;
margin-bottom:20px;
border-radius:18px;
box-shadow:0 4px 20px rgba(0,0,0,.06);
}}
table {{
width:100%;
border-collapse:collapse;
}}
td,th {{
padding:10px;
border-bottom:1px solid #eee;
}}
</style>
</head>
<body>

<h1>Lenaba Data Audit</h1>
<p>{timestamp()}</p>

<div class="card">
<h2>Overview</h2>
<table>
<tr><td>Rows</td><td>{quality["rows"]:,}</td></tr>
<tr><td>Columns</td><td>{quality["columns"]}</td></tr>
<tr><td>Female</td><td>{gender.get("Female",0):,}</td></tr>
<tr><td>Male</td><td>{gender.get("Male",0):,}</td></tr>
</table>
</div>

<div class="card">
<h2>Quality</h2>
<table>
<tr><td>Exact duplicates</td><td>{quality["exact_duplicates"]}</td></tr>
<tr><td>Leading spaces</td><td>{quality["leading_spaces"]}</td></tr>
<tr><td>First-letter mismatches</td><td>{quality["first_letter_errors"]}</td></tr>
</table>
</div>

<div class="card">
<h2>Missing Values</h2>
<table>
<tr><th>Field</th><th>Missing</th></tr>
{"".join(f"<tr><td>{k}</td><td>{v:,}</td></tr>" for k,v in missing.items())}
</table>
</div>

</body>
</html>
"""

REPORT.write_text(html, encoding="utf-8")

print("Audit complete.")
print(REPORT)