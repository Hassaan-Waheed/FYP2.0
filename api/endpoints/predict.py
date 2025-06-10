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
    ErrorResponse
)
from api.services.prediction_service import PredictionService
from api.services.feature_service import FeatureService
from api.services.monitoring_service import MonitoringService
from database.session import get_db

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
    
    @param request: Prediction request
    @param db: Database session
    @return: Prediction response
    """
    try:
        # Initialize services
        feature_service = FeatureService()
        prediction_service = PredictionService()
        monitoring_service = MonitoringService()
        
        # Extract features
        features = await feature_service.get_features(request.ticker)
        
        # Make prediction
        prediction = await prediction_service.predict(features)
        
        # Monitor prediction
        monitoring_results = await monitoring_service.monitor_prediction(
            prediction,
            features
        )
        
        # Store results
        await prediction_service.store_prediction(
            request.ticker,
            prediction,
            features,
            monitoring_results
        )
        
        return {
            "ticker": request.ticker,
            "prediction": prediction,
            "features": features,
            "monitoring": monitoring_results,
            "timestamp": monitoring_results["timestamp"]
        }

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


@router.get("/predict/{ticker}/features")
async def get_features(ticker: str) -> Dict[str, Any]:
    """
    @brief Get features for a given cryptocurrency ticker
    @param ticker: Cryptocurrency ticker symbol
    @return: Dictionary containing all features
    """
    try:
        features = await feature_service.get_features(ticker)
        return features

    except Exception as e:
        logger.error(f"Error in features endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/predict/{ticker}/confidence")
async def get_confidence(ticker: str) -> Dict[str, float]:
    """
    @brief Get prediction confidence for a given cryptocurrency ticker
    @param ticker: Cryptocurrency ticker symbol
    @return: Dictionary containing confidence scores
    """
    try:
        confidence = await prediction_service.get_confidence(ticker)
        return confidence

    except Exception as e:
        logger.error(f"Error in confidence endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        ) 