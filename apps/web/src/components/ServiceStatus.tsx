"use client";

import { useEffect, useState } from "react";
import type { ServiceHealth } from "@supportpilot/types";

type ServiceState = "online" | "checking" | "offline";

function getStatusClass(state: ServiceState): string {
  if (state === "online") return "status-online";
  if (state === "checking") return "status-checking";
  return "status-offline";
}

function formatLabel(name: string, state: ServiceState): string {
  const labels: Record<ServiceState, string> = {
    online: "Online",
    checking: "Checking...",
    offline: "Offline",
  };
  return `${name}: ${labels[state]}`;
}

async function checkService(url: string): Promise<boolean> {
  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) return false;
    const data = (await response.json()) as ServiceHealth;
    return data.status === "ok";
  } catch {
    return false;
  }
}

export function ServiceStatus() {
  const [apiState, setApiState] = useState<ServiceState>("checking");
  const [aiEngineState, setAiEngineState] = useState<ServiceState>("checking");

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3001";
    const aiEngineUrl = process.env.NEXT_PUBLIC_AI_ENGINE_URL ?? "http://localhost:8000";

    void checkService(`${apiUrl}/health`).then((ok) => {
      setApiState(ok ? "online" : "offline");
    });

    void checkService(`${aiEngineUrl}/health`).then((ok) => {
      setAiEngineState(ok ? "online" : "offline");
    });
  }, []);

  return (
    <section className="status-section">
      <h2>System Status</h2>
      <ul className="status-list">
        <li className="status-online">Web: Online</li>
        <li className={getStatusClass(apiState)}>{formatLabel("API", apiState)}</li>
        <li className={getStatusClass(aiEngineState)}>
          {formatLabel("AI Engine", aiEngineState)}
        </li>
      </ul>
    </section>
  );
}
