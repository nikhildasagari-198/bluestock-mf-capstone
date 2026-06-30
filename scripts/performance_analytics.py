import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
import os

# ==============================
# Create reports/charts folder
# ==============================
os.makedirs("reports/charts", exist_ok=True)

# ==============================
# Load datasets
# ==============================
nav = pd.read_csv("data/processed/02_nav_history_clean.csv")
performance = pd.read_csv("data/processed/07_scheme_performance_clean.csv")
benchmark = pd.read_csv("data/processed/10_benchmark_indices_clean.csv")

# ==============================
# Convert dates
# ==============================
nav["date"] = pd.to_datetime(nav["date"])
benchmark["date"] = pd.to_datetime(benchmark["date"])

# ==============================
# Daily Returns
# ==============================
nav = nav.sort_values(["amfi_code", "date"])

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)

# ==============================
# Daily Return Distribution Chart
# ==============================
plt.figure(figsize=(10,5))

sns.histplot(
    nav["daily_return"].dropna(),
    bins=50,
    kde=True
)

plt.title("Distribution of Daily Returns")

plt.savefig("reports/charts/11_daily_return_distribution.png", dpi=300)

plt.close()

print("Daily Return chart saved")

# ==============================
# CAGR
# ==============================
cagr = []

for code, group in nav.groupby("amfi_code"):

    start_nav = group.iloc[0]["nav"]
    end_nav = group.iloc[-1]["nav"]

    years = (
        group.iloc[-1]["date"] -
        group.iloc[0]["date"]
    ).days / 365

    if years > 0:

        value = ((end_nav / start_nav) ** (1 / years)) - 1

        cagr.append([code, value])

cagr = pd.DataFrame(
    cagr,
    columns=["amfi_code", "cagr"]
)

# ==============================
# Sharpe Ratio
# ==============================
risk_free = 0.065

sharpe = []

for code, group in nav.groupby("amfi_code"):

    annual_return = group["daily_return"].mean() * 252

    annual_std = group["daily_return"].std() * np.sqrt(252)

    ratio = (annual_return - risk_free) / annual_std

    sharpe.append([code, ratio])

sharpe = pd.DataFrame(
    sharpe,
    columns=["amfi_code", "sharpe_ratio"]
)

# ==============================
# Sortino Ratio
# ==============================
sortino = []

for code, group in nav.groupby("amfi_code"):

    downside = group[group["daily_return"] < 0]["daily_return"]

    downside_std = downside.std() * np.sqrt(252)

    annual_return = group["daily_return"].mean() * 252

    ratio = (annual_return - risk_free) / downside_std

    sortino.append([code, ratio])

sortino = pd.DataFrame(
    sortino,
    columns=["amfi_code", "sortino_ratio"]
)

# ==============================
# Benchmark Returns
# ==============================
benchmark["benchmark_return"] = benchmark["close_value"].pct_change()

merged = pd.merge(
    nav,
    benchmark[["date", "benchmark_return"]],
    on="date",
    how="inner"
)

# ==============================
# Alpha Beta
# ==============================
alpha_beta = []

for code, group in merged.groupby("amfi_code"):

    group = group.dropna()

    if len(group) > 20:

        beta, alpha, r, p, std = linregress(
            group["benchmark_return"],
            group["daily_return"]
        )

        alpha_beta.append([
            code,
            alpha * 252,
            beta
        ])

alpha_beta = pd.DataFrame(
    alpha_beta,
    columns=[
        "amfi_code",
        "alpha",
        "beta"
    ]
)

# ==============================
# Maximum Drawdown
# ==============================
drawdown = []

for code, group in nav.groupby("amfi_code"):

    running_max = group["nav"].cummax()

    dd = (group["nav"] / running_max) - 1

    drawdown.append([
        code,
        dd.min()
    ])

drawdown = pd.DataFrame(
    drawdown,
    columns=[
        "amfi_code",
        "max_drawdown"
    ]
)

# ==============================
# Merge Scorecard
# ==============================
scorecard = cagr.merge(sharpe, on="amfi_code")

scorecard = scorecard.merge(sortino, on="amfi_code")

scorecard = scorecard.merge(drawdown, on="amfi_code")

scorecard = scorecard.merge(alpha_beta, on="amfi_code")

# ==============================
# Fund Score
# ==============================
scorecard["score"] = (

    scorecard["cagr"].rank(pct=True) * 30 +

    scorecard["sharpe_ratio"].rank(pct=True) * 25 +

    scorecard["alpha"].rank(pct=True) * 20 +

    scorecard["sortino_ratio"].rank(pct=True) * 15 +

    scorecard["max_drawdown"].rank(
        pct=True,
        ascending=False
    ) * 10

)

scorecard = scorecard.sort_values(
    "score",
    ascending=False
)

# ==============================
# Save CSV files
# ==============================
scorecard.to_csv(
    "reports/fund_scorecard.csv",
    index=False
)

alpha_beta.to_csv(
    "reports/alpha_beta.csv",
    index=False
)

print("CSV files exported")

# ==============================
# Benchmark Comparison
# ==============================
plot = scorecard.head(5).merge(
    performance,
    on="amfi_code"
)

plt.figure(figsize=(12,6))

sns.barplot(
    data=plot,
    x="scheme_name",
    y="return_3yr_pct"
)

plt.xticks(rotation=90)

plt.title("Top 5 Funds")

plt.tight_layout()

plt.savefig(
    "reports/charts/12_top5_benchmark.png",
    dpi=300
)

plt.close()

print("Benchmark comparison chart saved")

print("\n====================================")
print("Performance Analytics Completed")
print("====================================")
print("Generated Files:")
print("1. reports/fund_scorecard.csv")
print("2. reports/alpha_beta.csv")
print("3. reports/charts/11_daily_return_distribution.png")
print("4. reports/charts/12_top5_benchmark.png")