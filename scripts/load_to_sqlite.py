
from sqlalchemy import create_engine
import pandas as pd

# Create SQLite database
engine = create_engine("sqlite:///bluestock_mf.db")

files = {
    "fund_master": "data/processed/01_fund_master_clean.csv",
    "nav_history": "data/processed/02_nav_history_clean.csv",
    "scheme_performance": "data/processed/07_scheme_performance_clean.csv",
    "investor_transactions": "data/processed/08_investor_transactions_clean.csv"
}

for table, file in files.items():

    df = pd.read_csv(file)

    df.to_sql(
        table,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{table} loaded successfully")

print("\nDatabase Created Successfully!")