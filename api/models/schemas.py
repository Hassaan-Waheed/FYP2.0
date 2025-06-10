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
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


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