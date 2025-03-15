from pydantic import BaseModel
from bson import ObjectId

class UserSchema(BaseModel):
    username: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class PaymentSchema(BaseModel):
    amount: int

class UserInDB(UserSchema):
    hashed_password: str

class DashboardResponse(BaseModel):
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class PaymentIntentResponse(BaseModel):
    client_secret: str
