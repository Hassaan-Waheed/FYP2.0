from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.ohlcv import OHLCV as OHLCVModel
from api.db.timescaledb import SessionLocal, OHLCV as OHLCVORM

router = APIRouter()

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ohlcv")
def ingest_ohlcv(data: OHLCVModel, db: Session = Depends(get_db)):
    db_ohlcv = OHLCVORM(**data.dict())
    db.add(db_ohlcv)
    db.commit()
    db.refresh(db_ohlcv)
    return {"status": "inserted", "id": db_ohlcv.id} 