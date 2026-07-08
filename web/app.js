/* =====================================================================
   Python Revision Workspace — framework-free single-page app.
   Reads window.__COURSE_DATA__ (built by tools/build.py). No runtime
   parsing, no backend required (Ask-a-Doubt is optional and degrades
   gracefully when its endpoint is absent).
   ===================================================================== */
(function () {
  "use strict";

  var DATA = window.__COURSE_DATA__;
  if (!DATA) { document.getElementById("content").innerHTML = "<p>Failed to load course data.</p>"; return; }

  var TOPICS = {};
  DATA.topics.forEach(function (t) { TOPICS[t.id] = t; });
  var MODULE_BY_ID = {};
  DATA.modules.forEach(function (m) { MODULE_BY_ID[m.id] = m; });

  var COLLAPSE_THRESHOLD = 6; // sections with >= this many steps start collapsed

  // ---- persistent state -------------------------------------------------
  var LS_ANSWERS = "pyrev.answers.v1";
  var LS_THEME = "pyrev.theme.v1";
  var answers = loadJSON(LS_ANSWERS, {});      // { topicId: { qIndex: chosenOption } }

  function loadJSON(key, fallback) {
    try { var v = JSON.parse(localStorage.getItem(key)); return v == null ? fallback : v; }
    catch (e) { return fallback; }
  }
  function saveAnswers() { try { localStorage.setItem(LS_ANSWERS, JSON.stringify(answers)); } catch (e) {} }

  // ---- theme ------------------------------------------------------------
  function initTheme() {
    var saved = localStorage.getItem(LS_THEME);
    var theme = saved || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);
  }
  function toggleTheme() {
    var cur = document.documentElement.getAttribute("data-theme");
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem(LS_THEME, next); } catch (e) {}
  }

  // ---- quiz completion helpers -----------------------------------------
  function topicAnswered(topicId) {
    var a = answers[topicId] || {};
    return Object.keys(a).length;
  }
  function topicQuizLen(topicId) { return (TOPICS[topicId].quiz || []).length; }
  function topicComplete(topicId) {
    var len = topicQuizLen(topicId);
    return len > 0 && topicAnswered(topicId) >= len;
  }
  function topicFraction(topicId) {
    var len = topicQuizLen(topicId);
    return len === 0 ? 0 : topicAnswered(topicId) / len;
  }
  function totalComplete() {
    return DATA.topics.reduce(function (n, t) { return n + (topicComplete(t.id) ? 1 : 0); }, 0);
  }

  // ---- HTML escaping ----------------------------------------------------
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // ---- Python syntax highlighter (self-contained, regex-based) ----------
  var KEYWORDS = ("False None True and as assert async await break class continue def del elif else " +
    "except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield").split(" ");
  var BUILTINS = ("print len range type int float str bool list dict set tuple max min sum sorted enumerate zip map " +
    "filter abs round open help dir isinstance getattr setattr id input format reversed any all").split(" ");
  var KW_RE = new RegExp("\\b(?:" + KEYWORDS.join("|") + ")\\b");
  var BI_RE = new RegExp("\\b(?:" + BUILTINS.join("|") + ")\\b");

  // One master pass; the first matching alternative at each position wins so
  // string/comment interiors are never re-tokenized.
  var MASTER = new RegExp(
    "(#[^\\n]*)" +                                                   // 1 comment
    "|(\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?''')" +                   // 2 triple string
    "|([rRbBfFuU]{0,2}(?:\"(?:\\\\.|[^\"\\\\])*\"|'(?:\\\\.|[^'\\\\])*'))" + // 3 string (+f/r/b)
    "|(\\b\\d+\\.?\\d*(?:[eE][-+]?\\d+)?\\b)" +                      // 4 number
    "|(" + KW_RE.source + ")" +                                     // 5 keyword
    "|(" + BI_RE.source + ")" +                                     // 6 builtin
    "|(\\b[A-Za-z_]\\w*(?=\\s*\\())",                               // 7 function call
    "g"
  );

  function highlight(code) {
    // Tokenize the RAW code, then escape gaps and token text separately.
    // (Escaping first would turn quotes into &quot; and defeat string
    // detection.)
    var re = new RegExp(MASTER.source, "g");
    var out = "", last = 0, m;
    while ((m = re.exec(code)) !== null) {
      out += esc(code.slice(last, m.index));
      var text = esc(m[0]);
      if (m[1]) out += span("tok-com", text);
      else if (m[2] || m[3]) out += span("tok-str", text);
      else if (m[4]) out += span("tok-num", text);
      else if (m[5]) out += span("tok-kw", text);
      else if (m[6]) out += span("tok-builtin", text);
      else if (m[7]) out += span("tok-fn", text);
      else out += text;
      last = m.index + m[0].length;
      if (m[0].length === 0) re.lastIndex++;
    }
    out += esc(code.slice(last));
    return out;
  }
  function span(cls, text) { return '<span class="' + cls + '">' + text + "</span>"; }

  // ---- code block with copy button -------------------------------------
  function codeBlock(code) {
    var wrap = document.createElement("div");
    wrap.className = "code-wrap";
    var pre = document.createElement("pre");
    pre.className = "code";
    pre.innerHTML = highlight(code);
    var btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () { copyText(code, btn); });
    wrap.appendChild(pre);
    wrap.appendChild(btn);
    return wrap;
  }
  function copyText(text, btn) {
    function done() { toast("Copied to clipboard"); if (btn) { var o = btn.textContent; btn.textContent = "Copied!"; setTimeout(function () { btn.textContent = o; }, 1200); } }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text, done); });
    } else { fallbackCopy(text, done); }
  }
  function fallbackCopy(text, done) {
    var ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  var toastTimer;
  function toast(msg) {
    var el = document.getElementById("toast");
    el.textContent = msg; el.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { el.classList.remove("show"); }, 1600);
  }

  // ---- sidebar ----------------------------------------------------------
  function renderSidebar() {
    var nav = document.getElementById("nav");
    nav.innerHTML = "";
    var globalNum = 0;
    DATA.modules.forEach(function (mod) {
      var wrap = document.createElement("div"); wrap.className = "nav-module";
      var title = document.createElement("div"); title.className = "nav-module-title"; title.textContent = mod.name;
      wrap.appendChild(title);
      mod.topicIds.forEach(function (tid) {
        globalNum++;
        var t = TOPICS[tid];
        var btn = document.createElement("button");
        btn.className = "nav-topic"; btn.dataset.topic = tid;
        btn.dataset.search = (t.title + " " + mod.name).toLowerCase();
        btn.innerHTML =
          '<span class="tick">✓</span>' +
          '<span class="tnum">' + globalNum + "</span>" +
          "<span>" + esc(t.title) + "</span>";
        btn.addEventListener("click", function () { location.hash = "#/" + tid; });
        wrap.appendChild(btn);
      });
      nav.appendChild(wrap);
    });
    refreshSidebarState();
  }

  function refreshSidebarState() {
    var current = currentTopicId();
    document.querySelectorAll(".nav-topic").forEach(function (btn) {
      var tid = btn.dataset.topic;
      btn.classList.toggle("active", tid === current);
      btn.classList.toggle("done", topicComplete(tid));
    });
    document.getElementById("global-progress").textContent = totalComplete() + " / " + DATA.totalTopics;
  }

  // ---- search -----------------------------------------------------------
  function initSearch() {
    var input = document.getElementById("search");
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      document.querySelectorAll(".nav-topic").forEach(function (btn) {
        btn.classList.toggle("hidden", q !== "" && btn.dataset.search.indexOf(q) === -1);
      });
      document.querySelectorAll(".nav-module").forEach(function (mod) {
        var anyVisible = mod.querySelector(".nav-topic:not(.hidden)");
        mod.style.display = anyVisible ? "" : "none";
      });
    });
    input.addEventListener("keydown", function (e) { if (e.key === "Escape") { input.value = ""; input.dispatchEvent(new Event("input")); input.blur(); } });
  }

  // ---- ring & breadcrumb ------------------------------------------------
  var RING_C = 2 * Math.PI * 18;
  function updateRing(topicId) {
    var frac = topicFraction(topicId);
    var fill = document.getElementById("ring-fill");
    fill.style.strokeDashoffset = String(RING_C * (1 - frac));
    document.getElementById("ring-label").textContent = Math.round(frac * 100) + "%";
    document.getElementById("ring-wrap").classList.toggle("complete", topicComplete(topicId));
  }
  function renderBreadcrumb(topic) {
    var mod = MODULE_BY_ID[topic.moduleId];
    document.getElementById("breadcrumb").innerHTML =
      '<span class="crumb-module">' + esc(mod.name) + "</span>" +
      '<span class="sep">›</span>' +
      '<span class="crumb-topic">' + esc(topic.title) + "</span>";
  }

  // ---- topic page -------------------------------------------------------
  var observer = null;

  function renderTopic(topicId) {
    var topic = TOPICS[topicId];
    var content = document.getElementById("content");
    content.innerHTML = "";
    if (observer) { observer.disconnect(); observer = null; }

    renderBreadcrumb(topic);
    updateRing(topicId);

    content.appendChild(renderHero(topic));
    if (topic.syntaxPointers.length) content.appendChild(renderPointers(topic));
    content.appendChild(renderLesson(topic));
    content.appendChild(renderQuiz(topic));
    content.appendChild(renderDoubt(topic));

    setupScrollSpy(topic);
    refreshSidebarState();
    content.focus();
    window.scrollTo(0, 0);
  }

  function renderHero(topic) {
    var mod = MODULE_BY_ID[topic.moduleId];
    var hero = document.createElement("div"); hero.className = "hero";
    var chips =
      '<span class="chip meta">' + topic.meta.sections + " sections</span>" +
      '<span class="chip meta">' + topic.meta.steps + " steps</span>" +
      '<span class="chip meta">' + topic.meta.pointers + " syntax pointers</span>" +
      '<span class="chip meta">' + topic.meta.quizQuestions + " quiz Qs</span>";
    var jumps = topic.sections.map(function (s) {
      return '<button class="jump-chip" data-jump="sec-' + s.number + '">' + s.number + ". " + esc(s.title) + "</button>";
    }).join("");
    hero.innerHTML =
      '<div class="chips"><span class="chip">' + esc(mod.name) + "</span></div>" +
      "<h1>" + esc(topic.title) + "</h1>" +
      '<p class="desc">' + esc(topic.description) + "</p>" +
      '<div class="chips">' + chips + "</div>" +
      '<div class="jump-chips">' + jumps + "</div>";
    hero.querySelectorAll(".jump-chip").forEach(function (b) {
      b.addEventListener("click", function () {
        var el = document.getElementById(b.dataset.jump);
        if (el) {
          var sec = el.closest(".lesson-section");
          if (sec && sec.classList.contains("collapsed")) sec.classList.remove("collapsed");
          el.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
    return hero;
  }

  function renderPointers(topic) {
    var card = document.createElement("section"); card.className = "card";
    card.innerHTML = "<h2>Syntax Pointers <span class=\"card-badge\">" + topic.syntaxPointers.length + "</span></h2>" +
      '<p class="card-sub">Python syntax &amp; idioms detected in this topic’s source, with the mechanic or gotcha.</p>';
    topic.syntaxPointers.forEach(function (p) {
      var d = document.createElement("div"); d.className = "pointer";
      d.innerHTML =
        '<div class="pointer-head"><span class="pointer-label">' + esc(p.label) + "</span>" +
        '<span class="pointer-count">' + p.count + "×</span></div>" +
        '<div class="pointer-explain">' + esc(p.explanation) + "</div>";
      if (p.example) d.appendChild(codeBlock(p.example));
      card.appendChild(d);
    });
    return card;
  }

  function renderLesson(topic) {
    var card = document.createElement("section"); card.className = "card";
    var head = document.createElement("h2"); head.textContent = "Lesson and Syntax"; card.appendChild(head);
    var sub = document.createElement("p"); sub.className = "card-sub";
    sub.textContent = "Every step is verbatim from the source. Large sections start collapsed as an outline.";
    card.appendChild(sub);

    topic.sections.forEach(function (section) {
      var many = section.steps.length >= COLLAPSE_THRESHOLD;
      var sec = document.createElement("div");
      sec.className = "lesson-section" + (many ? " collapsed" : "");

      var shead = document.createElement("div"); shead.className = "section-head";
      shead.innerHTML =
        '<span class="section-caret">▾</span>' +
        '<span class="section-num">' + section.number + "</span>" +
        "<h3 id=\"sec-" + section.number + "\">" + esc(section.title) + "</h3>";
      var tools = document.createElement("div"); tools.className = "section-tools";
      var count = document.createElement("span"); count.className = "step-count";
      count.textContent = section.steps.length + (section.steps.length === 1 ? " step" : " steps");
      tools.appendChild(count);
      if (many) {
        var exp = document.createElement("button"); exp.className = "expand-all"; exp.textContent = "Expand all";
        exp.addEventListener("click", function (e) {
          e.stopPropagation();
          var collapsedNow = sec.classList.contains("collapsed");
          sec.classList.remove("collapsed");
          var steps = sec.querySelectorAll(".step");
          var anyCollapsed = Array.prototype.some.call(steps, function (s) { return s.classList.contains("collapsed"); });
          steps.forEach(function (s) { s.classList.toggle("collapsed", !anyCollapsed); });
          exp.textContent = anyCollapsed ? "Collapse all" : "Expand all";
        });
        tools.appendChild(exp);
      }
      shead.appendChild(tools);
      shead.addEventListener("click", function () { sec.classList.toggle("collapsed"); });
      sec.appendChild(shead);

      var body = document.createElement("div"); body.className = "section-body";
      section.steps.forEach(function (step) {
        body.appendChild(renderStep(step, many));
      });
      sec.appendChild(body);
      card.appendChild(sec);
    });
    return card;
  }

  function renderStep(step, startCollapsed) {
    var hasCode = step.code && step.code.trim() !== "";
    if (!hasCode) {
      // comment-only step -> plain note callout, not an empty code block
      var note = document.createElement("div"); note.className = "note-callout";
      note.textContent = step.note || step.label;
      return note;
    }
    var el = document.createElement("div");
    el.className = "step" + (startCollapsed ? " collapsed" : "");
    var head = document.createElement("div"); head.className = "step-head";
    head.innerHTML = '<span class="step-caret">▾</span><span class="step-title">' + esc(step.label) + "</span>";
    head.addEventListener("click", function () { el.classList.toggle("collapsed"); });
    var body = document.createElement("div"); body.className = "step-body";
    if (step.note && step.note !== step.label) {
      var n = document.createElement("div"); n.className = "note-callout"; n.textContent = step.note;
      body.appendChild(n);
    }
    body.appendChild(codeBlock(step.code));
    el.appendChild(head); el.appendChild(body);
    return el;
  }

  // ---- quiz -------------------------------------------------------------
  function renderQuiz(topic) {
    var card = document.createElement("section"); card.className = "card";
    card.innerHTML = "<h2>Practice Quiz</h2>" +
      '<p class="card-sub">Answers are saved as you go. Green/red mark correctness; the ring above tracks completion.</p>';
    var quiz = topic.quiz || [];
    if (!quiz.length) { var e = document.createElement("p"); e.className = "empty"; e.textContent = "No quiz for this topic yet."; card.appendChild(e); return card; }
    quiz.forEach(function (q, qi) { card.appendChild(renderQuestion(topic, q, qi)); });
    return card;
  }

  function renderQuestion(topic, q, qi) {
    var wrap = document.createElement("div"); wrap.className = "quiz-q";
    var tag = q.auto ? '<span class="quiz-tag auto">snippet</span>' : '<span class="quiz-tag hand">concept</span>';
    var qhtml = '<div class="qnum">Q' + (qi + 1) + tag + "</div>" +
      '<div class="qtext">' + esc(q.question) + "</div>";
    wrap.innerHTML = qhtml;
    if (q.code) { var cw = codeBlock(q.code); cw.classList.add("quiz-code"); wrap.appendChild(cw); }

    var chosen = (answers[topic.id] || {})[qi];
    var answered = chosen !== undefined;

    q.options.forEach(function (opt, oi) {
      var b = document.createElement("button");
      b.className = "opt";
      b.innerHTML = '<span class="opt-key">' + "ABCD"[oi] + "</span><span>" + esc(opt) + "</span>";
      if (answered) {
        b.disabled = true;
        if (oi === q.answer) b.classList.add(oi === chosen ? "correct" : "reveal-correct");
        if (oi === chosen && chosen !== q.answer) b.classList.add("incorrect");
        if (oi === chosen && chosen === q.answer) b.classList.add("correct");
      }
      b.addEventListener("click", function () { onAnswer(topic, qi, oi); });
      wrap.appendChild(b);
    });

    if (answered) wrap.appendChild(explainEl(q, chosen));
    return wrap;
  }

  function explainEl(q, chosen) {
    var ex = document.createElement("div");
    var good = chosen === q.answer;
    ex.className = "quiz-explain " + (good ? "good" : "bad");
    ex.innerHTML = "<strong>" + (good ? "Correct. " : "Not quite. ") + "</strong>" + esc(q.explanation);
    return ex;
  }

  function onAnswer(topic, qi, oi) {
    if (!answers[topic.id]) answers[topic.id] = {};
    if (answers[topic.id][qi] !== undefined) return; // lock first answer per question
    answers[topic.id][qi] = oi;
    saveAnswers();
    // Re-render just this question in place.
    var card = document.querySelectorAll("#content .card");
    // Simplest reliable path: re-render the topic to keep everything consistent.
    var scrollY = window.scrollY;
    renderTopic(topic.id);
    window.scrollTo(0, scrollY);
  }

  // ---- Ask a Doubt (optional; degrades gracefully) ----------------------
  var AI_ENDPOINT = "/api/ask"; // single serverless function; absent in pure-static deploys

  function renderDoubt(topic) {
    var card = document.createElement("section"); card.className = "card";
    card.innerHTML = "<h2>Ask a Doubt</h2>" +
      '<p class="card-sub">Grounded only in this topic’s parsed lesson text. Optional feature — the workspace works fully without it.</p>';
    var ta = document.createElement("textarea"); ta.id = "doubt-input"; ta.placeholder = "e.g. Why does y = x change x too?";
    card.appendChild(ta);
    var row = document.createElement("div"); row.className = "doubt-row";
    var ask = document.createElement("button"); ask.className = "btn"; ask.textContent = "Ask";
    var clear = document.createElement("button"); clear.className = "btn ghost"; clear.textContent = "Clear";
    row.appendChild(ask); row.appendChild(clear); card.appendChild(row);
    var out = document.createElement("div"); out.className = "doubt-answer"; card.appendChild(out);
    var note = document.createElement("div"); note.className = "doubt-note";
    note.textContent = "Sends your question plus this topic’s lesson text to the AI endpoint if one is deployed.";
    card.appendChild(note);

    clear.addEventListener("click", function () { ta.value = ""; out.textContent = ""; });
    ask.addEventListener("click", function () { askDoubt(topic, ta.value, out, ask); });
    return card;
  }

  function lessonPlainText(topic) {
    var parts = [topic.title, topic.description];
    topic.sections.forEach(function (s) {
      parts.push("## " + s.title);
      s.steps.forEach(function (st) { if (st.note) parts.push(st.note); if (st.code) parts.push(st.code); });
    });
    return parts.join("\n");
  }

  function askDoubt(topic, question, out, btn) {
    question = (question || "").trim();
    if (!question) { out.innerHTML = '<span class="doubt-disabled">Type a question first.</span>'; return; }
    out.textContent = "Thinking…"; btn.disabled = true;
    fetch(AI_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question, topic: topic.title, context: lessonPlainText(topic) })
    }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    }).then(function (j) {
      out.textContent = j.answer || "(no answer returned)";
    }).catch(function () {
      out.innerHTML = '<span class="doubt-disabled">The Ask-a-Doubt endpoint isn’t available in this deployment. ' +
        "Everything else works offline. Deploy the serverless function in <code>api/ask</code> and set its API key to enable it.</span>";
    }).then(function () { btn.disabled = false; });
  }

  // ---- scroll-spy (IntersectionObserver) --------------------------------
  function setupScrollSpy(topic) {
    var chips = {};
    document.querySelectorAll(".jump-chip").forEach(function (c) { chips[c.dataset.jump] = c; });
    var heads = Array.prototype.slice.call(document.querySelectorAll(".section-head h3"));
    if (!heads.length) return;
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var id = en.target.id;
          Object.keys(chips).forEach(function (k) { chips[k].classList.toggle("active", k === id); });
        }
      });
    }, { rootMargin: "-70px 0px -70% 0px", threshold: 0 });
    heads.forEach(function (h) { observer.observe(h); });
  }

  // ---- reading-progress bar --------------------------------------------
  function initProgressBar() {
    var bar = document.getElementById("progress-bar");
    function update() {
      var h = document.documentElement;
      var scrollable = h.scrollHeight - h.clientHeight;
      var pct = scrollable > 0 ? (h.scrollTop / scrollable) * 100 : 0;
      bar.style.width = pct + "%";
    }
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // ---- routing ----------------------------------------------------------
  function currentTopicId() {
    var m = location.hash.match(/^#\/(.+)$/);
    return m ? decodeURIComponent(m[1]) : null;
  }
  function route() {
    var id = currentTopicId();
    if (!id || !TOPICS[id]) { location.replace("#/" + DATA.topicOrder[0]); return; }
    renderTopic(id);
  }

  function neighbor(delta) {
    var id = currentTopicId();
    var idx = DATA.topicOrder.indexOf(id);
    if (idx === -1) idx = 0;
    var next = idx + delta;
    if (next < 0 || next >= DATA.topicOrder.length) return;
    location.hash = "#/" + DATA.topicOrder[next];
  }

  // ---- keyboard shortcuts ----------------------------------------------
  function initShortcuts() {
    document.addEventListener("keydown", function (e) {
      var tag = (e.target.tagName || "").toLowerCase();
      var typing = tag === "input" || tag === "textarea";
      if (e.key === "/" && !typing) { e.preventDefault(); document.getElementById("search").focus(); return; }
      if (typing) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "j") { e.preventDefault(); neighbor(1); }
      else if (e.key === "k") { e.preventDefault(); neighbor(-1); }
      else if (e.key === "[") { e.preventDefault(); toggleSidebar(); }
      else if (e.key === "t") { toggleTheme(); }
    });
  }

  function toggleSidebar() { document.getElementById("app").classList.toggle("sidebar-collapsed"); }

  // ---- init -------------------------------------------------------------
  function init() {
    initTheme();
    renderSidebar();
    initSearch();
    initShortcuts();
    initProgressBar();
    document.getElementById("theme-toggle").addEventListener("click", toggleTheme);
    document.getElementById("sidebar-toggle").addEventListener("click", toggleSidebar);
    window.addEventListener("hashchange", route);
    route();
  }

  init();
})();
