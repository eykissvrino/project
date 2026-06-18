// app.js — VRIN 에이전트 관제탑 프론트엔드 (의존성 0)
const $ = (s) => document.querySelector(s);
const $$ = (s) => document.querySelectorAll(s);
let ROSTER = [], BYNAME = {}, ACTIVITY = {};

const MAIN = { name: "main", emoji: "🎛️", role: "메인 세션 (대표님↔관제탑)", color: "#5b8cff", dept: "메인", avatar: null };
function agent(name) { return BYNAME[name] || (name === "main" ? MAIN : { name, emoji: "🧠", role: name, color: "#8b94a8", avatar: null }); }
function ago(ts) {
  const s = Math.floor((Date.now() - ts) / 1000);
  if (s < 5) return "방금"; if (s < 60) return s + "초 전";
  const m = Math.floor(s / 60); if (m < 60) return m + "분 전";
  const h = Math.floor(m / 60); if (h < 24) return h + "시간 전";
  return Math.floor(h / 24) + "일 전";
}
function clock(ts){const d=new Date(ts);return ("0"+d.getHours()).slice(-2)+":"+("0"+d.getMinutes()).slice(-2)+":"+("0"+d.getSeconds()).slice(-2);}
function avaHTML(a, cls) {
  const inner = a.avatar ? `<img src="${a.avatar}" alt="">` : a.emoji;
  return `<div class="${cls}" style="--avbg:${a.color}26;background:${a.color}1f">${inner}</div>`;
}

// ── 탭 전환 ──
$$(".tab").forEach((t) => t.addEventListener("click", () => {
  $$(".tab").forEach((x) => x.classList.remove("active"));
  $$(".panel").forEach((x) => x.classList.remove("active"));
  t.classList.add("active");
  $("#tab-" + t.dataset.tab).classList.add("active");
  if (t.dataset.tab === "sessions") loadSessions();
  if (t.dataset.tab === "projects") loadProjects();
  if (t.dataset.tab === "dispatch") loadJobs();
}));

// ── 데이터 로드 ──
async function loadRoster() {
  try {
    const r = await fetch("/api/roster").then((x) => x.json());
    ROSTER = r.agents; ACTIVITY = r.activity || {};
    BYNAME = Object.fromEntries(ROSTER.map((a) => [a.name, a]));
    renderGallery(); renderNow();
  } catch {
    setTimeout(loadRoster, 1500); // 서버 기동 대기 후 재시도
  }
}
async function loadStats() {
  try {
    const s = await fetch("/api/stats").then((x) => x.json());
    renderKPIs(s);
    $("#footStat").textContent = `누적 이벤트 ${s.totalEvents} · 세션 ${s.sessionsCount} · 에이전트 ${s.rosterSize}명`;
  } catch {}
}
function renderKPIs(s) {
  const live = s.activeAgents.length;
  const kpis = [
    { v: live, l: "지금 작동 중", c: live ? "#22c55e" : "#5d6678" },
    { v: s.eventsToday, l: "오늘 활동 수", c: "#5b8cff" },
    { v: s.sessionsCount, l: "세션 수", c: "#a855f7" },
    { v: Object.keys(s.agentsUsed).length, l: "투입된 에이전트", c: "#f59e0b" },
    { v: s.rosterSize, l: "전체 직원(에이전트)", c: "#14b8a6" },
  ];
  $("#kpis").innerHTML = kpis.map((k) => `<div class="kpi" style="--kc:${k.c}"><div class="v" style="color:${k.c}">${k.v}</div><div class="l">${k.l}</div></div>`).join("");
}

// ── 실시간 피드 ──
const feed = $("#feed"); let feedCount = 0;
function pushFeed(e) {
  const a = agent(e.actor);
  const li = document.createElement("li");
  li.innerHTML = `${avaHTML(a, "ava")}<div class="txt"><div class="who" style="color:${a.color}">${a.name === "main" ? "관제탑" : a.name}</div><div class="sum">${esc(e.summary)}</div></div><span class="t">${clock(e.ts)}</span>`;
  feed.prepend(li);
  if (++feedCount > 120) feed.lastChild && feed.removeChild(feed.lastChild);
}
function esc(s){return String(s==null?"":s).replace(/[<>&]/g,(c)=>({"<":"&lt;",">":"&gt;","&":"&amp;"}[c]));}

// ── 지금 일하는 중 ──
function renderNow() {
  const now = Date.now();
  const live = Object.entries(ACTIVITY)
    .filter(([n, x]) => n !== "main" && now - x.lastTs < 90000)
    .sort((a, b) => b[1].lastTs - a[1].lastTs);
  const el = $("#nowList");
  if (!live.length) { el.innerHTML = `<div class="empty">대기 중 — 에이전트가 작동하면 여기 나타납니다.</div>`; return; }
  el.innerHTML = live.map(([n, x]) => {
    const a = agent(n);
    return `<div class="now-item"><div class="ring"></div>${avaHTML(a, "ava")}<div><div class="nm" style="color:${a.color}">${a.name}</div><div class="ds">${esc(x.lastSummary || a.role)}</div></div></div>`;
  }).join("");
}

// ── 에이전트 갤러리 ──
function renderGallery(filter = "") {
  const f = filter.trim().toLowerCase();
  const now = Date.now();
  const isLive = (a) => ACTIVITY[a.name] && now - ACTIVITY[a.name].lastTs < 90000;
  const match = (a) => !f || (a.name + a.role + a.dept + a.description).toLowerCase().includes(f);

  const liveCount = ROSTER.filter(isLive).length;
  const matchCount = ROSTER.filter(match).length;
  $("#galleryCount").textContent = `${matchCount} / ${ROSTER.length}명` + (liveCount ? ` · 🟢 작동중 ${liveCount}` : "");

  const card = (a) => {
    const live = isLive(a);
    const cnt = ACTIVITY[a.name] ? ACTIVITY[a.name].count : 0;
    return `<div class="org-card${live ? " live" : ""}${match(a) ? "" : " dim"}" style="--ac:${a.color}" data-name="${a.name}">
      ${live ? '<span class="oc-pulse"></span>' : ""}
      ${avaHTML(a, "oc-ava")}
      <div class="oc-nm" style="color:${a.color}">${a.name}</div>
      <div class="oc-rl">${esc(a.role)}</div>
      ${live ? '<span class="oc-live">● 작동중</span>' : (cnt ? `<span class="oc-cnt">활동 ${cnt}</span>` : "")}
    </div>`;
  };

  const cos = ROSTER.find((a) => a.name === "cos");
  const govRest = ROSTER.filter((a) => a.deptKey === "gov" && a.name !== "cos"); // bar, clo
  const deptKeys = [...new Set(ROSTER.filter((a) => a.deptKey !== "gov").map((a) => a.deptKey))];

  const deptBoxes = deptKeys.map((dk) => {
    const arr = ROSTER.filter((a) => a.deptKey === dk);
    const dc = arr[0].deptColor;
    const lead = arr.find((a) => a.isLead) || arr[0];
    const members = arr.filter((a) => a !== lead);
    const liveInDept = arr.filter(isLive).length;
    return `<div class="dept-box" style="--dc:${dc}">
      <div class="dept-box-head">
        <div class="dept-label">${esc(lead.dept)}${liveInDept ? `<span class="dept-live">🟢 ${liveInDept}</span>` : ""}</div>
        ${card(lead)}
      </div>
      ${members.length ? `<div class="dept-members">${members.map(card).join("")}</div>` : ""}
    </div>`;
  }).join("");

  $("#gallery").innerHTML = `
    <div class="org-tree">
      <div class="org-ceo">
        <div class="oc-ava ceo-ava">🏢</div>
        <div class="oc-nm">VRIN · 이석주 대표</div>
        <div class="oc-rl">AI 컨설팅 컴퍼니 · 직원 ${ROSTER.length}명</div>
      </div>
      <div class="org-stem"></div>
      <div class="org-tier-label">비서실장 · 관제탑</div>
      <div class="org-gov org-cos">${cos ? card(cos) : ""}</div>
      <div class="org-stem"></div>
      <div class="org-tier-label">거버넌스 (품질·진화)</div>
      <div class="org-gov">${govRest.map(card).join("")}</div>
      <div class="org-stem"></div>
      <div class="org-tier-label">7개 부서 · 부장과 팀원</div>
      <div class="org-depts">${deptBoxes}</div>
    </div>`;

  $$("#gallery .org-card[data-name]").forEach((el) => el.addEventListener("click", () => openModal(el.dataset.name)));
}
$("#agentSearch").addEventListener("input", (e) => renderGallery(e.target.value));

// ── 모달 ──
function openModal(name) {
  const a = agent(name);
  const act = ACTIVITY[name];
  $("#modalBox").innerHTML = `
    <div class="mhead">${avaHTML(a, "ava")}<div><h3 style="color:${a.color}">${a.name}${a.isLead ? ' <span class="lead-badge" style="background:'+a.color+'">리드</span>' : ""}</h3><div class="mrole">${esc(a.dept)}</div></div></div>
    <div class="mdesc">${esc(a.description || a.role)}</div>
    <div class="mtags"><span class="mtag">모델: ${a.model}</span><span class="mtag">누적 활동 ${act ? act.count : 0}회</span>${act ? '<span class="mtag">최근 ' + ago(act.lastTs) + "</span>" : '<span class="mtag">아직 미투입</span>'}</div>
    <button class="mclose">닫기</button>`;
  $("#modal").classList.remove("hidden");
  $(".mclose").onclick = () => $("#modal").classList.add("hidden");
}
$("#modal").addEventListener("click", (e) => { if (e.target.id === "modal") $("#modal").classList.add("hidden"); });

// ── 세션 ──
async function loadSessions() {
  const r = await fetch("/api/sessions").then((x) => x.json());
  const el = $("#sessions");
  if (!r.sessions.length) { el.innerHTML = `<div class="empty">아직 기록된 세션이 없습니다.</div>`; return; }
  el.innerHTML = r.sessions.map((s) => {
    const actors = Object.keys(s.actors).sort((a, b) => s.actors[b] - s.actors[a]);
    const avs = actors.slice(0, 8).map((n) => avaHTML(agent(n), "miniava")).join("") || '<span class="hint">메인 세션</span>';
    const topTools = Object.entries(s.tools).sort((a, b) => b[1] - a[1]).slice(0, 3).map(([t, c]) => `${t}×${c}`).join(" · ");
    const dur = Math.max(1, Math.round((s.last - s.start) / 60000));
    return `<div class="sess"><div class="sid">#${s.id}</div><div class="smid"><div style="font-size:12.5px;color:var(--mut)">${topTools || "활동 기록"}</div><div class="sactors">${avs}</div></div><div class="sstat"><b>${s.count}</b>활동 · ${dur}분<br>${ago(s.last)}</div></div>`;
  }).join("");
}

// ── 프로젝트 칸반 + 결과물 ──
const PHASES = ["대기·비활성", "1 Frame 착수", "2 Plan 기획", "3 Produce 생산", "4 Critique 검토", "5 Validate 검증", "6 Deliver 납품", "7 Learn 학습"];
const PSTAT = { green: ["#22c55e", "정상"], amber: ["#f59e0b", "주의"], red: ["#ef4444", "지연"], dropped: ["#5d6678", "비활성"], "": ["#5d6678", "-"] };
let PROJECTS = [];

async function loadProjects() {
  try {
    const r = await fetch("/api/projects").then((x) => x.json());
    PROJECTS = r.projects || [];
    renderKanban();
  } catch { $("#kanban").innerHTML = `<div class="empty">프로젝트를 불러오지 못했습니다.</div>`; }
}

function renderKanban() {
  const active = PROJECTS.filter((p) => p.status !== "dropped" && p.phase > 0);
  $("#projCount").textContent = `프로젝트 ${PROJECTS.length}개 · 활성 ${active.length}개`;
  const cols = PHASES.map((_, i) => PROJECTS.filter((p) => (p.status === "dropped" || p.phase === 0) ? i === 0 : p.phase === i));
  $("#kanban").innerHTML = PHASES.map((label, i) => {
    const items = cols[i];
    const cards = items.map(projCard).join("") || `<div class="kan-empty">—</div>`;
    return `<div class="kan-col${i === 0 ? " kan-col-idle" : ""}">
      <div class="kan-head">${esc(label)} <span class="kan-n">${items.length}</span></div>
      <div class="kan-body">${cards}</div>
    </div>`;
  }).join("");
  $$("#kanban .kan-card[data-folder]").forEach((el) => el.addEventListener("click", () => openProject(el.dataset.folder, el.dataset.project)));
}

function projCard(p) {
  const [sc, sl] = PSTAT[p.status] || PSTAT[""];
  const squad = p.squad.slice(0, 5).map((s) => `<span class="kan-chip">${esc(s)}</span>`).join("");
  return `<div class="kan-card" data-folder="${esc(p.folder)}" data-project="${esc(p.project)}" style="--sc:${sc}">
    <div class="kan-title">${esc(p.project)}</div>
    <div class="kan-cli">${esc(p.client)}${p.type ? " · " + esc(p.type) : ""}</div>
    <div class="kan-bar"><span style="width:${Math.max(3, p.progress)}%;background:${sc}"></span></div>
    <div class="kan-meta">
      <span class="kan-stat" style="color:${sc}">● ${sl} ${p.progress}%</span>
      ${p.deliverableCount ? `<span class="kan-deliv">📎 ${p.deliverableCount}</span>` : ""}
    </div>
    ${p.lead || squad ? `<div class="kan-squad"><span class="kan-lead">${esc(p.lead)}</span>${squad}</div>` : ""}
    ${p.next ? `<div class="kan-next">▸ ${esc(p.next)}</div>` : ""}
    ${p.due ? `<div class="kan-due">📅 ${esc(p.due)}</div>` : ""}
  </div>`;
}

const EXT_ICON = { ".docx": "📄", ".pdf": "📕", ".pptx": "📊", ".pptm": "📊", ".xlsx": "📗", ".xls": "📗",
  ".hwp": "📃", ".hwpx": "📃", ".html": "🌐", ".md": "📝", ".csv": "📈", ".png": "🖼️", ".jpg": "🖼️", ".txt": "📄" };

async function openProject(folder, project) {
  $("#modalBox").innerHTML = `<h3>📋 ${esc(project)}</h3><div class="mrole" style="margin:4px 0 14px">${esc(folder)}</div><div class="empty">결과물 불러오는 중…</div>`;
  $("#modal").classList.remove("hidden");
  let files = [];
  try { files = (await fetch("/api/deliverables?folder=" + encodeURIComponent(folder)).then((x) => x.json())).files || []; } catch {}
  const list = files.length ? files.map((f) => {
    const ic = EXT_ICON[f.ext] || "📎";
    const kb = f.size > 1048576 ? (f.size / 1048576).toFixed(1) + "MB" : Math.max(1, Math.round(f.size / 1024)) + "KB";
    return `<div class="deliv" data-path="${esc(f.path)}">
      <span class="deliv-ic">${ic}</span>
      <span class="deliv-nm">${esc(f.name)}${f.isDeliverable ? ' <span class="deliv-tag">산출물</span>' : ""}<div class="deliv-rel">${esc(f.rel)}</div></span>
      <span class="deliv-sz">${kb}</span>
    </div>`;
  }).join("") : `<div class="empty">결과물 파일이 없습니다.</div>`;
  $("#modalBox").innerHTML = `<h3>📋 ${esc(project)}</h3><div class="mrole" style="margin:4px 0 12px">${esc(folder)} · 결과물 ${files.length}개 (클릭하면 열림)</div>
    <div class="deliv-list">${list}</div><button class="mclose">닫기</button>`;
  $(".mclose").onclick = () => $("#modal").classList.add("hidden");
  $$("#modalBox .deliv[data-path]").forEach((el) => el.addEventListener("click", () => openFile(el.dataset.path, el)));
}

async function openFile(p, el) {
  if (el) { el.classList.add("opening"); }
  try {
    const r = await fetch("/open?path=" + encodeURIComponent(p)).then((x) => x.json());
    if (el) { el.classList.remove("opening"); el.classList.add(r.ok ? "opened" : "failed"); setTimeout(() => el.classList.remove("opened", "failed"), 1500); }
  } catch { if (el) { el.classList.remove("opening"); el.classList.add("failed"); } }
}

// ── 일 시키기 (cos 비서 ③) ──
let JOBS = [];
let dispatchInit = false;
async function initDispatch() {
  if (dispatchInit || !ROSTER.length) return; dispatchInit = true;
  $("#dpAgent").innerHTML = '<option value="">자동 (cos 비서가 판단)</option>' +
    ROSTER.map((a) => `<option value="${a.name}">${a.emoji} ${a.name} — ${esc(a.role).slice(0, 22)}</option>`).join("");
  try {
    const ps = (await fetch("/api/projects").then((x) => x.json())).projects || [];
    $("#dpProject").innerHTML = '<option value="">(지정 안 함 · 워크스페이스 전체)</option>' +
      ps.filter((p) => p.status !== "dropped").map((p) => `<option value="${esc(p.folder)}">${esc(p.project)}</option>`).join("");
  } catch {}
  $("#dpMode").addEventListener("change", (e) => {
    const w = $("#dpWarn");
    if (e.target.value === "bypassPermissions") { w.textContent = "⚠️ 제한 없음 — 파일 수정·명령 실행이 확인 없이 자동 진행됩니다."; w.className = "dp-warn danger"; }
    else if (e.target.value === "acceptEdits") { w.textContent = "✏️ 파일 작성이 자동 허용됩니다 (명령 실행은 제한)."; w.className = "dp-warn"; }
    else { w.textContent = ""; w.className = "dp-warn"; }
  });
  $("#dpRun").addEventListener("click", runDispatch);
}
async function runDispatch() {
  const prompt = $("#dpPrompt").value.trim();
  if (!prompt) { $("#dpPrompt").focus(); return; }
  const body = { prompt, agent: $("#dpAgent").value, mode: $("#dpMode").value, project: $("#dpProject").value };
  const btn = $("#dpRun"); btn.disabled = true; btn.textContent = "전송 중…";
  try {
    const r = await fetch("/api/dispatch", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then((x) => x.json());
    if (r.ok) { $("#dpPrompt").value = ""; upsertJob(r.job); }
    else alert("실행 실패: " + (r.error || ""));
  } catch (e) { alert("전송 실패: " + e.message); }
  btn.disabled = false; btn.textContent = "▶ 실행";
}
async function loadJobs() {
  initDispatch();
  try { JOBS = (await fetch("/api/jobs").then((x) => x.json())).jobs || []; renderJobs(); } catch {}
}
function upsertJob(job) {
  const i = JOBS.findIndex((j) => j.id === job.id);
  if (i >= 0) JOBS[i] = job; else JOBS.unshift(job);
  renderJobs();
}
const JOBST = { running: ["#f59e0b", "⏳ 진행 중"], done: ["#22c55e", "✅ 완료"], error: ["#ef4444", "⚠️ 실패"] };
function renderJobs() {
  const el = $("#jobs"); if (!el) return;
  if (!JOBS.length) { el.innerHTML = `<div class="empty">아직 지시한 작업이 없습니다. 위에 지시를 입력하고 ▶ 실행을 눌러보세요.</div>`; return; }
  el.innerHTML = JOBS.map((j) => {
    const [c, l] = JOBST[j.status] || JOBST.running;
    const who = j.agent ? agent(j.agent).emoji + " " + j.agent : "🧭 cos 비서";
    const dur = j.endTs ? Math.max(1, Math.round((j.endTs - j.startTs) / 1000)) + "초" : ago(j.startTs);
    const res = j.status === "running"
      ? `<div class="job-run">실행 중… 진행상황은 ⚡실시간 활동 탭에서 볼 수 있습니다.</div>`
      : `<div class="job-res">${esc(j.result)}</div>`;
    return `<div class="job s-${j.status}" data-id="${j.id}">
      <div class="job-head"><span class="job-who">${who}</span><span class="job-st" style="color:${c}">${l}</span></div>
      <div class="job-prompt">${esc(j.prompt)}</div>
      <div class="job-meta">${j.project ? "📁 " + esc(j.project) + " · " : ""}권한 ${esc(j.mode)} · ${dur}${j.cost ? " · $" + Number(j.cost).toFixed(3) : ""}</div>
      ${res}
    </div>`;
  }).join("");
  $$("#jobs .job").forEach((el2) => el2.addEventListener("click", () => el2.classList.toggle("expanded")));
}

// ── SSE 실시간 연결 ──
function connect() {
  const es = new EventSource("/api/stream");
  es.onopen = () => { $("#conn").className = "conn on"; $("#connTxt").textContent = "실시간 연결됨"; };
  es.onerror = () => { $("#conn").className = "conn off"; $("#connTxt").textContent = "재연결 중…"; };
  es.onmessage = (m) => {
    let e; try { e = JSON.parse(m.data); } catch { return; }
    if (e._type === "job") { upsertJob(e); return; }
    pushFeed(e);
    // 활동 갱신
    const a = ACTIVITY[e.actor] || (ACTIVITY[e.actor] = { lastTs: 0, count: 0, lastSummary: "" });
    a.lastTs = e.ts; a.count++; a.lastSummary = e.summary;
    renderNow();
    if ($("#tab-agents").classList.contains("active")) renderGallery($("#agentSearch").value);
  };
}

// ── 부팅 ──
loadRoster(); loadStats(); connect();
setInterval(loadStats, 5000);
setInterval(renderNow, 5000);
setInterval(() => { if ($("#tab-agents").classList.contains("active")) renderGallery($("#agentSearch").value); }, 8000);
