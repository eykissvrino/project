// projects.js — projects/*/00_관리/_현황.md 파싱 + 산출물(결과물) 파일 스캔.
// 의존성 0. 칸반 데이터와 "결과물 클릭→열기"의 소스.
const fs = require("fs");
const path = require("path");
const { HUB } = require("./roster");

const PROJ = path.join(HUB, "projects");
// 결과물로 볼 확장자
const DELIVER_EXT = new Set([".docx", ".pptx", ".pptm", ".xlsx", ".xls", ".pdf",
  ".hwp", ".hwpx", ".html", ".md", ".csv", ".png", ".jpg", ".key", ".txt"]);
// 스캔 제외 폴더
// 결과물 탭이므로 입력자료·리서치자료·관리·보관은 제외 (실제 만든 산출물만)
const SKIP_DIR = new Set([".git", "node_modules", ".claude", ".omc", ".gstack",
  "00_관리", "01_입력자료", "02_지식리서치", "05_보관", "_screenshots", "data"]);
const SKIP_FILE = new Set(["CLAUDE.md", "AGENTS.md", "README.md", ".gitignore"]);

function parseFM(filePath) {
  let txt;
  try { txt = fs.readFileSync(filePath, "utf8"); } catch { return null; }
  const m = txt.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!m) return null;
  const fm = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":");
    if (i === -1) continue;
    fm[line.slice(0, i).trim()] = line.slice(i + 1).trim().replace(/^["']|["']$/g, "");
  }
  return fm;
}

function parseSquad(s) {
  if (!s) return [];
  return s.replace(/[\[\]]/g, "").split(",").map((x) => x.trim().replace(/^["']|["']$/g, "")).filter(Boolean);
}

function loadProjects() {
  let dirs = [];
  try { dirs = fs.readdirSync(PROJ, { withFileTypes: true }).filter((d) => d.isDirectory()); } catch { return []; }
  const out = [];
  for (const d of dirs) {
    const dir = path.join(PROJ, d.name);
    const fm = parseFM(path.join(dir, "00_관리", "_현황.md")) || {};
    out.push({
      folder: d.name,
      project: fm.project || d.name,
      client: fm.client || "",
      type: fm.type || "",
      phase: parseInt(fm.phase) || 0,
      status: fm.status || "green",
      lead: fm.lead || "",
      squad: parseSquad(fm.squad),
      progress: parseInt(fm.progress) || 0,
      next: fm.next || "",
      due: fm.due || "",
      updated: fm.updated || "",
      deliverableCount: countDeliverables(dir),
    });
  }
  // 활성(phase 높은) 우선, 비활성 뒤로
  out.sort((a, b) => (b.phase - a.phase) || a.folder.localeCompare(b.folder));
  return out;
}

function countDeliverables(dir) {
  let n = 0;
  walk(dir, 0, (f) => { n++; });
  return n;
}

function listDeliverables(folder, limit = 80) {
  const base = path.join(PROJ, folder);
  const norm = path.resolve(base);
  if (!norm.startsWith(path.resolve(PROJ))) return []; // 경로 탈출 방지
  const files = [];
  walk(base, 0, (f) => files.push(f));
  files.sort((a, b) => (b.isDeliverable - a.isDeliverable) || b.mtime - a.mtime);
  return files.slice(0, limit);
}

function walk(dir, depth, cb, base) {
  base = base || dir;
  if (depth > 4) return;
  let ents;
  try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch { return; }
  for (const e of ents) {
    if (e.isDirectory()) {
      if (SKIP_DIR.has(e.name) || e.name.startsWith(".")) continue;
      walk(path.join(dir, e.name), depth + 1, cb, base);
    } else {
      const ext = path.extname(e.name).toLowerCase();
      if (!DELIVER_EXT.has(ext)) continue;
      if (e.name.startsWith("_") || e.name.startsWith("~$")) continue; // _현황.md, 임시파일 제외
      if (SKIP_FILE.has(e.name)) continue; // 프로젝트 설정 문서 제외
      const fp = path.join(dir, e.name);
      let st;
      try { st = fs.statSync(fp); } catch { continue; }
      cb({
        name: e.name,
        path: fp,
        rel: path.relative(base, fp),
        folder: path.relative(PROJ, fp).split(path.sep)[0],
        ext,
        size: st.size,
        mtime: st.mtimeMs,
        isDeliverable: fp.includes(path.sep + "04_산출물" + path.sep),
      });
    }
  }
}

// 파일을 OS 기본 앱으로 열기 (Windows). 워크스페이스 내부만 허용.
function openPath(p) {
  const full = path.resolve(p);
  if (!full.startsWith(path.resolve(HUB))) throw new Error("forbidden");
  if (!fs.existsSync(full)) throw new Error("not found");
  const { spawn } = require("child_process");
  if (process.platform === "win32") {
    spawn("cmd", ["/c", "start", "", full], { detached: true, stdio: "ignore" }).unref();
  } else {
    spawn(process.platform === "darwin" ? "open" : "xdg-open", [full], { detached: true, stdio: "ignore" }).unref();
  }
}

module.exports = { loadProjects, listDeliverables, openPath, PROJ };
