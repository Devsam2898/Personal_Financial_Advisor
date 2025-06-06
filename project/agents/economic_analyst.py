# This agent is designed to analyze user financial profiles and provide a detailed demographic and risk assessment.
# It interprets user inputs to create a structured profile that includes life stage, disposable income, risk behavior, tax implications, and planning horizon.
from llama_index.core.agent import ReActAgent
from llama_index.llms.nebius import NebiusLLM
from llama_index.core.prompts import PromptTemplate
from tools.interest_rates import hardcoded_interest_tool, INTEREST_RATES
from tools.worldbank_inflation_rates import worldbank_inflation_tool
from tools.yahoofinance import yahoofinance_tool, market_indices_tool, sector_performance_tool
from tools.worldbank_gdp import worldbank_tool
import os

NEBIUS_API_KEY = os.getenv('NEBIUS_API_KEY-1')

ECONOMIC_ANALYST_PROMPT = """
You are the **Economic Analyst Agent**.
Your role is to gather and interpret current economic conditions relevant to investment decisions.

### Available Tools:
1. `worldbank_inflation_tool(country_code)` → Returns inflation rate (%) for any supported country
2. `hardcoded_interest_tool(country)` → Returns central bank interest rate (%)
3. `worldbank_gdp_tool(country_code)` → Returns GDP growth rate (%)
4. `yahoofinance_tool(ticker)` → Returns bull/bear market trend

### Your Task:
1. Identify the user's country and corresponding code (e.g., India → IN)
2. Call all tools to fetch:
   - Inflation Rate
   - Interest Rate
   - GDP Growth
   - Market Trend
3. Interpret how these factors impact investment strategy:
   - High inflation → suggest inflation-hedging assets
   - Rising interest rates → favor bonds or income-generating assets
   - Bullish market → consider more equity exposure
   - Strong GDP growth → increase equity allocation
4. Return all findings in structured format usable by Strategy Advisor

### Output Format:
{
  "country": "India",
  "country_code": "IN",
  "inflation_rate": 4.7,
  "interest_rate": 6.0,
  "gdp_growth": 6.8,
  "market_trend": "bullish",
  "advice_weighting": {
    "equity": 0.6,
    "bonds": 0.3,
    "cash": 0.1
  },
  "notes": "High inflation and rising interest rates suggest caution with equities; recommend diversified portfolio."
}

### Instructions:
- Always return JSON output only
- If any tool fails, set value to null
- Keep notes concise but informative
"""

prompt = PromptTemplate(ECONOMIC_ANALYST_PROMPT)

def create_economic_analyst():
    llm = NebiusLLM(api_key=NEBIUS_API_KEY, model='meta-llama/Meta-Llama-3.1-8B-Instruct-fast') 
    eco_prompt = PromptTemplate(ECONOMIC_ANALYST_PROMPT)
    eco_agent = ReActAgent(
        llm=llm,
        name='Economic Analyst',
        tools=[hardcoded_interest_tool,worldbank_inflation_tool,worldbank_tool,yahoofinance_tool, market_indices_tool, sector_performance_tool],
        description='You analyze inflation, interest rates, GDP growth, and market trends.')
    eco_agent.update_prompts({"react_header": eco_prompt})
    return eco_agent



# economic_analyst = Agent(
#     role='Economic Analyst',
#     goal='Fetch and interpret macroeconomic indicators relevant to investment decisions',
#     backstory='You analyze inflation, interest rates, GDP growth, and market trends.',
#     verbose=True,
#     allow_delegation=False
# )