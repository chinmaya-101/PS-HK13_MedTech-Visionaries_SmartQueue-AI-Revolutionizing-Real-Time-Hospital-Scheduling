from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
import random 
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DOCTOR LIST DATA ---
DOCTORS_DATABASE = [
    {"name": "Dr. Ayush", "spec": "Cardiology", "status": "Available", "cat": "Adult Surgery", "arrival": "09:00 AM"},
    {"name": "Dr. Sharma", "spec": "Pediatrics", "status": "Busy", "cat": "Child Care", "arrival": "11:30 AM"},
    {"name": "Dr. Patel", "spec": "General", "status": "Available", "cat": "Minor Diseases", "arrival": "08:30 AM"},
    {"name": "Dr. Sarah", "spec": "Orthopedic", "status": "Available", "cat": "Surgery", "arrival": "10:15 AM"}
]

@app.get("/doctors/")
def get_doctors():
    return DOCTORS_DATABASE

@app.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = models.User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return {"message": "Account created successfully"}

@app.post("/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username, models.User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.post("/predict/")
def predict_queue(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    new_app = models.Appointment(
        patient_name=appointment.patient_name,
        phone_number=appointment.phone_number,
        patient_age=appointment.patient_age,
        disease=appointment.disease,
        doctor_name=appointment.doctor_name
    )
    db.add(new_app)
    db.commit()

    disease_lower = appointment.disease.lower()
    suggested_doctor = "Dr. Patel"
    
    # --- DYNAMIC EXPLAINABLE AI LOGIC ---
    reasons = [f"• Base triage for '{appointment.disease}'"]
    
    if appointment.patient_age > 60:
        reasons.append("• Age > 60 elevated priority score")
    elif appointment.patient_age < 12:
        reasons.append("• Pediatric status prioritized")

    if "child" in disease_lower or appointment.patient_age < 12:
        suggested_doctor = "Dr. Sharma"
        reasons.append(f"• Routed to {suggested_doctor} (Pediatrics)")
        recommendation = f"AI recommends switching to {suggested_doctor} for specialized child care."
    elif "heart" in disease_lower or "cardio" in disease_lower:
        suggested_doctor = "Dr. Ayush"
        reasons.append(f"• High-risk keywords detected, routed to {suggested_doctor} (Cardiology)")
        recommendation = f"Urgent: {suggested_doctor} is the best match for cardiac issues."
    else:
        reasons.append(f"• General queue matching optimal for {suggested_doctor}")
        recommendation = "Scheduling optimal. No reassignment required."

    # Join the bullet points together with HTML line breaks
    explanation = "<br>".join(reasons)
    
    load = random.randint(40, 95)
    queue_pos = random.randint(1, 15)
    consult = random.randint(10, 30)
    wait_time = (queue_pos * 3) + random.randint(1, 10)
    arrival_time = (datetime.now() + timedelta(minutes=wait_time)).strftime("%I:%M %p")
    # Fetch the actual status from the DOCTORS_DATABASE
    status = "Available" # Default fallback
    for doc in DOCTORS_DATABASE:
        if doc["name"] == appointment.doctor_name:
            status = doc["status"]
            break

    # --- REAL DATABASE QUEUE ---
    # 1. Fetch all real patients that have been saved in the database
    # 4. Enforce Max 6 Patients (Remove the oldest if the queue is full)
    while db.query(models.Appointment).count() > 6:
        oldest_patient = db.query(models.Appointment).order_by(models.Appointment.id.asc()).first()
        db.delete(oldest_patient)
        db.commit()

    # 5. Fetch Queue: Oldest First, Newest Last
    # .order_by(id.asc()) ensures the oldest patient is at the top of the list
    current_patients = db.query(models.Appointment).order_by(models.Appointment.id.asc()).all()

    live_queue = []
    current_score = 95 # The oldest person at the top gets the highest priority score
    
    for record in current_patients:
        live_queue.append({"name": record.patient_name, "score": current_score})
        current_score -= random.randint(4, 10) # Lower the score for newer people waiting

    # 6. Calculate Doctor Busy Schedule times in exact order
    current_time = datetime.now()
    for idx, p in enumerate(live_queue):
        start_t = current_time + timedelta(minutes=(idx * 12))
        end_t = start_t + timedelta(minutes=10)
        p["start_time"] = start_t.strftime("%I:%M %p")
        p["end_time"] = end_t.strftime("%I:%M %p")

    return {
        "load": load,
        "status": status,
        "queue": queue_pos,
        "wait": wait_time,
        "arrival_time": arrival_time,
        "consult": consult,
        "recommend": recommendation,
        "explain": explanation,
        "suggested_doctor": suggested_doctor,
        "live_queue": live_queue 
    }

# --- TWILIO SMS INTEGRATION ---
# Load credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+17744925982")

@app.post("/send-sms/")
def send_sms(request: schemas.SMSRequest):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        msg_body = f"Hello {request.patient_name}, your appointment with {request.doctor_name} is confirmed. Estimated wait time: {request.wait_time} mins. - MedhTech AI"
        
        # Clean up the phone number coming from the frontend
        to_number = request.phone_number.strip()
        if not to_number.startswith('+'):
            to_number = "+91" + to_number # Adds +91 for India

        print(f"\n--- ATTEMPTING TO SEND SMS ---")
        print(f"FROM: {TWILIO_PHONE_NUMBER}")
        print(f"TO: {to_number}")
        
        message = client.messages.create(
            body=msg_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"SUCCESS! Message SID: {message.sid}\n")
        return {"message": "SMS sent successfully"}
        
    except Exception as e:
        print(f"\n--- TWILIO ERROR ---")
        print(e)
        print(f"--------------------\n")
        raise HTTPException(status_code=500, detail=str(e))