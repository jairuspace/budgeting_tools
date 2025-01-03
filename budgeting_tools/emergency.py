# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/emergency_fund.ipynb.

# %% auto 0
__all__ = ['get_emergency_fund_status']

# %% ../nbs/emergency_fund.ipynb 4
from budgeting_tools.ynab_utils import (
    get_transactions,
    get_avg_monthly_spend,
    get_cash_balance,
    get_budgeted_balance,
)

# %% ../nbs/emergency_fund.ipynb 13
def get_emergency_fund_status(
    essential_categories, n_months=6, emergency_fund_months=6
):
    """Function to get the status of the emergency fund.  Returns the amount
    needed to fully fund the emergency fund or the amount of non-emergency cash
    if the emergency fund is fully funded"""
    trans_df = get_transactions(n_months)
    monthly_spend = get_avg_monthly_spend(trans_df, essential_categories)
    cash = get_cash_balance()
    budgeted = get_budgeted_balance()
    emergency_fund_size = monthly_spend * emergency_fund_months
    unbudgeted_cash = cash - budgeted
    non_emergency_cash = unbudgeted_cash - (emergency_fund_size * -1)
    return non_emergency_cash
