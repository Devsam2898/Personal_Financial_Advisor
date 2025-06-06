# modal_app.py - Optimized for faster response times
import os
import traceback
import asyncio
from modal import App, Function, Image, Secret, asgi_app

app = App("personal-investment-strategist-optimized")

# Optimized image with minimal dependencies
image = (
    Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi",
        "uvicorn",
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

# Country-specific financial information
def get_country_financial_info(country: str) -> str:
    """Get country-specific tax and interest rate information"""
    
    country_data = {
        "United States": {
            "capital_gains_tax": "0% (long-term), 15-20% (high earners)",
            "income_tax_rate": "10-37% (federal)",
            "current_interest_rate": "5.25-5.50% (Fed rate)",
            "tax_accounts": "401(k), IRA, Roth IRA, HSA",
            "investment_options": "US stocks, bonds, REITs, international funds"
        },
        "Canada": {
            "capital_gains_tax": "50% of capital gains taxed as income",
            "income_tax_rate": "15-33% (federal) + provincial",
            "current_interest_rate": "5.00% (BoC rate)",
            "tax_accounts": "RRSP, TFSA, RESP",
            "investment_options": "Canadian stocks, bonds, GICs, international funds"
        },
        "United Kingdom": {
            "capital_gains_tax": "10-20% (above £6,000 allowance)",
            "income_tax_rate": "20-45%",
            "current_interest_rate": "5.25% (BoE rate)",
            "tax_accounts": "ISA, SIPP, workplace pensions",
            "investment_options": "UK stocks, bonds, funds, ETFs"
        },
        "Germany": {
            "capital_gains_tax": "26.375% (withholding tax)",
            "income_tax_rate": "14-45%",
            "current_interest_rate": "4.50% (ECB rate)",
            "tax_accounts": "Private pension schemes, company pensions",
            "investment_options": "German stocks, EU bonds, funds, ETFs"
        },
        "France": {
            "capital_gains_tax": "30% flat tax or progressive income tax",
            "income_tax_rate": "0-45%",
            "current_interest_rate": "4.50% (ECB rate)",
            "tax_accounts": "PEA, Assurance Vie, company savings plans",
            "investment_options": "French stocks, EU bonds, funds, ETFs"
        },
        "Italy": {
            "capital_gains_tax": "26% on financial assets",
            "income_tax_rate": "23-43%",
            "current_interest_rate": "4.50% (ECB rate)",
            "tax_accounts": "Private pension funds, TFR",
            "investment_options": "Italian stocks, EU bonds, funds, ETFs"
        },
        "Japan": {
            "capital_gains_tax": "20.315% (separate taxation)",
            "income_tax_rate": "5-45%",
            "current_interest_rate": "-0.10% (BoJ rate)",
            "tax_accounts": "iDeCo, NISA, company pensions",
            "investment_options": "Japanese stocks, bonds, funds, international assets"
        },
        "India": {
            "capital_gains_tax": "10% (long-term equity), 15% (short-term)",
            "income_tax_rate": "5-30%",
            "current_interest_rate": "6.50% (RBI rate)",
            "tax_accounts": "EPF, PPF, ELSS, NPS",
            "investment_options": "Indian stocks, bonds, mutual funds, gold"
        }
    }
    
    if country not in country_data:
        return f"Limited tax information available for {country}. Consider consulting local financial advisors."
    
    data = country_data[country]
    return f"""
• Capital Gains Tax: {data['capital_gains_tax']}
• Income Tax Rate: {data['income_tax_rate']}
• Current Interest Rate: {data['current_interest_rate']}
• Tax-Advantaged Accounts: {data['tax_accounts']}
• Common Investment Options: {data['investment_options']}
"""

@app.function(
    image=image,
    secrets=[Secret.from_name("nebius-secret")],
    timeout=300,  # Reduced to 5 minutes
    cpu=4,  # Use CPU instead of GPU for faster cold starts
    memory=8192,  # Reduced memory
    keep_warm=2,  # Keep more containers warm
    concurrency_limit=10,  # Allow more concurrent requests
    container_idle_timeout=300  # Keep containers alive longer
)
async def generate_investment_strategy(profile_data: dict):
    """Optimized investment strategy generation"""
    try:
        print(f"🚀 Processing profile: {profile_data}")
        
        # Import here to avoid cold start delays
        from llama_index.llms.nebius import NebiusLLM
        
        # Get country-specific tax and interest rate info
        country_info = get_country_financial_info(profile_data.get('country', 'United States'))
        
        # Use faster model variant
        llm = NebiusLLM(
            api_key=os.getenv("NEBIUS_API_KEY"),
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-fast",  # Smaller, faster model
            timeout=60,  # Shorter LLM timeout
            max_tokens=1500,  # Limit response length
            temperature=0.7
        )
        
        # Enhanced prompt with country-specific information
        prompt = f"""Create a comprehensive investment strategy for a {profile_data.get('country')} resident:

Profile:
• Age: {profile_data.get('age_group')}
• Income: ${profile_data.get('income')}/month
• Expenses: ${profile_data.get('expenses')}/month  
• Risk: {profile_data.get('risk_profile')}
• Goal: {profile_data.get('goal')}
• Timeline: {profile_data.get('timeframe')}
• Country: {profile_data.get('country')}

Country-Specific Financial Context:
{country_info}

Provide:
1. Asset Allocation (percentages) - consider local tax implications
2. Investment Types (prioritize tax-efficient options available in {profile_data.get('country')})
3. Monthly Investment Amount (after considering local taxes)
4. Tax Optimization Strategies specific to {profile_data.get('country')}
5. Key Action Steps

Consider local tax rates, available tax-advantaged accounts, and current interest rates in your recommendations.
Keep response under 400 words."""
        
        # Add timeout to the LLM call
        response = await asyncio.wait_for(
            llm.acomplete(prompt),
            timeout=45  # 45 second timeout for LLM
        )
        
        return {"strategy": str(response), "status": "success"}
        
    except asyncio.TimeoutError:
        return {
            "strategy": "⏱️ **Strategy Generation Timeout**\n\nThe AI took too long to respond. This might be due to high server load. Please try again in a moment.",
            "status": "timeout"
        }
    except Exception as e:
        error_msg = f"Strategy generation error: {str(e)}"
        return {
            "strategy": f"❌ **Error**: {error_msg}\n\nPlease check your inputs and try again.",
            "status": "error"
        }

@app.function(
    image=image,
    timeout=60,  # Quick fallback function
    cpu=2,
    memory=2048,
    keep_warm=1
)
async def generate_basic_strategy(profile_data: dict):
    """Fallback function with rule-based strategy"""
    try:
        age = profile_data.get('age_group', '30s')
        income = float(profile_data.get('income', 0))
        expenses = float(profile_data.get('expenses', 0))
        risk = profile_data.get('risk_profile', 'Moderate')
        goal = profile_data.get('goal', 'General investing')
        timeframe = profile_data.get('timeframe', '5-10 years')
        country = profile_data.get('country', 'United States')
        
        surplus = income - expenses
        
        # Get country-specific info
        country_info = get_country_financial_info(country)
        
        # Rule-based strategy
        if risk == "Conservative":
            stocks, bonds, cash = 30, 50, 20
        elif risk == "Aggressive":
            stocks, bonds, cash = 80, 15, 5
        else:  # Moderate
            stocks, bonds, cash = 60, 30, 10
        
        # Adjust based on age
        if age == "20s":
            stocks += 10
            bonds -= 10
        elif age == "50s+":
            stocks -= 20
            bonds += 15
            cash += 5
        
        monthly_investment = max(surplus * 0.2, 100)
        
        strategy = f"""## 📊 Your Investment Strategy ({country})

**Monthly Investment Capacity:** ${monthly_investment:,.0f}

**Recommended Asset Allocation:**
• Stocks/Equity: {stocks}%
• Bonds: {bonds}%  
• Cash/Emergency: {cash}%

**{country}-Specific Considerations:**
{country_info}

**Action Steps:**
1. Build emergency fund (3-6 months expenses)
2. Maximize tax-advantaged accounts first
3. Start with broad market index funds
4. Consider local tax implications
5. Review and rebalance quarterly

**Timeline:** {timeframe}
**Goal:** {goal}

*This is a basic strategy. Consider consulting a local financial advisor for personalized advice.*"""

        return {"strategy": strategy, "status": "basic"}
        
    except Exception as e:
        return {
            "strategy": f"❌ Unable to generate strategy: {str(e)}",
            "status": "error"
        }

@app.function(image=image, keep_warm=1)
@asgi_app()
def web():
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import time

    web_app = FastAPI(title="Personal Finance Strategist", version="2.0")
    
    # Add CORS middleware
    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @web_app.post("/strategy")
    async def strategy_endpoint(data: dict):
        start_time = time.time()
        
        try:
            if "profile" not in data:
                raise HTTPException(400, "Missing 'profile' field")
            
            profile_data = data["profile"]
            
            # Validate required fields
            required_fields = ['age_group', 'income', 'expenses', 'risk_profile', 'goal', 'timeframe', 'country']
            missing_fields = [field for field in required_fields if not profile_data.get(field)]
            
            if missing_fields:
                raise HTTPException(400, f"Missing fields: {', '.join(missing_fields)}")
            
            print(f"🎯 Processing request: {profile_data}")
            
            # Try AI-powered strategy first with timeout
            try:
                result = await asyncio.wait_for(
                    generate_investment_strategy.remote.aio(profile_data),
                    timeout=120  # 2 minute timeout for the entire function
                )
                
                if result["status"] == "success":
                    print(f"✅ AI strategy completed in {time.time() - start_time:.2f}s")
                    return result
                    
            except asyncio.TimeoutError:
                print("⏱️ AI strategy timed out, falling back to basic strategy")
            except Exception as e:
                print(f"⚠️ AI strategy failed: {e}, falling back to basic strategy")
            
            # Fallback to rule-based strategy
            result = await generate_basic_strategy.remote.aio(profile_data)
            print(f"✅ Basic strategy completed in {time.time() - start_time:.2f}s")
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"❌ Endpoint error: {e}")
            return {
                "strategy": f"❌ **Server Error**: Unable to process your request.\n\nPlease try again or contact support if the issue persists.",
                "status": "error"
            }

    @web_app.get("/health")
    async def health_check():
        return {
            "status": "healthy", 
            "timestamp": time.time(),
            "message": "Service is running"
        }

    @web_app.get("/test")
    async def quick_test():
        """Quick test endpoint"""
        test_profile = {
            "age_group": "30s",
            "income": 5000,
            "expenses": 3000,
            "risk_profile": "Moderate",
            "goal": "Retirement",
            "timeframe": "10 years",
            "country": "United States"
        }
        
        result = await generate_basic_strategy.remote.aio(test_profile)
        return {"test_result": "success", "sample_strategy": result}

    @web_app.get("/")
    async def root():
        return {
            "message": "Personal Finance Strategist API v2.0",
            "endpoints": ["/strategy", "/health", "/test"],
            "optimizations": ["Faster model", "CPU compute", "Fallback strategy", "Better error handling"]
        }

    return web_app



# # modal_app.py
# import os
# from modal import App, Function, Image, Secret, asgi_app
# # from main. import InvestmentWorkflow, ProfileDemographicsEvent

# app = App("personal-investment-strategist-8")

# # Define image with dependencies
# image = (
#     Image.debian_slim(python_version="3.11")
#     .pip_install(
#         "fastapi",
#         "uvicorn",
#         "llama-index",
#         "llama-index-core",
#         "llama-index-llms-nebius",
#         "langchain",
#         "requests",
#         "yfinance",
#         "gradio"
#     ).add_local_file(local_path="main.py", remote_path="/root/main.py").add_local_dir('agents', remote_path='/root/agents').add_local_dir('tools', remote_path='/root/tools')
# )
# # Mount your local code into the image
# # MOUNTS = [
# #     mount.Mount.from_local_dir("./agents", remote_path="/root/agents"),
# #     mount.Mount.from_local_dir("./tools", remote_path="/root/tools"),
# #     mount.Mount.from_local_dir(".", remote_path="/root")  # Main folder mounted here
# # ]

# @app.function(image=image, secrets=[Secret.from_name("nebius-secret")])
# async def run_agent(user_input: str):
#     import sys
#     sys.path.append("/root")

#     try:
#         from main import InvestmentWorkflow
#         workflow = InvestmentWorkflow()
#         result = await workflow.run(user_input=user_input)

#         # Ensure it's a string even if result.response is None
#         strategy_text = result.response or "No strategy generated by LLM."
        
#         return {"strategy": strategy_text}
    
#     except Exception as e:
#         return {
#             "strategy": f"Error generating strategy:\n\n{str(e)}"
#         }
# ## Define a simple function to keep the app alive    
# def fn():
#     pass
    
# @app.function(image=image)
# @asgi_app()
# def web():
#     from fastapi import FastAPI

#     web_app = FastAPI()

#     @web_app.post("/strategy")
#     async def strategy_endpoint(data: dict):
#         user_input = data.get("user_input", "")
#         strategy = await run_agent.remote.aio(user_input)
#         return strategy

#     return web_app
    
# @app.function(image=image)
# @asgi_app()
# def web():
#     from fastapi import FastAPI, Request
#     app = FastAPI()

#     # @app.post("/strategy")
#     # async def strategy_endpoint(request: Request):
#     #     data = await request.json()
#     #     user_input = data.get("user_input", "")
#     #     strategy = await run_agent.remote.aio(user_input)
#     #     return strategy
#     @app.post("/strategy")
#     async def strategy_endpoint(data: dict):
#         user_input = data.get("user_input", "")
#         strategy = await run_agent.remote.aio(user_input)
#         return {"strategy": strategy["strategy"]}
#     return app

# # modal_app.py

# import os
# from modal import App, Function, Image, Secret

# # Define image with FastAPI explicitly installed
# image = (
#     Image.from_registry("nvidia/cuda:12.1.0-base", add_python="3.11")
#     .apt_install("git", "ffmpeg")
#     .pip_install(
#         "llama-index",
#         "llama-index-core",
#         "llama-index-llms-nebius",
#         "langchain",
#         "requests",
#         "yfinance",
#         "gradio",
#         "fastapi",
#         "uvicorn"
#     )
# )

# app = App("investment-strategist")

# @app.function(
#     image=image,
#     secrets=[Secret.from_name("nebius-secret")],
#     timeout=600,
#     max_containers=5,
#     gpu="A10G"  # or A100-40gb if you prefer more power
# )
# def f():
#     pass

# # Import InvestmentWorkflow inside function to avoid top-level import issues
# @app.function(image=image, secrets=[Secret.from_name("nebius-secret")])
# async def run_agent(user_input: str):
#     from main import InvestmentWorkflow
#     workflow = InvestmentWorkflow()
#     result = await workflow.run(user_input=user_input)
#     return {"strategy": result.response}

# # Create FastAPI app
# web_app = FastAPI()

# @web_app.post("/strategy")
# async def strategy_endpoint(data: dict):
#     user_input = data.get("user_input", "")
#     strategy = await run_agent.remote(user_input)
#     return strategy

# # Expose the web endpoint
# app.web_endpoint()(web_app)