import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import JSONB
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:5432/crypto_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Asset(Base):
    __tablename__ = "asset"
    id = Column(String, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    ohlcv = relationship("OHLCV", back_populates="asset")
    tokenomics_features = relationship("TokenomicsFeatures", back_populates="asset")
    technical_features = relationship("TechnicalFeatures", back_populates="asset")
    sentiment_features = relationship("SentimentFeatures", back_populates="asset")
    model_predictions = relationship("ModelPrediction", back_populates="asset")

class OHLCV(Base):
    __tablename__ = "ohlcv"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String, ForeignKey("asset.id"))
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    asset = relationship("Asset", back_populates="ohlcv")

class TokenomicsFeatures(Base):
    __tablename__ = "tokenomics_features"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String, ForeignKey("asset.id"))
    date = Column(DateTime, index=True)
    tvl_ratio = Column(Float)
    weekly_active_wallets = Column(Integer)
    dev_commit_activity = Column(Integer)
    wallet_concentration = Column(Float)
    unlock_volume = Column(Float)
    fdv_ratio = Column(Float)
    avg_daily_volume = Column(Float)
    asset = relationship("Asset", back_populates="tokenomics_features")

class TechnicalFeatures(Base):
    __tablename__ = "technical_features"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String, ForeignKey("asset.id"))
    date = Column(DateTime, index=True)
    ma_50 = Column(Float)
    ma_200 = Column(Float)
    ma_crossover = Column(Boolean)
    rsi_14 = Column(Float)
    macd_hist = Column(Float)
    bb_width = Column(Float)
    obv = Column(Float)
    asset = relationship("Asset", back_populates="technical_features")

class SentimentFeatures(Base):
    __tablename__ = "sentiment_features"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String, ForeignKey("asset.id"))
    date = Column(DateTime, index=True)
    finbert_polarity = Column(Float)
    sentiment_volatility = Column(Float)
    news_freq = Column(Integer)
    social_mentions = Column(Integer)
    yt_growth = Column(Float)
    asset = relationship("Asset", back_populates="sentiment_features")

class ModelPrediction(Base):
    __tablename__ = "model_predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(String, ForeignKey("asset.id"))
    model_name = Column(String)
    prediction = Column(Float)
    score = Column(Float)
    created_at = Column(DateTime, index=True)
    extra = Column(JSONB)
    asset = relationship("Asset", back_populates="model_predictions")

# Utility to create all tables
def create_all_tables():
    Base.metadata.create_all(bind=engine)

# Utility to create hypertables (run after table creation)
def create_hypertable(table_name, time_column):
    with engine.connect() as conn:
        conn.execute(f"""
            SELECT create_hypertable('{table_name}', '{time_column}', if_not_exists => TRUE);
        """) 