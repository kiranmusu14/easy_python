/* =====================================================================
   Cloudflare Pages Function entry point for Ask-a-Doubt.

   Maps to the route  /api/ask  (functions/api/ask.js → /api/ask).

   It reuses the portable handler in /api/ask.js so there is one source of
   truth. Cloudflare passes a `context` object; we hand its `request` and
   `env` (where the GROQ_API_KEY secret is bound) to the shared handler.
   ===================================================================== */
import handler from "../../api/ask.js";

export function onRequest(context) {
  return handler(context.request, context.env);
}
