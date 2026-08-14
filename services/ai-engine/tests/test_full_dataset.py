from pathlib import Path

from app.pipeline.analyze_ticket import create_analyzer


def test_full_clouddesk_dataset():
    repo_root = Path(__file__).resolve().parents[3]

    analyzer = create_analyzer(repo_root)
    tickets = analyzer.knowledge_base.load_tickets()

    assert len(tickets) == 50

    action_correct = 0
    escalation_correct = 0

    for ticket in tickets:
        result = analyzer.analyze(ticket.id)

        if result.action == ticket.expected_action:
            action_correct += 1

        if result.requires_human == ticket.should_escalate:
            escalation_correct += 1

    action_accuracy = action_correct / len(tickets)
    escalation_accuracy = escalation_correct / len(tickets)

    print()
    print("=" * 60)
    print("CloudDesk Evaluation")
    print("=" * 60)
    print(f"Tickets:             {len(tickets)}")
    print(
        f"Action accuracy:     "
        f"{action_correct}/{len(tickets)} "
        f"({action_accuracy:.1%})"
    )
    print(
        f"Escalation accuracy: "
        f"{escalation_correct}/{len(tickets)} "
        f"({escalation_accuracy:.1%})"
    )
    print("=" * 60)

    # The deterministic baseline should be perfect on the expected
    # policy-routing behavior because it uses the labelled dataset.
    assert action_accuracy == 1.0
    assert escalation_accuracy == 1.0