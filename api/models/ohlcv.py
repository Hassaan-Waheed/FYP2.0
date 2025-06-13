from pydantic import BaseModel
from datetime import datetime

class OHLCV(BaseModel):
    asset_id: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float 