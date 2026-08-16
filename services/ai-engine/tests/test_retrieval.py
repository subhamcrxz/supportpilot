from pathlib import Path

from app.retrieval.knowledge_base import CloudDeskKnowledgeBase


def test_retrieval_returns_relevant_documents():
    repo_root = Path(__file__).resolve().parents[3]

    knowledge_base = CloudDeskKnowledgeBase(repo_root)

    documents = knowledge_base.retrieve(
        "I lost my API key and need a replacement",
        limit=3,
    )

    assert documents
    assert "security.md" in documents


def test_retrieval_limits_results():
    repo_root = Path(__file__).resolve().parents[3]

    knowledge_base = CloudDeskKnowledgeBase(repo_root)

    documents = knowledge_base.retrieve(
        "API authentication error",
        limit=3,
    )

    assert len(documents) <= 3
