# Email Management Agent

**Version**: 1.0.0  
**Type**: Multi-node agent  
**Created**: 2026-03-08  

## Overview

An intelligent email inbox management system that processes Gmail emails using natural language rules provided by the user. The agent can automatically classify emails and take actions like archiving, starring, marking as spam, or trashing based on user-defined rules.

## Features

- **Natural Language Rules**: Describe email management rules in plain English
- **Intelligent Classification**: AI-powered email categorization and action selection
- **Comprehensive Actions**: Support for all major Gmail operations
- **Safety First**: Conservative approach to destructive actions (spam, trash)
- **Detailed Reporting**: Comprehensive summary of all actions taken
- **Interactive Setup**: User-friendly configuration and confirmation

## Architecture

### Execution Flow

```
intake → fetch_emails → classify_and_act → report
```

### Nodes (4 total)

1. **intake** (event_loop, client-facing)
   - Gather email management rules from user
   - Confirm maximum email processing limit
   - Present interpreted rules for confirmation
   - Reads: `rules, max_emails`
   - Writes: `validated_rules, max_emails`

2. **fetch_emails** (event_loop)
   - Fetch emails from Gmail INBOX only
   - Process in batches to handle large volumes
   - Extract key information from each email
   - Reads: `validated_rules, max_emails`
   - Writes: `emails, fetch_summary`
   - Tools: `gmail_list_messages, gmail_get_message`

3. **classify_and_act** (event_loop)
   - Apply user rules to classify each email
   - Execute appropriate Gmail actions
   - Batch similar operations for efficiency
   - Reads: `emails, validated_rules`
   - Writes: `actions_taken, processing_summary`
   - Tools: `gmail_batch_modify_messages, gmail_modify_message, gmail_trash_message`

4. **report** (event_loop)
   - Generate comprehensive summary report
   - Analyze rule effectiveness
   - Provide recommendations for improvement
   - Reads: `actions_taken, processing_summary, fetch_summary`
   - Writes: `final_report`

### Edges (3 total)

- `intake` → `fetch_emails` (on_success, priority=1)
- `fetch_emails` → `classify_and_act` (on_success, priority=1)
- `classify_and_act` → `report` (on_success, priority=1)

## Usage

### Command Line Interface

```bash
# Run the agent
python -m email_management_agent run \
  --rules "Archive newsletters, star emails from my boss, mark spam as spam" \
  --max-emails 100

# Validate configuration
python -m email_management_agent validate

# Show agent information
python -m email_management_agent info

# Start interactive shell
python -m email_management_agent shell
```

### Example Rules

- "Archive all newsletters and promotional emails"
- "Star emails from my boss or important clients"
- "Mark emails with 'unsubscribe' as spam"
- "Trash emails older than 1 year"
- "Move receipts to a specific folder"
- "Flag emails that need my response"

## Goal Criteria

### Success Criteria

1. **Classification Accuracy** (weight: 0.3)
   - Target: 90% classification match rate
   - Metric: classification_match_rate

2. **Action Correctness** (weight: 0.25)
   - Target: 95% correct actions
   - Metric: action_correctness

3. **Inbox Scope Compliance** (weight: 0.2)
   - Target: 100% inbox-only processing
   - Metric: inbox_scope_accuracy

4. **Comprehensive Processing** (weight: 0.15)
   - Target: 100% of fetched emails processed
   - Metric: emails_processed_ratio

5. **Report Completeness** (weight: 0.1)
   - Target: 100% complete reporting
   - Metric: report_completeness

### Constraints

1. **Inbox Only** (hard, safety)
   - Must only process emails from INBOX label

2. **Max Email Limit** (hard, operational)
   - Must not exceed configured max_emails parameter

3. **Valid Labels Only** (hard, operational)
   - Must only use Gmail system labels, not custom labels

4. **Spam Preservation** (hard, safety)
   - Spam moves to spam folder, trash only deletes explicitly

## Requirements

- Python 3.11+
- Gmail API access
- Appropriate OAuth permissions
- Hive framework dependencies

## Setup

1. **Install Dependencies**
   ```bash
   # From hive root directory
   ./quickstart.sh
   ```

2. **Configure Gmail API**
   - Enable Gmail API in Google Cloud Console
   - Create OAuth credentials
   - Set up authentication

3. **Set Up Credentials**
   ```bash
   /hive-credentials --agent email_management_agent
   ```

4. **Run the Agent**
   ```bash
   hive tui
   # Select "Email Management Agent" from the list
   ```

## Development

### Testing

```bash
# Validate agent structure
python -m email_management_agent validate

# Run in mock mode for testing
python -m email_management_agent run --mock --rules "test rules" --max-emails 10
```

### Extending the Agent

- Add new email classification logic in `classify_and_act` node
- Extend reporting capabilities in `report` node
- Add new Gmail tools as needed
- Implement custom rule parsing in `intake` node

## Troubleshooting

### Common Issues

1. **Gmail API Authentication**
   - Ensure OAuth credentials are properly configured
   - Check that required scopes are granted

2. **Rate Limiting**
   - Gmail API has rate limits
   - Agent includes batching to minimize API calls

3. **Rule Ambiguity**
   - Be specific in natural language rules
   - Review classification results in the report

### Debug Mode

Use the Hive debugger to analyze runtime issues:
```bash
/hive-debugger
```

## License

Apache License 2.0 - see LICENSE file for details.
