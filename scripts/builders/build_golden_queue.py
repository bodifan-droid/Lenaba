from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

MASTER = ROOT / "data" / "enriched" / "names_enriched.csv"
SEED = ROOT / "data" / "seed" / "knowledge_seed.csv"
OUTPUT = ROOT / "data" / "seed" / "golden_500.csv"

master = pd.read_csv(MASTER)
seed = pd.read_csv(SEED)

# Робимо копію
master = master.copy()

# Усі seed-імена отримують найвищий пріоритет
seed_names = set(seed["name"].str.lower())
master["is_seed"] = master["name"].str.lower().isin(seed_names)

# Якщо є popularity_score — використовуємо його
sort_columns = ["is_seed"]
ascending = [False]

if "popularity_score" in master.columns:
    sort_columns.append("popularity_score")
    ascending.append(False)

sort_columns.append("name")
ascending.append(True)

golden = (
    master
    .sort_values(sort_columns, ascending=ascending)
    .drop_duplicates(subset=["name"])
    .head(500)
    .copy()
)

golden["priority"] = range(1, len(golden) + 1)

# Country може бути відсутнім
if "country" not in golden.columns:
    golden["country"] = ""

# Статус знадобиться для пайплайна
golden["status"] = "pending"

golden = golden[["priority", "name", "gender", "country", "status"]]

golden.to_csv(OUTPUT, index=False)

print(f"✓ Created {OUTPUT}")
print(f"✓ Rows: {len(golden)}")
print(f"✓ Seed names prioritized: {golden['name'].str.lower().isin(seed_names).sum()}")