from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from passlib.context import CryptContext
import jwt
import datetime
import stripe

# FastAPI app
app = FastAPI()

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/")
db = client['ai_saas_db']
users_collection = db['users']

# JWT Secret Key
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Stripe API Key
stripe.api_key = "your_stripe_secret_key"

# Register User
@app.post("/register")
def register_user(username: str, password: str):
    hashed_password = pwd_context.hash(password)
    users_collection.insert_one({"username": username, "password": hashed_password})
    return {"msg": "User Registered Successfully"}

# Login User
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"username": form_data.username})
    if not user or not pwd_context.verify(form_data.password, user['password']):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    access_token = jwt.encode({"sub": form_data.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Route
@app.get("/dashboard")
def dashboard(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return {"message": f"Welcome to your dashboard, {username}!"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")

# Stripe Payment Endpoint
@app.post("/create-payment")
def create_payment(amount: int):
    payment_intent = stripe.PaymentIntent.create(
        amount=amount * 100, # Amount in cents
        currency="usd",
    )
    return {"client_secret": payment_intent['client_secret']}
