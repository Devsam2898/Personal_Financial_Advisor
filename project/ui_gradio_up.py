# app.py - Updated for New Modal Backend
import gradio as gr
import requests
import json
import asyncio
import aiohttp
from typing import Optional
from fpdf import FPDF

# Updated URLs to match your actual Modal deployment
MODAL_BASE_URL = "https://devsam2898--personal-investment-strategist-enhanced-web.modal.run"
# Based on your original code, these might be the correct endpoints:
STRATEGY_URL = f"{MODAL_BASE_URL}/strategy"  # Original endpoint name
HEALTH_URL = f"{MODAL_BASE_URL}/health"
MARKET_DATA_URL = f"{MODAL_BASE_URL}/market_data"  # May not exist yet
COUNTRY_ANALYSIS_URL = f"{MODAL_BASE_URL}/country_analysis"  # May not exist yet
TEST_URL = f"{MODAL_BASE_URL}/test"  # Original test endpoint

async def get_investment_strategy_async(age_group, income, expenses, current_assets, current_liabilities, risk_profile, goal, timeframe, country):
    """Updated async function for new Modal backend structure"""
    
    # Input validation
    if not all([age_group, income, expenses, risk_profile, goal, timeframe, country]):
        return "❌ Please fill in all fields to get a personalized strategy."
    
    # Convert income, expenses, assets, and liabilities to numbers
    try:
        income_val = float(str(income).replace('$', '').replace(',', '')) if income else 0
        expenses_val = float(str(expenses).replace('$', '').replace(',', '')) if expenses else 0
        assets_val = float(str(current_assets).replace('$', '').replace(',', '')) if current_assets else 0
        liabilities_val = float(str(current_liabilities).replace('$', '').replace(',', '')) if current_liabilities else 0
    except ValueError:
        return "❌ Please enter valid numbers for income, expenses, assets, and liabilities."
    
    # Validate financial logic
    if income_val <= 0:
        return "❌ Income must be greater than 0."
    if expenses_val < 0:
        return "❌ Expenses cannot be negative."
    if assets_val < 0:
        return "❌ Assets cannot be negative."
    if liabilities_val < 0:
        return "❌ Liabilities cannot be negative."
    if expenses_val >= income_val:
        return "⚠️ **Warning**: Your expenses are equal to or exceed your income. Consider budgeting advice before investing."

    # Clean country name (remove emoji flags if present)
    clean_country = country.split(' ', 1)[-1] if '🇺🇸' in country or '🇨🇦' in country else country

    # Updated payload structure to match original Modal backend
    payload = {
        "profile": {
            "age_group": age_group,
            "income": income_val,
            "expenses": expenses_val,
            "current_assets": assets_val,
            "current_liabilities": liabilities_val,
            "risk_profile": risk_profile,
            "goal": goal,
            "timeframe": timeframe,
            "country": clean_country
        }
    }
    
    try:
        print(f"🚀 Sending request to: {STRATEGY_URL}")
        
        # Use aiohttp for better async handling
        timeout = aiohttp.ClientTimeout(total=180)  # 3 minute timeout for comprehensive analysis
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                STRATEGY_URL,
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
                    processing_time = result.get("processing_time", 0)
                    
                    # Add enhanced status indicator
                    if status == "success":
                        prefix = f"## 💼 Your Comprehensive Investment Strategy\n*✨ AI-Powered Analysis Complete (Generated in {processing_time:.1f}s)*\n\n"
                    elif status == "validation_error":
                        return f"❌ **Validation Error**\n\n{strategy}"
                    elif status == "llm_error":
                        prefix = "## 📊 Your Investment Strategy (Rule-Based Fallback)\n*⚠️ AI service temporarily unavailable, using optimized rule-based strategy*\n\n"
                    else:
                        prefix = "## 📊 Your Investment Strategy\n*Generated using advanced algorithms*\n\n"
                    
                    return f"{prefix}{strategy}"
                else:
                    error_text = await response.text()
                    return f"❌ **Service Error ({response.status})**\n\nThe backend service returned an error. Please try again in a moment.\n\nDetails: {error_text[:200]}..."
                    
    except asyncio.TimeoutError:
        return """⏱️ **Request Timeout**

The comprehensive AI analysis is taking longer than expected. This could be due to:
- Extensive market data collection and analysis
- Real-time financial data processing
- High server load or cold start
- Complex tax calculations

**What to try:**
1. Wait 1-2 minutes and try again
2. Check if the service is healthy using the 'Test Service' button
3. Simplify your goal description if very detailed"""

    except aiohttp.ClientError as e:
        return f"""🔌 **Connection Error**

Unable to connect to the enhanced backend service.

**Possible causes:**
- Service is performing cold start (initial startup)
- Network connectivity issues
- Enhanced features are initializing

**What to try:**
1. Wait 2-3 minutes and try again (cold start can take time)
2. Check service health with 'Test Service' button
3. Refresh the page

*Technical details: {str(e)}*"""

    except Exception as e:
        return f"""❌ **Unexpected Error**

An unexpected error occurred: {str(e)}

Please try again or contact support if the issue persists."""

def get_investment_strategy(age_group, income, expenses, current_assets, current_liabilities, risk_profile, goal, timeframe, country):
    """Sync wrapper for async function"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            get_investment_strategy_async(age_group, income, expenses, current_assets, current_liabilities, risk_profile, goal, timeframe, country)
        )
        loop.close()
        return result
    except Exception as e:
        return f"❌ **Error**: {str(e)}"

async def test_service_async():
    """Enhanced service connectivity test"""
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Test health endpoint
            try:
                async with session.get(HEALTH_URL) as response:
                    if response.status == 200:
                        health_data = await response.json()
                        health_status = f"""✅ **Service is healthy**
- Status: {health_data.get('status')}
- Version: {health_data.get('version', 'N/A')}
- Timestamp: {health_data.get('timestamp')}"""
                    else:
                        health_status = f"⚠️ Health check returned status {response.status}"
            except Exception as e:
                health_status = f"❌ Health check failed: {str(e)}"
            
            # Test market data endpoint (may not be available)
            try:
                async with session.get(MARKET_DATA_URL) as response:
                    if response.status == 200:
                        market_data = await response.json()
                        market_status = f"""✅ **Market data service working**
- Status: {market_data.get('status')}
- Timestamp: {market_data.get('timestamp')}
- Features: Real-time market data, sector analysis"""
                    else:
                        market_status = f"⚠️ Market data endpoint returned status {response.status}"
            except Exception as e:
                market_status = f"ℹ️ Market data endpoint not available (integrated into strategy generation)"
            
            # Test strategy endpoint with sample data (using original test endpoint)
            try:
                async with session.get(TEST_URL) as response:
                    if response.status == 200:
                        test_data = await response.json()
                        country_status = f"""✅ **Strategy endpoint working**
- Result: {test_data.get('test_result', 'Test passed')}
- Features: Investment strategy generation"""
                    else:
                        country_status = f"⚠️ Test endpoint returned status {response.status}"
            except Exception as e:
                country_status = f"❌ Strategy test failed: {str(e)}"
            
            return f"""## 🔍 Enhanced Service Status Check

**Core Health:**
{health_status}

**Market Data Service:**
{market_status}

**Strategy Service:**
{country_status}

**Service Features:**
✨ Real-time market data via Yahoo Finance
🏦 Comprehensive tax analysis for 8+ countries  
🤖 AI-powered strategy generation
📊 Bullish sector and stock analysis
🌍 Country-specific financial context

**Service URL:** {MODAL_BASE_URL}

*Last checked: {asyncio.get_event_loop().time()}*"""
            
    except Exception as e:
        return f"""❌ **Service Test Failed**

Unable to connect to the enhanced service.

Error: {str(e)}

**Troubleshooting:**
1. Check if the Modal deployment is running
2. Verify the service URL is correct: {MODAL_BASE_URL}
3. Check network connectivity
4. Allow extra time for cold start (enhanced features take longer to initialize)"""

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

async def get_market_preview_async():
    """Get current market data preview - simplified for original backend"""
    try:
        # Since market data might be integrated into the main strategy endpoint,
        # we'll provide a static preview and note that full data is in strategy generation
        return """## 📊 Market Analysis Available

**Real-Time Data Integration:**
• Market indices (S&P 500, NASDAQ, Dow Jones, etc.)
• Sector performance analysis  
• Bullish stock identification
• Economic indicators by country

**📈 Full market analysis included in your personalized strategy generation**

*Click 'Generate Strategy' for comprehensive market data and analysis*"""
                
    except Exception as e:
        return "📊 **Market analysis integrated into strategy generation**\n\nFull market data will be included in your personalized strategy."

def get_market_preview():
    """Sync wrapper for market preview"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_market_preview_async())
        loop.close()
        return result
    except Exception as e:
        return "📊 **Market preview unavailable**\n\nFull analysis available in strategy generation."
    
def generate_pdf(strategy):
    """Generate PDF from strategy"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add strategy content to PDF with UTF-8 encoding
    for line in strategy.split('\n'):
        # Encode the line to UTF-8 and decode it back to handle Unicode characters
        pdf.cell(0, 10, txt=line.encode('utf-8').decode('latin-1', 'ignore'), ln=True)

    pdf_output = "investment_strategy.pdf"
    pdf.output(pdf_output)
    return pdf_output

def download_strategy(strategy):
    """Download strategy as PDF"""
    pdf_path = generate_pdf(strategy)
    return pdf_path

# Enhanced CSS with new features
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

/* Enhanced form sections */
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

/* Input styling - only for textboxes and numbers */
input[type="text"], input[type="number"], textarea {
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    transition: all 0.3s ease !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}

input[type="text"]:focus, input[type="number"]:focus, textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    outline: none !important;
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

/* Market preview styling */
.market-preview {
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    margin: 1.5rem 0 !important;
    border-left: 4px solid #0ea5e9 !important;
    font-size: 0.9rem !important;
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
"""

# Create the enhanced interface
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"),
    title="💼 Vittaśāstra - AI Strategist Enhanced",
    css=custom_css
) as interface:
    
    # Header Section
    with gr.Row(elem_classes="finance-header finance-bg"):
        gr.HTML("""
            <div style="text-align: center; position: relative; z-index: 1;">
                <div class="finance-icon">💼</div>
                <h1>Vittaśāstra - AI Strategist Enhanced</h1>
                <p>Professional-Grade Investment Strategy Generator</p>
                <div style="margin-top: 1rem; font-size: 0.95rem; opacity: 0.8;">
                    🤖 Enhanced AI Analysis • 📊 Real-Time Market Data • 🏦 Tax Optimization • 🔒 Secure & Private
                </div>
            </div>
        """)
    
    with gr.Row(elem_classes="main-content"):
        with gr.Column():
            
            # Market Preview Section
            with gr.Group(elem_classes="market-preview"):
                market_preview = gr.Markdown(
                    value="📊 **Loading current market data...**",
                    elem_id="market-preview"
                )
            
            # Personal Information Section
            with gr.Group(elem_classes="form-section"):
                gr.HTML("<h3>👤 Personal Profile</h3>")

                with gr.Row():
                    age_group = gr.Textbox(
                        label="📅 Age Group",
                        value="30s",
                        info="Your current life stage affects investment timeline",
                        interactive=True,
                        show_label=True
                    )

                    country = gr.Textbox(
                        label="🌍 Country of Residence",
                        value="United States",
                        info="Tax jurisdiction for investment recommendations",
                        interactive=True,
                        show_label=True
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
                
                with gr.Row():
                    current_assets = gr.Number(
                        label="💎 Current Assets ($)", 
                        value=25000,
                        minimum=0,
                        info="Total value of current investments, savings, property, etc."
                    )
                    current_liabilities = gr.Number(
                        label="💳 Current Liabilities ($)", 
                        value=10000,
                        minimum=0,
                        info="Total debt including credit cards, loans, mortgages, etc."
                    )
                
                # Financial health indicator
                gr.HTML("""
                    <div style="background: linear-gradient(90deg, #10b981, #059669); color: white; 
                               padding: 1rem; border-radius: 8px; margin-top: 1rem; font-size: 0.9rem;">
                        💡 <strong>Enhanced Analysis:</strong> The new system provides comprehensive tax optimization, 
                        real-time market data, and personalized asset allocation based on your complete financial profile.
                    </div>
                """)
            
            # Investment Preferences Section
            with gr.Group(elem_classes="form-section"):
                gr.HTML("<h3>🎯 Investment Strategy</h3>")
                
                risk_profile = gr.Radio(
                    choices=["Conservative", "Moderate", "Aggressive"], 
                    label="📊 Risk Tolerance",
                    value="Moderate",
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
                        "🚀 Generate Enhanced Investment Strategy", 
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
            
            # Enhanced Tips Section
            with gr.Group(elem_classes="tips-section"):
                gr.HTML("""
                    <h4>✨ Enhanced Features & Pro Tips</h4>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 1rem;">
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">📊</span>
                            <span><strong>Real-Time Market Data:</strong> Live analysis of market conditions and sector performance</span>
                        </div>
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">🏦</span>
                            <span><strong>Tax Optimization:</strong> Country-specific tax strategies and account recommendations</span>
                        </div>
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">🤖</span>
                            <span><strong>AI-Powered Analysis:</strong> Advanced algorithms for personalized recommendations</span>
                        </div>
                        <div style="display: flex; align-items: start; gap: 0.5rem;">
                            <span style="color: #10b981; font-size: 1.2rem;">💎</span>
                            <span><strong>Complete Financial Picture:</strong> Assets, liabilities, and cash flow analysis</span>
                        </div>
                    </div>
                """)
            
            # Output Section
            with gr.Group(elem_classes="output-area"):
                output = gr.Markdown(
                    value="""
                    ## 🎯 Ready for Enhanced Analysis?

                    The enhanced system provides:

                    📊 **Real-Time Market Analysis** - Current indices, sector performance, bullish stocks
                    🏦 **Comprehensive Tax Optimization** - Country-specific strategies and calculations  
                    💼 **Professional Asset Allocation** - Based on your complete financial profile
                    📈 **Advanced Risk Management** - Tailored to your risk tolerance and timeline
                    🌍 **Global Financial Context** - Economic indicators and country-specific advice
                    💡 **Implementation Roadmap** - Step-by-step action plan

                    *Enhanced with real-time data processing and comprehensive financial analysis.*
                    """,
                    elem_id="strategy-output"
                )
                download_btn = gr.Button("📥 Download Strategy as PDF", variant="secondary", elem_classes="secondary-btn")
    
    # Event handlers
    submit_btn.click(
        fn=get_investment_strategy,
        inputs=[age_group, income, expenses, current_assets, current_liabilities, risk_profile, goal, timeframe, country],
        outputs=output,
        show_progress=True
    )
    
    test_btn.click(
        fn=test_service,
        outputs=output,
        show_progress=True
    )

    download_btn.click(
        fn=download_strategy,
        inputs=output,
        outputs=gr.File(label="Download PDF")
    )
    
    # Load market data on startup
    interface.load(
        fn=get_market_preview,
        outputs=market_preview
    )

if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        debug=True
    )
