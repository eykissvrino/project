const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx.js');

const DIR = __dirname;
const TMP = process.env.TEMP || 'C:/Users/PC/AppData/Local/Temp';
const F = 'Malgun Gothic';
const NAVY = '16324F', BLUE = '2E74B5', RED = 'C0392B', GREEN = '1E8449', GRAYL = 'EEF2F7', GRAYB = 'D5DCE3', TXT = '2B2B2B';

async function main() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = '이석주';
  pptx.title = '시앤피컨설팅 HR시스템 진단 및 개선과제 — 디자인 샘플';

  // Slide 1: cover
  await html2pptx(path.join(DIR, 'slide1_cover.html'), pptx, { tmpDir: TMP });

  // Slide 2: fit table
  const { slide: s2, placeholders: p2 } = await html2pptx(path.join(DIR, 'slide2_table.html'), pptx, { tmpDir: TMP });
  const hdr = (t) => ({ text: t, options: { fill: { color: NAVY }, color: 'FFFFFF', bold: true, fontSize: 9.5 } });
  const ok = { text: '○', options: { color: GREEN, bold: true, align: 'center' } };
  const tri = { text: '△', options: { color: 'D9A441', bold: true, align: 'center' } };
  const bad = { text: '✗', options: { color: RED, bold: true, align: 'center' } };
  const cell = (t, opt = {}) => ({ text: t, options: { fontSize: 8.5, color: TXT, ...opt } });
  const area = (t) => cell(t, { bold: true, fill: { color: GRAYL } });
  const fitRows = [
    [hdr('HR 영역'), hdr('차별화 전략이 요구하는 관행'), hdr('시앤피 현행'), hdr('정합성')],
    [area('직무분석·설계'), cell('다양한 직무 · 복잡한 업무 · 일반적 직무기술'), cell('적은 직무 분류, 프로젝트별 유동적 업무'), tri],
    [area('채용·선발'), cell('집중적인 사회화 · 일반적 스킬 평가'), cell('수시·결원 채용 중심, 온보딩 체계 미흡'), tri],
    [area('훈련·개발'), cell('미래 직무스킬 · 그룹 지향 · 전 직원 훈련'), cell('방향은 부합하나 체계 없는 도제식 — 인당 교육비 연 69만 원'), tri],
    [area('성과관리'), cell('결과+장기 기준 · 개발적 목적 · 그룹 중심'), cell('본부별 자체 평가, 당해 영업익 중심(20~40%) · 역량 비중 10~20%'), bad],
    [area('보상'), cell('장기 인센티브 · 외적 형평성 · 그룹 인센티브'), cell('주임·선임(48%) 평가 무관 자동 인상 · 변동급 미미 · 페이밴드 비공개'), bad],
    [area('노사/직원관계'), cell('참여식 의사결정 · 직원=자산'), cell('하향식 의사결정 관행'), bad],
  ];
  s2.addTable(fitRows, {
    x: p2[0].x, y: p2[0].y, w: p2[0].w, h: p2[0].h,
    colW: [1.25, 3.05, 3.7, 1.0],
    border: { pt: 0.75, color: GRAYB }, valign: 'middle', fontFace: F, align: 'left',
  });

  // Slide 3: charts
  const { slide: s3, placeholders: p3 } = await html2pptx(path.join(DIR, 'slide3_chart.html'), pptx, { tmpDir: TMP });
  const years = ['2019', '2020', '2021', '2022', '2023', '2024', '2025'];
  const rev = p3.find(p => p.id === 'rev-chart');
  s3.addChart(pptx.charts.BAR, [{ name: '매출액', labels: years, values: [44.5, 59.9, 52.4, 77.6, 78.3, 85.9, 89.8] }], {
    ...rev, barDir: 'col', showLegend: false, showTitle: false,
    chartColors: [NAVY], dataLabelPosition: 'outEnd', showValue: true,
    dataLabelColor: '404040', dataLabelFontSize: 8, dataLabelFontFace: F,
    catAxisLabelFontSize: 8.5, catAxisLabelFontFace: F,
    valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMaxVal: 100,
    catAxisLineColor: GRAYB,
  });
  const mar = p3.find(p => p.id === 'margin-chart');
  s3.addChart(pptx.charts.LINE, [{ name: '영업이익률', labels: years, values: [18.1, 3.5, -3.1, 6.5, 4.2, 3.8, 2.6] }], {
    ...mar, lineSize: 2.5, showLegend: false, showTitle: false,
    chartColors: [RED], lineDataSymbol: 'circle', lineDataSymbolSize: 5,
    showValue: true, dataLabelPosition: 't', dataLabelColor: RED, dataLabelFontSize: 8, dataLabelFontFace: F,
    catAxisLabelFontSize: 8.5, catAxisLabelFontFace: F,
    valAxisHidden: true, valGridLine: { style: 'none' }, valAxisMinVal: -6, valAxisMaxVal: 22,
    catAxisLineColor: GRAYB,
  });

  // Slide 4: roadmap gantt
  const { slide: s4, placeholders: p4 } = await html2pptx(path.join(DIR, 'slide4_roadmap.html'), pptx, { tmpDir: TMP });
  const qh = (t) => ({ text: t, options: { fill: { color: NAVY }, color: 'FFFFFF', bold: true, fontSize: 8, align: 'center' } });
  const task = (t) => ({ text: t, options: { fontSize: 8, color: TXT, align: 'left' } });
  const e = { text: '', options: { fill: { color: BLUE } } };
  const i = { text: '', options: { fill: { color: NAVY } } };
  const v = { text: '', options: { fill: { color: GREEN } } };
  const g = { text: '', options: { fill: { color: '9AA5AF' } } };
  const o = { text: '', options: {} };
  const rows = [
    [qh('과제'), qh("'26 3Q"), qh('4Q'), qh("'27 1Q"), qh('2Q'), qh('3Q'), qh('4Q'), qh("'28"), qh("'29")],
    [task('C1 HR 전담 기능 신설 — "자사를 0호 고객사로"'), g, o, o, o, o, o, o, o],
    [task('C2 구성원 경험 진단 (eNPS·이직원인)'), g, g, o, o, o, o, o, o],
    [task('B1 컨설턴트 역량모델 (BEI·행동지표)'), e, e, o, o, o, o, o, o],
    [task('A1 평가 단순화·전사 표준화 (프로젝트 리뷰)'), o, i, i, o, o, o, o, o],
    [task('A2 상시 성과관리 OKR+CFR — 보상과 분리'), o, o, i, i, i, i, i, i],
    [task('B2 경력경로 CDP·전문가 트랙(Dual Ladder)'), o, o, e, e, o, o, o, o],
    [task('A3 보상 4P 재설계 (변동급·페이밴드 공개)'), o, o, o, i, i, i, i, o],
    [task('B3 CNP 컨설턴트 아카데미 (70:20:10)'), o, o, o, o, e, e, e, e],
    [task('A4·C5 총보상 체계 + 핵심인재 리텐션'), o, o, o, o, o, o, v, v],
  ];
  s4.addTable(rows, {
    x: p4[0].x, y: p4[0].y, w: p4[0].w, h: p4[0].h,
    colW: [3.35, 0.69, 0.69, 0.69, 0.69, 0.69, 0.69, 0.69, 0.69],
    border: { pt: 0.75, color: 'FFFFFF' }, valign: 'middle', fontFace: F,
    fill: { color: 'F5F7FA' },
  });

  await pptx.writeFile({ fileName: path.join(DIR, '디자인샘플_시앤피HR진단.pptx') });
  console.log('done');
}
main().catch(err => { console.error(err); process.exit(1); });
