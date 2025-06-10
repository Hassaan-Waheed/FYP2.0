"""
@file model_service.py
@brief Model service for crypto investment analysis
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module implements the model service for the Crypto Investment
Analysis System, handling model training and inference.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import torch
import numpy as np
from models.technical.train_cnn_lstm import train_model as train_cnn_lstm
from models.technical.infer_cnn_lstm import load_model as load_cnn_lstm
from models.sentiment.train_finbert import train_model as train_finbert
from models.sentiment.infer_finbert import load_model as load_finbert
from models.ensemble.ensemble_model import EnsembleModel

# Configure logging
logger = logging.getLogger(__name__)


class ModelService:
    """Service for handling model training and inference."""

    def __init__(self):
        """Initialize model service."""
        self.models = {}
        logger.info("Model service initialized")

    async def train_models(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Train all models.
        
        @param data: Training data
        @param config: Training configuration
        @return: Training results
        """
        try:
            results = {}
            
            # Train CNN-LSTM
            cnn_lstm_results = await self._train_cnn_lstm(
                data["technical"],
                config["cnn_lstm"]
            )
            results["cnn_lstm"] = cnn_lstm_results
            
            # Train FinBERT
            finbert_results = await self._train_finbert(
                data["sentiment"],
                config["finbert"]
            )
            results["finbert"] = finbert_results
            
            # Train ensemble
            ensemble_results = await self._train_ensemble(
                data,
                config["ensemble"]
            )
            results["ensemble"] = ensemble_results
            
            return results

        except Exception as e:
            logger.error(f"Model training failed: {str(e)}")
            raise

    async def _train_cnn_lstm(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Train CNN-LSTM model.
        
        @param data: Technical data
        @param config: Model configuration
        @return: Training results
        """
        try:
            model, metrics = await train_cnn_lstm(data, config)
            self.models["cnn_lstm"] = model
            return metrics

        except Exception as e:
            logger.error(f"CNN-LSTM training failed: {str(e)}")
            raise

    async def _train_finbert(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Train FinBERT model.
        
        @param data: Sentiment data
        @param config: Model configuration
        @return: Training results
        """
        try:
            model, metrics = await train_finbert(data, config)
            self.models["finbert"] = model
            return metrics

        except Exception as e:
            logger.error(f"FinBERT training failed: {str(e)}")
            raise

    async def _train_ensemble(
        self,
        data: Dict[str, Any],
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Train ensemble model.
        
        @param data: All training data
        @param config: Model configuration
        @return: Training results
        """
        try:
            model = EnsembleModel(config)
            metrics = await model.train(data)
            self.models["ensemble"] = model
            return metrics

        except Exception as e:
            logger.error(f"Ensemble training failed: {str(e)}")
            raise

    async def predict(
        self,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make predictions using all models.
        
        @param features: Input features
        @return: Model predictions
        """
        try:
            predictions = {}
            
            # CNN-LSTM prediction
            if "cnn_lstm" in self.models:
                cnn_lstm_pred = await self._predict_cnn_lstm(
                    features["technical"]
                )
                predictions["cnn_lstm"] = cnn_lstm_pred
            
            # FinBERT prediction
            if "finbert" in self.models:
                finbert_pred = await self._predict_finbert(
                    features["sentiment"]
                )
                predictions["finbert"] = finbert_pred
            
            # Ensemble prediction
            if "ensemble" in self.models:
                ensemble_pred = await self._predict_ensemble(features)
                predictions["ensemble"] = ensemble_pred
            
            return predictions

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise

    async def _predict_cnn_lstm(
        self,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make CNN-LSTM prediction.
        
        @param features: Technical features
        @return: Model prediction
        """
        try:
            model = self.models["cnn_lstm"]
            prediction, confidence = await model.predict(features)
            return {
                "prediction": prediction,
                "confidence": confidence
            }

        except Exception as e:
            logger.error(f"CNN-LSTM prediction failed: {str(e)}")
            raise

    async def _predict_finbert(
        self,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make FinBERT prediction.
        
        @param features: Sentiment features
        @return: Model prediction
        """
        try:
            model = self.models["finbert"]
            prediction, confidence = await model.predict(features)
            return {
                "prediction": prediction,
                "confidence": confidence
            }

        except Exception as e:
            logger.error(f"FinBERT prediction failed: {str(e)}")
            raise

    async def _predict_ensemble(
        self,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make ensemble prediction.
        
        @param features: All features
        @return: Model prediction
        """
        try:
            model = self.models["ensemble"]
            prediction, confidence = await model.predict(features)
            return {
                "prediction": prediction,
                "confidence": confidence
            }

        except Exception as e:
            logger.error(f"Ensemble prediction failed: {str(e)}")
            raise 