# tools/worldbank_gdp.py
import requests
from llama_index.core.tools import FunctionTool

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

# Create the tool instance
worldbank_tool = FunctionTool.from_defaults(
    fn=get_gdp_growth,
    name="get_gdp_growth",
    description="Get GDP growth rate for a specific country using World Bank data"
)




# # The country code should be dynamic, based on user input. 
# # This code fetches GDP growth rate for a specified country using the World Bank API.
# # tools/worldbank.py
# import requests
# from llama_index.core.tools import FunctionTool

# @FunctionTool.from_defaults()
# def get_gdp_growth(country_code="US"):
#     url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD.ZG?format=json"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return float(data[1][0]['value']) if data[1] and data[1][0]['value'] else None
#     return None

# worldbank_tool = FunctionTool.from_defaults(fn=get_gdp_growth)
