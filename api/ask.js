/* =====================================================================
   Ask-a-Doubt — single serverless function (Groq, OpenAI-compatible API).

   Portable by design: uses only the Web Fetch API (fetch / Request /
   Response / JSON) and no Node-specific built-ins, so the same file runs
   unmodified on Vercel Edge, Cloudflare Workers, Netlify Edge, and Deno
   Deploy.

   Grounding: the ONLY context is the current topic's already-parsed lesson
   text, sent by the frontend. No separate retrieval index or embedding
   store — the exact parsed lesson text already is the correct grounding.

   Secret: the API key is read from the GROQ_API_KEY environment variable,
   which must be set as a PLATFORM SECRET. It is never written into any
   shipped file.
   ===================================================================== */

// Vercel Edge opt-in (ignored by other runtimes).
export const config = { runtime: "edge" };

const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";
const DEFAULT_MODEL = "llama-3.3-70b-versatile";
const MAX_CONTEXT_CHARS = 12000;

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status: status || 200,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

// Read env from whichever runtime we're on:
//  - Cloudflare Workers / Deno Deploy pass an `env` object.
//  - Vercel Edge / Netlify expose globalThis.process.env.
function readEnv(name, envArg) {
  if (envArg && envArg[name] != null) return envArg[name];
  const g = globalThis;
  if (g.process && g.process.env && g.process.env[name] != null) return g.process.env[name];
  if (typeof Deno !== "undefined" && Deno.env) return Deno.env.get(name);
  return undefined;
}

// Single handler usable as:
//   Vercel Edge / Netlify:   export default (req) => handler(req)
//   Cloudflare Workers:      export default { fetch: (req, env) => handler(req, env) }
export default async function handler(request, env) {
  if (request.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });
  }
  if (request.method !== "POST") return json({ error: "Method not allowed" }, 405);

  const apiKey = readEnv("GROQ_API_KEY", env);
  if (!apiKey) {
    return json({ error: "Server is missing GROQ_API_KEY. Set it as a platform secret to enable Ask-a-Doubt." }, 503);
  }

  let payload;
  try {
    payload = await request.json();
  } catch (e) {
    return json({ error: "Invalid JSON body." }, 400);
  }

  const question = (payload && payload.question ? String(payload.question) : "").trim();
  const topic = (payload && payload.topic ? String(payload.topic) : "this topic").trim();
  let context = payload && payload.context ? String(payload.context) : "";
  if (!question) return json({ error: "Missing 'question'." }, 400);
  if (context.length > MAX_CONTEXT_CHARS) context = context.slice(0, MAX_CONTEXT_CHARS) + "\n…(truncated)";

  const model = readEnv("GROQ_MODEL", env) || DEFAULT_MODEL;

  const system =
    "You are a concise Python teaching assistant helping a student revise. " +
    "Answer ONLY using the lesson material provided in the user's message. " +
    "If the answer is not contained in that material, say so plainly and suggest what to review — do not invent APIs or facts. " +
    "Prefer short explanations and small code snippets drawn from the lesson. Never fabricate outputs.";

  const user =
    "Topic: " + topic + "\n\n" +
    "=== LESSON MATERIAL (your only source of truth) ===\n" +
    context + "\n" +
    "=== END LESSON MATERIAL ===\n\n" +
    "Student question: " + question;

  let groqRes;
  try {
    groqRes = await fetch(GROQ_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + apiKey,
      },
      body: JSON.stringify({
        model: model,
        temperature: 0.2,
        max_tokens: 700,
        messages: [
          { role: "system", content: system },
          { role: "user", content: user },
        ],
      }),
    });
  } catch (e) {
    return json({ error: "Failed to reach the model provider." }, 502);
  }

  if (!groqRes.ok) {
    let detail = "";
    try { detail = (await groqRes.text()).slice(0, 300); } catch (e) {}
    return json({ error: "Model provider returned " + groqRes.status, detail: detail }, 502);
  }

  let data;
  try { data = await groqRes.json(); } catch (e) { return json({ error: "Bad response from model provider." }, 502); }
  const answer =
    data && data.choices && data.choices[0] && data.choices[0].message
      ? data.choices[0].message.content
      : "(no answer returned)";

  return json({ answer: answer, model: model }, 200);
}
