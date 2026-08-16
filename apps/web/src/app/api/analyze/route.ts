import { NextRequest, NextResponse } from "next/server";

const AI_ENGINE_URL =
  process.env.AI_ENGINE_URL ?? "http://localhost:8000";

const AI_ENGINE_API_KEY = process.env.AI_ENGINE_API_KEY;

export async function POST(request: NextRequest) {
  if (!AI_ENGINE_API_KEY) {
    return NextResponse.json(
      {
        detail: "AI engine authentication is not configured.",
      },
      { status: 503 },
    );
  }

  try {
    const body = await request.json();

    const response = await fetch(`${AI_ENGINE_URL}/analyze/request`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": AI_ENGINE_API_KEY,
      },
      body: JSON.stringify(body),
      cache: "no-store",
    });

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch {
    return NextResponse.json(
      {
        detail: "Unable to reach the AI engine.",
      },
      { status: 503 },
    );
  }
}
