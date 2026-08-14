import json
from collections import Counter
from pathlib import Path

DATA = Path(__file__).with_name("tickets.json")
tickets = json.loads(DATA.read_text(encoding="utf-8"))

required = {
    "id", "subject", "message", "category", "severity", "difficulty",
    "expected_action", "expected_answer_summary", "required_sources",
    "should_escalate", "policy_tags"
}
valid_categories = {
    "billing", "technical_api", "account_authentication",
    "permissions_security", "integrations", "product_how_to",
    "refund_cancellation", "feature_request"
}
valid_severity = {"P0", "P1", "P2", "P3"}
valid_difficulty = {"easy", "medium", "hard"}
valid_actions = {
    "answer", "human_review", "refuse_and_guide", "refuse",
    "escalate", "refuse_and_escalate", "clarify"
}

assert len(tickets) == 50, f"Expected 50 tickets, got {len(tickets)}"
assert len({t["id"] for t in tickets}) == 50, "Ticket IDs must be unique"

for t in tickets:
    missing = required - t.keys()
    assert not missing, f'{t["id"]} missing fields: {sorted(missing)}'
    assert t["category"] in valid_categories, t["id"]
    assert t["severity"] in valid_severity, t["id"]
    assert t["difficulty"] in valid_difficulty, t["id"]
    assert t["expected_action"] in valid_actions, t["id"]
    assert t["required_sources"], f'{t["id"]} needs at least one source'

expected_categories = {
    "billing": 10, "technical_api": 8, "account_authentication": 7,
    "permissions_security": 7, "integrations": 6, "product_how_to": 5,
    "refund_cancellation": 4, "feature_request": 3
}
assert Counter(t["category"] for t in tickets) == expected_categories
assert Counter(t["difficulty"] for t in tickets) == {
    "easy": 20, "medium": 20, "hard": 10
}

adversarial_tags = {
    "secret_protection", "no_secrets", "no_passwords", "identity_verification",
    "security_incident", "prompt_injection", "destructive_action",
    "contractual_exception", "refund_exception"
}
adversarial = [t for t in tickets if adversarial_tags.intersection(t["policy_tags"])]
ambiguous = [t for t in tickets if "ambiguous" in " ".join(t["policy_tags"])]
multi_step = [t for t in tickets if "multi_step" in t["policy_tags"]]

assert len(adversarial) >= 10
assert len(ambiguous) >= 2
assert len(multi_step) >= 5

print("CloudDesk dataset validation passed.")
print(f"Tickets: {len(tickets)}")
print(f"Categories: {dict(Counter(t['category'] for t in tickets))}")
print(f"Difficulty: {dict(Counter(t['difficulty'] for t in tickets))}")
print(f"Safety/adversarial: {len(adversarial)}")
print(f"Ambiguous: {len(ambiguous)}")
print(f"Multi-step: {len(multi_step)}")
