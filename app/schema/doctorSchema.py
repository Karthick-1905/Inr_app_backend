from pydantic import BaseModel, Field
from app.model import DosageSchedule
from typing import List

class editDosageSchema(BaseModel):
    dosage_schedule : List[DosageSchedule]


class NextReviewUpdate(BaseModel):
    next_review_date: str = Field(...)