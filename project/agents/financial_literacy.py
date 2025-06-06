from llama_index.core.agent import ReActAgent
from llama_index.llms.nebius import NebiusLLM
import os
from llama_index.core.prompts import PromptTemplate

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY-1")

LITERACY_PROMPT = """
You are the **Financial Literacy Detector Agent**.
Your role is to determine the user's financial knowledge level based on their inputs.

### Your Task:
1. Analyze the user's language and questions
2. Determine if the user is:
   - Beginner: Uses simple terms, asks basic questions
   - Intermediate: Understands common investment terms, wants to optimize
   - Advanced: Asks about tax brackets, asset classes, portfolio optimization
3. Return result as one of: beginner / intermediate / advanced

### Example Input:
"I'm in my 30s, earn $6k/month, spend $4k, and want to buy a house in 5 years."

Output:
{
  "literacy_level": "beginner",
  "notes": "User uses simple terms, no mention of existing investments or tax implications"
}

### Instructions:
- Only return JSON
- Don't use extra text
"""

prompt = PromptTemplate(LITERACY_PROMPT)

def create_literacy_detector():
    llm = NebiusLLM(
        api_key=NEBIUS_API_KEY,
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-fast",
    )

    return ReActAgent(
        name="Literacy Detector",
        description="Determines user's financial literacy level to customize advice depth.",
        tools=[],
        llm=llm,
        system_prompt=prompt.template,
        verbose=False
    )