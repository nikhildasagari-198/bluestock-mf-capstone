import pandas as pd

files = {
    "fund_master": "data/raw/01_fund_master.csv",
    "nav_history": "data/raw/02_nav_history.csv",
    "aum": "data/raw/03_aum_by_fund_house.csv",
    "sip": "data/raw/04_monthly_sip_inflows.csv",
    "category": "data/raw/05_category_inflows.csv",
    "folio": "data/raw/06_industry_folio_count.csv",
    "performance": "data/raw/07_scheme_performance.csv",
    "transactions": "data/raw/08_investor_transactions.csv",
    "holdings": "data/raw/09_portfolio_holdings.csv",
    "benchmark": "data/raw/10_benchmark_indices.csv"
}

for name, path in files.items():
    print("\n" + "="*60)
    print(f"DATASET: {name}")

    df = pd.read_csv(path)

    print("Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())