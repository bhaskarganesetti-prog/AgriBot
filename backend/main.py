import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the current directory to sys.path to resolve imports correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routers import auth, prediction, training, chatbot

app = FastAPI(title="Agriculture Crop Chatbot Backend API", version="1.0.0")

# CORS settings to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the routers
app.include_router(auth.router)
app.include_router(prediction.router)
app.include_router(training.router)
app.include_router(chatbot.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crop Prediction Chatbot API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
