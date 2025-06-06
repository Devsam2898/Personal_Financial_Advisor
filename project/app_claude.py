# app.py - Optimized with better timeout handling
import gradio as gr
import requests
import json
import asyncio
import aiohttp
from typing import Optional

# Update this to your new optimized Modal URL
MODAL_URL = "https://devsam2898--personal-investment-strategist-optimized-web.modal.run/strategy"
HEALTH_URL = "https://devsam2898--personal-investment-strategist-optimized-web.modal.run/health"
TEST_URL = "https://devsam2898--personal-investment-strategist-optimized-web.modal.run/test"

async def get_investment_strategy_async(age_group, income, expenses, risk_profile, goal, timeframe, country):
    """Async version with better timeout handling"""
    
    # Input validation
    if not all([age_group, income, expenses, risk_profile, goal, timeframe, country]):
        return "❌ Please fill in all fields to get a personalized strategy."
    
    # Convert income and expenses to numbers
    try:
        income_val = float(str(income).replace('$', '').replace(',', '')) if income else 0
        expenses_val = float(str(expenses).replace('$', '').replace(',', '')) if expenses else 0
    except ValueError:
        return "❌ Please enter valid numbers for income and expenses."
    
    # Validate financial logic
    if income_val <= 0:
        return "❌ Income must be greater than 0."
    if expenses_val < 0:
        return "❌ Expenses cannot be negative."
    if expenses_val >= income_val:
        return "⚠️ **Warning**: Your expenses are equal to or exceed your income. Consider budgeting advice before investing."

    payload = {
        "profile": {
            "age_group": age_group,
            "income": income_val,
            "expenses": expenses_val,
            "risk_profile": risk_profile,
            "goal": goal,
            "timeframe": timeframe,
            "country": country
        }
    }
    
    try:
        print(f"🚀 Sending request to: {MODAL_URL}")
        
        # Use aiohttp for better async handling
        timeout = aiohttp.ClientTimeout(total=150)  # 2.5 minute timeout
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                MODAL_URL,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            ) as response:
                
                print(f"📊 Response status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    strategy = result.get("strategy", "No strategy returned.")
                    status = result.get("status", "unknown")
                    
                    # Add status indicator
                    if status == "basic":
                        prefix = "## 📊 Your Investment Strategy (Rule-Based)\n*AI service was unavailable, using optimized rule-based strategy*\n\n"
                    else:
                        prefix = "## 📊 Your Personalized Investment Strategy\n*Powered by AI*\n\n"
                    
                    return f"{prefix}{strategy}"
                else:
                    error_text = await response.text()
                    return f"❌ **Service Error ({response.status})**\n\nThe backend service returned an error. Please try again in a moment.\n\nDetails: {error_text[:200]}..."
                    
    except asyncio.TimeoutError:
        return """⏱️ **Request Timeout**

The AI service is taking longer than expected. This could be due to:
- High server load
- Cold start (first request after idle period)
- Network connectivity issues

**What to try:**
1. Wait 30 seconds and try again
2. Simplify your goal description
3. Check if the service is healthy using the 'Test Service' button"""

    except aiohttp.ClientError as e:
        return f"""🔌 **Connection Error**

Unable to connect to the backend service.

**Possible causes:**
- Service is starting up (cold start)
- Network connectivity issues
- Service is temporarily down

**What to try:**
1. Wait 1-2 minutes and try again
2. Check service health with 'Test Service' button
3. Refresh the page

*Technical details: {str(e)}*"""

    except Exception as e:
        return f"""❌ **Unexpected Error**

An unexpected error occurred: {str(e)}

Please try again or contact support if the issue persists."""

def get_investment_strategy(age_group, income, expenses, risk_profile, goal, timeframe, country):
    """Sync wrapper for async function"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            get_investment_strategy_async(age_group, income, expenses, risk_profile, goal, timeframe, country)
        )
        loop.close()
        return result
    except Exception as e:
        return f"❌ **Error**: {str(e)}"

async def test_service_async():
    """Test service connectivity"""
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Test health endpoint first
            try:
                async with session.get(HEALTH_URL) as response:
                    if response.status == 200:
                        health_data = await response.json()
                        health_status = f"✅ Service is healthy\n- Status: {health_data.get('status')}\n- Timestamp: {health_data.get('timestamp')}"
                    else:
                        health_status = f"⚠️ Health check returned status {response.status}"
            except Exception as e:
                health_status = f"❌ Health check failed: {str(e)}"
            
            # Test strategy endpoint with sample data
            try:
                async with session.get(TEST_URL) as response:
                    if response.status == 200:
                        test_data = await response.json()
                        test_status = f"✅ Test endpoint working\n- Result: {test_data.get('test_result')}"
                    else:
                        test_status = f"⚠️ Test endpoint returned status {response.status}"
            except Exception as e:
                test_status = f"❌ Test endpoint failed: {str(e)}"
            
            return f"""## 🔍 Service Status Check

**Health Check:**
{health_status}

**Functionality Test:**
{test_status}

**Service URL:** {MODAL_URL}

*Last checked: {asyncio.get_event_loop().time()}*"""
            
    except Exception as e:
        return f"""❌ **Service Test Failed**

Unable to connect to the service.

Error: {str(e)}

**Troubleshooting:**
1. Check if the Modal deployment is running
2. Verify the service URL is correct
3. Check network connectivity"""

def test_service():
    """Sync wrapper for service test"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test_service_async())
        loop.close()
        return result
    except Exception as e:
        return f"❌ **Test Error**: {str(e)}"

# Create the interface with better UX
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"), 
    title="📈 Personal Finance Strategist",
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .status-box {
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
    }
    """
) as interface:
    
    gr.Markdown(
        """
        # 📈 Personal Finance Strategist
        **AI-Powered Investment Strategy Generator**
        
        Get personalized investment recommendations based on your financial profile and goals.
        
        ---
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 👤 Personal Information")
            age_group = gr.Dropdown(
                choices=["20s", "30s", "40s", "50s+"], 
                label="Age Group",
                value="30s",
                info="Select your current age range"
            )
            
            country = gr.Dropdown(
                choices=[
                    "United States", "Canada", "United Kingdom", 
                    "Germany", "France", "Italy", "Japan", "India"
                ],
                label="Country of Residence",
                value="United States",
                info="Your tax residence country"
            )
            
            gr.Markdown("### 💰 Financial Information")
            income = gr.Number(
                label="Monthly Income ($)", 
                value=6000,
                minimum=0,
                info="Your total monthly income before taxes"
            )
            expenses = gr.Number(
                label="Monthly Expenses ($)", 
                value=4000,
                minimum=0,
                info="Your total monthly expenses"
            )
            
        with gr.Column(scale=1):
            gr.Markdown("### 🎯 Investment Preferences")
            risk_profile = gr.Radio(
                choices=["Conservative", "Moderate", "Aggressive"], 
                label="Risk Tolerance",
                value="Moderate",
                info="How comfortable are you with investment risk?"
            )
            goal = gr.Textbox(
                label="Financial Goal", 
                placeholder="e.g., buy a house, retirement, emergency fund, child's education",
                info="What are you saving/investing for?"
            )
            timeframe = gr.Textbox(
                label="Investment Timeframe", 
                placeholder="e.g., 5 years, 10 years, until retirement",
                info="How long do you plan to invest?"
            )
    
    gr.Markdown("---")
    
    with gr.Row():
        submit_btn = gr.Button(
            "🚀 Generate Investment Strategy", 
            variant="primary",
            size="lg"
        )
        test_btn = gr.Button(
            "🔍 Test Service", 
            variant="secondary",
            size="lg"
        )
    
    with gr.Row():
        gr.Markdown(
            """
            **💡 Tips for best results:**
            - Be specific about your financial goal
            - Include realistic timeframes  
            - Consider your actual risk tolerance
            - Make sure your income > expenses for meaningful investing
            - Country selection affects tax-advantaged account recommendations
            """
        )
    
    output = gr.Markdown(
        label="Investment Strategy",
        value="Click 'Generate Investment Strategy' to get your personalized recommendations!"
    )
    
    # Event handlers
    submit_btn.click(
        fn=get_investment_strategy,
        inputs=[age_group, income, expenses, risk_profile, goal, timeframe, country],
        outputs=output,
        show_progress=True
    )
    
    test_btn.click(
        fn=test_service,
        outputs=output,
        show_progress=True
    )

if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        debug=True
    )