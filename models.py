from pydantic import BaseModel, Field
from typing import Optional, List

class Expense(BaseModel):
    amount: float = Field(gt=0)
    description: str
    paid_by: str
    shared_by: Optional[List[str]] = None  # optional for default equal split

class UpdateExpense(Expense):
    id: str
