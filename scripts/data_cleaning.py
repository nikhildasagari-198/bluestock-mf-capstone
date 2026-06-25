import pandas as pd

# Load NAV History
nav = pd.read_csv("data/raw/02_nav_history.csv")

# Convert date
nav["date"] = pd.to_datetime(nav["date"])

# Sort values
nav = nav.sort_values(["amfi_code", "date"])

# Check missing values
print(nav.isnull().sum())

# Forward fill NAV values if any missing
nav["nav"] = nav.groupby("amfi_code")["nav"].ffill()

# Save
nav.to_csv("data/processed/02_nav_history_clean.csv", index=False)

print("NAV History cleaned successfully")

# Load transactions
txn = pd.read_csv("data/raw/08_investor_transactions.csv")

# Standardize transaction types
txn["transaction_type"] = txn["transaction_type"].str.strip().str.title()

# Keep valid amounts
txn = txn[txn["amount_inr"] > 0]

# Convert date
txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])

# Save
txn.to_csv(
    "data/processed/08_investor_transactions_clean.csv",
    index=False
)

print("Investor transactions cleaned successfully")

import pandas as pd

perf = pd.read_csv("data/raw/07_scheme_performance.csv")

print(perf.columns.tolist())

perf = pd.read_csv("data/raw/07_scheme_performance.csv")

cols = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio"
]

for col in cols:
    perf[col] = pd.to_numeric(
        perf[col],
        errors="coerce"
    )

print(perf[cols].isnull().sum())

perf.to_csv(
    "data/processed/07_scheme_performance_clean.csv",
    index=False
)

print("Scheme performance cleaned")

datasets = [
    "01_fund_master",
    "03_aum_by_fund_house",
    "04_monthly_sip_inflows",
    "05_category_inflows",
    "06_industry_folio_count",
    "09_portfolio_holdings",
    "10_benchmark_indices"
]

for ds in datasets:

    df = pd.read_csv(f"data/raw/{ds}.csv")

    df = df.drop_duplicates()

    df.to_csv(
        f"data/processed/{ds}_clean.csv",
        index=False
    )

print("All datasets cleaned")