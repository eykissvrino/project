// roster.js — _core/agents/v2/*.md 프론트매터를 읽어 43명 에이전트 캐릭터 명단을 만든다.
// 의존성 0 (Node 내장 fs/path만 사용).
const fs = require("fs");
const path = require("path");

const HUB = path.resolve(__dirname, "..", "..");
const AGENTS_DIR = path.join(HUB, "_core", "agents", "v2");
const AVATAR_DIR = path.join(__dirname, "..", "public", "avatars");

// 부서 정의: 이름 접두어 → 부서 메타
const DEPTS = {
  gov: { code: "거버넌스", color: "#8b5cf6", order: 0 },
  str: { code: "@STR 전략기획부", color: "#6366f1", order: 1 },
  hr: { code: "@HR HR컨설팅부", color: "#14b8a6", order: 2 },
  res: { code: "@RES 리서치부", color: "#0ea5e9", order: 3 },
  pt: { code: "@PT 제품기술부", color: "#a855f7", order: 4 },
  gtm: { code: "@GTM 그로스부", color: "#f59e0b", order: 5 },
  del: { code: "@DEL 딜리버리부", color: "#ec4899", order: 6 },
  leg: { code: "@LEG 법무리스크부", color: "#64748b", order: 7 },
};

// Tailwind 계열 색상명 → hex (프론트매터 color 필드용)
const COLOR_HEX = {
  slate: "#64748b", gray: "#6b7280", zinc: "#71717a", red: "#ef4444",
  orange: "#f97316", amber: "#f59e0b", yellow: "#eab308", lime: "#84cc16",
  green: "#22c55e", emerald: "#10b981", teal: "#14b8a6", cyan: "#06b6d4",
  sky: "#0ea5e9", blue: "#3b82f6", indigo: "#6366f1", violet: "#8b5cf6",
  purple: "#a855f7", fuchsia: "#d946ef", pink: "#ec4899", rose: "#f43f5e",
};

// 에이전트별 이모지 (아바타 일러스트 없을 때 캐릭터 대체)
const EMOJI = {
  cos: "🧭", bar: "🛡️", clo: "🦉",
  str: "♟️", "str-strategy": "🎯", "str-finance": "💰", "str-newbiz": "🚀",
  hr: "🧑‍💼", "hr-skills": "🧩", "hr-disability": "♿", "hr-culture": "🌱",
  "hr-org": "🏛️", "hr-perf": "📈", "hr-learn": "📚", "hr-analytics": "📊", "hr-aix": "🤖",
  res: "🔬", "res-web": "🌐", "res-market": "📡", "res-data": "📉", "res-wiki": "📖",
  pt: "🛠️", "pt-pm": "🗺️", "pt-ai": "🧠", "pt-be": "⚙️", "pt-fe": "🎨",
  "pt-mobile": "📱", "pt-devops": "🚢", "pt-qa": "🔍", "pt-game": "🎮",
  gtm: "📣", "gtm-brand": "✨", "gtm-content": "✍️", "gtm-proposal": "📑", "gtm-sales": "🤝",
  del: "🎬", "del-report": "📄", "del-deck": "🎞️", "del-visual": "🖌️",
  leg: "⚖️", "leg-contract": "📜", "leg-labor": "👷", "leg-compliance": "🔒",
};

function deptOf(name) {
  if (["cos", "bar", "clo"].includes(name)) return "gov";
  const pre = name.split("-")[0];
  return DEPTS[pre] ? pre : "gov";
}

function parseFrontmatter(text) {
  const m = text.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!m) return null;
  const fm = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":");
    if (i === -1) continue;
    const k = line.slice(0, i).trim();
    let v = line.slice(i + 1).trim().replace(/^["']|["']$/g, "");
    fm[k] = v;
  }
  return fm;
}

function loadRoster() {
  let files = [];
  try {
    files = fs.readdirSync(AGENTS_DIR).filter((f) => f.endsWith(".md"));
  } catch (e) {
    return [];
  }
  const agents = [];
  for (const f of files) {
    let txt;
    try { txt = fs.readFileSync(path.join(AGENTS_DIR, f), "utf8"); } catch { continue; }
    const fm = parseFrontmatter(txt);
    if (!fm || !fm.name) continue;
    const name = fm.name;
    const dk = deptOf(name);
    const dept = DEPTS[dk];
    const isLead = name === dk || ["cos", "bar", "clo"].includes(name);
    // 아바타 파일 자동 인식 (png/jpg/webp)
    let avatar = null;
    for (const ext of [".png", ".jpg", ".jpeg", ".webp", ".svg"]) {
      if (fs.existsSync(path.join(AVATAR_DIR, name + ext))) { avatar = "avatars/" + name + ext; break; }
    }
    agents.push({
      name,
      role: (fm.description || "").split(/[.。]/)[0].slice(0, 80),
      description: fm.description || "",
      model: fm.model || "sonnet",
      color: COLOR_HEX[fm.color] || dept.color,
      colorName: fm.color || "",
      dept: dept.code,
      deptKey: dk,
      deptColor: dept.color,
      deptOrder: dept.order,
      isLead,
      emoji: EMOJI[name] || "🧠",
      avatar,
    });
  }
  agents.sort((a, b) => a.deptOrder - b.deptOrder || (b.isLead - a.isLead) || a.name.localeCompare(b.name));
  return agents;
}

module.exports = { loadRoster, DEPTS, HUB };
