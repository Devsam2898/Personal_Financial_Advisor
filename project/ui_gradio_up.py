# app.py - Enhanced Professional UI
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

# Enhanced professional CSS styling
custom_css = """
/* Global container styling */
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    min-height: 100vh;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Main content area */
.main-content {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    margin: 2rem !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Header styling */
.finance-header {
    text-align: center;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.finance-header::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.1;
}

.finance-header h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    margin-bottom: 1rem !important;
    background: linear-gradient(45deg, #ffffff, #e0e7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    z-index: 1;
}

.finance-header p {
    font-size: 1.25rem !important;
    opacity: 0.9 !important;
    margin-bottom: 0 !important;
    position: relative;
    z-index: 1;
}

/* Icon styling */
.finance-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    position: relative;
    z-index: 1;
}

/* Form sections */
.form-section {
    background: white !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s ease !important;
}

.form-section:hover {
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12) !important;
    transform: translateY(-2px) !important;
}

.form-section h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    margin-bottom: 1.5rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
}

/* Input styling */
.gradio-textbox, .gradio-number {
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    transition: all 0.3s ease !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}

.gradio-textbox:focus, .gradio-number:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
}

/* Dropdown styling - more specific selectors */
.gradio-dropdown .wrap {
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    transition: all 0.3s ease !important;
}

.gradio-dropdown .wrap:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

.gradio-dropdown select, .gradio-dropdown input {
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    border: none !important;
    background: transparent !important;
}

.gradio-dropdown .dropdown {
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
}

/* Button styling */
.primary-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: white !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3) !important;
    min-height: 56px !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4) !important;
}

.secondary-btn {
    background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: white !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 24px rgba(100, 116, 139, 0.3) !important;
    min-height: 56px !important;
}

.secondary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(100, 116, 139, 0.4) !important;
}

/* Output area styling */
.output-area {
    background: white !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    margin-top: 2rem !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    min-height: 200px !important;
}

/* Tips section */
.tips-section {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    margin: 2rem 0 !important;
    border-left: 4px solid #667eea !important;
}

.tips-section h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
    margin-bottom: 1rem !important;
}

/* Radio button styling */
.gradio-radio {
    gap: 1rem !important;
}

.gradio-radio label {
    background: white !important;
    border: 2px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

.gradio-radio label:hover {
    border-color: #667eea !important;
    background: #f8fafc !important;
}

.gradio-radio input:checked + label {
    border-color: #667eea !important;
    background: linear-gradient(135deg, #667eea10, #764ba210) !important;
    color: #1e3c72 !important;
}

/* Progress indicator */
.loading-indicator {
    background: linear-gradient(90deg, #667eea, #764ba2, #667eea) !important;
    background-size: 200% 100% !important;
    animation: gradient 2s ease infinite !important;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Responsive design */
@media (max-width: 768px) {
    .finance-header h1 {
        font-size: 2rem !important;
    }
    
    .form-section {
        padding: 1.5rem !important;
    }
    
    .main-content {
        margin: 1rem !important;
        padding: 1.5rem !important;
    }
}

/* Chart and finance icons */
.finance-bg {
    position: relative;
    overflow: hidden;
}

.finance-bg::after {
    content: "📈📊💰🏦💳📋";
    position: absolute;
    top: -20px;
    right: -20px;
    font-size: 6rem;
    opacity: 0.05;
    z-index: 0;
    transform: rotate(12deg);
}
"""

# Create the enhanced interface
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"),
    title="💼 AI Investment Strategist Pro",
    css=custom_css
) as interface:
    
    # Header Section
    with gr.Row(elem_classes="finance-header finance-bg"):
        gr.HTML("""
            <div style="text-align: center; position: relative; z-index: 1;">
                <div class="finance-icon">💼</div>
                <h1>AI Investment Strategist Pro</h1>
                <p>Professional-Grade Investment Strategy Generator</p>
                <div style="margin-top: 1rem; font-size: 0.95rem; opacity: 0.8;">
                    🤖 Powered by Advanced AI  •  🔒 Secure & Private  •  📊 Data-Driven Insights
                </div>
            </div>
        """)
    
    with gr.Row(elem_classes="main-content"):
        with gr.Column():
            
            # Personal Information Section
            with gr.Group(elem_classes="form-section"):
                gr.HTML("<h3>👤 Personal Profile</h3>")
                
                with gr.Row():
                    age_group = gr.Dropdown(
                        choices=["20s", "30s", "40s", "50s+"], 
                        label="📅 Age Group",
                        value="30s",
                        info="Your current life stage affects investment timeline"
                    )
                    
                    country = gr.Dropdown(
                        choices=[
                            "🇺🇸 United States", "🇨🇦 Canada", "🇬🇧 United Kingdom", 
                            "🇩🇪 Germany", "🇫🇷 France", "🇮🇹 Italy", "🇯🇵 Japan", "🇮🇳 India"
                        ],
                        label="🌍 Country of Residence",
                        value="🇺🇸 United States",
                        info="Tax jurisdiction for investment recommendations"
                    )
            
            # Financial Information Section
            with gr.Group(elem_classes="form-section"):
                gr.HTML("<h3>💰 Financial Overview</h3>")
                
                with gr.Row():
                    income = gr.Number(
                        label="💵 Monthly Income ($)", 
                        value=6000,
                        minimum=0,
                        info="Total monthly income before taxes and deductions"
                    )
                    expenses = gr.Number(
                        label="💸 Monthly Expenses ($)", 
                        value=4000,
                        minimum=0,
                        info="Total monthly living expenses and obligations"
                    )
                
                # Financial health indicator
                gr.HTML("""
                    <div style="background: linear-gradient(90deg, #10b981, #059669); color: white; 
                               padding: 1rem; border-radius: 8px; margin-top: 1rem; font-size: 0.9rem;">
                        💡 <strong>Quick Tip:</strong> A healthy savings rate is typically 20% or more of your income
                    </div>
                """)
            
            # Investment Preferences Section
            with gr.Group(elem_classes="form-section"):
                gr.HTML("<h3>🎯 Investment Strategy</h3>")
                
                risk_profile = gr.Radio(
                    choices=["🛡️ Conservative", "⚖️ Moderate", "🚀 Aggressive"], 
                    label="📊 Risk Tolerance",
                    value="⚖️ Moderate",
                    info="How comfortable are you with potential investment losses?"
                )
                
                with gr.Row():
                    goal = gr.Textbox(
                        label="🎯 Primary Financial Goal", 
                        placeholder="e.g., Down payment for house, retirement planning, children's education, emergency fund",
                        info="Be specific about what you're working towards",
                        lines=2
                    )
                    timeframe = gr.Textbox(
                        label="⏰ Investment Timeline", 
                        placeholder="e.g., 3-5 years, 10+ years, until age 65",
                        info="When do you need to access these funds?",
                        lines=2
                    )
            
            # Action Buttons
            with gr.Row():
                with gr.Column(scale=3):
                    submit_btn = gr.Button(
                        "🚀 Generate My Investment Strategy", 
                        variant="primary",
                        size="lg",
                        elem_classes="primary-btn"
                    )
                with gr.Column(scale=1):
                    test_btn = gr.Button(
                        "🔍 Test Service", 
                        variant="secondary",
                        size="lg",
                        elem_classes="secondary-btn"
                    )
            
            # Tips Section
            with gr.Group(elem_classes="tips-section"):
                gr.HTML("""
                    <h4>💡 Pro Tips for Better Results</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem;">
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">✓</span>
                            <span><strong>Be Specific:</strong> Detailed goals lead to better recommendations</span>
                        </div>
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">✓</span>
                            <span><strong>Realistic Timeline:</strong> Match your goals with appropriate timeframes</span>
                        </div>
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">✓</span>
                            <span><strong>Know Your Risk:</strong> Be honest about your comfort level</span>
                        </div>
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">✓</span>
                            <span><strong>Positive Cash Flow:</strong> Ensure income exceeds expenses</span>
                        </div>
                    </div>
                """)
            
            # Output Section
            with gr.Group(elem_classes="output-area"):
                output = gr.Markdown(
                    value="""
                    ## 🎯 Ready to Get Started?
                    
                    Fill out your financial profile above and click **"Generate My Investment Strategy"** to receive:
                    
                    📋 **Personalized Investment Plan**  
                    📊 **Asset Allocation Recommendations**  
                    🏦 **Account Type Suggestions**  
                    💡 **Tax Optimization Strategies**  
                    📈 **Risk Management Advice**  
                    
                    *Your data is processed securely and never stored permanently.*
                    """,
                    elem_id="strategy-output"
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