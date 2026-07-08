# Python Revision Workspace

A self-hosted, offline-first revision site built **from the course's own
Python source files** — parsed, not LLM-summarised. Five modules
(Foundations, pandas, Matplotlib, EDA, Statistics) across 19 chapter
"topics", each with a verbatim lesson, detected syntax pointers, and a
practice quiz. The whole thing is static HTML/CSS/JS plus one optional
serverless function.

## Layout

```
basics/  Pandas/  Mathplotlib/  EDA/  "Stats In Python"/
  └── src/*.py         reconstructed, verbatim course source (the source of truth)
tools/
  parse_lessons.py     tokenizes a .py file into sections + {label, code} steps
  concepts.py          the 97-entry concept dictionary (label, regex, explanation)
  test_concepts.py     validates every regex against every topic (no false positives)
  corpus.py            builds the code-only scan corpus (strings/comments neutralized)
  quizzes.py           hand-authored "why" MCQs, keyed by topic
  build.py             parse → pointers → quiz → modules → web/data.js
web/
  index.html styles.css app.js   the single-page frontend (no framework, no CDN)
  data.js              AUTO-GENERATED — the whole workspace serialized
api/
  ask.js               optional Ask-a-Doubt serverless function (Groq)
```

## Rebuild the data

Any time you edit a `src/*.py`, the dictionary, or the quizzes:

```bash
python3 tools/test_concepts.py     # sanity-check regexes (optional)
python3 tools/build.py             # regenerates web/data.js and web/data.json
```

`build.py` output is **deterministic** — the same inputs always produce a
byte-identical `data.js` (quiz shuffling uses a stable hash, not random).

## Run locally

Pure static (Ask-a-Doubt shows a graceful "not deployed" note):

```bash
cd web && python3 -m http.server 8000
# open http://localhost:8000
```

With the AI function, use your platform's dev server (e.g. `vercel dev`
from the project root) and put `GROQ_API_KEY=...` in a root `.env`
(git-ignored — see `.env.example`).

## Deploy

The frontend works fully with the AI function switched off; only the
"Ask a Doubt" card degrades to an inline notice. Set `GROQ_API_KEY` as a
**platform secret** (never in a shipped file); optionally `GROQ_MODEL`
(default `llama-3.3-70b-versatile`).

### Cloudflare Pages (recommended here)

This repo is preconfigured for Cloudflare Pages:

- Static site is served from `web/`.
- `functions/api/ask.js` is the Pages Function → route `/api/ask` (it just
  reuses the shared handler in `api/ask.js`).
- `wrangler.toml` sets `pages_build_output_dir = "web"`.

**Option A — Dashboard (Git, auto-deploys on push):**
1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to
   Git**, pick `kiranmusu14/easy_python`.
2. Build settings: **Framework preset = None**, **Build command = (empty)**,
   **Build output directory = `web`**. Save & deploy.
3. **Settings → Environment variables → add secret `GROQ_API_KEY`** (and
   optionally `GROQ_MODEL`). Redeploy so the function picks it up.

**Option B — CLI (Wrangler):**
```bash
npx wrangler login
npx wrangler pages project create easy-python   # first time only
npx wrangler pages secret put GROQ_API_KEY       # paste the key when prompted
npx wrangler pages deploy                        # uses wrangler.toml (web/ + functions/)
```

### Other hosts

- **Vercel:** deploy the repo; `api/ask.js` already carries
  `export const config = { runtime: "edge" }`. Set the static root to `web/`
  and add `GROQ_API_KEY` in project env vars.
- **Netlify / Deno Deploy:** the same `api/ask.js` runs unmodified (Web
  Fetch API only).

## Keyboard shortcuts

`j` / `k` next / previous topic · `/` focus search · `[` toggle sidebar ·
`t` toggle theme.

## How grounding works (Ask a Doubt)

The frontend sends the question plus the **current topic's already-parsed
lesson text** as the only context. There is no separate retrieval index or
embedding store — the parsed lesson text already is the correct grounding.
The system prompt instructs the model to answer only from that material.

## Notes on the source files

The `src/*.py` files were reconstructed from the course's slide PDFs (the
original scripts weren't available). Code is kept verbatim to what the
slides show; a few spots where the *original slides* were internally
inconsistent are flagged in code comments (e.g. an EDA `.fillna` without
reassignment, and differing `dogs` weights between pandas chapters) rather
than silently "fixed". `Machine learning`, `Numpy`, and `Seaborn` folders
had no source material and are intentionally omitted.
