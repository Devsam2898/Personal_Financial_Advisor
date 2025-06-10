# modal_app.py - Complete version with comprehensive tax database and agent integration
import os
import traceback
import asyncio
import time
import requests
from datetime import datetime
from modal import App, Function, Image, Secret, asgi_app

app = App("personal-investment-strategist-enhanced")

# Optimized image with all dependencies
image = (
    Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi",
        "uvicorn",
        "pydantic",
        "llama-index",
        "llama-index-core",
        "llama-index-llms-nebius",
        "langchain",
        "requests",
        "yfinance",
        "gradio"
    ).add_local_file(local_path="main.py", remote_path="/root/main.py")
    .add_local_dir('agents', remote_path='/root/agents')
    .add_local_dir('tools', remote_path='/root/tools')
)

# Yahoo Finance integration functions
def get_stock_data(symbol: str, period: str = "1mo") -> dict:
    """
    Fetch stock data from Yahoo Finance.
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
        period (str): Time period for data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        Dict containing stock information
    """
    try:
        import yfinance as yf
        
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

def get_market_indices() -> dict:
    """
    Get current data for major market indices.
    
    Returns:
        Dict containing market indices data
    """
    try:
        import yfinance as yf
        
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
        
    except Exception as e:
        return {"error": f"Failed to fetch market indices: {str(e)}"}

def get_sector_performance() -> dict:
    """
    Get performance data for major sector ETFs.
    
    Returns:
        Dict containing sector performance data
    """
    try:
        import yfinance as yf
        
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
        
    except Exception as e:
        return {"error": f"Failed to fetch sector performance: {str(e)}"}

def get_bullish_stocks(symbols: list) -> list:
    """
    Get stocks with price change > 5% over the selected period.
    
    Args:
        symbols (list): List of stock symbols to check
    
    Returns:
        List of bullish stock symbols
    """
    bullish = []
    for symbol in symbols:
        data = get_stock_data(symbol)
        if data.get("price_change_percent", 0) > 5:
            bullish.append(symbol)
    return bullish

# Enhanced functions for bullish sector and stock analysis
def get_bullish_sectors_analysis() -> dict:
    """Get bullish sector analysis with performance data"""
    try:
        import yfinance as yf
        
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
        
        sector_analysis = {}
        bullish_sectors = []
        
        for name, symbol in sectors.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1mo")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    month_ago_price = hist['Close'].iloc[0]
                    change_pct = ((current_price - month_ago_price) / month_ago_price) * 100
                    
                    sector_data = {
                        "symbol": symbol,
                        "current_price": float(current_price),
                        "monthly_change_percent": float(change_pct),
                        "trend": "bullish" if change_pct > 3 else "bearish" if change_pct < -3 else "neutral"
                    }
                    
                    sector_analysis[name] = sector_data
                    
                    # Add to bullish list if performance > 3%
                    if change_pct > 3:
                        bullish_sectors.append({
                            "sector": name,
                            "performance": f"{change_pct:.1f}%",
                            "symbol": symbol
                        })
                        
            except Exception as e:
                sector_analysis[name] = {"error": str(e)}
        
        # Sort bullish sectors by performance
        bullish_sectors.sort(key=lambda x: float(x['performance'].replace('%', '')), reverse=True)
        
        return {
            "sector_analysis": sector_analysis,
            "bullish_sectors": bullish_sectors[:5],  # Top 5
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch sector analysis: {str(e)}", "status": "error"}

def get_bullish_stocks_analysis() -> dict:
    """Get bullish stock analysis with top performers"""
    try:
        import yfinance as yf
        
        # Popular stocks across sectors
        stock_symbols = [
            # Tech & AI
            "NVDA", "MSFT", "GOOGL", "AAPL", "META", "AMZN", "TSLA",
            # Finance
            "JPM", "BAC", "V", "MA", "GS",
            # Healthcare
            "UNH", "JNJ", "PFE", "ABBV",
            # Other sectors
            "HD", "PG", "KO", "DIS", "MCD"
        ]
        
        bullish_stocks = []
        
        for symbol in stock_symbols[:12]:  # Limit to avoid timeout
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1mo")
                info = ticker.info
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    month_ago_price = hist['Close'].iloc[0]
                    change_pct = ((current_price - month_ago_price) / month_ago_price) * 100
                    
                    # Only include if bullish (>2% monthly gain)
                    if change_pct > 2:
                        stock_data = {
                            "symbol": symbol,
                            "company_name": info.get('longName', symbol)[:30],
                            "sector": info.get('sector', 'N/A'),
                            "current_price": float(current_price),
                            "monthly_change_percent": float(change_pct),
                            "market_cap": info.get('marketCap', 0),
                            "pe_ratio": info.get('trailingPE'),
                            "dividend_yield": info.get('dividendYield')
                        }
                        bullish_stocks.append(stock_data)
                        
            except Exception as e:
                continue
        
        # Sort by performance
        bullish_stocks.sort(key=lambda x: x['monthly_change_percent'], reverse=True)
        
        return {
            "bullish_stocks": bullish_stocks[:8],  # Top 8
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Failed to fetch bullish stocks: {str(e)}", "status": "error"}

def format_bullish_data_for_strategy(bullish_sectors, bullish_stocks) -> str:
    """Format bullish data for inclusion in strategy"""
    formatted_output = ""
    
    # Add bullish sectors
    if bullish_sectors.get("bullish_sectors"):
        formatted_output += "\n🚀 **Top Bullish Sectors (Monthly Performance):**\n"
        for sector in bullish_sectors["bullish_sectors"][:5]:
            formatted_output += f"• {sector['sector']}: {sector['performance']} ({sector['symbol']})\n"
    
    # Add bullish stocks  
    if bullish_stocks.get("bullish_stocks"):
        formatted_output += "\n📈 **Top Bullish Stocks to Watch:**\n"
        for stock in bullish_stocks["bullish_stocks"][:6]:
            div_yield = f", Div: {(stock['dividend_yield']*100):.1f}%" if stock.get('dividend_yield') else ""
            pe_text = f", PE: {stock['pe_ratio']:.1f}" if stock.get('pe_ratio') else ""
            formatted_output += f"• {stock['symbol']} ({stock['company_name']}): +{stock['monthly_change_percent']:.1f}%{pe_text}{div_yield}\n"
    
    return formatted_output

async def get_dynamic_country_info(country: str, profile_data: dict = None) -> str:
    """Get comprehensive country-specific financial information using agents and advanced tax tools"""
    try:
        # Import agents and tools from main.py
        import sys
        import os
        sys.path.append('/root')
        
        from main import economic_analyst, strategy_advisor
        from tools.hardcoded_interest_rates import INTEREST_RATES, get_interest_rate
        from tools.country_tax_db import (
            get_country_financial_info, 
            get_tax_efficient_strategies, 
            calculate_tax_liability,
            TAX_RULES
        )
        
        # Standardize country names for tax database
        country_mapping = {
            "United States": "USA",
            "United Kingdom": "UK", 
            "India": "India",
            "Canada": "Canada",
            "France": "France",
            "Germany": "Germany",
            "Italy": "Italy",
            "Japan": "Japan"
        }
        
        tax_country_code = country_mapping.get(country, country)
        
        # Get current interest rate using the hardcoded tool
        interest_data = get_interest_rate(country)
        rate_info = INTEREST_RATES.get(country, {})
        
        if interest_data.get('interest_rate'):
            current_interest_rate = f"{interest_data['interest_rate']}% (as of {rate_info.get('as_of', 'N/A')})"
        else:
            current_interest_rate = "Contact local advisor for current rates"
        
        # Get comprehensive tax information from tax database
        tax_financial_info = get_country_financial_info(tax_country_code)
        tax_strategies = get_tax_efficient_strategies(tax_country_code)
        
        # Calculate tax liability if profile data is available
        tax_calculation = ""
        if profile_data:
            try:
                income = float(profile_data.get('income', 0)) * 12  # Annual income
                # Estimate capital gains based on investment capacity
                monthly_surplus = float(profile_data.get('income', 0)) - float(profile_data.get('expenses', 0))
                estimated_annual_gains = max(0, monthly_surplus * 12 * 0.1)  # Assume 10% returns
                
                tax_calc = calculate_tax_liability(tax_country_code, income, estimated_annual_gains)
                
                if not tax_calc.get('error'):
                    tax_calculation = f"""
**💰 Estimated Tax Impact (Annual):**
• Income Tax: {tax_calc.get('currency', '')} {tax_calc.get('income_tax', 0):,.0f}
• Capital Gains Tax: {tax_calc.get('currency', '')} {tax_calc.get('capital_gains_tax', 0):,.0f}
• Total Tax: {tax_calc.get('currency', '')} {tax_calc.get('total_tax', 0):,.0f}
• Effective Tax Rate: {tax_calc.get('effective_rate', 0):.1f}%
"""
            except Exception as e:
                print(f"Tax calculation error: {e}")
        
        # Use economic analyst for additional economic context
        economic_query = f"What are the current inflation rates, GDP growth, and key economic indicators for {country}? How do these factors specifically affect personal investment and savings strategies?"
        
        try:
            economic_data = await economic_analyst.ainvoke({
                "input": economic_query
            })
            economic_context = economic_data.get('output', 'Economic analysis unavailable')
        except Exception as e:
            print(f"Economic analyst error: {e}")
            economic_context = "Economic analysis temporarily unavailable"
        
        # Format tax strategies
        strategy_text = ""
        if tax_strategies:
            strategy_text = "\n**🎯 Tax-Efficient Investment Strategies:**\n"
            for i, strategy in enumerate(tax_strategies[:5], 1):
                strategy_text += f"{i}. {strategy}\n"
        
        # Format the comprehensive response
        formatted_response = f"""
📊 **{country} Financial Context** (Comprehensive Analysis):

**💹 Current Interest Rate**: {current_interest_rate}

**🏛️ Tax & Investment Information**:
{tax_financial_info}
{tax_calculation}
{strategy_text}

**📈 Economic Analysis**:
{economic_context}

⚠️ **Important**: This information combines real-time data with comprehensive tax analysis. For specific tax advice and investment decisions, always consult with local financial advisors and verify current rates with official sources.
"""
        
        return formatted_response
        
    except Exception as e:
        print(f"Error in dynamic country info: {e}")
        # Fallback to static data if agents/tools fail
        return get_static_country_info_fallback(country)

def get_static_tax_info_fallback(country: str) -> str:
    """Fallback static tax information"""
    tax_data = {
        "United States": "401(k), IRA, Roth IRA, HSA accounts available. Long-term capital gains: 0-20%",
        "Canada": "RRSP, TFSA, RESP accounts available. 50% of capital gains taxed as income",
        "France": "PEA, Assurance Vie available. 30% flat tax or progressive income tax on gains",
        "Germany": "Private pension schemes available. 26.375% withholding tax on gains",
        "United Kingdom": "ISA, SIPP, workplace pensions available. 10-20% capital gains tax",
        "Italy": "PIR, Previdenza Complementare available. 26% capital gains tax",
        "Japan": "NISA, iDeCo available. 20.315% tax on capital gains",
        "India": "PPF, EPF, NPS available. 10% LTCG above ₹1 lakh, STCG as per income slab"
    }
    
    return tax_data.get(country, "Consult local advisor for tax-advantaged accounts and capital gains rates")

def get_static_country_info_fallback(country: str) -> str:
    """Fallback static information if dynamic lookup fails"""
    # Your existing static data as backup
    interest_rates = {
        "United States": "5.25-5.50%", # Federal Funds Rate unchanged
        "Canada": "4.75%", # Bank of Canada recently cut rates
        "United Kingdom": "5.00%", # Bank of England held rates steady but expected to cut soon
        "France": "4.25%", # ECB recently cut rates
        "Germany": "4.25%", # ECB recently cut rates
        "Italy": "4.25%", # ECB recently cut rates
        "Japan": "0.00-0.10%", # Bank of Japan recently raised rates slightly
        "India": "6.50%" # Reserve Bank of India held steady
        }

    
    current_interest_rate = interest_rates.get(country, "Contact local advisor")
    
    static_tax_data = {
        "United States": {
            "tax_accounts": "401(k), IRA, Roth IRA, HSA",
            "capital_gains_structure": "0% (long-term), 15-20% (high earners)"
        },
        "Canada": {
            "tax_accounts": "RRSP, TFSA, RESP",
            "capital_gains_structure": "50% of capital gains taxed as income"
        },
        "France": {
            "tax_accounts": "PEA, Assurance Vie, company savings plans",
            "capital_gains_structure": "30% flat tax or progressive income tax"
        },
        "Germany": {
            "tax_accounts": "Private pension schemes, company pensions",
            "capital_gains_structure": "26.375% (withholding tax)"
        },
        "United Kingdom": {
            "tax_accounts": "ISA, SIPP, workplace pensions",
            "capital_gains_structure": "10-20% (above £6,000 allowance)"
        },
        "Italy": {
            "tax_accounts": "Piani Individuali di Risparmio (PIR), Previdenza Complementare",
            "capital_gains_structure": "26% capital gains tax"
        },
        "Japan": {
            "tax_accounts": "NISA, iDeCo",
            "capital_gains_structure": "20.315% (including local tax)"
        },
        "India": {
            "tax_accounts": "PPF, EPF, NPS, Sukanya Samriddhi Account",
            "capital_gains_structure": "Long-term capital gains: 10% (above ₹1 lakh), Short-term: as per income tax slab"
        }
    }
    
    tax_info = ""
    if country in static_tax_data:
        data = static_tax_data[country]
        tax_info = f"""
• Tax-Advantaged Accounts: {data['tax_accounts']}
• Capital Gains Tax: {data['capital_gains_structure']}"""
    else:
        tax_info = "\n• Tax-Advantaged Accounts: Consult local advisor\n• Capital Gains: Varies by jurisdiction"
    
    return f"""
📊 **{country} Financial Context** (Static Data):
• Current Interest Rate: {current_interest_rate}
• Inflation: Contact local advisor for current rates
• GDP Growth: Contact local advisor for current rates
{tax_info}

⚠️ This is fallback static data. For current information and specific advice, consult local financial advisors.
"""

def get_country_stock_symbols(country: str) -> list:
    """Get relevant stock symbols for country-specific recommendations"""
    country_stocks = {
        "India": ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "ITC.NS"],
        "United States": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "JPM"],
        "United Kingdom": ["SHEL.L", "AZN.L", "ULVR.L", "LSEG.L", "HSBA.L", "BP.L"],
        "Canada": ["SHOP.TO", "RY.TO", "TD.TO", "CNR.TO", "BNS.TO", "BMO.TO"],
        "France": ["MC.PA", "OR.PA", "SAN.PA", "TTE.PA", "BNP.PA", "AIR.PA"],
        "Germany": ["SAP.DE", "SIE.DE", "ALV.DE", "DTE.DE", "MUV2.DE", "ADS.DE"],
        "Italy": ["ISP.MI", "UCG.MI", "ENI.MI", "TIT.MI", "RACE.MI", "STM.MI"],
        "Japan": ["7203.T", "6758.T", "9984.T", "8306.T", "6861.T", "9432.T"]
    }
    
    return country_stocks.get(country, ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])

# World Bank GDP Integration
def get_gdp_growth(country_code: str = "US") -> float:
    """
    Fetches GDP growth rate for a specified country using the World Bank API.
    
    Args:
        country_code: The ISO country code (e.g., 'US', 'GB', 'IN', 'CN')
    
    Returns:
        The GDP growth rate as a float, or None if data is not available
    """
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD.ZG?format=json&date=2023:2023"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1] and len(data[1]) > 0 and data[1][0].get('value'):
                return float(data[1][0]['value'])
            return None
    except Exception as e:
        print(f"Error fetching GDP data: {e}")
        return None
    
    return None

def get_country_code_from_name(country: str) -> str:
    """Convert country name to ISO code for World Bank API"""
    country_codes = {
        "United States": "US",
        "United Kingdom": "GB", 
        "India": "IN",
        "Canada": "CA",
        "France": "FR",
        "Germany": "DE",
        "Italy": "IT",
        "Japan": "JP",
        "China": "CN",
        "Brazil": "BR",
        "Australia": "AU",
        "South Korea": "KR",
        "Mexico": "MX",
        "Netherlands": "NL",
        "Spain": "ES",
        "Switzerland": "CH"
    }
    return country_codes.get(country, "US")  # Default to US

def get_comprehensive_economic_data(country: str) -> dict:
    """Get comprehensive economic data including GDP growth"""
    try:
        country_code = get_country_code_from_name(country)
        gdp_growth = get_gdp_growth(country_code)
        
        # Additional economic indicators can be added here
        economic_data = {
            "country": country,
            "country_code": country_code,
            "gdp_growth_rate": gdp_growth,
            "data_year": "2023",
            "status": "success" if gdp_growth is not None else "partial"
        }
        
        return economic_data
        
    except Exception as e:
        print(f"Error fetching economic data for {country}: {e}")
        return {
            "country": country,
            "status": "error",
            "error": str(e)
        }

async def generate_investment_strategy_direct(profile_data: dict):
    """Direct strategy generation for web endpoint - without Modal .remote() call"""
    start_time = time.time()
    
    try:
        print(f"🚀 Processing profile directly: {profile_data}")
        
        # Validate profile data
        required_fields = ['age_group', 'income', 'expenses', 'risk_profile', 'goal', 'timeframe', 'country']
        for field in required_fields:
            if not profile_data.get(field):
                return {
                    "strategy": f"❌ **Missing Required Field**: {field}\n\nPlease provide all required information.",
                    "status": "validation_error"
                }
        
        # Set defaults for optional fields
        profile_data.setdefault('current_assets', 0)
        profile_data.setdefault('current_liabilities', 0)
        
        # Calculate derived metrics
        monthly_income = float(profile_data.get('income', 0))
        monthly_expenses = float(profile_data.get('expenses', 0))
        current_assets = float(profile_data.get('current_assets', 0))
        current_liabilities = float(profile_data.get('current_liabilities', 0))
        net_worth = current_assets - current_liabilities
        monthly_surplus = monthly_income - monthly_expenses
        savings_rate = (monthly_surplus / monthly_income * 100) if monthly_income > 0 else 0
        
        country = profile_data.get('country', 'United States')
        
        # Get real-time economic data using World Bank API
        economic_data = {}
        economic_context = ""
        try:
            print(f"🌍 Fetching economic data for {country}...")
            economic_data = get_comprehensive_economic_data(country)
            
            if economic_data.get("status") == "success":
                gdp_growth = economic_data.get("gdp_growth_rate")
                economic_context = f"""
📈 **Real-Time Economic Indicators ({country}):**
• GDP Growth Rate (2023): {gdp_growth:.2f}% (World Bank)
• Economic Outlook: {"Positive growth" if gdp_growth > 2 else "Moderate growth" if gdp_growth > 0 else "Economic challenges"}
"""
            else:
                economic_context = f"\n📈 **Economic Data**: Real-time data temporarily unavailable for {country}\n"
                
        except Exception as e:
            print(f"⚠️ Economic data fetch failed: {e}")
            economic_context = f"\n📈 **Economic Data**: Analysis temporarily unavailable\n"
        
        # Get comprehensive market data WITH bullish analysis
        market_context = ""
        bullish_analysis = ""
        
        try:
            print("📊 Fetching comprehensive market analysis...")
            
            # Get market indices
            market_data = get_market_indices()
            if market_data and not market_data.get('error'):
                market_context += "\n📊 **Current Market Overview:**\n"
                for index, data in market_data.items():
                    if not data.get('error'):
                        change_emoji = "📈" if data.get('change_percent', 0) > 0 else "📉"
                        market_context += f"• {change_emoji} {index}: {data.get('current_price', 'N/A'):.2f} ({data.get('change_percent', 0):+.2f}%)\n"
            
            # Get bullish sectors analysis - THIS IS KEY!
            print("🚀 Fetching bullish sectors...")
            bullish_sectors = get_bullish_sectors_analysis()
            
            print("📈 Fetching bullish stocks...")
            bullish_stocks_data = get_bullish_stocks_analysis()
            
            # Format bullish analysis for strategy
            if bullish_sectors.get("status") == "success" or bullish_stocks_data.get("status") == "success":
                bullish_analysis = format_bullish_data_for_strategy(bullish_sectors, bullish_stocks_data)
                print(f"✅ Bullish analysis generated: {len(bullish_analysis)} characters")
            else:
                print("⚠️ Bullish analysis failed - using fallback")
                bullish_analysis = "\n🚀 **Market Opportunities**: Analysis temporarily unavailable\n"
                
        except Exception as e:
            print(f"⚠️ Market data collection failed: {e}")
            market_context = "\n📊 **Market Data**: Currently unavailable\n"
            bullish_analysis = "\n🚀 **Market Opportunities**: Analysis temporarily unavailable\n"
        
        # Generate strategy using basic template since LLM might not be available in web context
        try:
            # Try to use LLM if available
            from llama_index.llms.nebius import NebiusLLM
            
            llm = NebiusLLM(
                api_key=os.getenv("NEBIUS_API_KEY_LLAMA3"),
                model="meta-llama/Llama-3.3-70B-Instruct-fast",
                timeout=120,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Enhanced prompt
            enhanced_prompt = f"""Create a comprehensive investment strategy for a {country} resident with REAL-TIME MARKET ANALYSIS:

📋 **INVESTOR PROFILE:**
• Age Group: {profile_data.get('age_group')}
• Monthly Income: ${monthly_income:,.0f}
• Monthly Expenses: ${monthly_expenses:,.0f}
• Monthly Surplus: ${monthly_surplus:,.0f} (Savings Rate: {savings_rate:.1f}%)
• Current Assets: ${current_assets:,.0f}
• Current Liabilities: ${current_liabilities:,.0f}
• Net Worth: ${net_worth:,.0f}
• Risk Profile: {profile_data.get('risk_profile')}
• Investment Goal: {profile_data.get('goal')}
• Time Horizon: {profile_data.get('timeframe')}

📊 **REAL-TIME MARKET ANALYSIS:**
{economic_context}
{market_context}
{bullish_analysis}

🎯 **STRATEGY REQUIREMENTS:**
1. **Asset Allocation**: Provide specific percentages based on risk profile
2. **Bullish Opportunities**: Incorporate the bullish sectors and stocks identified above
3. **Tax Optimization**: Include {country}-specific tax-advantaged accounts
4. **Implementation Plan**: Step-by-step actions with timeline
5. **Risk Management**: Diversification strategy
6. **Market Timing**: How to take advantage of current market conditions

**IMPORTANT**: Include specific recommendations about the bullish sectors and stocks mentioned above. Explain which ones align with the investor's profile and why.

Format with clear sections and actionable advice."""

            print(f"📝 Generating enhanced strategy with bullish analysis...")
            response = await llm.acomplete(enhanced_prompt)
            strategy_content = response.text.strip()
            
        except Exception as e:
            print(f"⚠️ LLM generation failed: {e}, using rule-based strategy")
            
            # Rule-based strategy with bullish data
            risk_equity = 70 if profile_data.get('risk_profile') == 'Aggressive' else 60 if profile_data.get('risk_profile') == 'Moderate' else 40
            risk_bonds = 20 if profile_data.get('risk_profile') == 'Aggressive' else 30 if profile_data.get('risk_profile') == 'Moderate' else 50
            
            strategy_content = f"""
## 📊 Your Enhanced Investment Strategy ({country})

**Current Financial Position:**
• Net Worth: ${net_worth:,.0f}
• Monthly Surplus: ${monthly_surplus:,.0f}
• Savings Rate: {savings_rate:.1f}%

**Recommended Asset Allocation:**
• Stocks/Equity: {risk_equity}%
• Bonds: {risk_bonds}%
• Cash/Emergency: 10%

{economic_context}
{market_context}
{bullish_analysis}

**🎯 BULLISH SECTOR STRATEGY:**
Based on current market analysis, consider allocating a portion of your equity investments to the top-performing sectors identified above. These sectors are showing strong momentum and could align well with your {profile_data.get('timeframe')} investment timeline.

**📋 ACTION PLAN:**
1. **Emergency Fund**: Build 3-6 months of expenses in high-yield savings
2. **Tax-Advantaged Accounts**: Maximize contributions to 401(k), IRA, etc.
3. **Core Holdings**: 70% in broad market index funds (VTI, VXUS)
4. **Bullish Opportunities**: 20% allocated to top-performing sectors/stocks identified above
5. **Bonds**: 10% in government or corporate bonds for stability

**⚡ MARKET TIMING CONSIDERATIONS:**
Given the current bullish trends in the identified sectors, consider dollar-cost averaging into these positions over the next 3-6 months rather than investing all at once.

**Goal**: {profile_data.get('goal')}
**Timeline**: {profile_data.get('timeframe')}
"""
        
        # Add processing metadata
        processing_time = time.time() - start_time
        
        # Check if bullish data was included
        has_bullish_data = "bullish" in strategy_content.lower() or "sectors" in strategy_content.lower()
        
        footer = f"""

---
**📊 REAL-TIME DATA INTEGRATION:**
• Market Analysis: Live market indices and sector performance
• Bullish Opportunities: {"✅ Included" if has_bullish_data else "⚠️ Limited"}
• Economic Data: {"✅ GDP growth from World Bank" if economic_data.get("status") == "success" else "⚠️ Limited"}
• Processing Time: {processing_time:.1f} seconds

**⚠️ IMPORTANT DISCLAIMERS:**
• This strategy incorporates real-time market and economic data
• Bullish sectors/stocks are based on recent performance - conduct additional research
• Economic indicators from World Bank (2023 data)
• Past performance does not guarantee future results
• Consult with licensed financial advisors before making investment decisions

**📊 Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}**
"""
        
        final_strategy = strategy_content + footer
        
        print(f"✅ Enhanced strategy generated in {processing_time:.1f}s")
        
        return {
            "strategy": final_strategy,
            "status": "success",
            "processing_time": processing_time,
            "bullish_analysis_included": bool(bullish_analysis),
            "economic_data_included": economic_data.get("status") == "success",
            "gdp_growth_rate": economic_data.get("gdp_growth_rate") if economic_data.get("status") == "success" else None
        }
        
    except Exception as e:
        print(f"❌ Strategy generation failed: {e}")
        return {
            "strategy": f"❌ **Strategy Generation Failed**\n\nError: {str(e)}",
            "status": "error"
        }

@app.function(
    image=image,
    secrets=[Secret.from_name("nebius-secret-2")],
    timeout=180,  # 3 minutes
    cpu=4,
    memory=8192,
    keep_warm=2,
    concurrency_limit=10,
    container_idle_timeout=300
)
async def generate_investment_strategy(profile_data: dict):
    """Enhanced investment strategy generation with comprehensive market analysis and tax optimization"""
    start_time = time.time()
    
    try:
        print(f"🚀 Processing profile: {profile_data}")
        
        # Import here to avoid cold start delays
        from llama_index.llms.nebius import NebiusLLM
        
        # Validate profile data
        required_fields = ['age_group', 'income', 'expenses', 'risk_profile', 'goal', 'timeframe', 'country']
        for field in required_fields:
            if not profile_data.get(field):
                return {
                    "strategy": f"❌ **Missing Required Field**: {field}\n\nPlease provide all required information.",
                    "status": "validation_error"
                }
        
        # Set defaults for optional fields
        profile_data.setdefault('current_assets', 0)
        profile_data.setdefault('current_liabilities', 0)
        
        # Calculate derived metrics
        monthly_income = float(profile_data.get('income', 0))
        monthly_expenses = float(profile_data.get('expenses', 0))
        current_assets = float(profile_data.get('current_assets', 0))
        current_liabilities = float(profile_data.get('current_liabilities', 0))
        net_worth = current_assets - current_liabilities
        monthly_surplus = monthly_income - monthly_expenses
        savings_rate = (monthly_surplus / monthly_income * 100) if monthly_income > 0 else 0
        
        # Get country-specific financial context using agents and comprehensive tax tools
        country = profile_data.get('country', 'United States')
        try:
            country_info = await get_dynamic_country_info(country, profile_data)
        except Exception as e:
            print(f"⚠️ Dynamic country info fetch failed: {e}")
            # Fallback to static data
            country_info = get_static_country_info_fallback(country)
        
        # Get real-time economic data using World Bank API
        economic_data = {}
        try:
            print(f"🌍 Fetching economic data for {country}...")
            economic_data = get_comprehensive_economic_data(country)
            
            if economic_data.get("status") == "success":
                gdp_growth = economic_data.get("gdp_growth_rate")
                economic_context = f"""
📈 **Real-Time Economic Indicators ({country}):**
• GDP Growth Rate (2023): {gdp_growth:.2f}% (World Bank)
• Economic Outlook: {"Positive growth" if gdp_growth > 2 else "Moderate growth" if gdp_growth > 0 else "Economic challenges"}
"""
            else:
                economic_context = f"\n📈 **Economic Data**: Real-time data temporarily unavailable for {country}\n"
                
        except Exception as e:
            print(f"⚠️ Economic data fetch failed: {e}")
            economic_context = f"\n📈 **Economic Data**: Analysis temporarily unavailable\n"
        
        # Get comprehensive market data WITH bullish analysis
        market_context = ""
        stock_recommendations = []
        bullish_analysis = ""
        
        try:
            print("📊 Fetching comprehensive market analysis...")
            
            # Get market indices
            market_data = get_market_indices()
            if market_data and not market_data.get('error'):
                market_context += "\n📊 **Current Market Overview:**\n"
                for index, data in market_data.items():
                    if not data.get('error'):
                        change_emoji = "📈" if data.get('change_percent', 0) > 0 else "📉"
                        market_context += f"• {change_emoji} {index}: {data.get('current_price', 'N/A'):.2f} ({data.get('change_percent', 0):+.2f}%)\n"
            
            # Get bullish sectors analysis - THIS IS KEY!
            print("🚀 Fetching bullish sectors...")
            bullish_sectors = get_bullish_sectors_analysis()
            
            print("📈 Fetching bullish stocks...")
            bullish_stocks_data = get_bullish_stocks_analysis()
            
            # Format bullish analysis for strategy
            if bullish_sectors.get("status") == "success" or bullish_stocks_data.get("status") == "success":
                bullish_analysis = format_bullish_data_for_strategy(bullish_sectors, bullish_stocks_data)
                print(f"✅ Bullish analysis generated: {len(bullish_analysis)} characters")
            else:
                print("⚠️ Bullish analysis failed - using fallback")
                bullish_analysis = "\n🚀 **Market Opportunities**: Analysis temporarily unavailable\n"
            
            # Get country-specific stock recommendations
            stock_symbols = get_country_stock_symbols(country)
            
            for symbol in stock_symbols[:4]:  # Limit to avoid timeout
                try:
                    stock_data = get_stock_data(symbol, "1mo")
                    if not stock_data.get('error'):
                        stock_recommendations.append({
                            "symbol": symbol,
                            "name": stock_data.get('company_name', symbol)[:35],
                            "sector": stock_data.get('sector', 'N/A'),
                            "current_price": stock_data.get('current_price'),
                            "change_percent": stock_data.get('price_change_percent'),
                            "pe_ratio": stock_data.get('pe_ratio'),
                            "dividend_yield": stock_data.get('dividend_yield'),
                            "market_cap": stock_data.get('market_cap')
                        })
                except Exception as e:
                    print(f"Error fetching {symbol}: {e}")
                    continue
                    
        except Exception as e:
            print(f"⚠️ Market data collection failed: {e}")
            market_context = "\n📊 **Market Data**: Currently unavailable\n"
        
        # Format stock recommendations for prompt
        stock_context = ""
        if stock_recommendations:
            stock_context = f"\n💡 **{country} Stock Analysis:**\n"
            for stock in stock_recommendations:
                div_text = f", Div: {(stock['dividend_yield']*100):.1f}%" if stock.get('dividend_yield') else ""
                pe_text = f", PE: {stock['pe_ratio']:.1f}" if stock.get('pe_ratio') else ""
                mc_text = f", Cap: ${stock['market_cap']/1e9:.1f}B" if stock.get('market_cap') else ""
                
                stock_context += f"• {stock['symbol']} ({stock['name']}): ${stock['current_price']:.2f} "
                stock_context += f"({stock['change_percent']:+.2f}%){pe_text}{div_text}{mc_text}\n"
        
        # Initialize LLM with optimized settings
        llm = NebiusLLM(
            api_key=os.getenv("NEBIUS_API_KEY_LLAMA3"),
            model="meta-llama/Llama-3.3-70B-Instruct-fast",
            timeout=120,
            max_tokens=1800,
            temperature=0.7
        )
        
        # Create enhanced investment strategy prompt with comprehensive data
        prompt = f"""Create a comprehensive, actionable investment strategy for a {country} resident using the provided financial analysis:

📋 **INVESTOR PROFILE:**
• Age Group: {profile_data.get('age_group')}
• Monthly Income: ${monthly_income:,.0f}
• Monthly Expenses: ${monthly_expenses:,.0f}
• Monthly Surplus: ${monthly_surplus:,.0f} (Savings Rate: {savings_rate:.1f}%)
• Current Assets: ${current_assets:,.0f}
• Current Liabilities: ${current_liabilities:,.0f}
• Net Worth: ${net_worth:,.0f}
• Risk Profile: {profile_data.get('risk_profile')}
• Investment Goal: {profile_data.get('goal')}
• Time Horizon: {profile_data.get('timeframe')}
• Location: {country}

🌍 **COMPREHENSIVE COUNTRY ANALYSIS:**
{country_info}
{economic_context}

{market_context}
{bullish_analysis}
{stock_context}

**INVESTMENT STRATEGY REQUIREMENTS:**
1. Create a specific, actionable allocation strategy based on the investor's risk profile and goals
2. **INCORPORATE BULLISH SECTORS & STOCKS**: Use the real-time bullish analysis provided above
3. Include country-specific tax-advantaged accounts and strategies
4. **ECONOMIC CONTEXT**: Consider the GDP growth and economic indicators provided
5. Provide concrete next steps and implementation timeline
6. Address risk management and diversification
7. Include emergency fund recommendations
8. Consider current market conditions and capitalize on bullish opportunities
9. Provide specific percentage allocations including bullish sectors
10. Include rebalancing strategy and monitoring plan
11. Address inflation protection and currency considerations

**CRITICAL**: The strategy MUST include specific recommendations about the bullish sectors and stocks identified above. Explain which ones align with the investor's profile and how to incorporate them into the portfolio.

Format the response with clear headers, bullet points, and actionable advice. Focus on practical implementation rather than general theory."""

        print(f"📝 Generating strategy with LLM...")
        
        # Generate strategy using LLM
        try:
            response = await llm.acomplete(prompt)
            strategy_content = response.text.strip()
            
            # Add processing time and metadata
            processing_time = time.time() - start_time
            
            # Check if bullish data was included
            has_bullish_data = "bullish" in strategy_content.lower() or "sectors" in strategy_content.lower()
            
            # Add footer with disclaimers and processing info
            footer = f"""

---
**📊 REAL-TIME DATA INTEGRATION:**
• Market Analysis: Live market indices and sector performance
• Bullish Opportunities: {"✅ Included" if has_bullish_data else "⚠️ Limited"}
• Economic Data: {"✅ GDP growth from World Bank" if economic_data.get("status") == "success" else "⚠️ Limited"}
• Processing Time: {processing_time:.1f} seconds

**⚠️ IMPORTANT DISCLAIMERS:**
• This strategy incorporates real-time market and economic data
• Bullish sectors/stocks are based on recent performance - conduct additional research
• Economic indicators from World Bank (2023 data)
• Past performance does not guarantee future results
• Consult with licensed financial advisors before making investment decisions
• Tax laws and regulations may change; verify current rules with tax professionals

**📊 Analysis Metadata:**
• Market Data: Real-time via Yahoo Finance
• Economic Data: World Bank API
• Tax Analysis: Comprehensive country-specific database
• Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
            
            final_strategy = strategy_content + footer
            
            print(f"✅ Strategy generated successfully in {processing_time:.1f}s")
            
            return {
                "strategy": final_strategy,
                "status": "success",
                "processing_time": processing_time,
                "market_data_included": len(stock_recommendations) > 0,
                "country_analysis_included": bool(country_info),
                "bullish_analysis_included": bool(bullish_analysis),
                "economic_data_included": economic_data.get("status") == "success",
                "gdp_growth_rate": economic_data.get("gdp_growth_rate") if economic_data.get("status") == "success" else None
            }
            
        except Exception as e:
            print(f"❌ LLM generation error: {e}")
            return {
                "strategy": f"❌ **Strategy Generation Failed**\n\nError: {str(e)}\n\nPlease try again or contact support if the issue persists.",
                "status": "llm_error",
                "error": str(e)
            }
            
    except Exception as e:
        print(f"❌ Unexpected error in generate_investment_strategy: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        
        return {
            "strategy": f"❌ **System Error**\n\nAn unexpected error occurred: {str(e)}\n\nPlease try again or contact support.",
            "status": "system_error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.function(
    image=image,
    timeout=60,
    cpu=2,
    memory=4096,
    keep_warm=1
)
def get_market_data_endpoint():
    """Standalone endpoint for fetching current market data"""
    try:
        market_data = get_market_indices()
        sector_data = get_sector_performance()
        bullish_sectors = get_bullish_sectors_analysis()
        bullish_stocks = get_bullish_stocks_analysis()
        
        return {
            "market_indices": market_data,
            "sector_performance": sector_data,
            "bullish_sectors": bullish_sectors,
            "bullish_stocks": bullish_stocks,
            "status": "success",
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        
    except Exception as e:
        return {
            "error": f"Failed to fetch market data: {str(e)}",
            "status": "error"
        }

@app.function(
    image=image,
    timeout=30,
    cpu=1,
    memory=2048
)
def get_stock_info(symbol: str, period: str = "1mo"):
    """Standalone endpoint for fetching individual stock data"""
    try:
        stock_data = get_stock_data(symbol, period)
        return {
            "data": stock_data,
            "status": "success" if not stock_data.get('error') else "error"
        }
    except Exception as e:
        return {
            "error": f"Failed to fetch stock data: {str(e)}",
            "status": "error"
        }

@app.function(
    image=image,
    timeout=60,
    cpu=2,
    memory=4096
)
async def get_country_analysis(country: str, include_tax_calc: bool = False, annual_income: float = 0, annual_gains: float = 0):
    """Standalone endpoint for comprehensive country analysis"""
    try:
        profile_data = None
        if include_tax_calc and annual_income > 0:
            profile_data = {
                'income': annual_income / 12,  # Convert to monthly
                'expenses': annual_income / 12 * 0.7,  # Assume 70% expense ratio
            }
        
        country_info = await get_dynamic_country_info(country, profile_data)
        
        return {
            "country_analysis": country_info,
            "status": "success",
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        
    except Exception as e:
        # Fallback to static data
        fallback_info = get_static_country_info_fallback(country)
        return {
            "country_analysis": fallback_info,
            "status": "fallback",
            "error": str(e),
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC')
        }

# Remove the conditional FastAPI setup since we're handling it in the web function
# FastAPI application for HTTP endpoints - moved inside web() function

# Pydantic models and endpoints are now defined inside the web() function

# FastAPI endpoints are now defined inside the web() function

# Deploy FastAPI app as ASGI (always create web endpoint)
@app.function(
    image=image,
    secrets=[Secret.from_name("nebius-secret-2")],
    keep_warm=2,
    cpu=2,
    memory=4096,
    container_idle_timeout=300
)
@asgi_app()
def web():
    # Import FastAPI inside the function to avoid deployment issues
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        from typing import Optional
        
        # Create FastAPI app
        web_app = FastAPI(
            title="Personal Investment Strategist API",
            description="Comprehensive investment strategy generation with real-time market data and tax optimization",
            version="2.0.0"
        )
        
        # Define models
        class ProfileRequest(BaseModel):
            profile: dict
        
        # Simple strategy endpoint that matches your Gradio app expectation
        @web_app.post("/strategy")
        async def strategy_endpoint(request: ProfileRequest):
            """Generate investment strategy - matches original endpoint"""
            try:
                profile_data = request.profile
                
                # Since we're inside the Modal function, we need to call the strategy generation directly
                # Instead of using .remote(), we'll call the function directly
                result = await generate_investment_strategy_direct(profile_data)
                return result
            except Exception as e:
                return {
                    "strategy": f"❌ **Error**: {str(e)}",
                    "status": "error"
                }
        
        @web_app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC'),
                "version": "2.0.0",
                "features": [
                    "Real-time market data via Yahoo Finance",
                    "World Bank GDP data integration",
                    "Bullish sector and stock analysis",
                    "Comprehensive tax analysis",
                    "AI-powered strategy generation"
                ]
            }
        
        @web_app.get("/test")
        async def test_endpoint():
            """Test endpoint for Gradio app"""
            return {
                "test_result": "Service is working",
                "status": "success",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC'),
                "endpoints_available": ["/strategy", "/health", "/test"]
            }
        
        @web_app.get("/")
        async def root():
            """Root endpoint"""
            return {
                "name": "Personal Investment Strategist API Enhanced",
                "version": "2.0.0",
                "status": "operational",
                "description": "AI-powered investment strategy generation with real-time market data",
                "main_endpoint": "/strategy",
                "features": [
                    "🤖 AI-powered strategy generation",
                    "📊 Real-time market data (Yahoo Finance)",
                    "🌍 World Bank economic data",
                    "🚀 Bullish sector analysis",
                    "🏦 Tax optimization strategies",
                    "💼 Country-specific recommendations"
                ]
            }
        
        return web_app
        
    except ImportError as e:
        # Fallback minimal web app if FastAPI import fails
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import json
        
        class SimpleHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "status": "limited",
                    "message": "FastAPI unavailable, using basic handler",
                    "error": str(e)
                }
                self.wfile.write(json.dumps(response).encode())
        
        # This is a fallback - in practice, FastAPI should work
        return SimpleHandler

# Simplified function for basic strategy generation (fallback)
@app.function(
    image=image,
    secrets=[Secret.from_name("nebius-secret-2")],
    timeout=180,
    cpu=4,
    memory=8192,
    keep_warm=2,
    concurrency_limit=10,
    container_idle_timeout=300
)
async def strategy_basic(profile_data: dict):
    """Basic strategy generation without FastAPI dependency"""
    try:
        result = await generate_investment_strategy(profile_data)
        return result
    except Exception as e:
        return {
            "strategy": f"❌ **Error**: {str(e)}",
            "status": "error"
        }
