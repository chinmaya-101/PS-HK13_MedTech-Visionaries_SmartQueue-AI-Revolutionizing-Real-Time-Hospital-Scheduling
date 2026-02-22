# SmartQueue AI - Real-Time Hospital Scheduling

## Overview
This project is a healthcare scheduling app that uses AI to optimize real-time hospital queues. It features a FastAPI backend and a simple HTML frontend.

## Features
- Real-time queue management
- Doctor suggestion system
- Twilio SMS integration (credentials via environment variables)
- Secure secret handling with `.env` and `.gitignore`

## 🛠️ Tech Stack

This project is built using a modern, lightweight, and incredibly fast architecture, separating the client-side dashboard from the AI-driven backend API.

### Frontend
* **HTML5 & CSS3:** For the responsive, glowing, glass-morphism dashboard UI.
* **Vanilla JavaScript:** For DOM manipulation, dynamic HTML updates, and asynchronous API calls (`fetch`).
* **Chart.js:** For rendering the real-time "Predicted Wait Trend" line chart.

### Backend
* **Python 3:** Core programming language handling the queue optimization and logic.
* **FastAPI:** A modern, high-performance web framework for building the RESTful APIs.
* **Uvicorn:** Lightning-fast ASGI server to run the FastAPI application.
* **SQLAlchemy:** Object-Relational Mapper (ORM) for secure and efficient database management.

### Database
* **SQLite / SQL:** Relational database used to store patient details, appointment logs, and queue history seamlessly.

### External Integrations & APIs
* **Twilio API:** Integrated for automated SMS notifications, sending real-time appointment confirmations and predicted wait times to patients.

### AI & Core Logic
* **Custom Priority Algorithm:** Calculates patient position based on age, disease severity, and time of arrival (FIFO).
* **Explainable AI (XAI) Engine:** Generates transparent, human-readable reasoning for why a patient was assigned a specific priority or doctor.
* **Time-Block Scheduling Math:** Dynamically computes reporting times and doctor schedules using Python's `datetime` module.

## Setup
1. Clone the repository
2. Create a `.env` file in the root directory:
   ```
   TWILIO_ACCOUNT_SID=your_actual_sid_here
   TWILIO_AUTH_TOKEN=your_actual_token_here
   TWILIO_PHONE_NUMBER=+1your_number_here
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   (If `requirements.txt` is missing, install FastAPI, SQLAlchemy, Twilio, python-dotenv)
4. Run the backend:
   ```
   uvicorn main:app --reload
   ```
5. Open `front_end/index.html` in your browser for the frontend.

## Security
- Secrets are never hardcoded; use environment variables.
- `.gitignore` prevents sensitive files and cache from being tracked.

## License
MIT
