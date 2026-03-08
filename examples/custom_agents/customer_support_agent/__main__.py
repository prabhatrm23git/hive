"""Customer Support Agent CLI Interface."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .agent import CustomerSupportAgent


def cli():
    """Command-line interface for the Customer Support Agent."""
    parser = argparse.ArgumentParser(
        description="Customer Support Agent - Intelligent ticket triage and response automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m customer_support_agent run --ticket "Login issue with account" --customer "john@example.com" --priority "high"
  python -m customer_support_agent validate
  python -m customer_support_agent info
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the customer support agent")
    run_parser.add_argument(
        "--ticket",
        type=str,
        required=True,
        help="Customer support ticket content or issue description",
    )
    run_parser.add_argument(
        "--customer",
        type=str,
        required=True,
        help="Customer identifier (email, customer ID, etc.)",
    )
    run_parser.add_argument(
        "--priority",
        type=str,
        choices=["critical", "high", "medium", "low"],
        default="medium",
        help="Initial priority assessment (default: medium)",
    )
    run_parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock mode without real integration",
    )
    
    # Validate command
    subparsers.add_parser("validate", help="Validate agent configuration")
    
    # Info command
    subparsers.add_parser("info", help="Show agent information")
    
    # Shell command
    shell_parser = subparsers.add_parser("shell", help="Start interactive shell")
    shell_parser.add_argument(
        "--mock",
        action="store_true",
        help="Start shell in mock mode",
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    agent = CustomerSupportAgent()
    
    if args.command == "run":
        asyncio.run(run_agent(agent, args))
    elif args.command == "validate":
        validate_agent(agent)
    elif args.command == "info":
        show_info(agent)
    elif args.command == "shell":
        asyncio.run(start_shell(agent, args))


async def run_agent(agent: CustomerSupportAgent, args):
    """Run the customer support agent."""
    input_data = {
        "ticket_content": args.ticket,
        "customer_info": args.customer,
        "priority_indicators": args.priority,
    }
    
    print("🎧 Starting Customer Support Agent...")
    print(f"📝 Ticket: {args.ticket}")
    print(f"👤 Customer: {args.customer}")
    print(f"🔥 Priority: {args.priority}")
    print()
    
    if args.mock:
        print("⚠️  Running in mock mode - no real integrations will be used")
        # TODO: Implement mock execution
        print("Mock execution not yet implemented")
        return
    
    try:
        # TODO: Implement actual agent execution
        print("Agent execution not yet implemented - need to integrate with framework")
        print("Input data:", json.dumps(input_data, indent=2))
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        sys.exit(1)


def validate_agent(agent: CustomerSupportAgent):
    """Validate agent configuration."""
    print("🔍 Validating Customer Support Agent...")
    
    try:
        # Validate goal
        goal = agent.goal
        print(f"✅ Goal: {goal.name}")
        print(f"   Description: {goal.description}")
        print(f"   Success criteria: {len(goal.success_criteria)}")
        print(f"   Constraints: {len(goal.constraints)}")
        
        # Validate graph
        graph = agent.graph
        print(f"✅ Graph: {graph.id}")
        print(f"   Nodes: {len(graph.nodes)}")
        print(f"   Edges: {len(graph.edges)}")
        print(f"   Entry points: {graph.entry_points}")
        print(f"   Terminal nodes: {graph.terminal_nodes}")
        
        # Validate nodes
        for node in graph.nodes:
            print(f"   ✅ Node: {node.id} ({node.node_type})")
        
        print("\n✅ Agent validation successful!")
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)


def show_info(agent: CustomerSupportAgent):
    """Show agent information."""
    print("🎧 Customer Support Agent")
    print("=" * 50)
    print(f"Version: 1.0.0")
    print(f"Description: {agent.goal.description}")
    print()
    print("Capabilities:")
    print("• Automatic ticket triage and categorization")
    print("• Personalized response generation")
    print("• Urgency detection and escalation")
    print("• Knowledge base integration")
    print("• Quality assurance and validation")
    print("• Multi-channel support delivery")
    print()
    print("Workflow:")
    print("1. Ticket intake and initial analysis")
    print("2. Triage and categorization")
    print("3. Knowledge base solution search")
    print("4. Response generation and personalization")
    print("5. Quality review and delivery")
    print("6. Escalation management for complex issues")
    print()
    print("Usage:")
    print("  python -m customer_support_agent run --ticket 'issue description' --customer customer@example.com")


async def start_shell(agent: CustomerSupportAgent, args):
    """Start interactive shell."""
    print("🐚 Customer Support Agent Shell")
    print("Type 'help' for available commands or 'exit' to quit")
    print()
    
    if args.mock:
        print("⚠️  Running in mock mode")
    
    while True:
        try:
            command = input("support-agent> ").strip()
            
            if command.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            elif command.lower() == "help":
                print("Available commands:")
                print("  help     - Show this help")
                print("  info     - Show agent info")
                print("  examples - Show ticket examples")
                print("  exit     - Exit shell")
            elif command.lower() == "info":
                show_info(agent)
            elif command.lower() == "examples":
                show_examples()
            elif command:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break


def show_examples():
    """Show example ticket scenarios."""
    print("📝 Example Ticket Scenarios:")
    print()
    print("1. Technical Support")
    print("   Ticket: 'I cannot log in to my account, getting error 500'")
    print("   Customer: 'premium_user@company.com'")
    print("   Priority: 'high'")
    print()
    print("2. Billing Issue")
    print("   Ticket: 'Charged twice for monthly subscription'")
    print("   Customer: 'customer123@example.com'")
    print("   Priority: 'medium'")
    print()
    print("3. Product Question")
    print("   Ticket: 'How do I export data from the dashboard?'")
    print("   Customer: 'new_user@example.com'")
    print("   Priority: 'low'")
    print()
    print("4. Critical Outage")
    print("   Ticket: 'Production system down, all users affected'")
    print("   Customer: 'enterprise_client@corp.com'")
    print("   Priority: 'critical'")
    print()


if __name__ == "__main__":
    cli()
