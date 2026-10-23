"""
02_data_quality_audit.py - Detects the injected data-quality problems.

Reproduces Deliverable #13 (Data Quality Audit). The two "*_Audit" sheets
contain deliberate issues; this script finds and quantifies them:
  - duplicate primary keys (users, events)
  - malformed / unparseable dates
  - inconsistent capitalisation in a categorical field
  - impossible values (negative days-since-registration)

Usage:
    python 02_data_quality_audit.py [data_dir]

NOTE: all data is SIMULATED / FICTIONAL.
"""
import sys
from pathlib import Path
import pandas as pd

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "data"
F1 = DATA / "VELoop_Rewards_Data_01.xlsx"
F2 = DATA / "VELOOP_Simulated_User_Behavior_1000.xlsx"


def main():
    messy = pd.read_excel(F1, "Users_Messy_Audit")
    clean = pd.read_excel(F1, "Users_1000_Clean")
    events_clean = pd.read_excel(F2, "03_Feature_Events")
    events_audit = pd.read_excel(F2, "10_Event_Data_Quality_Audit")

    print("=== VELOOP Data Quality Audit (simulated) ===\n")

    # 1. Duplicate user IDs
    dup_users = messy.loc[messy["user_id"].duplicated(keep=False), "user_id"].unique()
    print(f"[High]   Duplicate user_id in Users_Messy_Audit: "
          f"{len(dup_users)} ids / {messy['user_id'].duplicated(keep=False).sum()} rows")
    print(f"         {sorted(dup_users)}")

    # 2. Duplicate event IDs
    dup_ev = events_audit.loc[events_audit["event_id"].duplicated(keep=False), "event_id"].unique()
    print(f"[High]   Duplicate event_id in Event_DQ_Audit: {len(dup_ev)} ids / "
          f"{events_audit['event_id'].duplicated(keep=False).sum()} rows")

    # 3. Malformed dates
    rd = messy["registration_datetime"]
    bad = rd[pd.to_datetime(rd, errors="coerce").isna() & rd.notna()]
    print(f"[High]   Malformed registration_datetime: {len(bad)} -> {list(bad.astype(str).unique())}")

    # 4. Inconsistent capitalisation (feature_name not in the canonical set)
    canon = set(events_clean["feature_name"].dropna().unique())
    bad_case = events_audit.loc[~events_audit["feature_name"].isin(canon), "feature_name"].dropna().unique()
    print(f"[Medium] Non-canonical feature_name casing: {len(bad_case)} -> {sorted(bad_case)}")

    # 5. Impossible values
    neg = clean.loc[clean["days_since_registration"] < 0, "days_since_registration"]
    print(f"[Medium] Negative days_since_registration (impossible): {len(neg)} rows")

    print("\nNote: the clean operational sheets pass logic checks - "
          "issues are isolated to the *_Audit sheets by design.")


if __name__ == "__main__":
    main()
