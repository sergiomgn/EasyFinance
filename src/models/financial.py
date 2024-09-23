from datetime import date
from typing import List

from pydantic import BaseModel


class Stock(BaseModel):
    # TODO: Need to implement the Sotck information class
    pass


class Expense(BaseModel):
    """"""

    id: int
    user_id: int
    account_id: int
    category: str
    ammount: float
    date: date
    tags: List[str] = []
    description: str = ""
    recurring: bool = False
    due_date: date = None
    currency: str = None
    location: str = None


class FinancialInfo(BaseModel):
    """Finanancial information class"""

    expenses: List[Expense] = []
    stocks: List[Stock] = []
