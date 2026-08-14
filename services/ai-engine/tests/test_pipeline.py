from pathlib import Path

from app.pipeline.analyze_ticket import create_analyzer


def test_saml_ticket_is_answered():
    repo_root = Path(__file__).resolve().parents[3]

    analyzer = create_analyzer(repo_root)

    result = analyzer.analyze("CD-0029")

    assert result.action.value == "answer"
    assert result.requires_human is False
    assert "pricing.md" in result.sources


def test_api_secret_is_protected():
    repo_root = Path(__file__).resolve().parents[3]

    analyzer = create_analyzer(repo_root)

    result = analyzer.analyze("CD-0014")

    assert result.action.value == "refuse_and_guide"
    assert "secret_protection" in result.policy_flags
    assert result.requires_human is False


def test_security_incident_is_escalated():
    repo_root = Path(__file__).resolve().parents[3]

    analyzer = create_analyzer(repo_root)

    result = analyzer.analyze("CD-0018")

    assert result.action.value == "escalate"
    assert result.requires_human is True
    assert "security_incident" in result.policy_flags


def test_ambiguous_ticket_requests_clarification():
    repo_root = Path(__file__).resolve().parents[3]

    analyzer = create_analyzer(repo_root)

    result = analyzer.analyze("CD-0048")

    assert result.action.value == "clarify"
    assert result.requires_human is False