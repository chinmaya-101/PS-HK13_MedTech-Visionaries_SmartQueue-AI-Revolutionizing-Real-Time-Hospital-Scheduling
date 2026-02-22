# SmartQueue AI - Real-Time Hospital Scheduling

## Overview
This project is a healthcare scheduling app that uses AI to optimize real-time hospital queues. It features a FastAPI backend and a simple HTML frontend.

## Features
- Real-time queue management
- Doctor suggestion system
- Twilio SMS integration (credentials via environment variables)
- Secure secret handling with `.env` and `.gitignore`

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
