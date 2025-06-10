"""
@file main.py
@brief Main FastAPI application entry point for the Crypto Investment Analysis System
@author [Your Name]
@date [Current Date]
@version 1.0
@copyright [Your Organization]

This module implements the main FastAPI application for the Crypto Investment Analysis System.
It provides endpoints for cryptocurrency analysis and prediction.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import predict
from api.models.schemas import PredictionResponse, ErrorResponse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Crypto Investment Analysis API",
    description="API for cryptocurrency investment analysis and prediction",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/predict", tags=["predictions"])

@app.get("/health")
async def health_check():
    """
    @brief Health check endpoint
    @return dict: Status of the API
    """
    return {"status": "healthy", "version": "1.0.0"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    @brief Global exception handler for HTTP exceptions
    @param request: The request that caused the exception
    @param exc: The exception that was raised
    @return ErrorResponse: Standardized error response
    """
    logger.error(f"HTTP Exception: {exc.detail}")
    return ErrorResponse(detail=exc.detail)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 