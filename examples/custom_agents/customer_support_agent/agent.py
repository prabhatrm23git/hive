"""
Customer Support Agent

An intelligent customer support automation system that handles ticket triage,
response generation, and escalation for efficient customer service.
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


class CustomerSupportAgent(Agent):
    """Customer Support Agent for intelligent ticket triage and response automation."""

    def __init__(self):
        """Initialize the Customer Support Agent."""
        super().__init__(
            goal=self._get_goal(),
            graph=self._get_graph(),
            config=self._get_config(),
        )

    def _get_goal(self) -> Goal:
        """Define the agent's goal."""
        return Goal(
            id="customer-support",
            name="Customer Support Automation",
            description="Automatically triage support tickets, generate responses, and escalate complex issues",
            success_criteria=[
                SuccessCriteria(
                    id="triage_accuracy",
                    description="Accurately categorize and prioritize incoming support tickets",
                    metric="categorization_accuracy",
                    target=0.90,
                    weight=0.25,
                ),
                SuccessCriteria(
                    id="response_quality",
                    description="Generate helpful, personalized responses to customer inquiries",
                    metric="response_satisfaction_score",
                    target=0.85,
                    weight=0.25,
                ),
                SuccessCriteria(
                    id="urgency_detection",
                    description="Correctly identify and escalate urgent issues",
                    metric="urgency_detection_rate",
                    target=0.95,
                    weight=0.20,
                ),
                SuccessCriteria(
                    id="response_time",
                    description="Provide timely responses within service level agreements",
                    metric="response_time_compliance",
                    target=0.90,
                    weight=0.15,
                ),
                SuccessCriteria(
                    id="escalation_efficiency",
                    description="Efficiently escalate complex issues to appropriate teams",
                    metric="escalation_accuracy",
                    target=0.88,
                    weight=0.15,
                ),
            ],
            constraints=[
                Constraint(
                    id="customer_privacy",
                    description="Must protect customer data and maintain confidentiality",
                    constraint_type="hard",
                    category="safety",
                ),
                Constraint(
                    id="professional_communication",
                    description="Must maintain professional and empathetic communication tone",
                    constraint_type="hard",
                    category="quality",
                ),
                Constraint(
                    id="escalation_thresholds",
                    description="Must follow defined escalation protocols and thresholds",
                    constraint_type="hard",
                    category="operational",
                ),
                Constraint(
                    id="knowledge_base_limits",
                    description="Must not provide information beyond verified knowledge base",
                    constraint_type="soft",
                    category="accuracy",
                ),
            ],
        )

    def _get_graph(self) -> Graph:
        """Define the agent's workflow graph."""
        nodes = [
            NodeSpec(
                id="intake",
                name="Ticket Intake and Initial Analysis",
                description="Receive and analyze incoming support tickets",
                node_type="event_loop",
                input_keys=["ticket_content", "customer_info", "priority_indicators"],
                output_keys=["parsed_ticket", "initial_assessment"],
                tools=[],
                system_prompt="""You are a customer service intake specialist.

Your role is to:
1. Receive and parse incoming support tickets
2. Extract key information and context
3. Perform initial assessment of ticket nature
4. Identify any urgency indicators

**STEP 1 — Respond to the user (text only, NO tool calls):**
- Acknowledge the ticket receipt
- Confirm understanding of the issue
- Ask for any missing critical information
- Set expectations for resolution timeline

**STEP 2 — After user confirmation, call set_output:**
- set_output("parsed_ticket", "Structured ticket information")
- set_output("initial_assessment", "Initial categorization and urgency assessment")

**Information to Extract:**
- Customer details and account status
- Issue description and technical details
- Expected outcomes and urgency
- Previous interactions or history
- Product/service information

**Urgency Indicators:**
- Service outage or production down
- Security or data breach concerns
- Financial impact or revenue loss
- Regulatory compliance issues
- VIP customer escalations

Be thorough but efficient in gathering essential information.""",
                client_facing=True,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="triage",
                name="Ticket Triage and Categorization",
                description="Categorize tickets and determine priority and routing",
                node_type="event_loop",
                input_keys=["parsed_ticket", "initial_assessment"],
                output_keys=["ticket_category", "priority_level", "routing_decision"],
                tools=["knowledge_base_search", "sentiment_analysis", "category_classifier"],
                system_prompt="""You are a ticket triage specialist.

Your role is to:
1. Categorize tickets into appropriate types
2. Assess priority levels based on urgency and impact
3. Determine optimal routing for resolution
4. Identify escalation requirements

**Categories:**
- Technical Issues (bugs, errors, performance)
- Account/Billing (payments, subscriptions, access)
- Product Questions (features, usage, guidance)
- Service Requests (configurations, customizations)
- Complaints/Feedback (dissatisfaction, suggestions)
- Policy/Compliance (terms, regulations, privacy)

**Priority Levels:**
- Critical: Production down, security breach, financial loss
- High: VIP customer, major feature broken, compliance issue
- Medium: Standard issues, normal business impact
- Low: Minor issues, informational requests, general questions

**Routing Logic:**
- Technical → Engineering/Development teams
- Account/Billing → Finance/Account management
- Product Questions → Product/Documentation teams
- Service Requests → Customer success/Implementation
- Complaints → Customer success/Management
- Policy → Legal/Compliance teams

**Tools Usage:**
- Use knowledge_base_search for similar issues
- Use sentiment_analysis to assess customer emotion
- Use category_classifier for automated categorization

**Output:**
Use set_output("ticket_category", "Assigned category")
Use set_output("priority_level", "Priority: Critical/High/Medium/Low")
Use set_output("routing_decision", "Recommended team and escalation path")

Consider customer tier, contract SLAs, and business impact in routing decisions.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="knowledge_check",
                name="Knowledge Base and Solution Search",
                description="Search for existing solutions and knowledge base articles",
                node_type="event_loop",
                input_keys=["ticket_category", "parsed_ticket"],
                output_keys=["solutions_found", "knowledge_articles", "resolution_confidence"],
                tools=["knowledge_base_search", "solution_matcher", "documentation_search"],
                system_prompt="""You are a knowledge management specialist.

Your role is to:
1. Search knowledge base for relevant solutions
2. Match current issue with historical resolutions
3. Find appropriate documentation and guides
4. Assess confidence in proposed solutions

**Search Strategy:**
1. Keyword matching with ticket content
2. Category-specific solution databases
3. Similar issue patterns and resolutions
4. Product documentation and guides
5. Community forums and discussions

**Solution Types:**
- Step-by-step resolution guides
- Configuration instructions
- Troubleshooting procedures
- Workaround solutions
- Best practice recommendations

**Confidence Assessment:**
- High: Exact match with proven solution
- Medium: Similar issue with adaptable solution
- Low: Partial match requiring customization
- None: No relevant solutions found

**Tools Usage:**
- knowledge_base_search: Broad search across all knowledge
- solution_matcher: Find specific solution patterns
- documentation_search: Product documentation lookup

**Output:**
Use set_output("solutions_found", "List of potential solutions")
Use set_output("knowledge_articles", "Relevant documentation links")
Use set_output("resolution_confidence", "Confidence level in solutions")

Be thorough in searching but prioritize the most relevant and recent solutions.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="response_generation",
                name="Response Generation and Personalization",
                description="Generate personalized responses based on analysis and solutions",
                node_type="event_loop",
                input_keys=["parsed_ticket", "solutions_found", "ticket_category", "priority_level"],
                output_keys=["generated_response", "next_steps", "follow_up_actions"],
                tools=["response_templates", "personalization_engine", "solution_formatter"],
                system_prompt="""You are a customer communication specialist.

Your role is to:
1. Generate personalized, empathetic responses
2. Provide clear, actionable solutions
3. Set appropriate expectations and timelines
4. Include relevant resources and next steps

**Response Structure:**
1. **Acknowledge and Empathize**
   - Show understanding of the issue
   - Acknowledge customer frustration or urgency
   - Express commitment to resolution

2. **Solution Overview**
   - Explain the issue in clear terms
   - Provide step-by-step resolution
   - Include relevant links and resources

3. **Timeline and Expectations**
   - Set realistic resolution expectations
   - Provide estimated timeframes
   - Explain next steps in the process

4. **Additional Support**
   - Offer further assistance options
   - Provide escalation paths if needed
   - Include contact information for urgent issues

**Personalization Elements:**
- Reference customer history and context
- Use customer's preferred communication style
- Acknowledge customer tier and status
- Reference previous interactions when relevant

**Tools Usage:**
- response_templates: Base templates for different categories
- personalization_engine: Customize for customer context
- solution_formatter: Format solutions clearly

**Output:**
Use set_output("generated_response", "Complete personalized response")
Use set_output("next_steps", "Clear next steps for customer")
Use set_output("follow_up_actions", "Internal follow-up requirements")

Maintain professional, empathetic tone while being solution-focused.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="review_and_send",
                name="Response Review and Delivery",
                description="Review response quality and deliver to customer",
                node_type="event_loop",
                input_keys=["generated_response", "next_steps", "priority_level"],
                output_keys=["final_response", "delivery_status", "customer_satisfaction_prediction"],
                tools=["response_validator", "tone_analyzer", "delivery_system"],
                system_prompt="""You are a quality assurance and delivery specialist.

Your role is to:
1. Validate response quality and accuracy
2. Ensure appropriate tone and professionalism
3. Deliver response through appropriate channels
4. Monitor for customer satisfaction indicators

**Quality Validation:**
- Solution accuracy and completeness
- Clarity and readability
- Professional tone and empathy
- Appropriate technical detail level
- Compliance with brand guidelines

**Tone Analysis:**
- Empathetic and understanding
- Professional but approachable
- Confident and reassuring
- Culturally appropriate
- Brand voice consistency

**Delivery Channels:**
- Email (standard response)
- Chat (real-time interaction)
- Phone (urgent issues)
- Portal (formal documentation)
- SMS (critical updates only)

**Satisfaction Indicators:**
- Response completeness
- Solution clarity
- Timeline appropriateness
- Personalization quality
- Follow-up clarity

**Tools Usage:**
- response_validator: Check accuracy and completeness
- tone_analyzer: Ensure appropriate communication tone
- delivery_system: Send through appropriate channel

**Output:**
Use set_output("final_response", "Validated and approved response")
Use set_output("delivery_status", "Delivery confirmation and tracking")
Use set_output("customer_satisfaction_prediction", "Predicted satisfaction score")

Ensure every response meets quality standards before delivery.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="escalation",
                name="Escalation Management",
                description="Handle complex issues requiring escalation to specialized teams",
                node_type="event_loop",
                input_keys=["parsed_ticket", "resolution_confidence", "priority_level"],
                output_keys=["escalation_plan", "specialist_assignment", "escalation_timeline"],
                tools=["escalation_matrix", "specialist_finder", "escalation_tracker"],
                system_prompt="""You are an escalation management specialist.

Your role is to:
1. Identify issues requiring escalation
2. Determine appropriate escalation level
3. Assign to specialized teams or individuals
4. Track and manage escalation process

**Escalation Triggers:**
- No solution found in knowledge base
- Low confidence in proposed solutions
- Critical priority issues
- VIP customer requests
- Technical complexity beyond standard scope
- Legal or compliance implications

**Escalation Levels:**
- Level 1: Senior support specialist
- Level 2: Technical lead or product specialist
- Level 3: Engineering or development team
- Level 4: Management or executive level
- Level 5: Legal or compliance team

**Specialist Assignment:**
- Match expertise to issue type
- Consider current workload and availability
- Account for customer tier and SLA requirements
- Factor in geographic and time zone considerations

**Escalation Process:**
1. Document escalation reason and context
2. Assign to appropriate specialist
3. Set response time expectations
4. Monitor progress and follow-up
5. Communicate status to customer

**Tools Usage:**
- escalation_matrix: Determine appropriate escalation level
- specialist_finder: Identify best specialist for issue
- escalation_tracker: Monitor escalation progress

**Output:**
Use set_output("escalation_plan", "Detailed escalation strategy")
Use set_output("specialist_assignment", "Assigned specialist and contact")
Use set_output("escalation_timeline", "Expected resolution timeline")

Ensure escalations are handled efficiently and with clear communication.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
        ]

        edges = [
            Edge(
                id="intake-to-triage",
                source="intake",
                target="triage",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="triage-to-knowledge",
                source="triage",
                target="knowledge_check",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="knowledge-to-response",
                source="knowledge_check",
                target="response_generation",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="response-to-review",
                source="response_generation",
                target="review_and_send",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="knowledge-to-escalation",
                source="knowledge_check",
                target="escalation",
                condition="conditional",
                condition_expr="resolution_confidence in ['Low', 'None'] or priority_level == 'Critical'",
                priority=2,
            ),
        ]

        return Graph(
            id="customer-support-graph",
            nodes=nodes,
            edges=edges,
            entry_points={"start": "intake"},
            terminal_nodes=["review_and_send", "escalation"],
        )

    def _get_config(self) -> Dict[str, Any]:
        """Get agent configuration."""
        return {
            "llm": LLMConfig(
                model="gpt-4o",
                max_tokens=4000,
                temperature=0.3,
            ),
            "runtime": RuntimeConfig(
                storage_path=Path.home() / ".hive" / "agents" / "customer_support_agent",
                max_iterations=100,
                conversation_mode="continuous",
            ),
        }
