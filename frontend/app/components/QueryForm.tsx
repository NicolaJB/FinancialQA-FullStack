// frontend/app/components/QueryForm.tsx
"use client";

import { useState } from "react";
import axios from "axios";

export default function QueryForm() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResults([]);

    if (!query.trim()) {
      setError("Please enter a query.");
      return;
    }

    setLoading(true);

    try {
      // Send query and k to the Next.js API proxy
      const response = await axios.post("/api/query", { query, k: 3 });

      const data = response.data;

      if (data.summary && data.summary.trim()) {
        setResults([data.summary]);
      } else if (data.answer_chunks && data.answer_chunks.length > 0) {
        setResults(data.answer_chunks);
      } else if (data.error) {
        setError(data.error);
      } else {
        setResults(["No results found."]);
      }
    } catch (err: any) {
      console.error("Error calling API:", err);
      setError(err.response?.data?.error || "Server error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-5xl font-extrabold text-blue-700 mb-6 tracking-wide">Financial QA Query</h1>
      <p className="mb-4 text-gray-600">
        Enter a financial question or text snippet to search in the embedded documents.
      </p>

      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          className="w-full p-2 border border-gray-300 rounded mb-2"
          rows={4}
          placeholder="Example: Summarise Tesla's Q2 2025 earnings report."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Submit"}
        </button>
      </form>

      {error && <p className="text-red-600 mb-2">{error}</p>}

      {results.length > 0 && (
        <div>
          <h2 className="font-semibold mb-2 text-gray-950">Results:</h2>
          <ul className="list-disc pl-5 text-gray-700">
            {results.map((chunk, idx) => (
              <li key={idx} className="mb-1">{chunk}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
