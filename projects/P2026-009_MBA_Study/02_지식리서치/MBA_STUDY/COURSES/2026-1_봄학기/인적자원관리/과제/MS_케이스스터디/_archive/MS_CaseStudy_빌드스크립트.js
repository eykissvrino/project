const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.defineLayout({ name: "A4L", width: 11.69, height: 8.27 });
pres.layout = "A4L";
pres.author = "이석주";
pres.title = "Satya Nadella at Microsoft — Building a Growth Culture";

const NAVY = "1F3864", NAVY2 = "2B4A7A", BLUE = "2E5BBA", BLUEL = "EAF0FA";
const RED = "C0392B", REDL = "FBEEEC", GRAY = "5A6478", LGRAY = "F4F5F8";
const MGRAY = "D6D9E0", INK = "1F2433", WHITE = "FFFFFF";
const GRN = "2F8F4E", GRNL = "EDF5EF", AMBER = "B8862F", AMBERL = "FAF3E4";
const HEAD = "맑은 고딕", BODY = "맑은 고딕";
const PW = 11.69, PH = 8.27, ML = 0.55, CW = 10.59;

const shC = () => ({ type: "outer", color: "9AA2B1", blur: 5, offset: 1.5, angle: 135, opacity: 0.15 });
const shS = () => ({ type: "outer", color: "9AA2B1", blur: 3, offset: 1, angle: 135, opacity: 0.10 });
let pageNo = 0;

function body(s, cat, sub, nav1, nav2) {
  s.background = { color: WHITE };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.13, h: PH, fill: { color: NAVY } });
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 0.4, w: 0.08, h: 0.44, fill: { color: RED } });
  s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.08, y: 0.4, w: 1.78, h: 0.44, fill: { color: NAVY } });
  s.addText(cat, { x: ML + 0.08, y: 0.4, w: 1.78, h: 0.44, align: "center", valign: "middle", color: WHITE, bold: true, fontSize: 11.5, fontFace: HEAD, margin: 0 });
  s.addText(sub, { x: ML + 2.0, y: 0.4, w: 6.0, h: 0.44, valign: "middle", color: GRAY, fontSize: 11.5, fontFace: BODY, margin: 0 });
  s.addText([
    { text: nav1, options: { breakLine: true, color: BLUE, bold: true } },
    { text: nav2, options: { color: "9BA3B4" } },
  ], { x: 8.7, y: 0.38, w: 2.44, h: 0.48, align: "right", fontSize: 8.5, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.1 });
}
function govmsg(s, runs) {
  const arr = runs.map((r) => ({ text: r.t, options: { color: r.b ? BLUE : NAVY, bold: true } }));
  s.addText(arr, { x: ML, y: 0.96, w: CW, h: 0.5, fontSize: 15.5, fontFace: HEAD, margin: 0, valign: "middle" });
  s.addShape(pres.shapes.LINE, { x: ML, y: 1.5, w: CW, h: 0, line: { color: NAVY, width: 1.5 } });
}
function footer(s, src) {
  pageNo++;
  if (src) s.addText(src, { x: ML, y: 7.92, w: 8.2, h: 0.26, fontSize: 7, color: "9BA3B4", fontFace: BODY, margin: 0 });
  s.addText("Microsoft Case Study · HRM #7", { x: 8.0, y: 7.92, w: 3.0, h: 0.26, fontSize: 7, color: MGRAY, fontFace: BODY, align: "right", margin: 0 });
  s.addText(String(pageNo).padStart(2, "0"), { x: 11.05, y: 7.88, w: 0.45, h: 0.28, fontSize: 9, color: NAVY, bold: true, fontFace: BODY, align: "right", margin: 0 });
}
function takeaway(s, text, y) {
  const yy = y || 7.36;
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: yy, w: CW, h: 0.46, fill: { color: NAVY } });
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: yy, w: 0.07, h: 0.46, fill: { color: RED } });
  s.addText([
    { text: "핵심 메시지    ", options: { bold: true, color: "8FA3CC", fontFace: BODY } },
    { text: text, options: { color: WHITE, fontFace: BODY } },
  ], { x: ML + 0.22, y: yy, w: CW - 0.4, h: 0.46, fontSize: 10, valign: "middle", margin: 0 });
}
function card(s, x, y, w, h, fill, soft) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill || WHITE }, line: { color: MGRAY, width: 1 }, shadow: soft ? shS() : shC() });
}
function secthdr(s, x, y, w, txt, col) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.36, fill: { color: col || NAVY } });
  s.addText(txt, { x: x + 0.12, y, w: w - 0.2, h: 0.36, fontSize: 10, color: WHITE, bold: true, fontFace: BODY, valign: "middle", margin: 0 });
}
function quote(s, x, y, w, h, txt, src, dark) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: dark ? NAVY : LGRAY } });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h, fill: { color: dark ? RED : BLUE } });
  s.addText([
    { text: txt + "\n", options: { italic: true, color: dark ? WHITE : INK, fontSize: 9.5 } },
    { text: src, options: { color: dark ? "8FA3CC" : GRAY, fontSize: 8 } },
  ], { x: x + 0.18, y, w: w - 0.32, h, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.18 });
}
function divider(num, kr, en, items) {
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: PW, h: 0.11, fill: { color: RED } });
  s.addText(num, { x: 0.86, y: 0.5, w: 7.0, h: 2.7, fontSize: 150, color: NAVY2, bold: true, fontFace: HEAD, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 0.99, y: 3.66, w: 1.9, h: 0, line: { color: RED, width: 3 } });
  s.addText(en.toUpperCase(), { x: 0.99, y: 3.78, w: 9, h: 0.34, fontSize: 11.5, color: "7E8CAE", bold: true, charSpacing: 3, fontFace: BODY, margin: 0 });
  s.addText(kr, { x: 0.99, y: 4.14, w: 10.2, h: 0.9, fontSize: 30, color: WHITE, bold: true, fontFace: HEAD, margin: 0 });
  if (items) {
    let iy = 5.4;
    items.forEach((it) => {
      s.addShape(pres.shapes.RECTANGLE, { x: 1.01, y: iy + 0.05, w: 0.12, h: 0.12, fill: { color: RED } });
      s.addText(it, { x: 1.27, y: iy, w: 10, h: 0.32, fontSize: 11.5, color: "C7CFE0", fontFace: BODY, margin: 0 });
      iy += 0.44;
    });
  }
  s.addText("Microsoft Case Study", { x: 8.0, y: 7.85, w: 3.0, h: 0.3, fontSize: 7.5, color: NAVY2, fontFace: BODY, align: "right", margin: 0 });
  pageNo++;
  s.addText(String(pageNo).padStart(2, "0"), { x: 11.05, y: 7.84, w: 0.45, h: 0.28, fontSize: 9, color: "8190B5", bold: true, fontFace: BODY, align: "right", margin: 0 });
  return s;
}
// reusable Competing Values 2x2 — pos: null | 'asis' | 'tobe'
function cvfQuad(s, qx, qy, qw, qh, mode) {
  const hw = qw / 2, hh = qh / 2;
  const asisOn = mode === "asis" || mode === "tobe";
  const tobeOn = mode === "tobe";
  const quads = [
    ["Clan  관계", "협력·팀워크·인재개발", qx, qy, tobeOn ? "E4EEE7" : "EEF1F6", tobeOn ? GRN : "9098A8"],
    ["Adhocracy  혁신", "창의·모험·기업가정신", qx + hw, qy, tobeOn ? "E4EEE7" : "EEF1F6", tobeOn ? GRN : "9098A8"],
    ["Hierarchy  위계", "규칙·절차·통제·효율", qx, qy + hh, asisOn && !tobeOn ? REDL : (mode === "concept" ? "EEF1F6" : "F2F3F5"), asisOn && !tobeOn ? RED : "9098A8"],
    ["Market  시장", "경쟁·성과·결과지향", qx + hw, qy + hh, asisOn && !tobeOn ? REDL : (mode === "concept" ? "EEF1F6" : "F2F3F5"), asisOn && !tobeOn ? RED : "9098A8"],
  ];
  quads.forEach((q) => {
    s.addShape(pres.shapes.RECTANGLE, { x: q[2], y: q[3], w: hw, h: hh, fill: { color: q[4] }, line: { color: WHITE, width: 2 } });
    s.addText(q[0], { x: q[2] + 0.1, y: q[3] + 0.09, w: hw - 0.18, h: 0.3, fontSize: 10.5, color: q[5], bold: true, fontFace: HEAD, margin: 0 });
    s.addText(q[1], { x: q[2] + 0.1, y: q[3] + 0.38, w: hw - 0.18, h: 0.3, fontSize: 7.8, color: q[5], fontFace: BODY, margin: 0 });
  });
  // axis labels
  s.addText("유연성 · 재량", { x: qx, y: qy - 0.26, w: qw, h: 0.22, fontSize: 8.5, color: NAVY, bold: true, align: "center", fontFace: BODY, margin: 0 });
  s.addText("안정성 · 통제", { x: qx, y: qy + qh + 0.04, w: qw, h: 0.22, fontSize: 8.5, color: NAVY, bold: true, align: "center", fontFace: BODY, margin: 0 });
  s.addText("내부\n지향", { x: qx - 0.54, y: qy + hh - 0.22, w: 0.48, h: 0.44, fontSize: 8, color: NAVY, bold: true, align: "center", valign: "middle", fontFace: BODY, margin: 0, lineSpacingMultiple: 0.9 });
  s.addText("외부\n지향", { x: qx + qw + 0.06, y: qy + hh - 0.22, w: 0.48, h: 0.44, fontSize: 8, color: NAVY, bold: true, align: "center", valign: "middle", fontFace: BODY, margin: 0, lineSpacingMultiple: 0.9 });
  // markers
  if (mode === "asis") {
    s.addShape(pres.shapes.OVAL, { x: qx + qw * 0.62, y: qy + qh * 0.72, w: 0.4, h: 0.4, fill: { color: RED }, line: { color: WHITE, width: 2 } });
    s.addText("As-Is", { x: qx + qw * 0.62 - 0.3, y: qy + qh * 0.72 + 0.42, w: 1.0, h: 0.24, fontSize: 8.5, color: RED, bold: true, align: "center", fontFace: BODY, margin: 0 });
  }
  if (mode === "tobe") {
    s.addShape(pres.shapes.OVAL, { x: qx + qw * 0.62, y: qy + qh * 0.72, w: 0.36, h: 0.36, fill: { color: "E2B6B1" }, line: { color: WHITE, width: 1.5 } });
    s.addText("As-Is", { x: qx + qw * 0.62 - 0.25, y: qy + qh * 0.72 + 0.36, w: 0.9, h: 0.22, fontSize: 7.5, color: "A86A62", bold: true, align: "center", fontFace: BODY, margin: 0 });
    s.addShape(pres.shapes.OVAL, { x: qx + qw * 0.22, y: qy + qh * 0.2, w: 0.42, h: 0.42, fill: { color: GRN }, line: { color: WHITE, width: 2 } });
    s.addText("To-Be", { x: qx + qw * 0.22 - 0.28, y: qy + qh * 0.2 - 0.26, w: 0.98, h: 0.24, fontSize: 8.5, color: GRN, bold: true, align: "center", fontFace: BODY, margin: 0 });
    s.addShape(pres.shapes.LINE, { x: qx + qw * 0.64, y: qy + qh * 0.74, w: -(qw * 0.4), h: -(qh * 0.5), line: { color: NAVY, width: 2.5, endArrowType: "triangle", dashType: "dash" } });
  }
}

// ====================== S1 COVER ======================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 3.85, h: PH, fill: { color: NAVY } });
  s.addShape("triangle", { x: 3.05, y: -0.5, w: 1.6, h: 1.6, rotate: 180, fill: { color: NAVY2 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 3.85, h: 0.11, fill: { color: RED } });
  s.addShape(pres.shapes.RECTANGLE, { x: 3.85, y: 0, w: 0.055, h: PH, fill: { color: RED } });
  s.addText("CASE\nSTUDY\n#7", { x: 0.5, y: 2.35, w: 3.1, h: 2.5, fontSize: 38, color: WHITE, bold: true, fontFace: HEAD, margin: 0, lineSpacingMultiple: 1.0 });
  s.addShape(pres.shapes.LINE, { x: 0.56, y: 4.85, w: 1.4, h: 0, line: { color: RED, width: 3 } });
  s.addText("조직문화와 변화관리\nOrganizational Culture & Change", { x: 0.56, y: 5.0, w: 3.1, h: 0.9, fontSize: 11.5, color: "AEB9D3", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.2 });
  s.addText("HUMAN RESOURCE MANAGEMENT", { x: 4.35, y: 1.5, w: 7.0, h: 0.4, fontSize: 11.5, color: BLUE, bold: true, charSpacing: 2, fontFace: BODY, margin: 0 });
  s.addText("Satya Nadella\nat Microsoft", { x: 4.32, y: 1.95, w: 7.2, h: 1.8, fontSize: 42, color: NAVY, bold: true, fontFace: HEAD, margin: 0, lineSpacingMultiple: 1.0 });
  s.addText("나델라는 어떻게 조직문화를 다시 세웠는가", { x: 4.35, y: 3.6, w: 7.2, h: 0.5, fontSize: 18, color: GRAY, italic: true, fontFace: HEAD, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 4.35, y: 4.32, w: 2.3, h: 0.04, fill: { color: NAVY } });
  s.addText("케이스 서사로 따라가는 문화 변혁 — 위기·각성·경청·선언·구현·변화, 그리고 그 후", { x: 4.35, y: 4.46, w: 7.0, h: 0.4, fontSize: 11.5, color: INK, fontFace: BODY, margin: 0 });
  card(s, 4.35, 5.16, 6.95, 1.5, LGRAY, true);
  const meta = [
    ["분석 대상", "Microsoft Corp.  ·  London Business School Case LBS128 (2018)"],
    ["과     목", "인적자원관리 (정혜정 교수)  ·  대학원 MBA 인사조직 전공"],
    ["발  표  자", "이석주   |   2026. 5. 16"],
  ];
  let my = 5.3;
  meta.forEach((m) => {
    s.addText(m[0], { x: 4.58, y: my, w: 1.5, h: 0.4, fontSize: 10, color: BLUE, bold: true, fontFace: BODY, valign: "middle", margin: 0 });
    s.addText(m[1], { x: 6.1, y: my, w: 5.0, h: 0.4, fontSize: 10, color: INK, fontFace: BODY, valign: "middle", margin: 0 });
    my += 0.42;
  });
  s.addText("건국대학교 경영대학원 MBA", { x: 4.35, y: 6.82, w: 7, h: 0.32, fontSize: 9, color: GRAY, bold: true, fontFace: BODY, margin: 0 });
  pageNo++;
}

// ====================== S2 CONTENTS ======================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.13, h: PH, fill: { color: NAVY } });
  s.addText("Contents", { x: ML, y: 0.46, w: 3.0, h: 0.7, fontSize: 31, color: NAVY, bold: true, fontFace: HEAD, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 3.35, y: 0.82, w: 7.79, h: 0, line: { color: NAVY, width: 2.5 } });
  s.addText("나델라의 조직문화 구축 서사 — 8개 PART의 흐름", { x: ML, y: 1.04, w: 8, h: 0.3, fontSize: 10, color: GRAY, italic: true, fontFace: BODY, margin: 0 });
  const toc = [
    ["01", "위기", "\"잃어버린 10년\" — 게이츠·발머 시대의 전략·HR 제도·문화", "05"],
    ["02", "각성", "한 리더의 '공감' — 나델라와 성장 마인드셋의 씨앗", "12"],
    ["03", "경청", "진단으로서의 첫 1년 — 인터뷰·포커스그룹·\"왜 존재하는가\"", "15"],
    ["04", "선언", "\"Know-it-all에서 Learn-it-all로\" — 새 미션과 3대 Pillar", "18"],
    ["05", "구현", "문화를 일상에 심다 — 제도 재설계·솔선수범·넛지", "23"],
    ["06", "변화", "퀸 모델로 확인하는 문화의 이동 — 성과와 미해결 과제", "30"],
    ["07", "그 후", "케이스 이후, 현재까지 (2018→2026) — 2025년 대량 정리해고", "34"],
    ["08", "시사점 & 토론", "전략·제도·문화의 정합성, 실무 시사점, 그리고 토론", "38"],
  ];
  let ty = 1.42;
  toc.forEach((t) => {
    card(s, ML, ty, CW, 0.74, WHITE, true);
    s.addShape(pres.shapes.RECTANGLE, { x: ML, y: ty, w: 0.86, h: 0.74, fill: { color: NAVY } });
    s.addText(t[0], { x: ML, y: ty, w: 0.86, h: 0.74, fontSize: 19, color: WHITE, bold: true, fontFace: HEAD, align: "center", valign: "middle", margin: 0 });
    s.addText(t[1], { x: ML + 1.06, y: ty, w: 2.0, h: 0.74, fontSize: 14, color: NAVY, bold: true, fontFace: HEAD, valign: "middle", margin: 0 });
    s.addShape(pres.shapes.LINE, { x: ML + 3.05, y: ty + 0.16, w: 0, h: 0.42, line: { color: MGRAY, width: 1 } });
    s.addText(t[2], { x: ML + 3.25, y: ty, w: 6.2, h: 0.74, fontSize: 9.7, color: GRAY, fontFace: BODY, valign: "middle", margin: 0 });
    s.addText("p." + t[3], { x: ML + CW - 0.95, y: ty, w: 0.82, h: 0.74, fontSize: 11.5, color: BLUE, bold: true, fontFace: BODY, align: "right", valign: "middle", margin: 0 });
    ty += 0.82;
  });
  footer(s, "");
}

// ====================== S3 STORYLINE ======================
{
  const s = pres.addSlide();
  body(s, "발표 개요", "스토리라인 — 케이스 서사를 따라가는 7막의 흐름", "발표 개요", "분석 Storyline");
  govmsg(s, [{ t: "본 발표는 케이스의 서사를 " }, { t: "'위기 → 각성 → 경청 → 선언 → 구현 → 변화 → 그 후'", b: true }, { t: "로 따라간다" }]);
  const arc = [
    ["01", "위기", "영혼을 잃은 회사", RED],
    ["02", "각성", "한 리더의 '공감'", NAVY],
    ["03", "경청", "진단으로서의 1년", NAVY],
    ["04", "선언", "Learn-it-all 선언", BLUE],
    ["05", "구현", "문화를 일상에 심다", BLUE],
    ["06", "변화", "퀸 모델로 본 이동", GRN],
    ["07", "그 후", "케이스 이후의 역설", AMBER],
  ];
  const aw = 1.4, ag = 0.115;
  let ax = ML;
  arc.forEach((a, i) => {
    card(s, ax, 1.74, aw, 1.62);
    s.addShape(pres.shapes.RECTANGLE, { x: ax, y: 1.74, w: aw, h: 0.46, fill: { color: a[3] } });
    s.addText(a[0] + "  " + a[1], { x: ax, y: 1.74, w: aw, h: 0.46, fontSize: 9.5, color: WHITE, bold: true, align: "center", valign: "middle", fontFace: HEAD, margin: 0 });
    s.addText(a[2], { x: ax + 0.06, y: 2.26, w: aw - 0.12, h: 1.0, fontSize: 9, color: INK, align: "center", valign: "middle", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.12 });
    if (i < 6) s.addText("▶", { x: ax + aw - 0.02, y: 1.74, w: 0.13, h: 1.62, fontSize: 8, color: MGRAY, align: "center", valign: "middle", margin: 0 });
    ax += aw + ag;
  });
  // Quinn spine
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 3.62, w: CW, h: 1.46, fill: { color: NAVY } });
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 3.62, w: 0.07, h: 1.46, fill: { color: RED } });
  s.addText("분석의 척추 — Cameron & Quinn 경쟁가치모형(CVF)", { x: ML + 0.22, y: 3.74, w: 7, h: 0.3, fontSize: 11, color: WHITE, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "퀸 모델이 서사의 ", options: { color: "C7CFE0", fontSize: 10 } },
    { text: "양 끝을 잡는다", options: { color: WHITE, bold: true, fontSize: 10 } },
    { text: " — PART 1에서 As-Is 좌표(위계+시장)를 찍고, PART 6에서 To-Be(관계+혁신)로의 이동을 확인한다. '기존 문화가 어떻게 변했는가'를 하나의 좌표로 추적.", options: { color: "C7CFE0", fontSize: 10 } },
  ], { x: ML + 0.22, y: 4.06, w: CW - 0.5, h: 0.9, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });
  // analysis tools
  s.addText("그 외 분석 도구", { x: ML, y: 5.34, w: 4, h: 0.3, fontSize: 10, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  const th = [
    ["Carol Dweck Growth Mindset", "변화의 이론적 씨앗 — 고정형 vs 성장형"],
    ["성과평가 이론 — 상대·절대평가", "Stack Ranking(강제배분)의 진단과 재설계"],
    ["Kotter 8단계 · Schein 문화론", "변화관리 과정의 해석"],
    ["1차 자료의 적극 활용", "케이스 원문 + 나델라 『히트 리프레시』 직접 인용"],
  ];
  let tx = ML;
  th.forEach((t) => {
    card(s, tx, 5.66, 2.55, 1.5, LGRAY, true);
    s.addShape(pres.shapes.RECTANGLE, { x: tx, y: 5.66, w: 0.07, h: 1.5, fill: { color: BLUE } });
    s.addText([
      { text: t[0] + "\n", options: { bold: true, color: INK, fontSize: 9.3, breakLine: true } },
      { text: t[1], options: { color: GRAY, fontSize: 8.3 } },
    ], { x: tx + 0.16, y: 5.66, w: 2.32, h: 1.5, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.25 });
    tx += 2.68;
  });
  footer(s, "출처: LBS128 케이스 / 분석 프레임 — 케이스 서사 + 경쟁가치모형(CVF)");
}

// ====================== S4 QUINN MODEL CONCEPT ======================
{
  const s = pres.addSlide();
  body(s, "발표 개요", "분석의 척추 — Cameron & Quinn 경쟁가치모형이란", "발표 개요", "퀸 경쟁가치모형");
  govmsg(s, [{ t: "조직문화를 두 축으로 4유형으로 나누는 " }, { t: "'경쟁가치모형(Competing Values Framework)'", b: true }]);
  // left: 2x2
  cvfQuad(s, 1.35, 2.3, 4.4, 3.7, "concept");
  // right: explanation
  card(s, 6.2, 1.66, 4.94, 4.7, LGRAY);
  s.addText("개념 — 무엇을 보는 도구인가", { x: 6.4, y: 1.78, w: 4.6, h: 0.3, fontSize: 11, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "미시간대 Robert Quinn & Kim Cameron이 개발. 조직문화를 ", options: { color: INK, fontSize: 9.2 } },
    { text: "두 개의 가치 축", options: { color: BLUE, bold: true, fontSize: 9.2 } },
    { text: "으로 진단한다.\n", options: { color: INK, fontSize: 9.2 } },
    { text: "· 세로축 : 유연성·재량 ↔ 안정성·통제\n", options: { color: GRAY, fontSize: 8.7 } },
    { text: "· 가로축 : 내부 지향 ↔ 외부 지향\n", options: { color: GRAY, fontSize: 8.7 } },
    { text: "두 축이 만나 ", options: { color: INK, fontSize: 9.2 } },
    { text: "4가지 문화 유형", options: { color: BLUE, bold: true, fontSize: 9.2 } },
    { text: "이 나온다. '경쟁가치'란 협력 vs 경쟁처럼 동시에 추구하기 어려운 가치들의 긴장을 뜻한다.", options: { color: INK, fontSize: 9.2 } },
  ], { x: 6.4, y: 2.12, w: 4.62, h: 1.5, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });
  const types = [
    ["Clan (관계문화)", "가족적·협력적. 리더=멘토. 인재 개발과 몰입이 성공 기준", "9098A8"],
    ["Adhocracy (혁신문화)", "창의적·모험적. 리더=기업가. 혁신과 새 시도가 성공 기준", "9098A8"],
    ["Hierarchy (위계문화)", "공식적·구조적. 리더=조정자. 효율·안정·통제가 성공 기준", RED],
    ["Market (시장문화)", "경쟁적·성과중심. 리더=관리자. 실적·점유율이 성공 기준", RED],
  ];
  let ty = 3.74;
  types.forEach((t) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.4, y: ty, w: 0.08, h: 0.56, fill: { color: t[2] } });
    s.addText([
      { text: t[0] + "  ", options: { bold: true, color: INK, fontSize: 9.3 } },
      { text: t[1], options: { color: GRAY, fontSize: 8.6 } },
    ], { x: 6.56, y: ty, w: 4.46, h: 0.56, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.1 });
    ty += 0.62;
  });
  takeaway(s, "본 발표는 As-Is(위계+시장 고착) → To-Be(관계+혁신으로 이동)를 이 좌표 위에서 추적한다");
  footer(s, "출처: Cameron & Quinn, Diagnosing and Changing Organizational Culture (경쟁가치모형)");
}

// ====================== 01 DIVIDER ======================
divider("01", "위기 — \"잃어버린 10년\", 영혼을 잃은 회사", "Crisis", [
  "재무는 멀쩡한데 죽어가던 회사 — 게이츠·발머 시대의 전략과 의도",
  "전략을 떠받친 HR 제도(Stack Ranking)와 그것이 낳은 조직문화",
]);

// ====================== S6 LOST DECADE ======================
{
  const s = pres.addSlide();
  body(s, "01. 위기", "\"잃어버린 10년\" — 재무 성장과 시장 불신의 괴리", "01. 위기", "1. 잃어버린 10년");
  govmsg(s, [{ t: "매출은 3배 늘었지만 " }, { t: "주가는 10년간 정체", b: true }, { t: "했다 — 재무제표에 잡히지 않는 위기" }]);
  card(s, ML, 1.66, 4.95, 3.32);
  s.addText("Microsoft 주가 추이 (2000–2018)  ·  Exhibit 1", { x: ML + 0.18, y: 1.76, w: 4.6, h: 0.3, fontSize: 10, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addChart(pres.charts.LINE, [{ name: "주가($)", labels: ["'00", "'02", "'04", "'06", "'08", "'10", "'12", "'14", "'16", "'18"], values: [24, 26, 27, 28, 22, 26, 29, 38, 60, 95] }], {
    x: ML + 0.02, y: 2.08, w: 4.85, h: 2.72, lineSize: 2.75, lineSmooth: true, chartColors: [BLUE], chartArea: { fill: { color: WHITE } },
    catAxisLabelColor: GRAY, valAxisLabelColor: GRAY, catAxisLabelFontSize: 8, valAxisLabelFontSize: 8,
    valGridLine: { color: "ECEEF2", size: 0.5 }, catGridLine: { style: "none" }, showLegend: false, valAxisMaxVal: 100, valAxisMinVal: 0, lineDataSymbolSize: 4,
  });
  s.addText("◀ Ballmer 재임 — 10년 정체", { x: ML + 1.15, y: 4.32, w: 2.3, h: 0.24, fontSize: 8, color: RED, bold: true, fontFace: BODY, margin: 0 });
  s.addText("Nadella 이후 급등 ▶", { x: ML + 3.05, y: 2.32, w: 1.75, h: 0.24, fontSize: 8, color: BLUE, bold: true, fontFace: BODY, align: "right", margin: 0 });
  s.addText("'잃어버린 10년'의 5대 증상", { x: 5.78, y: 1.62, w: 6, h: 0.3, fontSize: 11, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  const sym = [
    ["핵심 인재 유출", "2004년부터 Google 등으로 이탈 — Google은 업계 평균 대비 +23% 보상"],
    ["시장 선점 기회 상실", "e-book(1998)·스마트폰 기술이 사내 정치 속에 \"killed or delayed\""],
    ["제품 경쟁 패배", "Bing은 Google 검색을, Zune은 iPod을 이기지 못함"],
    ["리더십 신뢰 붕괴", "Ballmer Glassdoor 지지율 29% (당시 Page 94%·Zuckerberg 99%)"],
    ["산업 트렌드 역행", "데스크톱→스마트폰 전환기에 Windows를 \"안전담요처럼\" 고수"],
  ];
  let sy = 1.96;
  sym.forEach((m, i) => {
    card(s, 5.78, sy, 5.36, 0.56, LGRAY, true);
    s.addShape(pres.shapes.OVAL, { x: 5.9, y: sy + 0.13, w: 0.3, h: 0.3, fill: { color: RED } });
    s.addText(String(i + 1), { x: 5.9, y: sy + 0.13, w: 0.3, h: 0.3, fontSize: 10, color: WHITE, bold: true, fontFace: HEAD, align: "center", valign: "middle", margin: 0 });
    s.addText([{ text: m[0] + "   ", options: { bold: true, color: INK } }, { text: m[1], options: { color: GRAY } }],
      { x: 6.32, y: sy, w: 4.72, h: 0.56, fontSize: 8.5, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.05 });
    sy += 0.64;
  });
  quote(s, ML, 5.18, CW, 0.62, "\"관료주의가 혁신을 대체했고, 사내 정치가 팀워크를 대신했다. 우리는 낙오했다.\"", "— Satya Nadella, 『히트 리프레시』 p19", true);
  takeaway(s, "주가는 미래 가치의 거울 — 시장은 재무제표가 아니라 '조직의 미래 역량'을 불신했다");
  footer(s, "출처: LBS128 케이스, Exhibit 1 / 『히트 리프레시』 p19");
}

// ====================== S7 GATES/BALLMER STRATEGY ======================
{
  const s = pres.addSlide();
  body(s, "01. 위기", "게이츠·발머의 경영전략과 그 '의도'", "01. 위기", "2. 기존 경영전략");
  govmsg(s, [{ t: "기존 경영진의 전략은 " }, { t: "'PC 시대의 지배를 지키는 것'", b: true }, { t: " — 그 의도가 조직을 빚었다" }]);
  // left: strategy timeline / intent
  card(s, ML, 1.66, 5.55, 2.5);
  secthdr(s, ML, 1.66, 5.55, "전략과 의도 — 무엇을 지키려 했는가", NAVY);
  const strat = [
    ["Gates의 창업 미션", "\"A computer on every desk and in every home\" — PC의 보편화. 한 시대를 지배한 명료한 비전"],
    ["Ballmer의 수성 전략 (2000–14)", "Windows·Office라는 '캐시카우'를 방어. 산업이 모바일·클라우드로 가는데 PC 프랜차이즈에 고착"],
    ["경영의 핵심 의도", "'책임(accountability)과 실적'의 극대화 — 정시 납기·숫자 달성이 모든 것에 우선. 개인 성과를 쥐어짜는 경영"],
  ];
  let sty = 2.16;
  strat.forEach((t) => {
    s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.18, y: sty + 0.04, w: 0.1, h: 0.1, fill: { color: BLUE } });
    s.addText(t[0], { x: ML + 0.36, y: sty - 0.04, w: 5.0, h: 0.3, fontSize: 9.8, color: NAVY, bold: true, fontFace: HEAD, margin: 0 });
    s.addText(t[1], { x: ML + 0.36, y: sty + 0.26, w: 5.05, h: 0.42, fontSize: 8.7, color: GRAY, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.12, valign: "top" });
    sty += 0.78;
  });
  // left bottom: paradox
  card(s, ML, 4.32, 5.55, 1.66, REDL);
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 4.32, w: 0.08, h: 1.66, fill: { color: RED } });
  s.addText("전략의 역설", { x: ML + 0.2, y: 4.42, w: 5, h: 0.3, fontSize: 9.5, color: RED, bold: true, fontFace: BODY, margin: 0 });
  s.addText("발머 재임 14년간 매출은 3배·이익은 2배 늘었다. 그러나 '수성'에 갇힌 전략은 모바일·클라우드 전환을 놓쳤고, '실적 압박'의 의도는 다음 장의 HR 제도(Stack Ranking)로 제도화되었다.", { x: ML + 0.2, y: 4.72, w: 5.2, h: 1.16, fontSize: 9.3, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });
  // right: intent -> system -> culture chain
  card(s, 6.3, 1.66, 4.84, 4.32, NAVY);
  s.addText("전략의 의도가 조직을 빚는 인과 사슬", { x: 6.5, y: 1.8, w: 4.5, h: 0.3, fontSize: 11, color: WHITE, bold: true, fontFace: BODY, margin: 0 });
  const chain = [
    ["전략 의도", "PC 시대 수성 + 책임·실적의 극대화", RED],
    ["HR 제도", "Stack Ranking — 개인을 줄 세우는 강제평가", AMBER],
    ["구성원 행동", "내부 경쟁·정치, 위험 회피", BLUE],
    ["조직문화", "사일로 + Know-it-all (과시의 문화)", "8FA3CC"],
  ];
  let cy = 2.24;
  chain.forEach((c, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.55, y: cy, w: 4.34, h: 0.6, fill: { color: "26406B" } });
    s.addShape(pres.shapes.RECTANGLE, { x: 6.55, y: cy, w: 0.07, h: 0.6, fill: { color: c[2] } });
    s.addText([
      { text: c[0] + "  —  ", options: { bold: true, color: WHITE, fontSize: 9.5 } },
      { text: c[1], options: { color: "C7CFE0", fontSize: 9 } },
    ], { x: 6.72, y: cy, w: 4.15, h: 0.6, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.05 });
    if (i < 3) s.addText("▼", { x: 6.55, y: cy + 0.6, w: 4.34, h: 0.24, fontSize: 9, color: "5A6F9A", align: "center", margin: 0 });
    cy += 0.84;
  });
  s.addText("→ 다음 장: 이 의도를 '제도'로 못박은 Stack Ranking", { x: 6.55, y: 5.62, w: 4.4, h: 0.3, fontSize: 8.7, color: "8FA3CC", italic: true, fontFace: BODY, margin: 0 });
  takeaway(s, "전략의 '의도'는 반드시 'HR 제도'로 번역된다 — 발머의 실적주의가 Stack Ranking을 낳았다");
  footer(s, "출처: LBS128 케이스 / 분석 — 전략 의도·HR 제도·문화의 인과 사슬");
}

// ====================== S8 STACK RANKING ======================
{
  const s = pres.addSlide();
  body(s, "01. 위기", "전략을 떠받친 HR 제도 — Stack Ranking", "01. 위기", "3. HR 제도");
  govmsg(s, [{ t: "Stack Ranking = " }, { t: "'상대평가 + 강제배분'", b: true }, { t: "의 결합 — GE 잭 웰치 'vitality curve' 계열" }]);
  card(s, ML, 1.66, 5.55, 3.5);
  s.addText("강제배분 — 직원을 5등급 칸에 '비율'로 끼워넣다", { x: ML + 0.18, y: 1.78, w: 5.2, h: 0.3, fontSize: 10, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText("각 등급의 인원 '비율'이 사전에 고정 — 실제 성과가 아니라 '분포'가 등급을 결정한다", { x: ML + 0.18, y: 2.1, w: 5.2, h: 0.34, fontSize: 8.5, color: GRAY, fontFace: BODY, margin: 0 });
  const segs = [["Top", 0.8, "F0F4FB", "1F4B86"], ["Good", 1.05, "DCE6F5", "1F4B86"], ["Average", 1.55, "C9D6EC", NAVY], ["Below Avg", 0.85, "F3DAD6", "8E3A30"], ["Poor", 0.8, RED, WHITE]];
  let sgx = ML + 0.25;
  segs.forEach((g) => {
    s.addShape(pres.shapes.RECTANGLE, { x: sgx, y: 2.56, w: g[1], h: 0.6, fill: { color: g[2] }, line: { color: WHITE, width: 1.5 } });
    s.addText(g[0], { x: sgx, y: 2.56, w: g[1], h: 0.6, fontSize: 7.6, color: g[3], bold: true, align: "center", valign: "middle", fontFace: BODY, margin: 0 });
    sgx += g[1];
  });
  s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.18, y: 3.42, w: 5.19, h: 0.64, fill: { color: REDL } });
  s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.18, y: 3.42, w: 0.06, h: 0.64, fill: { color: RED } });
  s.addText([
    { text: "Poor 등급 — ", options: { bold: true, color: RED } },
    { text: "기여도와 무관하게 '10명 중 1명'을 강제 배정. 케이스가 명시한 유일한 확정 비율이 이 'must 10%'다.", options: { color: INK } },
  ], { x: ML + 0.34, y: 3.42, w: 4.95, h: 0.64, fontSize: 8.5, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.12 });
  s.addText([
    { text: "비유 — 케이스:  ", options: { bold: true, color: NAVY } },
    { text: "\"Like a stack of LEGO bricks, employees were essentially slotted into top, good, average, below average and poor positions.\"", options: { color: GRAY, italic: true } },
  ], { x: ML + 0.18, y: 4.2, w: 5.2, h: 0.82, fontSize: 8.5, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.18, valign: "top" });
  s.addText("제도 작동 4대 요소", { x: 6.3, y: 1.62, w: 5, h: 0.3, fontSize: 11, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  const mech = [
    ["평가 주기", "6개월(반기) — 1년에 두 번 전 직원 서열화"],
    ["등급 구조", "5등급: Top / Good / Average / Below Average / Poor"],
    ["배분 방식", "강제배분(forced distribution) — 등급별 인원 비율 사전 고정"],
    ["보상 연동", "보상·승진이 등급에 '알고리즘'으로 자동 연동"],
  ];
  let my = 1.96;
  mech.forEach((m, i) => {
    card(s, 6.3, my, 4.84, 0.74, i === 3 ? REDL : WHITE, true);
    s.addShape(pres.shapes.RECTANGLE, { x: 6.3, y: my, w: 0.09, h: 0.74, fill: { color: i === 3 ? RED : NAVY } });
    s.addText(m[0], { x: 6.48, y: my, w: 1.15, h: 0.74, fontSize: 9.5, color: NAVY, bold: true, fontFace: BODY, valign: "middle", margin: 0 });
    s.addText(m[1], { x: 7.62, y: my, w: 3.45, h: 0.74, fontSize: 8.8, color: INK, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.1 });
    my += 0.82;
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.3, y: 5.04, w: 4.84, h: 1.02, fill: { color: NAVY } });
  s.addText("가장 치명적 결함", { x: 6.48, y: 5.12, w: 4.5, h: 0.28, fontSize: 9, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText("'평가'가 '보상'에 알고리즘으로 직결 → 평가가 '개발의 도구'가 아니라 '돈을 분배하는 도구'로만 작동. 평가 면담은 코칭이 아닌 정치·협상의 시간이 됐다.", { x: 6.48, y: 5.4, w: 4.5, h: 0.6, fontSize: 9, color: WHITE, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.18, valign: "top" });
  takeaway(s, "성과관리 제도는 '문화의 DNA' — 제도가 직원의 행동을 정밀하게 (잘못된 방향으로) 설계했다");
  footer(s, "출처: LBS128 케이스 (5등급·강제배분·6개월·알고리즘 보상연동 명시) — 확정 비율은 'Poor 10%'");
}

// ====================== S9 CULTURE FROM SYSTEM ======================
{
  const s = pres.addSlide();
  body(s, "01. 위기", "제도가 낳은 조직문화 — 사일로와 'Know-it-all'", "01. 위기", "4. As-Is 문화");
  govmsg(s, [{ t: "강제평가가 낳은 행동이 누적되어 " }, { t: "'봉건 영주국'의 구조와 '과시'의 문화", b: true }, { t: "로 굳었다" }]);
  card(s, ML, 1.66, 5.35, 2.66);
  secthdr(s, ML, 1.66, 5.35, "구조 — \"Confederation of Fiefdoms\"", NAVY);
  const silos = [["Windows", ML + 0.55], ["Office", ML + 2.18], ["Server", ML + 3.81]];
  silos.forEach((si) => {
    s.addShape(pres.shapes.RECTANGLE, { x: si[1], y: 2.22, w: 0.95, h: 0.42, fill: { color: NAVY } });
    s.addText(si[0], { x: si[1], y: 2.22, w: 0.95, h: 0.42, fontSize: 8.5, color: WHITE, bold: true, align: "center", valign: "middle", fontFace: BODY, margin: 0 });
    for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++)
      s.addShape(pres.shapes.RECTANGLE, { x: si[1] + 0.06 + c * 0.29, y: 2.94 + r * 0.27, w: 0.22, h: 0.21, fill: { color: "C7CEDC" } });
  });
  s.addShape(pres.shapes.LINE, { x: ML + 1.5, y: 2.43, w: 0.68, h: 0, line: { color: RED, width: 2, endArrowType: "triangle", beginArrowType: "triangle" } });
  s.addShape(pres.shapes.LINE, { x: ML + 3.13, y: 2.43, w: 0.68, h: 0, line: { color: RED, width: 2, endArrowType: "triangle", beginArrowType: "triangle" } });
  s.addText("제품별 사일로 = '봉건 영주국의 연합'. 부서 간 경쟁이 협업을 대체했고, 수직적 위계가 자발성·창의성을 억압했다.", { x: ML + 0.18, y: 3.62, w: 5.0, h: 0.62, fontSize: 8.8, color: GRAY, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.15, valign: "top" });
  card(s, 6.1, 1.66, 5.04, 2.66);
  secthdr(s, 6.1, 1.66, 5.04, "문화 — Know-it-all (과시의 문화)", NAVY);
  s.addText([
    { text: "\"가장 똑똑함을 증명하라\"\n", options: { bold: true, color: RED, fontSize: 10, breakLine: true } },
    { text: "직원들은 회의실에서 '자신이 가장 똑똑하다'는 것을 증명해야 했다. 학습보다 과시가, 질문보다 정답이 우선.\n\n", options: { color: GRAY, fontSize: 8.8, breakLine: true } },
    { text: "Precision Questioning & 폐쇄성\n", options: { bold: true, color: RED, fontSize: 10, breakLine: true } },
    { text: "회의는 아이디어의 허점을 찌르는 검증의 장. Ballmer는 Linux를 \"암(a cancer)\"으로 규정 — 외부에 닫힌 'Not Invented Here'.", options: { color: GRAY, fontSize: 8.8 } },
  ], { x: 6.28, y: 2.16, w: 4.7, h: 2.05, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.16, valign: "top" });
  quote(s, ML, 4.46, CW, 0.92, "\"직원들은 회의실 안에서 자신이 가장 똑똑하다는 것을 증명해야 했다. 계급과 서열이 조직을 지배하면서 자발성과 창의성이 고통받았다.\"", "— Satya Nadella, 『히트 리프레시』 p151", true);
  // mini summary
  s.addText("As-Is 종합 — 전략 의도가 제도를, 제도가 문화를 만든 3단 사슬", { x: ML, y: 5.5, w: CW, h: 0.28, fontSize: 9.5, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  const ssum = [["전략 의도", "PC 수성 + 실적주의", RED], ["HR 제도", "Stack Ranking (상대평가·강제배분)", AMBER], ["조직문화", "사일로 + Know-it-all", NAVY]];
  let sx = ML;
  ssum.forEach((c, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: sx, y: 5.82, w: 3.3, h: 0.6, fill: { color: LGRAY }, line: { color: MGRAY, width: 0.75 } });
    s.addShape(pres.shapes.RECTANGLE, { x: sx, y: 5.82, w: 0.07, h: 0.6, fill: { color: c[2] } });
    s.addText([{ text: c[0] + "\n", options: { bold: true, color: NAVY, fontSize: 8.8, breakLine: true } }, { text: c[1], options: { color: GRAY, fontSize: 8.3 } }],
      { x: sx + 0.16, y: 5.82, w: 3.05, h: 0.6, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.12 });
    if (i < 2) s.addText("▶", { x: sx + 3.3, y: 5.82, w: 0.36, h: 0.6, fontSize: 9, color: MGRAY, align: "center", valign: "middle", margin: 0 });
    sx += 3.66;
  });
  takeaway(s, "병소는 '한 곳'이 아니다 — 전략·제도·문화가 한 덩어리로 맞물려 '심리적 안전감 제로'의 조직을 만들었다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p151");
}

// ====================== S10 CVF AS-IS ======================
{
  const s = pres.addSlide();
  body(s, "01. 위기", "퀸 모델로 본 As-Is — '위계 + 시장' 사분면 고착", "01. 위기", "5. CVF As-Is 좌표");
  govmsg(s, [{ t: "Ballmer 시대 문화의 좌표는 " }, { t: "'안정·통제' 축의 위계(Hierarchy) + 시장(Market)", b: true }]);
  cvfQuad(s, 1.55, 2.36, 4.3, 3.6, "asis");
  card(s, 6.3, 1.66, 4.84, 4.7, LGRAY);
  s.addText("As-Is 좌표 해석 — 왜 여기에 갇혔나", { x: 6.5, y: 1.78, w: 4.5, h: 0.3, fontSize: 11, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  const interp = [
    ["Hierarchy (위계) 고착", "수직적 위계·서열·규칙이 지배. 형식적 회의, 상사 결재 중심 — 자발성·창의성 억압"],
    ["Market (시장) 고착", "Stack Ranking이 만든 내부 경쟁·실적주의. 동료를 이겨야 하는 제로섬 — '협력'은 비합리적 행동"],
    ["빠진 사분면 — Clan (관계)", "협력·인재개발의 '관계문화'가 부재. 지식 공유는 곧 자기 손해가 됐다"],
    ["빠진 사분면 — Adhocracy (혁신)", "창의·모험의 '혁신문화'가 부재. 실패가 약점이 되는 곳에서 누구도 위험을 감수하지 않았다"],
  ];
  let iy = 2.2;
  interp.forEach((t, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.5, y: iy, w: 0.08, h: 0.96, fill: { color: i < 2 ? RED : "9098A8" } });
    s.addText([
      { text: t[0] + "\n", options: { bold: true, color: i < 2 ? RED : GRAY, fontSize: 9.3, breakLine: true } },
      { text: t[1], options: { color: INK, fontSize: 8.7 } },
    ], { x: 6.68, y: iy, w: 4.32, h: 0.96, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.16 });
    iy += 1.02;
  });
  takeaway(s, "환경(모바일·클라우드)은 '유연성'을 요구했지만, 문화는 정반대인 '안정·통제' 축에 갇혀 있었다 — 전략-문화 부정합");
  footer(s, "출처: LBS128 케이스 / 경쟁가치모형(Cameron & Quinn)으로 본 진단");
}

// ====================== 02 DIVIDER ======================
divider("02", "각성 — 한 리더의 '공감'", "Awakening", [
  "왜 나델라인가 — 22년 내부자가 가진 '내부에서 본 외부의 시선'",
  "장남 Zain에게서 배운 공감, 그리고 Dweck의 『Mindset』 — 변화의 씨앗",
]);

// ====================== S12 WHY NADELLA / EMPATHY ======================
{
  const s = pres.addSlide();
  body(s, "02. 각성", "왜 나델라인가 — '공감'이라는 변화의 씨앗", "02. 각성", "1. 공감의 뿌리");
  govmsg(s, [{ t: "나델라의 리더십은 전략이 아니라 " }, { t: "장남에게서 배운 '공감'", b: true }, { t: "에서 출발했다" }]);
  card(s, ML, 1.66, 5.3, 2.06);
  secthdr(s, ML, 1.66, 5.3, "프로필 — 내부에서 본 외부의 시선", NAVY);
  s.addText([
    "1992년 입사 — 22년 내부자, Cloud & Enterprise 부문 EVP 역임",
    "Bing 등 리스크 큰 보직을 자발적으로 수행 — \"거절하기 어려운 학습 기회\"",
    "내부자의 맥락 이해 + 그 문화에 '포섭되지 않은' 비판적 시선",
  ].map((m) => ({ text: m, options: { bullet: { code: "2022" }, breakLine: true, paraSpaceAfter: 8 } })),
    { x: ML + 0.2, y: 2.16, w: 4.95, h: 1.45, fontSize: 9.5, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.14 });
  card(s, ML, 3.88, 5.3, 2.78);
  secthdr(s, ML, 3.88, 5.3, "공감의 뿌리 — 장남 Zain", RED);
  s.addText("뇌성마비를 안고 태어난 장남 Zain을 키우며, 나델라는 '공감'을 추상적 가치가 아닌 '체화된 역량'으로 받아들였다. 입사 면접에서 한 면접관이 던진 말이 그를 오래 따라다녔다.", { x: ML + 0.2, y: 4.36, w: 5.0, h: 0.86, fontSize: 9.2, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });
  quote(s, ML + 0.2, 5.28, 4.95, 1.2, "\"당신은 공감 능력이 조금 필요하군요. 아기가 거리에서 울고 있다면 아기를 안아 올려야지요.\"", "— 입사 면접관의 말, 『히트 리프레시』 p26", false);
  // right column
  card(s, 6.05, 1.66, 5.09, 2.4, NAVY);
  s.addText("공감은 '전략적 역량'이다", { x: 6.25, y: 1.8, w: 4.7, h: 0.32, fontSize: 11, color: WHITE, bold: true, fontFace: BODY, margin: 0 });
  s.addText("나델라에게 공감은 단순한 인성이 아니라 경영의 핵심 역량이다. 직원·고객의 '미충족 니즈'를 느낄 수 있어야 그것을 충족시킬 수 있기 때문이다. 그는 이 공감을 Microsoft의 제품·시장·직원·파트너 한가운데 심고자 했다.", { x: 6.25, y: 2.18, w: 4.7, h: 1.05, fontSize: 9.3, color: "D6DEEC", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });
  quote(s, 6.25, 3.28, 4.69, 0.66, "\"나는 삶의 부침을 통해서만 공감 능력을 발전시킬 수 있다는 것을 알게 되었다.\"", "— 『히트 리프레시』 p28", true);
  card(s, 6.05, 4.22, 5.09, 2.44, LGRAY);
  s.addText("핵심 통찰 — 변화는 '인간'에서 출발한다", { x: 6.25, y: 4.34, w: 4.7, h: 0.3, fontSize: 10, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "나델라는 '전략 전환'이 아니라 \"인간 시스템(human system)의 변화\"를 변혁의 목표로 삼았다. 평가·보상·구조를 바꾸기 전에 — '인재를 보는 눈'과 '리더의 태도'부터 바꾸려 했다.\n\n", options: { color: INK, fontSize: 9.2, breakLine: true } },
    { text: "→ 다음 장: 이 공감의 리더가 만난 또 하나의 씨앗, Carol Dweck의 『Mindset』", options: { color: GRAY, fontSize: 8.7, italic: true } },
  ], { x: 6.25, y: 4.68, w: 4.7, h: 1.9, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });
  takeaway(s, "변혁의 첫 단추는 제도가 아니라 리더의 '인간관' — 나델라의 공감이 그 출발점이었다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p26, p28");
}

// ====================== S13 DWECK MINDSET ======================
{
  const s = pres.addSlide();
  body(s, "02. 각성", "성장 마인드셋과의 만남 — Carol Dweck 『Mindset』", "02. 각성", "2. 성장 마인드셋");
  govmsg(s, [{ t: "아내가 건넨 한 권의 책이 " }, { t: "12.5만 명 조직 변혁의 '청사진'", b: true }, { t: "이 되었다" }]);
  card(s, ML, 1.66, 4.5, 2.0, LGRAY);
  s.addText("한 권의 책에서 시작된 청사진", { x: ML + 0.18, y: 1.78, w: 4.1, h: 0.3, fontSize: 10, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText("아내 Anu가 추천한 스탠퍼드 심리학자 Carol Dweck의 『Mindset』. 학습 차이가 있는 딸을 위한 책이었지만, 나델라는 거기서 '조직'을 위한 변혁의 원리를 발견했다.", { x: ML + 0.18, y: 2.12, w: 4.18, h: 1.4, fontSize: 9.2, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });
  // fixed vs growth mini-table
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 3.84, w: 2.25, h: 0.4, fill: { color: RED } });
  s.addText("Fixed Mindset", { x: ML, y: 3.84, w: 2.25, h: 0.4, fontSize: 9.5, color: WHITE, bold: true, align: "center", valign: "middle", fontFace: BODY, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: ML + 2.25, y: 3.84, w: 2.25, h: 0.4, fill: { color: BLUE } });
  s.addText("Growth Mindset", { x: ML + 2.25, y: 3.84, w: 2.25, h: 0.4, fontSize: 9.5, color: WHITE, bold: true, align: "center", valign: "middle", fontFace: BODY, margin: 0 });
  const fg = [["능력은 고정된 자질", "능력은 노력으로 성장"], ["실패 = 약점 노출, 회피", "실패 = 학습 기회"], ["익숙한 것만 고수", "새로운 도전을 추구"], ["타인의 성공은 위협", "타인의 성공은 영감"], ["Know-it-all", "Learn-it-all"]];
  let fy = 4.24;
  fg.forEach((r, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: ML, y: fy, w: 2.25, h: 0.4, fill: { color: i % 2 ? "FBEEEC" : "FCF4F2" }, line: { color: "F0DAD6", width: 0.5 } });
    s.addText(r[0], { x: ML + 0.1, y: fy, w: 2.05, h: 0.4, fontSize: 8.4, color: "8E3A30", valign: "middle", fontFace: BODY, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: ML + 2.25, y: fy, w: 2.25, h: 0.4, fill: { color: i % 2 ? "EAF0FA" : "F0F4FB" }, line: { color: "DAE3F2", width: 0.5 } });
    s.addText(r[1], { x: ML + 2.35, y: fy, w: 2.05, h: 0.4, fontSize: 8.4, color: "1F4B86", valign: "middle", fontFace: BODY, margin: 0 });
    fy += 0.4;
  });
  // right
  card(s, 5.25, 1.66, 5.89, 2.5, NAVY);
  s.addText("나델라가 읽어낸 것 — '조직'의 마인드셋", { x: 5.45, y: 1.8, w: 5.5, h: 0.3, fontSize: 11, color: WHITE, bold: true, fontFace: BODY, margin: 0 });
  s.addText("Dweck은 세상을 '학습자'와 '비학습자'로 나눈다. 나델라는 이 개인 심리학을 '조직'의 차원으로 끌어올렸다 — 회사 전체가 '아는 척하는 집단(know-it-all)'에서 '배우려는 집단(learn-it-all)'으로 바뀔 수 있다는 것.", { x: 5.45, y: 2.16, w: 5.5, h: 1.05, fontSize: 9.3, color: "D6DEEC", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.25, valign: "top" });
  quote(s, 5.45, 3.26, 5.49, 0.74, "\"고정된 사고는 발목을 붙잡지만, 성장하는 사고는 사람들을 앞으로 나아가게 한다. … 사람들이 받은 패는 출발점에 불과하다.\"", "— 『히트 리프레시』 p140", true);
  card(s, 5.25, 4.32, 5.89, 2.34, LGRAY);
  s.addText("'성장'의 정의 — 손익이 아니라 사람", { x: 5.45, y: 4.44, w: 5.5, h: 0.3, fontSize: 10, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  quote(s, 5.45, 4.78, 5.49, 0.72, "\"여기서 성장이란 손익 계산과 관련된 것이 아니다. 이건 개인의 성장에 관한 것이었다.\"", "— 『히트 리프레시』 p142", false);
  s.addText("→ 이 '성장 마인드셋'이 PART 4의 새 미션과 3대 Pillar, PART 5의 제도 재설계로 구체화된다.", { x: 5.45, y: 5.6, w: 5.5, h: 0.9, fontSize: 8.9, color: GRAY, italic: true, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });
  takeaway(s, "성장 마인드셋은 슬로건이 아니라 — 평가·보상·문화를 다시 설계하는 '이론적 근간'이 되었다");
  footer(s, "출처: LBS128 케이스 / Carol Dweck, 『Mindset』 / 『히트 리프레시』 p140, p142");
}

// ====================== 03 DIVIDER ======================
divider("03", "경청 — 진단으로서의 첫 1년", "Listening", [
  "지시가 아니라 듣는 것부터 — 수백 명 인터뷰와 익명 포커스 그룹",
  "\"Microsoft는 왜 존재하는가\" — 그리고 '변화를 이끌 사람을 버스에 태우다'",
]);

// ====================== S15 LISTENING ======================
{
  const s = pres.addSlide();
  body(s, "03. 경청", "취임과 경청 — '진단 없이 처방하지 않는다'", "03. 경청", "1. 경청의 1년");
  govmsg(s, [{ t: "나델라의 첫 1년은 비전 '선포'가 아니라 " }, { t: "'경청'을 통한 조직 진단", b: true }, { t: "이었다" }]);
  s.addText("진단 방법론 — 듣는 것부터 시작하다", { x: ML, y: 1.62, w: 5, h: 0.3, fontSize: 10.5, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  const tl = [
    ["2014.2", "CEO 취임 & 전 직원 서한", "\"22년 전 첫 출근날처럼 겸허하다\" — 첫날부터 '의미'를 묻다"],
    ["상징적 신호", "리더십 팀에 'NVC' 의무 독서", "비폭력대화(Nonviolent Communication) — '소통의 방식'부터 바꾸겠다는 신호"],
    ["진단 ①", "수백 명 인터뷰", "모든 레벨·모든 부서를 직접 경청"],
    ["진단 ②", "익명 포커스 그룹", "솔직한 의견을 끌어내는 안전한 채널"],
    ["핵심 질문", "\"Why does Microsoft exist?\"", "존재 이유에 대한 근본적 재질문"],
  ];
  let ty = 1.98;
  tl.forEach((t, i) => {
    s.addShape(pres.shapes.OVAL, { x: ML, y: ty, w: 0.38, h: 0.38, fill: { color: i === 1 ? RED : BLUE } });
    s.addText(String(i + 1), { x: ML, y: ty, w: 0.38, h: 0.38, fontSize: 11, color: WHITE, bold: true, fontFace: HEAD, align: "center", valign: "middle", margin: 0 });
    if (i < 4) s.addShape(pres.shapes.LINE, { x: ML + 0.19, y: ty + 0.38, w: 0, h: 0.5, line: { color: MGRAY, width: 1.5 } });
    s.addText([{ text: t[0] + "  ", options: { bold: true, color: BLUE, fontSize: 8.5 } }, { text: t[1], options: { bold: true, color: INK, fontSize: 10.5, fontFace: HEAD } }],
      { x: ML + 0.52, y: ty - 0.04, w: 5.0, h: 0.32, fontFace: BODY, margin: 0, valign: "middle" });
    s.addText(t[2], { x: ML + 0.52, y: ty + 0.28, w: 5.0, h: 0.3, fontSize: 8.6, color: GRAY, fontFace: BODY, margin: 0, valign: "middle" });
    ty += 0.88;
  });
  quote(s, ML, 6.4, 5.45, 0.7, "\"경청은 내가 매일 실천한 가장 중요한 과제였다. 앞으로 몇 년간 내 리더십의 기초를 다질 요소였기 때문이다.\"", "— 『히트 리프레시』 p118", false);
  card(s, 6.1, 1.66, 5.04, 5.16, LGRAY);
  s.addText("진단 결과 — 직원들이 원한 5가지", { x: 6.3, y: 1.8, w: 5, h: 0.32, fontSize: 11, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  const needs = [
    "변화를 만들되, Microsoft의 원래 이상을 존중하는 CEO",
    "명확하고 구체적이며 영감을 주는 비전",
    "투명하고 단순한 방식의 진행 상황 공유",
    "따라가는 것이 아니라 다시 '선도(lead)'하는 회사",
    "잃어버린 \"멋진 것(coolness)\"의 회복",
  ];
  let ny = 2.28;
  needs.forEach((n, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.3, y: ny, w: 4.64, h: 0.74, fill: { color: WHITE }, line: { color: MGRAY, width: 0.75 } });
    s.addText(String(i + 1), { x: 6.4, y: ny, w: 0.55, h: 0.74, fontSize: 22, color: "BCC8DE", bold: true, fontFace: HEAD, align: "center", valign: "middle", margin: 0 });
    s.addText(n, { x: 6.98, y: ny, w: 3.9, h: 0.74, fontSize: 9.6, color: INK, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.08 });
    ny += 0.82;
  });
  s.addText("진단의 결론 — \"우리가 존재하는 이유는 사람들이 우리 제품으로 더 많은 힘을 얻게(empower) 하는 데 있다\"", { x: 6.3, y: 6.42, w: 4.7, h: 0.4, fontSize: 8.8, color: NAVY, bold: true, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.12 });
  takeaway(s, "내부 승진 CEO의 강점(맥락 이해)을 '경청·진단 방법론'으로 전환 — 처방은 진단 다음이다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p118");
}

// ====================== S16 SLT ======================
{
  const s = pres.addSlide();
  body(s, "03. 경청", "SLT 재구성 — '변화를 이끌 사람을 버스에 태운다'", "03. 경청", "2. 리더십팀 재구성");
  govmsg(s, [{ t: "비전보다 먼저 한 일 — " }, { t: "변화를 이끌 '리더십 팀'을 다시 짜는 것", b: true }]);
  quote(s, ML, 1.64, CW, 0.6, "\"우선은 나와 함께 이런 변화를 이끌 사람을 버스에 태워야 했다. SLT는 같은 세계관을 공유하는 끈끈한 조직으로 바뀌어야 했다.\"", "— 『히트 리프레시』 p125", true);
  s.addText("새 SLT(시니어 리더십 팀)의 면면 — '독특한 초능력의 슈퍼히어로 군단'", { x: ML, y: 2.42, w: CW, h: 0.3, fontSize: 10, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  const slt = [
    ["Kathleen Hogan", "최고인사책임자 (CPO)", "맥킨지·오라클 출신. 문화·인사 변혁을 HR이 총괄 — '문화 고문단' 운영", NAVY, "변혁의 설계·총괄", "문화·인사 변혁을 HR 어젠다로 끌어올린 핵심 축"],
    ["Jill T. Nichols", "비서실장 (Chief of Staff)", "발머 시절 인물. 발탁 이유 = \"권력이 아니라 문화를 위한 사무실\"", BLUE, "소통·문화의 실무", "구 인물을 품어 — '문화는 사람을 가리지 않는다'는 신호"],
    ["Peggy Johnson", "사업개발 총괄", "퀄컴 출신. 실리콘밸리 경쟁사와 '놀라운 파트너십' 구축", BLUE, "외부와의 연결", "닫힌 조직을 외부 생태계로 여는 가교"],
    ["Kurt DelBene", "최고전략책임자 (CSO)", "오바마 행정부 Healthcare.gov 복구 주역 — 외부 경험을 다시 안으로", NAVY, "전략·실행력", "떠났던 인재를 다시 불러 — 학습한 외부 경험을 이식"],
  ];
  let sy = 2.82;
  slt.forEach((p) => {
    card(s, ML, sy, CW, 0.78, WHITE, true);
    s.addShape(pres.shapes.RECTANGLE, { x: ML, y: sy, w: 0.1, h: 0.78, fill: { color: p[3] } });
    s.addText([{ text: p[0] + "    ", options: { bold: true, color: INK, fontSize: 11.5 } }, { text: p[1], options: { color: p[3], fontSize: 9, bold: true } }],
      { x: ML + 0.25, y: sy + 0.08, w: 6.0, h: 0.36, fontFace: BODY, margin: 0, valign: "middle" });
    s.addText(p[2], { x: ML + 0.25, y: sy + 0.42, w: 6.0, h: 0.3, fontSize: 9, color: GRAY, fontFace: BODY, margin: 0, valign: "middle" });
    s.addShape(pres.shapes.LINE, { x: ML + 6.4, y: sy + 0.14, w: 0, h: 0.5, line: { color: MGRAY, width: 1 } });
    s.addText([{ text: p[4] + "\n", options: { bold: true, color: p[3], fontSize: 9, breakLine: true } }, { text: p[5], options: { color: GRAY, fontSize: 8.3 } }],
      { x: ML + 6.6, y: sy, w: 3.9, h: 0.78, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.12 });
    sy += 0.86;
  });
  card(s, ML, 6.34, CW, 0.86, LGRAY);
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 6.34, w: 0.07, h: 0.86, fill: { color: BLUE } });
  s.addText([
    { text: "단, '예스맨'은 아니다    ", options: { bold: true, color: BLUE, fontSize: 9.5 } },
    { text: "나델라는 분명히 했다 — \"논쟁이나 논의는 반드시 필요하다. 서로의 아이디어를 개선하는 것이 핵심이다. 그러나 동시에 '높은 수준의 합의'에 도달해야 한다.\" SLT를 '또 하나의 회의'가 아니라 '각자의 첫 번째 팀(first team)'으로 인식하게 했다.", options: { color: INK, fontSize: 9 } },
  ], { x: ML + 0.2, y: 6.34, w: CW - 0.4, h: 0.86, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.18 });
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p125~127");
}

// ====================== 04 DIVIDER ======================
divider("04", "선언 — \"Know-it-all에서 Learn-it-all로\"", "Declaration", [
  "새로운 미션 — \"지구상 모든 사람과 조직이 더 많이 성취하도록\"",
  "성장 마인드셋을 '조직의 언어'로 — Culture Cabinet과 3대 Pillar",
]);

// ====================== S18 NEW MISSION ======================
{
  const s = pres.addSlide();
  body(s, "04. 선언", "새 미션 선언 — 2015 올랜도, '의미'를 다시 정의하다", "04. 선언", "1. 새 미션");
  govmsg(s, [{ t: "미션을 " }, { t: "'제품(컴퓨터)'에서 '사람의 역량(empower)'", b: true }, { t: "으로 다시 정의했다" }]);
  // mission transition
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 1.66, w: 5.15, h: 2.0, fill: { color: LGRAY } });
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 1.66, w: 0.07, h: 2.0, fill: { color: GRAY } });
  s.addText("기존 미션 (Gates)", { x: ML + 0.2, y: 1.78, w: 4.7, h: 0.3, fontSize: 9.5, color: GRAY, bold: true, fontFace: BODY, margin: 0 });
  s.addText("\"A computer on every desk and in every home\"", { x: ML + 0.2, y: 2.1, w: 4.8, h: 0.5, fontSize: 11.5, color: INK, italic: true, bold: true, fontFace: HEAD, margin: 0 });
  s.addText("PC의 보편화 — 한 시대를 지배했으나, 모바일·클라우드 시대에는 '이미 달성된, 닫힌 목표'였다.", { x: ML + 0.2, y: 2.66, w: 4.8, h: 0.9, fontSize: 8.8, color: GRAY, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 3.86, w: 5.15, h: 2.18, fill: { color: NAVY } });
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 3.86, w: 0.07, h: 2.18, fill: { color: RED } });
  s.addText("새 미션 (Nadella, 2015 올랜도)", { x: ML + 0.2, y: 3.98, w: 4.7, h: 0.3, fontSize: 9.5, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText("\"To empower every person and every organisation on the planet to achieve more\"", { x: ML + 0.2, y: 4.3, w: 4.8, h: 0.78, fontSize: 12, color: WHITE, italic: true, bold: true, fontFace: HEAD, margin: 0, lineSpacingMultiple: 1.05 });
  s.addText("지구상 모든 사람과 조직이 '더 많이 성취하도록'. 끝이 없는 목표 — 제품이 아니라 '타인의 역량'을 향한다.", { x: ML + 0.2, y: 5.16, w: 4.8, h: 0.8, fontSize: 8.8, color: "C7CFE0", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.2, valign: "top" });
  // right
  card(s, 6.1, 1.66, 5.04, 2.3);
  secthdr(s, 6.1, 1.66, 5.04, "왜 미션부터 바꿨나", NAVY);
  s.addText("진단(PART 3)에서 직원들이 가장 원한 것은 '명확하고 영감을 주는 비전'이었다. 나델라는 올랜도 세계 영업 컨퍼런스에서 새 미션을 선언하며 — 자녀들의 특수한 필요를 통해 배운 것을 이야기하고, 곧바로 '문화'를 말했다.", { x: 6.28, y: 2.16, w: 4.7, h: 1.7, fontSize: 9.2, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
  quote(s, 6.1, 4.16, 5.04, 1.5, "\"우리는 담대한 목표를 세울 수 있습니다. 그러나 그것은 우리가 문화를 살아내고, 문화를 가르칠 때에만 일어납니다. … 그 문화의 모델이 바로 '성장하는 사고(growth mindset)'입니다.\"", "— Satya Nadella, 2015 올랜도 연설 / 『히트 리프레시』", true);
  card(s, 6.1, 5.82, 5.04, 1.0, LGRAY);
  s.addShape(pres.shapes.RECTANGLE, { x: 6.1, y: 5.82, w: 0.07, h: 1.0, fill: { color: BLUE } });
  s.addText("→ 미션(외부를 향한 약속)이 곧 내부 문화의 방향타가 된다. '역량 강화'를 외친 회사는, 내부 구성원도 '역량을 키우는' 방식으로 평가·보상해야 한다.", { x: 6.28, y: 5.82, w: 4.7, h: 1.0, fontSize: 9, color: INK, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.2 });
  takeaway(s, "미션을 '제품'에서 '사람의 역량'으로 옮긴 순간 — 평가·보상 제도가 바뀌어야 할 이유가 생겼다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p122~123, p142");
}

// ====================== S19 CULTURE CABINET ======================
{
  const s = pres.addSlide();
  body(s, "04. 선언", "성장 마인드셋을 '조직의 언어'로 — Culture Cabinet", "04. 선언", "2. Culture Cabinet");
  govmsg(s, [{ t: "추상적 개념을 " }, { t: "임원 180명이 '17개 팀'으로 직접 정의", b: true }, { t: "하게 했다" }]);
  card(s, ML, 1.66, 5.4, 2.5);
  secthdr(s, ML, 1.66, 5.4, "Culture Cabinet — 문화를 '함께' 정의하다", NAVY);
  s.addText([
    { text: "나델라는 성장 마인드셋을 위에서 '하달'하지 않았다. 임원 180명을 17개 팀으로 나눠, '우리에게 성장 마인드셋이란 무엇인가'를 직접 정의하게 했다. 17명의 리더가 '문화 고문단(culture cabinet)'이 되었다.\n", options: { color: INK, fontSize: 9.3, breakLine: true } },
    { text: "→ 문화는 '선언'이 아니라 '참여'로 만들어진다. 정의의 주체가 곧 실행의 주체가 된다.", options: { color: GRAY, fontSize: 8.8, italic: true } },
  ], { x: ML + 0.18, y: 2.16, w: 5.05, h: 1.9, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.28, valign: "top" });
  card(s, ML, 4.32, 5.4, 2.5, LGRAY);
  s.addText("'성장'의 재정의 — 손익이 아니라 사람", { x: ML + 0.18, y: 4.44, w: 5, h: 0.3, fontSize: 10, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  quote(s, ML + 0.18, 4.78, 5.04, 0.86, "\"실제로 우리의 새로운 문화를 설명해주는 문구는 '성장하는 사고'입니다. … 여기서 성장이란 손익 계산과 관련된 것이 아니라, 개인의 성장에 관한 것이었습니다.\"", "— 『히트 리프레시』 p142", false);
  s.addText("'know-it-all(다 아는 사람)'에서 'learn-it-all(다 배우려는 사람)'로 — 회사의 정체성을 한 문장으로 압축했다.", { x: ML + 0.18, y: 5.74, w: 5.05, h: 0.95, fontSize: 9, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
  // right: drucker + chain
  quote(s, 6.15, 1.66, 4.99, 0.92, "\"문화는 아침 식사로 전략을 먹는다 (Culture eats strategy for breakfast).\"", "— Peter Drucker, 『히트 리프레시』 p138 인용", true);
  card(s, 6.15, 2.74, 4.99, 4.08, LGRAY);
  s.addText("선언에서 구현으로 — 다음 단계의 예고", { x: 6.33, y: 2.86, w: 4.6, h: 0.3, fontSize: 10, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText("나델라는 '문화가 전략을 이긴다'는 드러커의 말을 빌려, 문화를 경영의 1순위로 올렸다. 그러나 그는 알았다 — 선언만으로는 아무것도 바뀌지 않는다는 것을.", { x: 6.33, y: 3.2, w: 4.6, h: 0.9, fontSize: 9.2, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
  const steps2 = [["선언", "새 미션 + 성장 마인드셋의 언어화", BLUE], ["구체화", "3대 Pillar — 다음 장", BLUE], ["구현", "제도·행동·환경으로 — PART 5", RED]];
  let sy2 = 4.18;
  steps2.forEach((c, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.33, y: sy2, w: 4.6, h: 0.56, fill: { color: WHITE }, line: { color: MGRAY, width: 0.75 } });
    s.addShape(pres.shapes.RECTANGLE, { x: 6.33, y: sy2, w: 0.07, h: 0.56, fill: { color: c[2] } });
    s.addText([{ text: c[0] + "  —  ", options: { bold: true, color: NAVY, fontSize: 9.3 } }, { text: c[1], options: { color: GRAY, fontSize: 8.7 } }],
      { x: 6.5, y: sy2, w: 4.35, h: 0.56, fontFace: BODY, valign: "middle", margin: 0 });
    if (i < 2) s.addText("▼", { x: 6.33, y: sy2 + 0.56, w: 4.6, h: 0.18, fontSize: 8, color: MGRAY, align: "center", margin: 0 });
    sy2 += 0.74;
  });
  takeaway(s, "문화는 '하달'이 아니라 '공동 정의'로 만들어진다 — 정의의 주체가 곧 실행의 주체가 된다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p138, p142");
}

// ====================== S20 THREE PILLARS ======================
{
  const s = pres.addSlide();
  body(s, "04. 선언", "성장 마인드셋의 3대 Pillar", "04. 선언", "3. 3대 Pillar");
  govmsg(s, [{ t: "성장 마인드셋을 실천하는 " }, { t: "세 가지 구체적 방법", b: true }, { t: " — 고객 집착 · 다양성과 포용 · One Microsoft" }]);
  const pil = [
    ["Customer Obsession", "고객 집착", "\"초심자의 마음으로 소비자에게 배운다\" — 소비자가 표현한 적 없고 충족된 적 없는 요구를 채우려는 열망과 호기심", "성장 마인드셋을 '외부'로 향하게 한다", BLUE],
    ["Diversity & Inclusion", "다양성과 포용", "\"적극적으로 다양성과 포용을 추구해야 최고의 성과를 얻는다\" — 자신의 편견을 깨닫고 행동을 바꾸는 것", "성장 마인드셋을 '서로'에게 향하게 한다", NAVY],
    ["One Microsoft", "하나의 마이크로소프트", "\"우리는 하나의 회사다. 여러 세력으로 구성된 연합체가 아니다\" — 사일로를 넘는 협업", "성장 마인드셋을 '조직 전체'로 향하게 한다", RED],
  ];
  const pw = 3.45, pg = 0.12;
  let px = ML;
  pil.forEach((p) => {
    card(s, px, 1.66, pw, 4.0);
    s.addShape(pres.shapes.RECTANGLE, { x: px, y: 1.66, w: pw, h: 0.78, fill: { color: p[4] } });
    s.addText(p[0], { x: px + 0.16, y: 1.7, w: pw - 0.3, h: 0.46, fontSize: 11.5, color: WHITE, bold: true, fontFace: HEAD, margin: 0 });
    s.addText(p[1], { x: px + 0.16, y: 2.12, w: pw - 0.3, h: 0.3, fontSize: 9, color: "D6DEEC", fontFace: BODY, margin: 0 });
    s.addText("개념", { x: px + 0.16, y: 2.58, w: 1, h: 0.24, fontSize: 8, color: p[4], bold: true, fontFace: BODY, margin: 0 });
    s.addText(p[2], { x: px + 0.16, y: 2.82, w: pw - 0.32, h: 1.7, fontSize: 9, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
    s.addShape(pres.shapes.LINE, { x: px + 0.16, y: 4.62, w: pw - 0.32, h: 0, line: { color: MGRAY, width: 0.75 } });
    s.addText("역할", { x: px + 0.16, y: 4.7, w: 1, h: 0.24, fontSize: 8, color: p[4], bold: true, fontFace: BODY, margin: 0 });
    s.addText(p[3], { x: px + 0.16, y: 4.94, w: pw - 0.32, h: 0.66, fontSize: 9, color: GRAY, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.15, valign: "top" });
    px += pw + pg;
  });
  quote(s, ML, 5.84, CW, 0.7, "\"우리는 하나의 회사, 하나의 마이크로소프트다. 여러 세력으로 구성된 연합체가 아니다.\"", "— Satya Nadella, 『히트 리프레시』 p152", true);
  takeaway(s, "3대 Pillar는 성장 마인드셋을 '외부(고객)·서로(동료)·전체(조직)'의 세 방향으로 작동시키는 설계도다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p151~153");
}

// ====================== 05 DIVIDER ======================
divider("05", "구현 — 문화를 일상에 심다", "Grounding the Pillars", [
  "선언을 현실로 — '큰 변화'(제도)와 '작은 변화'(넛지)의 동시 작동",
  "성과평가·보상 제도의 재설계, 리더의 솔선수범, 그리고 일상의 넛지",
]);

// ====================== S22 GROUNDING PRINCIPLE ======================
{
  const s = pres.addSlide();
  body(s, "05. 구현", "구현의 원리 — '큰 변화'와 '작은 변화'의 동시 작동", "05. 구현", "1. 구현 원리");
  govmsg(s, [{ t: "문화는 " }, { t: "하나의 큰 조치가 아니라, 크고 작은 수많은 것들", b: true }, { t: "이 변화를 강화하며 만들어진다" }]);
  quote(s, ML, 1.64, CW, 0.62, "\"우리는 큰 변화를 만들었습니다 — 성과 평가 시스템을 바꾸는 것처럼. 그리고 작은 변화도 만들었습니다 … 우리는 결코 '단 하나의 조치'가 회사를 바꿀 거라고 믿지 않았습니다.\"", "— Kathleen Hogan (CPO), LBS128 케이스", true);
  // two columns: 큰 변화 / 작은 변화
  card(s, ML, 2.46, 5.15, 3.55);
  secthdr(s, ML, 2.46, 5.15, "큰 변화 (Big) — 제도를 바꾸다", RED);
  const big = [
    ["성과평가 제도 개혁", "Stack Ranking 폐지 → 상시 피드백·코칭 (S23)"],
    ["보상 제도 개혁", "알고리즘 연동 → 매니저 재량 예산 (S23)"],
    ["리더십 팀 재구성", "SLT를 '하나의 first team'으로 (S16)"],
    ["다양성 목표의 제도화", "임원 보너스에 다양성 지표 연계 (S24)"],
  ];
  let by = 2.94;
  big.forEach((b) => {
    s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.18, y: by, w: 0.08, h: 0.62, fill: { color: RED } });
    s.addText([{ text: b[0] + "\n", options: { bold: true, color: NAVY, fontSize: 9.5, breakLine: true } }, { text: b[1], options: { color: GRAY, fontSize: 8.6 } }],
      { x: ML + 0.34, y: by, w: 4.75, h: 0.62, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.1 });
    by += 0.7;
  });
  card(s, 5.95, 2.46, 5.19, 3.55);
  secthdr(s, 5.95, 2.46, 5.19, "작은 변화 (Small) — 일상을 바꾸다", BLUE);
  const small = [
    ["회의 마무리 성찰", "\"이 회의는 Growth였나 Fixed였나?\" (S26)"],
    ["월간 학습 영상", "나델라가 자신의 배움을 직접 공유 (S26)"],
    ["10가지 포용 행동 리스트", "추상적 가치를 구체적 행동으로 (S26)"],
    ["리더의 공개적 실패 인정", "Grace Hopper·Tay 사건 (S25)"],
  ];
  let smy = 2.94;
  small.forEach((b) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.13, y: smy, w: 0.08, h: 0.62, fill: { color: BLUE } });
    s.addText([{ text: b[0] + "\n", options: { bold: true, color: NAVY, fontSize: 9.5, breakLine: true } }, { text: b[1], options: { color: GRAY, fontSize: 8.6 } }],
      { x: 6.29, y: smy, w: 4.8, h: 0.62, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.1 });
    smy += 0.7;
  });
  quote(s, ML, 6.18, CW, 0.66, "\"문화 쇄신을 위한 에너지는 우리 내부에 존재했다. 우리는 둑을 무너뜨려 변화가 흐르게 했다.\"", "— Satya Nadella, 『히트 리프레시』 p162", false);
  takeaway(s, "제도(큰 변화)는 방향을 정하고, 넛지(작은 변화)는 일상에 스며든다 — 둘이 함께여야 문화가 바뀐다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p162");
}

// ====================== S23 HR SYSTEM REDESIGN ======================
{
  const s = pres.addSlide();
  body(s, "05. 구현", "[핵심] 성과평가·보상 제도의 재설계", "05. 구현", "2. HR 제도 재설계");
  govmsg(s, [{ t: "Stack Ranking을 폐지하고 " }, { t: "'상대평가·강제배분'을 '절대평가·상시 피드백'", b: true }, { t: "으로 재설계했다" }]);
  const colA = [[ML, 1.85, "차원"], [ML + 1.85, 4.15, "As-Is — Stack Ranking"], [ML + 6.0, 4.59, "To-Be — 재설계"]];
  colA.forEach((c, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: c[0], y: 1.64, w: c[1], h: 0.4, fill: { color: i === 0 ? NAVY : (i === 1 ? RED : BLUE) } });
    s.addText(c[2], { x: c[0] + 0.1, y: 1.64, w: c[1] - 0.16, h: 0.4, fontSize: 9, color: WHITE, bold: true, valign: "middle", fontFace: BODY, margin: 0 });
  });
  const prows = [
    ["평가 철학", "분류·도태 (Sort & Yank)", "성장·개발 (Grow & Develop)"],
    ["평가 방식", "상대평가 + 강제배분", "절대평가 — 개인의 절대적 기여·성장 기준"],
    ["평가 주기", "6개월마다 강제 서열화", "상시 피드백·코칭 (continual feedback & coaching)"],
    ["등급", "5등급 강제 분포 (10명 중 1명 必 poor)", "강제 분포 폐지"],
    ["보상 결정", "등급에 알고리즘으로 자동 연동", "매니저에게 '재량 보상 예산' 부여"],
    ["평가–보상 관계", "등급 = 곧 돈 (한 몸)", "평가(개발)와 보상(매니저 판단)을 부분 분리"],
  ];
  let ry = 2.04;
  prows.forEach((r, i) => {
    const h = 0.56;
    s.addShape(pres.shapes.RECTANGLE, { x: ML, y: ry, w: 1.85, h, fill: { color: LGRAY }, line: { color: MGRAY, width: 0.5 } });
    s.addText(r[0], { x: ML + 0.1, y: ry, w: 1.7, h, fontSize: 8.8, color: NAVY, bold: true, valign: "middle", fontFace: BODY, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: ML + 1.85, y: ry, w: 4.15, h, fill: { color: i % 2 ? "FCF4F2" : "FBEEEC" }, line: { color: MGRAY, width: 0.5 } });
    s.addText(r[1], { x: ML + 1.96, y: ry, w: 3.95, h, fontSize: 8.6, color: "8E3A30", valign: "middle", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.05 });
    s.addShape(pres.shapes.RECTANGLE, { x: ML + 6.0, y: ry, w: 4.59, h, fill: { color: i % 2 ? "F0F4FB" : "EAF0FA" }, line: { color: MGRAY, width: 0.5 } });
    s.addText(r[2], { x: ML + 6.11, y: ry, w: 4.39, h, fontSize: 8.6, color: "1F4B86", valign: "middle", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.05 });
    ry += h;
  });
  s.addText("케이스: \"The infamous stack-ranking system was abolished, replaced by continual feedback and coaching … managers are given a budget for compensation that they can hand out as they see fit.\"  ·  권기욱 칼럼: 상대평가→절대평가 전환, 관리자 권한 대폭 이양", { x: ML, y: 5.46, w: CW, h: 0.5, fontSize: 7.8, color: GRAY, italic: true, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.15 });
  const mean = [
    ["상대평가 → 절대평가", "'파이 나눠먹기'를 끝내고 각자의 절대적 성장을 본다 → 제로섬 구조 해체"],
    ["서열 → 상시 피드백", "평가가 '연 2회의 심판'에서 '일상의 코칭'으로 — 개발의 도구로 복귀"],
    ["평가·보상의 분리", "보상은 매니저가 맥락으로 판단 — 평가가 '돈'에서 풀려나 '사람'을 향한다"],
  ];
  let mx = ML;
  mean.forEach((m) => {
    card(s, mx, 6.1, 3.45, 1.1, LGRAY, true);
    s.addShape(pres.shapes.RECTANGLE, { x: mx, y: 6.1, w: 0.07, h: 1.1, fill: { color: BLUE } });
    s.addText([{ text: m[0] + "\n", options: { bold: true, color: NAVY, fontSize: 8.8, breakLine: true } }, { text: m[1], options: { color: GRAY, fontSize: 8 } }],
      { x: mx + 0.16, y: 6.1, w: 3.22, h: 1.1, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.18 });
    mx += 3.59;
  });
  footer(s, "출처: LBS128 케이스 / 권기욱 「조직문화 변화」 칼럼");
}

// ====================== S24 PILLARS GROUNDED ======================
{
  const s = pres.addSlide();
  body(s, "05. 구현", "3대 Pillar의 현장 구현 — 말이 행동이 되다", "05. 구현", "3. Pillar의 구현");
  govmsg(s, [{ t: "각 Pillar는 " }, { t: "구체적인 '현장의 행동'과 '제도'", b: true }, { t: "로 번역되었다" }]);
  const gr = [
    ["Customer Obsession", "고객 집착의 구현", BLUE, [
      "오스트리아 GM Dorothee Ritz — 직원들을 '고객의 현장'으로",
      "한 계정 매니저는 경찰서에서 1주일, 다른 매니저는 병원에서 2일을 보내며 고객의 일을 직접 관찰",
      "\"고객의 문제를 함께 푸는 것\"이 추상적 워크숍보다 강력했다",
    ]],
    ["Diversity & Inclusion", "다양성·포용의 구현", NAVY, [
      "훈련보다 '시니어 매니저의 행동 모델링'을 우선",
      "Xbox가 GDC 파티에서 부적절한 공연 → Phil Spencer가 신속히 공개 사과",
      "다양성 목표를 '수치'로 설정하고 시니어 경영진의 보너스에 연계 — 의도를 숫자로 못박다",
    ]],
    ["One Microsoft", "원 마이크로소프트의 구현", RED, [
      "연례 해커톤 OneWeek — 부서를 넘어 한 팀으로",
      "첫해 83개국 1만 2천여 명이 3천여 개 해커톤에 참여 (난독증 학습도구가 실제 제품에 탑재된 사례)",
      "직급·부서 자격을 깨고 피인수 기업 창업자를 임원 리트릿에 초대",
    ]],
  ];
  let gy = 1.64;
  gr.forEach((g) => {
    card(s, ML, gy, CW, 1.66);
    s.addShape(pres.shapes.RECTANGLE, { x: ML, y: gy, w: 2.35, h: 1.66, fill: { color: g[2] } });
    s.addText(g[0], { x: ML + 0.14, y: gy + 0.2, w: 2.1, h: 0.5, fontSize: 11, color: WHITE, bold: true, fontFace: HEAD, margin: 0 });
    s.addText(g[1], { x: ML + 0.14, y: gy + 0.78, w: 2.1, h: 0.6, fontSize: 9, color: "E6EBF4", fontFace: BODY, margin: 0, lineSpacingMultiple: 1.1 });
    s.addText(g[3].map((t) => ({ text: t, options: { bullet: { code: "2022" }, breakLine: true, paraSpaceAfter: 4 } })),
      { x: ML + 2.55, y: gy + 0.14, w: 7.85, h: 1.4, fontSize: 8.8, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.12, valign: "middle" });
    gy += 1.74;
  });
  takeaway(s, "Pillar는 '구호'가 아니다 — 현장 방문, 보너스 연계, 해커톤 같은 '구체적 행동·제도'로 번역됐다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p154");
}

// ====================== S25 ROLE MODELING ======================
{
  const s = pres.addSlide();
  body(s, "05. 구현", "리더의 솔선수범 — 취약성을 통한 신뢰", "05. 구현", "4. Role Modeling");
  govmsg(s, [{ t: "나델라는 자신의 공개적 실패를 " }, { t: "'성장 마인드셋의 시연'", b: true }, { t: "으로 전환했다" }]);
  const cases = [
    ["Grace Hopper 발언 사건", "2014. 10", RED, [
      "여성 컴퓨팅 학회에서 '임금 인상을 요구 못 하는 여성'에게 \"시스템을 믿고 기다리라\"고 답 → 거센 비판",
      "전 직원에게 이메일로 \"내가 그 질문에 완전히 잘못 답했다\"고 공개 인정",
      "자신의 편견을 탐구하고 임원진에게도 동일하게 요구",
    ], "Hogan: \"나는 Satya에 대한 신뢰가 줄지 않고 오히려 늘었다 — 그는 누구도 비난하지 않고, 그것을 자신의 책임으로 받아들였다.\""],
    ["Tay AI 챗봇 사건", "2016. 03", BLUE, [
      "출시 24시간 만에 트롤들에 의해 9.6만 개의 혐오 트윗 — 공개적 'humiliation'",
      "나델라는 개발팀에 \"계속 밀어붙여라. 나는 너희와 함께 있다\"고 메시지",
      "실패를 처벌하지 않고 학습으로 — 이후 개선된 Zo 출시",
    ], "실패를 '심리적 안전감(psychological safety)'을 구축하는 기회로 전환 — 리더가 먼저 취약성을 드러냈다."],
  ];
  let cx = ML;
  cases.forEach((c) => {
    card(s, cx, 1.66, 5.27, 4.6);
    s.addShape(pres.shapes.RECTANGLE, { x: cx, y: 1.66, w: 5.27, h: 0.5, fill: { color: c[2] } });
    s.addText(c[0], { x: cx + 0.2, y: 1.66, w: 3.6, h: 0.5, fontSize: 11, color: WHITE, bold: true, fontFace: HEAD, valign: "middle", margin: 0 });
    s.addText(c[1], { x: cx + 3.8, y: 1.66, w: 1.3, h: 0.5, fontSize: 9, color: WHITE, bold: true, fontFace: BODY, align: "right", valign: "middle", margin: 0 });
    s.addText(c[3].map((t) => ({ text: t, options: { bullet: { code: "2022" }, breakLine: true, paraSpaceAfter: 9 } })),
      { x: cx + 0.22, y: 2.34, w: 4.85, h: 2.3, fontSize: 9, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.18 });
    s.addShape(pres.shapes.RECTANGLE, { x: cx + 0.22, y: 4.78, w: 4.83, h: 1.36, fill: { color: LGRAY } });
    s.addShape(pres.shapes.RECTANGLE, { x: cx + 0.22, y: 4.78, w: 0.06, h: 1.36, fill: { color: c[2] } });
    s.addText(c[4], { x: cx + 0.4, y: 4.78, w: 4.6, h: 1.36, fontSize: 8.8, color: INK, italic: true, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.2 });
    cx += 5.39;
  });
  takeaway(s, "\"완벽한 리더\"가 아니라 \"학습하는 리더\" — 리더가 먼저 취약성을 드러내야 심리적 안전감이 생긴다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p165~168");
}

// ====================== S26 NUDGES ======================
{
  const s = pres.addSlide();
  body(s, "05. 구현", "일상의 넛지 — 환경에 심은 문화", "05. 구현", "5. 일상의 넛지");
  govmsg(s, [{ t: "변혁은 큰 조치가 아니라, " }, { t: "12.5만 명의 '일상'을 둘러싼 수많은 넛지", b: true }, { t: "로 내재화됐다" }]);
  const nd = [
    ["회의 마무리 리플렉션", "모든 회의를 \"이 회의는 Growth였나 Fixed였나? 왜?\"로 마무리 — 성찰의 습관화"],
    ["나델라의 월간 학습 영상", "CEO가 매달 자신의 배움을 공유 ('반쯤 마신 우유팩' 같은 자기 실수도) — 학습 문화 모델링"],
    ["엘리베이터의 한자 '聽'", "맞이 공간에 '경청'을 상징하는 한자 — 물리적 환경에 가치를 새기다"],
    ["식당 냅킨 홀더 메시지", "\"평생 학습자가 되라\" — 일상의 가장 사소한 접점까지 메시지를 심다"],
    ["10가지 포용 행동 리스트", "전 직원에게 배포, 하나를 골라 토론 — 추상적 가치를 구체적 행동으로"],
    ["『히트 리프레시』 전 직원 배포", "12.5만 명 전원에게 CEO의 책을 제공 — 비전 공유이자 문화 교육"],
  ];
  let nx = ML, ny = 1.66;
  nd.forEach((n, i) => {
    card(s, nx, ny, 3.45, 1.62);
    s.addShape(pres.shapes.OVAL, { x: nx + 0.18, y: ny + 0.18, w: 0.42, h: 0.42, fill: { color: BLUE } });
    s.addText(String(i + 1), { x: nx + 0.18, y: ny + 0.18, w: 0.42, h: 0.42, fontSize: 13, color: WHITE, bold: true, fontFace: HEAD, align: "center", valign: "middle", margin: 0 });
    s.addText(n[0], { x: nx + 0.72, y: ny + 0.18, w: 2.6, h: 0.44, fontSize: 9.6, color: NAVY, bold: true, fontFace: HEAD, valign: "middle", margin: 0, lineSpacingMultiple: 0.95 });
    s.addText(n[1], { x: nx + 0.2, y: ny + 0.68, w: 3.08, h: 0.86, fontSize: 8.6, color: GRAY, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.16, valign: "top" });
    nx += 3.57;
    if (i % 3 === 2) { nx = ML; ny += 1.74; }
  });
  quote(s, ML, 5.2, CW, 0.62, "\"문화 쇄신은 어려운 작업이다. 고통스러울 수도 있다. 사람들이 변화에 저항하는 근본적인 이유는 미지에 대한 두려움 때문이다.\"", "— Satya Nadella, 『히트 리프레시』 p163", false);
  takeaway(s, "\"단 하나의 큰 조치\"는 없다 — 회의·영상·냅킨까지, 일상의 모든 접점이 문화의 전달자가 된다");
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p163");
}

// ====================== 06 DIVIDER ======================
divider("06", "변화 — 퀸 모델로 확인하는 문화의 이동", "Transformation", [
  "As-Is(위계+시장)에서 To-Be(관계+혁신)로 — 좌표로 확인하는 변화",
  "4년의 성과, 그리고 케이스가 남긴 미해결 과제",
]);

// ====================== S28 CVF TO-BE ======================
{
  const s = pres.addSlide();
  body(s, "06. 변화", "퀸 모델로 본 To-Be — '관계 + 혁신'으로의 이동", "06. 변화", "1. CVF To-Be 좌표");
  govmsg(s, [{ t: "문화의 무게중심이 " }, { t: "'안정·통제'에서 '유연·재량' 축으로 이동", b: true }, { t: " — 위계·시장 → 관계·혁신" }]);
  cvfQuad(s, 1.55, 2.36, 4.3, 3.6, "tobe");
  card(s, 6.3, 1.66, 4.84, 4.7, LGRAY);
  s.addText("이동의 해석 — 무엇이 새 사분면을 채웠나", { x: 6.5, y: 1.78, w: 4.5, h: 0.3, fontSize: 11, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  const interp = [
    ["Clan (관계) 강화", "Stack Ranking 폐지·상시 코칭으로 협력이 가능해졌고, One Microsoft·SLT 재구성으로 '하나의 팀' 의식 형성", GRN],
    ["Adhocracy (혁신) 강화", "성장 마인드셋·실패 학습(Tay)·OneWeek 해커톤으로 '도전과 창의'가 일상이 됨", GRN],
    ["유의점 — '시장'을 버린 게 아니다", "경쟁력·실적(Market)을 포기한 것이 아니라, 부족했던 관계·혁신 축을 보강해 네 사분면의 '균형'을 재편한 것", NAVY],
  ];
  let iy = 2.16;
  interp.forEach((t) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.5, y: iy, w: 0.08, h: 1.16, fill: { color: t[2] } });
    s.addText([
      { text: t[0] + "\n", options: { bold: true, color: t[2] === GRN ? GRN : NAVY, fontSize: 9.8, breakLine: true } },
      { text: t[1], options: { color: INK, fontSize: 8.9 } },
    ], { x: 6.68, y: iy, w: 4.3, h: 1.16, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.22 });
    iy += 1.26;
  });
  takeaway(s, "'기존 문화가 어떻게 변했나'의 답 — 위계·시장 고착에서 관계·혁신으로, 좌표 자체가 이동했다");
  footer(s, "출처: LBS128 케이스 / 경쟁가치모형(Cameron & Quinn)으로 본 변화");
}

// ====================== S29 FOUR YEARS RESULTS ======================
{
  const s = pres.addSlide();
  body(s, "06. 변화", "4년의 성과 — 'lumbering giant'에서 '인재 자석'으로", "06. 변화", "2. 4년의 성과");
  govmsg(s, [{ t: "문화의 이동은 " }, { t: "시총 $700B·Glassdoor 95%의 성과", b: true }, { t: "로 이어졌다 (2018, 케이스 시점)" }]);
  const kpis = [["$700B", "시가총액 도달", "주가 사상 최고가 경신"], ["95%", "Fortune 500의 Azure 채택", "글로벌 50개 리전 — 클라우드 선두권"], ["29% → 95%", "CEO Glassdoor 지지율", "Ballmer → Nadella, 직원 신뢰 회복"], ["Top 5", "AI 기업 (직원 평가)", "최고 엔지니어링 인재의 '자석'으로"]];
  let kx = ML;
  kpis.forEach((k) => {
    card(s, kx, 1.66, 2.55, 1.62);
    s.addShape(pres.shapes.RECTANGLE, { x: kx, y: 1.66, w: 2.55, h: 0.08, fill: { color: GRN } });
    s.addText(k[0], { x: kx + 0.06, y: 1.82, w: 2.43, h: 0.6, fontSize: k[0].length > 6 ? 19 : 26, color: NAVY, bold: true, fontFace: HEAD, align: "center", valign: "middle", margin: 0 });
    s.addText(k[1], { x: kx + 0.1, y: 2.44, w: 2.35, h: 0.42, fontSize: 9.3, color: GRN, bold: true, fontFace: BODY, align: "center", valign: "middle", margin: 0, lineSpacingMultiple: 1.0 });
    s.addText(k[2], { x: kx + 0.12, y: 2.86, w: 2.31, h: 0.38, fontSize: 8, color: GRAY, fontFace: BODY, align: "center", valign: "top", margin: 0, lineSpacingMultiple: 1.05 });
    kx += 2.68;
  });
  card(s, ML, 3.5, CW, 1.5, LGRAY);
  s.addText("전략적 행동이 곧 '문화 시그널'이었다", { x: ML + 0.2, y: 3.62, w: 6, h: 0.3, fontSize: 10, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  const sig = [["Office → iOS/iPad 출시", "\"Windows 우선이 아닌 고객 우선\""], ["Linux 포용", "\"적을 만드는 대신 배우겠다\" (과거: Linux=암)"], ["LinkedIn $26B 인수", "\"외부 생태계와 통합하겠다\""]];
  let sx = ML + 0.2;
  sig.forEach((g) => {
    s.addShape(pres.shapes.RECTANGLE, { x: sx, y: 4.0, w: 0.07, h: 0.86, fill: { color: BLUE } });
    s.addText([{ text: g[0] + "\n", options: { bold: true, color: INK, fontSize: 9.3, breakLine: true } }, { text: g[1], options: { color: GRAY, fontSize: 8.6 } }],
      { x: sx + 0.16, y: 4.0, w: 3.3, h: 0.86, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.15, valign: "top" });
    sx += 3.5;
  });
  quote(s, ML, 5.22, CW, 0.78, "\"그들은 소문 속의 총을 내려놓고, 마이크로소프트가 사명을 완수할 새로운 방법을 발견했다.\"  (Exhibit 3의 '서로에게 총을 겨누던 조직도'를 떠올리게 하는 표현)", "— Satya Nadella, 『히트 리프레시』 p129", true);
  takeaway(s, "문화 변혁은 '비용'이 아니라 '성장 엔진' — 협력·혁신의 문화가 클라우드·AI 전환을 가능케 했다");
  footer(s, "출처: LBS128 케이스, Exhibit 2 / 『히트 리프레시』 p129");
}

// ====================== S30 UNRESOLVED ======================
{
  const s = pres.addSlide();
  body(s, "06. 변화", "케이스가 남긴 미해결 과제", "06. 변화", "3. 미해결 과제");
  govmsg(s, [{ t: "변혁은 Top과 현장은 움직였지만 — " }, { t: "'빠진 고리'와 '오용의 위험'", b: true }, { t: "을 남겼다" }]);
  card(s, ML, 1.66, 5.35, 4.62);
  secthdr(s, ML, 1.66, 5.35, "과제 ① — 'Missing Middle' (중간관리자)", RED);
  s.addText("취임 3년 후 설문에서 \"당신의 부사장·리더가 인재 육성에 우선순위를 두는가\"라는 질문의 응답이 오히려 악화됐다. 나델라가 직접 인정한 가장 큰 미해결 과제다.", { x: ML + 0.18, y: 2.16, w: 5.05, h: 0.86, fontSize: 9, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
  const lyr = [["최고경영진 · 시니어", "변혁에 적극 동참", GRN, "O"], ["중간관리자 (VP·그룹리더)", "인재 육성 지표 오히려 악화", RED, "X"], ["일반 직원 · 현장", "\"올바른 방향\"이라 응답", GRN, "O"]];
  let lyy = 3.04;
  lyr.forEach((L) => {
    const bad = L[2] === RED;
    s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.18, y: lyy, w: 4.99, h: 0.56, fill: { color: bad ? REDL : GRNL }, line: { color: L[2], width: 0.75 } });
    s.addShape(pres.shapes.OVAL, { x: ML + 0.3, y: lyy + 0.13, w: 0.3, h: 0.3, fill: { color: L[2] } });
    s.addText(L[3], { x: ML + 0.3, y: lyy + 0.13, w: 0.3, h: 0.3, fontSize: 10, color: WHITE, bold: true, align: "center", valign: "middle", fontFace: BODY, margin: 0 });
    s.addText([{ text: L[0] + "  —  ", options: { bold: true, color: INK, fontSize: 8.8 } }, { text: L[1], options: { color: bad ? "8E3A30" : GRAY, fontSize: 8.6 } }],
      { x: ML + 0.72, y: lyy, w: 4.4, h: 0.56, valign: "middle", fontFace: BODY, margin: 0 });
    lyy += 0.64;
  });
  quote(s, ML + 0.18, 5.04, 4.99, 0.66, "\"우리에게는 빠진 고리가 있었다. 중간 관리자였다.\"", "— 『히트 리프레시』 p173", false);
  s.addText("→ 중간관리자는 평가·보상 제도를 실제로 '운영'하는 집행 계층. 이들이 '관리자→코치'로 바뀌지 않으면 제도 개혁도 작동하지 않는다.", { x: ML + 0.18, y: 5.78, w: 5.05, h: 0.46, fontSize: 8, color: RED, italic: true, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.15 });
  card(s, 6.1, 1.66, 5.04, 4.62);
  secthdr(s, 6.1, 1.66, 5.04, "과제 ② — '거짓 성장 마인드셋'", RED);
  s.addText("한 매니저가 \"우리 팀원 5명은 성장 마인드셋이 없다\"고 보고하자, 나델라는 그것이 '성장 마인드셋을 남을 비판하는 새 도구로 쓴 것'이라며 일축했다.", { x: 6.28, y: 2.16, w: 4.7, h: 0.9, fontSize: 9, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
  quote(s, 6.28, 3.08, 4.68, 0.86, "\"여러분이 이 회사에서 리더가 되고 싶다면, 쓰레기통에서 보석을 찾아야 합니다.\"", "— Satya Nadella, 『히트 리프레시』 p174", false);
  s.addShape(pres.shapes.RECTANGLE, { x: 6.28, y: 4.1, w: 4.68, h: 2.04, fill: { color: NAVY } });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.28, y: 4.1, w: 0.07, h: 2.04, fill: { color: RED } });
  s.addText("변혁의 최대 리스크", { x: 6.46, y: 4.22, w: 4.4, h: 0.3, fontSize: 9.5, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText("\"새로운 언어, 오래된 행동\" — 좋은 제도·언어도 운영자가 오용하면 변질된다. 제도 개혁이 행동 변화를 '보장'하지는 않는다. 그리고 이 리스크는, PART 7에서 보듯 — '호황기'가 끝났을 때 가장 위험하게 드러난다.", { x: 6.46, y: 4.54, w: 4.4, h: 1.5, fontSize: 9.3, color: WHITE, bold: true, fontFace: HEAD, margin: 0, lineSpacingMultiple: 1.24, valign: "top" });
  footer(s, "출처: LBS128 케이스 / 『히트 리프레시』 p173~174");
}

// ====================== 07 DIVIDER ======================
divider("07", "그 후 — 케이스 이후, 현재까지 (2018→2026)", "Aftermath", [
  "케이스 이후의 성취 — 시총 $3조 돌파와 AI 시대의 주도",
  "2025년의 역설 — 사상 최대 이익 속의 대량 정리해고, 그리고 신뢰의 균열",
]);

// ====================== S32 AFTER THE CASE ======================
{
  const s = pres.addSlide();
  body(s, "07. 그 후", "케이스 이후의 성취 — 문화 변혁이 만든 'AI 시대의 주도권'", "07. 그 후", "1. 케이스 이후");
  govmsg(s, [{ t: "2018년 이후 Microsoft는 " }, { t: "시총 $3조를 돌파하고 AI 시대를 주도", b: true }, { t: "했다" }]);
  card(s, ML, 1.66, 5.35, 2.4, LGRAY);
  s.addText("케이스(2018) 이후의 궤적", { x: ML + 0.18, y: 1.78, w: 5, h: 0.3, fontSize: 10, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    "시가총액 $700B(2018) → $3조 돌파 — 세계 최고 수준 기업으로",
    "OpenAI와의 전략적 파트너십 — 생성형 AI 시대의 선두 주자로",
    "Azure·Copilot 등 클라우드·AI를 핵심 성장 엔진으로",
    "케이스가 그린 '협력·혁신의 문화'가 AI 전환의 토대가 되었다는 평가",
  ].map((m) => ({ text: m, options: { bullet: { code: "2022" }, breakLine: true, paraSpaceAfter: 7 } })),
    { x: ML + 0.2, y: 2.14, w: 5.0, h: 1.8, fontSize: 9, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.16 });
  card(s, ML, 4.22, 5.35, 2.06, NAVY);
  s.addText("케이스의 '해피엔딩'은 계속되는가?", { x: ML + 0.18, y: 4.34, w: 5, h: 0.3, fontSize: 10, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText("표면적으로 나델라의 문화 변혁은 '성공 신화'로 굳어졌다. 그러나 2025년, 그 신화에 균열을 내는 사건이 일어난다 — 사상 최대 이익 속의 대량 정리해고.", { x: ML + 0.18, y: 4.68, w: 5.0, h: 1.5, fontSize: 9.5, color: WHITE, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.26, valign: "top" });
  card(s, 6.1, 1.66, 5.04, 4.62, LGRAY);
  s.addText("왜 '그 후'를 보는가 — 케이스를 넘어선 질문", { x: 6.28, y: 1.78, w: 4.7, h: 0.3, fontSize: 10.5, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "케이스(2018)는 변혁의 '성공'에서 끝난다. 그러나 진짜 질문은 그 다음에 있다:\n\n", options: { color: INK, fontSize: 9.3, breakLine: true } },
    { text: "“성장 마인드셋·공감·One Microsoft의 문화는 — 호황기에만 작동하는가, 아니면 위기에도 지속되는가?”\n\n", options: { color: NAVY, fontSize: 10, bold: true, italic: true, breakLine: true } },
    { text: "PART 30에서 본 '거짓 성장 마인드셋'의 리스크 — '새로운 언어, 오래된 행동' — 이 위험은 2025년 대량 정리해고 국면에서 가장 첨예하게 시험대에 오른다.\n\n", options: { color: GRAY, fontSize: 9, breakLine: true } },
    { text: "→ 다음 장: 2025년의 역설", options: { color: RED, fontSize: 9, bold: true, italic: true } },
  ], { x: 6.28, y: 2.16, w: 4.7, h: 4.0, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.24, valign: "top" });
  takeaway(s, "케이스의 '해피엔딩' 이후가 진짜 시험대 — 문화는 위기에도 지속될 때 비로소 '진짜'다");
  footer(s, "출처: 외부 보도 종합 (케이스 이후 시점) — 본 분석의 케이스 범위는 2018년까지");
}

// ====================== S33 2025 LAYOFFS PARADOX ======================
{
  const s = pres.addSlide();
  body(s, "07. 그 후", "[핵심] 2025년의 역설 — 사상 최대 이익 속의 대량 정리해고", "07. 그 후", "2. 2025 정리해고");
  govmsg(s, [{ t: "\"모든 객관적 지표에서 번창하는데, 동시에 정리해고를 한다\" — " }, { t: "나델라가 부른 '수수께끼(enigma)'", b: true }]);
  // left: the numbers
  card(s, ML, 1.66, 5.35, 2.84);
  secthdr(s, ML, 1.66, 5.35, "규모 — 2025년 한 해의 정리해고", RED);
  const nums = [
    ["15,000명+", "2025년 한 해 누적 감원 — 회사 역사상 가장 공격적인 시기 중 하나"],
    ["9,000명", "2025년 7월 단일 라운드 — 전체 인력의 약 4%"],
    ["$80B+", "같은 해 AI 인프라(CapEx) 투자 — 감원과 동시에 진행"],
    ["사상 최대", "정리해고 와중에도 분기 이익·매출은 기록 경신"],
  ];
  let ny = 2.14;
  nums.forEach((n) => {
    s.addShape(pres.shapes.RECTANGLE, { x: ML + 0.18, y: ny, w: 1.3, h: 0.52, fill: { color: REDL } });
    s.addText(n[0], { x: ML + 0.2, y: ny, w: 1.26, h: 0.52, fontSize: 11, color: RED, bold: true, align: "center", valign: "middle", fontFace: HEAD, margin: 0 });
    s.addText(n[1], { x: ML + 1.6, y: ny, w: 3.6, h: 0.52, fontSize: 8.5, color: INK, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.1 });
    ny += 0.58;
  });
  // left bottom: enigma memo
  quote(s, ML, 4.66, 5.35, 1.62, "\"우리가 처한 시대의 불확실성과 겉보기의 모순(incongruence)을 인정하고 싶다. 모든 객관적 지표로 보면 Microsoft는 번창하고 있다 … 그런데도 우리는 정리해고를 단행했다.\"", "— Satya Nadella, 2025년 사내 메모 ('enigma' memo)", true);
  // right: why + interpretation
  card(s, 6.1, 1.66, 5.04, 2.7, LGRAY);
  s.addText("왜 — AI 시대의 구조조정 논리", { x: 6.28, y: 1.78, w: 4.7, h: 0.3, fontSize: 10.5, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "· AI 인프라에 천문학적 투자 → 비용 구조 재편 압박\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "· 관리 계층 축소(flattening) — 의사결정 속도 제고\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "· \"AI로 효율을 얻겠다\"면서 인력을 줄이는 빅테크 공통 흐름 (Meta·Amazon 등과 동시 진행)\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "→ '성장을 위한 고통'이라는 논리. 그러나 직원에게 그것은 — 공감·One Microsoft를 외쳐온 회사의 '말과 행동의 불일치'로 다가왔다.", options: { color: RED, fontSize: 9, bold: true } },
  ], { x: 6.28, y: 2.14, w: 4.7, h: 2.16, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
  // right bottom: the contradiction framing
  s.addShape(pres.shapes.RECTANGLE, { x: 6.1, y: 4.52, w: 5.04, h: 1.76, fill: { color: NAVY } });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.1, y: 4.52, w: 0.07, h: 1.76, fill: { color: RED } });
  s.addText("케이스의 가치와 충돌하는가?", { x: 6.28, y: 4.64, w: 4.7, h: 0.3, fontSize: 10, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText("케이스가 그린 '공감의 리더십'과 'One Microsoft(하나의 가족)'의 서사 — 그것을 외쳐온 CEO가 15,000명을 내보낸다. 이 '모순'은 본 발표 토론(S38)의 핵심 쟁점이 된다.", { x: 6.28, y: 4.98, w: 4.7, h: 1.24, fontSize: 9.3, color: WHITE, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.24, valign: "top" });
  takeaway(s, "2025년의 역설 — '공감의 문화'는 호황기의 산물인가, 위기에도 지킬 수 있는 원칙인가");
  footer(s, "출처: CNBC·GeekWire·Windows Central 등 외부 보도 종합 (2025) — 케이스 범위 밖, 참고용");
}

// ====================== S34 BACK TO OLD MICROSOFT ======================
{
  const s = pres.addSlide();
  body(s, "07. 그 후", "다시 '옛 Microsoft'로? — 신뢰의 균열과 나델라의 응답", "07. 그 후", "3. 신뢰의 균열");
  govmsg(s, [{ t: "직원들은 묻는다 — " }, { t: "\"우리가 극복했던 '옛 Microsoft'로 돌아가는 것 아닌가\"", b: true }]);
  card(s, ML, 1.66, 5.35, 2.7, REDL);
  s.addShape(pres.shapes.RECTANGLE, { x: ML, y: 1.66, w: 0.08, h: 2.7, fill: { color: RED } });
  s.addText("균열 — 내부에서 들리는 우려", { x: ML + 0.2, y: 1.78, w: 5, h: 0.3, fontSize: 10, color: RED, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    "일부 장기 근속 직원·전직 직원: 정리해고 처리 방식이 '나델라가 10년간 쌓은 따뜻한 환경'을 침식했다고 토로",
    "\"내부 경쟁, 소통 부재, 고용 불안 — 우리가 극복했던 '옛 Microsoft'의 징후가 다시 보인다\"",
    "사무실 복귀(주 3일) 의무화까지 겹치며 — '공감 부재'에 대한 직원 불만이 공개적으로 제기됨",
  ].map((m) => ({ text: m, options: { bullet: { code: "2022" }, breakLine: true, paraSpaceAfter: 8 } })),
    { x: ML + 0.2, y: 2.16, w: 5.0, h: 2.1, fontSize: 9, color: INK, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.18 });
  card(s, ML, 4.52, 5.35, 1.76, NAVY);
  s.addText("나델라의 응답 (2025.9)", { x: ML + 0.18, y: 4.62, w: 5, h: 0.3, fontSize: 9.5, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText("한 직원이 '회사 문화의 공감 부재'를 직접 제기하자, 나델라는 답했다 — \"리더십 팀과 나에 대한 피드백으로 받아들이겠다. 결국 우리는 더 잘할 수 있고, 더 잘할 것이다(we will do better).\"", { x: ML + 0.18, y: 4.94, w: 5.0, h: 1.26, fontSize: 9.3, color: WHITE, italic: true, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.24, valign: "top" });
  // right: 2026 + reading
  card(s, 6.1, 1.66, 5.04, 2.3, LGRAY);
  s.addText("2026년 — 구조조정은 계속된다", { x: 6.28, y: 1.78, w: 4.7, h: 0.3, fontSize: 10, color: NAVY, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "· 2026년, 미국 직원 약 8,750명 대상 '자발적 조기퇴직(mutual separation)' 프로그램 — 회사 첫 사례\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "· AI 핵심 부서·Azure 엔지니어링은 제외 — '레거시 역할 축소'가 목적임을 시사\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "· CFO: \"향후 회계연도에도 인력은 더 줄어들 것\"", options: { color: GRAY, fontSize: 9 } },
  ], { x: 6.28, y: 2.14, w: 4.7, h: 1.76, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
  card(s, 6.1, 4.12, 5.04, 2.16, NAVY);
  s.addText("HRM 관점의 읽기", { x: 6.28, y: 4.24, w: 4.7, h: 0.3, fontSize: 10, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "케이스의 교훈이 여기서 되돌아온다 — ", options: { color: "C7CFE0", fontSize: 9.2 } },
    { text: "문화는 '제도와 행동의 정합성'이 깨지는 순간 가장 빠르게 무너진다.", options: { color: WHITE, fontSize: 9.2, bold: true } },
    { text: " '공감'을 선언으로만 두고 '정리해고의 실행 방식'이 그것과 어긋나면 — 10년의 변혁도 흔들릴 수 있다. 나델라의 \"we will do better\"는 그 위험을 스스로 인정한 말이다.", options: { color: "C7CFE0", fontSize: 9.2 } },
  ], { x: 6.28, y: 4.56, w: 4.7, h: 1.66, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.26, valign: "top" });
  takeaway(s, "선언된 가치(공감)와 실행(정리해고 방식)의 정합성이 깨지면 — 문화 변혁의 성취도 되돌려질 수 있다");
  footer(s, "출처: CNBC·GeekWire·Fast Company 등 외부 보도 종합 (2025~2026) — 케이스 범위 밖, 참고용");
}

// ====================== 08 DIVIDER ======================
divider("08", "시사점 & 토론", "Implications & Discussion", [
  "전략 의도·HR 제도·문화의 '정합성'이라는 핵심 교훈",
  "시앤피컨설팅 실무 적용, 그리고 '공감 vs 정리해고'의 모순을 둘러싼 토론",
]);

// ====================== S36 KEY LESSON ======================
{
  const s = pres.addSlide();
  body(s, "08. 시사점", "핵심 교훈 — 전략 의도·HR 제도·문화의 '정합성'", "08. 시사점", "1. 핵심 교훈");
  govmsg(s, [{ t: "MS의 변혁과 그 흔들림 모두가 말한다 — " }, { t: "정합성(Alignment)이 조직 효과성을 결정한다", b: true }]);
  // left: transition table
  const C = [[ML, 1.55], [ML + 1.55, 2.55], [ML + 4.1, 2.55]];
  ["층위", "As-Is (Ballmer)", "To-Be (Nadella)"].forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: C[i][0], y: 1.66, w: C[i][1], h: 0.4, fill: { color: i === 0 ? NAVY : (i === 1 ? RED : BLUE) } });
    s.addText(h, { x: C[i][0] + 0.1, y: 1.66, w: C[i][1] - 0.16, h: 0.4, fontSize: 9, color: WHITE, bold: true, valign: "middle", fontFace: BODY, margin: 0 });
  });
  const tr = [
    ["전략 의도", "PC 수성 + 실적주의", "역량 강화(empower) + 클라우드·AI"],
    ["HR 제도", "Stack Ranking (상대·강제배분)", "절대평가 + 상시 피드백·재량 보상"],
    ["조직문화", "위계+시장 (Know-it-all)", "관계+혁신 (Learn-it-all)"],
  ];
  let ry = 2.06;
  tr.forEach((r) => {
    const h = 0.62;
    s.addShape(pres.shapes.RECTANGLE, { x: C[0][0], y: ry, w: C[0][1], h, fill: { color: LGRAY }, line: { color: MGRAY, width: 0.5 } });
    s.addText(r[0], { x: C[0][0] + 0.1, y: ry, w: C[0][1] - 0.16, h, fontSize: 9, color: NAVY, bold: true, valign: "middle", fontFace: BODY, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: C[1][0], y: ry, w: C[1][1], h, fill: { color: "FCF4F2" }, line: { color: MGRAY, width: 0.5 } });
    s.addText(r[1], { x: C[1][0] + 0.1, y: ry, w: C[1][1] - 0.18, h, fontSize: 8.5, color: "8E3A30", valign: "middle", fontFace: BODY, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: C[2][0], y: ry, w: C[2][1], h, fill: { color: "F0F4FB" }, line: { color: MGRAY, width: 0.5 } });
    s.addText(r[2], { x: C[2][0] + 0.1, y: ry, w: C[2][1] - 0.18, h, fontSize: 8.5, color: "1F4B86", valign: "middle", fontFace: BODY, margin: 0 });
    ry += h;
  });
  s.addText("→ 진단도 처방도 같은 3층위 — 전략 의도가 제도를, 제도가 문화를 만든다", { x: ML, y: 4.0, w: 6.65, h: 0.3, fontSize: 8.6, color: GRAY, italic: true, fontFace: BODY, margin: 0 });
  // change mgmt theory
  card(s, ML, 4.4, 6.65, 1.88, LGRAY);
  s.addText("변화관리 이론으로 본 종합", { x: ML + 0.18, y: 4.5, w: 5, h: 0.3, fontSize: 9.5, color: BLUE, bold: true, fontFace: BODY, margin: 0 });
  s.addText([
    { text: "Kotter 8단계  ", options: { bold: true, color: NAVY, fontSize: 8.7 } },
    { text: "위기감(위기)→추진연합(SLT)→비전(선언)→전파→장애제거(제도)→단기성과→정착(넛지)에 정확히 매핑.\n", options: { color: GRAY, fontSize: 8.7 } },
    { text: "Schein 3수준  ", options: { bold: true, color: NAVY, fontSize: 8.7 } },
    { text: "넛지(가시적 산물)→3대 Pillar(표방 가치)→\"누구나 성장한다\"(기본 가정)까지 깊이 파고듦.\n", options: { color: GRAY, fontSize: 8.7 } },
    { text: "단, Lewin의 '재동결'은 거부  ", options: { bold: true, color: RED, fontSize: 8.7 } },
    { text: "\"문화 쇄신은 종료일이 정해진 프로그램이 아니라 존재의 방식\"(p156) — 2025년의 흔들림이 이를 입증한다.", options: { color: GRAY, fontSize: 8.7 } },
  ], { x: ML + 0.18, y: 4.82, w: 6.3, h: 1.4, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.26, valign: "top" });
  // right: proposition
  card(s, 7.4, 1.66, 3.74, 4.62, NAVY);
  s.addText("핵심 명제", { x: 7.6, y: 1.8, w: 3.4, h: 0.32, fontSize: 12, color: "8FA3CC", bold: true, fontFace: BODY, margin: 0 });
  s.addText("문화는\n'전략·제도·행동'이\n한 방향일 때만\n변하고, 유지된다", { x: 7.6, y: 2.16, w: 3.4, h: 1.3, fontSize: 14, color: WHITE, bold: true, fontFace: HEAD, margin: 0, lineSpacingMultiple: 1.18 });
  s.addShape(pres.shapes.LINE, { x: 7.6, y: 3.6, w: 1.4, h: 0, line: { color: RED, width: 2 } });
  s.addText([
    { text: "· 제도 없이 문화만 외치면 → 구호로 끝난다\n\n", options: { color: "D6DEEC", fontSize: 9, breakLine: true } },
    { text: "· 철학 없이 제도만 바꾸면 → 중간관리자가 되돌린다\n\n", options: { color: "D6DEEC", fontSize: 9, breakLine: true } },
    { text: "· 선언(공감)과 실행(정리해고)이 어긋나면 → 10년의 변혁도 흔들린다", options: { color: WHITE, fontSize: 9, bold: true } },
  ], { x: 7.6, y: 3.78, w: 3.4, h: 2.4, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.1, valign: "top" });
  footer(s, "출처: LBS128 케이스 / Kotter·Schein 이론 / 『히트 리프레시』 p156");
}

// ====================== S37 PRACTICAL ======================
{
  const s = pres.addSlide();
  body(s, "08. 시사점", "실무 시사점 — 시앤피컨설팅 관점", "08. 시사점", "2. 실무 시사점");
  govmsg(s, [{ t: "MS 케이스는 컨설팅 펌의 '자기 진단'이자, " }, { t: "클라이언트 변혁 컨설팅의 '방법론'", b: true }, { t: "이다" }]);
  card(s, ML, 1.66, 5.22, 5.0);
  secthdr(s, ML, 1.66, 5.22, "① 시앤피컨설팅 — 자사 인사제도 관점", NAVY);
  s.addText([
    { text: "구조적 유사성\n", options: { bold: true, color: BLUE, fontSize: 10, breakLine: true } },
    { text: "컨설팅 펌의 직급체계·프로젝트 단가 기반 평가·보상은 본질적으로 상대평가·내부경쟁 압력이 크다 — MS의 Stack Ranking과 구조적으로 닮았다.\n\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "적용 방향\n", options: { bold: true, color: BLUE, fontSize: 10, breakLine: true } },
    { text: "· 프로젝트 평가를 '도태'가 아닌 '역량 성장 피드백'으로 재설계\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "· 컨설턴트 간 지식 공유·협업 기여를 보상에 반영 (One Microsoft식)\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "· 파트너의 Role Modeling — '실패한 제안·프로젝트'를 학습 자산으로 공유\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "· 경영 환경이 어려울 때일수록 '선언한 가치'와 '인력 운영'의 정합성을 지킬 것", options: { color: RED, fontSize: 9, bold: true } },
  ], { x: ML + 0.2, y: 2.2, w: 4.85, h: 4.3, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.34, valign: "top" });
  card(s, 5.97, 1.66, 5.22, 5.0);
  secthdr(s, 5.97, 1.66, 5.22, "② 클라이언트 — 컨설팅 서비스 관점", BLUE);
  s.addText([
    { text: "방법론 패키징\n", options: { bold: true, color: BLUE, fontSize: 10, breakLine: true } },
    { text: "'문화 진단(퀸 모델) → 전략 의도·HR 제도 정렬 → 변화관리 로드맵(Kotter)'을 컨설팅 상품으로 패키징.\n\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "경영진 설득 포인트\n", options: { bold: true, color: BLUE, fontSize: 10, breakLine: true } },
    { text: "\"재무가 멀쩡해도 문화 부정합은 미래 가치를 잠식한다\" — MS의 10년 주가 정체가 강력한 각성 메시지.\n\n", options: { color: INK, fontSize: 9, breakLine: true } },
    { text: "필수 설계 요소\n", options: { bold: true, color: RED, fontSize: 10, breakLine: true } },
    { text: "① 성과평가·보상 제도를 문화와 '함께' 설계  ② 중간관리자 역할 전환(관리자→코치) 프로그램 포함  ③ 구조조정·위기 국면의 '가치-실행 정합성' 가이드까지 컨설팅 범위에 포함", options: { color: INK, fontSize: 9 } },
  ], { x: 6.17, y: 2.2, w: 4.85, h: 4.3, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.3, valign: "top" });
  footer(s, "출처: 케이스 분석 기반 실무 적용 — 시앤피컨설팅 관점");
}

// ====================== S38 DISCUSSION ======================
{
  const s = pres.addSlide();
  body(s, "08. 토론", "생각해 볼 내용 — 네 가지 쟁점", "08. 시사점", "3. 토론");
  govmsg(s, [{ t: "정답을 찾는 게 아니라, " }, { t: "케이스의 교훈을 '우리 조직의 현실'에 비춰본다", b: true }]);
  const qs = [
    ["Q1", "공감 vs 대량 정리해고 — 모순인가?", "'공감'과 'One Microsoft(하나의 가족)'를 외쳐온 나델라가 2025년 15,000명을 내보냈다. 이것은 문화의 '배신'인가, 아니면 책임 있는 경영의 '불가피한 선택'인가? '성장 마인드셋' 문화는 호황기에만 작동하는가?", RED],
    ["Q2", "상대평가 vs 절대평가", "Stack Ranking은 GE에선 성공, MS에선 실패했다. 제도 자체의 문제인가, 산업·전략 맥락 적합성의 문제인가? 우리 산업엔 어느 쪽이 맞는가?", BLUE],
    ["Q3", "퀸 모델 — 문화는 '이동'시킬 수 있는가", "MS는 위계·시장에서 관계·혁신으로 좌표를 옮겼다. 그러나 '시장(경쟁)'을 완전히 버릴 수 없다면 — 네 사분면의 '이상적 균형'은 무엇이며, 우리 조직은 지금 어디에 있는가?", NAVY],
    ["Q4", "우리 조직에의 적용", "우리 회사(또는 한국 기업)에 이식한다면 — 가장 먼저 바꿀 평가·보상 제도는? 가장 큰 현실적 장벽은 'Missing Middle(중간관리자)'인가?", NAVY],
  ];
  let qx = ML, qy = 1.66;
  qs.forEach((q, i) => {
    card(s, qx, qy, 5.22, 2.34);
    s.addShape(pres.shapes.RECTANGLE, { x: qx, y: qy, w: 0.1, h: 2.34, fill: { color: q[3] } });
    s.addText(q[0], { x: qx + 0.22, y: qy + 0.14, w: 0.95, h: 0.55, fontSize: 25, color: q[3], bold: true, fontFace: HEAD, margin: 0 });
    s.addText(q[1], { x: qx + 1.12, y: qy + 0.14, w: 3.98, h: 0.6, fontSize: 11, color: INK, bold: true, fontFace: HEAD, margin: 0, lineSpacingMultiple: 1.05, valign: "middle" });
    s.addShape(pres.shapes.LINE, { x: qx + 0.24, y: qy + 0.8, w: 4.78, h: 0, line: { color: "ECEEF2", width: 1 } });
    s.addText(q[2], { x: qx + 0.26, y: qy + 0.9, w: 4.78, h: 1.36, fontSize: 9, color: GRAY, fontFace: BODY, margin: 0, lineSpacingMultiple: 1.22, valign: "top" });
    qx += 5.37;
    if (i % 2 === 1) { qx = ML; qy += 2.46; }
  });
  takeaway(s, "특히 Q1 — 케이스의 '해피엔딩' 너머, '공감의 문화'가 위기에도 진짜인지를 우리 스스로에게 물어보자");
  footer(s, "출처: 케이스 분석 + 외부 보도(2025~2026) 기반 토론 설계");
}

// ====================== S39 CLOSING ======================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: PW, h: 0.11, fill: { color: RED } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 8.16, w: PW, h: 0.11, fill: { color: RED } });
  s.addText("핵심 인사이트 5가지", { x: 0.85, y: 0.6, w: 10, h: 0.5, fontSize: 21, color: WHITE, bold: true, fontFace: HEAD, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 0.87, y: 1.14, w: 2.1, h: 0, line: { color: RED, width: 2.5 } });
  const ins = [
    "전략의 '의도'는 반드시 'HR 제도'로 번역된다 — 발머의 실적주의가 Stack Ranking을 낳았다",
    "변화의 출발점은 제도가 아니라 리더의 '인간관' — 나델라의 '공감'이 그 씨앗이었다",
    "문화 변혁 = 선언(미션) + 제도(평가·보상) + 행동(솔선수범) + 환경(넛지)의 정합성",
    "퀸 모델로 본 변화 — '위계+시장'에서 '관계+혁신'으로 좌표 자체가 이동했다",
    "문화는 '존재의 방식' — 선언과 실행이 어긋나면(2025 정리해고) 언제든 흔들린다",
  ];
  let iy = 1.46;
  ins.forEach((t, i) => {
    s.addShape(pres.shapes.OVAL, { x: 0.87, y: iy, w: 0.44, h: 0.44, fill: { color: RED } });
    s.addText(String(i + 1), { x: 0.87, y: iy, w: 0.44, h: 0.44, fontSize: 14, color: WHITE, bold: true, fontFace: HEAD, align: "center", valign: "middle", margin: 0 });
    s.addText(t, { x: 1.48, y: iy, w: 10.0, h: 0.44, fontSize: 11.5, color: "E4E8F1", fontFace: BODY, valign: "middle", margin: 0 });
    iy += 0.6;
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.85, y: 4.7, w: 9.99, h: 1.05, fill: { color: NAVY2 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.85, y: 4.7, w: 0.08, h: 1.05, fill: { color: RED } });
  s.addText([
    { text: "\"우리는 많은 진전을 이뤘지만 결코 완수하지 못할 것이다. 문화 쇄신은 시작일과 종료일이 정해진 프로그램이 아니다. 그것은 존재의 방식이다.\"\n", options: { color: WHITE, italic: true, fontSize: 11.5 } },
    { text: "— Satya Nadella, 『히트 리프레시』 p156", options: { color: "8FA3CC", fontSize: 9 } },
  ], { x: 1.12, y: 4.7, w: 9.5, h: 1.05, fontFace: BODY, valign: "middle", margin: 0, lineSpacingMultiple: 1.18 });
  s.addText("감사합니다  ·  Q & A", { x: 0.85, y: 6.05, w: 7, h: 0.5, fontSize: 19, color: WHITE, bold: true, fontFace: HEAD, margin: 0 });
  s.addText("건국대학교 경영대학원 MBA  ·  인적자원관리 (정혜정 교수)  ·  Case #7  ·  발표: 이석주", { x: 0.85, y: 6.58, w: 10, h: 0.32, fontSize: 9.5, color: "8FA3CC", fontFace: BODY, margin: 0 });
  pageNo++;
  s.addText(String(pageNo).padStart(2, "0"), { x: 11.05, y: 7.85, w: 0.45, h: 0.28, fontSize: 9, color: "8190B5", bold: true, fontFace: BODY, align: "right", margin: 0 });
}

pres.writeFile({ fileName: "MS_CaseStudy_발표자료_v5.pptx" }).then(() => console.log("DONE " + pageNo));
