# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_budget_utils.ipynb.

# %% auto 0
__all__ = ['get_transactions', 'get_cash_balance', 'get_budgeted_balance', 'get_avg_monthly_spend']

# %% ../nbs/00_budget_utils.ipynb 1
import datetime
import requests
import json
import pandas as pd
from typing import List
from .utils import monthdelta

# %% ../nbs/00_budget_utils.ipynb 2
def get_transactions(token: str, n_months: int) -> pd.DataFrame:
    """Function to get all transactions from the last N months"""
    since_date = datetime.datetime.strftime(
        monthdelta(datetime.datetime.now(), -n_months), "%Y-%m-01"
    )
    end_date = datetime.datetime.strftime(
        monthdelta(datetime.datetime.now(), -n_months), "%Y-%m"
    )
    response = requests.get(
        f"https://api.youneedabudget.com/v1/budgets/last-used/transactions?access_token={token}&since_date={since_date}"
    )
    transactions = json.loads(response.content)["data"]["transactions"]
    tran_df = pd.DataFrame().from_dict(transactions)
    tran_df["date"] = pd.to_datetime(tran_df.date)
    tran_df["month"] = tran_df.date.dt.strftime("%Y-%m")
    tran_df["amount"] = tran_df.amount / 1000
    tran_df = pd.concat(
        [
            tran_df[~tran_df.category_name.str.contains("Split")],
            pd.DataFrame(
                list(
                    tran_df[tran_df.category_name.str.contains("Split")][
                        "subtransactions"
                    ].apply(lambda x: x[0])
                )
            ),
        ]
    )
    tran_df = tran_df[tran_df["month"] <= end_date]
    return tran_df

# %% ../nbs/00_budget_utils.ipynb 3
def get_cash_balance(token: str) -> float:
    """Function to get the total cash balance in YNAB"""
    accounts = requests.get(
        f"https://api.youneedabudget.com/v1/budgets/last-used/accounts?access_token={token}"
    )
    account_data = pd.DataFrame(json.loads(accounts.content)["data"]["accounts"])
    active_account_data = account_data.query(
        "closed==False and type!='otherAsset' and on_budget==True"
    )
    cash = active_account_data.balance.sum() / 1000
    return cash


def get_budgeted_balance(token: str, max_category_balance: int = 50000) -> float:
    """Function to get the total category balances in YNAB"""
    date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m") + "-01"
    month = requests.get(
        f"https://api.youneedabudget.com/v1/budgets/last-used/months/{date}?access_token={token}"
    )
    category_balances = pd.DataFrame(
        json.loads(month.content)["data"]["month"]["categories"]
    )
    to_be_budgeted = json.loads(month.content)["data"]["month"]["to_be_budgeted"] / 1000
    current_balance = (
        category_balances.query(f"balance < {max_category_balance * 100}").balance.sum()
        / 1000
    )
    total_budgeted = current_balance + to_be_budgeted
    return total_budgeted

# %% ../nbs/00_budget_utils.ipynb 4
def get_avg_monthly_spend(
    tran_df: pd.DataFrame, essential_categories: List[str]
) -> float:
    """Function to get the average monthly spend for a list of categories.  The
    category names must match exactly what is in YNAB"""
    monthly_spending = (
        tran_df[tran_df.category_name.isin(essential_categories)]
        .query("amount<=0 and amount>=-5000")
        .groupby("month")["amount"]
        .sum()
    )
    avg_essential = monthly_spending.mean()
    return avg_essential
