/* =====================================================================
   Cloudflare Worker entry point (Workers Static Assets model).

   - Serves the static site in web/ via the ASSETS binding.
   - Handles POST /api/ask by delegating to the shared, portable handler
     in ../api/ask.js, which reads GROQ_API_KEY from env.

   Deployed with `wrangler deploy` using the [assets] config in
   wrangler.toml. The API key is a platform secret, never shipped.
   ===================================================================== */
import handler from "../api/ask.js";

export default {
  async fetch(request, env) {
    const { pathname } = new URL(request.url);
    if (pathname === "/api/ask") {
      return handler(request, env);
    }
    // Everything else is a static asset (index.html, app.js, data.js, …).
    return env.ASSETS.fetch(request);
  },
};
