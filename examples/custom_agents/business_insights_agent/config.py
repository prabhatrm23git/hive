"""Business Insights Agent Configuration"""

from datetime import timedelta
from pathlib import Path
from typing import Optional

from framework.config import AgentMetadata, LLMConfig, RuntimeConfig


def get_agent_metadata() -> AgentMetadata:
    """Get agent metadata for display in TUI."""
    return AgentMetadata(
        name="Business Insights Agent",
        description="AI-powered data analysis and business intelligence generator",
        version="1.0.0",
        intro_message="📊 Welcome to Business Insights Agent!\n\nI can help you analyze data and generate actionable business insights. Whether you have sales data, customer metrics, or operational KPIs, I'll turn your raw data into strategic recommendations.\n\nWhat I can do:\n• Analyze structured data (CSV, JSON, Excel)\n• Generate trend analysis and forecasts\n• Create visualizations and dashboards\n• Identify key performance indicators\n• Provide strategic recommendations\n\nLet's start by understanding your data and analysis goals!",
    )


def get_llm_config() -> LLMConfig:
    """Get LLM configuration for the agent."""
    return LLMConfig(
        model="gpt-4o",
        max_tokens=8000,
        temperature=0.2,
        timeout=timedelta(minutes=10),
    )


def get_runtime_config() -> RuntimeConfig:
    """Get runtime configuration for the agent."""
    return RuntimeConfig(
        storage_path=Path.home() / ".hive" / "agents" / "business_insights_agent",
        max_iterations=30,
        conversation_mode="continuous",
    )
