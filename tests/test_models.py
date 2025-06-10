"""
@file test_models.py
@brief Test suite for machine learning models
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module contains test cases for the machine learning models of the
Crypto Investment Analysis System. It includes unit tests for model training,
inference, and performance metrics.
"""

import pytest
import numpy as np
import torch
from models.technical.train_cnn_lstm import CNNLSTMModel, train_model
from models.technical.infer_cnn_lstm import load_model, predict
from models.sentiment.train_finbert import train_finbert
from models.sentiment.infer_finbert import load_sentiment_model, predict_sentiment
from models.ensemble.ensemble_model import EnsembleModel
import pandas as pd
from sklearn.metrics import mean_squared_error, accuracy_score

# Test data
SAMPLE_SEQUENCE_LENGTH = 100
SAMPLE_FEATURE_DIM = 10
SAMPLE_BATCH_SIZE = 32
SAMPLE_TEXTS = [
    "Bitcoin price is expected to rise",
    "Ethereum shows strong fundamentals",
    "Crypto market is volatile"
]

def test_cnn_lstm_model_architecture():
    """
    @brief Test CNN-LSTM model architecture
    """
    model = CNNLSTMModel(
        input_dim=SAMPLE_FEATURE_DIM,
        hidden_dim=64,
        num_layers=2,
        output_dim=1
    )
    
    # Test model initialization
    assert isinstance(model, torch.nn.Module)
    assert hasattr(model, "conv1d")
    assert hasattr(model, "lstm")
    assert hasattr(model, "fc")
    
    # Test forward pass
    x = torch.randn(SAMPLE_BATCH_SIZE, SAMPLE_SEQUENCE_LENGTH, SAMPLE_FEATURE_DIM)
    output = model(x)
    assert output.shape == (SAMPLE_BATCH_SIZE, 1)

def test_cnn_lstm_training():
    """
    @brief Test CNN-LSTM model training
    """
    # Generate dummy data
    X = torch.randn(SAMPLE_BATCH_SIZE, SAMPLE_SEQUENCE_LENGTH, SAMPLE_FEATURE_DIM)
    y = torch.randn(SAMPLE_BATCH_SIZE, 1)
    
    # Train model
    model, loss_history = train_model(
        model=CNNLSTMModel(SAMPLE_FEATURE_DIM, 64, 2, 1),
        X=X,
        y=y,
        epochs=2,
        batch_size=SAMPLE_BATCH_SIZE
    )
    
    # Check training results
    assert isinstance(model, CNNLSTMModel)
    assert isinstance(loss_history, list)
    assert len(loss_history) > 0
    assert all(isinstance(loss, float) for loss in loss_history)

def test_cnn_lstm_inference():
    """
    @brief Test CNN-LSTM model inference
    """
    # Load model
    model = load_model("models/technical/saved/cnn_lstm_model.pt")
    
    # Generate test data
    X = torch.randn(1, SAMPLE_SEQUENCE_LENGTH, SAMPLE_FEATURE_DIM)
    
    # Make prediction
    prediction, confidence = predict(model, X)
    
    # Check prediction results
    assert isinstance(prediction, float)
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 1

def test_finbert_training():
    """
    @brief Test FinBERT model training
    """
    # Generate dummy data
    texts = SAMPLE_TEXTS
    labels = [1, 1, 0]  # Positive, Positive, Negative
    
    # Train model
    model, tokenizer = train_finbert(texts, labels, epochs=2)
    
    # Check training results
    assert model is not None
    assert tokenizer is not None

def test_finbert_inference():
    """
    @brief Test FinBERT model inference
    """
    # Load model
    model, tokenizer = load_sentiment_model("models/sentiment/saved/finbert_model")
    
    # Test prediction
    for text in SAMPLE_TEXTS:
        sentiment, confidence = predict_sentiment(model, tokenizer, text)
        assert isinstance(sentiment, str)
        assert sentiment in ["positive", "negative", "neutral"]
        assert isinstance(confidence, float)
        assert 0 <= confidence <= 1

def test_ensemble_model():
    """
    @brief Test ensemble model
    """
    # Initialize ensemble model
    ensemble = EnsembleModel()
    
    # Generate dummy predictions
    technical_pred = np.random.rand(10)
    sentiment_pred = np.random.rand(10)
    onchain_pred = np.random.rand(10)
    
    # Test ensemble prediction
    final_pred, confidence = ensemble.predict(
        technical_pred,
        sentiment_pred,
        onchain_pred
    )
    
    # Check prediction results
    assert isinstance(final_pred, float)
    assert isinstance(confidence, float)
    assert 0 <= confidence <= 1

def test_model_performance_metrics():
    """
    @brief Test model performance metrics
    """
    # Generate dummy data
    y_true = np.random.rand(100)
    y_pred = y_true + np.random.normal(0, 0.1, 100)
    
    # Calculate metrics
    mse = mean_squared_error(y_true, y_pred)
    accuracy = accuracy_score(y_true > 0.5, y_pred > 0.5)
    
    # Check metrics
    assert isinstance(mse, float)
    assert isinstance(accuracy, float)
    assert 0 <= accuracy <= 1

def test_model_robustness():
    """
    @brief Test model robustness
    """
    # Test with noisy data
    X_noisy = torch.randn(SAMPLE_BATCH_SIZE, SAMPLE_SEQUENCE_LENGTH, SAMPLE_FEATURE_DIM) + 0.1 * torch.randn(SAMPLE_BATCH_SIZE, SAMPLE_SEQUENCE_LENGTH, SAMPLE_FEATURE_DIM)
    model = CNNLSTMModel(SAMPLE_FEATURE_DIM, 64, 2, 1)
    
    # Check if model can handle noisy input
    try:
        output = model(X_noisy)
        assert output.shape == (SAMPLE_BATCH_SIZE, 1)
    except Exception as e:
        pytest.fail(f"Model failed to handle noisy data: {str(e)}")

def test_model_save_load():
    """
    @brief Test model save and load functionality
    """
    # Create and save model
    model = CNNLSTMModel(SAMPLE_FEATURE_DIM, 64, 2, 1)
    torch.save(model.state_dict(), "test_model.pt")
    
    # Load model
    loaded_model = CNNLSTMModel(SAMPLE_FEATURE_DIM, 64, 2, 1)
    loaded_model.load_state_dict(torch.load("test_model.pt"))
    
    # Compare models
    x = torch.randn(1, SAMPLE_SEQUENCE_LENGTH, SAMPLE_FEATURE_DIM)
    assert torch.allclose(model(x), loaded_model(x)) 