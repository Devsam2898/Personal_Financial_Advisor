from llama_index.core.agent import ReActAgent
from llama_index.llms.nebius import NebiusLLM
import os
from llama_index.core.prompts import PromptTemplate

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY-1")

NETWORTH_PROMPT = """
You are the **Net Worth & Investment Checker Agent**.
Your role is to extract information about user's current assets and liabilities.

### Your Task:
1. From the user input, identify:
   - Cash savings
   - Equity/ETF holdings
   - Bonds or fixed deposits
   - Loans or debts
   - Monthly savings rate
   -if "holdings" is not in user input equity holdings then set it to null.s
2. Return structured summary of:
   - Total Assets
   - Total Liabilities
   - Net Worth
   - Investment Experience
   - Risk Exposure Already Taken

### Example Input:
"I've been investing for 2 years. I currently hold $20k in VOO ETF and $10k in crypto. I have $10k in student loan debt."

### Output:
{
  "cash_savings": 5000,
  "equity_holdings": 20000,
  "crypto_holdings": 10000,
  "debt": 10000,
  "monthly_savings": 1000,
  "investment_experience": "intermediate",
  "risk_exposure": "moderate"
}

### Instructions:
- Always return JSON only
- If info not provided, set field to null
"""

prompt = PromptTemplate(NETWORTH_PROMPT)

def create_networth_checker():
    llm = NebiusLLM(
        api_key=NEBIUS_API_KEY,
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-fast"
    )

    return ReActAgent(
        name="Net Worth Checker",
        description="Analyzes user's existing investments, debts, and savings habits.",
        tools=[],
        llm=llm,
        system_prompt=prompt.template,
        verbose=False
    )