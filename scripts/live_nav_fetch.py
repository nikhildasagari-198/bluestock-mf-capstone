import requests
import pandas as pd
import os

os.makedirs("data/raw/live_nav", exist_ok=True)

schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        nav_df.to_csv(
            f"data/raw/live_nav/{name}.csv",
            index=False
        )

        print(f"Downloaded {name}")

    else:
        print(f"Failed {name}")