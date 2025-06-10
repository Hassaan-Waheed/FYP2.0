"""
@file test_feature_engineering.py
@brief Test suite for feature engineering components
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module contains test cases for the feature engineering components of the
Crypto Investment Analysis System. It includes unit tests for technical,
sentiment, and on-chain feature extraction.
"""

import pytest
import numpy as np
import pandas as pd
from feature_engineering.technical_features import extract_technical_features
from feature_engineering.sentiment_features import extract_sentiment_features
from feature_engineering.onchain_features import extract_onchain_features
from feature_engineering.feature_combiner import combine_features
from datetime import datetime, timedelta

# Test data
SAMPLE_PRICE_DATA = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    'open': np.random.rand(100) * 1000,
    'high': np.random.rand(100) * 1000,
    'low': np.random.rand(100) * 1000,
    'close': np.random.rand(100) * 1000,
    'volume': np.random.rand(100) * 1000000
})

SAMPLE_SOCIAL_DATA = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    'mentions': np.random.randint(0, 1000, 100),
    'sentiment': np.random.rand(100),
    'tweets': ['Sample tweet ' + str(i) for i in range(100)]
})

SAMPLE_ONCHAIN_DATA = pd.DataFrame({
    'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    'transactions': np.random.randint(0, 10000, 100),
    'volume': np.random.rand(100) * 1000000,
    'holders': np.random.randint(0, 1000000, 100)
})

def test_technical_feature_extraction():
    """
    @brief Test technical feature extraction
    """
    features = extract_technical_features(SAMPLE_PRICE_DATA)
    
    # Check feature types and shapes
    assert isinstance(features, pd.DataFrame)
    assert len(features) == len(SAMPLE_PRICE_DATA)
    
    # Check for common technical indicators
    required_features = [
        'sma_20', 'sma_50', 'rsi_14', 'macd',
        'bollinger_upper', 'bollinger_lower',
        'volume_sma_20'
    ]
    for feature in required_features:
        assert feature in features.columns
        assert not features[feature].isnull().any()

def test_sentiment_feature_extraction():
    """
    @brief Test sentiment feature extraction
    """
    features = extract_sentiment_features(SAMPLE_SOCIAL_DATA)
    
    # Check feature types and shapes
    assert isinstance(features, pd.DataFrame)
    assert len(features) == len(SAMPLE_SOCIAL_DATA)
    
    # Check for sentiment features
    required_features = [
        'sentiment_score', 'sentiment_volatility',
        'mention_volume', 'mention_velocity'
    ]
    for feature in required_features:
        assert feature in features.columns
        assert not features[feature].isnull().any()

def test_onchain_feature_extraction():
    """
    @brief Test on-chain feature extraction
    """
    features = extract_onchain_features(SAMPLE_ONCHAIN_DATA)
    
    # Check feature types and shapes
    assert isinstance(features, pd.DataFrame)
    assert len(features) == len(SAMPLE_ONCHAIN_DATA)
    
    # Check for on-chain features
    required_features = [
        'transaction_volume', 'holder_growth',
        'network_activity', 'gas_usage'
    ]
    for feature in required_features:
        assert feature in features.columns
        assert not features[feature].isnull().any()

def test_feature_combiner():
    """
    @brief Test feature combination
    """
    technical_features = extract_technical_features(SAMPLE_PRICE_DATA)
    sentiment_features = extract_sentiment_features(SAMPLE_SOCIAL_DATA)
    onchain_features = extract_onchain_features(SAMPLE_ONCHAIN_DATA)
    
    combined_features = combine_features(
        technical_features,
        sentiment_features,
        onchain_features
    )
    
    # Check combined features
    assert isinstance(combined_features, pd.DataFrame)
    assert len(combined_features) == len(SAMPLE_PRICE_DATA)
    assert not combined_features.isnull().any()

def test_feature_normalization():
    """
    @brief Test feature normalization
    """
    features = extract_technical_features(SAMPLE_PRICE_DATA)
    
    # Check if features are normalized
    for column in features.columns:
        if column != 'timestamp':
            assert features[column].mean() >= -1
            assert features[column].mean() <= 1
            assert features[column].std() <= 1

def test_feature_temporal_alignment():
    """
    @brief Test temporal alignment of features
    """
    technical_features = extract_technical_features(SAMPLE_PRICE_DATA)
    sentiment_features = extract_sentiment_features(SAMPLE_SOCIAL_DATA)
    onchain_features = extract_onchain_features(SAMPLE_ONCHAIN_DATA)
    
    combined_features = combine_features(
        technical_features,
        sentiment_features,
        onchain_features
    )
    
    # Check temporal alignment
    assert combined_features['timestamp'].is_monotonic_increasing
    assert not combined_features['timestamp'].duplicated().any()

def test_feature_correlation():
    """
    @brief Test feature correlation analysis
    """
    features = extract_technical_features(SAMPLE_PRICE_DATA)
    
    # Calculate correlation matrix
    corr_matrix = features.corr()
    
    # Check correlation matrix properties
    assert isinstance(corr_matrix, pd.DataFrame)
    assert corr_matrix.shape[0] == corr_matrix.shape[1]
    assert (corr_matrix >= -1).all().all()
    assert (corr_matrix <= 1).all().all()

def test_feature_importance():
    """
    @brief Test feature importance calculation
    """
    features = extract_technical_features(SAMPLE_PRICE_DATA)
    
    # Calculate feature importance (example using variance)
    importance = features.var()
    
    # Check importance scores
    assert isinstance(importance, pd.Series)
    assert (importance >= 0).all()
    assert not importance.isnull().any()

def test_feature_selection():
    """
    @brief Test feature selection
    """
    features = extract_technical_features(SAMPLE_PRICE_DATA)
    
    # Select top features based on variance
    top_features = features.var().nlargest(5).index
    
    # Check selected features
    assert len(top_features) == 5
    assert all(feature in features.columns for feature in top_features)

def test_feature_pipeline():
    """
    @brief Test complete feature engineering pipeline
    """
    # Extract features
    technical_features = extract_technical_features(SAMPLE_PRICE_DATA)
    sentiment_features = extract_sentiment_features(SAMPLE_SOCIAL_DATA)
    onchain_features = extract_onchain_features(SAMPLE_ONCHAIN_DATA)
    
    # Combine features
    combined_features = combine_features(
        technical_features,
        sentiment_features,
        onchain_features
    )
    
    # Check pipeline output
    assert isinstance(combined_features, pd.DataFrame)
    assert not combined_features.isnull().any()
    assert combined_features['timestamp'].is_monotonic_increasing
    assert not combined_features['timestamp'].duplicated().any() 