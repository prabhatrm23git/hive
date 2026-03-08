"""Business Insights Agent CLI Interface."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .agent import BusinessInsightsAgent


def cli():
    """Command-line interface for the Business Insights Agent."""
    parser = argparse.ArgumentParser(
        description="Business Insights Agent - AI-powered data analysis and strategic recommendations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m business_insights_agent run --question "What drives customer churn?" --data sales.csv,customers.csv
  python -m business_insights_agent validate
  python -m business_insights_agent info
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the business insights analysis")
    run_parser.add_argument(
        "--question",
        type=str,
        required=True,
        help="Business question or objective to analyze",
    )
    run_parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Comma-separated list of data files or sources",
    )
    run_parser.add_argument(
        "--goals",
        type=str,
        help="Specific analysis goals or hypotheses",
    )
    run_parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock mode without real data processing",
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
    
    agent = BusinessInsightsAgent()
    
    if args.command == "run":
        asyncio.run(run_agent(agent, args))
    elif args.command == "validate":
        validate_agent(agent)
    elif args.command == "info":
        show_info(agent)
    elif args.command == "shell":
        asyncio.run(start_shell(agent, args))


async def run_agent(agent: BusinessInsightsAgent, args):
    """Run the business insights agent."""
    input_data = {
        "business_question": args.question,
        "data_sources": args.data.split(","),
        "analysis_goals": args.goals or "Generate actionable business insights",
    }
    
    print("🚀 Starting Business Insights Agent...")
    print(f"📊 Question: {args.question}")
    print(f"📁 Data sources: {args.data}")
    if args.goals:
        print(f"🎯 Goals: {args.goals}")
    print()
    
    if args.mock:
        print("⚠️  Running in mock mode - no real data processing will be done")
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


def validate_agent(agent: BusinessInsightsAgent):
    """Validate agent configuration."""
    print("🔍 Validating Business Insights Agent...")
    
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


def show_info(agent: BusinessInsightsAgent):
    """Show agent information."""
    print("📊 Business Insights Agent")
    print("=" * 50)
    print(f"Version: 1.0.0")
    print(f"Description: {agent.goal.description}")
    print()
    print("Capabilities:")
    print("• Analyze structured data (CSV, JSON, Excel)")
    print("• Generate statistical insights and trends")
    print("• Build predictive models and forecasts")
    print("• Create visualizations and dashboards")
    print("• Provide strategic business recommendations")
    print()
    print("Analysis Process:")
    print("1. Discovery and scoping")
    print("2. Data ingestion and preparation")
    print("3. Exploratory data analysis")
    print("4. Confirmatory statistical analysis")
    print("5. Insight synthesis and recommendations")
    print("6. Results presentation and review")
    print()
    print("Usage:")
    print("  python -m business_insights_agent run --question 'your question' --data file1.csv,file2.csv")


async def start_shell(agent: BusinessInsightsAgent, args):
    """Start interactive shell."""
    print("🐚 Business Insights Agent Shell")
    print("Type 'help' for available commands or 'exit' to quit")
    print()
    
    if args.mock:
        print("⚠️  Running in mock mode")
    
    while True:
        try:
            command = input("insights-agent> ").strip()
            
            if command.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            elif command.lower() == "help":
                print("Available commands:")
                print("  help     - Show this help")
                print("  info     - Show agent info")
                print("  examples - Show analysis examples")
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
    """Show example analysis scenarios."""
    print("📊 Example Analysis Scenarios:")
    print()
    print("1. Customer Churn Analysis")
    print("   Question: 'What factors predict customer churn?'")
    print("   Data: customer_demographics.csv, usage_data.csv, support_tickets.csv")
    print()
    print("2. Sales Performance Analysis")
    print("   Question: 'What drives sales performance across regions?'")
    print("   Data: sales_data.csv, regional_metrics.csv, marketing_spend.csv")
    print()
    print("3. Operational Efficiency")
    print("   Question: 'How can we improve operational efficiency?'")
    print("   Data: process_times.csv, resource_allocation.csv, quality_metrics.csv")
    print()
    print("4. Market Basket Analysis")
    print("   Question: 'What products are frequently purchased together?'")
    print("   Data: transactions.csv, product_catalog.csv, customer_segments.csv")
    print()


if __name__ == "__main__":
    cli()
