#Gradio app
# app.py
# app.py - Original approach with profile object
import gradio as gr
import requests

MODAL_URL = "https://devsam2898--personal-investment-strategist-9-web.modal.run/strategy"

def get_investment_strategy(age_group, income, expenses, risk_profile, goal, timeframe):
    """Get investment strategy from Modal backend"""
    payload = {
        "profile": {
            "age_group": age_group,
            "income": income,
            "expenses": expenses,
            "risk_profile": risk_profile,
            "goal": goal,
            "timeframe": timeframe
        }
    }
    try:
        response = requests.post(MODAL_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("strategy", "No strategy returned.")
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ Network error: {str(e)}"

demo = gr.Interface(
    fn=get_investment_strategy,
    inputs=[
        gr.Dropdown(["20s", "30s", "40s", "50s+"], label="Age Group", value="30s"),
        gr.Textbox(label="Monthly Income ($)", value="6000"),
        gr.Textbox(label="Monthly Expenses ($)", value="4000"),
        gr.Radio(["Conservative", "Moderate", "Aggressive"], label="Risk Tolerance", value="Moderate"),
        gr.Textbox(label="Financial Goal (e.g., buy a house)", value="retirement planning"),
        gr.Textbox(label="Timeframe (e.g., 5 years)", value="10 years")
    ],
    outputs=gr.Markdown(label="Investment Strategy"),
    title="📈 Personal Finance Strategist",
    description="Powered by LlamaIndex + Nebius Qwen3 | Get personalized strategies based on life stage and goals.",
    theme="soft",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()






# # app.py

# import gradio as gr
# import requests

# MODAL_URL = "https://devsam2898--personal-investment-strategist-8-web.modal.run/strategy" 

# def get_investment_strategy(age_group, income, expenses, risk_profile, goal, timeframe):
#     payload = {
#         "profile": {
#             "age_group": age_group,
#             "income": income,
#             "expenses": expenses,
#             "risk_profile": risk_profile,
#             "goal": goal,
#             "timeframe": timeframe
#         }
#     }
#     try:
#         response = requests.post(MODAL_URL, json=payload)
#         if response.status_code == 200:
#             return response.json().get("strategy", "No strategy returned.")
#         else:
#             return f"Error {response.status_code}: {response.text}"
#     except Exception as e:
#         return f"Network error: {str(e)}"

# interface = gr.Interface(
#     fn=get_investment_strategy,
#     inputs=[
#         gr.Dropdown(["20s", "30s", "40s", "50s+"], label="Age Group"),
#         gr.Textbox(label="Monthly Income ($)", value="6000"),
#         gr.Textbox(label="Monthly Expenses ($)", value="4000"),
#         gr.Radio(["Conservative", "Moderate", "Aggressive"], label="Risk Tolerance"),
#         gr.Textbox(label="Financial Goal (e.g., buy a house)"),
#         gr.Textbox(label="Timeframe (e.g., 5 years)")
#     ],
#     outputs=gr.Markdown(label="Investment Strategy"),
#     title="📈 Personal Finance Strategist",
#     description="Powered by LlamaIndex + Nebius Qwen3 | Get personalized strategies based on life stage and goals.",
#     theme="soft",
#     allow_flagging="never"
# )

# if __name__ == "__main__":
#     interface.launch()


# import gradio as gr
# from crew import InvestmentCrew

# def run_crew(age_group, income, expenses, risk_profile, goal, timeframe):
#     user_input = f"""
#     I'm in my {age_group}, earn ${income}/month, spend ${expenses}/month,
#     have {risk_profile} risk tolerance, and want to {goal} in {timeframe}.
#     """
    
#     investment_crew = InvestmentCrew(user_input)
#     result = investment_crew.run()
    
#     return result.final_output
# # For the personalized investment strategy, we will think on some web api or some external information.
# title = "📈 Personal Finance Investment Strategist"
# description = "Get personalized investment strategies based on your life stage, goals, and current economic conditions."
# examples = [
#     ["30s", "6000", "4000", "moderate", "buy a house", "5 years"],
#     ["20s", "3000", "2500", "aggressive", "retire early", "10 years"]
# ]

# interface = gr.Interface(
#     fn=run_crew,
#     inputs=[
#         gr.Dropdown(["20s", "30s", "40s", "50s+"], label="Age Group"),
#         gr.Textbox(label="Monthly Income ($)", value="6000"),
#         gr.Textbox(label="Monthly Expenses ($)", value="4000"),
#         gr.Radio(["Conservative", "Moderate", "Aggressive"], label="Risk Tolerance"),
#         gr.Textbox(label="Financial Goal (e.g., buy a house)"),
#         gr.Textbox(label="Timeframe (e.g., 5 years)")
#     ],
#     outputs=gr.Markdown(label="Investment Strategy"),
#     title=title,
#     description=description,
#     examples=examples,
#     theme="soft",
#     allow_flagging="never"
# )

# if __name__ == "__main__":
#     interface.launch()