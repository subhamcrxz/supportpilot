# Placeholder: Ticket Classification

> Status: Placeholder — not used in production yet.

## Intent

Classify incoming support tickets by category and urgency to route them to the appropriate workflow.

## Expected Inputs

- `subject`: Ticket subject line
- `body`: Ticket body text
- `customer_tier`: Optional customer tier (free, pro, enterprise)

## Expected Outputs

- `category`: One of billing, technical, account, feature_request, other
- `urgency`: One of low, medium, high, critical
- `confidence`: Float between 0 and 1

## Prompt Template

```
You are a support operations assistant for a B2B SaaS company.

Classify the following support ticket.

Subject: {{subject}}
Body: {{body}}
Customer tier: {{customer_tier}}

Respond with JSON containing category, urgency, and confidence.
```
