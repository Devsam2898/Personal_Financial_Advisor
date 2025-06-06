# country_tax_db.py - Complete tax rules and financial information database
from llama_index.core.tools import FunctionTool

# Comprehensive tax rules database
TAX_RULES = {
    "USA": {
        "capital_gains": {"short_term": 37, "long_term": 20},
        "income_brackets": [0, 10475, 41885, 89405, 174050, 214200, 539900],
        "rates": [0.10, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37],
        "currency": "USD"
    },
    "India": {
        "capital_gains": {"short_term": 15, "long_term": 12.5},  # Updated for FY 2025-26: LTCG is 12.5%
        "tax_free_threshold": 400000,  # Updated: No tax up to Rs. 4 lakh in new regime
        "slabs": [
            {"up_to": 800000, "rate": 0.05},
            {"up_to": 1200000, "rate": 0.10},
            {"up_to": 1600000, "rate": 0.15},
            {"up_to": 2000000, "rate": 0.20},
            {"up_to": 2400000, "rate": 0.25},
            {"above": 2400000, "rate": 0.30}
        ],
        "currency": "INR"
    },
    "UK": {
        "capital_gains": {"allowance": 6000, "basic_rate": 10, "higher_rate": 20},
        "income_brackets": [0, 12570, 50270, 125140],
        "rates": [0.00, 0.20, 0.40, 0.45],
        "currency": "GBP"
    },
    "Canada": {
        "capital_gains": {"inclusion_rate": 0.5, "rate_1": 15, "rate_2": 27},
        "federal_tax_brackets": [0, 53359, 106717, 165430, 235675],
        "federal_rates": [0.15, 0.205, 0.26, 0.29, 0.33],
        "currency": "CAD"
    },
    "France": {
        "capital_gains": {"individual": 30},  # Flat rate for most cases; can be higher with social contributions
        "income_brackets": [0, 11094, 28218, 80297, 170000],
        "rates": [0.00, 0.11, 0.30, 0.41, 0.45],
        "currency": "EUR"
    },
    "Germany": {
        "capital_gains": {"individual": 26.375},  # Flat rate (25% + solidarity surcharge)
        "income_brackets": [0, 11604, 63469, 277825],  # Example: 2024 brackets, may vary slightly
        "rates": [0.00, 0.14, 0.42, 0.45],
        "currency": "EUR"
    },
    "Italy": {
        "capital_gains": {"individual": 26},  # Flat rate for most financial assets
        "income_brackets": [0, 15000, 28000, 50000, 75000, 120000, 150000],  # Example: 2024 brackets
        "rates": [0.23, 0.25, 0.35, 0.43, 0.45, 0.47, 0.47],
        "currency": "EUR"
    },
    "Japan": {
        "capital_gains": {"individual": 20.315},  # Flat rate (20% + 0.315% local tax)
        "income_brackets": [0, 1950000, 3300000, 6950000, 9000000, 18000000, 40000000],
        "rates": [0.05, 0.10, 0.20, 0.23, 0.33, 0.40, 0.45],
        "currency": "JPY"
    }
}

# Country-specific financial information database
COUNTRY_FINANCIAL_INFO = {
    "USA": {
        "capital_gains_tax": "0% (long-term), 15-20% (high earners)",
        "income_tax_rate": "10-37% (federal)",
        "current_interest_rate": "5.25-5.50% (Fed rate)",
        "tax_accounts": "401(k), IRA, Roth IRA, HSA",
        "investment_options": "US stocks, bonds, REITs, international funds",
        "currency": "USD"
    },
    "Canada": {
        "capital_gains_tax": "50% of capital gains taxed as income",
        "income_tax_rate": "15-33% (federal) + provincial",
        "current_interest_rate": "5.00% (BoC rate)",
        "tax_accounts": "RRSP, TFSA, RESP",
        "investment_options": "Canadian stocks, bonds, GICs, international funds",
        "currency": "CAD"
    },
    "UK": {
        "capital_gains_tax": "10-20% (above £6,000 allowance)",
        "income_tax_rate": "20-45%",
        "current_interest_rate": "5.25% (BoE rate)",
        "tax_accounts": "ISA, SIPP, workplace pensions",
        "investment_options": "UK stocks, bonds, funds, ETFs",
        "currency": "GBP"
    },
    "Germany": {
        "capital_gains_tax": "26.375% (withholding tax)",
        "income_tax_rate": "14-45%",
        "current_interest_rate": "4.50% (ECB rate)",
        "tax_accounts": "Private pension schemes, company pensions",
        "investment_options": "German stocks, EU bonds, funds, ETFs",
        "currency": "EUR"
    },
    "France": {
        "capital_gains_tax": "30% flat tax or progressive income tax",
        "income_tax_rate": "0-45%",
        "current_interest_rate": "4.50% (ECB rate)",
        "tax_accounts": "PEA, Assurance Vie, company savings plans",
        "investment_options": "French stocks, EU bonds, funds, ETFs",
        "currency": "EUR"
    },
    "Italy": {
        "capital_gains_tax": "26% on financial assets",
        "income_tax_rate": "23-43%",
        "current_interest_rate": "4.50% (ECB rate)",
        "tax_accounts": "Private pension funds, TFR",
        "investment_options": "Italian stocks, EU bonds, funds, ETFs",
        "currency": "EUR"
    },
    "Japan": {
        "capital_gains_tax": "20.315% (separate taxation)",
        "income_tax_rate": "5-45%",
        "current_interest_rate": "-0.10% (BoJ rate)",
        "tax_accounts": "iDeCo, NISA, company pensions",
        "investment_options": "Japanese stocks, bonds, funds, international assets",
        "currency": "JPY"
    },
    "India": {
        "capital_gains_tax": "12.5% (long-term equity), 15% (short-term)",
        "income_tax_rate": "5-30% (new regime)",
        "current_interest_rate": "6.50% (RBI rate)",
        "tax_accounts": "EPF, PPF, ELSS, NPS, SCSS",
        "investment_options": "Indian stocks, bonds, mutual funds, gold, FDs",
        "currency": "INR"
    }
}

def get_tax_rules(country="USA"):
    """Returns tax rules for a given country"""
    return TAX_RULES.get(country, {})

def get_country_financial_info(country: str) -> str:
    """Get country-specific tax and interest rate information"""
    
    if country not in COUNTRY_FINANCIAL_INFO:
        return f"Limited tax information available for {country}. Consider consulting local financial advisors."
    
    data = COUNTRY_FINANCIAL_INFO[country]
    return f"""
• Capital Gains Tax: {data['capital_gains_tax']}
• Income Tax Rate: {data['income_tax_rate']}
• Current Interest Rate: {data['current_interest_rate']}
• Tax-Advantaged Accounts: {data['tax_accounts']}
• Common Investment Options: {data['investment_options']}
• Currency: {data['currency']}
"""

def get_supported_countries():
    """Returns list of supported countries"""
    return list(TAX_RULES.keys())

def calculate_tax_liability(country: str, income: float, capital_gains: float = 0) -> dict:
    """Calculate estimated tax liability for a given country"""
    
    tax_rules = get_tax_rules(country)
    if not tax_rules:
        return {"error": f"Tax rules not available for {country}"}
    
    result = {
        "country": country,
        "income": income,
        "capital_gains": capital_gains,
        "income_tax": 0,
        "capital_gains_tax": 0,
        "total_tax": 0,
        "effective_rate": 0
    }
    
    try:
        # Calculate income tax
        if country == "India":
            # Special handling for India's slab system
            if income <= tax_rules.get("tax_free_threshold", 0):
                result["income_tax"] = 0
            else:
                taxable_income = income - tax_rules.get("tax_free_threshold", 0)
                income_tax = 0
                
                for slab in tax_rules.get("slabs", []):
                    if "up_to" in slab:
                        slab_limit = slab["up_to"] - tax_rules.get("tax_free_threshold", 0)
                        if taxable_income > slab_limit:
                            income_tax += slab_limit * slab["rate"]
                            taxable_income -= slab_limit
                        else:
                            income_tax += taxable_income * slab["rate"]
                            taxable_income = 0
                            break
                    elif "above" in slab and taxable_income > 0:
                        income_tax += taxable_income * slab["rate"]
                        break
                
                result["income_tax"] = income_tax
        
        else:
            # Standard bracket system for other countries
            brackets = tax_rules.get("income_brackets", [])
            rates = tax_rules.get("rates", [])
            
            if len(brackets) == len(rates):
                income_tax = 0
                remaining_income = income
                
                for i in range(len(brackets) - 1):
                    bracket_size = brackets[i + 1] - brackets[i]
                    if remaining_income > bracket_size:
                        income_tax += bracket_size * rates[i]
                        remaining_income -= bracket_size
                    else:
                        income_tax += remaining_income * rates[i]
                        remaining_income = 0
                        break
                
                if remaining_income > 0 and len(rates) > 0:
                    income_tax += remaining_income * rates[-1]
                
                result["income_tax"] = income_tax
        
        # Calculate capital gains tax
        cg_rules = tax_rules.get("capital_gains", {})
        if capital_gains > 0:
            if country == "UK":
                # UK has allowance system
                allowance = cg_rules.get("allowance", 0)
                taxable_gains = max(0, capital_gains - allowance)
                # Simplified: use basic rate for calculation
                result["capital_gains_tax"] = taxable_gains * (cg_rules.get("basic_rate", 0) / 100)
            
            elif country == "Canada":
                # Canada includes 50% of capital gains as income
                inclusion_rate = cg_rules.get("inclusion_rate", 0.5)
                taxable_gains = capital_gains * inclusion_rate
                # Simplified: use average rate
                avg_rate = (cg_rules.get("rate_1", 15) + cg_rules.get("rate_2", 27)) / 2
                result["capital_gains_tax"] = taxable_gains * (avg_rate / 100)
            
            elif "long_term" in cg_rules:
                # USA system - assume long-term
                result["capital_gains_tax"] = capital_gains * (cg_rules["long_term"] / 100)
            
            elif "individual" in cg_rules:
                # Flat rate systems (Germany, France, Italy, Japan)
                result["capital_gains_tax"] = capital_gains * (cg_rules["individual"] / 100)
            
            elif "short_term" in cg_rules:
                # India system - assume short-term for simplicity
                result["capital_gains_tax"] = capital_gains * (cg_rules["short_term"] / 100)
        
        # Calculate totals
        result["total_tax"] = result["income_tax"] + result["capital_gains_tax"]
        total_income = income + capital_gains
        result["effective_rate"] = (result["total_tax"] / total_income * 100) if total_income > 0 else 0
        
    except Exception as e:
        result["error"] = f"Calculation error: {str(e)}"
    
    return result

def get_tax_efficient_strategies(country: str) -> list:
    """Get tax-efficient investment strategies for a specific country"""
    
    strategies = {
        "USA": [
            "Maximize 401(k) contributions (up to $23,000 in 2024)",
            "Use Roth IRA for tax-free growth ($7,000 limit)",
            "Hold investments >1 year for long-term capital gains rates",
            "Consider tax-loss harvesting",
            "Use HSA as retirement account (triple tax advantage)"
        ],
        "Canada": [
            "Maximize TFSA contributions first (tax-free growth)",
            "Use RRSP for tax deduction (18% of income, max $31,560)",
            "Hold Canadian eligible dividends for tax credit",
            "Consider capital gains vs dividends tax treatment",
            "Use RESP for children's education (government grants)"
        ],
        "UK": [
            "Use ISA allowance (£20,000 annually, tax-free)",
            "Maximize pension contributions (annual allowance £60,000)",
            "Utilize capital gains allowance (£6,000 annually)",
            "Consider dividend allowance (£1,000 tax-free)",
            "Use bed and breakfast rules for tax-loss harvesting"
        ],
        "Germany": [
            "Use Riester pension for tax benefits",
            "Consider company pension schemes (bAV)",
            "Utilize €1,000 annual capital gains exemption",
            "Hold investments in tax-efficient funds",
            "Consider real estate investment (no capital gains after 10 years)"
        ],
        "India": [
            "Maximize ELSS investments (₹1.5 lakh 80C deduction)",
            "Use PPF for long-term tax-free growth",
            "Consider NPS for additional tax benefits",
            "Hold equity investments >1 year for LTCG benefits",
            "Use SIP for rupee cost averaging"
        ],
        "France": [
            "Maximize PEA contributions (€150,000 limit, tax-free after 5 years)",
            "Use Assurance Vie for tax-efficient growth",
            "Consider company savings plans (PEE/PERCO)",
            "Hold investments >8 years for reduced tax rates",
            "Use life insurance for estate planning"
        ],
        "Italy": [
            "Use PIR (Individual Savings Plans) for tax benefits",
            "Consider pension funds for tax deductions",
            "Maximize TFR (employee severance) investments",
            "Hold government bonds for favorable tax treatment",
            "Use life insurance for tax-efficient savings"
        ],
        "Japan": [
            "Maximize iDeCo contributions (varies by employment status)",
            "Use NISA for tax-free investment growth",
            "Consider company pension schemes",
            "Hold investments for long-term capital gains",
            "Use life insurance for tax-efficient savings"
        ]
    }
    
    return strategies.get(country, ["Consult local tax advisor for country-specific strategies"])

# Wrap functions as LlamaIndex FunctionTools
tax_tool = FunctionTool.from_defaults(fn=get_tax_rules)
financial_info_tool = FunctionTool.from_defaults(fn=get_country_financial_info)
tax_calculation_tool = FunctionTool.from_defaults(fn=calculate_tax_liability)
tax_strategies_tool = FunctionTool.from_defaults(fn=get_tax_efficient_strategies)

# Export all tools as a list for easy import
ALL_TAX_TOOLS = [tax_tool, financial_info_tool, tax_calculation_tool, tax_strategies_tool]