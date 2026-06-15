const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx.js');

const DIR = __dirname;
const TMP = process.env.TEMP || 'C:/Users/PC/AppData/Local/Temp';
const FB = 'Paperlogy 7 Bold', FS = 'Paperlogy 6 SemiBold', FR = 'Paperlogy 4 Regular';
const ORANGE = 'F08000', CHAR = '3A3F45', INK = '26282B', RED = 'C0392B', GREEN = '1E8449',
      TINT = 'FDF1E3', GRAYL = 'F7F8F9', GRAYB = 'DDE1E5', TXT = '3A3F45', GRAY = 'B8BFC6';

async function main() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: 'A4L', width: 842 / 72, height: 595.5 / 72 });
  pptx.layout = 'A4L';
  pptx.author = '이석주';
  pptx.title = '시앤피컨설팅 HR시스템 진단 및 개선과제 — 디자인 샘플 v2';

  // 1. cover
  await html2pptx(path.join(DIR, 'v2_slide1_cover.html'), pptx, { tmpDir: TMP });

  // 2. fit table
  const { slide: s2, placeholders: p2 } = await html2pptx(path.join(DIR, 'v2_slide2_table.html'), pptx, { tmpDir: TMP });
  const hdr = (t) => ({ text: t, options: { fill: { color: INK }, color: 'FFFFFF', bold: true, fontSize: 10.5, fontFace: FS } });
  const tri = { text: '△', options: { color: 'D9A441', bold: true, align: 'center', fontSize: 12 } };
  const bad = { text: '✗', options: { color: RED, bold: true, align: 'center', fontSize: 12 } };
  const cell = (t, opt = {}) => ({ text: t, options: { fontSize: 9.5, color: TXT, fontFace: FR, ...opt } });
  const area = (t) => cell(t, { fontFace: FS, fill: { color: TINT }, color: INK });
  s2.addTable([
    [hdr('HR 영역'), hdr('차별화 전략이 요구하는 관행'), hdr('시앤피 현행'), hdr('정합성')],
    [area('직무분석·설계'), cell('다양한 직무 · 복잡한 업무 · 일반적 직무기술'), cell('적은 직무 분류, 프로젝트별 유동적 업무'), tri],
    [area('채용·선발'), cell('집중적인 사회화 · 일반적 스킬 평가'), cell('수시·결원 채용 중심, 온보딩 체계 미흡'), tri],
    [area('훈련·개발'), cell('미래 직무스킬 · 그룹 지향 · 전 직원 훈련'), cell('방향은 부합하나 체계 없는 도제식 — 인당 교육비 연 69만 원'), tri],
    [area('성과관리'), cell('결과+장기 기준 · 개발적 목적 · 그룹 중심'), cell('본부별 자체 평가, 당해 영업익 중심(20~40%) · 역량 비중 10~20%'), bad],
    [area('보상'), cell('장기 인센티브 · 외적 형평성 · 그룹 인센티브'), cell('주임·선임(48%) 평가 무관 자동 인상 · 변동급 미미 · 페이밴드 비공개'), bad],
    [area('노사/직원관계'), cell('참여식 의사결정 · 직원=자산'), cell('하향식 의사결정 관행'), bad],
  ], {
    x: p2[0].x, y: p2[0].y, w: p2[0].w, h: p2[0].h,
    colW: [1.55, 3.5, 4.3, 1.12],
    border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
  });

  // 3. charts
  const { slide: s3, placeholders: p3 } = await html2pptx(path.join(DIR, 'v2_slide3_chart.html'), pptx, { tmpDir: TMP });
  const years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025'];
  s3.addChart(pptx.charts.BAR, [{ name: '매출액', labels: years, values: [44.5, 59.9, 52.4, 77.6, 78.3, 85.9, 89.8] }], {
    ...p3.find(p => p.id === 'rev-chart'),
    barDir: 'col', showLegend: false, showTitle: false,
    chartColors: [CHAR, CHAR, CHAR, CHAR, CHAR, CHAR, ORANGE], chartColorsOpacity: 100,
    showValue: true, dataLabelPosition: 'outEnd', dataLabelColor: '6B7178', dataLabelFontSize: 9, dataLabelFontFace: FR, dataLabelFormatCode: '0.0',
    catAxisLabelFontSize: 9.5, catAxisLabelFontFace: FR, catAxisLineColor: GRAYB,
    valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMaxVal: 100,
    barGapWidthPct: 40,
  });
  s3.addChart(pptx.charts.LINE, [{ name: '영업이익률', labels: years, values: [18.1, 3.5, -3.1, 6.5, 4.2, 3.8, 2.6] }], {
    ...p3.find(p => p.id === 'margin-chart'),
    lineSize: 2.5, showLegend: false, showTitle: false,
    chartColors: [RED], lineDataSymbol: 'circle', lineDataSymbolSize: 6,
    showValue: true, dataLabelPosition: 't', dataLabelColor: RED, dataLabelFontSize: 9, dataLabelFontFace: FR, dataLabelFormatCode: '0.0',
    catAxisLabelFontSize: 9.5, catAxisLabelFontFace: FR, catAxisLineColor: GRAYB,
    valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMinVal: -6, valAxisMaxVal: 22,
  });

  // 4. roadmap gantt
  const { slide: s4, placeholders: p4 } = await html2pptx(path.join(DIR, 'v2_slide4_roadmap.html'), pptx, { tmpDir: TMP });
  const qh = (t) => ({ text: t, options: { fill: { color: INK }, color: 'FFFFFF', bold: true, fontSize: 9, align: 'center', fontFace: FS } });
  const task = (t) => ({ text: t, options: { fontSize: 9.5, color: TXT, align: 'left', fontFace: FR } });
  const E = { text: '', options: { fill: { color: ORANGE } } };
  const I = { text: '', options: { fill: { color: CHAR } } };
  const V = { text: '', options: { fill: { color: GREEN } } };
  const G = { text: '', options: { fill: { color: GRAY } } };
  const o = { text: '', options: { fill: { color: 'FAFBFC' } } };
  s4.addTable([
    [qh('과제'), qh("'26 3Q"), qh('4Q'), qh("'27 1Q"), qh('2Q'), qh('3Q'), qh('4Q'), qh("'28"), qh("'29")],
    [task('C1 HR 전담 기능 신설 — "자사를 0호 고객사로"'), G, o, o, o, o, o, o, o],
    [task('C2 구성원 경험 진단 (eNPS·이직원인 분석)'), G, G, o, o, o, o, o, o],
    [task('B1 컨설턴트 역량모델 구축 (BEI·행동지표)'), E, E, o, o, o, o, o, o],
    [task('A1 평가 단순화·전사 표준화 (프로젝트 단위 리뷰)'), o, I, I, o, o, o, o, o],
    [task('A2 상시 성과관리 OKR+CFR — 보상과 분리 운영'), o, o, I, I, I, I, I, I],
    [task('B2 경력경로 CDP·전문가 트랙(Dual Ladder) 설계'), o, o, E, E, o, o, o, o],
    [task('A3 보상체계 4P 재설계 (변동급·페이밴드 공개)'), o, o, o, I, I, I, I, o],
    [task('B3 CNP 컨설턴트 아카데미 (70:20:10 체계화)'), o, o, o, o, E, E, E, E],
    [task('A4·C5 총보상 체계 + 핵심인재 리텐션 프로그램'), o, o, o, o, o, o, V, V],
  ], {
    x: p4[0].x, y: p4[0].y, w: p4[0].w, h: p4[0].h,
    colW: [4.0, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81],
    border: { pt: 1, color: 'FFFFFF' }, valign: 'middle',
  });

  // 5. short-term action plan detail
  const { slide: s5, placeholders: p5 } = await html2pptx(path.join(DIR, 'v2_slide5_action.html'), pptx, { tmpDir: TMP });
  const ah = (t) => ({ text: t, options: { fill: { color: INK }, color: 'FFFFFF', bold: true, fontSize: 9.5, align: 'center', fontFace: FS } });
  const ac = (t, opt = {}) => ({ text: t, options: { fontSize: 8.5, color: TXT, fontFace: FR, valign: 'middle', ...opt } });
  const aq = (t) => ac(t, { align: 'center', fontFace: FS, color: INK });
  const at = (t) => ac(t, { fontFace: FS, color: INK });
  const ko = (t) => ac(t, { color: 'A85A00' });
  s5.addTable([
    [ah('분기'), ah('과제'), ah('핵심 실행 내용'), ah('산출물'), ah('담당'), ah('성공지표 (KPI)')],
    [aq("'26\n3Q"), at('C1 HR 전담 신설'), ac('HR파트 지정(전담 1명+겸직 TF 4명), 사내 컨설팅 프로젝트로 공식 발족 — 킥오프 전사 공유(Kotter ①위기감·②연합체)'), ac('TF 발족문, 추진 로드맵'), ac('대표이사'), ko('TF 발족, 전사 설명회 1회')],
    [aq("'26\n3Q"), at('C2 구성원 경험 진단'), ac('전 직원 조직진단 서베이(자사 HR진단 솔루션), 최근 2년 퇴직자 이직원인 분석, 직위·본부별 보상 데이터 분석'), ac('진단 보고서, 이직원인 Top5'), ac('TF'), ko('응답률 80%+')],
    [aq("'26\n3~4Q"), at('B1 역량모델 구축'), ac('우수성과자 BEI 인터뷰(8~10명), 전문가 패널 워크숍 → 역량군-역량-행동지표 도출 → 타당성 검증'), ac('컨설턴트 역량모델 1식'), ac('TF+본부'), ko('행동지표 커버리지 100%')],
    [aq("'26\n4Q"), at('A1 평가 재설계'), ac('프로젝트 단위 간이 리뷰(5문항) + 연 1회 종합 리뷰(3단계) 설계, 구성원 의견수렴 2회, 평가자 교육'), ac('신평가제 운영안, 평가자 가이드'), ac('TF'), ko("'27.1Q 시행, 수용도 60%+")],
    [aq("'27\n1Q"), at('A2 상시 성과관리'), ac('분기 OKR 체크인+원온원(CFR) 도입 — 보상 산정과 분리 원칙 공표, 우수 본부 1on1 관행 전사 확산'), ac('OKR 가이드, 원온원 툴킷'), ac('본부장'), ko('분기 체크인 실시율 90%')],
    [aq("'27\n1~2Q"), at('B2 경력경로 공표'), ac('승진 기준(PL→PM→수주)을 행동지표로 구체화, 직위별 육성 로드맵 연결, 전문가 트랙(Dual Ladder) 설계'), ac('CDP 가이드북'), ac('TF'), ko('전 직위 커버, 설명회 1회')],
    [aq("'27\n2Q"), at('A3 보상 설계 착수'), ac('시장 임금 조사(외부 형평성)+직무·역량 가치 분석(내부 형평성) → Pay Band 재설계안, 변동급 시뮬레이션'), ac('보상 개편안 1식'), ac('TF+보상硏'), ko("'27.3Q 이사회 보고")],
  ], {
    x: p5[0].x, y: p5[0].y, w: p5[0].w, h: p5[0].h,
    colW: [0.62, 1.32, 4.0, 1.62, 0.85, 2.06],
    border: { pt: 0.75, color: GRAYB }, valign: 'middle', align: 'left',
  });

  await pptx.writeFile({ fileName: path.join(DIR, '디자인샘플_v2b_시앤피HR진단.pptx') });
  console.log('done');
}
main().catch(err => { console.error(err); process.exit(1); });
