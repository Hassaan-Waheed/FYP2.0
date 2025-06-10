"""
@file monitoring_service.py
@brief Monitoring service for crypto investment analysis
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module implements the monitoring service for the Crypto Investment
Analysis System, handling model performance monitoring and alerts.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
import numpy as np
from prometheus_client import Counter, Gauge, Histogram
from monitoring.performance_metrics import (
    calculate_metrics,
    check_thresholds,
    generate_alert
)
from monitoring.data_quality import (
    check_data_quality,
    validate_features,
    check_data_drift
)

# Configure logging
logger = logging.getLogger(__name__)

# Prometheus metrics
PREDICTION_COUNTER = Counter(
    'model_predictions_total',
    'Total number of predictions made'
)
PREDICTION_LATENCY = Histogram(
    'prediction_latency_seconds',
    'Time spent processing predictions'
)
MODEL_ACCURACY = Gauge(
    'model_accuracy',
    'Model accuracy score'
)
FEATURE_DRIFT = Gauge(
    'feature_drift_score',
    'Feature drift detection score'
)


class MonitoringService:
    """Service for handling model monitoring and alerts."""

    def __init__(self):
        """Initialize monitoring service."""
        logger.info("Monitoring service initialized")

    async def monitor_prediction(
        self,
        prediction: Dict[str, Any],
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        @brief Monitor a single prediction
        @param prediction: Model prediction
        @param features: Input features
        @return: Monitoring results
        """
        try:
            # Update metrics
            PREDICTION_COUNTER.inc()
            
            # Check data quality
            quality_metrics = await self._check_data_quality(features)
            
            # Check for drift
            drift_metrics = await self._check_drift(features)
            
            # Generate monitoring report
            return {
                "timestamp": datetime.now(),
                "quality_metrics": quality_metrics,
                "drift_metrics": drift_metrics,
                "alerts": self._generate_alerts(
                    quality_metrics,
                    drift_metrics
                )
            }

        except Exception as e:
            logger.error(f"Prediction monitoring failed: {str(e)}")
            raise

    async def _check_data_quality(
        self,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        @brief Check data quality
        @param features: Input features
        @return: Quality metrics
        """
        try:
            return check_data_quality(features)

        except Exception as e:
            logger.error(f"Data quality check failed: {str(e)}")
            raise

    async def _check_drift(
        self,
        features: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        @brief Check for data drift
        @param features: Input features
        @return: Drift metrics
        """
        try:
            return check_data_drift(features)

        except Exception as e:
            logger.error(f"Drift check failed: {str(e)}")
            raise

    def _generate_alerts(
        self,
        quality_metrics: Dict[str, Any],
        drift_metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        @brief Generate alerts based on metrics
        @param quality_metrics: Data quality metrics
        @param drift_metrics: Drift detection metrics
        @return: List of alerts
        """
        alerts = []
        
        # Check quality thresholds
        quality_alerts = check_thresholds(quality_metrics)
        if quality_alerts:
            alerts.extend(quality_alerts)
        
        # Check drift thresholds
        drift_alerts = check_thresholds(drift_metrics)
        if drift_alerts:
            alerts.extend(drift_alerts)
        
        return alerts

    async def update_model_metrics(
        self,
        metrics: Dict[str, float]
    ) -> None:
        """
        @brief Update model performance metrics
        @param metrics: Model performance metrics
        """
        try:
            # Update Prometheus metrics
            MODEL_ACCURACY.set(metrics.get("accuracy", 0.0))
            FEATURE_DRIFT.set(metrics.get("drift_score", 0.0))
            
            logger.info(f"Model metrics updated: {metrics}")

        except Exception as e:
            logger.error(f"Failed to update model metrics: {str(e)}")
            raise 