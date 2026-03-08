"""Email Management Agent Configuration"""

from datetime import timedelta
from pathlib import Path
from typing import Optional

from framework.config import AgentMetadata, LLMConfig, RuntimeConfig


def get_agent_metadata() -> AgentMetadata:
    """Get agent metadata for display in TUI."""
    return AgentMetadata(
        name="Email Management Agent",
        description="Intelligent email inbox management with natural language rules",
        version="1.0.0",
        intro_message="📧 Welcome to Email Management Agent!\n\nI can help you automatically organize your Gmail inbox using natural language rules. Just tell me what you want done with different types of emails, and I'll handle the rest.\n\nExamples:\n- 'Move all newsletters to the Promotions tab'\n- 'Star emails from my boss'\n- 'Archive emails older than 30 days'\n- 'Mark spam emails as spam and trash them'\n\nLet's get started!",
    )


def get_llm_config() -> LLMConfig:
    """Get LLM configuration for the agent."""
    return LLMConfig(
        model="gpt-4o-mini",
        max_tokens=4000,
        temperature=0.1,
        timeout=timedelta(minutes=5),
    )


def get_runtime_config() -> RuntimeConfig:
    """Get runtime configuration for the agent."""
    return RuntimeConfig(
        storage_path=Path.home() / ".hive" / "agents" / "email_management_agent",
        max_iterations=50,
        conversation_mode="continuous",
    )
