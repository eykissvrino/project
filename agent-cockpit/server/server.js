// server.js — VRIN 에이전트 대시보드 로컬 서버 (외부 의존성 0, Node 내장만)
// 실행: node server/server.js   또는 START-대시보드.bat 더블클릭
const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");
const { loadRoster } = require("./roster");
const { loadProjects, listDeliverables, openPath } = require("./projects");
const { dispatch, listJobs, setJobListener } = require("./dispatch");

const PORT = process.env.VRIN_PORT || 9777;
const HOST = "127.0.0.1";
const ROOT = path.resolve(__dirname, "..");
const PUBLIC = path.join(ROOT, "public");
const DATA = path.join(ROOT, "data");
if (!fs.existsSync(DATA)) fs.mkdirSync(DATA, { recursive: true });

let ROSTER = loadRoster();
const rosterByName = () => Object.fromEntries(ROSTER.map((a) => [a.name, a]));

// ── 인메모리 이벤트 버퍼 ─────────────────────────────────────────
const MAX_BUFFER = 3000;
const events = []; // 최신이 뒤
const activity = {}; // name -> {lastTs, count, lastSummary, sessions:Set}
const sseClients = new Set();

function todayFile() {
  const d = new Date();
  const ymd = d.getFullYear() + ("0" + (d.getMonth() + 1)).slice(-2) + ("0" + d.getDate()).slice(-2);
  return path.join(DATA, `events-${ymd}.jsonl`);
}

function loadTodayFromDisk() {
  try {
    const f = todayFile();
    if (!fs.existsSync(f)) return;
    const lines = fs.readFileSync(f, "utf8").trim().split("\n").slice(-MAX_BUFFER);
    for (const ln of lines) {
      if (!ln.trim()) continue;
      try { ingest(JSON.parse(ln), false); } catch {}
    }
  } catch {}
}

const MODELS_TXT = { opus: "Opus", sonnet: "Sonnet", haiku: "Haiku" };

function summarize(e) {
  const t = e.tool_name || "";
  if (t === "Task" || t === "Agent") {
    const sub = e.subagent_type || "에이전트";
    return e.event === "PreToolUse" ? `🚀 ${sub} 호출` : `✅ ${sub} 완료`;
  }
  if (e.event === "UserPromptSubmit") return "💬 대표님 지시 수신";
  if (e.event === "SessionStart") return "🟢 세션 시작";
  if (e.event === "Stop") return "⏹️ 응답 완료";
  if (e.event === "SubagentStop") return "✅ 서브에이전트 종료";
  if (e.event === "Notification") return "🔔 알림";
  const map = { Read: "📖 파일 읽기", Write: "✍️ 파일 작성", Edit: "✏️ 파일 수정",
    Bash: "💻 명령 실행", Glob: "🔎 파일 탐색", Grep: "🔍 코드 검색",
    WebSearch: "🌐 웹 검색", WebFetch: "🌐 웹 수집", TodoWrite: "📝 할일 갱신" };
  return (map[t] || "⚙️ " + (t || e.event || "활동")) + (e.target ? ` · ${e.target}` : "");
}

// 행위자(에이전트) 판정: Task 도구면 subagent_type, 아니면 메인 세션
function actorOf(e) {
  if ((e.tool_name === "Task" || e.tool_name === "Agent") && e.subagent_type) return e.subagent_type;
  return "cos"; // 메인 세션 = 비서실장(@CoS, 라우터·PMO·관제탑)이 직접 수행하는 활동
}

function ingest(raw, persist = true) {
  const e = {
    ts: raw.ts || Date.now(),
    event: raw.event || raw.hook_event_name || "Event",
    session_id: (raw.session_id || "main").toString().slice(0, 12),
    tool_name: raw.tool_name || "",
    subagent_type: raw.subagent_type || (raw.tool_input && raw.tool_input.subagent_type) || "",
    target: raw.target || (raw.tool_input && shortTarget(raw.tool_input)) || "",
    cwd: raw.cwd || "",
  };
  e.actor = actorOf(e);
  e.summary = summarize(e);
  events.push(e);
  if (events.length > MAX_BUFFER) events.shift();

  // 활동 집계
  const a = activity[e.actor] || (activity[e.actor] = { lastTs: 0, count: 0, lastSummary: "", sessions: {} });
  a.lastTs = e.ts; a.count++; a.lastSummary = e.summary; a.sessions[e.session_id] = e.ts;

  if (persist) {
    try { fs.appendFileSync(todayFile(), JSON.stringify(e) + "\n"); } catch {}
    broadcast(e);
  }
  return e;
}

function shortTarget(ti) {
  if (!ti || typeof ti !== "object") return "";
  if (ti.file_path) return path.basename(ti.file_path);
  if (ti.pattern) return ti.pattern;
  if (ti.command) return String(ti.command).slice(0, 40);
  if (ti.query) return String(ti.query).slice(0, 40);
  if (ti.description) return String(ti.description).slice(0, 40);
  return "";
}

function broadcast(e) {
  const payload = `data: ${JSON.stringify(e)}\n\n`;
  for (const res of sseClients) { try { res.write(payload); } catch {} }
}

// 지시(dispatch) 작업 상태 변화를 실시간으로 대시보드에 전송
setJobListener((job) => broadcast({ _type: "job", ...job }));

// ── 세션/통계 집계 ───────────────────────────────────────────────
function sessions() {
  const map = {};
  for (const e of events) {
    const s = map[e.session_id] || (map[e.session_id] = {
      id: e.session_id, start: e.ts, last: e.ts, count: 0, actors: {}, tools: {},
    });
    s.last = e.ts; s.count++;
    if (e.actor && e.actor !== "main") s.actors[e.actor] = (s.actors[e.actor] || 0) + 1;
    if (e.tool_name) s.tools[e.tool_name] = (s.tools[e.tool_name] || 0) + 1;
  }
  return Object.values(map).sort((a, b) => b.last - a.last);
}

function stats() {
  const now = Date.now();
  const ACTIVE_MS = 90 * 1000;
  const liveActors = Object.entries(activity)
    .filter(([n, a]) => n !== "main" && now - a.lastTs < ACTIVE_MS)
    .map(([n]) => n);
  const today = events.filter((e) => now - e.ts < 24 * 3600 * 1000);
  const agentsUsed = {};
  for (const e of events) if (e.actor !== "main") agentsUsed[e.actor] = (agentsUsed[e.actor] || 0) + 1;
  return {
    totalEvents: events.length,
    eventsToday: today.length,
    activeAgents: liveActors,
    sessionsCount: sessions().length,
    agentsUsed,
    rosterSize: ROSTER.length,
    lastEventTs: events.length ? events[events.length - 1].ts : 0,
  };
}

// ── HTTP 라우팅 ──────────────────────────────────────────────────
const MIME = { ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
  ".webp": "image/webp", ".svg": "image/svg+xml", ".ico": "image/x-icon" };

function sendJSON(res, obj, code = 200) {
  res.writeHead(code, { "Content-Type": "application/json; charset=utf-8", "Access-Control-Allow-Origin": "*" });
  res.end(JSON.stringify(obj));
}

function serveStatic(res, reqPath) {
  let rel = decodeURIComponent(reqPath.split("?")[0]);
  if (rel === "/" || rel === "") rel = "/index.html";
  const fp = path.join(PUBLIC, path.normalize(rel).replace(/^(\.\.[/\\])+/, ""));
  if (!fp.startsWith(PUBLIC)) { res.writeHead(403); return res.end("forbidden"); }
  fs.readFile(fp, (err, buf) => {
    if (err) { res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" }); return res.end("404"); }
    res.writeHead(200, { "Content-Type": MIME[path.extname(fp)] || "application/octet-stream" });
    res.end(buf);
  });
}

const server = http.createServer((req, res) => {
  const u = url.parse(req.url, true);
  const p = u.pathname;

  // 이벤트 수신 (hook이 POST)
  if (req.method === "POST" && p === "/event") {
    let body = "";
    req.on("data", (c) => { body += c; if (body.length > 1e6) req.destroy(); });
    req.on("end", () => {
      try { ingest(JSON.parse(body || "{}")); } catch {}
      res.writeHead(204); res.end();
    });
    return;
  }

  // 지시 수신 (대시보드 → cos 비서)
  if (req.method === "POST" && p === "/api/dispatch") {
    let body = "";
    req.on("data", (c) => { body += c; if (body.length > 1e6) req.destroy(); });
    req.on("end", () => {
      try { const job = dispatch(JSON.parse(body || "{}")); sendJSON(res, { ok: true, job }); }
      catch (e) { sendJSON(res, { ok: false, error: String(e.message || e) }, 400); }
    });
    return;
  }

  // 실시간 스트림 (SSE)
  if (p === "/api/stream") {
    res.writeHead(200, {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache", Connection: "keep-alive", "Access-Control-Allow-Origin": "*",
    });
    res.write(`retry: 3000\n\n`);
    // 최근 60건 즉시 전송
    for (const e of events.slice(-60)) res.write(`data: ${JSON.stringify(e)}\n\n`);
    sseClients.add(res);
    const hb = setInterval(() => { try { res.write(": hb\n\n"); } catch {} }, 25000);
    req.on("close", () => { clearInterval(hb); sseClients.delete(res); });
    return;
  }

  if (p === "/api/jobs") return sendJSON(res, { jobs: listJobs() });
  if (p === "/api/projects") return sendJSON(res, { projects: loadProjects() });
  if (p === "/api/deliverables") return sendJSON(res, { files: listDeliverables(u.query.folder || "") });
  if (p === "/open") {
    try { openPath(u.query.path || ""); return sendJSON(res, { ok: true }); }
    catch (e) { return sendJSON(res, { ok: false, error: String(e.message || e) }, 400); }
  }
  if (p === "/api/roster") return sendJSON(res, { agents: ROSTER, activity });
  if (p === "/api/events") {
    const lim = Math.min(parseInt(u.query.limit) || 200, MAX_BUFFER);
    return sendJSON(res, { events: events.slice(-lim).reverse() });
  }
  if (p === "/api/sessions") return sendJSON(res, { sessions: sessions() });
  if (p === "/api/stats") return sendJSON(res, stats());
  if (p === "/api/reload") { ROSTER = loadRoster(); return sendJSON(res, { ok: true, size: ROSTER.length }); }

  serveStatic(res, req.url);
});

loadTodayFromDisk();
server.listen(PORT, HOST, () => {
  console.log("\n  ╔════════════════════════════════════════════════╗");
  console.log("  ║   VRIN 에이전트 대시보드 가동                    ║");
  console.log("  ╠════════════════════════════════════════════════╣");
  console.log(`  ║   브라우저에서 열기:  http://${HOST}:${PORT}    `);
  console.log(`  ║   에이전트 명단: ${ROSTER.length}명 로드됨`);
  console.log("  ║   종료: 이 창에서 Ctrl + C                       ║");
  console.log("  ╚════════════════════════════════════════════════╝\n");
});
