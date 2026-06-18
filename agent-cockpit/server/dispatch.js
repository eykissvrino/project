// dispatch.js — 대시보드에서 cos 비서(Claude Code)에게 일을 시킨다.
// claude -p (헤드리스)를 안전하게 spawn. 진행상황은 워크스페이스 hook이 실시간 피드로 흘려보냄.
const { spawn, execSync } = require("child_process");
const crypto = require("crypto");
const path = require("path");
const { HUB } = require("./roster");

// 프로젝트 지정 시 cos 비서에게 주입하는 폴더 규칙 (VRIN_PROJECT_STANDARD §2.1)
function folderRule(project) {
  return [
    `[작업 폴더 규칙] 작업 대상 프로젝트: projects/${project}`,
    `산출물은 반드시 이 프로젝트의 표준 폴더에 저장한다:`,
    `- 작업 중 초안·시안 → 03_작업실`,
    `- 최종 납품본 → 04_산출물`,
    `- 구버전·폐기 → 05_보관`,
    `새 최상위 번호폴더(예: 10_xxx) 생성 금지. 프로젝트 루트에 작업파일을 흩뿌리지 말 것.`,
    `세부 폴더는 한글 '번호_이름' 형식(예: 01_제안). 폴더가 모호하면 03_작업실 아래 적절한 한글 폴더를 만든다.`,
  ].join("\n");
}

const jobs = [];          // 최신이 앞 (unshift)
const MAX_JOBS = 60;
let onUpdate = () => {};
function setJobListener(fn) { onUpdate = fn; }

// claude 실행파일 절대경로 (shell 미사용 → 프롬프트 인젝션 방지)
let _bin = null;
function claudeBin() {
  if (_bin) return _bin;
  try {
    const cmd = process.platform === "win32" ? "where claude" : "which claude";
    _bin = execSync(cmd, { encoding: "utf8" }).split(/\r?\n/).map((s) => s.trim()).filter(Boolean)
      .find((p) => /claude(\.exe|\.cmd)?$/i.test(p)) || "claude";
  } catch { _bin = "claude"; }
  return _bin;
}

const MODES = new Set(["plan", "acceptEdits", "bypassPermissions", "default", "dontAsk"]);

function dispatch({ prompt, agent, mode, model, project }) {
  prompt = String(prompt || "").trim();
  if (!prompt) throw new Error("지시 내용이 비어 있습니다");
  mode = MODES.has(mode) ? mode : "plan";
  const sessionUuid = crypto.randomUUID();
  const job = {
    id: sessionUuid.slice(0, 8), sessionId: sessionUuid.slice(0, 12),
    prompt, agent: agent || "", project: project || "", mode, status: "running",
    result: "", cost: 0, startTs: Date.now(), endTs: 0,
  };
  jobs.unshift(job);
  if (jobs.length > MAX_JOBS) jobs.pop();
  onUpdate(job);

  const args = ["-p", prompt, "--output-format", "json",
    "--permission-mode", mode, "--add-dir", HUB, "--session-id", sessionUuid];
  if (agent) args.push("--agent", agent);
  if (model) args.push("--model", model);
  if (project) {
    args.push("--add-dir", path.join(HUB, "projects", project));
    args.push("--append-system-prompt", folderRule(project));
  }

  let child;
  try {
    // 대시보드 서버가 Claude Code 세션 안에서 떠 있으면 CLAUDECODE를 물려받아
    // 중첩 세션 차단에 걸린다 → 자식 claude에는 이 변수를 넘기지 않는다.
    const env = { ...process.env };
    // 부모 Claude Code 세션의 흔적을 모두 제거 → 자식 claude가 독립 세션으로 실행되도록.
    // (대시보드를 Claude Code 안에서 띄운 경우의 중첩/인증 충돌 방지. 일반 터미널에선 영향 없음)
    for (const k of Object.keys(env)) {
      if (/^CLAUDE/.test(k) || k === "ANTHROPIC_BASE_URL" || k === "AI_AGENT") delete env[k];
    }
    child = spawn(claudeBin(), args, { cwd: HUB, env, windowsHide: true, stdio: ["ignore", "pipe", "pipe"] });
  } catch (e) {
    finish(job, "error", "Claude 실행 실패: " + e.message);
    return job;
  }
  let out = "", err = "";
  child.stdout.on("data", (d) => { out += d; if (out.length > 4e6) child.kill(); });
  child.stderr.on("data", (d) => { err += d; });
  child.on("error", (e) => finish(job, "error", "Claude 실행 실패: " + e.message));
  child.on("close", (code) => {
    let result = "", cost = 0, isErr = code !== 0;
    try {
      const j = JSON.parse(out);
      result = j.result || j.text || JSON.stringify(j).slice(0, 200);
      cost = j.total_cost_usd || j.cost_usd || 0;
      isErr = j.is_error || isErr;
    } catch {
      result = (out || err || "(출력 없음)").trim().slice(0, 6000);
    }
    job.cost = cost;
    finish(job, isErr ? "error" : "done", result.slice(0, 8000));
  });
  return job;
}

function finish(job, status, result) {
  job.status = status; job.result = result; job.endTs = Date.now();
  onUpdate(job);
}

function listJobs() { return jobs; }

module.exports = { dispatch, listJobs, setJobListener };
