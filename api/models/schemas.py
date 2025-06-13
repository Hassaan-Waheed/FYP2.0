"""
@file schemas.py
@brief Data models and schemas for the crypto investment system
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module defines the data models and schemas used throughout the
Crypto Investment Analysis System, including request/response models
and feature data structures.
"""

from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta


class RiskLevel(str, Enum):
    """Risk level enumeration for investment predictions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class TokenomicsFeatures(BaseModel):
    """Tokenomics features model."""
    total_supply: float = Field(..., description="Total token supply")
    circulating_supply: float = Field(..., description="Circulating supply")
    market_cap: float = Field(..., description="Market capitalization")
    token_distribution: Dict[str, float] = Field(
        ...,
        description="Token distribution percentages"
    )
    inflation_rate: float = Field(..., description="Annual inflation rate")
    staking_apy: Optional[float] = Field(None, description="Staking APY")


class TechnicalFeatures(BaseModel):
    """Technical analysis features model."""
    price: float = Field(..., description="Current price")
    volume_24h: float = Field(..., description="24-hour volume")
    price_change_24h: float = Field(..., description="24-hour price change")
    volatility: float = Field(..., description="Price volatility")
    rsi: float = Field(..., description="Relative Strength Index")
    macd: Dict[str, float] = Field(..., description="MACD indicators")
    moving_averages: Dict[str, float] = Field(
        ...,
        description="Moving averages"
    )


class SentimentFeatures(BaseModel):
    """Sentiment analysis features model."""
    overall_sentiment: float = Field(..., description="Overall sentiment score")
    social_mentions: int = Field(..., description="Social media mentions")
    news_sentiment: float = Field(..., description="News sentiment score")
    social_sentiment: float = Field(..., description="Social sentiment score")
    sentiment_volatility: float = Field(
        ...,
        description="Sentiment volatility"
    )


class OnchainFeatures(BaseModel):
    """On-chain analysis features model."""
    transaction_volume: float = Field(..., description="Transaction volume")
    active_addresses: int = Field(..., description="Active addresses")
    network_hashrate: Optional[float] = Field(
        None,
        description="Network hashrate"
    )
    gas_price: Optional[float] = Field(None, description="Gas price")
    network_utilization: float = Field(
        ...,
        description="Network utilization"
    )


class PredictionResponse(BaseModel):
    """Prediction response model."""
    ticker: str = Field(..., description="Cryptocurrency ticker")
    timestamp: datetime = Field(..., description="Prediction timestamp")
    score: float = Field(..., description="Investment score")
    risk: RiskLevel = Field(..., description="Risk level")
    predictions: Dict[str, float] = Field(
        ...,
        description="Individual model predictions"
    )
    features: Dict[str, Dict] = Field(
        ...,
        description="Feature values used for prediction"
    )
    confidence: float = Field(..., description="Prediction confidence")


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Error timestamp"
    )


class TimeFrame(str, Enum):
    """Time frame for prediction analysis."""
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1m"
    QUARTER = "3m"
    YEAR = "1y"


class AnalysisType(str, Enum):
    """Type of analysis to perform."""
    TECHNICAL = "technical"
    FUNDAMENTAL = "fundamental"
    SENTIMENT = "sentiment"
    ONCHAIN = "onchain"
    COMPREHENSIVE = "comprehensive"


class PredictionRequest(BaseModel):
    """Prediction request model with comprehensive fields."""
    # Required fields
    ticker: str = Field(..., description="Cryptocurrency ticker symbol (e.g., BTC, ETH)")
    
    # Optional fields with defaults
    timeframe: TimeFrame = Field(
        default=TimeFrame.DAY,
        description="Time frame for the prediction"
    )
    analysis_type: AnalysisType = Field(
        default=AnalysisType.COMPREHENSIVE,
        description="Type of analysis to perform"
    )
    
    # Advanced configuration
    include_technical: bool = Field(
        default=True,
        description="Include technical analysis"
    )
    include_fundamental: bool = Field(
        default=True,
        description="Include fundamental analysis"
    )
    include_sentiment: bool = Field(
        default=True,
        description="Include sentiment analysis"
    )
    include_onchain: bool = Field(
        default=True,
        description="Include on-chain analysis"
    )
    
    # Historical data parameters
    historical_days: int = Field(
        default=30,
        ge=1,
        le=365,
        description="Number of historical days to consider"
    )
    
    # Feature weights (optional)
    feature_weights: Optional[Dict[str, float]] = Field(
        default=None,
        description="Custom weights for different features"
    )
    
    # Risk parameters
    risk_tolerance: Optional[RiskLevel] = Field(
        default=None,
        description="User's risk tolerance level"
    )
    
    # Market context
    market_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional market context data"
    )
    
    # Custom indicators
    custom_indicators: Optional[List[str]] = Field(
        default=None,
        description="List of custom technical indicators to include"
    )
    
    # Validation
    @validator('ticker')
    def validate_ticker(cls, v):
        """Validate ticker symbol format."""
        if not v.isalnum():
            raise ValueError('Ticker must be alphanumeric')
        return v.upper()
    
    @validator('feature_weights')
    def validate_feature_weights(cls, v):
        """Validate feature weights sum to 1 if provided."""
        if v is not None:
            total = sum(v.values())
            if not 0.99 <= total <= 1.01:  # Allow for small floating point errors
                raise ValueError('Feature weights must sum to 1')
        return v 