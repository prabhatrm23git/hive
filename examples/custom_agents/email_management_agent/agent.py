"""
Email Management Agent

An intelligent email inbox management system that processes Gmail emails
using natural language rules provided by the user.
"""

from pathlib import Path
from typing import Any, Dict, List

from framework.agent import Agent
from framework.config import GraphSpec
from framework.goal import Goal, SuccessCriteria, Constraint
from framework.graph import Edge, Graph
from framework.llm import LLMConfig
from framework.node import NodeSpec
from framework.runtime import RuntimeConfig


class EmailManagementAgent(Agent):
    """Email Management Agent for intelligent inbox organization."""

    def __init__(self):
        """Initialize the Email Management Agent."""
        super().__init__(
            goal=self._get_goal(),
            graph=self._get_graph(),
            config=self._get_config(),
        )

    def _get_goal(self) -> Goal:
        """Define the agent's goal."""
        return Goal(
            id="email-management",
            name="Email Inbox Management",
            description="Automatically manage Gmail inbox emails using user-defined natural language rules",
            success_criteria=[
                SuccessCriteria(
                    id="classification_accuracy",
                    description="Each email is classified according to user's rules with high accuracy",
                    metric="classification_match_rate",
                    target=0.90,
                    weight=0.3,
                ),
                SuccessCriteria(
                    id="action_correctness",
                    description="Email actions (trash, spam, archive, star, etc.) are applied correctly",
                    metric="action_correctness",
                    target=0.95,
                    weight=0.25,
                ),
                SuccessCriteria(
                    id="inbox_scope",
                    description="Only inbox emails are processed and acted upon",
                    metric="inbox_scope_accuracy",
                    target=1.0,
                    weight=0.2,
                ),
                SuccessCriteria(
                    id="comprehensive_processing",
                    description="All fetched emails up to max limit are processed",
                    metric="emails_processed_ratio",
                    target=1.0,
                    weight=0.15,
                ),
                SuccessCriteria(
                    id="report_completeness",
                    description="Generate comprehensive summary report of actions taken",
                    metric="report_completeness",
                    target=1.0,
                    weight=0.1,
                ),
            ],
            constraints=[
                Constraint(
                    id="inbox_only",
                    description="Must only fetch and process emails from INBOX label",
                    constraint_type="hard",
                    category="safety",
                ),
                Constraint(
                    id="max_emails_limit",
                    description="Must not process more emails than configured max_emails parameter",
                    constraint_type="hard",
                    category="operational",
                ),
                Constraint(
                    id="valid_labels",
                    description="Must only use valid Gmail system labels, not custom labels",
                    constraint_type="hard",
                    category="operational",
                ),
                Constraint(
                    id="spam_preservation",
                    description="Marking as spam moves to spam folder but preserves email; only explicit trash rules delete",
                    constraint_type="hard",
                    category="safety",
                ),
            ],
        )

    def _get_graph(self) -> Graph:
        """Define the agent's workflow graph."""
        nodes = [
            NodeSpec(
                id="intake",
                name="Intake and Configuration",
                description="Gather email management rules and configuration from user",
                node_type="event_loop",
                input_keys=["rules", "max_emails"],
                output_keys=["validated_rules", "max_emails"],
                tools=[],
                system_prompt="""You are an email management intake specialist.

Your role is to:
1. Receive and understand the user's email management rules
2. Clarify any ambiguous instructions
3. Confirm the maximum number of emails to process
4. Present the interpreted rules back for user confirmation

**STEP 1 — Respond to the user (text only, NO tool calls):**
- Ask about their email management preferences
- Understand what types of emails they want to process
- Clarify actions for different email categories
- Confirm the maximum number of emails to process

**STEP 2 — After the user responds, call set_output:**
- set_output("validated_rules", "The user's confirmed email management rules")
- set_output("max_emails", "The maximum number of emails to process")

Common email categories to consider:
- Newsletters and marketing emails
- Work-related emails
- Personal emails
- Spam and promotional content
- Emails requiring action
- Archived or old emails

Available Gmail actions:
- Archive (remove from inbox)
- Star (mark as important)
- Mark as read/unread
- Move to spam
- Trash (permanently delete)
- Apply labels (using Gmail system labels only)""",
                client_facing=True,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="fetch_emails",
                name="Fetch Emails",
                description="Fetch emails from Gmail inbox according to configuration",
                node_type="event_loop",
                input_keys=["validated_rules", "max_emails"],
                output_keys=["emails", "fetch_summary"],
                tools=["gmail_list_messages", "gmail_get_message"],
                system_prompt="""You are an email fetching specialist.

Your role is to:
1. Fetch emails from the Gmail INBOX only
2. Process in batches to handle large numbers efficiently
3. Respect the max_emails limit
4. Extract key information from each email

Use these tools:
- gmail_list_messages: to list messages from INBOX
- gmail_get_message: to get full message details

**Process:**
1. Use gmail_list_messages with label:INBOX and maxResults
2. For each message, use gmail_get_message to get full details
3. Extract: subject, from, to, date, snippet, body, labels
4. Store emails in a structured format

**Output format:**
Use set_output("emails", JSON string of email array)
Use set_output("fetch_summary", "Summary of what was fetched")

Each email should include:
- id, threadId, subject, from, to, date, snippet, body, labels
- Keep only essential fields to stay within token limits

**Important:**
- Only fetch from INBOX label
- Respect the max_emails limit strictly
- Handle pagination if needed""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="classify_and_act",
                name="Classify and Act",
                description="Apply user rules to classify emails and take appropriate actions",
                node_type="event_loop",
                input_keys=["emails", "validated_rules"],
                output_keys=["actions_taken", "processing_summary"],
                tools=[
                    "gmail_batch_modify_messages",
                    "gmail_modify_message",
                    "gmail_trash_message",
                ],
                system_prompt="""You are an email classification and action specialist.

Your role is to:
1. Analyze each email against the user's rules
2. Determine the appropriate action for each email
3. Execute the actions using Gmail tools
4. Track all actions taken

**Available Tools:**
- gmail_batch_modify_messages: for bulk operations
- gmail_modify_message: for single email operations
- gmail_trash_message: to delete emails

**Process:**
1. Read the validated_rules and emails
2. For each email, determine which rule applies
3. Execute the appropriate action:
   - Archive: remove label:INBOX
   - Star: add label:STARRED
   - Mark as read: remove label:UNREAD
   - Mark as spam: add label:SPAM
   - Trash: use gmail_trash_message
4. Batch similar actions when possible

**Classification Logic:**
Consider email content, sender, subject, and patterns
Apply rules in priority order if multiple match
Be conservative with destructive actions (trash, spam)

**Output:**
Use set_output("actions_taken", JSON string of actions array)
Use set_output("processing_summary", "Summary of all actions taken")

Track:
- Email ID and action taken
- Success/failure of each action
- Reason for classification""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="report",
                name="Generate Report",
                description="Generate comprehensive summary report of email processing",
                node_type="event_loop",
                input_keys=["actions_taken", "processing_summary", "fetch_summary"],
                output_keys=["final_report"],
                tools=[],
                system_prompt="""You are an email management report specialist.

Your role is to:
1. Analyze all actions taken during email processing
2. Generate a comprehensive summary report
3. Present results in a clear, organized format

**Report Sections:**
1. **Processing Summary**
   - Total emails processed
   - Actions taken by category
   - Success/failure rates

2. **Actions Breakdown**
   - Emails archived: count and examples
   - Emails starred: count and examples
   - Emails marked as spam: count and examples
   - Emails trashed: count and examples
   - Other actions: count and details

3. **Rule Effectiveness**
   - How well rules matched emails
   - Any ambiguous cases
   - Suggestions for rule improvements

4. **Recommendations**
   - Optimize rules for better classification
   - Handle edge cases
   - Suggest additional rules

**Format:**
Use clear headings, bullet points, and examples
Include email subjects for context
Provide actionable insights

Use set_output("final_report", "The complete report as a formatted string")""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
        ]

        edges = [
            Edge(
                id="intake-to-fetch",
                source="intake",
                target="fetch_emails",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="fetch-to-classify",
                source="fetch_emails",
                target="classify_and_act",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="classify-to-report",
                source="classify_and_act",
                target="report",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
        ]

        return Graph(
            id="email-management-graph",
            nodes=nodes,
            edges=edges,
            entry_points={"start": "intake"},
            terminal_nodes=["report"],
        )

    def _get_config(self) -> Dict[str, Any]:
        """Get agent configuration."""
        return {
            "llm": LLMConfig(
                model="gpt-4o-mini",
                max_tokens=4000,
                temperature=0.1,
            ),
            "runtime": RuntimeConfig(
                storage_path=Path.home() / ".hive" / "agents" / "email_management_agent",
                max_iterations=50,
                conversation_mode="continuous",
            ),
        }
