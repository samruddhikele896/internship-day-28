from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

PositiveDecimal = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
NonEmptyString = Annotated[str, Field(min_length=1, strip_whitespace=True)]


# ---------------- Initial Balance ----------------

class InitialBalanceCreate(BaseModel):
    total_amount: PositiveDecimal


class InitialBalanceResponse(BaseModel):
    id: int
    total_amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------- Expense ----------------

class ExpenseCreate(BaseModel):
    expense_for: NonEmptyString
    amount: PositiveDecimal


class ExpenseResponse(BaseModel):
    id: int
    expense_for: str
    amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------- Saving Goal ----------------

class SavingGoalCreate(BaseModel):
    monthly_goal: PositiveDecimal
    weekly_goal: PositiveDecimal
    daily_goal: PositiveDecimal


class SavingGoalResponse(BaseModel):
    id: int
    monthly_goal: Decimal
    weekly_goal: Decimal
    daily_goal: Decimal

    model_config = ConfigDict(from_attributes=True)