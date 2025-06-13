"""
@file predict.py
@brief Prediction endpoint for crypto investment analysis
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module implements the prediction endpoint for the Crypto Investment
Analysis System, handling model predictions and feature extraction.
"""

from typing import Dict, Any
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models.schemas import (
    PredictionRequest,
    PredictionResponse,
    ErrorResponse,
    AnalysisType,
    TimeFrame
)
from api.services.prediction_service import PredictionService
from api.services.feature_service import FeatureService
from api.services.monitoring_service import MonitoringService
from database.session import get_db
from api.db.timescaledb import SessionLocal, ModelPrediction
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Make prediction for a cryptocurrency.
    
    @param request: Prediction request containing analysis parameters
    @param db: Database session
    @return: Prediction response with analysis results
    """
    try:
        # Initialize services
        feature_service = FeatureService()
        prediction_service = PredictionService()
        monitoring_service = MonitoringService()
        
        # Extract features based on request parameters
        features = await feature_service.get_features(
            ticker=request.ticker,
            timeframe=request.timeframe,
            include_technical=request.include_technical,
            include_fundamental=request.include_fundamental,
            include_sentiment=request.include_sentiment,
            include_onchain=request.include_onchain,
            historical_days=request.historical_days
        )
        
        # Make prediction with custom weights if provided
        prediction = await prediction_service.predict(
            features=features,
            analysis_type=request.analysis_type,
            feature_weights=request.feature_weights,
            risk_tolerance=request.risk_tolerance
        )
        
        # Monitor prediction
        monitoring_results = await monitoring_service.monitor_prediction(
            prediction=prediction,
            features=features,
            market_context=request.market_context
        )
        
        # Store results
        await prediction_service.store_prediction(
            ticker=request.ticker,
            prediction=prediction,
            features=features,
            monitoring_results=monitoring_results
        )
        
        # After each model prediction, log to DB
        for model_name, pred in prediction["predictions"].items():
            db_pred = ModelPrediction(
                asset_id=request.ticker,
                model_name=model_name,
                prediction=pred,
                score=prediction["score"],
                created_at=datetime.now(),
                extra=None
            )
            db.add(db_pred)
        db.commit()
        
        return {
            "ticker": request.ticker,
            "prediction": prediction,
            "features": features,
            "monitoring": monitoring_results,
            "timestamp": monitoring_results["timestamp"]
        }

    except ValueError as e:
        logger.error(f"Invalid request parameters: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request parameters: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get(
    "/predict/{ticker}",
    response_model=PredictionResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_prediction(
    ticker: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get latest prediction for a cryptocurrency.
    
    @param ticker: Cryptocurrency ticker
    @param db: Database session
    @return: Latest prediction
    """
    try:
        prediction_service = PredictionService()
        prediction = await prediction_service.get_latest_prediction(ticker)
        
        if not prediction:
            raise HTTPException(
                status_code=404,
                detail=f"No prediction found for {ticker}"
            )
        
        return prediction

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get prediction: {str(e)}"
        )

@router.get(
    "/predict/{ticker}/features",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_features(ticker: str) -> Dict[str, Any]:
    """
    Get features for a given cryptocurrency ticker.
    
    @param ticker: Cryptocurrency ticker symbol
    @return: Dictionary containing all features
    """
    try:
        feature_service = FeatureService()
        features = await feature_service.get_features(ticker)
        
        if not features:
            raise HTTPException(
                status_code=404,
                detail=f"No features found for {ticker}"
            )
            
        return features

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in features endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving features: {str(e)}"
        )

@router.get(
    "/predict/{ticker}/confidence",
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_confidence(ticker: str) -> Dict[str, float]:
    """
    Get prediction confidence for a given cryptocurrency ticker.
    
    @param ticker: Cryptocurrency ticker symbol
    @return: Dictionary containing confidence scores
    """
    try:
        prediction_service = PredictionService()
        confidence = await prediction_service.get_confidence(ticker)
        
        if not confidence:
            raise HTTPException(
                status_code=404,
                detail=f"No confidence data found for {ticker}"
            )
            
        return confidence

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in confidence endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving confidence: {str(e)}"
        ) 