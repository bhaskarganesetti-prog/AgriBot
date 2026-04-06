from fastapi import APIRouter, HTTPException
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

router = APIRouter(prefix="/training", tags=["Model Training"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_PATH = os.path.join(BASE_DIR, 'media', 'Crop_recommendation.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'media', 'crop_model.pkl')

@router.post("/train_model")
def train_model():
    if not os.path.exists(DATASET_PATH):
        raise HTTPException(status_code=404, detail=f"Dataset file not found at {DATASET_PATH}")
    
    try:
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        df.dropna(inplace=True)

        X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = df['label']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Accuracy
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Save model
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)

        return {"message": "Model trained successfully", "accuracy": accuracy * 100}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")
