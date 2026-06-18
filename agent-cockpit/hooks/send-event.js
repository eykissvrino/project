// send-event.js — Claude Code hook → 대시보드 서버로 이벤트 전송 (fire-and-forget)
// settings.json hooks에서 호출: node "<경로>/send-event.js" <EventName>
// 설계 원칙: 절대 블로킹/에러로 Claude를 방해하지 않는다. 서버가 꺼져있으면 조용히 통과.
const http = require("http");

const PORT = process.env.VRIN_PORT || 9777;
const eventArg = process.argv[2] || "";

let input = "";
process.stdin.on("data", (c) => (input += c));
process.stdin.on("end", () => {
  let data = {};
  try { data = JSON.parse(input || "{}"); } catch {}
  const payload = JSON.stringify({
    ts: Date.now(),
    event: eventArg || data.hook_event_name || "Event",
    session_id: data.session_id,
    tool_name: data.tool_name,
    tool_input: data.tool_input,
    cwd: data.cwd,
  });
  const req = http.request(
    { host: "127.0.0.1", port: PORT, path: "/event", method: "POST",
      headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(payload) } },
    (res) => { res.on("data", () => {}); res.on("end", () => process.exit(0)); }
  );
  req.on("error", () => process.exit(0)); // 서버 꺼짐 등 → 조용히 종료
  req.setTimeout(400, () => { req.destroy(); process.exit(0); });
  req.write(payload);
  req.end();
});
// stdin이 없을 때 대비 (안전장치)
setTimeout(() => process.exit(0), 800);
