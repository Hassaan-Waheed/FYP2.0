# Automated Crypto Investment Analysis and Forecasting System

## Overview
A modular platform for automated multi-angle crypto asset research, combining tokenomics, technical, and sentiment analysis using machine learning. Features data ingestion, feature engineering, model training, risk assessment, and a web dashboard.

## Directory Structure
```
api/                # FastAPI backend
  main.py
  endpoints/
  models/
dashboard/          # React + Chart.js frontend
  src/
data_ingestion/     # Data ingestion microservice
feature_engineering/ # Feature engineering scripts
models/             # ML models and training
  tokenomics/
  technical/
  sentiment/
ensemble/           # Model ensembling and risk
monitoring/         # Monitoring & retraining
db/                 # Database schema/migrations
tests/              # Unit and integration tests
requirements.txt
```

## How to Train the Models
1. Prepare and clean data using scripts in `data_ingestion/` and `feature_engineering/`.
2. Train models using scripts in `models/tokenomics/`, `models/technical/`, and `models/sentiment/`.
3. Tune hyperparameters and validate using walk-forward validation.
4. Save trained models for inference.
5. Use `ensemble/ensemble_predict.py` to combine model outputs.

See module folders for detailed instructions and scripts. 