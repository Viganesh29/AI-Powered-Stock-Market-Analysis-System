from dotenv import load_dotenv
load_dotenv()

print(">>> main.py started")

from crewai import Agent, Task, Crew, Process
from tools.yahoo_tool import fetch_financial_data

# ---------------- FETCH DATA (PURE PYTHON) ---------------- #
financial_data = fetch_financial_data("AAPL")

# ---------------- AGENT ---------------- #
analysis_agent = Agent(
    role="Financial Analyst",
    goal="Analyze financial data and explain company health clearly",
    backstory=(
        "You are a careful financial analyst. "
        "You ONLY analyze the data provided to you. "
        "You never invent or estimate numbers."
    ),
    verbose=True
)

# ---------------- TASK ---------------- #
analysis_task = Task(
    description=(
        "Analyze the following financial data:\n\n"
        f"{financial_data}\n\n"
        "Explain clearly:\n"
        "1. Revenue and profit trend\n"
        "2. Debt position\n"
        "3. Cash flow health\n"
        "4. Overall financial strength\n"
    ),
    expected_output="Clear, beginner-friendly financial analysis report",
    agent=analysis_agent
)

# ---------------- CREW ---------------- #
crew = Crew(
    agents=[analysis_agent],
    tasks=[analysis_task],
    process=Process.sequential,
    memory=False,   # REQUIRED for Ollama
    verbose=True
)

# ---------------- RUN ---------------- #
result = crew.kickoff()

print("\n===== FINAL OUTPUT =====\n")
print(result)
