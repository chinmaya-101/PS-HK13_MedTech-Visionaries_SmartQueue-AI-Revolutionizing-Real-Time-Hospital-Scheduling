from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    patient_name: str
    phone_number: str
    patient_age: int
    disease: str
    doctor_name: str

class UserCreate(BaseModel):
    username: str
    password: str

# --- NEW: SCHEMA FOR SMS ---
class SMSRequest(BaseModel):
    phone_number: str
    patient_name: str
    wait_time: str
    doctor_name: str