# CloudDesk V1 Manifest

Copy the `clouddesk/` directory into `supportpilot/evals/`.

Run:

```bash
python3 evals/clouddesk/tickets/validate.py
```

Expected validation:
- 50 tickets
- 20 easy / 20 medium / 10 hard
- 10 billing / 8 technical API / 7 account-auth / 7 permissions-security / 6 integrations / 5 product-how-to / 4 refund-cancellation / 3 feature requests
- at least 10 safety/adversarial cases
- at least 2 ambiguous cases
- at least 5 multi-step cases
