"""
@file ensemble_model.py
@brief Ensemble model for combining predictions
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module implements the ensemble model that combines predictions
from different models (technical, sentiment, etc.) into a final prediction.
"""

from typing import Dict, Any, List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class EnsembleModel:
    """Ensemble model for combining multiple predictions."""
    
    def __init__(self):
        """Initialize the ensemble model."""
        self.weights = {
            'technical': 0.4,
            'sentiment': 0.3,
            'fundamental': 0.2,
            'onchain': 0.1
        }
        logger.info("Ensemble model initialized")

    def predict(self, predictions: Dict[str, float]) -> float:
        """
        Combine multiple predictions into a final prediction.
        
        @param predictions: Dictionary of predictions from different models
        @return: Combined prediction score
        """
        try:
            weighted_sum = 0
            total_weight = 0
            
            for model_name, prediction in predictions.items():
                if model_name in self.weights:
                    weighted_sum += prediction * self.weights[model_name]
                    total_weight += self.weights[model_name]
            
            if total_weight == 0:
                return 0.5  # Default neutral prediction
            
            return weighted_sum / total_weight
            
        except Exception as e:
            logger.error(f"Ensemble prediction failed: {str(e)}")
            return 0.5  # Return neutral prediction on error

    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """
        Update the weights for different models.
        
        @param new_weights: Dictionary of new weights
        """
        try:
            # Validate weights sum to 1
            total = sum(new_weights.values())
            if not 0.99 <= total <= 1.01:  # Allow for small floating point errors
                raise ValueError("Weights must sum to 1")
            
            self.weights = new_weights
            logger.info("Ensemble weights updated")
            
        except Exception as e:
            logger.error(f"Failed to update weights: {str(e)}")
            raise 