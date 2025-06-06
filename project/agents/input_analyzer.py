from llama_index.core.agent import ReActAgent
from llama_index.llms.nebius import NebiusLLM
from llama_index.core.prompts import PromptTemplate
import os

NEBIUS_API_KEY = os.getenv('NEBIUS_API_KEY-1')

INPUT_ANALYZER_PROMPT = """
You are the **Input Analyzer Agent**.
Your role is to extract and structure key financial details from natural language input you get from the user.

### Your Task:
1. Identify and extract the following information from the user's input:
   - Age group (e.g., 20s, 30s)
   - Monthly or annual income
   - Monthly or annual expenses
   - Risk tolerance (Conservative / Moderate / Aggressive)
   - Financial goal (e.g., buy house, retire early, save for child education)
   - Timeframe for achieving the goal (e.g., 5 years)

2. Convert all values to **monthly figures** where applicable
3. Normalize risk profile to one of: Conservative / Moderate / Aggressive
4. Return all findings in a structured JSON format

### Output Format:
{
  "age_group": "30s",
  "income_monthly": 6000,
  "expenses_monthly": 4000,
  "risk_profile": "moderate",
  "goal": "buy house",
  "goal_timeframe": "5 years"
}

### Example Input:
"I'm 35, earn $72,000 per year, spend around $48,000 annually, and want to buy a house within 5 years. I’m okay with moderate risk."

### Expected Output:
{
  "age_group": "30s",
  "income_monthly": 6000,
  "expenses_monthly": 4000,
  "risk_profile": "moderate",
  "goal": "buy house",
  "goal_timeframe": "5 years"
}

### Instructions:
- Always return only the structured JSON — no extra text
- If any value is missing, set it to null
- Normalize age to nearest decade group (20s, 30s, etc.)
- Convert annual values to monthly (divide by 12)
"""

input_analyzer_prompt = PromptTemplate(INPUT_ANALYZER_PROMPT)

def create_input_analyzer():
    llm = NebiusLLM(api_key = NEBIUS_API_KEY, model = 'meta-llama/Meta-Llama-3.1-8B-Instruct-fast')
    input_analyzer_prompt = PromptTemplate(INPUT_ANALYZER_PROMPT)
    analyze_agent =  ReActAgent(
        llm=llm,
        name='Input Analyzer',
        description='You extract structured financial data from natural language input.',
        tools=[]
    )
    analyze_agent.update_prompts({"react_header": input_analyzer_prompt})
    return analyze_agent
# input_analyzer = Agent(
#     role='Input Analyzer',
#     goal='Parse and structure user financial inputs',
#     backstory='You extract structured financial data from natural language input.',
#     verbose=True,
#     allow_delegation=False
# )