from typing import List, Dict, Optional
from pydantic import BaseModel, Field, validator,constr
from datetime import date, datetime

class SessionData(BaseModel):
    data: dict

class Item(BaseModel):
    item: str

class PatientCreate(BaseModel):
    ID: str  # Should contain "PAT" prefix
    fullName: str
    contact: str
    caretaker: Optional[str] = None  # Caretaker ID if exists
    type: str = "Patient"

class DoctorCreate(BaseModel):
    ID: constr(strip_whitespace=True, min_length=4, pattern=r'^DOC')  # Enforce DOC prefix
    fullName: str
    contact: str
    password: str  # Raw password to be hashed
    type: str = "Doctor"  # Auto-set for consistency

class MedicalHistory(BaseModel):
    diagnosis: str
    duration_value: int
    duration_unit: str

class DosageSchedule(BaseModel):
    day: str
    dosage: float

    def as_dict(self) -> dict:
        return {"day": self.day, "dosage": self.dosage}

class Patient(BaseModel):
    name: str = Field(...)
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., pattern="^(M|F|O)$")
    target_inr_min: float
    target_inr_max: float
    therapy: str
    medical_history: List[MedicalHistory]
    therapy_start_date: date
    dosage_schedule: List[DosageSchedule]
    contact: str = Field(..., pattern=r"^\+91\s?(\d\s?){10}$")
    kin_name: str = Field(..., pattern="^[a-zA-Z ]{2,}$")
    kin_contact: str = Field(..., pattern=r"^\+91\s?(\d\s?){10}$")
    refresh_token:str
    def as_dict(self) -> Dict:
        dct = self.dict()
        dct["therapy_start_date"] = datetime.strftime( dct["therapy_start_date"], "%d/%m/%Y")
        return dct

class Doctor(BaseModel):
    fullName: str
    refresh_token:str
    ID: str

class INRReport(BaseModel):
    type: str = Field(default="INR Report")
    inr_value: float
    location_of_test: str
    date: datetime
    file_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)