# tools/yahoofinance.py - Fixed version
import yfinance as yf
from typing import Optional, Dict, Any
from llama_index.core.tools import FunctionTool

def get_stock_data(symbol: str, period: str = "1mo") -> Dict[str, Any]:
    """
    Fetch stock data from Yahoo Finance.
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
        period (str): Time period for data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        Dict containing stock information
    """
    try:
        stock = yf.Ticker(symbol)
        
        # Get historical data
        hist = stock.history(period=period)
        
        # Get stock info
        info = stock.info
        
        # Get current price
        current_price = hist['Close'].iloc[-1] if not hist.empty else None
        
        # Calculate basic metrics
        if len(hist) > 1:
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[-2]
            price_change_pct = (price_change / hist['Close'].iloc[-2]) * 100
        else:
            price_change = 0
            price_change_pct = 0
            
        return {
            "symbol": symbol,
            "current_price": float(current_price) if current_price is not None else None,
            "price_change": float(price_change),
            "price_change_percent": float(price_change_pct),
            "volume": int(hist['Volume'].iloc[-1]) if not hist.empty else None,
            "market_cap": info.get('marketCap'),
            "pe_ratio": info.get('trailingPE'),
            "dividend_yield": info.get('dividendYield'),
            "52_week_high": info.get('fiftyTwoWeekHigh'),
            "52_week_low": info.get('fiftyTwoWeekLow'),
            "company_name": info.get('longName', symbol),
            "sector": info.get('sector'),
            "industry": info.get('industry')
        }
        
    except Exception as e:
        return {
            "error": f"Failed to fetch data for {symbol}: {str(e)}",
            "symbol": symbol
        }

def get_market_indices() -> Dict[str, Any]:
    """
    Get current data for major market indices.
    
    Returns:
        Dict containing market indices data
    """
    indices = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC", 
        "Dow Jones": "^DJI",
        "Russell 2000": "^RUT",
        "VIX": "^VIX"
    }
    
    results = {}
    
    for name, symbol in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                if len(hist) > 1:
                    prev_price = hist['Close'].iloc[-2]
                    change = current_price - prev_price
                    change_pct = (change / prev_price) * 100
                else:
                    change = 0
                    change_pct = 0
                    
                results[name] = {
                    "symbol": symbol,
                    "current_price": float(current_price),
                    "change": float(change),
                    "change_percent": float(change_pct)
                }
        except Exception as e:
            results[name] = {"error": str(e)}
            
    return results

def get_sector_performance() -> Dict[str, Any]:
    """
    Get performance data for major sector ETFs.
    
    Returns:
        Dict containing sector performance data
    """
    sectors = {
        "Technology": "XLK",
        "Healthcare": "XLV", 
        "Financials": "XLF",
        "Consumer Discretionary": "XLY",
        "Communication Services": "XLC",
        "Industrials": "XLI",
        "Consumer Staples": "XLP",
        "Energy": "XLE",
        "Utilities": "XLU",
        "Real Estate": "XLRE",
        "Materials": "XLB"
    }
    
    results = {}
    
    for name, symbol in sectors.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1mo")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                month_ago_price = hist['Close'].iloc[0]
                change = current_price - month_ago_price
                change_pct = (change / month_ago_price) * 100
                
                results[name] = {
                    "symbol": symbol,
                    "current_price": float(current_price),
                    "monthly_change_percent": float(change_pct)
                }
        except Exception as e:
            results[name] = {"error": str(e)}
            
    return results

# Create the function tools
yahoofinance_tool = FunctionTool.from_defaults(
    fn=get_stock_data,
    name="get_stock_data",
    description="Get current stock price, historical data, and key metrics for a given stock symbol from Yahoo Finance"
)

market_indices_tool = FunctionTool.from_defaults(
    fn=get_market_indices,
    name="get_market_indices", 
    description="Get current prices and daily changes for major market indices (S&P 500, NASDAQ, Dow Jones, etc.)"
)

sector_performance_tool = FunctionTool.from_defaults(
    fn=get_sector_performance,
    name="get_sector_performance",
    description="Get monthly performance data for major market sectors using sector ETFs"
)




# import yfinance as yf
# from llama_index.core.tools import FunctionTool

# @FunctionTool.from_defaults()
# def get_market_trend(ticker="^GSPC"):
#     stock = yf.Ticker(ticker)
#     hist = stock.history(period="6mo")
#     trend = "bullish" if hist["Close"][-1] > hist["Close"][0] else "bearish"
#     return {"market_trend": trend}

# yahoofinance_tool = FunctionTool.from_defaults(fn=get_market_trend)