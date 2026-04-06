from fastapi import APIRouter, HTTPException, Depends
from schemas import PredictionInput, PredictionResponse
import pickle
import pandas as pd
import os

router = APIRouter(prefix="/prediction", tags=["Prediction"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'media', 'crop_model.pkl')

@router.post("/predict_crop", response_model=PredictionResponse)
def predict_crop(data: PredictionInput):
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=404, detail="Crop model not found. Please train the model first.")

    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        input_data = pd.DataFrame([{
            'N': data.N,
            'P': data.P,
            'K': data.K,
            'temperature': data.temperature,
            'humidity': data.humidity,
            'ph': data.ph,
            'rainfall': data.rainfall
        }])

        prediction = model.predict(input_data)[0]

        return PredictionResponse(prediction=prediction, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
