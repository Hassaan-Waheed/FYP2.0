"""
@file feature_service.py
@brief Feature service for crypto investment analysis
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module implements the feature service for the Crypto Investment
Analysis System, handling feature extraction and processing.
"""

from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta
from data_ingestion.ingest_market import fetch_market_data
from data_ingestion.ingest_social import fetch_social_data
from data_ingestion.ingest_onchain import fetch_onchain_data
from feature_engineering.technical_features import extract_technical_features
from feature_engineering.sentiment_features import extract_sentiment_features
from feature_engineering.onchain_features import extract_onchain_features

# Configure logging
logger = logging.getLogger(__name__)


class FeatureService:
    """Service for handling feature extraction and processing."""

    def __init__(self):
        """Initialize feature service."""
        logger.info("Feature service initialized")

    async def get_features(self, ticker: str) -> Dict[str, Any]:
        """
        @brief Get all features for a cryptocurrency
        @param ticker: Cryptocurrency ticker
        @return: Dictionary of features
        """
        try:
            # Fetch raw data
            market_data = await self._fetch_market_data(ticker)
            social_data = await self._fetch_social_data(ticker)
            onchain_data = await self._fetch_onchain_data(ticker)
            
            # Extract features
            technical_features = self._extract_technical_features(market_data)
            sentiment_features = self._extract_sentiment_features(social_data)
            onchain_features = self._extract_onchain_features(onchain_data)
            
            return {
                "technical": technical_features,
                "sentiment": sentiment_features,
                "onchain": onchain_features,
                "timestamp": datetime.now()
            }

        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            raise

    async def _fetch_market_data(
        self,
        ticker: str,
        timeframe: str = "1d"
    ) -> Dict[str, Any]:
        """
        @brief Fetch market data
        @param ticker: Cryptocurrency ticker
        @param timeframe: Data timeframe
        @return: Market data
        """
        try:
            return await fetch_market_data(ticker, timeframe)

        except Exception as e:
            logger.error(f"Market data fetch failed: {str(e)}")
            raise

    async def _fetch_social_data(
        self,
        ticker: str,
        timeframe: str = "1d"
    ) -> Dict[str, Any]:
        """
        @brief Fetch social media data
        @param ticker: Cryptocurrency ticker
        @param timeframe: Data timeframe
        @return: Social media data
        """
        try:
            return await fetch_social_data(ticker, timeframe)

        except Exception as e:
            logger.error(f"Social data fetch failed: {str(e)}")
            raise

    async def _fetch_onchain_data(
        self,
        ticker: str,
        timeframe: str = "1d"
    ) -> Dict[str, Any]:
        """
        @brief Fetch on-chain data
        @param ticker: Cryptocurrency ticker
        @param timeframe: Data timeframe
        @return: On-chain data
        """
        try:
            return await fetch_onchain_data(ticker, timeframe)

        except Exception as e:
            logger.error(f"On-chain data fetch failed: {str(e)}")
            raise

    def _extract_technical_features(
        self,
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        @brief Extract technical features
        @param market_data: Market data
        @return: Technical features
        """
        try:
            return extract_technical_features(market_data)

        except Exception as e:
            logger.error(f"Technical feature extraction failed: {str(e)}")
            raise

    def _extract_sentiment_features(
        self,
        social_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        @brief Extract sentiment features
        @param social_data: Social media data
        @return: Sentiment features
        """
        try:
            return extract_sentiment_features(social_data)

        except Exception as e:
            logger.error(f"Sentiment feature extraction failed: {str(e)}")
            raise

    def _extract_onchain_features(
        self,
        onchain_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        @brief Extract on-chain features
        @param onchain_data: On-chain data
        @return: On-chain features
        """
        try:
            return extract_onchain_features(onchain_data)

        except Exception as e:
            logger.error(f"On-chain feature extraction failed: {str(e)}")
            raise 