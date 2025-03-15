FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# JWT Authentication + MongoDB Atlas + Stripe Integration

# Install FastAPI and dependencies
RUN pip install fastapi uvicorn pymongo stripe

# Main Application File
COPY ./app/main.py ./app/main.py
