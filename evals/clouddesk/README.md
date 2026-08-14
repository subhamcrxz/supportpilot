# CloudDesk Evaluation Dataset

CloudDesk is a fictional B2B project-management SaaS used as the controlled evaluation environment for SupportPilot.

This dataset is synthetic and contains no real customer information.

## Purpose

The dataset is designed to test whether SupportPilot can:

- retrieve the correct product information
- classify support requests
- determine severity
- follow account, billing, security, and refund policies
- avoid revealing secrets
- recognize when information is insufficient
- escalate risky or exceptional cases
- resist prompt-injection attempts

## Structure

- `company/` — company, pricing, general policies, security
- `product/` — product behavior, roles, API, integrations
- `support/` — support, escalation, and refund rules
- `knowledge-base/` — customer-facing support knowledge
- `tickets/` — 50 labeled evaluation tickets

## Dataset counts

- 50 total tickets
- 10 billing
- 8 technical/API
- 7 account/authentication
- 7 permissions/security
- 6 integrations
- 5 product/how-to
- 4 refund/cancellation
- 3 feature requests

Difficulty:
- 20 easy
- 20 medium
- 10 hard

Safety cases:
- 10+ adversarial/policy-sensitive cases
- 5+ ambiguous cases
- 5+ multi-step cases

The expected fields are deliberately concise. We will later use these labels to evaluate SupportPilot rather than requiring one exact wording for every correct response.
