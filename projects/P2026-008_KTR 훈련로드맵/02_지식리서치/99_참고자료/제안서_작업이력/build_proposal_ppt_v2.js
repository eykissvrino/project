const fs = require('fs');
const path = require('path');
const pptxgen = require('../.agent/skills/pptx/node_modules/pptxgenjs');
const html2pptx = require('../.agent/skills/pptx/scripts/html2pptx');

const BASE_DIR = __dirname;
const SLIDE_DIR = path.join(BASE_DIR, 'ppt_v2_slides');
const OUTPUT_PPTX = path.join(BASE_DIR, '제안서_발표자료_v2.pptx');
const LOGO_SOURCE = path.resolve(__dirname, '../.claude/skills/ppt-brand-guidelines/assets/logo.png');
const LOGO_NAME = 'logo.png';

fs.mkdirSync(SLIDE_DIR, { recursive: true });
fs.copyFileSync(LOGO_SOURCE, path.join(SLIDE_DIR, LOGO_NAME));

const color = {
  navy: '#1E293B',
  white: '#FFFFFF',
  lime: '#BDFF00',
  slate: '#64748B',
  off: '#F8FAFC',
};

function shell({ dark = false, content = '' }) {
  const bg = dark ? color.navy : color.white;
  const fg = dark ? color.white : color.navy;
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <style>
    html { background: ${bg}; }
    body {
      width: 720pt;
      height: 405pt;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      background: ${bg};
      font-family: Arial, Helvetica, sans-serif;
      color: ${fg};
      box-sizing: border-box;
    }
    * { box-sizing: border-box; }
    .page { display: flex; flex-direction: column; flex: 1; margin: 24pt 32pt; }
    h1 { margin: 0; font-size: 28pt; line-height: 1.25; color: ${fg}; }
    h2 { margin: 0; font-size: 22pt; line-height: 1.25; color: ${fg}; }
    h3 { margin: 0; font-size: 16pt; line-height: 1.3; color: ${fg}; }
    p { margin: 0; font-size: 12pt; line-height: 1.45; color: ${fg}; }
    .muted { color: ${dark ? '#94A3B8' : color.slate}; }
    .lime { color: ${color.lime}; }
    .grid-2 { display: flex; gap: 12pt; }
    .grid-3 { display: flex; gap: 10pt; }
    .grid-4 { display: flex; gap: 8pt; }
    .col { display: flex; flex-direction: column; gap: 8pt; flex: 1; min-width: 0; }
    .card {
      background: ${dark ? 'rgba(255,255,255,0.06)' : color.off};
      border-radius: 8pt;
      padding: 10pt;
      display: flex;
      flex-direction: column;
      gap: 5pt;
      min-width: 0;
    }
    .kpi { font-size: 34pt; font-weight: 700; line-height: 1; color: ${dark ? color.lime : color.navy}; }
    .small { font-size: 10pt; line-height: 1.35; }
    .tiny { font-size: 9pt; line-height: 1.3; }
    ul { margin: 0; padding-left: 14pt; }
    li { margin: 0; font-size: 11pt; line-height: 1.35; color: ${fg}; }
    .table-header { background: ${color.navy}; border-radius: 6pt 6pt 0 0; padding: 6pt 8pt; }
    .table-header p { color: ${color.white}; font-size: 10pt; font-weight: 700; }
    .row { display: flex; gap: 6pt; }
    .cell { flex: 1; background: ${dark ? 'rgba(255,255,255,0.06)' : color.off}; padding: 6pt; border-radius: 4pt; }
  </style>
</head>
<body>${content}</body>
</html>`;
}

const slides = [
  shell({
    dark: true,
    content: `<div class="page" style="justify-content:center; align-items:center; gap:18pt; margin:0 56pt;">
      <div style="width:74pt; height:74pt;"></div>
      <h1 style="font-size:31pt; text-align:center;">산업전환 공동훈련센터(KTR) AI 교육과정개발 반영 교육로드맵 체계구축 용역을 통해 KTR의 AI 전환 실행력을 높이겠습니다.</h1>
      <p class="muted" style="font-size:13pt; text-align:center;">시앤피컨설팅 주식회사 · 2026.04</p>
    </div>`,
  }),
  shell({
    dark: true,
    content: `<div class="page" style="justify-content:center; align-items:flex-start; gap:12pt;">
      <p class="lime" style="font-size:14pt; font-weight:700;">Section</p>
      <h1 style="font-size:44pt;">Ⅱ. 제안개요</h1>
      <p class="muted" style="font-size:14pt;">KTR이 직면한 구조적 과제를 데이터로 정의하고 실행 해법으로 연결합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:16pt;">
      <h2>현재 25개 과정 체계는 갖추었지만 AI 반영이 전무하여 즉시 개편이 필요합니다.</h2>
      <div class="grid-2" style="flex:1; align-items:center;">
        <div class="col" style="justify-content:center;">
          <p class="kpi" style="font-size:96pt;">0</p>
          <p style="font-size:16pt; font-weight:700;">AI 관련 과정</p>
          <p class="muted">2026년 운영 예정 25개 훈련과정 기준</p>
        </div>
        <div class="col" style="justify-content:center;">
          <div class="card"><p style="font-weight:700;">문제</p><p>기존 과정은 친환경·ESG·규제 중심으로 설계되어 AI 적용 업무를 다루지 못합니다.</p></div>
          <div class="card"><p style="font-weight:700;">의미</p><p>교육현장과 산업현장의 직무 변화 속도 사이에 구조적 미스매치가 발생했습니다.</p></div>
          <div class="card"><p style="font-weight:700;">결론</p><p>기존 과정을 유지한 채 AI 모듈을 이식하는 체계적 리디자인이 필요합니다.</p></div>
        </div>
      </div>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:12pt;">
      <h2>기업은 변화를 체감하지만 대응 역량과 조직 체계는 아직 부족합니다.</h2>
      <div class="grid-3" style="flex:1;">
        <div class="card" style="justify-content:center; align-items:center;"><p class="kpi">97.1%</p><p style="font-weight:700; text-align:center;">산업환경 변화 영향 인식</p><p class="small muted" style="text-align:center;">대부분 기업이 변화 압력을 체감</p></div>
        <div class="card" style="justify-content:center; align-items:center;"><p class="kpi">81.4%</p><p style="font-weight:700; text-align:center;">산업전환 단계 기업</p><p class="small muted" style="text-align:center;">전환은 시작했으나 미완료 상태</p></div>
        <div class="card" style="justify-content:center; align-items:center;"><p class="kpi">58.6%</p><p style="font-weight:700; text-align:center;">전담인력 미구성</p><p class="small muted" style="text-align:center;">실행 조직과 운영 역량이 부족</p></div>
      </div>
      <p class="muted">시사점: AI 전문가 양성보다 현장 실무자의 업무 내 AI 활용 역량 강화가 우선입니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:12pt;">
      <h2>산업군별로 AI가 바꾸는 업무가 다르므로 일률 교육이 아니라 맞춤 설계가 필요합니다.</h2>
      <div class="grid-4" style="flex:1;">
        <div class="card"><h3>플라스틱</h3><p class="small muted">13.7%</p><p class="small">배합 최적화, 불량 예측, 물성 시뮬레이션</p></div>
        <div class="card"><h3>화장품</h3><p class="small muted">18.7%</p><p class="small">제형 안정성 예측, 소비자 트렌드 분석</p></div>
        <div class="card"><h3>의료기기</h3><p class="small muted">8.3%</p><p class="small">규제문서 자동화, 사이버보안 위협 모델링</p></div>
        <div class="card"><h3>정밀화학</h3><p class="small muted">주요 산업군</p><p class="small">위험성 평가, 공정 이상징후 탐지</p></div>
      </div>
      <p class="muted">핵심: 산업군×직무 단위로 “이 업무에 이 AI”를 매핑해야 현장 적용이 가능합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:14pt;">
      <h2>과업은 질문에서 답을 도출하고 실행 산출물로 연결되는 인과 체인으로 설계됩니다.</h2>
      <div class="card"><p style="font-weight:700;">질문 1</p><p>현재 무엇을 가르치고 있고 AI로 무엇을 더 가르쳐야 하는가?</p></div>
      <div style="display:flex; justify-content:center;"><p class="lime" style="font-size:26pt;">↓</p></div>
      <div class="card"><p style="font-weight:700;">질문 2</p><p>확인된 Gap을 5년 로드맵으로 어떻게 메울 것인가?</p></div>
      <div style="display:flex; justify-content:center;"><p class="lime" style="font-size:26pt;">↓</p></div>
      <div class="card"><p style="font-weight:700;">질문 3</p><p>실제 과정 재설계와 신규 과정 개발을 어떻게 실행할 것인가?</p></div>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:12pt;">
      <h2>본 과업은 세 가지 추진 원칙으로 실행 가능성과 현장 적용성을 동시에 확보합니다.</h2>
      <div class="grid-3" style="flex:1;">
        <div class="card"><p style="font-weight:700;">원칙 1</p><p>AI를 별도 교육이 아닌 기존 직무 Skill 위에 이식합니다.</p><p class="small muted">전담인력 미구성 58.6% 환경에 적합</p></div>
        <div class="card"><p style="font-weight:700;">원칙 2</p><p>모든 판단을 전년도 182개 기업 1차 데이터 기반으로 수행합니다.</p><p class="small muted">추정이 아닌 검증 가능한 의사결정</p></div>
        <div class="card"><p style="font-weight:700;">원칙 3</p><p>Gap 크기×기업 수요로 우선순위를 정해 선택과 집중합니다.</p><p class="small muted">8개월·3천만원 내 최대 효과</p></div>
      </div>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>전년도 축적 자산을 즉시 활용해 착수 즉시 고품질 산출물을 도출하겠습니다.</h2>
      <div class="table-header"><p>전년도 자산 → 금년도 활용</p></div>
      <div class="col" style="gap:6pt;">
        <div class="row"><div class="cell"><p class="small"><b>182개 기업 DB</b></p></div><div class="cell"><p class="small">AI 역량 진단 설문·기업군 분류 즉시 적용</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>진단지 5영역 35문항</b></p></div><div class="cell"><p class="small">AI Readiness 모듈 추가로 도구 재활용</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>25개 과정 분석 데이터</b></p></div><div class="cell"><p class="small">Skill Matrix 구축 기간 단축</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>전문가 네트워크 22명</b></p></div><div class="cell"><p class="small">검증 Gate 즉시 운영으로 품질 확보</p></div></div>
      </div>
      <p class="muted">결론: 타 기관이 0에서 시작할 때 당사는 70% 준비된 상태에서 출발합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>7대 핵심 산출물은 KTR의 연간 편성·기업 안내·과정 운영까지 직접 활용됩니다.</h2>
      <div class="grid-2" style="flex:1;">
        <div class="col">
          <div class="card"><p class="small"><b>① AI Skill Taxonomy</b> · 연간 편성 기준표</p></div>
          <div class="card"><p class="small"><b>② 과정×AI Gap 분석표</b> · 보강/개편/신설 판단</p></div>
          <div class="card"><p class="small"><b>③ AI 반영 교육체계 개편안</b> · 중장기 교육 지도</p></div>
          <div class="card"><p class="small"><b>④ 2026~2030 마스터플랜</b> · 연도별 실행 로드맵</p></div>
        </div>
        <div class="col">
          <div class="card"><p class="small"><b>⑤ 기업유형별 학습경로</b> · 기업 상담/안내 즉시 활용</p></div>
          <div class="card"><p class="small"><b>⑥ 신규 AI 과정 11개 기획안</b> · 과정 신설 의사결정 지원</p></div>
          <div class="card"><p class="small"><b>⑦ 상세 커리큘럼 2개+</b> · 강사가 바로 운영 가능한 수준</p></div>
          <div class="card" style="background:${color.lime};"><p class="small" style="color:${color.navy};"><b>활용 시나리오</b>: KTR 담당자는 기업 상담 시 진단 결과에 맞는 학습경로를 즉시 제시할 수 있습니다.</p></div>
        </div>
      </div>
    </div>`,
  }),
  shell({
    dark: true,
    content: `<div class="page" style="justify-content:center; align-items:flex-start; gap:12pt;">
      <p class="lime" style="font-size:14pt; font-weight:700;">Section</p>
      <h1 style="font-size:44pt;">Ⅲ. 과업수행 계획</h1>
      <p class="muted" style="font-size:14pt;">Discover → Design → Develop의 3단계로 데이터 기반 실행체계를 완성합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:12pt;">
      <h2>3개 Phase는 순차 연결 구조로 설계되어 판단 근거와 실행 결과가 일관되게 이어집니다.</h2>
      <div class="grid-3" style="flex:1;">
        <div class="card"><h3>Phase 1. Discover</h3><p class="small">5~7월</p><p class="small">Skill Matrix·AI Skill Set·Gap 분석</p></div>
        <div class="card"><h3>Phase 2. Design</h3><p class="small">7~10월</p><p class="small">교육체계 개편·5개년 마스터플랜·학습경로</p></div>
        <div class="card"><h3>Phase 3. Develop</h3><p class="small">9~12월</p><p class="small">과정 재설계·신규 11개·상세 커리큘럼</p></div>
      </div>
      <p class="muted">각 Phase 종료 시 Gate 검증을 통해 다음 단계 품질을 보증합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>Phase 1에서는 기존 Skill과 목표 AI Skill의 차이를 계량화해 우선순위를 확정합니다.</h2>
      <div class="grid-3" style="flex:1;">
        <div class="card"><h3>Skill Matrix</h3><p class="small">25개 과정의 K/S/A 역량 추출</p><p class="small muted">산업군·직무군 기준 정렬</p></div>
        <div class="card"><h3>AI Skill Set</h3><p class="small">산업군×직무 AI 역량 체계화</p><p class="small muted">Lv1~Lv3 수준 정의</p></div>
        <div class="card"><h3>Gap 분석</h3><p class="small">유지/보강/개편/신설 판정</p><p class="small muted">후속 투자 우선순위 도출</p></div>
      </div>
      <p class="muted">핵심 질문: 25개 과정 중 AI 대응이 가장 시급한 과정은 무엇인가?</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:8pt;">
      <h2>AI Skill Taxonomy는 산업별 직무 변화에 맞춰 교육 목표를 정밀하게 정의합니다.</h2>
      <div class="table-header"><p>산업군별 핵심 AI Skill</p></div>
      <div class="col" style="gap:5pt; flex:1;">
        <div class="row"><div class="cell"><p class="small"><b>플라스틱</b></p></div><div class="cell"><p class="small">소재 물성 예측 · 불량 예측 · LCA 자동화</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>의료기기</b></p></div><div class="cell"><p class="small">규제문서 자동화 · 임상평가 설계 · 위협 모델링</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>화장품</b></p></div><div class="cell"><p class="small">제형 안정성 예측 · 트렌드 분석 · 유해성 예측</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>정밀화학</b></p></div><div class="cell"><p class="small">위험성 평가 · 공정 이상탐지 · 안전 리스크 예측</p></div></div>
      </div>
      <p class="muted">Lv1 리터러시 → Lv2 실무응용 → Lv3 고도화로 단계별 교육목표를 설정합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>우선순위 매트릭스로 2026년 즉시 착수 대상과 중기 과제를 구분하겠습니다.</h2>
      <div class="grid-2" style="flex:1;">
        <div class="col">
          <div class="card" style="flex:1;"><p class="small"><b>기업 수요 高 · Gap 大</b></p><p class="small">★ 최우선 개편/신설 (2026 착수)</p></div>
          <div class="card" style="flex:1;"><p class="small"><b>기업 수요 高 · Gap 小</b></p><p class="small">보강 중심의 빠른 적용</p></div>
        </div>
        <div class="col">
          <div class="card" style="flex:1;"><p class="small"><b>기업 수요 低 · Gap 大</b></p><p class="small">2027~2028 순차 개편</p></div>
          <div class="card" style="flex:1;"><p class="small"><b>기업 수요 低 · Gap 小</b></p><p class="small">현행 유지 및 모니터링</p></div>
        </div>
      </div>
      <p class="muted">판정 기준: Gap 크기 × 기업 수요 × 강사 확보 가능성</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:12pt;">
      <h2>Phase 2에서는 기존 3모듈 구조를 유지하면서 AI 레이어를 체계적으로 이식합니다.</h2>
      <div class="grid-3" style="flex:1;">
        <div class="card"><h3>모듈1 인사이트</h3><p class="small">산업동향 + 바이오화학×AI 트렌드</p></div>
        <div class="card"><h3>모듈2 실무공통</h3><p class="small">ESG/LCA + AI 데이터관리·자동화</p></div>
        <div class="card"><h3>모듈3 산업특화</h3><p class="small">산업별 과정 + AI 적용 실무 8개+</p></div>
      </div>
      <p class="muted">핵심: 기존 체계 안정성은 유지하고 과정 단위의 AI 적용성을 강화합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:8pt;">
      <h2>산업전환 단계와 AI 역량 수준을 교차해 기업별 진입점을 자동 매핑합니다.</h2>
      <div class="table-header"><p>산업전환 × AI 수준 매트릭스</p></div>
      <div class="col" style="gap:5pt; flex:1;">
        <div class="row"><div class="cell"><p class="small"><b>Lv1 선제대응(14.3%)</b></p></div><div class="cell"><p class="small">AI 개념·동향</p></div><div class="cell"><p class="small">도구 체험</p></div><div class="cell"><p class="small">-</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>Lv2 전환(81.4%)</b></p></div><div class="cell"><p class="small">활용 가능성 이해</p></div><div class="cell"><p class="small">실무 도구 활용</p></div><div class="cell"><p class="small">공정·품질 분석</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>Lv3 정착(4.3%)</b></p></div><div class="cell"><p class="small">-</p></div><div class="cell"><p class="small">전략 수립</p></div><div class="cell"><p class="small">R&D 고도화</p></div></div>
      </div>
      <p class="tiny muted">열 순서: AI 리터러시 / AI 실무응용 / AI 고도화</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>2026~2030 마스터플랜으로 단계별 확산·고도화·완성 경로를 제시합니다.</h2>
      <div class="grid-5" style="display:flex; gap:7pt; flex:1;">
        <div class="card" style="flex:1;"><p class="small"><b>2026</b></p><p class="tiny">기반 구축</p><p class="tiny">3~4개</p></div>
        <div class="card" style="flex:1;"><p class="small"><b>2027</b></p><p class="tiny">확산</p><p class="tiny">5~6개</p></div>
        <div class="card" style="flex:1;"><p class="small"><b>2028</b></p><p class="tiny">고도화</p><p class="tiny">7~8개</p></div>
        <div class="card" style="flex:1;"><p class="small"><b>2029</b></p><p class="tiny">선도</p><p class="tiny">9~10개</p></div>
        <div class="card" style="flex:1;"><p class="small"><b>2030</b></p><p class="tiny">완성</p><p class="tiny">11개+</p></div>
      </div>
      <p class="muted">연차별 목표와 도입 과정 수를 연동해 성과를 추적 가능한 계획으로 설계합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>협약기업 유형별 맞춤 학습경로를 제공해 기업이 스스로 시작점을 찾도록 지원합니다.</h2>
      <div class="col" style="flex:1;">
        <div class="card"><p class="small"><b>플라스틱 제조 50인 / Lv1</b>: AI 리터러시 → AI ESG 데이터관리 → 재진단</p></div>
        <div class="card"><p class="small"><b>의료기기 중견 200인 / Lv2</b>: AI 리터러시 → AI 규제 대응 → AI 성능평가</p></div>
        <div class="card"><p class="small"><b>화장품 벤처 30인 / Lv2</b>: AI 리터러시 → AI 트렌드 분석 → AI 제형 최적화</p></div>
      </div>
      <p class="muted">결과물은 KTR 담당자가 기업 상담 시 즉시 제시 가능한 가이드 형태로 제공됩니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>Phase 3에서는 기존 과정을 보강·개편하고 신규 과정을 개발해 실행력을 완성합니다.</h2>
      <div class="grid-2" style="flex:1;">
        <div class="card"><h3>기존 과정 재설계</h3><ul><li>보강: AI 모듈 1~2개 삽입</li><li>개편: 과정명·목표·교과목 전면 조정</li><li>현업 적용 과제 중심 실습 강화</li></ul></div>
        <div class="card"><h3>신규 과정 개발</h3><ul><li>산업특화 AI 8개 + 공통 AI 3개</li><li>교육목표·대상·시간·운영안 명시</li><li>상세 커리큘럼 2개 이상 개발</li></ul></div>
      </div>
      <p class="muted">핵심 질문: 어떤 과정을 우선 상세 커리큘럼으로 확정할 것인가?</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>신규 AI 과정 11개를 산업특화와 공통과정으로 구성해 단계별 수요를 충족합니다.</h2>
      <div class="grid-2" style="flex:1;">
        <div class="card"><p class="small"><b>산업특화 8개</b></p><ul><li>플라스틱 2개</li><li>의료기기 2개</li><li>화장품 2개</li><li>정밀화학 2개</li></ul></div>
        <div class="card"><p class="small"><b>공통 3개</b></p><ul><li>AI 리터러시 세미나</li><li>AI 활용 ESG 데이터관리</li><li>AI 활용 LCA 자동화</li></ul></div>
      </div>
      <p class="muted">Lv1~Lv3 난이도 체계에 맞춰 기업의 전환 수준별 선택이 가능하도록 설계합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:8pt;">
      <h2>상세 커리큘럼은 실습 40% 이상과 자사 적용 설계를 포함해 현장 적용성을 보장합니다.</h2>
      <div class="grid-2" style="flex:1;">
        <div class="card"><p class="small"><b>과정 A: 바이오화학 AI 리터러시(4H)</b></p><p class="tiny">AI 개념 → 산업사례 → 도구 체험 → 자사 적용 토론</p><p class="tiny muted">대상: 전 직급 / Lv1~2</p></div>
        <div class="card"><p class="small"><b>과정 B: AI 기반 바이오플라스틱 생산관리(8H)</b></p><p class="tiny">공정이해 → AI 원리 → 품질예측 실습 → 적용 설계</p><p class="tiny muted">대상: 생산·품질 / Lv2~3</p></div>
      </div>
      <div class="card"><p class="small"><b>공통 원칙</b>: 산업 데이터 기반 실습 · 평가체계 운영 · 교육 후 3개월 적용 추적</p></div>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>전년도 연속 수행 인력을 중심으로 Phase별 책임 구조를 명확히 운영하겠습니다.</h2>
      <div class="card" style="flex:1;">
        <p class="small"><b>PM</b> 유대훈 본부장</p>
        <p class="small">├─ <b>Phase 1 Discover</b> 이석주 팀장</p>
        <p class="small">├─ <b>Phase 2 Design</b> 조예슬 선임연구원</p>
        <p class="small">└─ <b>Phase 3 Develop</b> 안은하 선임연구원 · 허상희 연구원</p>
        <p class="small muted">AI컨설팅연구소 및 외부 자문위원회가 전 Phase에 상시 결합</p>
      </div>
      <p class="muted">역할·책임·의사결정 라인을 단순화해 일정 지연과 품질 리스크를 최소화합니다.</p>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:8pt;">
      <h2>전문가 Pool 22명을 즉시 가동해 산출물 검증과 교육 현장 적합성을 확보합니다.</h2>
      <div class="grid-3" style="flex:1;">
        <div class="card"><p class="small"><b>산업전문가 12명</b></p><p class="tiny">FGI 참여 8명 + 진단 검증 4명</p></div>
        <div class="card"><p class="small"><b>강사진 10명</b></p><p class="tiny">산업별 실무 교육 자문·검증</p></div>
        <div class="card"><p class="small"><b>AI/교육공학 자문</b></p><p class="tiny">AI컨설팅연구소 + 외부 전문가</p></div>
      </div>
      <div class="card"><p class="small">Gate 1(자문회의) → Gate 2(워크숍) → Gate 3(간담회) 3단계 검증으로 완성도를 높입니다.</p></div>
    </div>`,
  }),
  shell({
    content: `<div class="page" style="gap:10pt;">
      <h2>5월 착수부터 12월 최종보고까지 월별 마일스톤 기반으로 과업을 관리합니다.</h2>
      <div class="col" style="flex:1; gap:5pt;">
        <div class="row"><div class="cell"><p class="small"><b>5~7월</b></p></div><div class="cell"><p class="small">Phase 1 수행 · Gate1 · 중간보고</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>7~10월</b></p></div><div class="cell"><p class="small">Phase 2 수행 · Gate2(8월/10월)</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>9~11월</b></p></div><div class="cell"><p class="small">Phase 3 수행 · Gate3</p></div></div>
        <div class="row"><div class="cell"><p class="small"><b>12월</b></p></div><div class="cell"><p class="small">최종보고 및 산출물 납품</p></div></div>
      </div>
      <p class="muted">주간 진도관리·격주 협의·리스크 버퍼로 납기와 품질을 동시 관리합니다.</p>
    </div>`,
  }),
  shell({
    dark: true,
    content: `<div class="page" style="justify-content:center; align-items:center; gap:16pt; margin:0 70pt;">
      <div style="width:80pt; height:80pt;"></div>
      <h2 style="font-size:26pt; text-align:center; color:${color.white};">시앤피컨설팅은 데이터 기반 AI 교육로드맵으로 KTR의 산업전환 성과를 실질적으로 높이겠습니다.</h2>
      <p class="lime" style="font-size:16pt; font-weight:700;">Thank you.</p>
    </div>`,
  }),
];

slides.forEach((html, idx) => {
  const f = path.join(SLIDE_DIR, `slide-${String(idx + 1).padStart(2, '0')}.html`);
  fs.writeFileSync(f, html, 'utf8');
});

async function run() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = '시앤피컨설팅';
  pptx.subject = 'KTR AI 교육로드맵 제안';
  pptx.title = '제안서 발표자료 v2';
  pptx.lang = 'ko-KR';

  const builtSlides = [];
  for (let i = 1; i <= slides.length; i += 1) {
    const f = path.join(SLIDE_DIR, `slide-${String(i).padStart(2, '0')}.html`);
    const result = await html2pptx(f, pptx);
    builtSlides.push(result.slide);
  }

  builtSlides[0].addImage({ path: LOGO_SOURCE, x: 4.49, y: 0.72, w: 1.03, h: 1.03 });
  builtSlides[24].addImage({ path: LOGO_SOURCE, x: 4.44, y: 1.01, w: 1.11, h: 1.11 });

  await pptx.writeFile({ fileName: OUTPUT_PPTX });
}

run();
