Live site:  deployed Vercel URL here · 
Project overview
VELOOP Rewards is an online rewards and engagement product in early development. The available data does not yet support all conventional product analytics. This project establishes an analytics foundation by documenting what the current simulated datasets can support, auditing data quality and coverage, and specifying the instrumentation and data structures needed for future analysis.
The static site includes four views:
- Overview: Readiness verdict and key findings.
- Dashboard: 13 charts based on the simulated behavioural data.
- Deliverables: Index of the 21 project deliverables, with download links.
- Data Model: Logical model covering 10 entities—6 existing and 4 proposed.
Key findings
1. The two supplied files represent different user populations. Although both use IDs following the VLUSR000001… pattern, none of the 1,000 shared IDs map to the same person. Therefore, user_id is not a reliable shared key between the files; they should be analysed separately unless a validated mapping or re-keying process is introduced.
2. The monetisation data layer is missing. Rewards ledger, wallet transactions, withdrawals, and referral lifecycle tables are not present in the supplied data, and no monetary amount field was found. As a result, only 7 of the 20 sampled KPIs are currently computable; others depend on proposed data structures or further engineering verification.
Readiness assessment
Status	Areas	Meaning
Confirmed	7	Data exists and has been verified in the simulated dataset
To Be Verified	8	Data is partially present and requires engineering confirmation
Proposed	15	Structures or instrumentation are not currently available and need to be built


These figures describe the project's readiness assessment, not actual product performance.
Deliverables
The repository contains the following 21 deliverables in the deliverables/ directory:
#	Deliverable	Format
1	Executive Summary	Word (.docx)
2	Product Data Audit	Word (.docx)
3	Data Coverage Matrix	Excel (.xlsx)
4	User & Account Analytics Specification	Word (.docx)
5	Earning & Reward Analytics	Word (.docx)
6	Wallet & Withdrawal Analytics	Word (.docx)
7	Referral & Engagement Analytics	Word (.docx)
8	Event Tracking Plan (38 events)	Excel (.xlsx)
9	Data Dictionary (121 fields)	Excel (.xlsx)
10	Logical Data Model and ER Diagram	Word (.docx) + PNG
11	KPI Catalogue (37 KPIs)	Excel (.xlsx)
12	Simulated Data Profiling	Excel (.xlsx)
13	Data Quality Audit	Excel (.xlsx)
14	Dashboard Blueprint	Static website
15	Developer Analytics Handoff	Excel (.xlsx)
16	Data Pipeline Proposal	Word (.docx) + PNG
17	Privacy & Governance Proposal	Word (.docx)
18	Analytics Readiness Assessment	Excel (.xlsx)
19	Source & Verification Register	Excel (.xlsx)
20	Implementation Backlog	Excel (.xlsx)
21	Final Consolidated Report	Word (.docx)


Additional quality-control and change-log workbooks are also included.
How the dashboard metrics were produced
The simulated behavioural dataset contains 1,000 users, 7,913 sessions, 35,704 events, and 9,846 task attempts. Python and pandas scripts profile and aggregate the data. The resulting metrics are stored in data.js and displayed in the browser using Chart.js.
The site is a static page and does not require a JavaScript build step.
Repository structure
.
├── index.html          # Dashboard and deliverables website
├── data.js             # Pre-computed metrics from simulated data
├── vercel.json         # Static deployment configuration
├── deliverables/       # Project reports, spreadsheets, and diagrams
├── analysis/
│   ├── 01_profile_datasets.py
│   ├── 02_data_quality_audit.py
│   ├── 03_build_dashboard_data.py
│   ├── requirements.txt
│   └── data/           # Input workbooks used by the analysis scripts
└── sql/
    └── kpi_queries.sql # KPI definitions and query examples
Reproduce the analysis
Use Python 3 and install the dependencies listed in analysis/requirements.txt.
cd analysis
pip install -r requirements.txt

# Run the scripts in order
python 01_profile_datasets.py
python 02_data_quality_audit.py
python 03_build_dashboard_data.py
The scripts use the workbooks in analysis/data/. If you move the scripts or data files, update the paths accordingly. The third script regenerates the root-level data.js file used by the dashboard.
KPI definitions are documented in [`sql/kpi_queries.sql`](sql/kpi_queries.sql). Seven sampled KPIs can be computed from the supplied data; three SQL KPI examples are marked as proposed because they depend on tables that do not currently exist.
View and deploy the dashboard
To view the dashboard locally, open index.html in a modern web browser. To publish it, import the repository into Vercel and deploy it as a static site. Once deployed, replace the live-site placeholder at the top of this README with the actual deployment URL.
Tools and technologies
- Python for analysis scripts
- pandas for data profiling and aggregation
- SQL for KPI query definitions
- HTML, CSS, and JavaScript for the static dashboard site
- Chart.js for visualisations
- Vercel for optional static hosting
Data integrity and limitations
- The supplied data is simulated and must not be interpreted as real business performance.
- Identically formatted user IDs across the two workbooks do not establish that they refer to the same person.
- Missing rewards, wallet, withdrawal, and referral-lifecycle data limits the KPIs that can be computed today.
- The Source & Verification Register (VELOOP_19_Source_Verification_Register.xlsx) documents the project's source and verification notes.
This project demonstrates data profiling, data-quality auditing, KPI definition, analytics readiness assessment, dashboard development, and documentation of proposed product instrumentation and data models.
