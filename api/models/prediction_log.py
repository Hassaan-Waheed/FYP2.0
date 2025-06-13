from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class ModelPredictionLog(BaseModel):
    asset_id: str
    model_name: str
    prediction: float
    score: float
    created_at: datetime
    extra: Optional[Dict[str, Any]] = None 