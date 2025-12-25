// frontend/app/api/query/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const query = body.query?.trim();
    const k = body.k ?? 3; // default to 3 if not provided

    if (!query) {
      return NextResponse.json({ error: "Query cannot be empty" }, { status: 400 });
    }

    const backendUrl = "http://127.0.0.1:8000/api/query";

    const resp = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, k }),
    });

    let data;
    try {
      data = await resp.json();
    } catch (jsonErr) {
      console.error("Failed to parse JSON from backend:", jsonErr);
      const text = await resp.text();
      console.error("Backend response text:", text);
      return NextResponse.json({ error: "Backend did not return valid JSON" }, { status: 500 });
    }

    if (!resp.ok) {
      return NextResponse.json(
        { error: data.detail || data.error || "Backend error" },
        { status: resp.status }
      );
    }

    // Ensure a summary is always returned
    if (!data.summary || !data.summary.trim()) {
      data.summary = "No answer could be generated for this query.";
    }

    return NextResponse.json(data);
  } catch (err) {
    console.error("API route error:", err);
    return NextResponse.json({ error: "Server error. Please try again." }, { status: 500 });
  }
}
