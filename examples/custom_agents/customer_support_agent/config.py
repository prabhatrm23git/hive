"""Customer Support Agent Configuration"""

from datetime import timedelta
from pathlib import Path
from typing import Optional

from framework.config import AgentMetadata, LLMConfig, RuntimeConfig


def get_agent_metadata() -> AgentMetadata:
    """Get agent metadata for display in TUI."""
    return AgentMetadata(
        name="Customer Support Agent",
        description="Intelligent customer support automation with ticket triage and response generation",
        version="1.0.0",
        intro_message="🎧 Welcome to Customer Support Agent!\n\nI can help automate your customer support workflow by intelligently triaging tickets, generating responses, and escalating complex issues. I handle common inquiries automatically and ensure urgent issues get immediate attention.\n\nWhat I can do:\n• Automatically categorize and prioritize support tickets\n• Generate personalized responses to common inquiries\n• Detect urgent issues and escalate appropriately\n• Learn from feedback to improve over time\n• Integrate with your existing support systems\n\nLet's set up your support automation workflow!",
    )


def get_llm_config() -> LLMConfig:
    """Get LLM configuration for the agent."""
    return LLMConfig(
        model="gpt-4o",
        max_tokens=4000,
        temperature=0.3,
        timeout=timedelta(minutes=3),
    )


def get_runtime_config() -> RuntimeConfig:
    """Get runtime configuration for the agent."""
    return RuntimeConfig(
        storage_path=Path.home() / ".hive" / "agents" / "customer_support_agent",
        max_iterations=100,
        conversation_mode="continuous",
    )
