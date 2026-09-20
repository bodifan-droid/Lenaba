# Lenaba Playbook

> Internal operating guide for Sprint 9+

## Daily Startup

Activate environment:

```powershell
.venv\Scripts\Activate.ps1
```

Run enrichment:

```powershell
python scripts/enrich_database.py
```

Run Queue Platform:

```powershell
python scripts/executors/queue_sync.py
python scripts/executors/queue_orchestrator.py
```

Check Fetch Doctor:

```powershell
python scripts/executors/fetch_doctor.py NAME
```

## Coverage

After enrichment always verify:

* Origin
* Meaning
* Language
* Country
* IPA
* Duplicate Slugs

## Adding a New Executor

1. Create inside `scripts/executors/`
2. Use shared normalization
3. Update DATA_SCHEMA if needed
4. Add to CHANGELOG
5. Run smoke test

## Release Checklist

* Coverage checked
* DATA_SCHEMA updated
* Changelog updated
* Roadmap updated
* Decisions updated
* Git tag created


## Large Family Run

Run:

```bash
python scripts/executors/fetch_behind_v2.py --limit 100
```

Features:

- automatic checkpoint
- resume support
- ETA calculator
- Run Summary
- Missing BTN collector
- completed-family skipping
