# Data Dictionary

## 01_fund_master

| Column | Type | Description |
|----------|---------|---------|
| amfi_code | Integer | AMFI Scheme Code |
| fund_house | Text | Fund House Name |
| scheme_name | Text | Scheme Name |
| category | Text | Fund Category |

## 02_nav_history

| Column | Type | Description |
|----------|---------|---------|
| amfi_code | Integer | Fund Code |
| date | Date | NAV Date |
| nav | Float | Net Asset Value |