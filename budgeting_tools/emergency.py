# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_emergency.ipynb.

# %% auto 0
__all__ = ['get_emergency_fund_status']

# %% ../nbs/00_emergency.ipynb 5
from budgeting_tools.budget_utils import (get_avg_monthly_spend,
                                          get_budgeted_balance,
                                          get_cash_balance, get_transactions)


# %% ../nbs/00_emergency.ipynb 15
def get_emergency_fund_status(
    token, essential_categories, n_months=6, emergency_fund_months=6
):
    """Function to get the status of the emergency fund.  Returns the amount
    needed to fully fund the emergency fund or the amount of non-emergency cash
    if the emergency fund is fully funded"""
    trans_df = get_transactions(token, n_months)
    monthly_spend = get_avg_monthly_spend(trans_df, essential_categories)
    cash = get_cash_balance(token)
    budgeted = get_budgeted_balance(token)
    emergency_fund_size = monthly_spend * emergency_fund_months
    unbudgeted_cash = cash - budgeted
    non_emergency_cash = unbudgeted_cash - (emergency_fund_size * -1)
    return non_emergency_cash