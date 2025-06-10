"""
@file conftest.py
@brief Test configuration and fixtures
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module contains test configuration and fixtures for the
Crypto Investment Analysis System test suite.
"""

import pytest
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="session")
def test_data_dir():
    """
    @brief Fixture for test data directory
    @return: Path to test data directory
    """
    return os.path.join(os.path.dirname(__file__), "test_data")

@pytest.fixture(scope="session")
def sample_price_data():
    """
    @brief Fixture for sample price data
    @return: DataFrame with sample price data
    """
    return pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'open': np.random.rand(100) * 1000,
        'high': np.random.rand(100) * 1000,
        'low': np.random.rand(100) * 1000,
        'close': np.random.rand(100) * 1000,
        'volume': np.random.rand(100) * 1000000
    })

@pytest.fixture(scope="session")
def sample_social_data():
    """
    @brief Fixture for sample social media data
    @return: DataFrame with sample social media data
    """
    return pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'mentions': np.random.randint(0, 1000, 100),
        'sentiment': np.random.rand(100),
        'tweets': ['Sample tweet ' + str(i) for i in range(100)]
    })

@pytest.fixture(scope="session")
def sample_onchain_data():
    """
    @brief Fixture for sample on-chain data
    @return: DataFrame with sample on-chain data
    """
    return pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'transactions': np.random.randint(0, 10000, 100),
        'volume': np.random.rand(100) * 1000000,
        'holders': np.random.randint(0, 1000000, 100)
    })

@pytest.fixture(scope="session")
def sample_model_metrics():
    """
    @brief Fixture for sample model metrics
    @return: Dictionary with sample model metrics
    """
    return {
        'accuracy': 0.85,
        'precision': 0.82,
        'recall': 0.88,
        'f1_score': 0.85
    }

@pytest.fixture(scope="session")
def sample_predictions():
    """
    @brief Fixture for sample model predictions
    @return: DataFrame with sample predictions
    """
    return pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
        'predicted': np.random.rand(100),
        'actual': np.random.rand(100),
        'confidence': np.random.rand(100)
    })

@pytest.fixture(scope="session")
def test_config():
    """
    @brief Fixture for test configuration
    @return: Dictionary with test configuration
    """
    return {
        'api': {
            'host': 'localhost',
            'port': 8000,
            'debug': True
        },
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'test_db',
            'user': 'test_user',
            'password': 'test_password'
        },
        'models': {
            'technical': {
                'path': 'models/technical/saved',
                'threshold': 0.8
            },
            'sentiment': {
                'path': 'models/sentiment/saved',
                'threshold': 0.7
            }
        },
        'monitoring': {
            'metrics_path': 'monitoring/metrics',
            'alert_threshold': 0.9
        }
    }

@pytest.fixture(scope="session")
def mock_api_client():
    """
    @brief Fixture for mock API client
    @return: Mock API client
    """
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)

@pytest.fixture(scope="session")
def mock_database():
    """
    @brief Fixture for mock database
    @return: Mock database connection
    """
    class MockDB:
        def __init__(self):
            self.data = {}
        
        def insert(self, collection, data):
            if collection not in self.data:
                self.data[collection] = []
            self.data[collection].append(data)
        
        def find(self, collection, query=None):
            if collection not in self.data:
                return []
            if query is None:
                return self.data[collection]
            return [doc for doc in self.data[collection] if all(doc[k] == v for k, v in query.items())]
    
    return MockDB()

@pytest.fixture(scope="session")
def mock_model():
    """
    @brief Fixture for mock ML model
    @return: Mock ML model
    """
    class MockModel:
        def __init__(self):
            self.predictions = []
        
        def predict(self, X):
            return np.random.rand(len(X))
        
        def predict_proba(self, X):
            return np.random.rand(len(X), 2)
    
    return MockModel()

@pytest.fixture(scope="session")
def mock_monitor():
    """
    @brief Fixture for mock monitoring system
    @return: Mock monitoring system
    """
    class MockMonitor:
        def __init__(self):
            self.metrics = {}
            self.alerts = []
        
        def update_metrics(self, metrics):
            self.metrics.update(metrics)
        
        def generate_alert(self, level, message):
            alert = {
                'timestamp': datetime.now(),
                'level': level,
                'message': message
            }
            self.alerts.append(alert)
            return alert
    
    return MockMonitor()

@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    @brief Fixture for test environment setup
    """
    # Create test directories
    os.makedirs('tests/test_data', exist_ok=True)
    os.makedirs('tests/test_output', exist_ok=True)
    
    # Set test environment variables
    os.environ['TESTING'] = 'true'
    os.environ['ENVIRONMENT'] = 'test'
    
    yield
    
    # Cleanup after tests
    import shutil
    shutil.rmtree('tests/test_output', ignore_errors=True) 