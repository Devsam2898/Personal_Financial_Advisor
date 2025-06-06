from llama_index.core.workflow import Workflow, Context, step, Event, StopEvent
from agents.input_analyzer import create_input_analyzer
from agents.demographic_profiler import create_demographic_profiler
from agents.net_worth_checker import create_networth_checker
from agents.financial_literacy import create_literacy_detector
from agents.economic_analyst import create_economic_analyst
from agents.strategy_advisor import create_strategy_advisor

# Define all event payload classes
class AnalyzeInputEvent(Event):
    user_input: str

class ProfileDemographicsEvent(Event):
    profile: dict

class EnrichedProfileEvent(Event):
    enriched_profile: dict

class NetWorthEvent(Event):
    networth_profile: dict

class LiteracyEvent(Event):
    literacy_profile: dict

class GenerateStrategyEvent(Event):
    econ_profile: dict

def format_strategy(result_dict):
    """Converts structured agent response into clean Markdown strategy"""
    strategy = result_dict.get("response", "")
    
    if isinstance(strategy, dict):
        strategy_str = ""

        if "recommended_allocation" in strategy:
            strategy_str += "### Asset Allocation\n"
            strategy_str += "- " + "\n- ".join([f"{k}: {v}" for k, v in strategy["recommended_allocation"].items()])
            strategy_str += "\n\n"

        if "recommended_instruments" in strategy:
            strategy_str += "### Recommended Instruments\n"
            strategy_str += "- " + "\n- ".join(strategy["recommended_instruments"])
            strategy_str += "\n\n"

        if "tax_optimization_tips" in strategy:
            strategy_str += "### Tax Optimization Tips\n"
            strategy_str += "- " + "\n- ".join(strategy["tax_optimization_tips"])
            strategy_str += "\n\n"

        if "risk_management_notes" in strategy:
            strategy_str += "### Risk Management Notes\n"
            strategy_str += strategy["risk_management_notes"]
        
        return strategy_str.strip() or "No strategy generated."
    
    # If already a string (Markdown), just return
    if isinstance(strategy, str):
        return strategy.strip()

    # Fallback: show raw response or error
    return f"Strategy not properly formatted:\n\n{str(strategy)}"

class InvestmentWorkflow(Workflow):
    def __init__(self):
        # Initialize all agents
        self.input_analyzer = create_input_analyzer()
        self.demographic_profiler = create_demographic_profiler()
        self.net_worth_checker = create_networth_checker()
        self.literacy_detector = create_literacy_detector()
        self.economic_analyst = create_economic_analyst()
        self.strategy_advisor = create_strategy_advisor()
        
        # Set the entry point AFTER initialization
        super().__init__()

    @step
    async def analyze_input(self, ctx: Context, ev: AnalyzeInputEvent) -> ProfileDemographicsEvent:
        """Entry point - analyze user input and extract profile"""
        profile = await self.input_analyzer.arun(ev.user_input)
        await ctx.set("profile", profile)
        return ProfileDemographicsEvent(profile=profile)

    @step
    async def profile_demographics(self, ctx: Context, ev: ProfileDemographicsEvent) -> EnrichedProfileEvent:
        """Enrich profile with demographic analysis"""
        enriched_profile = await self.demographic_profiler.arun(ev.profile)
        await ctx.set("enriched_profile", enriched_profile)
        return EnrichedProfileEvent(enriched_profile=enriched_profile)

    @step
    async def check_net_worth(self, ctx: Context, ev: EnrichedProfileEvent) -> NetWorthEvent:
        """Calculate and analyze net worth"""
        networth_profile = await self.net_worth_checker.arun(ev.enriched_profile)
        await ctx.set("networth_profile", networth_profile)
        return NetWorthEvent(networth_profile=networth_profile)

    @step
    async def detect_literacy(self, ctx: Context, ev: NetWorthEvent) -> LiteracyEvent:
        """Assess financial literacy level"""
        literacy_profile = await self.literacy_detector.arun(ev.networth_profile)
        await ctx.set("literacy_profile", literacy_profile)
        return LiteracyEvent(literacy_profile=literacy_profile)

    @step
    async def fetch_economic_data(self, ctx: Context, ev: LiteracyEvent) -> GenerateStrategyEvent:
        """Fetch current economic data and market conditions"""
        econ_profile = await self.economic_analyst.arun(ev.literacy_profile)
        await ctx.set("econ_profile", econ_profile)
        return GenerateStrategyEvent(econ_profile=econ_profile)

    @step
    async def generate_strategy(self, ctx: Context, ev: GenerateStrategyEvent) -> StopEvent:
        """Generate final investment strategy"""
        strategy = await self.strategy_advisor.arun(ev.econ_profile)
        
        # Format the strategy properly
        if hasattr(strategy, 'response'):
            formatted_strategy = format_strategy({"response": strategy.response})
        else:
            formatted_strategy = format_strategy({"response": str(strategy)})
        
        return StopEvent(result={"strategy": formatted_strategy})

    async def run_from_profile(self, profile_data):
        """Alternative entry point when you already have structured profile data"""
        try:
            # Start from profile_demographics step
            result = await super().run(ProfileDemographicsEvent(profile=profile_data))
            return result
        except Exception as e:
            return {"strategy": f"Error in workflow: {str(e)}"}

    async def run_from_text(self, user_input):
        """Standard entry point from text input"""
        try:
            # Start from analyze_input step
            result = await super().run(AnalyzeInputEvent(user_input=user_input))
            return result
        except Exception as e:
            return {"strategy": f"Error in workflow: {str(e)}"}

    # async def run(self, user_input: str):
    #     # Start the workflow with the AnalyzeInputEvent
    #     result = await self.start(AnalyzeInputEvent(user_input=user_input))
    #     return result
# import os
# from crew import InvestmentCrew

# if __name__ == "__main__":
#     os.environ["TRADINGECONOMICS_API_KEY"] = "your-te-key"
#     os.environ["NEBIUS_API_KEY"] = "your-nebius-key"

#     user_input = """
#     I'm in my 30s, earn $6000/month, spend $4000/month, have moderate risk tolerance,
#     and want to buy a house in 5 years.
#     """

#     investment_crew = InvestmentCrew(user_input)
#     result = investment_crew.run()

#     print("\n📈 Final Investment Strategy:\n")
#     print(result)