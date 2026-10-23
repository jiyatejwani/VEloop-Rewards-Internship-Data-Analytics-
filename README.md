# Analysis scripts

Python (pandas) scripts that produce the project's data findings. All input data is **simulated / fictional**.

## Setup
```bash
pip install -r requirements.txt
# place the two supplied workbooks in ./data/
#   VELOOP_Simulated_User_Behavior_1000.xlsx
#   VELoop_Rewards_Data_01.xlsx
```

## Scripts
| Script | What it does | Reproduces |
|---|---|---|
| `01_profile_datasets.py` | Record counts, nulls, duplicates, date ranges, referential-integrity tests, and the cross-file user-identity check | Deliverable #12 |
| `02_data_quality_audit.py` | Detects duplicate IDs, malformed dates, casing inconsistencies, impossible values | Deliverable #13 |
| `03_build_dashboard_data.py` | Aggregates the computable metrics and writes `../data.js` for the dashboard | Deliverable #14 |

```bash
python 01_profile_datasets.py
python 02_data_quality_audit.py
python 03_build_dashboard_data.py      # regenerates ../data.js
```

The SQL definitions for the KPIs are in [`../sql/kpi_queries.sql`](../sql/kpi_queries.sql).
