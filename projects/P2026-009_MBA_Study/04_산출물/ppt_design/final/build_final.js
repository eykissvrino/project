const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('../html2pptx.js');

const DIR = __dirname;
const TMP = process.env.TEMP || 'C:/Users/PC/AppData/Local/Temp';
const FB = 'Paperlogy 7 Bold', FS = 'Paperlogy 6 SemiBold', FR = 'Paperlogy 4 Regular';
const ORANGE = 'F08000', CHAR = '3A3F45', INK = '26282B', RED = 'C0392B', GREEN = '1E8449',
      TINT = 'FDF1E3', GRAYB = 'DDE1E5', TXT = '3A3F45', GRAY = 'B8BFC6', OFF = 'FAFBFC';

const hdr = (t) => ({ text: t, options: { fill: { color: INK }, color: 'FFFFFF', bold: true, fontSize: 10, fontFace: FS, align: 'center' } });
const cell = (t, opt = {}) => ({ text: t, options: { fontSize: 9, color: TXT, fontFace: FR, valign: 'middle', ...opt } });
const area = (t) => cell(t, { fontFace: FS, fill: { color: TINT }, color: INK });
const ok2 = { text: '○', options: { color: GREEN, bold: true, align: 'center', fontSize: 13, fontFace: FB } };
const tri = { text: '△', options: { color: 'D9A441', bold: true, align: 'center', fontSize: 12, fontFace: FB } };
const bad = { text: '✗', options: { color: RED, bold: true, align: 'center', fontSize: 12, fontFace: FB } };

async function slide(pptx, file) {
  return html2pptx(path.join(DIR, file), pptx, { tmpDir: TMP });
}

async function main() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: 'A4L', width: 842 / 72, height: 595.5 / 72 });
  pptx.layout = 'A4L';
  pptx.author = '이석주';
  pptx.title = '시앤피컨설팅 HR시스템 진단 및 개선과제 — 인적자원관리 기말 프로젝트';

  // s01 표지, s02 요약, s03 프레임 (HTML only)
  await slide(pptx, 's01.html');
  await slide(pptx, 's02.html');
  await slide(pptx, 's03.html');

  // s04 회사현황 + 매출 차트(2012-2025)
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's04.html');
    s.addChart(pptx.charts.BAR, [{
      name: '매출액',
      labels: ['2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024','2025'],
      values: [3.5, 7.7, 13.4, 16.8, 2.8, 20.0, 18.8, 44.5, 59.9, 52.4, 77.6, 78.3, 85.9, 89.8],
    }], {
      ...p.find(x => x.id === 'rev-chart'),
      barDir: 'col', showLegend: false, showTitle: false,
      chartColors: [CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, ORANGE],
      showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: '6B7178', dataLabelFontSize: 7, dataLabelFontFace: FR, dataLabelFormatCode: '0.#',
      catAxisLabelFontSize: 7.5, catAxisLabelFontFace: FR, catAxisLineColor: GRAYB,
      valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMaxVal: 100, barGapWidthPct: 35,
    });
  }

  await slide(pptx, 's04b.html'); // 조직도·주요 사업
  await slide(pptx, 's05.html');

  // s05b HR 영역별 운영 현황 (As-Is) 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's05b.html');
    const fact = (t) => cell(t, { fontSize: 8.5 });
    const src = (t) => cell(t, { fontSize: 7.5, color: '8B9197', align: 'center' });
    s.addTable([
      [hdr('HR 영역'), hdr('현행 운영 (사실 기술)'), hdr('근거 자료')],
      [area('채용'), fact('결원 발생 시 수시채용 중심(신입·경력 혼합) — 최근 2년 입사자 27명. 체계적 온보딩·사회화 프로그램은 없음'), src('인원현황 (2025.1)')],
      [area('성과평가'), fact('본부·센터 단위 자체 운영 — 팀장 70% + 센터장 30%, 점수 합산으로 S~D 5등급(절대평가). KPI = 목표영업익(20~40%) + 신규사업(10~30%) + 프로젝트 품질(40%) + 역량개발(10~20%). 일부 본부는 사전 질의지·1on1 면담·평가자 체크리스트 운영'), src('25년 개인평가 계획')],
      [area('보상'), fact('주임 초임 3,400만 + 연 200만 정액 인상, 선임 연 300만 정액 인상(평가 무관) · 책임·수석은 등급(S~D)별 % + 물가상승률. 페이밴드 존재하나 비공개, 변동급(인센티브)은 소액'), src('임금 운영 기준')],
      [area('승진·경력'), fact('표준연한(3·4·4년) + 직급별 기준: 선임=PL 가능, 책임=PM 가능, 수석=독자 수주 2억+·전체 경영진 합격. 직속리더 평가의견서(3기준 × Exceeds/Meets/NI) + 심사위원회. 트랙은 단일(관리·영업형)'), src('승진심사 기준 (2026.4)')],
      [area('육성'), fact('공식 교육체계 없음 — 도제식 OJT·비공식 학습 의존. 교육훈련비 연 6,325만 원(인당 약 69만 원, 매출의 0.07%). 관계사 HR아카데미 보유하나 자사 컨설턴트 육성에는 미활용'), src('손익계산서 (2025)')],
      [area('유지관리'), fact('이직 관리 제도(Stay Interview·이직원인 분석) 없음 — 연 10~20명 퇴사(증가 추세), 근속 중앙값 2.5년. HR 전담 조직 없음(경영지원팀 2명이 인사행정 겸무)'), src('인원현황·내부 확인')],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 7,
      colW: [1.25, 7.72, 1.5],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s06 외적 정합성 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's06.html');
    s.addTable([
      [hdr('HR 영역'), hdr('차별화 전략이 요구하는 관행'), hdr('시앤피 현행'), hdr('정합성')],
      [area('직무분석·설계'), cell('다양한 직무 · 복잡한 업무 · 일반적 직무기술'), cell('적은 직무 분류, 프로젝트별 유동적 업무'), tri],
      [area('채용·선발'), cell('집중적인 사회화 · 일반적 스킬 평가'), cell('수시·결원 채용 중심, 온보딩 체계 미흡'), tri],
      [area('훈련·개발'), cell('미래 직무스킬 · 그룹 지향 · 전 직원 훈련'), cell('방향은 부합하나 체계 없는 도제식 — 인당 교육비 연 69만 원'), tri],
      [area('성과관리'), cell('결과+장기 기준 · 개발적 목적 · 그룹 중심'), cell('본부별 자체 평가, 당해 영업익 중심(20~40%) · 역량 비중 10~20%'), bad],
      [area('보상'), cell('장기 인센티브 · 외적 형평성 · 그룹 인센티브'), cell('주임·선임(48%) 평가 무관 자동 인상 · 변동급 미미 · 페이밴드 비공개'), bad],
      [area('노사/직원관계'), cell('참여식 의사결정 · 직원=자산'), cell('하향식 의사결정 관행'), bad],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 8,
      colW: [1.55, 3.5, 4.3, 1.12],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s07 내적 정합성 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's07.html');
    s.addTable([
      [hdr('제도 간 연계'), hdr('현황 진단'), hdr('판정')],
      [area('평가 ↔ 보상'), cell('S~D 절대평가를 운영하나 주임·선임 44명(48%)은 평가와 무관한 자동 정액 인상 — 성장 욕구가 가장 큰 주니어 층에서 수단성(Instrumentality)이 구조적으로 0. 책임·수석도 기본급 인상률 차등뿐, 변동급 미미'), bad],
      [area('평가 ↔ 육성'), cell('평가가 관리적 목적(연봉 조정)에 치우쳐 개발적(developmental) 기능 부재 — 평가 결과가 교육·코칭·경력으로 이어지는 경로 없음'), bad],
      [area('육성 ↔ 경력'), cell('승진 기준(PL→PM→독자수주)·심사위원회는 존재하나 기준 도달을 돕는 육성 체계가 없음 — 검증만 있고 육성은 개인 몫, 역량 기준도 추상적(행동지표 부재)'), bad],
      [area('채용 ↔ 유지'), cell('주니어 수시 채용 → 조기 이탈 → 재채용 반복 — 채용 투자가 유지 제도로 회수되지 못하는 회전문 구조 (최근 2년 입사자 44%)'), bad],
      [area('훈련 ↔ 전략'), cell('"학습과 연구"를 경영철학으로 표방하고 관계사 HR아카데미까지 보유하나, 자사 컨설턴트 육성은 비공식 OJT 의존 — 자원이 제도로 조직화되지 않음'), tri],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 6,
      colW: [1.7, 7.65, 1.12],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s08 VRIO 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's08.html');
    const vr = (t) => cell(t, { fontFace: FB, fill: { color: INK }, color: 'FFFFFF', fontSize: 10, align: 'center' });
    s.addTable([
      [hdr('요소'), hdr('핵심 질문 (Barney, 1995 — 강의 정의)'), hdr('판정'), hdr('시앤피 근거')],
      [vr('V 가치'), cell('인적자원이 전략 실행에 기여하고 경제적 가치를 제공하는가?'), ok2, cell('석·박사 51%(47명), 공인노무사 등 전문자격, 400여 개사 프로젝트 수행 — 수익 창출의 직접 원천')],
      [vr('R 희소성'), cell('경쟁자들이 보유하지 못한 희소한 자원인가?'), ok2, cell('일터혁신 13년 연속 수행기관(4년 연속 우수사례), NCS 개발·활용 노하우, HRM+HRD+노무 Total Solution 조합은 중소 컨설팅 시장에서 희소')],
      [vr('I 모방가능성'), cell('경쟁사가 동일하게 모방하거나 대체하기 어려운가?'), tri, cell('경로 의존성·인과적 모호성·사회적 복잡성으로 모방은 곤란 — 단, 핵심 노하우가 개인 암묵지에 체화되어 인력 이탈과 함께 유출되기 쉬움')],
      [vr('O 조직화'), cell('구조·프로세스·문화가 인적자원의 가치를 극대화하도록 정렬되어 있는가?'), bad, cell('평가·보상·육성 시스템 미정렬(p.6~7), HR 전담 조직 부재, 지식관리 부재 — "전체 시스템이 중요(Horizontal Integration)" 조건 불충족')],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 5,
      colW: [1.15, 3.0, 0.85, 5.47],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  await slide(pptx, 's09.html');
  await slide(pptx, 's10.html');

  // s11 대시보드 차트 2개
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's11.html');
    const years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025'];
    s.addChart(pptx.charts.BAR, [{ name: '매출액', labels: years, values: [44.5, 59.9, 52.4, 77.6, 78.3, 85.9, 89.8] }], {
      ...p.find(x => x.id === 'rev-chart'),
      barDir: 'col', showLegend: false, showTitle: false,
      chartColors: [CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, ORANGE],
      showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: '6B7178', dataLabelFontSize: 9, dataLabelFontFace: FR, dataLabelFormatCode: '0.0',
      catAxisLabelFontSize: 9.5, catAxisLabelFontFace: FR, catAxisLineColor: GRAYB,
      valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMaxVal: 100, barGapWidthPct: 40,
    });
    s.addChart(pptx.charts.LINE, [{ name: '영업이익률', labels: years, values: [18.1, 3.5, -3.1, 6.5, 4.2, 3.8, 2.6] }], {
      ...p.find(x => x.id === 'margin-chart'),
      lineSize: 2.5, showLegend: false, showTitle: false,
      chartColors: [RED], lineDataSymbol: 'circle', lineDataSymbolSize: 6,
      showValue: true, dataLabelPosition: 't', dataLabelColor: RED, dataLabelFontSize: 9, dataLabelFontFace: FR, dataLabelFormatCode: '0.0',
      catAxisLabelFontSize: 9.5, catAxisLabelFontFace: FR, catAxisLineColor: GRAYB,
      valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMinVal: -6, valAxisMaxVal: 22,
    });
  }

  // s12 임금 인상 구조 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's12.html');
    s.addTable([
      [hdr('직위'), hdr('기본급 인상 방식'), hdr('평가 연동')],
      [area('주임 (16명)'), cell('초임 3,400만 원 + 연 200만 원 정액 인상'), cell('없음 — 성과 무관', { color: RED, fontFace: FS, align: 'center' })],
      [area('선임 (28명)'), cell('연 300만 원 정액 인상 (최대 집단)'), cell('없음 — 성과 무관', { color: RED, fontFace: FS, align: 'center' })],
      [area('책임 (17명)'), cell('평가 등급(S~D)별 % + 물가상승률'), cell('인상률만 연동', { color: 'D9A441', fontFace: FS, align: 'center' })],
      [area('수석 (18명)'), cell('평가 등급(S~D)별 % + 물가상승률'), cell('인상률만 연동', { color: 'D9A441', fontFace: FS, align: 'center' })],
      [area('전 직위 공통'), cell('페이밴드 존재하나 비공개 · 변동급(인센티브) 미미'), cell('정보공정성 결손', { color: RED, fontFace: FS, align: 'center' })],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 6,
      colW: [1.25, 2.55, 1.56],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  await slide(pptx, 's13.html');
  await slide(pptx, 's14.html');

  // s15 Kerr 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's15.html');
    const A = (t) => cell(t, { fontFace: FS, color: GREEN });
    const B = (t) => cell(t, { fontFace: FS, color: RED });
    s.addTable([
      [hdr('회사가 바라는 것 (Hoping for A)'), hdr('실제로 보상되는 것 (Rewarding B)'), hdr('결과')],
      [A('장기 전문성 축적 — 차별화 전략의 원천'), B('당해연도 영업익 달성률 (KPI 최대 40%)'), cell('단기 수주 우선, 역량 투자는 뒷전으로 밀림')],
      [A('본부 간 협업·지식공유 — Total Solution의 전제'), B('본부별 영업익 — 본부 단위 평가·보상'), cell('사일로 강화 (2025 조직재설계 과제 진단과 일치)')],
      [A('주니어의 도전과 성장 — 1990년대생 40%'), B('근속 연수 — 평가 무관 자동 인상'), cell('"잘해도 똑같다" — 고성과 주니어부터 이탈')],
      [A('고객과의 장기 파트너십 — 재계약 기반'), B('신규 수주 금액 (신규사업 발굴 KPI)'), cell('기존 고객 사후관리의 보상 공백')],
      [A('전문가로의 성장 — 학습·연구 철학'), B('영업 능력 — 수석 승진 = 독자 수주 2억'), cell('딜리버리 전문가의 성장 천장 → 이탈')],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 6,
      colW: [3.65, 3.45, 3.37],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s16 목표 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's16.html');
    s.addTable([
      [hdr('영역'), hdr('3년 목표'), hdr('핵심 지표')],
      [area('① 평가·보상'), cell('상시 성과관리 정착 + 강력한 성과 보상', { fontSize: 8 }), cell('체크인 90% · 수용도 70% · 잡플 3.5', { fontSize: 8 })],
      [area('② 확보·유지'), cell('핵심인재 이탈 차단', { fontSize: 8 }), cell('퇴사 연 7명 이하 · 근속 2.5→4년', { fontSize: 8 })],
      [area('③ 육성·경력'), cell('컨설턴트 성장 시스템 구축', { fontSize: 8 }), cell('역량모델·CDP 100% · 교육 40h/인', { fontSize: 8 })],
      [area('재무 연동'), cell('인적자본 생산성 회복', { fontSize: 8 }), cell('인당 매출 1.2억 · 영업이익률 8%', { fontSize: 8 })],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 5,
      colW: [1.0, 1.95, 1.97],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s17 E-I-V 맵 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's17.html');
    const ring = (t, c) => ({ text: t, options: { fontFace: FB, fill: { color: c }, color: 'FFFFFF', fontSize: 10.5, align: 'center', valign: 'middle' } });
    s.addTable([
      [hdr('동기의 고리'), hdr('끊어진 지점 (진단)'), hdr('복원 과제 (처방)')],
      [ring('E\n노력→성과', ORANGE), cell('역량을 키워주는 시스템 부재 — 성장이 운(어느 팀장)에 의존, 승진 기준은 추상적 (이슈③)'), cell('B1 역량모델(행동지표) · B2 경력경로 CDP·전문가 트랙 · B3 컨설턴트 아카데미(70:20:10) · B4 지식관리 + A2 상시 피드백(분기 OKR 체크인)')],
      [ring('I\n성과→보상', CHAR), cell('구성원 48% 평가-보상 무관(자동 인상), 변동급 ≈ 0, 단기 영업익만 보상 — Kerr의 오류 (이슈①)'), cell('A1 평가 단순화·전사 표준화(프로젝트 단위 리뷰) · A3 보상 4P 재설계 — 자동 인상 폐지, 성과 연동 변동급(Gain/Profit-sharing), 별도 캘리브레이션, 페이밴드 공개')],
      [ring('V\n보상→가치', GREEN), cell('보상 수준 시장 열위(초임 3,400만), 금전 외 보상(성장·인정)도 빈약 (이슈①·②)'), cell('A4 총보상 체계(직접+간접+비금전: 자율성·성장·인정 — 자기결정이론 3욕구) · C5 핵심인재 리텐션(장기 인센티브) · Pay Level의 시장 경쟁력 회복(Top of Market 지향)')],
      [ring('기반', '8B9197'), cell('사슬 전체를 측정·관리할 주체와 데이터 부재'), cell('C1 HR 전담 기능 신설("자사를 0호 고객사로") · C2 구성원 경험 진단(eNPS·Stay Interview·이직원인 분석)')],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 5,
      colW: [1.3, 3.6, 5.57],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s18 단기 액션플랜 상세 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's18.html');
    const ac = (t, opt = {}) => cell(t, { fontSize: 8.5, ...opt });
    const aq = (t) => ac(t, { align: 'center', fontFace: FS, color: INK });
    const at = (t) => ac(t, { fontFace: FS, color: INK });
    const ko = (t) => ac(t, { color: 'A85A00', fontFace: FS });
    s.addTable([
      [hdr('분기'), hdr('과제'), hdr('핵심 실행 내용'), hdr('산출물'), hdr('담당'), hdr('성공지표 (KPI)')],
      [aq("'26 3Q"), at('C1 HR 전담 신설'), ac('HR파트 지정(전담 1명+겸직 TF 4명), 사내 컨설팅 프로젝트로 공식 발족 — 수익성 데이터 공유로 위기감 조성, 킥오프 전사 설명회(Kotter ①·②)'), ac('TF 발족문, 추진 로드맵'), ac('대표이사'), ko('TF 발족, 전사 설명회 1회')],
      [aq("'26 3Q"), at('C2 구성원 경험 진단'), ac('전 직원 조직진단 서베이(자사 HR진단 솔루션 활용), 최근 2년 퇴직자 이직원인 분석, 직위·본부별 보상 데이터 분석'), ac('진단 보고서, 이직원인 Top5'), ac('TF'), ko('응답률 80%+')],
      [aq("'26 3~4Q"), at('B1 역량모델 구축'), ac('우수성과자 BEI 인터뷰(8~10명) + 전문가 패널 워크숍 → 역량군-역량-행동지표 도출 → 타당성 검증 (자사 역량모델링 방법론 활용)'), ac('컨설턴트 역량모델 1식'), ac('TF+본부'), ko('행동지표 커버리지 100%')],
      [aq("'26 4Q"), at('A1 평가 재설계'), ac('프로젝트 단위 간이 리뷰(5문항) + 연 1회 종합 리뷰(3단계) 설계, 우수 본부 1on1 관행 전사 표준화, 구성원 의견수렴 2회, 평가자 교육'), ac('신평가제 운영안, 평가자 가이드'), ac('TF'), ko("'27.1Q 시행, 수용도 60%+")],
      [aq("'27 1Q"), at('A2 상시 성과관리'), ac('분기 OKR 체크인 + 원온원(CFR) 도입 — "보상 산정과 분리" 원칙을 공표하여 도전적 목표와 솔직한 피드백 보호'), ac('OKR 가이드, 원온원 툴킷'), ac('본부장'), ko('분기 체크인 실시율 90%')],
      [aq("'27 1~2Q"), at('B2 경력경로 공표'), ac('승진 기준(PL→PM→수주)을 역량모델 행동지표로 구체화, 직위별 육성 로드맵 연결, 전문가 트랙(Dual Ladder) 설계'), ac('CDP 가이드북'), ac('TF'), ko('전 직위 커버, 설명회 1회')],
      [aq("'27 2Q"), at('A3 보상 설계 착수'), ac('시장 임금 조사(외부 형평성) + 직무·역량 가치 분석(내부 형평성) → Pay Band 재설계안, 변동급(집단 성과배분) 시뮬레이션 — 넥스트보상연구본부 방법론 활용'), ac('보상 개편안 1식'), ac('TF+보상硏'), ko("'27.3Q 경영진 보고")],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 8,
      colW: [0.72, 1.3, 3.95, 1.55, 0.85, 2.1],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s18x 변경 총괄표 (As-Is → To-Be)
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's18x.html');
    const dom = (t) => cell(t, { fontFace: FB, fill: { color: INK }, color: 'FFFFFF', fontSize: 9.5, align: 'center' });
    const asis = (t) => cell(t, { fontSize: 8, color: '8B9197' });
    const tobe = (t) => cell(t, { fontSize: 8, fontFace: FS, color: 'A85A00' });
    const why = (t) => cell(t, { fontSize: 7.5 });
    s.addTable([
      [hdr('제도'), hdr('As-Is (현재)'), hdr('To-Be (개선)'), hdr('이론적 근거 — 왜 바꾸는가'), hdr('실행적 근거 — 어떻게 가능한가')],
      [dom('성과평가\n(A1)'), asis('100점 산식·8개 KPI, 당해 영업익 중심(20~40%), 본부별 자체 운영으로 기준 상이'), tobe('2층 구조 — 프로젝트 리뷰(개발용) + 연간 종합 3단계, 전사 표준 + 캘리브레이션'), why('평가 5대 기준(Noe·S7): 단순하고 구체적인 기준이 수용성·신뢰성을 높임 · MS 사례 — 절대평가+상시 피드백'), why('우수 본부의 1on1·체크리스트 인프라 재활용 → 추가 비용 최소, \'27.1Q 시행 가능')],
      [dom('상시\n성과관리\n(A2)'), asis('연 1회 연말 평가 외 공식적 성과 대화 없음 — 기억 의존 평가, 피드백 공백'), tobe('분기 OKR 체크인 + CFR(대화·피드백·인정) — 보상 산정과 분리 운영'), why('OKR — "평가도구가 되는 순간 변질"(Doerr·S8) · 수시(CONTINUOUS) 성과관리(S7) · 자기결정이론 — 유능감·관계성(S9)'), why('프로젝트 종료 리듬과 일치, 문서 1장 원칙 — 92명 규모에 맞는 경량 운영, 추가 시스템 불필요')],
      [dom('보상\n(A3·A4)'), asis('주임·선임 자동 정액 인상(평가 무관, 구성원 48%), 책임·수석 인상률만 차등, 변동급 ≈ 0, 페이밴드 비공개'), tobe('Pay Band 공개 + 인상 매트릭스(밴드 위치×리뷰) + 변동급 2층(프로젝트 Gain-sharing·전사 Profit-sharing)'), why('기대이론 — 수단성(I) 복원(S7) · 4P Model·외부/내부 형평성·총보상(S9) · Gain-sharing 설계 3요소(Harrah\'s) · 정보공정성(S7)'), why('넥스트보상연구본부 방법론 자체 보유 — 외주 불필요 · 변동급은 이익 연동이라 고정비 증가 없음')],
      [dom('육성·경력\n(B1·B2·B3)'), asis('승진 기준(검증)만 있고 육성 없음 — 도제식 의존, 인당 교육비 69만 원, 단일 사다리(수석=영업 필수)'), tobe('역량모델(행동지표) + 직위별 육성 로드맵 + Dual Ladder(전문가 트랙 신설) + 컨설턴트 아카데미'), why('역량모델링·BEI(McClelland·S5) · 70:20:10의 \'10\' 설계(S10) · 피터의 법칙 방지(S8) · 유능감 충족(S9)'), why('관계사 HR아카데미 인프라 활용 — 한계비용 낮음 · 역량모델링은 자사의 핵심 상품(자체 수행)')],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 5,
      colW: [1.0, 2.3, 2.35, 2.5, 2.32],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  // s18a~d 제도 세부 설계 4종 (HTML only)
  await slide(pptx, 's18a.html');
  await slide(pptx, 's18b.html');
  await slide(pptx, 's18c.html');
  await slide(pptx, 's18d.html');

  // s19 중장기 간트
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's19.html');
    const qh = (t) => ({ text: t, options: { fill: { color: INK }, color: 'FFFFFF', bold: true, fontSize: 9, align: 'center', fontFace: FS } });
    const task = (t) => ({ text: t, options: { fontSize: 9, color: TXT, align: 'left', fontFace: FR } });
    const E = { text: '', options: { fill: { color: ORANGE } } };
    const I = { text: '', options: { fill: { color: CHAR } } };
    const V = { text: '', options: { fill: { color: GREEN } } };
    const G = { text: '', options: { fill: { color: GRAY } } };
    const o = { text: '', options: { fill: { color: OFF } } };
    s.addTable([
      [qh('과제'), qh("'26 3Q"), qh('4Q'), qh("'27 1Q"), qh('2Q'), qh('3Q'), qh('4Q'), qh("'28"), qh("'29")],
      [task('C1 HR 전담 기능 신설 — "자사를 0호 고객사로"'), G, o, o, o, o, o, o, o],
      [task('C2 구성원 경험 진단 (eNPS·이직원인 분석)'), G, G, o, o, o, o, o, o],
      [task('B1 컨설턴트 역량모델 구축 (BEI·행동지표)'), E, E, o, o, o, o, o, o],
      [task('A1 평가 단순화·전사 표준화 (프로젝트 단위 리뷰)'), o, I, I, o, o, o, o, o],
      [task('A2 상시 성과관리 OKR+CFR — 보상과 분리 운영'), o, o, I, I, I, I, I, I],
      [task('B2 경력경로 CDP·전문가 트랙(Dual Ladder) 설계'), o, o, E, E, o, o, o, o],
      [task('A3 보상체계 4P 재설계 (변동급·페이밴드 공개)'), o, o, o, I, I, I, I, o],
      [task('B3 CNP 컨설턴트 아카데미 (70:20:10 체계화)'), o, o, o, o, E, E, E, E],
      [task('B4 지식관리 체계 (프로젝트 방법론·산출물 자산화)'), o, o, o, o, o, E, E, E],
      [task('A4·C5 총보상 체계 + 핵심인재 리텐션 프로그램'), o, o, o, o, o, o, V, V],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 11,
      colW: [4.0, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81],
      border: { pt: 1, color: 'FFFFFF' }, valign: 'middle',
    });
  }

  // s20 Before/After 표
  {
    const { slide: s, placeholders: p } = await slide(pptx, 's20.html');
    const bf = (t) => cell(t, { color: '8B9197' });
    const af = (t) => cell(t, { fontFace: FS, color: GREEN });
    s.addTable([
      [hdr('관점'), hdr('Before (2026 현재)'), hdr('After (2029 목표)')],
      [area('외적 정합성'), bf('차별화 전략 vs 원가우위형 HR — 부정합'), af('전략-HR 정렬: 장기·개발·참여형 HR로 전환')],
      [area('내적 정합성'), bf('제도 단절 — 구성원 48% 평가·보상 무관'), af('역량모델 기반 채용-평가-보상-육성-승진의 일관 번들')],
      [area('VRIO'), bf('V·R 보유, O 결핍 → 일시적 우위'), af('O 확보 → 지속적 경쟁우위 (Sustained Advantage)')],
      [area('평가·보상'), bf('복잡한 산식 · 형식적 연결 · 약한 차등'), af('단순한 상시 성과관리(성장용) + 강력한 성과 보상(별도 결정)')],
      [area('인재'), bf('근속 2.5년 · 연 10~20명 퇴사 · 회전문 채용'), af('근속 4년+ · 이직률 한 자릿수 · 인재밀도가 인재를 부르는 선순환')],
      [area('재무'), bf('인당 매출 0.98억 · 영업이익률 2.6%'), af('인당 매출 1.2억 · 영업이익률 8%')],
      [area('구성원 경험'), bf('"갈려나간다" (잡플래닛 3.0)'), af('"일 잘하는 동료들과 성장한다" (3.5+)')],
    ], {
      x: p[0].x, y: p[0].y, w: p[0].w, h: p[0].h, rowH: p[0].h / 8,
      colW: [1.45, 4.3, 4.72],
      border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
    });
  }

  const out = path.join(DIR, '..', '..', '인적자원관리_기말과제_시앤피컨설팅_이석주.pptx');
  await pptx.writeFile({ fileName: out });
  console.log('saved:', out);
}
main().catch(err => { console.error(err); process.exit(1); });
