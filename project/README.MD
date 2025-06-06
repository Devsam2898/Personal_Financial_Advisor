# 📈 Personal Finance Investment Strategist
## Agentic Demo Showcase – Track 3 Entry

> **Agent-Based Financial Advisor Using LlamaIndex, Nebius AI, and Economic Data**

Built by: **[Devavrat Samak]**  
Tech Stack: LlamaIndex | meta-llama/Meta-Llama-3.1-70B-Instruct-fast (Nebius) | Modal Labs | Gradio | World Bank & Yahoo Finance APIs

---

## Hackathon Track

This submission is for:
**Track 3: Agentic Demo Showcase**
# agent-demo-track
We use a multi-agent system to:
1. Analyze user financial profile
2. Enrich with demographic insights
3. Fetch live economic indicators
4. Generate personalized investment strategy

---

## 🔍 Overview

This agentic system provides intelligent, context-aware investment strategies based on:

| Feature | Description |
|--------|-------------|
| User Profile | Age group, income, expenses, risk tolerance, goal, timeframe |
| Demographic Insights | Life stage, liquidity needs, planning horizon |
| Economic Analysis | Inflation, interest rates, GDP growth, market trends |
| Tax Awareness | Country-specific tax rules from India and G7 countries, i.e. USA, UK, Canada, Germany, France, Italy, Japan |
| Strategy Generation | Asset allocation, recommended instruments, monthly savings plan |

---

## How It Works: The Agentic Framework

### Agent Flow

Each agent uses natural language reasoning and external tools to build the final strategy.

### Agents

| Agent | Role |
|-------|------|
| **Input Analyzer** | Parses free-form input into structured profile |
| **Demographic Profiler** | Maps life stage, liquidity needs, planning horizon |
| **Net Worth Checker** | Identifies existing investments and assets |
| **Financial Literacy Detector** | Determines complexity level of advice |
| **Economic Analyst** | Gathers inflation, interest rate, GDP, and market trend |
| **Strategy Advisor** | Generates final investment plan |

---

## Technical Architecture

### Core Components

| Component | Purpose |
|----------|----------|
| LlamaIndex | Manages agent orchestration and reasoning flow |
| Qwen3-32B on Nebius | Generates human-readable investment strategy |
| World Bank API | Provides inflation and GDP data |
| Yahoo Finance | Detects market trend (bullish/bearish) |
| Hardcoded Interest Rates | For major countries (USA, India, UK, etc.) |
| Country Tax DB | Applies local tax logic to optimize portfolio |
| Modal Labs | Hosts backend as ASGI endpoint |
| Gradio | Frontend interface on Hugging Face Spaces |

---

## Features

| Feature | Status |
|--------|--------|
| ✅ Multi-Agent Workflow | LlamaIndex-based |
| ✅ Country Support | India, USA, UK, Canada, Germany, France, Italy, Japan |
| ✅ Economic Indicators | Inflation, Interest Rate, GDP Growth, Market Trend |
| ✅ Tax-Aware Advice | Yes – country-specific |
| ✅ Risk Tolerance Mapping | Conservative / Moderate / Aggressive |
| ✅ Markdown Strategy Output | Clean, formatted response |
---

## 📹 Video Walkthrough

🎬 [Insert your video link here explaining how the agents work together]

Example structure:
1. Introduction to the app
2. Walk through the agent flow
3. Show tool usage (World Bank, Yahoo Finance)
4. Demonstrate strategy generation
5. Explain tech stack (LlamaIndex + Nebius)

---
- Credits
- Built with ❤️ by [Devavrat Samak]
- For Hugging Face Gradio Hackathon 2025 – Track 3: Agentic Demo Showcase

- GitHub Repo: [link-to-your-repo]   # Will paste it later on!
- Model: meta-llama/Meta-Llama-3.1-70B-Instruct-fast (Nebius AI)
- Backend: Modal Labs
- Frontend: Hugging Face Gradio

Thank You!
If you're reading this — thank you for checking out our project. We hope you found it insightful and well-built.

