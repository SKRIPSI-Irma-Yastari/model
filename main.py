from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from train_model import train as train_logic

app = FastAPI(
    title="Stakeholder Relationship Monitoring API",
    description="API untuk memantau hubungan kerja sama stakeholder menggunakan Decision Tree",
    version="1.0.0"
)

# Global variables for model and encoders
model = None
le_kkks = None
le_interaksi = None
le_label = None

def load_resources():
    global model, le_kkks, le_interaksi, le_label
    try:
        model = joblib.load('models/decision_tree_model.joblib')
        le_kkks = joblib.load('models/le_kkks.joblib')
        le_interaksi = joblib.load('models/le_interaksi.joblib')
        le_label = joblib.load('models/le_label.joblib')
        print("Resources loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading resources: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    if not os.path.exists('models/decision_tree_model.joblib'):
        print("Model not found. Training initial model...")
        train_logic()
    load_resources()

class PredictionRequest(BaseModel):
    nama_kkks: str
    jenis_interaksi: str
    skor: int

class PredictionResponse(BaseModel):
    label: str
    confidence: float

@app.get("/")
def read_root():
    return {"message": "Stakeholder Monitoring API is running", "docs": "/docs"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Encode inputs
        # If the value is new, we might need a fallback or re-train
        try:
            kkks_encoded = le_kkks.transform([request.nama_kkks])[0]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Nama KKKS '{request.nama_kkks}' tidak dikenali. Silakan lakukan retraining.")
            
        try:
            interaksi_encoded = le_interaksi.transform([request.jenis_interaksi])[0]
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Jenis Interaksi '{request.jenis_interaksi}' tidak dikenali.")

        # Prepare features
        features = pd.DataFrame([[kkks_encoded, interaksi_encoded, request.skor]], 
                               columns=['Nama KKKS_Encoded', 'Jenis Interaksi_Encoded', 'Skor'])
        
        # Predict
        pred_encoded = model.predict(features)[0]
        label = le_label.inverse_transform([pred_encoded])[0]
        
        # Probabilities
        probs = model.predict_proba(features)[0]
        confidence = float(max(probs))
        
        return PredictionResponse(label=label, confidence=confidence)
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
def retrain():
    try:
        train_logic()
        success = load_resources()
        if success:
            return {"message": "Model retrained and reloaded successfully"}
        else:
            return {"message": "Model retrained but failed to reload", "error": "Check logs"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    data_path = 'data/Dataset_Monitoring_BPMA_Interaksi_Lengkap.csv'
    if not os.path.exists(data_path):
        return {"error": "Dataset not found"}
    
    df = pd.read_csv(data_path)
    stats = {
        "total_interactions": len(df),
        "total_stakeholders": df['Nama KKKS'].nunique(),
        "label_distribution": df['Label'].value_counts().to_dict(),
        "interaction_types": df['Jenis Interaksi'].value_counts().to_dict()
    }
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
