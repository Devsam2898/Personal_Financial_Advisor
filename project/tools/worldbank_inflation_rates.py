# This file has inflation rates for India and G7 countries taken from World Bank API.
# tools/worldbank_inflation.py

import requests
from llama_index.core.tools import FunctionTool

def get_worldbank_inflation(country_code="IN"):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/FP.CPI.TOTL.ZG?format=json&per_page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) == 2 and data[1]:
            value = data[1][0]["value"]
            return {"inflation_rate": round(float(value), 2)} if value else {"inflation_rate": None}
    return {"inflation_rate": None}

worldbank_inflation_tool = FunctionTool.from_defaults(fn=get_worldbank_inflation)