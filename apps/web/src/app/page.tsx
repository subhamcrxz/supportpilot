"use client";

import { FormEvent, useState } from "react";

type AnalysisResult = {
  ticket_id: string;
  category: string;
  severity: string;
  difficulty: string;
  action: string;
  answer: string | null;
  requires_human: boolean;
  policy_flags: string[];
  sources: string[];
};

const ACTION_LABELS: Record<string, string> = {
  answer: "ANSWER",
  human_review: "HUMAN REVIEW",
  refuse_and_guide: "REFUSE AND GUIDE",
  refuse: "REFUSE",
  escalate: "ESCALATE",
  refuse_and_escalate: "REFUSE AND ESCALATE",
  clarify: "CLARIFY",
};

function formatValue(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function getActionClass(action: string): string {
  if (
    action === "human_review" ||
    action === "escalate" ||
    action === "refuse_and_escalate"
  ) {
    return "action-danger";
  }

  if (action === "refuse" || action === "refuse_and_guide") {
    return "action-warning";
  }

  if (action === "clarify") {
    return "action-neutral";
  }

  return "action-success";
}

export default function HomePage() {
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyzeTicket(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!subject.trim() || !message.trim()) {
      setError("Please provide both a subject and a customer message.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject: subject.trim(),
          message: message.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ?? "The AI engine could not analyze this ticket.",
        );
      }

      setResult(data as AnalysisResult);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Something went wrong while analyzing the ticket.",
      );
    } finally {
      setLoading(false);
    }
  }

  function clearTicket() {
    setSubject("");
    setMessage("");
    setResult(null);
    setError("");
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div className="eyebrow">SUPPORT COPILOT</div>

        <h1>
          Turn support tickets into
          <br />
          safe, actionable responses.
        </h1>

        <p className="hero-copy">
          Analyze a customer request, apply your support policies, retrieve
          relevant knowledge, and generate a response for your support team.
        </p>
      </section>

      <section className="workspace">
        <form className="ticket-card" onSubmit={analyzeTicket}>
          <div className="card-header">
            <div>
              <h2>Customer ticket</h2>
              <p>Paste a ticket to analyze it.</p>
            </div>

            <button
              className="clear-button"
              type="button"
              onClick={clearTicket}
              disabled={loading}
            >
              Clear
            </button>
          </div>

          <label htmlFor="subject">Subject</label>

          <input
            id="subject"
            type="text"
            value={subject}
            onChange={(event) => setSubject(event.target.value)}
            placeholder="e.g. Production API is down"
            maxLength={500}
            disabled={loading}
          />

          <label htmlFor="message">Customer message</label>

          <textarea
            id="message"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Paste the customer's support request here..."
            maxLength={10000}
            disabled={loading}
            rows={7}
          />

          {error ? <div className="error-message">{error}</div> : null}

          <button
            className="analyze-button"
            type="submit"
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze ticket"}
          </button>
        </form>

        <section className="result-card">
          {!result ? (
            <div className="empty-result">
              <div className="empty-eyebrow">ANALYSIS</div>

              <h2>Ticket decision</h2>

              <p>
                Submit a customer ticket to see the recommended action,
                policy flags, response, and supporting knowledge sources.
              </p>
            </div>
          ) : (
            <>
              <div className="result-header">
                <div>
                  <div className="empty-eyebrow">ANALYSIS</div>
                  <h2>Ticket decision</h2>
                </div>

                <span
                  className={`action-badge ${getActionClass(result.action)}`}
                >
                  {ACTION_LABELS[result.action] ?? formatValue(result.action)}
                </span>
              </div>

              <div className="metadata-grid">
                <div className="metadata-item">
                  <span>Category</span>
                  <strong>{formatValue(result.category)}</strong>
                </div>

                <div className="metadata-item">
                  <span>Severity</span>
                  <strong>{result.severity}</strong>
                </div>

                <div className="metadata-item">
                  <span>Difficulty</span>
                  <strong>{formatValue(result.difficulty)}</strong>
                </div>

                <div className="metadata-item">
                  <span>Human review</span>
                  <strong>
                    {result.requires_human ? "Required" : "Not required"}
                  </strong>
                </div>
              </div>

              {result.policy_flags.length > 0 ? (
                <div className="result-section">
                  <h3>Policy flags</h3>

                  <div className="tag-list">
                    {result.policy_flags.map((flag) => (
                      <span className="tag tag-danger" key={flag}>
                        {formatValue(flag)}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}

              <div className="result-section">
                <h3>Suggested response</h3>

                <div className="response-box">
                  {result.answer || "No response was generated."}
                </div>
              </div>

              {result.sources.length > 0 ? (
                <div className="result-section">
                  <h3>Knowledge sources</h3>

                  <div className="tag-list">
                    {result.sources.map((source) => (
                      <span className="source-tag" key={source}>
                        {source}
                      </span>
                    ))}
                  </div>
                </div>
              ) : null}
            </>
          )}
        </section>
      </section>

      <footer className="app-footer">
        <span>SupportPilot</span>
        <span>Policy-controlled AI support</span>
      </footer>
    </main>
  );
}