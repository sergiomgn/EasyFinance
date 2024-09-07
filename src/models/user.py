from pydantic import BaseModel

from models.financial import FinancialInfo


class UserBase(BaseModel):
    """Base model for a user"""

    username: str
    password: str


class UserData(UserBase):
    """Model that contains the Diferent Financial Data of the user"""

    id: int
    financial_info: FinancialInfo
