// MS Case Study — HTML/CSS deck generator (McKinsey/BCG tone)
// pipeline: gen.js -> deck.html -> weasyprint -> PDF -> pdftoppm PNG -> pptxgenjs embed
const fs = require("fs");
const FD = "/sessions/cool-festive-turing/mnt/outputs/assets/fonts";

// ---- canvas: A4 landscape @96dpi = 1123 x 794 ----
const W = 1123, H = 794;
const RAIL = 13, ML = 58, CW = 1010, MR = ML + CW; // 1068

const CSS = `
@font-face{font-family:'P';src:url('file://${FD}/Pretendard-Regular.otf');font-weight:400}
@font-face{font-family:'P';src:url('file://${FD}/Pretendard-Medium.otf');font-weight:500}
@font-face{font-family:'P';src:url('file://${FD}/Pretendard-SemiBold.otf');font-weight:600}
@font-face{font-family:'P';src:url('file://${FD}/Pretendard-Bold.otf');font-weight:700}
@font-face{font-family:'P';src:url('file://${FD}/Pretendard-ExtraBold.otf');font-weight:800}
@font-face{font-family:'P';src:url('file://${FD}/Pretendard-Black.otf');font-weight:900}
@page{size:${W}px ${H}px;margin:0}
*{margin:0;padding:0;box-sizing:border-box}
html,body{font-family:'P',sans-serif}
.slide{position:relative;width:${W}px;height:${H}px;background:#fff;overflow:hidden;page-break-after:always}
.slide:last-child{page-break-after:auto}
:root{}
/* palette via classes */
.t-navy{color:#1F3864}.t-navy2{color:#2B4A7A}.t-blue{color:#2E5BBA}.t-blueink{color:#1F4B86}
.t-red{color:#C0392B}.t-ink{color:#222838}.t-gray{color:#5A6478}.t-gray2{color:#8A93A6}
.t-white{color:#fff}.t-green{color:#2F8F4E}.t-amber{color:#A9781F}.t-cloud{color:#C7CFE0}.t-steel{color:#8FA3CC}
.bg-navy{background:#1F3864}.bg-navy2{background:#2B4A7A}.bg-navy3{background:#26406B}
.bg-blue{background:#2E5BBA}.bg-red{background:#C0392B}.bg-lgray{background:#F5F6F9}
.bg-bluepale{background:#EAF0FA}.bg-redpale{background:#FBEEEC}.bg-greenpale{background:#EDF5EF}.bg-amberpale{background:#FAF3E4}
b,strong{font-weight:700}
.abs{position:absolute}
/* rail */
.rail{position:absolute;left:0;top:0;width:${RAIL}px;height:${H}px;background:#1F3864}
.rail-red{position:absolute;left:0;top:0;width:${RAIL}px;height:7px;background:#C0392B}
/* header */
.kick{position:absolute;top:40px;height:34px;display:block}
.kick .tick{position:absolute;left:${ML}px;top:0;width:6px;height:34px;background:#C0392B}
.kick .box{position:absolute;left:${ML+6}px;top:0;height:34px;background:#1F3864;color:#fff;font-weight:700;font-size:12.5px;
  letter-spacing:.3px;padding:0 16px;line-height:34px;white-space:nowrap}
.kick .sub{position:absolute;top:0;height:34px;line-height:34px;color:#5A6478;font-size:12px;font-weight:500}
.nav{position:absolute;right:${W-MR}px;top:38px;width:300px;text-align:right;line-height:1.45}
.nav .n1{color:#2E5BBA;font-weight:700;font-size:9px;letter-spacing:.2px}
.nav .n2{color:#9BA3B4;font-weight:500;font-size:9px}
/* governing message */
.gov{position:absolute;left:${ML}px;top:88px;width:${CW}px;color:#1F3864;font-weight:700;font-size:22px;letter-spacing:-.3px;line-height:1.32}
.gov .hl{color:#2E5BBA}
.govrule{position:absolute;left:${ML}px;top:140px;width:${CW}px;height:2px;background:#1F3864}
/* takeaway */
.take{position:absolute;left:${ML}px;width:${CW}px;height:42px;background:#1F3864;line-height:42px;overflow:hidden}
.take .tk{position:absolute;left:0;top:0;width:6px;height:42px;background:#C0392B}
.take .lb{color:#8FA3CC;font-weight:700;font-size:10px;letter-spacing:.4px;padding-left:20px}
.take .tx{color:#fff;font-size:11px;font-weight:500}
/* footer */
.foot{position:absolute;left:${ML}px;top:760px;width:${CW}px}
.foot .src{position:absolute;left:0;top:0;color:#A6AEBD;font-size:7.5px;font-weight:500}
.foot .mid{position:absolute;right:46px;top:0;color:#C2C8D3;font-size:7.5px;font-weight:500}
.foot .pg{position:absolute;right:0;top:-3px;color:#1F3864;font-weight:800;font-size:11px}
/* generic */
.card{position:absolute;background:#fff;border:1px solid #E1E3E9}
.card-flat{position:absolute;background:#fff;border:1px solid #E6E8ED}
.sechdr{position:absolute;height:30px;line-height:30px;color:#fff;font-weight:600;font-size:11px;padding-left:13px;letter-spacing:.2px}
.lbar{position:absolute;width:7px}
.tbar{position:absolute;height:6px}
.chip{position:absolute;border-radius:2px;font-weight:700;display:block;text-align:center}
.dot{position:absolute;border-radius:50%;text-align:center;color:#fff;font-weight:800}
.quote{position:absolute;overflow:hidden}
.quote .qbar{position:absolute;left:0;top:0;width:5px;height:100%}
.quote .qt{display:block;font-style:italic;line-height:1.5}
.quote .qs{display:block;font-weight:600}
.h-title{font-weight:700;color:#1F3864}
.lead{line-height:1.6}
.num-badge{position:absolute;border-radius:50%;color:#fff;font-weight:800;text-align:center}
table.cmp{position:absolute;border-collapse:collapse}
table.cmp td,table.cmp th{border:1px solid #DCDFE6;vertical-align:middle}
.arrowdown{position:absolute;text-align:center;color:#6B7C9E;font-size:10px}
`;

// ---------- helpers ----------
const esc = s => String(s);
function abs(x,y,w,h,extra){return `position:absolute;left:${x}px;top:${y}px;`+(w!=null?`width:${w}px;`:"")+(h!=null?`height:${h}px;`:"")+(extra||"");}

let PAGE = 0;
const slides = [];
function push(html){ slides.push(html); }

// master content-slide chrome
function chrome({kick, kickW, sub, n1, n2}){
  let h = `<div class="rail"></div><div class="rail-red"></div>`;
  h += `<div class="kick"><div class="tick"></div><div class="box">${kick}</div>`;
  const sl = ML+6+(kickW||120)+20;
  h += `<div class="sub" style="left:${sl}px;width:${748-sl}px;white-space:nowrap;overflow:hidden">${sub||""}</div></div>`;
  h += `<div class="nav"><div class="n1">${n1||""}</div><div class="n2">${n2||""}</div></div>`;
  return h;
}
function gov(runs){
  // runs: array of {t, hl}
  const inner = runs.map(r=> r.hl?`<span class="hl">${r.t}</span>`:`${r.t}`).join("");
  return `<div class="gov">${inner}</div><div class="govrule"></div>`;
}
function take(txt, y){
  y = y||702;
  return `<div class="take" style="top:${y}px"><div class="tk"></div>`+
    `<span class="lb">핵심 메시지</span><span class="tx">　${txt}</span></div>`;
}
function foot(src){
  PAGE++;
  return `<div class="foot"><div class="src">${src||""}</div>`+
    `<div class="mid">Microsoft Case Study · HRM #7</div>`+
    `<div class="pg">${String(PAGE).padStart(2,"0")}</div></div>`;
}
function card(x,y,w,h,extra){return `<div class="card" style="${abs(x,y,w,h,extra)}"></div>`;}
function cardF(x,y,w,h,extra){return `<div class="card-flat" style="${abs(x,y,w,h,extra)}"></div>`;}
function sechdr(x,y,w,txt,bg){return `<div class="sechdr" style="${abs(x,y,w,30)}background:${bg||'#1F3864'}">${txt}</div>`;}
function quote(x,y,w,h,txt,src,dark,fs){
  const bg = dark?"#1F3864":"#F5F6F9", bar=dark?"#C0392B":"#2E5BBA";
  const qc = dark?"#fff":"#222838", sc=dark?"#8FA3CC":"#5A6478";
  fs = fs||11;
  return `<div class="quote" style="${abs(x,y,w,h)}background:${bg}">`+
    `<div class="qbar" style="background:${bar}"></div>`+
    `<div style="position:absolute;left:18px;width:${w-32}px;top:0;height:${h}px;display:flex;flex-direction:column;justify-content:center">`+
    `<span class="qt" style="color:${qc};font-size:${fs}px">${txt}</span>`+
    `<span class="qs" style="color:${sc};font-size:8.5px;margin-top:5px">${src}</span></div></div></div>`;
}
// vcenter helper: wrap content vertically centered in a box
function vc(x,y,w,h,inner,extra){
  return `<div style="${abs(x,y,w,h,extra||'')}display:flex;align-items:center;justify-content:center">${inner}</div>`;
}
// numbered circle badge
function badge(x,y,d,n,bg,fs){
  return `<div class="num-badge" style="${abs(x,y,d,d)}background:${bg||'#2E5BBA'};font-size:${fs||13}px;line-height:${d}px">${n}</div>`;
}
// left accent bar
function lbar(x,y,h,col,w){return `<div class="lbar" style="${abs(x,y,(w||7),h)}background:${col}"></div>`;}
function tbar(x,y,w,col,h){return `<div class="tbar" style="${abs(x,y,w,(h||6))}background:${col}"></div>`;}

// ============================================================
// CVF 2x2 component — mode: 'concept' | 'asis' | 'tobe'
// ============================================================
function cvf(x,y,w,h,mode){
  const hw=w/2, hh=h/2;
  const tobe = mode==="tobe", asis = mode==="asis";
  // quadrant fills/text colors
  const Q = [
    // [label, sub, gx, gy, fill, txtcol]
    ["Clan  관계","협력 · 팀워크 · 인재개발", x, y,        tobe?"#E4EEE7":"#EEF1F6", tobe?"#2F8F4E":"#8A93A6"],
    ["Adhocracy  혁신","창의 · 모험 · 기업가정신", x+hw, y,  tobe?"#E4EEE7":"#EEF1F6", tobe?"#2F8F4E":"#8A93A6"],
    ["Hierarchy  위계","규칙 · 절차 · 통제 · 효율", x, y+hh, (asis)?"#FBEEEC":(mode==="concept"?"#EEF1F6":"#F2F3F5"), asis?"#C0392B":"#8A93A6"],
    ["Market  시장","경쟁 · 성과 · 결과지향", x+hw, y+hh, (asis)?"#FBEEEC":(mode==="concept"?"#EEF1F6":"#F2F3F5"), asis?"#C0392B":"#8A93A6"],
  ];
  let h2 = "";
  Q.forEach(q=>{
    h2 += `<div style="${abs(q[2],q[3],hw,hh)}background:${q[4]};border:2px solid #fff">`+
      `<div style="position:absolute;left:12px;top:11px;font-weight:700;font-size:11.5px;color:${q[5]}">${q[0]}</div>`+
      `<div style="position:absolute;left:12px;top:31px;font-size:8px;color:${q[5]}">${q[1]}</div></div>`;
  });
  // axis labels
  h2 += `<div style="${abs(x,y-22,w,18)}text-align:center;font-weight:700;font-size:9px;color:#1F3864">유연성 · 재량</div>`;
  h2 += `<div style="${abs(x,y+h+4,w,18)}text-align:center;font-weight:700;font-size:9px;color:#1F3864">안정성 · 통제</div>`;
  h2 += `<div style="${abs(x-46,y+hh-18,40,36)}font-weight:700;font-size:8.5px;color:#1F3864;text-align:center;line-height:1.25;display:flex;align-items:center;justify-content:center">내부 지향</div>`;
  h2 += `<div style="${abs(x+w+6,y+hh-18,40,36)}font-weight:700;font-size:8.5px;color:#1F3864;text-align:center;line-height:1.25;display:flex;align-items:center;justify-content:center">외부 지향</div>`;
  // markers
  if(asis){
    const mx=x+w*0.62-20, my=y+h*0.72-20;
    h2 += `<div class="dot" style="${abs(mx,my,40,40)}background:#C0392B;border:2px solid #fff;line-height:40px;font-size:9px">As-Is</div>`;
  }
  if(tobe){
    const ax=x+w*0.64-17, ay=y+h*0.74-17;
    h2 += `<div class="dot" style="${abs(ax,ay,34,34)}background:#E2B6B1;border:2px solid #fff;line-height:34px;font-size:8px;color:#8a4a42">As-Is</div>`;
    const bx=x+w*0.24-20, by=y+h*0.22-20;
    h2 += `<div class="dot" style="${abs(bx,by,40,40)}background:#2F8F4E;border:2px solid #fff;line-height:40px;font-size:9px">To-Be</div>`;
    // arrow line via svg
    h2 += `<svg style="${abs(x,y,w,h)}" width="${w}" height="${h}">`+
      `<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">`+
      `<path d="M0,0 L7,3 L0,6 Z" fill="#1F3864"/></marker></defs>`+
      `<line x1="${w*0.62}" y1="${h*0.70}" x2="${w*0.30}" y2="${h*0.30}" stroke="#1F3864" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#ah)"/></svg>`;
  }
  return h2;
}

// ============================================================
// SECTION DIVIDER
// ============================================================
function divider(num, kr, en, items){
  let h = `<div class="slide" style="background:#1F3864">`;
  h += `<div style="position:absolute;left:0;top:0;width:${W}px;height:9px;background:#C0392B"></div>`;
  h += `<div style="${abs(78,42,720,260)}font-weight:900;font-size:165px;color:#2B4A7A;line-height:1">${num}</div>`;
  h += `<div style="${abs(92,348,150,4)}background:#C0392B"></div>`;
  h += `<div style="${abs(92,364,900,22)}color:#7E8CAE;font-weight:700;font-size:11px;letter-spacing:3px">${en.toUpperCase()}</div>`;
  h += `<div style="${abs(92,394,960,86)}color:#fff;font-weight:800;font-size:33px;letter-spacing:-.5px;line-height:1.28">${kr}</div>`;
  if(items){
    let iy=520;
    items.forEach(it=>{
      h += `<div style="${abs(94,iy+5,11,11)}background:#C0392B"></div>`;
      h += `<div style="${abs(120,iy,920,30)}color:#C7CFE0;font-size:12px;font-weight:500;line-height:1.4">${it}</div>`;
      iy+=42;
    });
  }
  PAGE++;
  h += `<div style="${abs(W-260,760,200,20)}text-align:right;color:#3C5489;font-weight:600;font-size:8px">Microsoft Case Study</div>`;
  h += `<div style="${abs(W-58,754,40,22)}text-align:right;color:#8190B5;font-weight:800;font-size:11px">${String(PAGE).padStart(2,"0")}</div>`;
  h += `</div>`;
  push(h);
}

// ============================================================
// S1 — COVER
// ============================================================
{
  let h = `<div class="slide">`;
  h += `<div style="${abs(0,0,392,H)}background:#1F3864"></div>`;
  h += `<div style="${abs(0,0,392,9)}background:#C0392B"></div>`;
  h += `<div style="${abs(392,0,5,H)}background:#C0392B"></div>`;
  // triangle accent
  h += `<svg style="${abs(250,0,150,150)}" width="150" height="150"><path d="M0,0 L150,0 L75,150 Z" fill="#2B4A7A"/></svg>`;
  h += `<div style="${abs(46,212,320,250)}color:#fff;font-weight:900;font-size:46px;line-height:1.12;letter-spacing:-.5px">CASE<br>STUDY<br><span style="color:#C0392B">#7</span></div>`;
  h += `<div style="${abs(50,470,130,4)}background:#C0392B"></div>`;
  h += `<div style="${abs(50,488,320,60)}color:#AEB9D3;font-size:12px;font-weight:500;line-height:1.5">조직문화와 변화관리<br><span style="color:#7E8CAE;font-size:10.5px">Organizational Culture &amp; Change</span></div>`;
  h += `<div style="${abs(50,690,320,40)}color:#5C6E96;font-size:9.5px;font-weight:600;letter-spacing:.5px">LONDON BUSINESS SCHOOL · LBS128</div>`;
  // right
  const RX = 446;
  h += `<div style="${abs(RX,150,600,24)}color:#2E5BBA;font-weight:800;font-size:12px;letter-spacing:2.5px">HUMAN RESOURCE MANAGEMENT</div>`;
  h += `<div style="${abs(RX,184,640,140)}color:#1F3864;font-weight:900;font-size:47px;line-height:1.1;letter-spacing:-1px">Satya Nadella<br>at Microsoft</div>`;
  h += `<div style="${abs(RX,330,620,40)}color:#5A6478;font-style:italic;font-weight:600;font-size:19px">나델라는 어떻게 조직문화를 다시 세웠는가</div>`;
  h += `<div style="${abs(RX,392,210,4)}background:#1F3864"></div>`;
  h += `<div style="${abs(RX,410,610,24)}color:#222838;font-size:11.5px;font-weight:500">케이스 서사로 따라가는 문화 변혁 — 위기·각성·경청·선언·구현·변화, 그리고 그 후</div>`;
  // meta card
  h += card(RX,452,600,150,"background:#F5F6F9;border-color:#E3E5EA");
  const meta=[["분석 대상","Microsoft Corp.　·　London Business School Case LBS128 (2018)"],
    ["과　　목","인적자원관리 (정혜정 교수)　·　대학원 MBA 인사조직 전공"],
    ["발　표　자","이석주　　|　　2026. 5. 16"]];
  let my=476;
  meta.forEach(m=>{
    h += `<div style="${abs(RX+26,my,150,30)}color:#2E5BBA;font-weight:700;font-size:10.5px;line-height:30px">${m[0]}</div>`;
    h += `<div style="${abs(RX+182,my,400,30)}color:#222838;font-size:10.5px;line-height:30px">${m[1]}</div>`;
    my+=40;
  });
  h += `<div style="${abs(RX,622,600,30)}color:#5A6478;font-weight:700;font-size:10px">건국대학교 경영대학원 MBA</div>`;
  h += `</div>`;
  PAGE++;
  push(h);
}

// ============================================================
// S2 — CONTENTS
// ============================================================
{
  let h = `<div class="slide">`;
  h += `<div class="rail"></div><div class="rail-red"></div>`;
  h += `<div style="${abs(ML,46,300,52)}color:#1F3864;font-weight:900;font-size:33px;letter-spacing:-.5px">Contents</div>`;
  h += `<div style="${abs(ML+232,78,W-ML-232-46,3)}background:#1F3864"></div>`;
  h += `<div style="${abs(ML,104,700,22)}color:#5A6478;font-style:italic;font-size:11px;font-weight:500">나델라의 조직문화 구축 서사 — 8개 PART의 흐름</div>`;
  const toc=[
    ["01","위기","\"잃어버린 10년\" — 게이츠·발머 시대의 전략·HR 제도·문화","05"],
    ["02","각성","한 리더의 '공감' — 나델라와 성장 마인드셋의 씨앗","12"],
    ["03","경청","진단으로서의 첫 1년 — 인터뷰·포커스그룹·\"왜 존재하는가\"","15"],
    ["04","선언","\"Know-it-all에서 Learn-it-all로\" — 새 미션과 3대 Pillar","18"],
    ["05","구현","문화를 일상에 심다 — 제도 재설계·솔선수범·넛지","23"],
    ["06","변화","퀸 모델로 확인하는 문화의 이동 — 성과와 미해결 과제","30"],
    ["07","그 후","케이스 이후, 현재까지 (2018→2026) — 2025년 대량 정리해고","34"],
    ["08","시사점 &amp; 토론","전략·제도·문화의 정합성, 실무 시사점, 그리고 토론","38"],
  ];
  let ty=142;
  toc.forEach(t=>{
    h += card(ML,ty,CW,64);
    h += `<div style="${abs(ML,ty,76,64)}background:#1F3864;color:#fff;font-weight:900;font-size:20px;text-align:center;line-height:64px">${t[0]}</div>`;
    h += `<div style="${abs(ML+97,ty,180,64)}color:#1F3864;font-weight:800;font-size:15px;line-height:64px">${t[1]}</div>`;
    h += `<div style="${abs(ML+278,ty+18,1,28)}background:#D6D9E0"></div>`;
    h += `<div style="${abs(ML+300,ty,CW-300-104,64)}color:#5A6478;font-size:11px;font-weight:500;line-height:64px;overflow:hidden">${t[2]}</div>`;
    h += `<div style="${abs(ML+CW-92,ty,76,64)}color:#2E5BBA;font-weight:800;font-size:12.5px;text-align:right;line-height:64px">p.${t[3]}</div>`;
    ty+=72;
  });
  h += foot("");
  h += `</div>`;
  push(h);
}

// ============================================================
// S3 — STORYLINE
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"발표 개요",kickW:78,sub:"스토리라인 — 케이스 서사를 따라가는 7막의 흐름",n1:"발표 개요",n2:"분석 Storyline"});
  h += gov([{t:"본 발표는 케이스의 서사를 "},{t:"'위기 → 각성 → 경청 → 선언 → 구현 → 변화 → 그 후'",hl:1},{t:"로 따라간다"}]);
  const arc=[["01","위기","영혼을 잃은 회사","CRISIS","재무는 멀쩡, 시장은 불신","#C0392B"],
    ["02","각성","한 리더의 '공감'","AWAKENING","Zain·Dweck — 변화의 씨앗","#1F3864"],
    ["03","경청","진단으로서의 1년","LISTENING","수백 명 인터뷰·포커스그룹","#1F3864"],
    ["04","선언","Learn-it-all 선언","DECLARATION","새 미션·3대 Pillar","#2E5BBA"],
    ["05","구현","문화를 일상에 심다","GROUNDING","제도·솔선수범·넛지","#2E5BBA"],
    ["06","변화","퀸 모델로 본 이동","TRANSFORMATION","위계+시장 → 관계+혁신","#2F8F4E"],
    ["07","그 후","케이스 이후의 역설","AFTERMATH","2025년 대량 정리해고","#A9781F"]];
  const aw=131, ag=15.5; let ax=ML;
  arc.forEach((a,i)=>{
    h += card(ax,162,aw,118);
    h += `<div style="${abs(ax,162,aw,34)}background:${a[5]};color:#fff;font-weight:800;font-size:11px;text-align:center;line-height:34px">${a[0]}　${a[1]}</div>`;
    h += `<div style="${abs(ax+7,202,aw-14,16)}color:#9AA3B4;font-weight:700;font-size:6.5px;letter-spacing:1px;text-align:center">${a[3]}</div>`;
    h += `<div style="${abs(ax+7,216,aw-14,22)}color:#1F3864;font-size:11px;font-weight:700;text-align:center">${a[2]}</div>`;
    h += `<div style="${abs(ax+7,240,aw-14,32)}color:#5A6478;font-size:8px;font-weight:500;text-align:center;line-height:1.35">${a[4]}</div>`;
    if(i<6) h += `<div style="${abs(ax+aw-1,162,18,118)}color:#C9CFDA;font-size:11px;text-align:center;line-height:118px">▶</div>`;
    ax += aw+ag;
  });
  // Quinn spine
  h += `<div style="${abs(ML,296,CW,134)}background:#1F3864"></div>`;
  h += `<div style="${abs(ML,296,7,134)}background:#C0392B"></div>`;
  h += `<div style="${abs(ML+26,316,640,22)}color:#fff;font-weight:700;font-size:13px">분석의 척추 — Cameron &amp; Quinn 경쟁가치모형(CVF)</div>`;
  h += `<div style="${abs(ML+26,344,CW-260,72)}color:#C7CFE0;font-size:10.5px;line-height:1.62">`+
    `퀸 모델이 서사의 <b style="color:#fff">양 끝을 잡는다</b> — PART 1에서 Ballmer 시대의 As-Is 좌표(위계+시장 고착)를 찍고, PART 6에서 Nadella 전환 후의 To-Be(관계+혁신)로의 이동을 같은 좌표 위에서 확인한다. '기존 문화가 어떻게 변했는가'를 추적하는 단일 척도.</div>`;
  h += `<div style="${abs(ML+CW-208,318,184,90)}background:#26406B;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(ML+CW-190,332,158,16)}color:#8FA3CC;font-size:8.5px;font-weight:800;letter-spacing:1px">BOOKEND</div>`;
  h += `<div style="${abs(ML+CW-190,352,158,46)}color:#fff;font-size:10.5px;font-weight:700;line-height:1.5">As-Is 좌표　→　To-Be 좌표<br><span style="color:#C7CFE0;font-weight:500;font-size:9.5px">PART 1　·　PART 6</span></div>`;
  // analysis tools
  h += `<div style="${abs(ML,446,200,18)}color:#2E5BBA;font-weight:700;font-size:11px">그 외 분석 도구</div>`;
  h += `<div style="${abs(ML+90,449,400,14)}color:#9AA3B4;font-size:8.5px;font-weight:500">— 케이스 서사를 보조하는 4개 이론·자료 렌즈</div>`;
  const th=[["성장 마인드셋","Carol Dweck — 고정형 vs 성장형 사고","PART 2·4 변혁 원리의 이론적 근간"],
    ["성과평가 이론","상대·절대평가, 강제배분, 목표대체·calibration","PART 1 진단 · PART 5 제도 재설계"],
    ["변화관리 이론","Kotter 8단계 · Schein 문화 3수준","PART 8에서 변혁 과정의 종합 해석"],
    ["1차 자료의 활용","케이스 원문 + 나델라 『히트 리프레시』","전 PART에 걸쳐 페이지 단위 직접 인용"]];
  const tw=242, tg=14.67; let tx=ML;
  th.forEach(t=>{
    h += card(tx,468,tw,178);
    h += `<div style="${abs(tx,468,7,178)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(tx+20,488,tw-36,24)}color:#1F3864;font-weight:800;font-size:13px">${t[0]}</div>`;
    h += `<div style="${abs(tx+20,512,tw-36,2)}background:#E1E3E9"></div>`;
    h += `<div style="${abs(tx+20,524,tw-36,58)}color:#5A6478;font-size:9.5px;line-height:1.55">${t[1]}</div>`;
    h += `<div style="${abs(tx+20,596,tw-36,34)}background:#F0F3F8;border-left:3px solid #2E5BBA"></div>`;
    h += `<div style="${abs(tx+30,602,tw-50,22)}color:#1F4B86;font-size:8.5px;font-weight:600;line-height:1.3;display:flex;align-items:center;height:22px">${t[2]}</div>`;
    tx += tw+tg;
  });
  h += take("케이스 서사 + 경쟁가치모형 — '제도가 문화를 만든다'는 인과의 사슬을 좌표 위에서 추적한다");
  h += foot("출처: LBS128 케이스 / 분석 프레임 — 케이스 서사 + 경쟁가치모형(CVF)");
  h += `</div>`;
  push(h);
}

// ============================================================
// S4 — QUINN MODEL CONCEPT
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"발표 개요",kickW:78,sub:"분석의 척추 — Cameron & Quinn 경쟁가치모형이란",n1:"발표 개요",n2:"퀸 경쟁가치모형"});
  h += gov([{t:"조직문화를 두 축으로 4유형으로 나누는 "},{t:"'경쟁가치모형(Competing Values Framework)'",hl:1}]);
  // left: 2x2 inside a framed card
  h += card(ML,162,470,484,"background:#FAFBFC;border-color:#E1E3E9");
  h += `<div style="${abs(ML+24,182,420,20)}color:#1F3864;font-weight:700;font-size:12px">경쟁가치모형 — 2×2 문화 지형도</div>`;
  h += `<div style="${abs(ML+24,202,420,1)}background:#E1E3E9"></div>`;
  h += cvf(ML+92,266,326,272,"concept");
  h += `<div style="${abs(ML+24,588,422,40)}background:#EEF1F6;border-left:3px solid #1F3864"></div>`;
  h += `<div style="${abs(ML+38,596,400,26)}color:#1F3864;font-size:9px;font-weight:600;line-height:1.4;display:flex;align-items:center;height:24px">두 축의 교차로 만들어지는 네 사분면 — 어느 조직도 네 문화를 모두 갖되, 무게중심이 다르다</div>`;
  // right: explanation card
  h += card(540,162,528,484,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(564,182,480,22)}color:#1F3864;font-weight:700;font-size:13px">개념 — 무엇을 보는 도구인가</div>`;
  h += `<div style="${abs(564,210,484,2)}background:#1F3864"></div>`;
  h += `<div style="${abs(564,222,484,118)}color:#222838;font-size:10.5px;line-height:1.62">`+
    `미시간대 <b>Robert Quinn &amp; Kim Cameron</b>이 개발한 진단 도구. 조직문화를 <b style="color:#2E5BBA">두 개의 가치 축</b>으로 좌표화한다.<br>`+
    `<span style="color:#5A6478">· 세로축 : 유연성·재량　↔　안정성·통제</span><br>`+
    `<span style="color:#5A6478">· 가로축 : 내부 지향　↔　외부 지향</span><br>`+
    `두 축이 만나 <b style="color:#2E5BBA">4가지 문화 유형</b>이 나온다. '경쟁가치'란 협력 vs 경쟁처럼 동시에 추구하기 어려운 가치들의 본질적 긴장을 뜻한다.</div>`;
  h += `<div style="${abs(564,346,484,16)}color:#2E5BBA;font-weight:700;font-size:10px">네 가지 문화 유형</div>`;
  const types=[
    ["Clan (관계문화)","가족적·협력적. 리더=멘토. 인재 개발과 몰입이 성공 기준","#8A93A6"],
    ["Adhocracy (혁신문화)","창의적·모험적. 리더=기업가. 혁신과 새 시도가 성공 기준","#8A93A6"],
    ["Hierarchy (위계문화)","공식적·구조적. 리더=조정자. 효율·안정·통제가 성공 기준","#C0392B"],
    ["Market (시장문화)","경쟁적·성과중심. 리더=관리자. 실적·점유율이 성공 기준","#C0392B"]];
  let ty=368;
  types.forEach(t=>{
    h += card(564,ty,484,60,"background:#fff;border-color:#E6E8ED");
    h += `<div style="${abs(564,ty,7,60)}background:${t[2]}"></div>`;
    h += `<div style="${abs(584,ty+10,460,20)}color:#222838;font-weight:700;font-size:11px">${t[0]}</div>`;
    h += `<div style="${abs(584,ty+31,452,20)}color:#5A6478;font-size:9.5px;line-height:1.4">${t[1]}</div>`;
    ty += 67;
  });
  h += take("본 발표는 As-Is(위계+시장 고착) → To-Be(관계+혁신으로 이동)를 이 좌표 위에서 추적한다");
  h += foot("출처: Cameron & Quinn, Diagnosing and Changing Organizational Culture (경쟁가치모형)");
  h += `</div>`;
  push(h);
}

divider("01","위기 — \"잃어버린 10년\", 영혼을 잃은 회사","Crisis",[
  "재무는 멀쩡한데 죽어가던 회사 — 게이츠·발머 시대의 전략과 의도",
  "전략을 떠받친 HR 제도(Stack Ranking)와 그것이 낳은 조직문화",
]);

// ============================================================
// S6 — LOST DECADE
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"01. 위기",kickW:70,sub:"\"잃어버린 10년\" — 재무 성장과 시장 불신의 괴리",n1:"01. 위기",n2:"1. 잃어버린 10년"});
  h += gov([{t:"매출은 3배 늘었지만 "},{t:"주가는 10년간 정체",hl:1},{t:"했다 — 재무제표에 잡히지 않는 위기"}]);
  // left: chart card
  const LW=494;
  h += card(ML,162,LW,272);
  h += `<div style="${abs(ML+22,180,LW-160,18)}color:#1F3864;font-weight:700;font-size:11.5px">Microsoft 주가 추이 (2000–2018)</div>`;
  h += `<div style="${abs(ML+LW-110,180,90,18)}color:#9AA3B4;font-weight:800;font-size:9px;text-align:right;letter-spacing:.5px">EXHIBIT 1</div>`;
  h += `<div style="${abs(ML+22,200,LW-44,1)}background:#E1E3E9"></div>`;
  {
    const vals=[24,26,27,28,22,26,29,38,60,95], labs=["'00","'02","'04","'06","'08","'10","'12","'14","'16","'18"];
    const ox=48, oy=16, cw=406, ch=176;
    let pts=vals.map((v,i)=>[ox+i*(cw/9), oy+ch-(v/100)*ch]);
    let poly=pts.map(p=>`${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");
    let area=`${ox},${oy+ch} `+poly+` ${ox+cw},${oy+ch}`;
    let grid="";
    for(let g=0;g<=4;g++){let gy=oy+ch-(g/4)*ch; grid+=`<line x1="${ox}" y1="${gy.toFixed(1)}" x2="${ox+cw}" y2="${gy.toFixed(1)}" stroke="#ECEEF2" stroke-width="1"/>`+
      `<text x="${ox-8}" y="${(gy+3).toFixed(1)}" font-size="8" fill="#9AA3B4" text-anchor="end">$${g*25}</text>`;}
    let bx2=ox+7*(cw/9);
    let labels=labs.map((l,i)=>`<text x="${(ox+i*(cw/9)).toFixed(1)}" y="${oy+ch+15}" font-size="8" fill="#9AA3B4" text-anchor="middle">${l}</text>`).join("");
    let dots=pts.map(p=>`<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="2.8" fill="#fff" stroke="#2E5BBA" stroke-width="1.6"/>`).join("");
    h += `<svg style="${abs(ML+18,206,LW-36,222)}" width="${LW-36}" height="222">`+
      `<rect x="${ox}" y="${oy}" width="${(bx2-ox).toFixed(1)}" height="${ch}" fill="#FBEEEC"/>`+
      grid+
      `<polygon points="${area}" fill="#2E5BBA" opacity="0.07"/>`+
      `<polyline points="${poly}" fill="none" stroke="#2E5BBA" stroke-width="2.6"/>`+dots+labels+
      `<text x="${(ox+bx2)/2}" y="${oy+30}" font-size="8.5" fill="#C0392B" font-weight="bold" text-anchor="middle">◀ Ballmer 재임 — 10년 정체</text>`+
      `<text x="${ox+cw-4}" y="${oy+ch-150}" font-size="8.5" fill="#2E5BBA" font-weight="bold" text-anchor="end">Nadella 이후 급등 ▶</text>`+
      `</svg>`;
  }
  // left: dark quote below chart
  h += quote(ML,446,LW,190,"\"관료주의가 혁신을 대체했고, 사내 정치가 팀워크를 대신했다. 우리는 낙오했다. 우리는 한때 우리를 위대하게 만들었던 것을 잃어버렸다.\"","— Satya Nadella, 『히트 리프레시』 p19",true,12.5);
  // right: 5 symptoms
  const RX=576, RW=492;
  h += `<div style="${abs(RX,164,RW,20)}color:#2E5BBA;font-weight:800;font-size:12px">'잃어버린 10년'의 5대 증상</div>`;
  h += `<div style="${abs(RX,166,RW,18)}color:#9AA3B4;font-size:8.5px;font-weight:500;text-align:right">재무는 멀쩡, 미래는 잠식</div>`;
  const sym=[
    ["핵심 인재 유출","2004년부터 Google 등으로 이탈 — Google은 업계 평균 대비 +23% 보상을 제시했다"],
    ["시장 선점 기회 상실","e-book(1998)·태블릿·스마트폰 핵심 기술이 사내 정치 속에 \"killed or delayed\""],
    ["제품 경쟁의 연패","Bing은 Google 검색을, Zune은 iPod을, Windows Phone은 iOS를 끝내 이기지 못함"],
    ["리더십 신뢰 붕괴","Ballmer Glassdoor 지지율 29% — 당시 Page 94% · Zuckerberg 99%와 극명한 대비"],
    ["산업 트렌드 역행","데스크톱→스마트폰 전환기에 Windows를 \"안전담요(security blanket)처럼\" 고수"]];
  let sy=190;
  sym.forEach((m,i)=>{
    h += card(RX,sy,RW,84);
    h += `<div class="num-badge" style="${abs(RX+16,sy+27,30,30)}background:#C0392B;font-size:13px;line-height:30px">${i+1}</div>`;
    h += `<div style="${abs(RX+60,sy+15,RW-78,18)}color:#1F3864;font-weight:700;font-size:11px">${m[0]}</div>`;
    h += `<div style="${abs(RX+60,sy+35,RW-80,40)}color:#5A6478;font-size:9px;line-height:1.5">${m[1]}</div>`;
    sy+=89;
  });
  h += take("주가는 미래 가치의 거울 — 시장은 재무제표가 아니라 '조직의 미래 역량'을 불신했다");
  h += foot("출처: LBS128 케이스, Exhibit 1 / 『히트 리프레시』 p19");
  h += `</div>`;
  push(h);
}

// ============================================================
// S7 — GATES / BALLMER STRATEGY
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"01. 위기",kickW:70,sub:"게이츠·발머의 경영전략과 그 '의도'",n1:"01. 위기",n2:"2. 기존 경영전략"});
  h += gov([{t:"기존 경영진의 전략은 "},{t:"'PC 시대의 지배를 지키는 것'",hl:1},{t:" — 그 의도가 조직을 빚었다"}]);
  const LW=520;
  h += card(ML,162,LW,266);
  h += sechdr(ML,162,LW,"전략과 의도 — 무엇을 지키려 했는가","#1F3864");
  const strat=[
    ["Gates의 창업 미션 (1975–2000)","\"A computer on every desk and in every home\" — PC의 보편화. 한 시대를 지배한 명료한 비전이었다"],
    ["Ballmer의 수성 전략 (2000–2014)","Windows·Office라는 '캐시카우'를 방어. 산업이 모바일·클라우드로 가는데도 PC 프랜차이즈에 고착했다"],
    ["경영의 핵심 의도","'책임(accountability)과 실적'의 극대화 — 정시 납기·숫자 달성이 모든 것에 우선. 개인 성과를 쥐어짜는 경영"]];
  let sty=212;
  strat.forEach(t=>{
    h += `<div style="${abs(ML+24,sty+5,10,10)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(ML+44,sty,LW-68,18)}color:#1F3864;font-weight:700;font-size:11.5px">${t[0]}</div>`;
    h += `<div style="${abs(ML+44,sty+21,LW-70,42)}color:#5A6478;font-size:9.5px;line-height:1.55">${t[1]}</div>`;
    sty+=70;
  });
  h += card(ML,440,LW,196,"background:#FBEEEC;border-color:#EBC9C3");
  h += lbar(ML,440,196,"#C0392B");
  h += `<div style="${abs(ML+26,460,LW-44,20)}color:#C0392B;font-weight:800;font-size:12px">전략의 역설 — 성공이 곧 함정이었다</div>`;
  h += `<div style="${abs(ML+26,488,LW-50,130)}color:#222838;font-size:10px;line-height:1.65">발머 재임 14년간 매출은 <b>3배</b>·이익은 <b>2배</b> 늘었다. 재무 지표만 보면 성공한 경영이었다. 그러나 '수성'에 갇힌 전략은 모바일·클라우드 전환을 놓쳤고, '실적 압박'이라는 의도는 다음 장의 HR 제도(Stack Ranking)로 제도화되어 — 조직의 행동과 문화를 정밀하게 (잘못된 방향으로) 설계했다.</div>`;
  // right: causal chain
  const RX=602, RW=466;
  h += card(RX,162,RW,474,"background:#1F3864;border-color:#1F3864");
  h += `<div style="${abs(RX+24,184,RW-40,22)}color:#fff;font-weight:700;font-size:12.5px">전략의 의도가 조직을 빚는 인과 사슬</div>`;
  h += `<div style="${abs(RX+24,210,RW-48,1)}background:#3A547F"></div>`;
  const chain=[
    ["전략 의도","PC 시대 수성 + 책임·실적의 극대화","#C0392B"],
    ["HR 제도","Stack Ranking — 개인을 줄 세우는 강제평가","#A9781F"],
    ["구성원 행동","내부 경쟁·정치, 위험 회피, 지식 비공유","#2E5BBA"],
    ["조직문화","사일로 + Know-it-all (과시의 문화)","#8FA3CC"]];
  let cy=226;
  chain.forEach((c,i)=>{
    h += `<div style="${abs(RX+24,cy,RW-48,72)}background:#26406B"></div>`;
    h += `<div style="${abs(RX+24,cy,7,72)}background:${c[2]}"></div>`;
    h += `<div style="${abs(RX+44,cy+14,RW-80,18)}color:#fff;font-weight:700;font-size:11.5px">${c[0]}</div>`;
    h += `<div style="${abs(RX+44,cy+34,RW-80,28)}color:#C7CFE0;font-size:9.5px;line-height:1.4">${c[1]}</div>`;
    if(i<3) h += `<div style="${abs(RX+24,cy+72,RW-48,22)}color:#5A6F9A;text-align:center;font-size:11px">▼</div>`;
    cy+=94;
  });
  h += `<div style="${abs(RX+24,584,RW-48,40)}background:#26406B;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(RX+38,592,RW-72,26)}color:#8FA3CC;font-style:italic;font-size:9.5px;line-height:1.35;display:flex;align-items:center;height:24px">→ 다음 장: 이 '의도'를 '제도'로 못박은 Stack Ranking을 해부한다</div>`;
  h += take("전략의 '의도'는 반드시 'HR 제도'로 번역된다 — 발머의 실적주의가 Stack Ranking을 낳았다");
  h += foot("출처: LBS128 케이스 / 분석 — 전략 의도·HR 제도·문화의 인과 사슬");
  h += `</div>`;
  push(h);
}

// ============================================================
// S8 — STACK RANKING
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"01. 위기",kickW:70,sub:"전략을 떠받친 HR 제도 — Stack Ranking",n1:"01. 위기",n2:"3. HR 제도"});
  h += gov([{t:"Stack Ranking = "},{t:"'상대평가 + 강제배분'",hl:1},{t:"의 결합 — GE 잭 웰치 'vitality curve' 계열"}]);
  const LW=520;
  h += card(ML,162,LW,474);
  h += sechdr(ML,162,LW,"강제배분 — 직원을 5등급 칸에 '비율'로 끼워넣다","#1F3864");
  h += `<div style="${abs(ML+22,206,LW-44,28)}color:#5A6478;font-size:9.5px;line-height:1.45">각 등급의 인원 '비율'이 사전에 고정 — 실제 성과가 아니라 '분포'가 등급을 결정한다. 평가의 출발점이 '사람'이 아니라 '칸'이었다.</div>`;
  {
    const segs=[["Top","상위",72,"#F0F4FB","#1F4B86"],["Good","우수",96,"#DCE6F5","#1F4B86"],["Average","보통",140,"#C9D6EC","#1F3864"],["Below Avg","미흡",78,"#F3DAD6","#8E3A30"],["Poor","최하 必 10%",90,"#C0392B","#fff"]];
    let sx=ML+24;
    segs.forEach(g=>{
      h += `<div style="${abs(sx,244,g[2],58)}background:${g[3]};border:1.5px solid #fff;color:${g[4]};font-weight:700;font-size:9px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div>${g[0]}</div><div style="font-size:7px;font-weight:500;margin-top:2px">${g[1]}</div></div>`;
      sx+=g[2];
    });
  }
  h += `<div style="${abs(ML+22,316,LW-44,68)}background:#FBEEEC"></div>`;
  h += lbar(ML+22,316,68,"#C0392B",6);
  h += `<div style="${abs(ML+40,326,LW-72,50)}color:#222838;font-size:9.5px;line-height:1.55"><b style="color:#C0392B">Poor 등급 —</b> 기여도와 무관하게 '10명 중 1명'을 강제 배정. 케이스가 명시한 유일한 확정 비율이 바로 이 <b>'must bottom 10%'</b>다.</div>`;
  h += `<div style="${abs(ML+22,398,LW-44,54)}color:#5A6478;font-size:9px;line-height:1.55;font-style:italic"><b style="color:#1F3864;font-style:normal">케이스 원문 비유 —</b> "Like a stack of LEGO bricks, employees were essentially slotted into top, good, average, below average and poor positions."</div>`;
  h += `<div style="${abs(ML+22,460,LW-44,1)}background:#E1E3E9"></div>`;
  h += `<div style="${abs(ML+22,472,LW-44,16)}color:#2E5BBA;font-weight:800;font-size:10px">왜 이 제도가 '행동'을 왜곡했나</div>`;
  const why=[["제로섬","동료의 성공이 곧 내 등급 하락 — 협력이 비합리적 선택이 됨"],
    ["목표 대체","'성과'가 아니라 '서열'이 목표가 됨 — calibration 회의는 정치의 장"],
    ["위험 회피","실패가 곧 'Poor'이므로, 누구도 도전·실험을 하지 않음"]];
  let wx=ML+22, wcw=(LW-44-16)/3;
  why.forEach((w,i)=>{
    h += `<div style="${abs(wx,496,wcw,128)}background:#F5F6F9;border:1px solid #E1E3E9"></div>`;
    h += `<div style="${abs(wx,496,wcw,4)}background:#C0392B"></div>`;
    h += `<div style="${abs(wx+12,508,wcw-24,18)}color:#C0392B;font-weight:800;font-size:10px">${w[0]}</div>`;
    h += `<div style="${abs(wx+12,528,wcw-24,90)}color:#5A6478;font-size:8.5px;line-height:1.5">${w[1]}</div>`;
    wx+=wcw+8;
  });
  // right
  const RX=602, RW=466;
  h += `<div style="${abs(RX,164,RW,20)}color:#2E5BBA;font-weight:800;font-size:12px">제도 작동 4대 요소</div>`;
  const mech=[
    ["평가 주기","6개월(반기) — 1년에 두 번 전 직원을 서열화",0],
    ["등급 구조","5등급: Top / Good / Average / Below Average / Poor",0],
    ["배분 방식","강제배분(forced distribution) — 등급별 인원 비율을 사전 고정",0],
    ["보상 연동","보상·승진이 등급에 '알고리즘'으로 자동 연동",1]];
  let my=190;
  mech.forEach(m=>{
    h += card(RX,my,RW,66,m[2]?"background:#FBEEEC;border-color:#EBC9C3":"");
    h += `<div style="${abs(RX,my,8,66)}background:${m[2]?'#C0392B':'#1F3864'}"></div>`;
    h += `<div style="${abs(RX+24,my,116,66)}color:#1F3864;font-weight:700;font-size:11px;display:flex;align-items:center;height:66px">${m[0]}</div>`;
    h += `<div style="${abs(RX+148,my,RW-168,66)}color:#222838;font-size:9.5px;line-height:1.45;display:flex;align-items:center;height:66px">${m[1]}</div>`;
    my+=74;
  });
  h += `<div style="${abs(RX,492,RW,144)}background:#1F3864"></div>`;
  h += `<div style="${abs(RX,492,7,144)}background:#C0392B"></div>`;
  h += `<div style="${abs(RX+24,512,RW-40,18)}color:#8FA3CC;font-weight:800;font-size:10.5px">가장 치명적 결함 — 평가와 보상의 결합</div>`;
  h += `<div style="${abs(RX+24,536,RW-48,90)}color:#fff;font-size:10px;line-height:1.65">'평가'가 '보상'에 알고리즘으로 직결되면서, 평가가 '개발의 도구'가 아니라 <b style="color:#fff">'돈을 분배하는 도구'</b>로만 작동했다. 평가 면담은 성장을 위한 코칭이 아니라 — 한정된 보상 풀을 둘러싼 정치·협상의 시간이 되었다.</div>`;
  h += take("성과관리 제도는 '문화의 DNA' — 제도가 직원의 행동을 정밀하게 (잘못된 방향으로) 설계했다");
  h += foot("출처: LBS128 케이스 (5등급·강제배분·6개월·알고리즘 보상연동 명시) — 확정 비율은 'Poor 10%'");
  h += `</div>`;
  push(h);
}

// ============================================================
// S9 — CULTURE FROM SYSTEM
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"01. 위기",kickW:70,sub:"제도가 낳은 조직문화 — 사일로와 'Know-it-all'",n1:"01. 위기",n2:"4. As-Is 문화"});
  h += gov([{t:"강제평가가 낳은 행동이 누적되어 "},{t:"'봉건 영주국'의 구조와 '과시'의 문화",hl:1},{t:"로 굳었다"}]);
  const LW=502;
  h += card(ML,162,LW,288);
  h += sechdr(ML,162,LW,"구조 — \"Confederation of Fiefdoms\"","#1F3864");
  {
    const silos=[["Windows",ML+72],["Office",ML+222],["Server",ML+372]];
    silos.forEach(si=>{
      h += `<div style="${abs(si[1],214,98,34)}background:#1F3864;color:#fff;font-weight:700;font-size:9.5px;display:flex;align-items:center;justify-content:center">${si[0]}</div>`;
      for(let r=0;r<2;r++)for(let c=0;c<3;c++)
        h += `<div style="${abs(si[1]+7+c*30,258+r*26,24,21)}background:#C7CEDC"></div>`;
    });
    h += `<svg style="${abs(ML+152,222,80,16)}" width="80" height="16"><line x1="6" y1="8" x2="74" y2="8" stroke="#C0392B" stroke-width="2"/><path d="M6,8 L13,4 L13,12 Z" fill="#C0392B"/><path d="M74,8 L67,4 L67,12 Z" fill="#C0392B"/></svg>`;
    h += `<svg style="${abs(ML+302,222,80,16)}" width="80" height="16"><line x1="6" y1="8" x2="74" y2="8" stroke="#C0392B" stroke-width="2"/><path d="M6,8 L13,4 L13,12 Z" fill="#C0392B"/><path d="M74,8 L67,4 L67,12 Z" fill="#C0392B"/></svg>`;
  }
  h += `<div style="${abs(ML+22,328,LW-44,58)}color:#5A6478;font-size:9.5px;line-height:1.6">제품별 사일로 = <b style="color:#1F3864">'봉건 영주국의 연합'</b>. 부서 간 경쟁이 협업을 대체했고, 수직적 위계가 자발성·창의성을 억압했다. 부서끼리도 서로를 경쟁자로 여겨 — 같은 회사 안에서 정보가 흐르지 않았다.</div>`;
  h += `<div style="${abs(ML+22,394,LW-44,38)}background:#F5F6F9;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(ML+34,400,LW-60,26)}color:#8E3A30;font-size:9px;font-weight:600;line-height:1.35;display:flex;align-items:center;height:26px">한 임원의 회고: "회사가 아니라, 서로 싸우는 작은 나라들의 집합 같았다"</div>`;
  // right: culture
  const RX=586, RW=482;
  h += card(RX,162,RW,288);
  h += sechdr(RX,162,RW,"문화 — Know-it-all (과시의 문화)","#1F3864");
  h += `<div style="${abs(RX+22,208,RW-44,18)}color:#C0392B;font-weight:800;font-size:10.5px">\"가장 똑똑함을 증명하라\"</div>`;
  h += `<div style="${abs(RX+22,228,RW-44,46)}color:#5A6478;font-size:9.5px;line-height:1.55">직원들은 회의실에서 '자신이 가장 똑똑하다'는 것을 증명해야 했다. 학습보다 과시가, 질문보다 정답이 우선이었다.</div>`;
  h += `<div style="${abs(RX+22,282,RW-44,18)}color:#C0392B;font-weight:800;font-size:10.5px">Precision Questioning &amp; 폐쇄성</div>`;
  h += `<div style="${abs(RX+22,302,RW-44,46)}color:#5A6478;font-size:9.5px;line-height:1.55">회의는 아이디어의 허점을 찌르는 검증의 장. Ballmer는 Linux를 \"암(a cancer)\"으로 규정 — 외부에 닫힌 'Not Invented Here' 사고.</div>`;
  h += `<div style="${abs(RX+22,358,RW-44,72)}background:#F5F6F9;border-left:3px solid #2E5BBA"></div>`;
  h += `<div style="${abs(RX+36,368,RW-64,54)}color:#1F3864;font-size:9px;font-weight:600;line-height:1.55;display:flex;align-items:center;height:54px">학습보다 과시 · 질문보다 정답 · 외부보다 내부 — 세 가지 폐쇄성이 겹쳐 '심리적 안전감 제로'의 조직을 만들었다</div>`;
  // quote full
  h += quote(ML,464,CW,72,"\"직원들은 회의실 안에서 자신이 가장 똑똑하다는 것을 증명해야 했다. 계급과 서열이 조직을 지배하면서 자발성과 창의성이 고통받았다.\"","— Satya Nadella, 『히트 리프레시』 p151",true,12);
  // 3-chain
  h += `<div style="${abs(ML,552,CW,18)}color:#2E5BBA;font-weight:800;font-size:11px">As-Is 종합 — 전략 의도가 제도를, 제도가 문화를 만든 3단 사슬</div>`;
  const ssum=[["전략 의도","PC 수성 + 실적주의","#C0392B"],["HR 제도","Stack Ranking (상대평가·강제배분)","#A9781F"],["조직문화","사일로 + Know-it-all","#1F3864"]];
  let sx=ML;
  ssum.forEach((c,i)=>{
    h += `<div style="${abs(sx,576,308,60)}background:#F5F6F9;border:1px solid #E1E3E9"></div>`;
    h += `<div style="${abs(sx,576,7,60)}background:${c[2]}"></div>`;
    h += `<div style="${abs(sx+20,587,278,18)}color:#1F3864;font-weight:700;font-size:10.5px">${c[0]}</div>`;
    h += `<div style="${abs(sx+20,606,278,22)}color:#5A6478;font-size:9px">${c[1]}</div>`;
    if(i<2) h += `<div style="${abs(sx+308,576,42,60)}color:#C9CFDA;font-size:14px;display:flex;align-items:center;justify-content:center;height:60px">▶</div>`;
    sx+=351;
  });
  h += take("병소는 '한 곳'이 아니다 — 전략·제도·문화가 한 덩어리로 맞물려 '심리적 안전감 제로'의 조직을 만들었다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p151");
  h += `</div>`;
  push(h);
}

// ============================================================
// S10 — CVF AS-IS
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"01. 위기",kickW:70,sub:"퀸 모델로 본 As-Is — '위계 + 시장' 사분면 고착",n1:"01. 위기",n2:"5. CVF As-Is 좌표"});
  h += gov([{t:"Ballmer 시대 문화의 좌표는 "},{t:"'안정·통제' 축의 위계(Hierarchy) + 시장(Market)",hl:1}]);
  h += card(ML,162,470,474,"background:#FAFBFC;border-color:#E1E3E9");
  h += `<div style="${abs(ML+24,182,420,20)}color:#1F3864;font-weight:700;font-size:12px">As-Is 좌표 — Ballmer 시대 (2000–2014)</div>`;
  h += `<div style="${abs(ML+24,202,422,1)}background:#E1E3E9"></div>`;
  h += cvf(ML+92,262,326,266,"asis");
  h += `<div style="${abs(ML+24,576,422,46)}background:#FBEEEC;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(ML+38,584,398,32)}color:#8E3A30;font-size:9px;font-weight:600;line-height:1.5;display:flex;align-items:center;height:30px">무게중심이 '안정·통제' 축에 고착 — 환경이 요구한 '유연성' 사분면(관계·혁신)이 통째로 비었다</div>`;
  const RX=540, RW=528;
  h += card(RX,162,RW,474,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,182,RW-40,20)}color:#1F3864;font-weight:700;font-size:13px">As-Is 좌표 해석 — 왜 여기에 갇혔나</div>`;
  h += `<div style="${abs(RX+24,206,RW-48,2)}background:#1F3864"></div>`;
  const interp=[
    ["Hierarchy (위계) 고착","수직적 위계·서열·규칙이 지배. 형식적 회의와 상사 결재 중심 — 자발성과 창의성을 구조적으로 억압했다","#C0392B"],
    ["Market (시장) 고착","Stack Ranking이 만든 내부 경쟁·실적주의. 동료를 이겨야 하는 제로섬 — '협력'은 비합리적 행동이 됐다","#C0392B"],
    ["빠진 사분면 — Clan (관계)","협력·인재개발의 '관계문화'가 부재. 지식 공유는 곧 자기 손해 — 아무도 동료를 돕지 않았다","#8A93A6"],
    ["빠진 사분면 — Adhocracy (혁신)","창의·모험의 '혁신문화'가 부재. 실패가 약점이 되는 곳에서 누구도 위험을 감수하지 않았다","#8A93A6"]];
  let iy=224;
  interp.forEach(t=>{
    h += card(RX+24,iy,RW-48,94,"background:#fff;border-color:#E6E8ED");
    h += `<div style="${abs(RX+24,iy,7,94)}background:${t[2]}"></div>`;
    h += `<div style="${abs(RX+44,iy+13,RW-90,18)}color:${t[2]==='#C0392B'?'#C0392B':'#5A6478'};font-weight:700;font-size:11px">${t[0]}</div>`;
    h += `<div style="${abs(RX+44,iy+34,RW-92,50)}color:#222838;font-size:9.5px;line-height:1.5">${t[1]}</div>`;
    iy+=100;
  });
  h += take("환경(모바일·클라우드)은 '유연성'을 요구했지만, 문화는 정반대인 '안정·통제' 축에 갇혀 있었다 — 전략-문화 부정합");
  h += foot("출처: LBS128 케이스 / 경쟁가치모형(Cameron & Quinn)으로 본 진단");
  h += `</div>`;
  push(h);
}

divider("02","각성 — 한 리더의 '공감'","Awakening",[
  "왜 나델라인가 — 22년 내부자가 가진 '내부에서 본 외부의 시선'",
  "장남 Zain에게서 배운 공감, 그리고 Dweck의 『Mindset』 — 변화의 씨앗",
]);

// ============================================================
// S12 — WHY NADELLA / EMPATHY
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"02. 각성",kickW:70,sub:"왜 나델라인가 — '공감'이라는 변화의 씨앗",n1:"02. 각성",n2:"1. 공감의 뿌리"});
  h += gov([{t:"나델라의 리더십은 전략이 아니라 "},{t:"장남에게서 배운 '공감'",hl:1},{t:"에서 출발했다"}]);
  const LW=506, RX=592, RW=476;
  h += card(ML,162,LW,156);
  h += sechdr(ML,162,LW,"프로필 — 내부에서 본 외부의 시선","#1F3864");
  const prof=["1992년 입사 — 22년 내부자, Cloud & Enterprise 부문 EVP 역임",
    "Bing 등 리스크 큰 보직을 자발적으로 수행 — \"거절하기 어려운 학습 기회\"",
    "내부자의 맥락 이해 + 그 문화에 '포섭되지 않은' 비판적 시선"];
  let py=206;
  prof.forEach(p=>{
    h += `<div style="${abs(ML+24,py+5,7,7)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(ML+40,py,LW-64,28)}color:#222838;font-size:9.5px;line-height:1.45">${p}</div>`;
    py+=34;
  });
  h += card(ML,330,LW,306);
  h += sechdr(ML,330,LW,"공감의 뿌리 — 장남 Zain","#C0392B");
  h += `<div style="${abs(ML+24,376,LW-48,90)}color:#222838;font-size:10px;line-height:1.65">뇌성마비를 안고 태어난 장남 Zain을 키우며, 나델라는 '공감'을 추상적 가치가 아니라 <b>'체화된 역량'</b>으로 받아들였다. 입사 면접에서 한 면접관이 던진 말이 그를 오래도록 따라다녔다.</div>`;
  h += quote(ML+24,478,LW-48,138,"\"당신은 공감 능력이 조금 필요하군요. 아기가 거리에서 울고 있다면, 아기를 안아 올려야지요.\"","— 입사 면접관의 말, 『히트 리프레시』 p26",false,12);
  // right
  h += card(RX,162,RW,176,"background:#1F3864;border-color:#1F3864");
  h += `<div style="${abs(RX+24,182,RW-40,20)}color:#fff;font-weight:700;font-size:12.5px">공감은 '전략적 역량'이다</div>`;
  h += `<div style="${abs(RX+24,206,RW-48,1)}background:#3A547F"></div>`;
  h += `<div style="${abs(RX+24,218,RW-48,108)}color:#D6DEEC;font-size:10px;line-height:1.7">나델라에게 공감은 단순한 인성이 아니라 <b style="color:#fff">경영의 핵심 역량</b>이다. 직원·고객의 '미충족 니즈'를 느낄 수 있어야 그것을 충족시킬 수 있기 때문이다. 그는 이 공감을 Microsoft의 제품·시장·직원·파트너 한가운데 심고자 했다.</div>`;
  h += quote(RX,352,RW,84,"\"나는 삶의 부침을 통해서만 공감 능력을 발전시킬 수 있다는 것을 알게 되었다.\"","— 『히트 리프레시』 p28",true,11.5);
  h += card(RX,450,RW,186,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,470,RW-40,18)}color:#2E5BBA;font-weight:800;font-size:11px">핵심 통찰 — 변화는 '인간'에서 출발한다</div>`;
  h += `<div style="${abs(RX+24,492,RW-48,2)}background:#2E5BBA"></div>`;
  h += `<div style="${abs(RX+24,504,RW-48,90)}color:#222838;font-size:10px;line-height:1.65">나델라는 '전략 전환'이 아니라 <b>"인간 시스템(human system)의 변화"</b>를 변혁의 목표로 삼았다. 평가·보상·구조를 바꾸기 전에 — '인재를 보는 눈'과 '리더의 태도'부터 바꾸려 했다.</div>`;
  h += `<div style="${abs(RX+24,602,RW-48,24)}color:#5A6478;font-style:italic;font-size:9px;line-height:1.4">→ 다음 장: 이 공감의 리더가 만난 또 하나의 씨앗, Carol Dweck의 『Mindset』</div>`;
  h += take("변혁의 첫 단추는 제도가 아니라 리더의 '인간관' — 나델라의 공감이 그 출발점이었다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p26, p28");
  h += `</div>`;
  push(h);
}

// ============================================================
// S13 — DWECK MINDSET
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"02. 각성",kickW:70,sub:"성장 마인드셋과의 만남 — Carol Dweck 『Mindset』",n1:"02. 각성",n2:"2. 성장 마인드셋"});
  h += gov([{t:"아내가 건넨 한 권의 책이 "},{t:"12.5만 명 조직 변혁의 '청사진'",hl:1},{t:"이 되었다"}]);
  const LW=494, RX=580, RW=488;
  h += card(ML,162,LW,118,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(ML+22,180,LW-40,18)}color:#1F3864;font-weight:700;font-size:11.5px">한 권의 책에서 시작된 청사진</div>`;
  h += `<div style="${abs(ML+22,202,LW-44,68)}color:#222838;font-size:10px;line-height:1.65">아내 Anu가 추천한 스탠퍼드 심리학자 <b>Carol Dweck의 『Mindset』</b>. 학습 차이가 있는 딸을 위한 책이었지만, 나델라는 거기서 '조직'을 위한 변혁의 원리를 발견했다.</div>`;
  // fixed vs growth table
  h += `<div style="${abs(ML,294,LW/2,34)}background:#C0392B;color:#fff;font-weight:700;font-size:11px;display:flex;align-items:center;justify-content:center">Fixed Mindset　고정형</div>`;
  h += `<div style="${abs(ML+LW/2,294,LW/2,34)}background:#2E5BBA;color:#fff;font-weight:700;font-size:11px;display:flex;align-items:center;justify-content:center">Growth Mindset　성장형</div>`;
  const fg=[["능력은 고정된 자질","능력은 노력으로 성장"],["실패 = 약점 노출, 회피","실패 = 학습의 기회"],
    ["익숙한 것만 고수","새로운 도전을 추구"],["타인의 성공은 위협","타인의 성공은 영감"],["\"Know-it-all\"","\"Learn-it-all\""]];
  let fy=328;
  fg.forEach((r,i)=>{
    const rh=i===4?64:56;
    h += `<div style="${abs(ML,fy,LW/2,rh)}background:${i%2?'#FCF4F2':'#FBEEEC'};border:1px solid #F0DAD6"></div>`;
    h += `<div style="${abs(ML+14,fy,LW/2-24,rh)}color:#8E3A30;font-size:9.5px;${i===4?'font-weight:800;font-size:11px;':''}display:flex;align-items:center;height:${rh}px">${r[0]}</div>`;
    h += `<div style="${abs(ML+LW/2,fy,LW/2,rh)}background:${i%2?'#F0F4FB':'#EAF0FA'};border:1px solid #DAE3F2"></div>`;
    h += `<div style="${abs(ML+LW/2+14,fy,LW/2-24,rh)}color:#1F4B86;font-size:9.5px;${i===4?'font-weight:800;font-size:11px;':''}display:flex;align-items:center;height:${rh}px">${r[1]}</div>`;
    fy+=rh;
  });
  // right
  h += card(RX,162,RW,182,"background:#1F3864;border-color:#1F3864");
  h += `<div style="${abs(RX+24,182,RW-40,20)}color:#fff;font-weight:700;font-size:12.5px">나델라가 읽어낸 것 — '조직'의 마인드셋</div>`;
  h += `<div style="${abs(RX+24,206,RW-48,1)}background:#3A547F"></div>`;
  h += `<div style="${abs(RX+24,218,RW-48,114)}color:#D6DEEC;font-size:10px;line-height:1.7">Dweck은 세상을 '학습자'와 '비학습자'로 나눈다. 나델라는 이 <b style="color:#fff">개인 심리학을 '조직'의 차원으로 끌어올렸다</b> — 회사 전체가 '아는 척하는 집단(know-it-all)'에서 '배우려는 집단(learn-it-all)'으로 바뀔 수 있다는 것.</div>`;
  h += quote(RX,358,RW,108,"\"고정된 사고는 발목을 붙잡지만, 성장하는 사고는 사람들을 앞으로 나아가게 한다. … 사람들이 받은 패는 출발점에 불과하다.\"","— 『히트 리프레시』 p140",true,11.5);
  h += card(RX,480,RW,156,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,498,RW-40,18)}color:#2E5BBA;font-weight:800;font-size:11px">'성장'의 정의 — 손익이 아니라 사람</div>`;
  h += quote(RX+24,522,RW-48,72,"\"여기서 성장이란 손익 계산과 관련된 것이 아니다. 이건 개인의 성장에 관한 것이었다.\"","— 『히트 리프레시』 p142",false,11);
  h += `<div style="${abs(RX+24,602,RW-48,26)}color:#5A6478;font-style:italic;font-size:9px;line-height:1.4">→ 이 '성장 마인드셋'이 PART 4의 새 미션·3대 Pillar, PART 5의 제도 재설계로 구체화된다</div>`;
  h += take("성장 마인드셋은 슬로건이 아니라 — 평가·보상·문화를 다시 설계하는 '이론적 근간'이 되었다");
  h += foot("출처: LBS128 케이스 / Carol Dweck, 『Mindset』 / 『히트 리프레시』 p140, p142");
  h += `</div>`;
  push(h);
}

divider("03","경청 — 진단으로서의 첫 1년","Listening",[
  "지시가 아니라 듣는 것부터 — 수백 명 인터뷰와 익명 포커스 그룹",
  "\"Microsoft는 왜 존재하는가\" — 그리고 '변화를 이끌 사람을 버스에 태우다'",
]);

// ============================================================
// S15 — LISTENING
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"03. 경청",kickW:70,sub:"취임과 경청 — '진단 없이 처방하지 않는다'",n1:"03. 경청",n2:"1. 경청의 1년"});
  h += gov([{t:"나델라의 첫 1년은 비전 '선포'가 아니라 "},{t:"'경청'을 통한 조직 진단",hl:1},{t:"이었다"}]);
  const LW=512, RX=602, RW=466;
  h += `<div style="${abs(ML,166,LW,20)}color:#2E5BBA;font-weight:800;font-size:12px">진단 방법론 — 듣는 것부터 시작하다</div>`;
  const tl=[
    ["2014.2","CEO 취임 & 전 직원 서한","\"22년 전 첫 출근날처럼 겸허하다\" — 첫날부터 '의미'를 물었다"],
    ["상징적 신호","리더십 팀에 'NVC' 의무 독서","비폭력대화(Nonviolent Communication) — '소통의 방식'부터 바꾸겠다는 신호"],
    ["진단 ①","수백 명 인터뷰","모든 레벨·모든 부서를 직접 경청"],
    ["진단 ②","익명 포커스 그룹","솔직한 의견을 끌어내는 '안전한 채널'"],
    ["핵심 질문","\"Why does Microsoft exist?\"","존재 이유에 대한 근본적 재질문"]];
  let ty=196;
  tl.forEach((t,i)=>{
    h += `<div class="num-badge" style="${abs(ML,ty,34,34)}background:${i===1?'#C0392B':'#2E5BBA'};font-size:13px;line-height:34px">${i+1}</div>`;
    if(i<4) h += `<div style="${abs(ML+16,ty+34,2,42)}background:#D6D9E0"></div>`;
    h += `<div style="${abs(ML+50,ty-2,LW-50,18)}color:#1F3864;font-weight:700;font-size:11.5px"><span style="color:#2E5BBA;font-size:9px">${t[0]}　</span>${t[1]}</div>`;
    h += `<div style="${abs(ML+50,ty+18,LW-50,30)}color:#5A6478;font-size:9px;line-height:1.4">${t[2]}</div>`;
    ty+=76;
  });
  h += quote(ML,580,LW,56,"\"경청은 내가 매일 실천한 가장 중요한 과제였다. 내 리더십의 기초를 다질 요소였기 때문이다.\"","— 『히트 리프레시』 p118",false,10.5);
  // right
  h += card(RX,162,RW,474,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,182,RW-40,20)}color:#1F3864;font-weight:700;font-size:12.5px">진단 결과 — 직원들이 원한 5가지</div>`;
  h += `<div style="${abs(RX+24,206,RW-48,2)}background:#1F3864"></div>`;
  const needs=["변화를 만들되, Microsoft의 원래 이상을 존중하는 CEO",
    "명확하고 구체적이며 영감을 주는 비전","투명하고 단순한 방식의 진행 상황 공유",
    "따라가는 것이 아니라 다시 '선도(lead)'하는 회사","잃어버린 \"멋진 것(coolness)\"의 회복"];
  let ny=220;
  needs.forEach((n,i)=>{
    h += card(RX+24,ny,RW-48,62,"background:#fff;border-color:#E6E8ED");
    h += `<div style="${abs(RX+34,ny,52,62)}color:#BCC8DE;font-weight:900;font-size:26px;display:flex;align-items:center;justify-content:center;height:62px">${i+1}</div>`;
    h += `<div style="${abs(RX+92,ny,RW-120,62)}color:#222838;font-size:10px;line-height:1.4;display:flex;align-items:center;height:62px">${n}</div>`;
    ny+=70;
  });
  h += `<div style="${abs(RX+24,574,RW-48,52)}background:#1F3864"></div>`;
  h += `<div style="${abs(RX+38,582,RW-72,38)}color:#fff;font-size:9.5px;font-weight:600;line-height:1.5;display:flex;align-items:center;height:36px">진단의 결론 — "우리가 존재하는 이유는, 사람들이 우리 제품으로 더 많은 힘을 얻게(empower) 하는 데 있다"</div>`;
  h += take("내부 승진 CEO의 강점(맥락 이해)을 '경청·진단 방법론'으로 전환 — 처방은 진단 다음이다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p118");
  h += `</div>`;
  push(h);
}

// ============================================================
// S16 — SLT RECONSTRUCTION
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"03. 경청",kickW:70,sub:"SLT 재구성 — '변화를 이끌 사람을 버스에 태운다'",n1:"03. 경청",n2:"2. 리더십팀 재구성"});
  h += gov([{t:"비전보다 먼저 한 일 — "},{t:"변화를 이끌 '리더십 팀'을 다시 짜는 것",hl:1}]);
  h += quote(ML,160,CW,56,"\"우선은 나와 함께 이런 변화를 이끌 사람을 버스에 태워야 했다. SLT는 같은 세계관을 공유하는 끈끈한 조직으로 바뀌어야 했다.\"","— 『히트 리프레시』 p125",true,11);
  h += `<div style="${abs(ML,228,CW,18)}color:#2E5BBA;font-weight:800;font-size:11.5px">새 SLT(시니어 리더십 팀)의 면면 — '독특한 초능력의 슈퍼히어로 군단'</div>`;
  const slt=[
    ["Kathleen Hogan","최고인사책임자 (CPO)","맥킨지·오라클 출신. 문화·인사 변혁을 HR이 총괄 — '문화 고문단' 운영","변혁의 설계·총괄","문화·인사 변혁을 HR 어젠다로 끌어올린 핵심 축","#1F3864"],
    ["Jill T. Nichols","비서실장 (Chief of Staff)","발머 시절 인물. 발탁 이유 = \"권력이 아니라 문화를 위한 사무실\"","소통·문화의 실무","구(舊) 인물을 품어 — '문화는 사람을 가리지 않는다'는 신호","#2E5BBA"],
    ["Peggy Johnson","사업개발 총괄","퀄컴 출신. 실리콘밸리 경쟁사와 '놀라운 파트너십' 구축","외부와의 연결","닫힌 조직을 외부 생태계로 여는 가교","#2E5BBA"],
    ["Kurt DelBene","최고전략책임자 (CSO)","오바마 행정부 Healthcare.gov 복구 주역 — 외부 경험을 다시 안으로","전략·실행력","떠났던 인재를 다시 불러 — 학습한 외부 경험을 이식","#1F3864"]];
  let sy=252;
  slt.forEach(p=>{
    h += card(ML,sy,CW,82);
    h += `<div style="${abs(ML,sy,9,82)}background:${p[5]}"></div>`;
    h += `<div style="${abs(ML+26,sy+13,300,20)}color:#1F3864;font-weight:800;font-size:13px">${p[0]}</div>`;
    h += `<div style="${abs(ML+26,sy+35,300,16)}color:${p[5]};font-weight:700;font-size:9.5px">${p[1]}</div>`;
    h += `<div style="${abs(ML+26,sy+53,330,20)}color:#5A6478;font-size:9px;line-height:1.4">${p[2]}</div>`;
    h += `<div style="${abs(ML+372,sy+14,1,54)}background:#E1E3E9"></div>`;
    h += `<div style="${abs(ML+392,sy+15,150,18)}color:${p[5]};font-weight:800;font-size:9.5px">${p[3]}</div>`;
    h += `<div style="${abs(ML+392,sy+34,CW-410,40)}color:#5A6478;font-size:9px;line-height:1.45">${p[4]}</div>`;
    sy+=90;
  });
  h += `<div style="${abs(ML,616,CW,68)}"></div>`;
  h += card(ML,610,CW,26,"background:#F5F6F9;border-color:#E1E3E9");
  // actually a richer note bar:
  h = h.slice(0, h.lastIndexOf('<div class="card"'));
  h += card(ML,608,CW,28,"background:#F5F6F9;border-color:#E1E3E9");
  h += lbar(ML,608,28,"#2E5BBA",6);
  h += `<div style="${abs(ML+20,608,CW-36,28)}color:#222838;font-size:9px;line-height:1.3;display:flex;align-items:center;height:28px"><b style="color:#2E5BBA">단, '예스맨'은 아니다 —</b>　나델라는 분명히 했다: "논쟁은 반드시 필요하다. 그러나 동시에 '높은 수준의 합의'에 도달해야 한다." SLT를 '또 하나의 회의'가 아니라 '각자의 첫 번째 팀(first team)'으로 인식하게 했다.</div>`;
  h += take("비전보다 사람이 먼저 — '같은 세계관의 팀'을 짜는 것이 문화 변혁의 출발점이었다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p125~127");
  h += `</div>`;
  push(h);
}

divider("04","선언 — \"Know-it-all에서 Learn-it-all로\"","Declaration",[
  "새로운 미션 — \"지구상 모든 사람과 조직이 더 많이 성취하도록\"",
  "성장 마인드셋을 '조직의 언어'로 — Culture Cabinet과 3대 Pillar",
]);

// ============================================================
// S18 — NEW MISSION
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"04. 선언",kickW:70,sub:"새 미션 선언 — 2015 올랜도, '의미'를 다시 정의하다",n1:"04. 선언",n2:"1. 새 미션"});
  h += gov([{t:"미션을 "},{t:"'제품(컴퓨터)'에서 '사람의 역량(empower)'",hl:1},{t:"으로 다시 정의했다"}]);
  const LW=508, RX=594, RW=474;
  // old mission
  h += `<div style="${abs(ML,162,LW,148)}background:#F5F6F9;border:1px solid #E1E3E9"></div>`;
  h += lbar(ML,162,148,"#8A93A6");
  h += `<div style="${abs(ML+24,180,LW-44,18)}color:#5A6478;font-weight:800;font-size:10.5px">기존 미션 (Gates)</div>`;
  h += `<div style="${abs(ML+24,204,LW-48,40)}color:#222838;font-style:italic;font-weight:700;font-size:14px;line-height:1.3">"A computer on every desk and in every home"</div>`;
  h += `<div style="${abs(ML+24,254,LW-48,44)}color:#5A6478;font-size:9.5px;line-height:1.55">PC의 보편화 — 한 시대를 지배했으나, 모바일·클라우드 시대에는 '이미 달성된, 닫힌 목표'였다.</div>`;
  // arrow
  h += `<div style="${abs(ML,318,LW,24)}text-align:center;color:#C0392B;font-size:14px;font-weight:800">▼</div>`;
  // new mission
  h += `<div style="${abs(ML,350,LW,286)}background:#1F3864"></div>`;
  h += lbar(ML,350,286,"#C0392B");
  h += `<div style="${abs(ML+24,372,LW-44,18)}color:#8FA3CC;font-weight:800;font-size:10.5px">새 미션 (Nadella, 2015 올랜도)</div>`;
  h += `<div style="${abs(ML+24,396,LW-48,76)}color:#fff;font-style:italic;font-weight:700;font-size:15.5px;line-height:1.35">"To empower every person and every organisation on the planet to achieve more"</div>`;
  h += `<div style="${abs(ML+24,486,LW-48,1)}background:#3A547F"></div>`;
  h += `<div style="${abs(ML+24,500,LW-48,120)}color:#C7CFE0;font-size:10px;line-height:1.7">지구상 모든 사람과 조직이 <b style="color:#fff">'더 많이 성취하도록(achieve more)'</b>. 끝이 없는 목표 — 제품이 아니라 '타인의 역량'을 향한다. 외부를 향한 약속이, 곧 내부 문화의 방향타가 된다.</div>`;
  // right
  h += card(RX,162,RW,178);
  h += sechdr(RX,162,RW,"왜 미션부터 바꿨나","#1F3864");
  h += `<div style="${abs(RX+24,208,RW-48,116)}color:#222838;font-size:10px;line-height:1.7">진단(PART 3)에서 직원들이 가장 원한 것은 <b>'명확하고 영감을 주는 비전'</b>이었다. 나델라는 올랜도 세계 영업 컨퍼런스에서 새 미션을 선언하며 — 자녀들의 특수한 필요를 통해 배운 것을 이야기하고, 곧바로 '문화'를 말했다.</div>`;
  h += quote(RX,356,RW,158,"\"우리는 담대한 목표를 세울 수 있습니다. 그러나 그것은 우리가 문화를 살아내고, 문화를 가르칠 때에만 일어납니다. … 그 문화의 모델이 바로 '성장하는 사고(growth mindset)'입니다.\"","— Satya Nadella, 2015 올랜도 연설 / 『히트 리프레시』",true,11);
  h += card(RX,530,RW,106,"background:#F5F6F9;border-color:#E1E3E9");
  h += lbar(RX,530,106,"#2E5BBA");
  h += `<div style="${abs(RX+24,544,RW-44,78)}color:#222838;font-size:9.5px;line-height:1.6">→ 미션(외부를 향한 약속)이 곧 내부 문화의 방향타가 된다. <b style="color:#1F3864">'역량 강화'를 외친 회사는, 내부 구성원도 '역량을 키우는' 방식으로 평가·보상해야 한다.</b></div>`;
  h += take("미션을 '제품'에서 '사람의 역량'으로 옮긴 순간 — 평가·보상 제도가 바뀌어야 할 이유가 생겼다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p122~123, p142");
  h += `</div>`;
  push(h);
}

// ============================================================
// S19 — CULTURE CABINET
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"04. 선언",kickW:70,sub:"성장 마인드셋을 '조직의 언어'로 — Culture Cabinet",n1:"04. 선언",n2:"2. Culture Cabinet"});
  h += gov([{t:"추상적 개념을 "},{t:"임원 180명이 '17개 팀'으로 직접 정의",hl:1},{t:"하게 했다"}]);
  const LW=512, RX=602, RW=466;
  h += card(ML,162,LW,250);
  h += sechdr(ML,162,LW,"Culture Cabinet — 문화를 '함께' 정의하다","#1F3864");
  h += `<div style="${abs(ML+24,208,LW-48,118)}color:#222838;font-size:10px;line-height:1.7">나델라는 성장 마인드셋을 위에서 '하달'하지 않았다. <b>임원 180명을 17개 팀으로 나눠</b>, '우리에게 성장 마인드셋이란 무엇인가'를 직접 정의하게 했다. 17명의 리더가 <b>'문화 고문단(culture cabinet)'</b>이 되었다.</div>`;
  h += `<div style="${abs(ML+24,338,LW-48,52)}background:#F5F6F9;border-left:3px solid #2E5BBA"></div>`;
  h += `<div style="${abs(ML+38,346,LW-72,38)}color:#1F3864;font-size:9.5px;font-weight:600;line-height:1.5;display:flex;align-items:center;height:36px">→ 문화는 '선언'이 아니라 '참여'로 만들어진다. 정의의 주체가 곧 실행의 주체가 된다.</div>`;
  h += card(ML,426,LW,210,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(ML+24,444,LW-40,18)}color:#2E5BBA;font-weight:800;font-size:11px">'성장'의 재정의 — 손익이 아니라 사람</div>`;
  h += quote(ML+24,468,LW-48,96,"\"실제로 우리의 새로운 문화를 설명해주는 문구는 '성장하는 사고'입니다. … 여기서 성장이란 손익 계산이 아니라, 개인의 성장에 관한 것이었습니다.\"","— 『히트 리프레시』 p142",false,10.5);
  h += `<div style="${abs(ML+24,576,LW-48,48)}color:#222838;font-size:9.5px;line-height:1.55"><b style="color:#1F3864">'know-it-all'에서 'learn-it-all'로</b> — 회사의 정체성을 한 문장으로 압축했다.</div>`;
  // right
  h += quote(RX,162,RW,96,"\"문화는 아침 식사로 전략을 먹는다 (Culture eats strategy for breakfast).\"","— Peter Drucker, 『히트 리프레시』 p138 인용",true,11.5);
  h += card(RX,274,RW,362,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,294,RW-40,18)}color:#1F3864;font-weight:700;font-size:12px">선언에서 구현으로 — 다음 단계의 예고</div>`;
  h += `<div style="${abs(RX+24,316,RW-48,2)}background:#1F3864"></div>`;
  h += `<div style="${abs(RX+24,328,RW-48,72)}color:#222838;font-size:10px;line-height:1.65">나델라는 '문화가 전략을 이긴다'는 드러커의 말을 빌려 문화를 경영의 1순위로 올렸다. 그러나 그는 알았다 — <b>선언만으로는 아무것도 바뀌지 않는다</b>는 것을.</div>`;
  const steps2=[["선언","새 미션 + 성장 마인드셋의 언어화","#2E5BBA"],["구체화","3대 Pillar — 다음 장","#2E5BBA"],["구현","제도·행동·환경으로 — PART 5","#C0392B"]];
  let sy2=412;
  steps2.forEach((c,i)=>{
    h += `<div style="${abs(RX+24,sy2,RW-48,52)}background:#fff;border:1px solid #E1E3E9"></div>`;
    h += `<div style="${abs(RX+24,sy2,7,52)}background:${c[2]}"></div>`;
    h += `<div style="${abs(RX+44,sy2,90,52)}color:#1F3864;font-weight:800;font-size:11px;display:flex;align-items:center;height:52px">${c[0]}</div>`;
    h += `<div style="${abs(RX+134,sy2,RW-160,52)}color:#5A6478;font-size:9.5px;display:flex;align-items:center;height:52px">${c[1]}</div>`;
    if(i<2) h += `<div style="${abs(RX+24,sy2+52,RW-48,16)}text-align:center;color:#C9CFDA;font-size:9px">▼</div>`;
    sy2+=68;
  });
  h += take("문화는 '하달'이 아니라 '공동 정의'로 만들어진다 — 정의의 주체가 곧 실행의 주체가 된다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p138, p142");
  h += `</div>`;
  push(h);
}

// ============================================================
// S20 — THREE PILLARS
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"04. 선언",kickW:70,sub:"성장 마인드셋의 3대 Pillar",n1:"04. 선언",n2:"3. 3대 Pillar"});
  h += gov([{t:"성장 마인드셋을 실천하는 "},{t:"세 가지 구체적 방법",hl:1},{t:" — 고객 집착 · 다양성과 포용 · One Microsoft"}]);
  const pil=[
    ["Customer Obsession","고객 집착","\"초심자의 마음으로 소비자에게 배운다\" — 소비자가 표현한 적 없고, 충족된 적 없는 요구를 채우려는 열망과 호기심.","\"우리의 모든 것은 고객의 미충족 니즈에서 출발한다\"","성장 마인드셋을 '외부(고객)'로 향하게 한다","#2E5BBA"],
    ["Diversity & Inclusion","다양성과 포용","\"적극적으로 다양성과 포용을 추구해야 최고의 성과를 얻는다\" — 자신의 편견을 깨닫고 행동을 바꾸는 것.","\"포용은 더 나은 제품을 만드는 경쟁력이다\"","성장 마인드셋을 '서로(동료)'에게 향하게 한다","#1F3864"],
    ["One Microsoft","하나의 마이크로소프트","\"우리는 하나의 회사다. 여러 세력으로 구성된 연합체가 아니다\" — 사일로를 넘는 협업의 의무화.","\"승리는 부서가 아니라 회사 전체의 것\"","성장 마인드셋을 '조직 전체'로 향하게 한다","#C0392B"]];
  const pw=327, pg=14; let px=ML;
  pil.forEach((p,i)=>{
    h += card(px,162,pw,400);
    h += `<div style="${abs(px,162,pw,82)}background:${p[5]}"></div>`;
    h += `<div style="${abs(px+20,176,pw-36,28)}color:#fff;font-weight:800;font-size:14px">${p[0]}</div>`;
    h += `<div style="${abs(px+20,206,pw-36,24)}color:#D6DEEC;font-size:11px;font-weight:500">${p[1]}</div>`;
    h += `<div class="num-badge" style="${abs(px+pw-44,176,28,28)}background:rgba(255,255,255,.2);font-size:13px;line-height:28px">${i+1}</div>`;
    h += `<div style="${abs(px+20,258,80,16)}color:${p[5]};font-weight:800;font-size:9px;letter-spacing:.5px">개념</div>`;
    h += `<div style="${abs(px+20,278,pw-40,116)}color:#222838;font-size:10px;line-height:1.7">${p[2]}</div>`;
    h += `<div style="${abs(px+20,398,pw-40,46)}background:#F5F6F9;border-left:3px solid ${p[5]}"></div>`;
    h += `<div style="${abs(px+32,406,pw-62,32)}color:#1F3864;font-size:9px;font-style:italic;font-weight:600;line-height:1.4;display:flex;align-items:center;height:30px">${p[3]}</div>`;
    h += `<div style="${abs(px+20,460,pw-40,1)}background:#E1E3E9"></div>`;
    h += `<div style="${abs(px+20,472,80,16)}color:${p[5]};font-weight:800;font-size:9px;letter-spacing:.5px">역할</div>`;
    h += `<div style="${abs(px+20,492,pw-40,56)}color:#5A6478;font-size:10.5px;line-height:1.55;font-weight:600">${p[4]}</div>`;
    px+=pw+pg;
  });
  h += quote(ML,576,CW,60,"\"우리는 하나의 회사, 하나의 마이크로소프트다. 여러 세력으로 구성된 연합체가 아니다.\"","— Satya Nadella, 『히트 리프레시』 p152",true,11.5);
  h += take("3대 Pillar는 성장 마인드셋을 '외부(고객)·서로(동료)·전체(조직)'의 세 방향으로 작동시키는 설계도다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p151~153");
  h += `</div>`;
  push(h);
}

divider("05","구현 — 문화를 일상에 심다","Grounding the Pillars",[
  "선언을 현실로 — '큰 변화'(제도)와 '작은 변화'(넛지)의 동시 작동",
  "성과평가·보상 제도의 재설계, 리더의 솔선수범, 그리고 일상의 넛지",
]);

// ============================================================
// S22 — GROUNDING PRINCIPLE
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"05. 구현",kickW:70,sub:"구현의 원리 — '큰 변화'와 '작은 변화'의 동시 작동",n1:"05. 구현",n2:"1. 구현 원리"});
  h += gov([{t:"문화는 "},{t:"하나의 큰 조치가 아니라, 크고 작은 수많은 것들",hl:1},{t:"이 변화를 강화하며 만들어진다"}]);
  h += quote(ML,160,CW,62,"\"우리는 큰 변화를 만들었습니다 — 성과 평가 시스템을 바꾸는 것처럼. 그리고 작은 변화도 만들었습니다 … 우리는 결코 '단 하나의 조치'가 회사를 바꿀 거라고 믿지 않았습니다.\"","— Kathleen Hogan (CPO), LBS128 케이스",true,11);
  const LW=498, RX=ML+512, RW=498;
  h += card(ML,238,LW,338);
  h += sechdr(ML,238,LW,"큰 변화 (Big) — 제도를 바꾸다","#C0392B");
  const big=[
    ["성과평가 제도 개혁","Stack Ranking 폐지 → 절대평가·상시 피드백·코칭 (S23)"],
    ["보상 제도 개혁","등급-알고리즘 연동 폐지 → 매니저 재량 보상 예산 (S23)"],
    ["리더십 팀 재구성","SLT를 '하나의 first team'으로 재편 (S16)"],
    ["다양성 목표의 제도화","임원 보너스에 다양성 지표를 직접 연계 (S24)"]];
  let by=288;
  big.forEach(b=>{
    h += `<div style="${abs(ML+24,by,9,62)}background:#C0392B"></div>`;
    h += `<div style="${abs(ML+44,by+9,LW-70,18)}color:#1F3864;font-weight:700;font-size:11px">${b[0]}</div>`;
    h += `<div style="${abs(ML+44,by+30,LW-72,28)}color:#5A6478;font-size:9.5px;line-height:1.4">${b[1]}</div>`;
    by+=70;
  });
  h += card(RX,238,RW,338);
  h += sechdr(RX,238,RW,"작은 변화 (Small) — 일상을 바꾸다","#2E5BBA");
  const small=[
    ["회의 마무리 성찰","\"이 회의는 Growth였나 Fixed였나?\" — 성찰의 습관화 (S26)"],
    ["월간 학습 영상","나델라가 자신의 배움을 직접 공유 (S26)"],
    ["10가지 포용 행동 리스트","추상적 가치를 구체적 행동 목록으로 (S26)"],
    ["리더의 공개적 실패 인정","Grace Hopper·Tay 사건 — 취약성의 시연 (S25)"]];
  let smy=288;
  small.forEach(b=>{
    h += `<div style="${abs(RX+24,smy,9,62)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(RX+44,smy+9,RW-70,18)}color:#1F3864;font-weight:700;font-size:11px">${b[0]}</div>`;
    h += `<div style="${abs(RX+44,smy+30,RW-72,28)}color:#5A6478;font-size:9.5px;line-height:1.4">${b[1]}</div>`;
    smy+=70;
  });
  h += quote(ML,592,CW,44,"\"문화 쇄신을 위한 에너지는 우리 내부에 존재했다. 우리는 둑을 무너뜨려 변화가 흐르게 했다.\"","— Satya Nadella, 『히트 리프레시』 p162",false,10.5);
  h += take("제도(큰 변화)는 방향을 정하고, 넛지(작은 변화)는 일상에 스며든다 — 둘이 함께여야 문화가 바뀐다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p162");
  h += `</div>`;
  push(h);
}

// ============================================================
// S23 — HR SYSTEM REDESIGN  [핵심]
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"05. 구현",kickW:70,sub:"[핵심] 성과평가·보상 제도의 재설계",n1:"05. 구현",n2:"2. HR 제도 재설계"});
  h += gov([{t:"Stack Ranking을 폐지하고 "},{t:"'상대평가·강제배분'을 '절대평가·상시 피드백'",hl:1},{t:"으로 재설계했다"}]);
  // table
  const C0=ML, W0=156, C1=ML+156, W1=400, C2=ML+556, W2=454;
  const heads=["차원","As-Is — Stack Ranking","To-Be — 재설계"];
  [[C0,W0,"#1F3864"],[C1,W1,"#C0392B"],[C2,W2,"#2E5BBA"]].forEach((c,i)=>{
    h += `<div style="${abs(c[0],162,c[1],36)}background:${c[2]};color:#fff;font-weight:700;font-size:10px;display:flex;align-items:center;padding-left:12px">${heads[i]}</div>`;
  });
  const prows=[
    ["평가 철학","분류·도태 (Sort &amp; Yank)","성장·개발 (Grow &amp; Develop)"],
    ["평가 방식","상대평가 + 강제배분","절대평가 — 개인의 절대적 기여·성장 기준"],
    ["평가 주기","6개월마다 강제 서열화","상시 피드백·코칭 (continual feedback & coaching)"],
    ["등급","5등급 강제 분포 (10명 중 1명 必 Poor)","강제 분포 폐지"],
    ["보상 결정","등급에 알고리즘으로 자동 연동","매니저에게 '재량 보상 예산' 부여"],
    ["평가–보상 관계","등급 = 곧 돈 (한 몸)","평가(개발)와 보상(매니저 판단)을 부분 분리"]];
  let ry=198;
  prows.forEach((r,i)=>{
    const rh=44;
    h += `<div style="${abs(C0,ry,W0,rh)}background:#F5F6F9;border:1px solid #DCDFE6;color:#1F3864;font-weight:700;font-size:9.5px;display:flex;align-items:center;padding-left:12px">${r[0]}</div>`;
    h += `<div style="${abs(C1,ry,W1,rh)}background:${i%2?'#FCF4F2':'#FBEEEC'};border:1px solid #DCDFE6;color:#8E3A30;font-size:9.5px;display:flex;align-items:center;padding-left:12px">${r[1]}</div>`;
    h += `<div style="${abs(C2,ry,W2,rh)}background:${i%2?'#F0F4FB':'#EAF0FA'};border:1px solid #DCDFE6;color:#1F4B86;font-size:9.5px;display:flex;align-items:center;padding-left:12px">${r[2]}</div>`;
    ry+=rh;
  });
  // case note
  h += `<div style="${abs(ML,474,CW,50)}background:#F5F6F9;border-left:3px solid #1F3864"></div>`;
  h += `<div style="${abs(ML+16,482,CW-32,36)}color:#5A6478;font-size:8.5px;font-style:italic;line-height:1.5">`+
    `<b style="color:#1F3864;font-style:normal">케이스 원문 —</b> "The infamous stack-ranking system was abolished, replaced by continual feedback and coaching … managers are given a budget for compensation that they can hand out as they see fit."　·　<b style="color:#1F3864;font-style:normal">권기욱 칼럼 —</b> 상대평가→절대평가 전환, 관리자 권한의 대폭 이양</div>`;
  // 3 meaning cards
  h += `<div style="${abs(ML,536,CW,18)}color:#2E5BBA;font-weight:800;font-size:11px">재설계의 HRM적 의미</div>`;
  const mean=[
    ["상대평가 → 절대평가","'파이 나눠먹기'를 끝내고 각자의 절대적 성장을 본다 → 제로섬 구조의 해체"],
    ["서열 → 상시 피드백","평가가 '연 2회의 심판'에서 '일상의 코칭'으로 — 개발의 도구로 복귀"],
    ["평가·보상의 분리","보상은 매니저가 맥락으로 판단 — 평가가 '돈'에서 풀려나 '사람'을 향한다"]];
  const mw=326, mg=16; let mx=ML;
  mean.forEach(m=>{
    h += card(mx,560,mw,76,"background:#F5F6F9;border-color:#E1E3E9");
    h += `<div style="${abs(mx,560,7,76)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(mx+20,572,mw-32,16)}color:#1F3864;font-weight:800;font-size:10px">${m[0]}</div>`;
    h += `<div style="${abs(mx+20,592,mw-36,38)}color:#5A6478;font-size:9px;line-height:1.5">${m[1]}</div>`;
    mx+=mw+mg;
  });
  h += foot("출처: LBS128 케이스 / 권기욱 「조직문화 변화」 칼럼");
  h += `</div>`;
  push(h);
}

// ============================================================
// S24 — PILLARS GROUNDED
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"05. 구현",kickW:70,sub:"3대 Pillar의 현장 구현 — 말이 행동이 되다",n1:"05. 구현",n2:"3. Pillar의 구현"});
  h += gov([{t:"각 Pillar는 "},{t:"구체적인 '현장의 행동'과 '제도'",hl:1},{t:"로 번역되었다"}]);
  const gr=[
    ["Customer Obsession","고객 집착의 구현","#2E5BBA",[
      "오스트리아 GM Dorothee Ritz — 직원들을 '고객의 현장'으로 직접 파견",
      "한 계정 매니저는 경찰서에서 1주일, 다른 매니저는 병원에서 2일을 보내며 고객의 일을 직접 관찰",
      "\"고객의 문제를 함께 푸는 것\"이 추상적 워크숍보다 강력했다"]],
    ["Diversity & Inclusion","다양성·포용의 구현","#1F3864",[
      "훈련보다 '시니어 매니저의 행동 모델링'을 우선",
      "Xbox가 GDC 파티에서 부적절한 공연 → Phil Spencer가 신속히 공개 사과",
      "다양성 목표를 '수치'로 설정하고 시니어 경영진의 보너스에 연계 — 의도를 숫자로 못박다"]],
    ["One Microsoft","원 마이크로소프트의 구현","#C0392B",[
      "연례 해커톤 OneWeek — 부서를 넘어 한 팀으로",
      "첫해 83개국 1만 2천여 명이 3천여 개 해커톤에 참여 (난독증 학습도구가 실제 제품에 탑재된 사례)",
      "직급·부서 자격을 깨고 피인수 기업 창업자를 임원 리트릿에 초대"]]];
  let gy=162;
  gr.forEach(g=>{
    h += card(ML,gy,CW,150);
    h += `<div style="${abs(ML,gy,250,150)}background:${g[2]}"></div>`;
    h += `<div style="${abs(ML+20,gy+26,214,40)}color:#fff;font-weight:800;font-size:14px">${g[0]}</div>`;
    h += `<div style="${abs(ML+20,gy+66,214,40)}color:#D6DEEC;font-size:10.5px;font-weight:500">${g[1]}</div>`;
    let ly=gy+22;
    g[3].forEach(t=>{
      h += `<div style="${abs(ML+274,ly+5,7,7)}background:${g[2]}"></div>`;
      h += `<div style="${abs(ML+292,ly,CW-320,32)}color:#222838;font-size:10px;line-height:1.45">${t}</div>`;
      ly+=36;
    });
    gy+=162;
  });
  h += take("Pillar는 '구호'가 아니다 — 현장 방문, 보너스 연계, 해커톤 같은 '구체적 행동·제도'로 번역됐다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p154");
  h += `</div>`;
  push(h);
}

// ============================================================
// S25 — ROLE MODELING
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"05. 구현",kickW:70,sub:"리더의 솔선수범 — 취약성을 통한 신뢰",n1:"05. 구현",n2:"4. Role Modeling"});
  h += gov([{t:"나델라는 자신의 공개적 실패를 "},{t:"'성장 마인드셋의 시연'",hl:1},{t:"으로 전환했다"}]);
  const cases=[
    ["Grace Hopper 발언 사건","2014. 10","#C0392B",[
      ["발언","여성 컴퓨팅 학회에서 '임금 인상을 요구 못 하는 여성'에게 \"시스템을 믿고 기다리라\"고 답 → 거센 비판"],
      ["인정","전 직원에게 이메일로 \"내가 그 질문에 완전히 잘못 답했다\"고 공개적으로 인정"],
      ["행동","자신의 편견을 스스로 탐구하고, 임원진에게도 동일하게 요구했다"]],
      "Hogan: \"나는 Satya에 대한 신뢰가 줄지 않고 오히려 늘었다 — 그는 누구도 비난하지 않고, 그것을 자신의 책임으로 받아들였다.\""],
    ["Tay AI 챗봇 사건","2016. 03","#2E5BBA",[
      ["사건","출시 24시간 만에 트롤들에 의해 9.6만 개의 혐오 트윗 — 공개적 'humiliation'"],
      ["메시지","나델라는 개발팀에 \"계속 밀어붙여라. 나는 너희와 함께 있다\"고 메시지를 보냄"],
      ["전환","실패를 처벌하지 않고 학습으로 전환 — 이후 개선된 Zo를 출시했다"]],
      "실패를 '심리적 안전감(psychological safety)'을 구축하는 기회로 전환 — 리더가 먼저 취약성을 드러냈다."]];
  const cw=498, cg=14; let cx=ML;
  cases.forEach(c=>{
    h += card(cx,162,cw,474);
    h += `<div style="${abs(cx,162,cw,52)}background:${c[2]}"></div>`;
    h += `<div style="${abs(cx+22,162,cw-130,52)}color:#fff;font-weight:800;font-size:13px;display:flex;align-items:center;height:52px">${c[0]}</div>`;
    h += `<div style="${abs(cx+cw-110,162,90,52)}color:#fff;font-weight:700;font-size:10px;display:flex;align-items:center;justify-content:flex-end;height:52px">${c[1]}</div>`;
    let ly=234;
    c[3].forEach(t=>{
      h += `<div style="${abs(cx+24,ly,52,76)}background:#F5F6F9;border:1px solid #E1E3E9;color:${c[2]};font-weight:800;font-size:10px;display:flex;align-items:center;justify-content:center">${t[0]}</div>`;
      h += `<div style="${abs(cx+92,ly,cw-118,76)}color:#222838;font-size:10px;line-height:1.55;display:flex;align-items:center;height:76px">${t[1]}</div>`;
      ly+=86;
    });
    h += `<div style="${abs(cx+24,ly+6,cw-48,118)}background:#1F3864"></div>`;
    h += `<div style="${abs(cx+24,ly+6,6,118)}background:${c[2]}"></div>`;
    h += `<div style="${abs(cx+42,ly+22,cw-84,86)}color:#fff;font-size:10px;font-style:italic;line-height:1.7;display:flex;align-items:center;height:86px">${c[4]}</div>`;
    cx+=cw+cg;
  });
  h += take("\"완벽한 리더\"가 아니라 \"학습하는 리더\" — 리더가 먼저 취약성을 드러내야 심리적 안전감이 생긴다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p165~168");
  h += `</div>`;
  push(h);
}

// ============================================================
// S26 — NUDGES
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"05. 구현",kickW:70,sub:"일상의 넛지 — 환경에 심은 문화",n1:"05. 구현",n2:"5. 일상의 넛지"});
  h += gov([{t:"변혁은 큰 조치가 아니라, "},{t:"12.5만 명의 '일상'을 둘러싼 수많은 넛지",hl:1},{t:"로 내재화됐다"}]);
  const nd=[
    ["회의 마무리 리플렉션","모든 회의를 \"이 회의는 Growth였나 Fixed였나? 왜?\"로 마무리 — 성찰을 일상의 습관으로 만들었다","행동 넛지"],
    ["나델라의 월간 학습 영상","CEO가 매달 자신의 배움을 직접 공유 ('반쯤 마신 우유팩' 같은 자기 실수까지) — 학습 문화의 모델링","리더 모델링"],
    ["엘리베이터의 한자 '聽'","로비·맞이 공간에 '경청'을 상징하는 한자를 새김 — 물리적 환경에 가치를 각인했다","환경 신호"],
    ["식당 냅킨 홀더 메시지","\"평생 학습자가 되라\" — 일상의 가장 사소한 접점까지 메시지를 심어 반복 노출시켰다","환경 신호"],
    ["10가지 포용 행동 리스트","전 직원에게 배포하고 하나를 골라 토론 — 추상적 가치를 '구체적 행동'으로 번역했다","행동 넛지"],
    ["『히트 리프레시』 전 직원 배포","12.5만 명 전원에게 CEO의 책을 제공 — 비전 공유이자 전사적 문화 교육의 도구","교육 도구"]];
  const nw=326, ng=16, nh=158;
  let nx=ML, ny=162;
  nd.forEach((n,i)=>{
    h += card(nx,ny,nw,nh);
    h += `<div style="${abs(nx,ny,nw,6)}background:#2E5BBA"></div>`;
    h += `<div class="num-badge" style="${abs(nx+20,ny+20,34,34)}background:#2E5BBA;font-size:14px;line-height:34px">${i+1}</div>`;
    h += `<div style="${abs(nx+64,ny+18,nw-130,38)}color:#1F3864;font-weight:800;font-size:11.5px;line-height:1.25;display:flex;align-items:center;height:38px">${n[0]}</div>`;
    h += `<div style="${abs(nx+nw-78,ny+20,62,18)}background:#EAF0FA;color:#1F4B86;font-weight:700;font-size:7.5px;display:flex;align-items:center;justify-content:center">${n[2]}</div>`;
    h += `<div style="${abs(nx+20,ny+66,nw-40,1)}background:#E1E3E9"></div>`;
    h += `<div style="${abs(nx+20,ny+78,nw-42,70)}color:#5A6478;font-size:9.5px;line-height:1.6">${n[1]}</div>`;
    nx+=nw+ng;
    if(i%3===2){ nx=ML; ny+=nh+14; }
  });
  // synthesis strip
  h += `<div style="${abs(ML,506,CW,52)}background:#1F3864"></div>`;
  h += lbar(ML,506,52,"#C0392B");
  h += `<div style="${abs(ML+24,514,170,18)}color:#8FA3CC;font-weight:800;font-size:10px">넛지의 공통 원리</div>`;
  h += `<div style="${abs(ML+24,532,CW-48,18)}color:#fff;font-size:9.5px;font-weight:500">큰 제도 개혁이 '방향'을 정한다면, 넛지는 그 방향을 12.5만 명의 무의식적 일상에 스며들게 한다 — 회의·영상·한자·냅킨까지 모든 접점이 문화의 전달자</div>`;
  h += quote(ML,572,CW,64,"\"문화 쇄신은 어려운 작업이다. 사람들이 변화에 저항하는 근본적인 이유는 미지에 대한 두려움 때문이다.\"","— Satya Nadella, 『히트 리프레시』 p163",false,11);
  h += take("\"단 하나의 큰 조치\"는 없다 — 회의·영상·냅킨까지, 일상의 모든 접점이 문화의 전달자가 된다");
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p163");
  h += `</div>`;
  push(h);
}

divider("06","변화 — 퀸 모델로 확인하는 문화의 이동","Transformation",[
  "As-Is(위계+시장)에서 To-Be(관계+혁신)로 — 좌표로 확인하는 변화",
  "4년의 성과, 그리고 케이스가 남긴 미해결 과제",
]);

// ============================================================
// S28 — CVF TO-BE
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"06. 변화",kickW:70,sub:"퀸 모델로 본 To-Be — '관계 + 혁신'으로의 이동",n1:"06. 변화",n2:"1. CVF To-Be 좌표"});
  h += gov([{t:"문화의 무게중심이 "},{t:"'안정·통제'에서 '유연·재량' 축으로 이동",hl:1},{t:" — 위계·시장 → 관계·혁신"}]);
  h += card(ML,162,470,474,"background:#FAFBFC;border-color:#E1E3E9");
  h += `<div style="${abs(ML+24,182,420,20)}color:#1F3864;font-weight:700;font-size:12px">To-Be 좌표 — Nadella 전환 후</div>`;
  h += `<div style="${abs(ML+24,202,422,1)}background:#E1E3E9"></div>`;
  h += cvf(ML+92,266,326,262,"tobe");
  h += `<div style="${abs(ML+24,574,422,46)}background:#EDF5EF;border-left:3px solid #2F8F4E"></div>`;
  h += `<div style="${abs(ML+38,582,398,32)}color:#246B3C;font-size:9px;font-weight:600;line-height:1.5;display:flex;align-items:center;height:30px">무게중심이 '유연성' 축으로 이동 — As-Is(위계+시장)에서 To-Be(관계+혁신)로 좌표 자체가 옮겨졌다</div>`;
  const RX=540, RW=528;
  h += card(RX,162,RW,474,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,182,RW-40,20)}color:#1F3864;font-weight:700;font-size:13px">이동의 해석 — 무엇이 새 사분면을 채웠나</div>`;
  h += `<div style="${abs(RX+24,206,RW-48,2)}background:#1F3864"></div>`;
  const interp=[
    ["Clan (관계) 강화","Stack Ranking 폐지·상시 코칭으로 협력이 가능해졌고, One Microsoft·SLT 재구성으로 '하나의 팀' 의식이 형성됐다","#2F8F4E"],
    ["Adhocracy (혁신) 강화","성장 마인드셋·실패 학습(Tay)·OneWeek 해커톤으로 '도전과 창의'가 일상이 됐다","#2F8F4E"],
    ["유의점 — '시장'을 버린 게 아니다","경쟁력·실적(Market)을 포기한 것이 아니라, 부족했던 관계·혁신 축을 보강해 네 사분면의 '균형'을 재편한 것","#1F3864"]];
  let iy=224;
  interp.forEach((t,i)=>{
    const ch=i===2?134:130;
    h += card(RX+24,iy,RW-48,ch,"background:#fff;border-color:#E6E8ED");
    h += `<div style="${abs(RX+24,iy,7,ch)}background:${t[2]}"></div>`;
    h += `<div style="${abs(RX+44,iy+15,RW-90,18)}color:${t[2]};font-weight:700;font-size:11px">${t[0]}</div>`;
    h += `<div style="${abs(RX+44,iy+38,RW-92,80)}color:#222838;font-size:9.5px;line-height:1.6">${t[1]}</div>`;
    iy+=ch+8;
  });
  h += take("'기존 문화가 어떻게 변했나'의 답 — 위계·시장 고착에서 관계·혁신으로, 좌표 자체가 이동했다");
  h += foot("출처: LBS128 케이스 / 경쟁가치모형(Cameron & Quinn)으로 본 변화");
  h += `</div>`;
  push(h);
}

// ============================================================
// S29 — FOUR YEARS RESULTS
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"06. 변화",kickW:70,sub:"4년의 성과 — 'lumbering giant'에서 '인재 자석'으로",n1:"06. 변화",n2:"2. 4년의 성과"});
  h += gov([{t:"문화의 이동은 "},{t:"시총 $700B·Glassdoor 95%의 성과",hl:1},{t:"로 이어졌다 (2018, 케이스 시점)"}]);
  const kpis=[["$700B","시가총액 도달","주가 사상 최고가 경신"],["95%","Fortune 500의 Azure 채택","글로벌 50개 리전 — 클라우드 선두권"],
    ["29% → 95%","CEO Glassdoor 지지율","Ballmer → Nadella, 직원 신뢰 회복"],["Top 5","AI 기업 (직원 평가)","최고 엔지니어링 인재의 '자석'으로"]];
  const kw=242, kg=14; let kx=ML;
  kpis.forEach(k=>{
    h += card(kx,162,kw,160);
    h += `<div style="${abs(kx,162,kw,7)}background:#2F8F4E"></div>`;
    h += `<div style="${abs(kx+8,184,kw-16,52)}color:#1F3864;font-weight:900;font-size:${k[0].length>6?24:32}px;text-align:center;display:flex;align-items:center;justify-content:center">${k[0]}</div>`;
    h += `<div style="${abs(kx+12,242,kw-24,34)}color:#2F8F4E;font-weight:800;font-size:10.5px;text-align:center;line-height:1.3;display:flex;align-items:center;justify-content:center">${k[1]}</div>`;
    h += `<div style="${abs(kx+14,282,kw-28,32)}color:#5A6478;font-size:9px;text-align:center;line-height:1.4">${k[2]}</div>`;
    kx+=kw+kg;
  });
  h += card(ML,338,CW,170,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(ML+24,356,CW-40,20)}color:#1F3864;font-weight:700;font-size:12px">전략적 행동이 곧 '문화 시그널'이었다</div>`;
  h += `<div style="${abs(ML+24,378,CW-48,1)}background:#E1E3E9"></div>`;
  const sig=[["Office → iOS/iPad 출시","\"Windows 우선이 아닌 고객 우선\" — 캐시카우보다 고객을 택했다"],
    ["Linux 포용","\"적을 만드는 대신 배우겠다\" (과거 Ballmer: Linux = 암)"],
    ["LinkedIn $26B 인수","\"닫힌 조직을 외부 생태계와 통합하겠다\"는 의지의 표현"]];
  let sx=ML+24, scw=(CW-48-32)/3;
  sig.forEach(g=>{
    h += `<div style="${abs(sx,392,7,98)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(sx+20,396,scw-28,20)}color:#1F3864;font-weight:700;font-size:10.5px">${g[0]}</div>`;
    h += `<div style="${abs(sx+20,420,scw-32,64)}color:#5A6478;font-size:9.5px;line-height:1.55">${g[1]}</div>`;
    sx+=scw+16;
  });
  h += quote(ML,524,CW,112,"\"그들은 소문 속의 총을 내려놓고, 마이크로소프트가 사명을 완수할 새로운 방법을 발견했다.\"　— Exhibit 3의 '서로에게 총을 겨누던 조직도'를 떠올리게 하는 표현으로, 4년 만에 조직이 '경쟁'에서 '협력'으로 바뀌었음을 압축한다.","— Satya Nadella, 『히트 리프레시』 p129",true,11);
  h += take("문화 변혁은 '비용'이 아니라 '성장 엔진' — 협력·혁신의 문화가 클라우드·AI 전환을 가능케 했다");
  h += foot("출처: LBS128 케이스, Exhibit 2 / 『히트 리프레시』 p129");
  h += `</div>`;
  push(h);
}

// ============================================================
// S30 — UNRESOLVED
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"06. 변화",kickW:70,sub:"케이스가 남긴 미해결 과제",n1:"06. 변화",n2:"3. 미해결 과제"});
  h += gov([{t:"변혁은 Top과 현장은 움직였지만 — "},{t:"'빠진 고리'와 '오용의 위험'",hl:1},{t:"을 남겼다"}]);
  const LW=500, RX=ML+524, RW=486;
  h += card(ML,162,LW,474);
  h += sechdr(ML,162,LW,"과제 ① — 'Missing Middle' (중간관리자)","#C0392B");
  h += `<div style="${abs(ML+22,206,LW-44,56)}color:#222838;font-size:10px;line-height:1.65">취임 3년 후 설문에서 \"당신의 부사장·리더가 인재 육성에 우선순위를 두는가\"라는 질문의 응답이 <b>오히려 악화</b>됐다. 나델라가 직접 인정한 최대 미해결 과제다.</div>`;
  h += `<div style="${abs(ML+22,272,LW-44,16)}color:#5A6478;font-weight:700;font-size:9px">변혁의 침투 — 계층별 온도차</div>`;
  const lyr=[["최고경영진 · 시니어","변혁에 적극 동참","#2F8F4E","O"],["중간관리자 (VP·그룹리더)","인재 육성 지표 오히려 악화","#C0392B","X"],["일반 직원 · 현장","\"올바른 방향\"이라 응답","#2F8F4E","O"]];
  let lyy=294;
  lyr.forEach(L=>{
    const bad=L[2]==="#C0392B";
    h += `<div style="${abs(ML+22,lyy,LW-44,56)}background:${bad?'#FBEEEC':'#EDF5EF'};border:1px solid ${L[2]}"></div>`;
    h += `<div class="num-badge" style="${abs(ML+36,lyy+15,26,26)}background:${L[2]};font-size:11px;line-height:26px">${L[3]}</div>`;
    h += `<div style="${abs(ML+76,lyy,LW-96,56)}display:flex;align-items:center;height:56px"><span style="color:#1F3864;font-weight:700;font-size:10px">${L[0]}　—　</span><span style="color:${bad?'#8E3A30':'#5A6478'};font-size:9.5px">${L[1]}</span></div>`;
    lyy+=62;
  });
  h += quote(ML+22,488,LW-44,56,"\"우리에게는 빠진 고리가 있었다. 중간 관리자였다.\"","— 『히트 리프레시』 p173",false,11);
  h += `<div style="${abs(ML+22,556,LW-44,64)}background:#FBEEEC;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(ML+38,565,LW-72,48)}color:#8E3A30;font-size:9px;font-weight:600;line-height:1.55;display:flex;align-items:center;height:46px">→ 중간관리자는 평가·보상 제도를 실제로 '운영'하는 집행 계층. 이들이 '관리자→코치'로 바뀌지 않으면 제도 개혁도 작동하지 않는다.</div>`;
  // right
  h += card(RX,162,RW,474);
  h += sechdr(RX,162,RW,"과제 ② — '거짓 성장 마인드셋'","#C0392B");
  h += `<div style="${abs(RX+22,206,RW-44,72)}color:#222838;font-size:10px;line-height:1.65">한 매니저가 \"우리 팀원 5명은 성장 마인드셋이 없다\"고 보고하자, 나델라는 그것이 <b>'성장 마인드셋을 남을 비판하는 새 도구로 쓴 것'</b>이라며 일축했다.</div>`;
  h += quote(RX+22,288,RW-44,72,"\"여러분이 이 회사에서 리더가 되고 싶다면, 쓰레기통에서 보석을 찾아야 합니다.\"","— Satya Nadella, 『히트 리프레시』 p174",false,11);
  h += `<div style="${abs(RX+22,374,RW-44,16)}color:#5A6478;font-weight:700;font-size:9px">오용의 두 가지 양상</div>`;
  const mis=[["남을 평가하는 잣대로","'성장 마인드셋이 없다'며 동료를 재단 — 자기 성찰의 도구가 타인 비판의 무기로 변질"],
    ["면죄부로","\"나는 성장 중\"이라는 말로 현재의 부진을 정당화 — 책임 회피의 언어로 오용"]];
  let my=392;
  mis.forEach(m=>{
    h += `<div style="${abs(RX+22,my,RW-44,52)}background:#F5F6F9;border:1px solid #E1E3E9"></div>`;
    h += `<div style="${abs(RX+22,my,7,52)}background:#C0392B"></div>`;
    h += `<div style="${abs(RX+40,my+8,RW-78,16)}color:#1F3864;font-weight:700;font-size:9.5px">${m[0]}</div>`;
    h += `<div style="${abs(RX+40,my+25,RW-78,22)}color:#5A6478;font-size:8.5px;line-height:1.4">${m[1]}</div>`;
    my+=58;
  });
  h += `<div style="${abs(RX+22,512,RW-44,108)}background:#1F3864"></div>`;
  h += lbar(RX+22,512,108,"#C0392B");
  h += `<div style="${abs(RX+40,524,RW-80,18)}color:#8FA3CC;font-weight:800;font-size:10px">변혁의 최대 리스크</div>`;
  h += `<div style="${abs(RX+40,546,RW-82,68)}color:#fff;font-size:10px;font-weight:600;line-height:1.7">\"새로운 언어, 오래된 행동\" — 좋은 제도·언어도 운영자가 오용하면 변질된다. 제도 개혁이 행동 변화를 '보장'하지는 않으며, 이 리스크는 PART 7의 '호황기가 끝났을 때' 가장 위험하게 드러난다.</div>`;
  h += foot("출처: LBS128 케이스 / 『히트 리프레시』 p173~174");
  h += `</div>`;
  push(h);
}

divider("07","그 후 — 케이스 이후, 현재까지 (2018→2026)","Aftermath",[
  "케이스 이후의 성취 — 시총 $3조 돌파와 AI 시대의 주도",
  "2025년의 역설 — 사상 최대 이익 속의 대량 정리해고, 그리고 신뢰의 균열",
]);

// ============================================================
// S32 — AFTER THE CASE
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"07. 그 후",kickW:70,sub:"케이스 이후의 성취 — 문화 변혁이 만든 'AI 시대의 주도권'",n1:"07. 그 후",n2:"1. 케이스 이후"});
  h += gov([{t:"2018년 이후 Microsoft는 "},{t:"시총 $3조를 돌파하고 AI 시대를 주도",hl:1},{t:"했다"}]);
  const LW=500, RX=ML+524, RW=486;
  h += card(ML,162,LW,236,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(ML+22,182,LW-44,18)}color:#1F3864;font-weight:700;font-size:12px">케이스(2018) 이후의 궤적</div>`;
  h += `<div style="${abs(ML+22,204,LW-44,1)}background:#E1E3E9"></div>`;
  const traj=["시가총액 $700B(2018) → $3조 돌파 — 세계 최고 수준의 기업으로",
    "OpenAI와의 전략적 파트너십 — 생성형 AI 시대의 선두 주자로",
    "Azure·Copilot 등 클라우드·AI를 핵심 성장 엔진으로 확립",
    "케이스가 그린 '협력·혁신의 문화'가 AI 전환의 토대가 되었다는 평가"];
  let tjy=220;
  traj.forEach(t=>{
    h += `<div style="${abs(ML+24,tjy+5,7,7)}background:#2F8F4E"></div>`;
    h += `<div style="${abs(ML+40,tjy,LW-66,32)}color:#222838;font-size:9.5px;line-height:1.45">${t}</div>`;
    tjy+=42;
  });
  h += `<div style="${abs(ML,414,LW,222)}background:#1F3864"></div>`;
  h += lbar(ML,414,222,"#C0392B");
  h += `<div style="${abs(ML+24,434,LW-44,18)}color:#8FA3CC;font-weight:800;font-size:10.5px">케이스의 '해피엔딩'은 계속되는가?</div>`;
  h += `<div style="${abs(ML+24,460,LW-48,150)}color:#fff;font-size:11px;line-height:1.8">표면적으로 나델라의 문화 변혁은 <b>'성공 신화'</b>로 굳어졌다. 그러나 2025년, 그 신화에 균열을 내는 사건이 일어난다 — <b style="color:#fff">사상 최대 이익 속의 대량 정리해고</b>.</div>`;
  // right
  h += card(RX,162,RW,474,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,182,RW-40,20)}color:#1F3864;font-weight:700;font-size:12.5px">왜 '그 후'를 보는가 — 케이스를 넘어선 질문</div>`;
  h += `<div style="${abs(RX+24,206,RW-48,2)}background:#1F3864"></div>`;
  h += `<div style="${abs(RX+24,222,RW-48,46)}color:#222838;font-size:10px;line-height:1.6">케이스(2018)는 변혁의 '성공'에서 끝난다. 그러나 진짜 질문은 그 다음에 있다:</div>`;
  h += `<div style="${abs(RX+24,278,RW-48,86)}background:#fff;border:1px solid #D6D9E0"></div>`;
  h += `<div style="${abs(RX+44,294,RW-88,56)}color:#1F3864;font-size:11.5px;font-weight:700;font-style:italic;line-height:1.6;display:flex;align-items:center;height:54px">"성장 마인드셋·공감·One Microsoft의 문화는 — 호황기에만 작동하는가, 아니면 위기에도 지속되는가?"</div>`;
  h += `<div style="${abs(RX+24,382,RW-48,118)}color:#5A6478;font-size:10px;line-height:1.7">PART 6에서 본 '거짓 성장 마인드셋'의 리스크 — <b style="color:#1F3864">'새로운 언어, 오래된 행동'</b> — 이 위험은 2025년 대량 정리해고 국면에서 가장 첨예하게 시험대에 오른다.</div>`;
  h += `<div style="${abs(RX+24,512,RW-48,52)}background:#FBEEEC;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(RX+40,520,RW-72,38)}color:#C0392B;font-weight:700;font-style:italic;font-size:10.5px;display:flex;align-items:center;height:36px">→ 다음 장: 2025년의 역설 — 사상 최대 이익 속의 대량 정리해고</div>`;
  h += `<div style="${abs(RX+24,578,RW-48,40)}color:#9AA3B4;font-size:8.5px;line-height:1.5;display:flex;align-items:center;height:38px">※ 본 분석의 케이스 범위는 2018년까지이며, 'PART 7'은 외부 보도를 종합한 참고 확장이다</div>`;
  h += take("케이스의 '해피엔딩' 이후가 진짜 시험대 — 문화는 위기에도 지속될 때 비로소 '진짜'다");
  h += foot("출처: 외부 보도 종합 (케이스 이후 시점) — 본 분석의 케이스 범위는 2018년까지");
  h += `</div>`;
  push(h);
}

// ============================================================
// S33 — 2025 LAYOFFS PARADOX  [핵심]
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"07. 그 후",kickW:70,sub:"[핵심] 2025년의 역설 — 사상 최대 이익 속의 대량 정리해고",n1:"07. 그 후",n2:"2. 2025 정리해고"});
  h += gov([{t:"\"모든 객관적 지표에서 번창하는데, 동시에 정리해고를 한다\" — "},{t:"나델라가 부른 '수수께끼(enigma)'",hl:1}]);
  const LW=500, RX=ML+524, RW=486;
  h += card(ML,162,LW,300);
  h += sechdr(ML,162,LW,"규모 — 2025년 한 해의 정리해고","#C0392B");
  const nums=[["15,000+","2025년 한 해 누적 감원 — 회사 역사상 가장 공격적인 시기 중 하나"],
    ["9,000명","2025년 7월 단일 라운드 — 전체 인력의 약 4%에 해당"],
    ["$80B+","같은 해 AI 인프라(CapEx) 투자 — 감원과 동시에 진행됐다"],
    ["사상 최대","정리해고 와중에도 분기 이익·매출은 기록을 경신"]];
  let numy=210;
  nums.forEach(n=>{
    h += `<div style="${abs(ML+22,numy,112,52)}background:#FBEEEC;display:flex;align-items:center;justify-content:center;color:#C0392B;font-weight:900;font-size:14px">${n[0]}</div>`;
    h += `<div style="${abs(ML+146,numy,LW-168,52)}color:#222838;font-size:9.5px;line-height:1.45;display:flex;align-items:center;height:52px">${n[1]}</div>`;
    numy+=58;
  });
  h += quote(ML,478,LW,158,"\"우리 시대의 불확실성과 겉보기의 모순(incongruence)을 인정하고 싶다. 모든 객관적 지표로 보면 Microsoft는 번창하고 있다 … 그런데도 우리는 정리해고를 단행했다.\"","— Satya Nadella, 2025년 사내 메모 ('enigma' memo)",true,11.5);
  // right
  h += card(RX,162,RW,290,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,182,RW-40,18)}color:#1F3864;font-weight:700;font-size:12px">왜 — AI 시대의 구조조정 논리</div>`;
  h += `<div style="${abs(RX+24,204,RW-48,1)}background:#E1E3E9"></div>`;
  const why=["AI 인프라에 천문학적 투자 → 비용 구조의 전면 재편 압박",
    "관리 계층 축소(flattening) — 의사결정 속도 제고를 명분으로",
    "\"AI로 효율을 얻겠다\"면서 인력을 줄이는 빅테크 공통 흐름 (Meta·Amazon 등과 동시 진행)"];
  let wy=218;
  why.forEach(w=>{
    h += `<div style="${abs(RX+24,wy+5,7,7)}background:#C0392B"></div>`;
    h += `<div style="${abs(RX+40,wy,RW-66,42)}color:#222838;font-size:9.5px;line-height:1.55">${w}</div>`;
    wy+=48;
  });
  h += `<div style="${abs(RX+24,372,RW-48,62)}background:#FBEEEC;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(RX+40,381,RW-76,46)}color:#8E3A30;font-size:9px;font-weight:600;line-height:1.6;display:flex;align-items:center;height:44px">→ '성장을 위한 고통'이라는 논리. 그러나 직원에겐, 공감·One Microsoft를 외쳐온 회사의 '말과 행동의 불일치'로 다가왔다</div>`;
  h += `<div style="${abs(RX,468,RW,168)}background:#1F3864"></div>`;
  h += lbar(RX,468,168,"#C0392B");
  h += `<div style="${abs(RX+24,486,RW-44,18)}color:#8FA3CC;font-weight:800;font-size:10.5px">케이스의 가치와 충돌하는가?</div>`;
  h += `<div style="${abs(RX+24,512,RW-48,108)}color:#fff;font-size:11px;line-height:1.85">케이스가 그린 '공감의 리더십'과 'One Microsoft(하나의 가족)'의 서사 — 그것을 외쳐온 CEO가 15,000명을 내보낸다. 이 <b style="color:#fff">'모순'</b>은 본 발표 토론(S38)의 핵심 쟁점이 되며, '문화는 위기에도 지속되는가'라는 질문을 정면으로 던진다.</div>`;
  h += take("2025년의 역설 — '공감의 문화'는 호황기의 산물인가, 위기에도 지킬 수 있는 원칙인가");
  h += foot("출처: CNBC·GeekWire·Windows Central 등 외부 보도 종합 (2025) — 케이스 범위 밖, 참고용");
  h += `</div>`;
  push(h);
}

// ============================================================
// S34 — BACK TO OLD MICROSOFT
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"07. 그 후",kickW:70,sub:"다시 '옛 Microsoft'로? — 신뢰의 균열과 나델라의 응답",n1:"07. 그 후",n2:"3. 신뢰의 균열"});
  h += gov([{t:"직원들은 묻는다 — "},{t:"\"우리가 극복했던 '옛 Microsoft'로 돌아가는 것 아닌가\"",hl:1}]);
  const LW=500, RX=ML+524, RW=486;
  h += card(ML,162,LW,260,"background:#FBEEEC;border-color:#EBC9C3");
  h += lbar(ML,162,260,"#C0392B");
  h += `<div style="${abs(ML+24,182,LW-44,18)}color:#C0392B;font-weight:800;font-size:11.5px">균열 — 내부에서 들리는 우려</div>`;
  const cracks=["일부 장기 근속·전직 직원: 정리해고 처리 방식이 '나델라가 10년간 쌓은 따뜻한 환경'을 침식했다고 토로",
    "\"내부 경쟁, 소통 부재, 고용 불안 — 우리가 극복했던 '옛 Microsoft'의 징후가 다시 보인다\"",
    "사무실 복귀(주 3일) 의무화까지 겹치며 — '공감 부재'에 대한 직원 불만이 공개적으로 제기됨"];
  let cky=212;
  cracks.forEach(c=>{
    h += `<div style="${abs(ML+24,cky+5,7,7)}background:#C0392B"></div>`;
    h += `<div style="${abs(ML+40,cky,LW-66,52)}color:#222838;font-size:9.5px;line-height:1.55">${c}</div>`;
    cky+=64;
  });
  h += `<div style="${abs(ML,438,LW,198)}background:#1F3864"></div>`;
  h += lbar(ML,438,198,"#C0392B");
  h += `<div style="${abs(ML+24,458,LW-44,18)}color:#8FA3CC;font-weight:800;font-size:10.5px">나델라의 응답 (2025.9)</div>`;
  h += `<div style="${abs(ML+24,484,LW-48,134)}color:#fff;font-size:11px;font-style:italic;line-height:1.8">한 직원이 '회사 문화의 공감 부재'를 직접 제기하자, 나델라는 답했다 — "리더십 팀과 나에 대한 피드백으로 받아들이겠다. 결국 우리는 더 잘할 수 있고, 더 잘할 것이다(we will do better)."</div>`;
  // right
  h += card(RX,162,RW,256,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(RX+24,182,RW-40,18)}color:#1F3864;font-weight:700;font-size:12px">2026년 — 구조조정은 계속된다</div>`;
  h += `<div style="${abs(RX+24,204,RW-48,1)}background:#E1E3E9"></div>`;
  const y26=["2026년, 미국 직원 약 8,750명 대상 '자발적 조기퇴직(mutual separation)' 프로그램 — 회사 첫 사례",
    "AI 핵심 부서·Azure 엔지니어링은 제외 — '레거시 역할 축소'가 목적임을 시사",
    "CFO: \"향후 회계연도에도 인력은 더 줄어들 것\""];
  let y26y=218;
  y26.forEach(t=>{
    h += `<div style="${abs(RX+24,y26y+5,7,7)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(RX+40,y26y,RW-66,44)}color:#222838;font-size:9.5px;line-height:1.5">${t}</div>`;
    y26y+=48;
  });
  h += card(RX,434,RW,202,"background:#1F3864;border-color:#1F3864");
  h += lbar(RX,434,202,"#C0392B");
  h += `<div style="${abs(RX+24,454,RW-44,18)}color:#8FA3CC;font-weight:800;font-size:10.5px">HRM 관점의 읽기</div>`;
  h += `<div style="${abs(RX+24,480,RW-48,140)}color:#D6DEEC;font-size:10.5px;line-height:1.8">케이스의 교훈이 여기서 되돌아온다 — <b style="color:#fff">문화는 '제도와 행동의 정합성'이 깨지는 순간 가장 빠르게 무너진다.</b> '공감'을 선언으로만 두고 '정리해고의 실행 방식'이 그것과 어긋나면 — 10년의 변혁도 흔들릴 수 있다. 나델라의 "we will do better"는 그 위험을 스스로 인정한 말이다.</div>`;
  h += take("선언된 가치(공감)와 실행(정리해고 방식)의 정합성이 깨지면 — 문화 변혁의 성취도 되돌려질 수 있다");
  h += foot("출처: CNBC·GeekWire·Fast Company 등 외부 보도 종합 (2025~2026) — 케이스 범위 밖, 참고용");
  h += `</div>`;
  push(h);
}

divider("08","시사점 & 토론","Implications & Discussion",[
  "전략 의도·HR 제도·문화의 '정합성'이라는 핵심 교훈",
  "시앤피컨설팅 실무 적용, 그리고 '공감 vs 정리해고'의 모순을 둘러싼 토론",
]);

// ============================================================
// S36 — KEY LESSON
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"08. 시사점",kickW:80,sub:"핵심 교훈 — 전략 의도·HR 제도·문화의 '정합성'",n1:"08. 시사점",n2:"1. 핵심 교훈"});
  h += gov([{t:"MS의 변혁과 그 흔들림 모두가 말한다 — "},{t:"정합성(Alignment)이 조직 효과성을 결정한다",hl:1}]);
  const LW=648, RX=ML+672, RW=338;
  // transition table
  const c0=ML,w0=148,c1=ML+148,w1=250,c2=ML+398,w2=250;
  const heads=["층위","As-Is (Ballmer)","To-Be (Nadella)"];
  [[c0,w0,"#1F3864"],[c1,w1,"#C0392B"],[c2,w2,"#2E5BBA"]].forEach((c,i)=>{
    h += `<div style="${abs(c[0],162,c[1],36)}background:${c[2]};color:#fff;font-weight:700;font-size:10px;display:flex;align-items:center;padding-left:12px">${heads[i]}</div>`;
  });
  const tr=[["전략 의도","PC 수성 + 실적주의","역량 강화(empower) + 클라우드·AI"],
    ["HR 제도","Stack Ranking (상대·강제배분)","절대평가 + 상시 피드백·재량 보상"],
    ["조직문화","위계+시장 (Know-it-all)","관계+혁신 (Learn-it-all)"]];
  let ry=198;
  tr.forEach(r=>{
    const rh=58;
    h += `<div style="${abs(c0,ry,w0,rh)}background:#F5F6F9;border:1px solid #DCDFE6;color:#1F3864;font-weight:700;font-size:10px;display:flex;align-items:center;padding-left:12px">${r[0]}</div>`;
    h += `<div style="${abs(c1,ry,w1,rh)}background:#FCF4F2;border:1px solid #DCDFE6;color:#8E3A30;font-size:9.5px;display:flex;align-items:center;padding-left:12px">${r[1]}</div>`;
    h += `<div style="${abs(c2,ry,w2,rh)}background:#F0F4FB;border:1px solid #DCDFE6;color:#1F4B86;font-size:9.5px;display:flex;align-items:center;padding-left:12px">${r[2]}</div>`;
    ry+=rh;
  });
  h += `<div style="${abs(ML,378,LW,20)}color:#5A6478;font-style:italic;font-size:9px">→ 진단도 처방도 같은 3층위 — 전략 의도가 제도를, 제도가 문화를 만든다</div>`;
  // change mgmt card
  h += card(ML,406,LW,230,"background:#F5F6F9;border-color:#E1E3E9");
  h += `<div style="${abs(ML+22,424,LW-40,18)}color:#2E5BBA;font-weight:800;font-size:11.5px">변화관리 이론으로 본 종합</div>`;
  h += `<div style="${abs(ML+22,446,LW-44,1)}background:#E1E3E9"></div>`;
  const cm=[["Kotter 8단계","위기감(위기)→추진연합(SLT)→비전(선언)→전파→장애제거(제도)→단기성과→정착(넛지)에 정확히 매핑된다","#1F3864"],
    ["Schein 3수준","넛지(가시적 산물)→3대 Pillar(표방 가치)→\"누구나 성장한다\"(기본 가정)까지 깊이 파고들었다","#1F3864"],
    ["단, Lewin의 '재동결'은 거부","\"문화 쇄신은 종료일이 정해진 프로그램이 아니라 존재의 방식\"(p156) — 2025년의 흔들림이 이를 입증한다","#C0392B"]];
  let cmy=458;
  cm.forEach(c=>{
    h += `<div style="${abs(ML+22,cmy,7,52)}background:${c[2]}"></div>`;
    h += `<div style="${abs(ML+40,cmy+2,180,48)}color:${c[2]};font-weight:800;font-size:10px">${c[0]}</div>`;
    h += `<div style="${abs(ML+228,cmy,LW-258,52)}color:#5A6478;font-size:9px;line-height:1.5;display:flex;align-items:center;height:52px">${c[1]}</div>`;
    cmy+=58;
  });
  // right: proposition
  h += card(RX,162,RW,474,"background:#1F3864;border-color:#1F3864");
  h += `<div style="${abs(RX+26,184,RW-44,18)}color:#8FA3CC;font-weight:800;font-size:11px">핵심 명제</div>`;
  h += `<div style="${abs(RX+26,210,RW-52,140)}color:#fff;font-weight:800;font-size:19px;line-height:1.5">문화는<br>'전략·제도·행동'이<br>한 방향일 때만<br>변하고, 유지된다</div>`;
  h += `<div style="${abs(RX+26,356,80,3)}background:#C0392B"></div>`;
  const props=[["제도 없이 문화만 외치면","→ 구호로 끝난다","#8FA3CC"],
    ["철학 없이 제도만 바꾸면","→ 중간관리자가 되돌린다","#8FA3CC"],
    ["선언(공감)과 실행(정리해고)이 어긋나면","→ 10년의 변혁도 흔들린다","#fff"]];
  let py=378;
  props.forEach(p=>{
    h += `<div style="${abs(RX+26,py,RW-52,76)}background:#26406B"></div>`;
    h += `<div style="${abs(RX+26,py,6,76)}background:#C0392B"></div>`;
    h += `<div style="${abs(RX+42,py+12,RW-78,32)}color:#C7CFE0;font-size:9.5px;line-height:1.4">${p[0]}</div>`;
    h += `<div style="${abs(RX+42,py+44,RW-78,22)}color:${p[2]};font-weight:800;font-size:10.5px">${p[1]}</div>`;
    py+=84;
  });
  h += foot("출처: LBS128 케이스 / Kotter·Schein 이론 / 『히트 리프레시』 p156");
  h += `</div>`;
  push(h);
}

// ============================================================
// S37 — PRACTICAL IMPLICATIONS
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"08. 시사점",kickW:80,sub:"실무 시사점 — 시앤피컨설팅 관점",n1:"08. 시사점",n2:"2. 실무 시사점"});
  h += gov([{t:"MS 케이스는 컨설팅 펌의 '자기 진단'이자, "},{t:"클라이언트 변혁 컨설팅의 '방법론'",hl:1},{t:"이다"}]);
  const cw=498, cg=14;
  // card 1
  h += card(ML,162,cw,474);
  h += sechdr(ML,162,cw,"① 시앤피컨설팅 — 자사 인사제도 관점","#1F3864");
  h += `<div style="${abs(ML+24,208,cw-44,18)}color:#2E5BBA;font-weight:800;font-size:11px">구조적 유사성</div>`;
  h += `<div style="${abs(ML+24,228,cw-48,52)}color:#222838;font-size:9.5px;line-height:1.6">컨설팅 펌의 직급체계·프로젝트 단가 기반 평가·보상은 본질적으로 상대평가·내부경쟁 압력이 크다 — MS의 Stack Ranking과 구조적으로 닮았다.</div>`;
  h += `<div style="${abs(ML+24,288,cw-44,18)}color:#2E5BBA;font-weight:800;font-size:11px">적용 방향</div>`;
  const ap=["프로젝트 평가를 '도태'가 아닌 '역량 성장 피드백'으로 재설계",
    "컨설턴트 간 지식 공유·협업 기여를 보상에 반영 (One Microsoft식)",
    "파트너의 Role Modeling — '실패한 제안·프로젝트'를 학습 자산으로 공유"];
  let apy=312;
  ap.forEach(t=>{
    h += `<div style="${abs(ML+26,apy+5,7,7)}background:#2E5BBA"></div>`;
    h += `<div style="${abs(ML+42,apy,cw-70,40)}color:#222838;font-size:9.5px;line-height:1.5">${t}</div>`;
    apy+=46;
  });
  h += `<div style="${abs(ML+24,460,cw-48,60)}background:#FBEEEC;border-left:3px solid #C0392B"></div>`;
  h += `<div style="${abs(ML+40,470,cw-80,42)}color:#8E3A30;font-weight:700;font-size:9.5px;line-height:1.6;display:flex;align-items:center;height:40px">경영 환경이 어려울 때일수록 '선언한 가치'와 '인력 운영'의 정합성을 지킬 것 — MS의 2025년이 보여준 교훈</div>`;
  h += `<div style="${abs(ML+24,540,cw-48,76)}background:#F5F6F9;border:1px solid #E1E3E9"></div>`;
  h += `<div style="${abs(ML+40,552,cw-80,52)}color:#5A6478;font-size:9px;line-height:1.6;display:flex;align-items:center;height:52px">시앤피의 강점(HR 제도 설계 역량)에 'CVF 문화 진단 → 정합성 점검' 프로세스를 결합하면, 자사 인사제도 고도화의 표준 모델이 된다.</div>`;
  // card 2
  const RX=ML+cw+cg;
  h += card(RX,162,cw,474);
  h += sechdr(RX,162,cw,"② 클라이언트 — 컨설팅 서비스 관점","#2E5BBA");
  h += `<div style="${abs(RX+24,208,cw-44,18)}color:#2E5BBA;font-weight:800;font-size:11px">방법론 패키징</div>`;
  h += `<div style="${abs(RX+24,228,cw-48,40)}color:#222838;font-size:9.5px;line-height:1.6">'문화 진단(퀸 모델) → 전략 의도·HR 제도 정렬 → 변화관리 로드맵(Kotter)'을 컨설팅 상품으로 패키징한다.</div>`;
  h += `<div style="${abs(RX+24,276,cw-44,18)}color:#2E5BBA;font-weight:800;font-size:11px">경영진 설득 포인트</div>`;
  h += `<div style="${abs(RX+24,296,cw-48,40)}color:#222838;font-size:9.5px;line-height:1.6">"재무가 멀쩡해도 문화 부정합은 미래 가치를 잠식한다" — MS의 10년 주가 정체가 강력한 각성 메시지가 된다.</div>`;
  h += `<div style="${abs(RX+24,344,cw-44,18)}color:#C0392B;font-weight:800;font-size:11px">필수 설계 요소</div>`;
  const req=["성과평가·보상 제도를 문화와 '함께' 설계",
    "중간관리자 역할 전환(관리자→코치) 프로그램을 반드시 포함",
    "구조조정·위기 국면의 '가치-실행 정합성' 가이드까지 컨설팅 범위에 포함"];
  let rqy=368;
  req.forEach((t,i)=>{
    h += `<div class="num-badge" style="${abs(RX+26,rqy,22,22)}background:#C0392B;font-size:10px;line-height:22px">${i+1}</div>`;
    h += `<div style="${abs(RX+58,rqy,cw-86,44)}color:#222838;font-size:9.5px;line-height:1.5">${t}</div>`;
    rqy+=52;
  });
  h += `<div style="${abs(RX+24,532,cw-48,84)}background:#1F3864"></div>`;
  h += lbar(RX+24,532,84,"#C0392B");
  h += `<div style="${abs(RX+42,544,cw-84,60)}color:#fff;font-size:10px;font-weight:600;line-height:1.65;display:flex;align-items:center;height:60px">MS 케이스는 컨설턴트에게 '두 얼굴의 거울'이다 — 자사를 비추는 진단이자, 클라이언트에게 파는 방법론. 두 관점을 함께 가질 때 컨설팅의 설득력이 완성된다.</div>`;
  h += foot("출처: 케이스 분석 기반 실무 적용 — 시앤피컨설팅 관점");
  h += `</div>`;
  push(h);
}

// ============================================================
// S38 — DISCUSSION
// ============================================================
{
  let h = `<div class="slide">`;
  h += chrome({kick:"08. 토론",kickW:62,sub:"생각해 볼 내용 — 네 가지 쟁점",n1:"08. 시사점",n2:"3. 토론"});
  h += gov([{t:"정답을 찾는 게 아니라, "},{t:"케이스의 교훈을 '우리 조직의 현실'에 비춰본다",hl:1}]);
  const qs=[
    ["Q1","공감 vs 대량 정리해고 — 모순인가?","'공감'과 'One Microsoft(하나의 가족)'를 외쳐온 나델라가 2025년 15,000명을 내보냈다. 이것은 문화의 '배신'인가, 책임 있는 경영의 '불가피한 선택'인가?","논점: 문화의 진정성은 '위기 국면'에서 검증된다 — 호황기 문화 vs 항상성 문화","#C0392B"],
    ["Q2","상대평가 vs 절대평가 — 제도의 문제인가","Stack Ranking은 GE에선 성공, MS에선 실패했다. 제도 자체의 결함인가, 아니면 산업·전략 맥락과의 적합성(fit) 문제인가?","논점: 'best practice'는 없다 — 전략·산업 맥락에 맞는 'best fit'을 설계해야","#2E5BBA"],
    ["Q3","퀸 모델 — 문화는 '이동'시킬 수 있는가","MS는 위계·시장에서 관계·혁신으로 좌표를 옮겼다. 그러나 '시장(경쟁)'을 완전히 버릴 수는 없다 — 네 사분면의 '이상적 균형'은?","논점: 문화 전환은 '대체'가 아니라 '재균형' — 우리 조직의 현재 좌표는 어디인가","#1F3864"],
    ["Q4","우리 조직에의 적용 — 어디부터 바꿀까","우리 회사(또는 한국 기업)에 이식한다면 가장 먼저 바꿀 평가·보상 제도는? 가장 큰 현실적 장벽은 'Missing Middle'인가?","논점: 한국형 위계 문화에서 '중간관리자→코치' 전환의 현실적 장애물","#1F3864"]];
  const qw=498, qg=14, qh=224;
  let qx=ML, qy=162;
  qs.forEach((q,i)=>{
    h += card(qx,qy,qw,qh);
    h += `<div style="${abs(qx,qy,10,qh)}background:${q[4]}"></div>`;
    h += `<div style="${abs(qx+26,qy+18,82,44)}color:${q[4]};font-weight:900;font-size:26px">${q[0]}</div>`;
    h += `<div style="${abs(qx+110,qy+16,qw-132,52)}color:#1F3864;font-weight:800;font-size:13px;line-height:1.3;display:flex;align-items:center;height:50px">${q[1]}</div>`;
    h += `<div style="${abs(qx+26,qy+78,qw-50,1)}background:#E1E3E9"></div>`;
    h += `<div style="${abs(qx+26,qy+92,qw-52,80)}color:#5A6478;font-size:10px;line-height:1.7">${q[2]}</div>`;
    h += `<div style="${abs(qx+26,qy+178,qw-52,32)}background:#F5F6F9;border-left:3px solid ${q[4]}"></div>`;
    h += `<div style="${abs(qx+40,qy+184,qw-78,22)}color:#1F3864;font-size:8.5px;font-weight:600;line-height:1.3;display:flex;align-items:center;height:20px">${q[3]}</div>`;
    qx+=qw+qg;
    if(i%2===1){ qx=ML; qy+=qh+12; }
  });
  h += take("특히 Q1 — 케이스의 '해피엔딩' 너머, '공감의 문화'가 위기에도 진짜인지를 우리 스스로에게 물어보자");
  h += foot("출처: 케이스 분석 + 외부 보도(2025~2026) 기반 토론 설계");
  h += `</div>`;
  push(h);
}

// ============================================================
// S39 — CLOSING
// ============================================================
{
  let h = `<div class="slide" style="background:#1F3864">`;
  h += `<div style="${abs(0,0,W,9)}background:#C0392B"></div>`;
  h += `<div style="${abs(0,H-9,W,9)}background:#C0392B"></div>`;
  h += `<svg style="${abs(W-220,0,220,220)}" width="220" height="220"><path d="M220,0 L220,220 L0,0 Z" fill="#2B4A7A"/></svg>`;
  h += `<div style="${abs(72,62,800,40)}color:#fff;font-weight:900;font-size:27px">핵심 인사이트 5가지</div>`;
  h += `<div style="${abs(74,110,150,4)}background:#C0392B"></div>`;
  h += `<div style="${abs(74,124,700,20)}color:#8FA3CC;font-size:11px;font-weight:500">케이스 서사를 관통하는 다섯 개의 HRM 명제</div>`;
  const ins=[
    ["전략의 '의도'는 반드시 'HR 제도'로 번역된다","발머의 실적주의가 Stack Ranking을 낳았다 — 제도는 전략의 거울"],
    ["변화의 출발점은 제도가 아니라 리더의 '인간관'","나델라의 '공감'이 그 씨앗 — 'human system'을 먼저 바꾸려 했다"],
    ["문화 변혁 = 선언 + 제도 + 행동 + 환경의 '정합성'","미션·평가보상·솔선수범·넛지가 한 방향일 때만 문화는 바뀐다"],
    ["퀸 모델로 본 변화 — 좌표 자체가 이동했다","'위계+시장'의 안정·통제 축에서 '관계+혁신'의 유연성 축으로"],
    ["문화는 '존재의 방식' — 완결되지 않는다","선언과 실행이 어긋나면(2025 정리해고) 10년의 변혁도 흔들린다"]];
  let iy=164;
  ins.forEach((t,i)=>{
    h += `<div style="${abs(72,iy,979,66)}background:#26406B"></div>`;
    h += `<div style="${abs(72,iy,6,66)}background:#C0392B"></div>`;
    h += `<div class="num-badge" style="${abs(94,iy+15,36,36)}background:#C0392B;font-size:15px;line-height:36px">${i+1}</div>`;
    h += `<div style="${abs(150,iy+12,880,22)}color:#fff;font-weight:700;font-size:13px;display:flex;align-items:center;height:22px">${t[0]}</div>`;
    h += `<div style="${abs(150,iy+36,880,20)}color:#C7CFE0;font-size:10px;display:flex;align-items:center;height:20px">${t[1]}</div>`;
    iy+=74;
  });
  h += `<div style="${abs(72,540,979,96)}background:#2B4A7A"></div>`;
  h += lbar(72,540,96,"#C0392B");
  h += `<div style="${abs(96,556,940,64)}display:flex;flex-direction:column;justify-content:center;height:64px">`+
    `<span style="color:#fff;font-style:italic;font-size:13px;line-height:1.6">"우리는 많은 진전을 이뤘지만 결코 완수하지 못할 것이다. 문화 쇄신은 시작일과 종료일이 정해진 프로그램이 아니다. 그것은 존재의 방식이다."</span>`+
    `<span style="color:#8FA3CC;font-size:10px;margin-top:6px">— Satya Nadella, 『히트 리프레시』 p156</span></div>`;
  h += `<div style="${abs(72,664,8,40)}background:#C0392B"></div>`;
  h += `<div style="${abs(96,662,600,44)}color:#fff;font-weight:900;font-size:23px">감사합니다　·　Q &amp; A</div>`;
  h += `<div style="${abs(96,712,900,24)}color:#8FA3CC;font-size:10.5px">건국대학교 경영대학원 MBA　·　인적자원관리 (정혜정 교수)　·　Microsoft Case #7　·　발표: 이석주</div>`;
  PAGE++;
  h += `<div style="${abs(W-58,H-40,40,22)}text-align:right;color:#8190B5;font-weight:800;font-size:11px">${String(PAGE).padStart(2,"0")}</div>`;
  h += `</div>`;
  push(h);
}

// ===================== ASSEMBLY =====================
const _html = `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${slides.join("\n")}</body></html>`;
fs.writeFileSync("deck.html", _html);
console.log("BUILD OK — slides:", slides.length, "pages:", PAGE);
