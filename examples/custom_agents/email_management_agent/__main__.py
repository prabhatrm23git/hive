"""Email Management Agent CLI Interface."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .agent import EmailManagementAgent


def cli():
    """Command-line interface for the Email Management Agent."""
    parser = argparse.ArgumentParser(
        description="Email Management Agent - Intelligent inbox organization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m email_management_agent run --rules "Archive newsletters" --max-emails 50
  python -m email_management_agent validate
  python -m email_management_agent info
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the email management agent")
    run_parser.add_argument(
        "--rules",
        type=str,
        required=True,
        help="Email management rules in natural language",
    )
    run_parser.add_argument(
        "--max-emails",
        type=int,
        default=100,
        help="Maximum number of emails to process (default: 100)",
    )
    run_parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock mode without real API calls",
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
    
    agent = EmailManagementAgent()
    
    if args.command == "run":
        asyncio.run(run_agent(agent, args))
    elif args.command == "validate":
        validate_agent(agent)
    elif args.command == "info":
        show_info(agent)
    elif args.command == "shell":
        asyncio.run(start_shell(agent, args))


async def run_agent(agent: EmailManagementAgent, args):
    """Run the email management agent."""
    input_data = {
        "rules": args.rules,
        "max_emails": args.max_emails,
    }
    
    print("🚀 Starting Email Management Agent...")
    print(f"📋 Rules: {args.rules}")
    print(f"📧 Max emails: {args.max_emails}")
    print()
    
    if args.mock:
        print("⚠️  Running in mock mode - no real API calls will be made")
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


def validate_agent(agent: EmailManagementAgent):
    """Validate agent configuration."""
    print("🔍 Validating Email Management Agent...")
    
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


def show_info(agent: EmailManagementAgent):
    """Show agent information."""
    print("📧 Email Management Agent")
    print("=" * 50)
    print(f"Version: 1.0.0")
    print(f"Description: {agent.goal.description}")
    print()
    print("Capabilities:")
    print("• Fetch emails from Gmail inbox")
    print("• Apply natural language rules for classification")
    print("• Execute actions: archive, star, spam, trash, etc.")
    print("• Generate comprehensive reports")
    print()
    print("Requirements:")
    print("• Gmail API access")
    print("• Appropriate Gmail permissions")
    print()
    print("Usage:")
    print("  python -m email_management_agent run --rules 'your rules' --max-emails 100")


async def start_shell(agent: EmailManagementAgent, args):
    """Start interactive shell."""
    print("🐚 Email Management Agent Shell")
    print("Type 'help' for available commands or 'exit' to quit")
    print()
    
    if args.mock:
        print("⚠️  Running in mock mode")
    
    while True:
        try:
            command = input("email-agent> ").strip()
            
            if command.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            elif command.lower() == "help":
                print("Available commands:")
                print("  help     - Show this help")
                print("  info     - Show agent info")
                print("  exit     - Exit shell")
            elif command.lower() == "info":
                show_info(agent)
            elif command:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    cli()
