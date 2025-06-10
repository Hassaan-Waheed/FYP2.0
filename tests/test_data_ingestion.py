"""
@file test_data_ingestion.py
@brief Test suite for data ingestion services
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module contains test cases for the data ingestion services of the
Crypto Investment Analysis System. It includes unit tests for market data,
social media data, and on-chain data ingestion.
"""

import pytest
from data_ingestion.ingest_market import fetch_market_data
from data_ingestion.ingest_social import fetch_social_data
from data_ingestion.ingest_onchain import fetch_onchain_data
import pandas as pd
from datetime import datetime, timedelta

# Test data
VALID_TICKERS = ["BTC", "ETH", "BNB"]
INVALID_TICKERS = ["", "INVALID", "123"]
TEST_KEYWORDS = ["bitcoin", "ethereum", "crypto"]
TEST_ADDRESSES = ["0x123", "0x456", "0x789"]

def test_fetch_market_data_valid():
    """
    @brief Test market data ingestion with valid tickers
    """
    for ticker in VALID_TICKERS:
        data = fetch_market_data(ticker)
        assert isinstance(data, dict)
        assert "price" in data
        assert "volume" in data
        assert "market_cap" in data
        assert isinstance(data["price"], float)
        assert isinstance(data["volume"], float)
        assert isinstance(data["market_cap"], float)

def test_fetch_market_data_invalid():
    """
    @brief Test market data ingestion with invalid tickers
    """
    for ticker in INVALID_TICKERS:
        with pytest.raises(Exception):
            fetch_market_data(ticker)

def test_fetch_market_data_timeframe():
    """
    @brief Test market data ingestion with different timeframes
    """
    ticker = "BTC"
    timeframes = ["1d", "1w", "1m"]
    
    for timeframe in timeframes:
        data = fetch_market_data(ticker, timeframe=timeframe)
        assert isinstance(data, dict)
        assert "price" in data
        assert "volume" in data
        assert "market_cap" in data

def test_fetch_social_data_valid():
    """
    @brief Test social media data ingestion with valid keywords
    """
    for keyword in TEST_KEYWORDS:
        data = fetch_social_data(keyword)
        assert isinstance(data, dict)
        assert "mentions" in data
        assert "sentiment" in data
        assert "tweets" in data
        assert isinstance(data["mentions"], int)
        assert isinstance(data["sentiment"], float)
        assert isinstance(data["tweets"], list)

def test_fetch_social_data_invalid():
    """
    @brief Test social media data ingestion with invalid keywords
    """
    invalid_keywords = ["", " ", "@#$%"]
    for keyword in invalid_keywords:
        with pytest.raises(Exception):
            fetch_social_data(keyword)

def test_fetch_social_data_timeframe():
    """
    @brief Test social media data ingestion with different timeframes
    """
    keyword = "bitcoin"
    timeframes = ["1h", "1d", "1w"]
    
    for timeframe in timeframes:
        data = fetch_social_data(keyword, timeframe=timeframe)
        assert isinstance(data, dict)
        assert "mentions" in data
        assert "sentiment" in data
        assert "tweets" in data

def test_fetch_onchain_data_valid():
    """
    @brief Test on-chain data ingestion with valid addresses
    """
    for address in TEST_ADDRESSES:
        data = fetch_onchain_data(address)
        assert isinstance(data, dict)
        assert "transactions" in data
        assert "volume" in data
        assert "holders" in data
        assert isinstance(data["transactions"], int)
        assert isinstance(data["volume"], float)
        assert isinstance(data["holders"], int)

def test_fetch_onchain_data_invalid():
    """
    @brief Test on-chain data ingestion with invalid addresses
    """
    invalid_addresses = ["", "invalid", "0x"]
    for address in invalid_addresses:
        with pytest.raises(Exception):
            fetch_onchain_data(address)

def test_data_consistency():
    """
    @brief Test data consistency across multiple fetches
    """
    ticker = "BTC"
    keyword = "bitcoin"
    address = "0x123"
    
    # Fetch data multiple times
    market_data1 = fetch_market_data(ticker)
    market_data2 = fetch_market_data(ticker)
    social_data1 = fetch_social_data(keyword)
    social_data2 = fetch_social_data(keyword)
    onchain_data1 = fetch_onchain_data(address)
    onchain_data2 = fetch_onchain_data(address)
    
    # Check if data is consistent
    assert market_data1["ticker"] == market_data2["ticker"]
    assert social_data1["keyword"] == social_data2["keyword"]
    assert onchain_data1["address"] == onchain_data2["address"]

def test_data_timestamps():
    """
    @brief Test if data timestamps are within expected range
    """
    ticker = "BTC"
    data = fetch_market_data(ticker)
    
    assert "timestamp" in data
    timestamp = datetime.fromisoformat(data["timestamp"])
    now = datetime.now()
    
    # Check if timestamp is within last 24 hours
    assert now - timestamp < timedelta(hours=24)

def test_error_handling():
    """
    @brief Test error handling in data ingestion
    """
    # Test with network error simulation
    with pytest.raises(Exception):
        fetch_market_data("BTC", simulate_error=True)
    
    # Test with rate limit simulation
    with pytest.raises(Exception):
        fetch_social_data("bitcoin", simulate_rate_limit=True)
    
    # Test with invalid data simulation
    with pytest.raises(Exception):
        fetch_onchain_data("0x123", simulate_invalid_data=True) 