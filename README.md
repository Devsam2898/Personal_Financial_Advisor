# 📈 Vittaśāstra - AI Strategist Enhanced

### 🚀 Agentic Demo Showcase – Track 3 Entry  
**Hugging Face Gradio Hackathon 2025**

---

## 🧠 Built by: [Devavrat Samak]  
> Tech Stack: `LlamaIndex` | `meta-llama/Meta-Llama-3.1-70B-Instruct-fast (Nebius)` | `Modal Labs` | `Gradio`  
> Data Sources: `World Bank API`, `Yahoo Finance`

---

## 🎯 Track
This submission is for **Track 3: Agentic Demo Showcase**  
> `#agent-demo-track`

We’ve developed a **multi-agent AI financial advisor** that:
- Analyzes a user's financial profile
- Enriches it with demographic insights
- Retrieves real-time macroeconomic indicators
- Crafts a personalized investment strategy

---

## 🔍 Project Overview

This AI-powered platform generates intelligent and tax-aware investment strategies using your:
- Age group
- Monthly income & expenses
- Risk profile
- Financial goals
- Country of residence
- Investment timeframe

### 💡 Key Highlights
| Module | Description |
|--------|-------------|
| 👤 **User Profile** | Age, income, expenses, goals, risk, timeframe |
| 📊 **Demographic Mapping** | Life stage, planning horizon |
| 🌍 **Economic Context** | Inflation, GDP growth, interest rates, market sentiment |
| 🏦 **Country-Specific Tax Rules** | Supports India, USA, UK, Canada, Germany, France, Italy, Japan |
| 💼 **Strategy Generator** | Asset allocation, instruments, monthly plan |

---

## 🛠️ Agentic Framework

### 🧩 Agent Roles
| Agent | Description |
|-------|-------------|
| `Input Analyzer` | Parses user input into structured profile |
| `Demographic Profiler` | Identifies stage of life and liquidity needs |
| `Net Worth Checker` | Checks asset status (placeholder logic) |
| `Financial Literacy Detector` | Adjusts output complexity |
| `Economic Analyst` | Pulls inflation, GDP, interest rate, market trend |
| `Strategy Advisor` | Crafts personalized investment strategy |

---

## ⚙️ Technical Architecture

| Component | Role |
|----------|------|
| `LlamaIndex` | Multi-agent orchestration |
| `Nebius AI` | Hosts Meta-Llama-3.1-70B-Instruct-fast |
| `Modal Labs` | Backend ASGI deployment |
| `World Bank & Yahoo Finance` | Economic indicators |
| `Gradio` | Frontend UX (via Hugging Face Spaces) |

---

## ✨ Features

| Feature | Status |
|--------|--------|
| ✅ Multi-Agent Orchestration | LlamaIndex-powered |
| ✅ Risk Profile Support | Conservative, Moderate, Aggressive |
| ✅ Real-Time Economic Data | Inflation, Interest, GDP, Market |
| ✅ Country-Aware Tax Rules | India + G7 Countries |
| ✅ Markdown Output | Readable, well-structured strategy |
| ✅ Cold Start Handling | Modal + Gradio timeout logic |
| ✅ Service Status Check | Health and test endpoints |

---

## 📹 Demo Video

> 🎬 [https://youtu.be/_y4ShsIBVMQ]

**Suggested flow for video:**
1. Quick introduction to the idea
2. Step-by-step agent workflow
3. Show real-time API fetch (World Bank/Yahoo)
4. Demo the Gradio UI
5. Highlight architecture and model (Nebius + Modal)

---

## 🧑‍💻 Getting Started

### 🚀 Run Locally

```bash
git clone https://github.com/your-username/finance-strategist-agentic.git
cd finance-strategist-agentic
pip install -r requirements.txt
python app.py
