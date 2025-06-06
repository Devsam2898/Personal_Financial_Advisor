# This file has hardcoded most recent interest rates of the India and G7 countries.
# tools/hardcoded_interest_rates.py
from llama_index.core.tools import FunctionTool

INTEREST_RATES = {
    "United States": {
        "interest_rate_percent": 4.5,
        "as_of": "May 2025"
    },
    "Canada": {
        "interest_rate_percent": 2.75,
        "as_of": "April 2025"
    },
    "United Kingdom": {
        "interest_rate_percent": 4.25,
        "as_of": "May 2025"
    },
    "France": {
        "interest_rate_percent": 3.5,
        "as_of": "May 2025"
    },
    "Germany": {
        "interest_rate_percent": 3.3,
        "as_of": "May 2025"
    },
    "Italy": {
        "interest_rate_percent": 4.0,
        "as_of": "May 2025"
    },
    "Japan": {
        "interest_rate_percent": 0.5,
        "as_of": "May 2025"
    },
    "India": {
        "interest_rate_percent": 6.0,
        "as_of": "April 2025"
    }
}

def get_interest_rate(country="India"):
    rate_data = INTEREST_RATES.get(country, {"interest_rate_percent": None, "as_of": "N/A"})
    return {"interest_rate": rate_data["interest_rate_percent"]}

hardcoded_interest_tool = FunctionTool.from_defaults(fn=get_interest_rate)