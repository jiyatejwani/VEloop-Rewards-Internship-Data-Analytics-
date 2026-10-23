"""
03_build_dashboard_data.py - Computes the dashboard metrics and writes data.js.

Reads the File-2 behavioural dataset, aggregates the metrics that are actually
computable from the supplied data, and writes ../data.js (consumed by the
static dashboard in index.html). Monetisation metrics are intentionally left
empty because the data to compute them does not exist.

Usage:
    python 03_build_dashboard_data.py [data_dir] [out_js]

NOTE: all data is SIMULATED / FICTIONAL - figures are not actual VELOOP results.
"""
import sys, json
from pathlib import Path
import pandas as pd

DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "data"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).parent.parent / "data.js"
F2 = DATA / "VELOOP_Simulated_User_Behavior_1000.xlsx"

users = pd.read_excel(F2, "01_Users_1000")
sess = pd.read_excel(F2, "02_Sessions")
ev = pd.read_excel(F2, "03_Feature_Events")
daily = pd.read_excel(F2, "04_Daily_Activity")
tasks = pd.read_excel(F2, "05_Task_Activity")
mile = pd.read_excel(F2, "06_Milestones")
fuse = pd.read_excel(F2, "07_Feature_Usage")

vc = lambda s: {str(k): int(v) for k, v in s.value_counts(dropna=False).items()}
D = {}

D["tiles"] = {
    "total_users": len(users), "total_sessions": len(sess), "total_events": len(ev),
    "total_tasks": len(tasks), "features": int(fuse["feature_name"].nunique()),
    "task_completion_rate": round((tasks["task_status"] == "Completed").mean() * 100, 1),
    "avg_session_sec": round(float(sess["session_duration_seconds"].mean()), 1),
    "avg_active_days": round(float(daily.groupby("user_id").size().mean()), 1),
}

users["m"] = pd.to_datetime(users["registration_datetime"]).dt.to_period("M").astype(str)
D["reg_month"] = {k: int(v) for k, v in users["m"].value_counts().sort_index().items()}
D["acquisition"] = vc(users["acquisition_source"])
D["account_status"] = vc(users["account_status"])
D["device"] = vc(users["primary_device"])
D["onboarding"] = {k: int(users["onboarding_status"].value_counts().get(k, 0))
                   for k in ["Not Started", "Started", "Completed"]}

daily["activity_date"] = pd.to_datetime(daily["activity_date"])
wau = daily.groupby("activity_date")["user_id"].nunique().resample("W").mean()
D["wau_trend"] = {str(k)[:10]: round(float(v), 1) for k, v in wau.items()}

fs = fuse.sort_values("unique_users", ascending=False)
D["feature_adoption"] = {str(r.feature_name): int(r.unique_users) for r in fs.itertuples()}
D["feature_success_rate"] = {str(r.feature_name): round(100 * r.users_with_success_event / r.unique_users, 1)
                             for r in fs.itertuples()}

D["task_status"] = {k: int(tasks["task_status"].value_counts().get(k, 0))
                    for k in ["Completed", "Abandoned", "Failed", "Pending"]}
cat = tasks.groupby("task_category").apply(lambda g: (g["task_status"] == "Completed").mean() * 100,
                                           include_groups=False).sort_values(ascending=False)
D["completion_by_category"] = {str(k): round(float(v), 1) for k, v in cat.items()}
D["failure_reasons"] = vc(tasks["failure_reason"].dropna())
D["event_status"] = {k: int(ev["event_status"].value_counts().get(k, 0))
                     for k in ["Started", "Success", "Abandoned", "Failed"]}
D["milestones"] = vc(mile["milestone_type"])

# cohort activity by day-offset since registration
reg = pd.to_datetime(users.set_index("user_id")["registration_datetime"]).dt.normalize()
dm = daily[["user_id", "activity_date"]].copy()
dm["offset"] = (dm["activity_date"].dt.normalize() - dm["user_id"].map(reg)).dt.days
D["retention"] = {f"D{o}": round(100 * dm[dm.offset == o]["user_id"].nunique() / len(users), 1)
                  for o in [0, 1, 3, 7, 14, 30]}

# monetisation KPIs cannot be computed from the supplied data
D["proposed"] = {
    "Reward credit volume": "Requires a rewards ledger (amount, unit, state) - not in supplied data",
    "Wallet transaction volume": "Requires a wallet transactions table - not in supplied data",
    "Withdrawal completion rate": "Requires a withdrawals table - not in supplied data",
    "Referral conversion rate": "Requires a referral lifecycle table - not in supplied data",
}

OUT.write_text("window.VELOOP_DATA = " + json.dumps(D, indent=1) + ";\n")
print(f"wrote {OUT}  ({len(D)} metric groups)")
