"""
Business Insights Agent

An AI-powered data analysis agent that transforms raw business data
into actionable insights, visualizations, and strategic recommendations.
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


class BusinessInsightsAgent(Agent):
    """Business Insights Agent for data analysis and strategic recommendations."""

    def __init__(self):
        """Initialize the Business Insights Agent."""
        super().__init__(
            goal=self._get_goal(),
            graph=self._get_graph(),
            config=self._get_config(),
        )

    def _get_goal(self) -> Goal:
        """Define the agent's goal."""
        return Goal(
            id="business-insights",
            name="Business Data Analysis and Insights",
            description="Analyze business data to generate actionable insights, trends, and strategic recommendations",
            success_criteria=[
                SuccessCriteria(
                    id="data_quality_assessment",
                    description="Thoroughly assess data quality and identify issues",
                    metric="data_quality_score",
                    target=0.85,
                    weight=0.2,
                ),
                SuccessCriteria(
                    id="insight_depth",
                    description="Generate deep, non-obvious insights from data",
                    metric="insight_depth_score",
                    target=0.80,
                    weight=0.25,
                ),
                SuccessCriteria(
                    id="actionability",
                    description="Provide specific, actionable recommendations",
                    metric="recommendation_actionability",
                    target=0.90,
                    weight=0.25,
                ),
                SuccessCriteria(
                    id="visualization_quality",
                    description="Create clear, informative visualizations",
                    metric="visualization_effectiveness",
                    target=0.85,
                    weight=0.15,
                ),
                SuccessCriteria(
                    id="completeness",
                    description="Cover all relevant aspects of the business question",
                    metric="analysis_completeness",
                    target=0.90,
                    weight=0.15,
                ),
            ],
            constraints=[
                Constraint(
                    id="data_privacy",
                    description="Must handle sensitive data responsibly and maintain confidentiality",
                    constraint_type="hard",
                    category="safety",
                ),
                Constraint(
                    id="statistical_validity",
                    description="Must use statistically sound methods and avoid misleading conclusions",
                    constraint_type="hard",
                    category="accuracy",
                ),
                Constraint(
                    id="business_context",
                    description="Must consider business context and practical constraints",
                    constraint_type="soft",
                    category="relevance",
                ),
                Constraint(
                    id="transparency",
                    description="Must clearly explain methodology and limitations",
                    constraint_type="hard",
                    category="transparency",
                ),
            ],
        )

    def _get_graph(self) -> Graph:
        """Define the agent's workflow graph."""
        nodes = [
            NodeSpec(
                id="discovery",
                name="Discovery and Scoping",
                description="Understand business question and data requirements",
                node_type="event_loop",
                input_keys=["business_question", "data_sources", "analysis_goals"],
                output_keys=["analysis_scope", "data_requirements", "success_metrics"],
                tools=[],
                system_prompt="""You are a business analytics consultant specializing in discovery and scoping.

Your role is to:
1. Understand the business problem or question
2. Identify relevant data sources and requirements
3. Define clear analysis scope and success metrics
4. Set expectations for what insights are possible

**STEP 1 — Respond to the user (text only, NO tool calls):**
- Ask about their business objectives and questions
- Understand what decisions they're trying to make
- Identify available data sources (files, databases, APIs)
- Clarify timeline and resource constraints
- Define what success looks like for this analysis

**STEP 2 — After the user responds, call set_output:**
- set_output("analysis_scope", "Clearly defined scope of analysis")
- set_output("data_requirements", "Specific data needs and sources")
- set_output("success_metrics", "How we'll measure successful insights")

Key areas to explore:
- Business context and industry
- Specific questions or hypotheses
- Available data (format, quality, timeframe)
- Decision-making timeline
- Stakeholder needs and expectations
- Technical constraints and capabilities

Be thorough but focused - the better the scoping, the better the insights.""",
                client_facing=True,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="data_ingestion",
                name="Data Ingestion and Preparation",
                description="Load, clean, and prepare data for analysis",
                node_type="event_loop",
                input_keys=["data_requirements", "analysis_scope"],
                output_keys=["cleaned_data", "data_quality_report", "data_summary"],
                tools=["read_csv", "read_json", "read_excel", "data_cleaning", "data_validation"],
                system_prompt="""You are a data engineering specialist focused on data ingestion and preparation.

Your role is to:
1. Load data from specified sources
2. Clean and preprocess the data
3. Assess data quality and identify issues
4. Prepare data for analysis

**Process:**
1. Use appropriate tools to load data (CSV, JSON, Excel, etc.)
2. Perform data cleaning:
   - Handle missing values
   - Remove duplicates
   - Fix data types
   - Standardize formats
3. Validate data quality:
   - Check for outliers
   - Verify data integrity
   - Assess completeness
4. Generate data quality report

**Data Quality Assessment:**
- Completeness: % of missing values
- Accuracy: validation against business rules
- Consistency: format and value consistency
- Timeliness: data recency and relevance

**Output:**
Use set_output("cleaned_data", "Cleaned dataset information")
Use set_output("data_quality_report", "Detailed quality assessment")
Use set_output("data_summary", "Statistical summary of key variables")

Be thorough in documenting data issues and transformations applied.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="exploratory_analysis",
                name="Exploratory Data Analysis",
                description="Perform initial analysis to understand patterns and relationships",
                node_type="event_loop",
                input_keys=["cleaned_data", "analysis_scope", "data_quality_report"],
                output_keys=["eda_findings", "hypotheses", "analysis_plan"],
                tools=["statistical_analysis", "correlation_analysis", "trend_analysis", "visualization"],
                system_prompt="""You are a data scientist specializing in exploratory data analysis.

Your role is to:
1. Understand data structure and distributions
2. Identify patterns, trends, and relationships
3. Generate hypotheses for deeper analysis
4. Plan the detailed analysis approach

**Analysis Areas:**
1. **Descriptive Statistics**
   - Central tendencies and dispersion
   - Distribution shapes and outliers
   - Time series patterns (if applicable)

2. **Relationship Analysis**
   - Correlations between variables
   - Categorical associations
   - Temporal relationships

3. **Pattern Discovery**
   - Clustering and segmentation
   - Anomaly detection
   - Trend identification

4. **Hypothesis Generation**
   - Formulate testable hypotheses
   - Identify key drivers and factors
   - Suggest causal relationships

**Visualization Strategy:**
- Distribution plots for key variables
- Correlation heatmaps
- Time series plots
- Scatter plots for relationships
- Box plots for comparisons

**Output:**
Use set_output("eda_findings", "Key discoveries from exploratory analysis")
Use set_output("hypotheses", "Testable hypotheses for deeper analysis")
Use set_output("analysis_plan", "Detailed plan for confirmatory analysis")

Focus on insights that directly address the business question.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="confirmatory_analysis",
                name="Confirmatory Analysis",
                description="Perform detailed statistical analysis to test hypotheses",
                node_type="event_loop",
                input_keys=["eda_findings", "hypotheses", "analysis_plan", "cleaned_data"],
                output_keys=["statistical_results", "validated_insights", "model_performance"],
                tools=["statistical_testing", "regression_analysis", "machine_learning", "forecasting"],
                system_prompt="""You are a senior data scientist specializing in confirmatory analysis and statistical modeling.

Your role is to:
1. Test hypotheses generated in exploratory phase
2. Build predictive models if needed
3. Perform statistical significance testing
4. Validate findings with robust methods

**Analysis Methods:**
1. **Hypothesis Testing**
   - T-tests, ANOVA for group comparisons
   - Chi-square tests for categorical data
   - Non-parametric tests when appropriate

2. **Predictive Modeling**
   - Regression analysis (linear, logistic)
   - Time series forecasting
   - Classification models
   - Clustering and segmentation

3. **Advanced Analytics**
   - Causal inference methods
   - A/B testing analysis
   - Survival analysis (if applicable)
   - Monte Carlo simulations

4. **Validation and Robustness**
   - Cross-validation
   - Sensitivity analysis
   - Residual analysis
   - Model interpretation

**Statistical Rigor:**
- Check assumptions for all tests
- Report effect sizes and confidence intervals
- Adjust for multiple comparisons
- Address potential confounders

**Output:**
Use set_output("statistical_results", "Detailed statistical findings")
Use set_output("validated_insights", "Business insights backed by statistical evidence")
Use set_output("model_performance", "Model accuracy and validation metrics")

Ensure all findings are statistically sound and business-relevant.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="insight_synthesis",
                name="Insight Synthesis and Recommendations",
                description="Synthesize findings into actionable business recommendations",
                node_type="event_loop",
                input_keys=["statistical_results", "validated_insights", "analysis_scope"],
                output_keys=["business_insights", "strategic_recommendations", "implementation_plan"],
                tools=[],
                system_prompt="""You are a business strategy consultant specializing in data-driven insights and recommendations.

Your role is to:
1. Synthesize all analytical findings
2. Translate statistical results into business language
3. Generate actionable strategic recommendations
4. Create implementation roadmaps

**Synthesis Process:**
1. **Insight Integration**
   - Combine findings from all analysis phases
   - Identify consistent patterns across methods
   - Prioritize insights by business impact
   - Connect insights to business objectives

2. **Strategic Recommendations**
   - Specific, measurable, achievable, relevant, time-bound (SMART) recommendations
   - Short-term wins and long-term initiatives
   - Resource requirements and ROI estimates
   - Risk assessment and mitigation strategies

3. **Implementation Planning**
   - Step-by-step action plans
   - Timeline and milestones
   - Required resources and capabilities
   - Success metrics and monitoring

4. **Stakeholder Communication**
   - Executive summary for leadership
   - Detailed findings for analysts
   - Action items for teams
   - Follow-up and review processes

**Recommendation Framework:**
- What: Specific action to take
- Why: Evidence-based rationale
- How: Implementation steps
- Who: Responsible parties
- When: Timeline and milestones
- Metrics: Success measures

**Output:**
Use set_output("business_insights", "Key business insights and their implications")
Use set_output("strategic_recommendations", "Actionable recommendations with implementation plans")
Use set_output("implementation_plan", "Detailed roadmap for executing recommendations")

Ensure recommendations are practical, data-driven, and aligned with business goals.""",
                client_facing=False,
                nullable_output_keys=[],
                max_node_visits=1,
            ),
            NodeSpec(
                id="presentation",
                name="Results Presentation and Review",
                description="Present findings and gather feedback from stakeholders",
                node_type="event_loop",
                input_keys=["business_insights", "strategic_recommendations", "implementation_plan"],
                output_keys=["presentation_feedback", "action_items", "next_steps"],
                tools=[],
                system_prompt="""You are a data visualization and communication specialist.

Your role is to:
1. Present analytical findings clearly and effectively
2. Facilitate stakeholder understanding and discussion
3. Gather feedback and additional requirements
4. Define next steps and action items

**Presentation Structure:**
1. **Executive Summary**
   - Key findings in 2-3 bullet points
   - Bottom-line business impact
   - Top recommendations

2. **Detailed Findings**
   - Methodology overview
   - Key insights with supporting evidence
   - Visualizations and charts
   - Limitations and assumptions

3. **Recommendations**
   - Prioritized action items
   - Implementation timeline
   - Resource requirements
   - Expected outcomes

4. **Discussion and Feedback**
   - Address stakeholder questions
   - Clarify ambiguous findings
   - Gather additional requirements
   - Refine recommendations

**Communication Principles:**
- Start with the "so what" - business impact first
- Use clear, non-technical language for business audiences
- Provide both high-level summary and detailed backup
- Anticipate questions and concerns

**STEP 1 — Present findings (text only, NO tool calls):**
- Present key insights and recommendations
- Show supporting visualizations and evidence
- Explain business implications clearly
- Invite questions and discussion

**STEP 2 — After stakeholder feedback, call set_output:**
- set_output("presentation_feedback", "Summary of stakeholder reactions and questions")
- set_output("action_items", "Specific action items and responsibilities")
- set_output("next_steps", "Follow-up activities and timeline")

Be prepared to adapt recommendations based on stakeholder input.""",
                client_facing=True,
                nullable_output_keys=[],
                max_node_visits=2,  # Allow for follow-up presentations
            ),
        ]

        edges = [
            Edge(
                id="discovery-to-data",
                source="discovery",
                target="data_ingestion",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="data-to-exploratory",
                source="data_ingestion",
                target="exploratory_analysis",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="exploratory-to-confirmatory",
                source="exploratory_analysis",
                target="confirmatory_analysis",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="confirmatory-to-synthesis",
                source="confirmatory_analysis",
                target="insight_synthesis",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
            Edge(
                id="synthesis-to-presentation",
                source="insight_synthesis",
                target="presentation",
                condition="on_success",
                condition_expr="",
                priority=1,
            ),
        ]

        return Graph(
            id="business-insights-graph",
            nodes=nodes,
            edges=edges,
            entry_points={"start": "discovery"},
            terminal_nodes=["presentation"],
        )

    def _get_config(self) -> Dict[str, Any]:
        """Get agent configuration."""
        return {
            "llm": LLMConfig(
                model="gpt-4o",
                max_tokens=8000,
                temperature=0.2,
            ),
            "runtime": RuntimeConfig(
                storage_path=Path.home() / ".hive" / "agents" / "business_insights_agent",
                max_iterations=30,
                conversation_mode="continuous",
            ),
        }
