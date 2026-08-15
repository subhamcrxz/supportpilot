import json
import os
import statistics
import time
from pathlib import Path

import pytest

from app.policy.policy_engine import PolicyEngine
from app.providers.gemini import GeminiProvider
from app.providers.provider_models import ProviderContext
from app.providers.validator import (
    ProviderValidationError,
    validate_provider_response,
)
from app.retrieval.knowledge_base import CloudDeskKnowledgeBase

pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY is not set",
)


RESULTS_FILE = Path(__file__).parent / "artifacts" / "gemini_benchmark.json"


def percentile(values: list[float], percentage: float) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    index = (len(ordered) - 1) * percentage

    lower = int(index)
    upper = min(lower + 1, len(ordered))

    if lower == upper:
        return ordered[lower]

    weight = index - lower

    return ordered[lower] + (
        ordered[upper] - ordered[lower]
    ) * weight


def load_results() -> dict:
    if not RESULTS_FILE.exists():
        return {"tickets": {}}

    return json.loads(RESULTS_FILE.read_text())


def save_results(results: dict) -> None:
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    RESULTS_FILE.write_text(
        json.dumps(
            results,
            indent=2,
            sort_keys=True,
        )
    )


def test_gemini_full_clouddesk_benchmark():
    repo_root = Path(__file__).resolve().parents[3]

    knowledge_base = CloudDeskKnowledgeBase(repo_root)
    policy_engine = PolicyEngine()
    provider = GeminiProvider()

    tickets = knowledge_base.load_tickets()
    documents = knowledge_base.load_documents()

    assert len(tickets) == 50

    results = load_results()

    print()
    print("=" * 80)
    print("SupportPilot Gemini Benchmark")
    print("=" * 80)
    print(f"Tickets: {len(tickets)}")
    print(f"Results: {RESULTS_FILE}")
    print("=" * 80)

    for number, ticket in enumerate(tickets, start=1):
        ticket_id = ticket.id

        if ticket_id in results["tickets"]:

            print(
                f"[{number:02d}/50] "
                f"{ticket_id} SKIP "
                f"already tested"
            )

            continue

        policy = policy_engine.evaluate(ticket)

        context = ProviderContext(
            ticket=ticket,
            policy_action=policy.action,
            policy_flags=policy.flags,
            documents={
                source: documents[source]
                for source in ticket.required_sources
                if source in documents
            },
        )

        print(
            f"[{number:02d}/50] "
            f"{ticket_id} RUN"
        )

        start = time.perf_counter()

        try:
            response = provider.generate(context)

            validated = validate_provider_response(
                context,
                response,
            )

            latency = time.perf_counter() - start

            action_correct = (
                validated.action == ticket.expected_action
            )

            results["tickets"][ticket_id] = {
                "status": "success",
                "expected_action": ticket.expected_action.value,
                "actual_action": validated.action.value,
                "action_correct": action_correct,
                "confidence": validated.confidence,
                "latency_seconds": latency,
                "answer": validated.answer,
            }

            save_results(results)

            print(
                f"    PASS "
                f"{latency:.2f}s "
                f"action_correct={action_correct}"
            )

        except ProviderValidationError as exc:
            latency = time.perf_counter() - start

            results["tickets"][ticket_id] = {
                "status": "validation_failure",
                "error": str(exc),
                "latency_seconds": latency,
            }

            save_results(results)

            print(
                f"    VALIDATION FAILURE "
                f"{latency:.2f}s"
            )

        except Exception as exc:
            latency = time.perf_counter() - start

            error_text = repr(exc)

            results["tickets"][ticket_id] = {
                "status": "provider_error",
                "error": error_text,
                "latency_seconds": latency,
            }

            save_results(results)

            print(
                f"    PROVIDER ERROR "
                f"{latency:.2f}s"
            )

            # Stop immediately when the provider reports an error.
            # This prevents burning the remaining free-tier quota.
            print()
            print("Benchmark stopped after provider error.")
            print("Results have been saved.")
            break

    successful = [
        result
        for result in results["tickets"].values()
        if result["status"] == "success"
    ]

    validation_failures = [
        result
        for result in results["tickets"].values()
        if result["status"] == "validation_failure"
    ]

    provider_errors = [
        result
        for result in results["tickets"].values()
        if result["status"] == "provider_error"
    ]

    latencies = [
        result["latency_seconds"]
        for result in successful
        if "latency_seconds" in result
    ]

    correct_actions = sum(
        1
        for result in successful
        if result["action_correct"]
    )

    print()
    print("=" * 80)
    print("CURRENT BENCHMARK RESULTS")
    print("=" * 80)

    print(
        f"Completed successfully: "
        f"{len(successful)}/50"
    )

    print(
        f"Action accuracy: "
        f"{correct_actions}/{len(successful)} "
        f"("
        f"{correct_actions / len(successful):.1%}"
        f")"
        if successful
        else "Action accuracy: N/A"
    )

    print(
        f"Validation failures: "
        f"{len(validation_failures)}"
    )

    print(
        f"Provider errors: "
        f"{len(provider_errors)}"
    )

    if latencies:
        print(
            f"Average latency: "
            f"{statistics.mean(latencies):.2f}s"
        )

        print(
            f"P50 latency: "
            f"{percentile(latencies, 0.50):.2f}s"
        )

        print(
            f"P95 latency: "
            f"{percentile(latencies, 0.95):.2f}s"
        )

    print("=" * 80)

    # This is a diagnostic benchmark.
    assert len(results["tickets"]) >= len(successful)
