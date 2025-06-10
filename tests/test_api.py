"""
@file test_api.py
@brief Test suite for API endpoints
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module contains test cases for the Crypto Investment Analysis System API.
It includes unit tests, integration tests, and performance tests.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.models.schemas import RiskLevel
import time
import json

client = TestClient(app)

# Test data
VALID_TICKERS = ["BTC", "ETH", "BNB"]
INVALID_TICKERS = ["", "INVALID", "123"]

def test_health_check():
    """
    @brief Test health check endpoint
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "version" in data

@pytest.mark.parametrize("ticker", VALID_TICKERS)
def test_predict_valid_ticker(ticker):
    """
    @brief Test prediction endpoint with valid tickers
    @param ticker: Valid cryptocurrency ticker
    """
    response = client.get(f"/predict/{ticker}")
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "ticker" in data
    assert "score" in data
    assert "risk" in data
    assert "predictions" in data
    assert "features" in data
    assert "confidence" in data
    
    # Check data types
    assert isinstance(data["score"], float)
    assert data["risk"] in [level.value for level in RiskLevel]
    assert isinstance(data["predictions"], dict)
    assert isinstance(data["features"], dict)
    assert isinstance(data["confidence"], float)

@pytest.mark.parametrize("ticker", INVALID_TICKERS)
def test_predict_invalid_ticker(ticker):
    """
    @brief Test prediction endpoint with invalid tickers
    @param ticker: Invalid cryptocurrency ticker
    """
    response = client.get(f"/predict/{ticker}")
    assert response.status_code in [400, 404, 500]
    if response.status_code == 500:
        data = response.json()
        assert "detail" in data

def test_predict_response_time():
    """
    @brief Test prediction endpoint response time
    """
    start_time = time.time()
    response = client.get("/predict/BTC")
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 5.0  # Response should be under 5 seconds

def test_predict_concurrent_requests():
    """
    @brief Test prediction endpoint with concurrent requests
    """
    import concurrent.futures
    
    def make_request(ticker):
        return client.get(f"/predict/{ticker}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(make_request, ticker) for ticker in VALID_TICKERS]
        responses = [future.result() for future in futures]
    
    assert all(response.status_code == 200 for response in responses)

def test_predict_error_handling():
    """
    @brief Test prediction endpoint error handling
    """
    # Test with empty ticker
    response = client.get("/predict/")
    assert response.status_code == 404
    
    # Test with very long ticker
    response = client.get("/predict/" + "A" * 100)
    assert response.status_code in [400, 404, 500]
    
    # Test with special characters
    response = client.get("/predict/BTC@ETH")
    assert response.status_code in [400, 404, 500]

def test_predict_response_consistency():
    """
    @brief Test prediction endpoint response consistency
    """
    # Make multiple requests for the same ticker
    responses = []
    for _ in range(3):
        response = client.get("/predict/BTC")
        assert response.status_code == 200
        responses.append(response.json())
    
    # Check if responses are consistent
    first_response = responses[0]
    for response in responses[1:]:
        assert response["ticker"] == first_response["ticker"]
        assert response["risk"] == first_response["risk"]
        assert abs(response["score"] - first_response["score"]) < 0.1  # Allow small variations 