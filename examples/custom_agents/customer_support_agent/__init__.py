"""Customer Support Agent Package."""

from .agent import CustomerSupportAgent

__all__ = ["CustomerSupportAgent"]

default_agent = CustomerSupportAgent()
