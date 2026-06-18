// demo-seed.js — 데모용 가짜 활동을 서버로 흘려보낸다 (대시보드가 살아있는 모습을 즉시 확인).
// 사용: 서버를 켠 상태에서  node demo-seed.js
const http = require("http");
const PORT = process.env.VRIN_PORT || 9777;

function post(obj) {
  const body = JSON.stringify(obj);
  const req = http.request({ host: "127.0.0.1", port: PORT, path: "/event", method: "POST",
    headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(body) } });
  req.on("error", () => {});
  req.write(body); req.end();
}

const SID = "demo" + Math.floor(Date.now() / 100000 % 100000);
const scenario = [
  { event: "UserPromptSubmit" },
  { event: "PreToolUse", tool_name: "Task", tool_input: { subagent_type: "cos", description: "요청 라우팅" } },
  { event: "PreToolUse", tool_name: "Task", tool_input: { subagent_type: "hr-disability", description: "장애인 직무발굴" } },
  { event: "PreToolUse", tool_name: "Read", tool_input: { file_path: "기업조사.md" } },
  { event: "PreToolUse", tool_name: "WebSearch", tool_input: { query: "장애인 표준사업장 직무 사례" } },
  { event: "PreToolUse", tool_name: "Task", tool_input: { subagent_type: "res-web", description: "딥리서치" } },
  { event: "PreToolUse", tool_name: "Write", tool_input: { file_path: "직무후보군.xlsx" } },
  { event: "PreToolUse", tool_name: "Task", tool_input: { subagent_type: "del-report", description: "보고서 편집" } },
  { event: "PreToolUse", tool_name: "Task", tool_input: { subagent_type: "bar", description: "품질검증" } },
  { event: "Stop" },
];

let i = 0;
console.log("데모 활동 전송 시작 (서버가 켜져 있어야 합니다)…");
const timer = setInterval(() => {
  if (i >= scenario.length) { clearInterval(timer); console.log("데모 완료 — 브라우저를 확인하세요."); return; }
  post({ ...scenario[i], session_id: SID, ts: Date.now() });
  i++;
}, 700);
