"""
01_profile_datasets.py - Profiles the supplied VELOOP simulated datasets.

Reproduces the findings in Deliverable #12 (Simulated Data Profiling):
  - record counts, columns, null counts, duplicate IDs, date ranges
  - referential integrity between the File-2 behavioural tables
  - the cross-file user-identity check (the two files are different populations)

Usage:
    python 01_profile_datasets.py [data_dir]

Expects, in data_dir (default ./data):
    VELOOP_Simulated_User_Behavior_1000.xlsx   (File 2 - integrated behaviour)
    VELoop_Rewards_Data_01.xlsx                 (File 1 - standalone users)

NOTE: all data is SIMULATED / FICTIONAL - not actual VELOOP figures.
"""
import sys
from pathlib import Path
import pandas as pd
from pandas.api import types as pt

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "data"
F2 = DATA / "VELOOP_Simulated_User_Behavior_1000.xlsx"
F1 = DATA / "VELoop_Rewards_Data_01.xlsx"


def load(path):
    """Load every sheet of a workbook into {sheet_name: DataFrame}."""
    xl = pd.ExcelFile(path)
    return {s: pd.read_excel(path, sheet_name=s) for s in xl.sheet_names}


def profile_sheet(name, df, id_col=None):
    print(f"\n[{name}]  rows={len(df):,}  cols={df.shape[1]}")
    nulls = df.isna().sum()
    nulls = nulls[nulls > 0]
    if len(nulls):
        print("  nulls:", {k: int(v) for k, v in nulls.items()})
    if id_col and id_col in df.columns:
        dup = int((df[id_col].duplicated(keep=False) & df[id_col].notna()).sum())
        print(f"  {id_col}: unique={df[id_col].nunique():,}  duplicate_rows={dup}")
    for col in df.columns:
        if pt.is_datetime64_any_dtype(df[col]):
            s = pd.to_datetime(df[col], errors="coerce")
            print(f"  date {col}: {s.min()}  ->  {s.max()}")


def referential_integrity(d2):
    """Every child key should resolve to its parent table (no orphans)."""
    print("\n=== Referential integrity (File 2) ===")
    users = set(d2["01_Users_1000"]["user_id"])
    sessions = set(d2["02_Sessions"]["session_id"])
    checks = [
        ("02_Sessions", "user_id", users),
        ("03_Feature_Events", "user_id", users),
        ("03_Feature_Events", "session_id", sessions),
        ("05_Task_Activity", "user_id", users),
        ("05_Task_Activity", "session_id", sessions),
        ("04_Daily_Activity", "user_id", users),
        ("06_Milestones", "user_id", users),
    ]
    for sheet, col, parent in checks:
        vals = d2[sheet][col].dropna()
        orphans = int((~vals.isin(parent)).sum())
        print(f"  {sheet}.{col:<12} -> {'PASS' if orphans == 0 else f'FAIL ({orphans} orphans)'}")


def cross_file_check(d1, d2):
    """The headline finding: the two files are NOT the same user population."""
    print("\n=== Cross-file user identity check ===")
    n1 = d1["Users_1000_Clean"].set_index("user_id")["full_name"].to_dict()
    n2 = d2["01_Users_1000"].set_index("user_id")["full_name"].to_dict()
    shared = set(n1) & set(n2)
    same = sum(1 for k in shared if n1[k] == n2[k])
    print(f"  shared user_ids: {len(shared)}   |   same person in both files: {same}")
    print(f"  VLUSR000001 -> File1='{n1.get('VLUSR000001')}'  File2='{n2.get('VLUSR000001')}'")
    print("  => Different simulated populations. Do NOT join the two files on user_id.")


def main():
    d2 = load(F2)
    profile_sheet("File2.01_Users_1000", d2["01_Users_1000"], "user_id")
    profile_sheet("File2.02_Sessions", d2["02_Sessions"], "session_id")
    profile_sheet("File2.03_Feature_Events", d2["03_Feature_Events"], "event_id")
    profile_sheet("File2.05_Task_Activity", d2["05_Task_Activity"], "activity_id")
    referential_integrity(d2)
    if F1.exists():
        cross_file_check(load(F1), d2)
    print("\nDone.")


if __name__ == "__main__":
    main()
