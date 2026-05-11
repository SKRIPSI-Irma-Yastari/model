from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import os
import logging
from datetime import datetime

# Ensure log directory exists before initializing logging
os.makedirs('logs', exist_ok=True)

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/api_usage.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Stakeholder Monitoring API (CART)",
    description="API untuk pemantauan hubungan kerja sama stakeholder menggunakan Decision Tree CART",
    version="2.0.0"
)

# Model paths
MODEL_PATH = 'models/stakeholder_cart_model.joblib'
MAPPING_PATH = 'models/label_mapping.joblib'

# Global variables
model = None
label_mapping = None
reverse_mapping = None

def load_resources():
    global model, label_mapping, reverse_mapping
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(MAPPING_PATH):
            model = joblib.load(MODEL_PATH)
            label_mapping = joblib.load(MAPPING_PATH)
            reverse_mapping = {v: k for k, v in label_mapping.items()}
            logger.info("Machine Learning model and mappings loaded successfully.")
            return True
        else:
            logger.warning("Model files not found. Please run training script first.")
            return False
    except Exception as e:
        logger.error(f"Error loading resources: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    load_resources()

# Schemas
class PredictionRequest(BaseModel):
    nama_kkks: str = Field(..., example="Conrad Asia Energy")
    skor_komunikasi: float = Field(..., ge=1, le=3, example=3.0)
    skor_laporan: float = Field(..., ge=1, le=3, example=3.0)
    skor_rapat: float = Field(..., ge=1, le=3, example=2.5)
    skor_partisipasi: float = Field(..., ge=1, le=3, example=3.0)

class PredictionResponse(BaseModel):
    nama_kkks: str
    label: str
    confidence: float
    timestamp: str

@app.get("/")
def root():
    return {
        "status": "online",
        "model_loaded": model is not None,
        "docs": "/docs"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        if not load_resources():
            raise HTTPException(status_code=503, detail="Model is not available.")

    try:
        # Prepare features in the exact order used during training
        features = pd.DataFrame([[
            request.skor_komunikasi,
            request.skor_laporan,
            request.skor_rapat,
            request.skor_partisipasi
        ]], columns=['Skor_Komunikasi', 'Skor_Laporan', 'Skor_Rapat', 'Skor_Partisipasi'])

        # Predict
        pred_encoded = model.predict(features)[0]
        label = reverse_mapping.get(pred_encoded, "Unknown")
        
        # Get probability
        probs = model.predict_proba(features)[0]
        confidence = float(max(probs))

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log the prediction
        logger.info(f"Prediction for {request.nama_kkks}: {label} (Conf: {confidence:.2f})")

        return PredictionResponse(
            nama_kkks=request.nama_kkks,
            label=label,
            confidence=confidence,
            timestamp=timestamp
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

@app.get("/visualize-tree")
async def visualize_tree():
    tree_path = 'reports/decision_tree_visual.png'
    if os.path.exists(tree_path):
        return FileResponse(tree_path, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Tree visualization image not found. Run training first.")

@app.get("/stats")
async def get_stats():
    dataset_path = 'data/Dataset2.csv'
    if not os.path.exists(dataset_path):
        return {"error": "Dataset not found"}
    
    df = pd.read_csv(dataset_path)
    return {
        "total_records": len(df),
        "total_kkks": df['Nama KKKS'].nunique(),
        "label_distribution": df['Label_Akhir'].value_counts().to_dict(),
        "average_scores": {
            "Komunikasi": float(df['Skor_Komunikasi'].mean()),
            "Laporan": float(df['Skor_Laporan'].mean()),
            "Rapat": float(df['Skor_Rapat'].mean()),
            "Partisipasi": float(df['Skor_Partisipasi'].mean())
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
