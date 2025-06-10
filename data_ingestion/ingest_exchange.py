# Placeholder: Ingest OHLCV data using ccxt
import ccxt
from typing import List, Any

def fetch_ohlcv(symbol: str, exchange_name: str = 'binance') -> List[Any]:
    exchange = getattr(ccxt, exchange_name)()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d')
    return ohlcv

if __name__ == "__main__":
    data = fetch_ohlcv('ETH/USDT')
    print(data) 