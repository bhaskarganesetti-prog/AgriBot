from pydantic import BaseModel
from typing import Optional

class UserRegistration(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    mobile: str

class UserLogin(BaseModel):
    email: str
    password: str

class PredictionInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class PredictionResponse(BaseModel):
    prediction: str
    status: str

class ChatbotInput(BaseModel):
    query: str

class ChatbotResponse(BaseModel):
    text: str
    audio_url: Optional[str] = None
