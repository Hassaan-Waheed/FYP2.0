"""
@file data_service.py
@brief Data service for crypto investment analysis
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module implements the data service for the Crypto Investment
Analysis System, handling data ingestion and storage.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import Session
from data_ingestion.ingest_market import fetch_market_data
from data_ingestion.ingest_social import fetch_social_data
from data_ingestion.ingest_onchain import fetch_onchain_data
from database.models import (
    MarketData,
    SocialData,
    OnchainData,
    FeatureData
)

# Configure logging
logger = logging.getLogger(__name__)


class DataService:
    """Service for handling data ingestion and storage."""

    def __init__(self, db_session: Session):
        """
        Initialize data service.
        
        @param db_session: Database session
        """
        self.db = db_session
        logger.info("Data service initialized")

    async def ingest_market_data(
        self,
        ticker: str,
        timeframe: str = "1d"
    ) -> Dict[str, Any]:
        """
        Ingest market data for a cryptocurrency.
        
        @param ticker: Cryptocurrency ticker
        @param timeframe: Data timeframe
        @return: Ingested market data
        """
        try:
            # Fetch data
            data = await fetch_market_data(ticker, timeframe)
            
            # Store in database
            market_data = MarketData(
                ticker=ticker,
                timestamp=datetime.now(),
                data=data
            )
            self.db.add(market_data)
            self.db.commit()
            
            return data

        except Exception as e:
            logger.error(f"Market data ingestion failed: {str(e)}")
            raise

    async def ingest_social_data(
        self,
        ticker: str,
        timeframe: str = "1d"
    ) -> Dict[str, Any]:
        """
        Ingest social media data for a cryptocurrency.
        
        @param ticker: Cryptocurrency ticker
        @param timeframe: Data timeframe
        @return: Ingested social data
        """
        try:
            # Fetch data
            data = await fetch_social_data(ticker, timeframe)
            
            # Store in database
            social_data = SocialData(
                ticker=ticker,
                timestamp=datetime.now(),
                data=data
            )
            self.db.add(social_data)
            self.db.commit()
            
            return data

        except Exception as e:
            logger.error(f"Social data ingestion failed: {str(e)}")
            raise

    async def ingest_onchain_data(
        self,
        ticker: str,
        timeframe: str = "1d"
    ) -> Dict[str, Any]:
        """
        Ingest on-chain data for a cryptocurrency.
        
        @param ticker: Cryptocurrency ticker
        @param timeframe: Data timeframe
        @return: Ingested on-chain data
        """
        try:
            # Fetch data
            data = await fetch_onchain_data(ticker, timeframe)
            
            # Store in database
            onchain_data = OnchainData(
                ticker=ticker,
                timestamp=datetime.now(),
                data=data
            )
            self.db.add(onchain_data)
            self.db.commit()
            
            return data

        except Exception as e:
            logger.error(f"On-chain data ingestion failed: {str(e)}")
            raise

    def store_features(
        self,
        ticker: str,
        features: Dict[str, Any]
    ) -> None:
        """
        Store extracted features in database.
        
        @param ticker: Cryptocurrency ticker
        @param features: Extracted features
        """
        try:
            feature_data = FeatureData(
                ticker=ticker,
                timestamp=datetime.now(),
                features=features
            )
            self.db.add(feature_data)
            self.db.commit()
            
            logger.info(f"Features stored for {ticker}")

        except Exception as e:
            logger.error(f"Feature storage failed: {str(e)}")
            raise

    def get_latest_data(
        self,
        ticker: str,
        data_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get latest data for a cryptocurrency.
        
        @param ticker: Cryptocurrency ticker
        @param data_type: Type of data to retrieve
        @return: Latest data or None if not found
        """
        try:
            if data_type == "market":
                data = self.db.query(MarketData).filter(
                    MarketData.ticker == ticker
                ).order_by(
                    MarketData.timestamp.desc()
                ).first()
            elif data_type == "social":
                data = self.db.query(SocialData).filter(
                    SocialData.ticker == ticker
                ).order_by(
                    SocialData.timestamp.desc()
                ).first()
            elif data_type == "onchain":
                data = self.db.query(OnchainData).filter(
                    OnchainData.ticker == ticker
                ).order_by(
                    OnchainData.timestamp.desc()
                ).first()
            else:
                raise ValueError(f"Unknown data type: {data_type}")
            
            return data.data if data else None

        except Exception as e:
            logger.error(f"Data retrieval failed: {str(e)}")
            raise 