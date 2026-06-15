#!/usr/bin/env python3
"""
Microsoft Case Study — Satya Nadella Growth Mindset
MBA 인적자원관리 발표 덱 v2 (23 slides)
케이스 원문(LBS128) + 히트 리프레시 + 조직설계 프레임 통합
"""

import sys, os
sys.path.insert(0, os.path.expanduser("C:/Users/eykis/.claude/plugins/mckinsey-pptx"))

from dataclasses import replace
from mckinsey_pptx import PresentationBuilder, DEFAULT_THEME
from mckinsey_pptx.theme import Typography

# Windows Korean theme
KO_THEME = replace(
    DEFAULT_THEME,
    typography=replace(DEFAULT_THEME.typography, family="Malgun Gothic"),
    copyright_text="ⓒ 2026 Konkuk MBA 32기 이석주",
)

b = PresentationBuilder(theme=KO_THEME, default_section_marker="MS Culture Transformation")

# ═══════════════════════════════════════════════════════════════
# Slide 1: Cover
# ═══════════════════════════════════════════════════════════════
b.add("cover_slide",
      title="Microsoft 문화 변혁 케이스 스터디",
      subtitle="Satya Nadella at Microsoft:\nInstilling a Growth Mindset (LBS128, 2018)\n\n인적자원관리(HRM) + 조직설계 프레임 통합 분석",
      client="건국대 MBA 32기 | 인적자원관리 (MBA9512)",
      date="2026. 5. 16. (토)")

# ═══════════════════════════════════════════════════════════════
# Slide 2: Agenda
# ═══════════════════════════════════════════════════════════════
b.add("agenda",
      title="Agenda",
      items=[
          "Executive Summary — 핵심 인사이트 4가지",
          "PART 1 — 케이스 배경: '잃어버린 10년'의 역설",
          "PART 2 — As-Is 진단: 7S 모델로 본 조직 병리",
          "PART 3 — 변화의 동인: Satya Nadella",
          "PART 4 — To-Be 재설계: Growth Mindset 조직",
          "PART 5 — 실행 메커니즘: Kotter 8단계 × Schein 3수준",
          "PART 6 — 성과, 미해결 과제, 시사점 & 토론",
      ])

# ═══════════════════════════════════════════════════════════════
# Slide 3: Core Thesis — Dark Navy Impact
# ═══════════════════════════════════════════════════════════════
b.add("dark_navy_summary",
      body='[Core Thesis]: Nadella는 전략이나 구조가 아니라 "인간 시스템(human system)"을 변혁의 출발점으로 삼았다.\n\n"CEO의 C는 Culture(문화)의 약자다.\nCEO는 조직 문화를 담당하는 큐레이터다."\n— Satya Nadella, 『히트 리프레시』 p.150',
      eyebrow="Microsoft Culture Transformation")

# ═══════════════════════════════════════════════════════════════
# Slide 4: Executive Summary — 4 Takeaways
# ═══════════════════════════════════════════════════════════════
b.add("executive_summary_takeaways",
      title="Executive Summary — 핵심 인사이트",
      sections=[
          {"takeaway": "① 성과관리 시스템은 '문화의 DNA'다",
           "bullets": [
               "Stack Ranking이 내부 경쟁·정치·위험회피 행동을 직접 설계했다",
               "폐지 후 상시 피드백으로 전환 → 협업 문화 복원의 필수 선행조건",
               "\"staffers were rewarded not just for doing well but for making sure their colleagues failed\" (케이스 p.2)",
           ]},
          {"takeaway": "② 문화 변혁 = '말 + 제도 + 행동 + 환경'의 동시 정합성",
           "bullets": [
               "새 미션(말) + Stack Ranking 폐지(제도) + CEO 솔선수범(행동) + 넛지(환경)",
               "7S 7요소를 'Cloud·Empowerment'라는 새 축으로 동시에 재정렬",
           ]},
          {"takeaway": "③ 변혁적 리더는 취약성(Vulnerability)으로 신뢰를 구축한다",
           "bullets": [
               "Grace Hopper 실수 공개 인정 → Hogan: \"나는 Satya에 대한 신뢰가 늘었다\"",
               "Tay 챗봇 사건 → 처벌이 아닌 \"Keep pushing, I am with you\"",
           ]},
          {"takeaway": "④ 최대 리스크: '새로운 언어, 오래된 행동'",
           "bullets": [
               "Missing Middle — 중간관리자의 변화 저항이 가장 큰 공백",
               "Growth Mindset이 남을 비판하는 새 도구로 전락할 위험",
           ]},
      ],
      final_conclusion="전략·구조·문화·제도의 정합성(Alignment)이 조직 효과성을 결정한다",
      source="LBS128 Case + 히트 리프레시 + McKinsey 7S / Kotter / Schein 프레임워크")

# ═══════════════════════════════════════════════════════════════
# Slide 5: Section — PART 1
# ═══════════════════════════════════════════════════════════════
b.add("section_divider",
      section_number="01",
      section_title="케이스 배경",
      subtitle="'잃어버린 10년'의 역설:\n재무는 멀쩡한데 시장은 불신했다")

# ═══════════════════════════════════════════════════════════════
# Slide 6: Big Number — Lost Decade Paradox
# ═══════════════════════════════════════════════════════════════
b.add("stat_hero",
      title="잃어버린 10년의 역설",
      stat="29%",
      stat_label="Steve Ballmer CEO 지지율 (Glassdoor, 2011)",
      context="같은 시기 Larry Page 94%, Mark Zuckerberg 99%.\n매출은 3배, 이익은 2배 성장했지만 주가는 10년간 정체.\n\"It was an enormously profitable company... it was just a question of whether they'd go into permanent decline.\" — Jan Dawson, 산업 분석가",
      source="LBS128 Case, p.2-3")

# ═══════════════════════════════════════════════════════════════
# Slide 7: Lost Decade Symptoms — KPI Dashboard
# ═══════════════════════════════════════════════════════════════
b.add("kpi_dashboard",
      title="잃어버린 10년: 5대 증상",
      kpis=[
          {"label": "핵심 인재 유출", "value": "가속",
           "delta": "2004년~", "delta_dir": "down",
           "context": "Google이 업계 평균 대비 +23% 보상 제공"},
          {"label": "시장 선점 상실", "value": "e-book·폰",
           "delta": "killed or delayed", "delta_dir": "down",
           "context": "bickering and power plays로 상실"},
          {"label": "제품 경쟁 패배", "value": "Bing·Zune",
           "delta": "vs Google·Apple", "delta_dir": "down",
           "context": "designing software by committee"},
          {"label": "리더십 신뢰 붕괴", "value": "29%→46%",
           "delta": "Ballmer 지지율", "delta_dir": "down",
           "context": "업계 최하위 수준"},
          {"label": "산업 트렌드 역행", "value": "PC 고착",
           "delta": "모바일 전환 실패", "delta_dir": "down",
           "context": "Windows를 안전담요처럼 고수"},
      ],
      columns=3,
      source="LBS128 Case / Vanity Fair (2012)")

# ═══════════════════════════════════════════════════════════════
# Slide 8: Quote — Nadella's Reflection
# ═══════════════════════════════════════════════════════════════
b.add("quote_slide",
      title="CEO의 진단",
      quote="관료주의가 혁신을 대체했고, 사내 정치가 팀워크를 대신했다. 우리는 낙오했다.\n\n무엇보다 슬픈 사실은 회사가 영혼을 잃었다고 생각하는 직원이 많다는 점이었다.",
      author="Satya Nadella",
      author_title="『히트 리프레시』 p.19, p.107")

# ═══════════════════════════════════════════════════════════════
# Slide 9: Section — PART 2
# ═══════════════════════════════════════════════════════════════
b.add("section_divider",
      section_number="02",
      section_title="As-Is 진단",
      subtitle="McKinsey 7S 모델로 본\nBallmer 시대의 조직 병리")

# ═══════════════════════════════════════════════════════════════
# Slide 10: 7S As-Is — Overview Areas (7 items)
# ═══════════════════════════════════════════════════════════════
b.add("overview_areas",
      title="McKinsey 7S 모델 — As-Is 진단: 7요소 부정합(Misalignment)",
      areas=[
          {"name": "Strategy",
           "bullets": ["Windows 방어 중심, PC 시대 성공공식 고착", "모바일·클라우드 전환 실패"]},
          {"name": "Structure",
           "bullets": ["제품별 사일로 — \"봉건 영주국의 연합\"", "부서들이 서로 총을 겨눔 (Exhibit 3)"]},
          {"name": "Systems",
           "bullets": ["Stack Ranking: 6개월 강제 서열화", "10명 중 1명 必 poor — 알고리즘 보상"]},
          {"name": "Style",
           "bullets": ["Precision Questioning: 아이디어 허점 찌르기", "위계·서열이 지배, 창의성 억압"]},
          {"name": "Staff",
           "bullets": ["\"정치 게임이 경력 개발의 핵심\"", "Google 등으로 핵심 인재 유출 가속"]},
          {"name": "Skills",
           "bullets": ["PC 소프트웨어 역량에 고착", "클라우드·오픈소스·모바일 역량 부재"]},
          {"name": "Shared Values",
           "bullets": ["Know-it-all: 가장 똑똑함을 증명하라", "내부 경쟁이 곧 성과라는 믿음"]},
      ],
      call_out="7요소가 'PC 시대의 방어'라는 잘못된 축으로 정렬 → 악순환",
      source="McKinsey 7S Framework / LBS128 Case")

# ═══════════════════════════════════════════════════════════════
# Slide 11: Stack Ranking — Issue Tree (Root Cause)
# ═══════════════════════════════════════════════════════════════
b.add("issue_tree",
      title="핵심 병리: Stack Ranking이 문화를 파괴한 메커니즘",
      root="Stack Ranking\n(강제 서열화)",
      main_drivers=[
          {"label": "협업 파괴\n(제로섬)",
           "secondaries": [
               {"label": "동료의 실패 = 나의 성공",
                "underlying": [
                    "\"rewarded for making sure colleagues failed\"",
                    "최고의 아이디어도 공유하면 불리",
                ]},
           ]},
          {"label": "정치의\n제도화",
           "secondaries": [
               {"label": "정치가 경력개발의 핵심",
                "underlying": [
                    "\"management by character assassination\"",
                    "\"kiss enough ass so they'll approve\"",
                ]},
           ]},
          {"label": "혁신 억압 +\n인재 유출",
           "secondaries": [
               {"label": "관료적 의사결정",
                "underlying": [
                    "\"designing software by committee\"",
                    "Google 등으로 핵심 인재 이탈 가속",
                ]},
           ]},
      ],
      source="LBS128 Case p.2 / Vanity Fair (2012)",
      footnote="HRM 핵심 명제: 성과관리 시스템은 단순 평가 도구가 아니라 '문화의 DNA'다")

# ═══════════════════════════════════════════════════════════════
# Slide 12: Section — PART 3
# ═══════════════════════════════════════════════════════════════
b.add("section_divider",
      section_number="03",
      section_title="변화의 동인",
      subtitle="Satya Nadella — 내부자의 외부 시선")

# ═══════════════════════════════════════════════════════════════
# Slide 13: Nadella Profile — Five Key Areas
# ═══════════════════════════════════════════════════════════════
b.add("five_key_areas",
      title="왜 Nadella인가 — 변혁을 이끈 5가지 자원",
      areas=[
          {"name": "22년 내부자",
           "description": "1992년 입사, Cloud & Enterprise EVP. 맥락을 깊이 이해하되 고착되지 않은 리더"},
          {"name": "학습 지향 경력",
           "description": "Bing 등 리스크 큰 보직 자발 수행 — \"거절하기 어려운 학습 기회\" (Case p.3)"},
          {"name": "공감(Empathy)의 체화",
           "description": "장남 Zain의 뇌성마비 → \"삶의 부침을 통해서만 공감 능력을 발전시킬 수 있다\" (p.28)"},
          {"name": "Growth Mindset",
           "description": "아내 Anu가 추천한 Carol Dweck 『Mindset』 → Microsoft 변혁의 이론적 기반"},
          {"name": "경청의 첫 1년",
           "description": "모든 레벨 수백 명 인터뷰 + 익명 포커스 그룹. \"Why does Microsoft exist?\""},
      ],
      source="LBS128 Case p.3-5 / 히트 리프레시 p.28-29, p.118")

# ═══════════════════════════════════════════════════════════════
# Slide 14: Quote — Listening
# ═══════════════════════════════════════════════════════════════
b.add("quote_slide",
      title="경청의 리더십",
      quote="경청은 내가 매일 실천한 가장 중요한 과제였다. 앞으로 몇 년간 내 리더십의 기초를 다질 요소였기 때문이다.\n\n직원들은 다시 선도(lead)하는 회사를 원했다. 따라가는 것이 아니라.",
      author="Satya Nadella",
      author_title="히트 리프레시 p.118 / LBS128 Case p.4-5")

# ═══════════════════════════════════════════════════════════════
# Slide 15: Section — PART 4
# ═══════════════════════════════════════════════════════════════
b.add("section_divider",
      section_number="04",
      section_title="To-Be 재설계",
      subtitle="Growth Mindset 조직으로의 전환:\nKnow-it-all → Learn-it-all")

# ═══════════════════════════════════════════════════════════════
# Slide 16: Fixed vs Growth — Comparison Table
# ═══════════════════════════════════════════════════════════════
b.add("comparison_table",
      title="Carol Dweck의 Mindset → Microsoft 조직 적용",
      subtitle="\"a fixed mindset will limit you and a growth mindset can move you forward\" (Case p.7)",
      options=["Fixed Mindset (As-Is)", "Growth Mindset (To-Be)"],
      criteria=[
          {"name": "핵심 신념",
           "scores": [0, 4],
           "notes": ["능력은 타고난 것, 고정적", "능력은 노력으로 성장 가능"]},
          {"name": "실패 대응",
           "scores": [0, 4],
           "notes": ["회피·은폐·남 탓", "학습 기회로 활용"]},
          {"name": "도전 태도",
           "scores": [1, 4],
           "notes": ["익숙한 것만 고수", "새로운 도전 추구"]},
          {"name": "타인의 성공",
           "scores": [0, 4],
           "notes": ["위협으로 인식 → 내부 경쟁", "영감의 원천 → 협업"]},
          {"name": "조직 문화",
           "scores": [0, 4],
           "notes": ["Know-it-all (증명하라)", "Learn-it-all (배워라)"]},
      ],
      recommended_index=1,
      source="Carol Dweck, Mindset (2006) / LBS128 Case p.6-7")

# ═══════════════════════════════════════════════════════════════
# Slide 17: New Mission + 3 Pillars
# ═══════════════════════════════════════════════════════════════
b.add("three_trends_table",
      title="새 미션 + Growth Mindset 3대 Pillar — \"To empower every person and every organisation on the planet to achieve more\"",
      trends=[
          {"name": "Customer\nObsession",
           "description": [
               "고객의 미충족·비명시적 니즈에 대한 호기심과 경청",
               "책상에서 일어나 현장으로 — 고객의 문제를 직접 체험",
           ],
           "examples": [
               "오스트리아 GM Ritz: 경찰서 1주일, 병원 2일 현장 관찰",
               "2015 임원 리트릿에서 고객 방문 의무화 → 전환점",
           ]},
          {"name": "Diversity &\nInclusion",
           "description": [
               "\"지구를 섬기려면 지구를 반영하라\"",
               "포용은 훈련이 아니라 시니어 리더의 행동 모델링",
           ],
           "examples": [
               "다양성 목표 수치화, 시니어 매니저 보너스에 연계",
               "10가지 포용 행동 리스트 배포 — 하나를 골라 토론",
           ]},
          {"name": "One\nMicrosoft",
           "description": [
               "\"봉건 영주국의 연합이 아닌 하나의 회사\"",
               "혁신과 경쟁은 사일로를 존중하지 않는다",
           ],
           "examples": [
               "OneWeek 해커톤: 부서 횡단 팀, 우수작 실제 프로젝트화",
               "SLT를 '나의 First Team'으로 인식하라",
           ]},
      ],
      source="LBS128 Case p.7-9 / 히트 리프레시 p.152",
      footnote="Culture Cabinet: Hogan CPO 주도, 180명 임원 → 17개 팀, Dweck 자문")

# ═══════════════════════════════════════════════════════════════
# Slide 18: Before/After — Stack Ranking → Continuous Feedback
# ═══════════════════════════════════════════════════════════════
b.add("two_column_compare",
      title="제도 재설계: Stack Ranking → 상시 피드백",
      left_label="As-Is: Stack Ranking",
      right_label="To-Be: Continuous Feedback",
      left_items=[
          "6개월마다 강제 서열화 (top ~ poor)",
          "강제 분포: 10명 중 1명 必 poor",
          "알고리즘이 등급 → 보상 자동 결정",
          "목적: 분류와 도태",
          "결과: 제로섬 경쟁, 협업 파괴",
      ],
      right_items=[
          "상시 피드백과 코칭 중심",
          "절대적 기여도 + 성장 가능성 평가",
          "매니저 재량 보상 예산 배분",
          "목적: 성장과 개발",
          "결과: 심리적 안전감, 협업 촉진",
      ],
      left_color="navy",
      right_color="blue",
      source="LBS128 Case p.8-9",
      footnote="\"We never believed one thing would change the company. It would be a lot of things, big and small\" — Nichols")

# ═══════════════════════════════════════════════════════════════
# Slide 19: CVF — Grouped Column Chart (문화 유형 전환)
# ═══════════════════════════════════════════════════════════════
b.add("grouped_column_chart",
      title="경쟁가치모형(CVF): 문화 유형 전환 — Cameron & Quinn 4유형 가중치 변화",
      categories=["Hierarchy\n(위계·통제)", "Market\n(경쟁·성과)", "Clan\n(협력·팀워크)", "Adhocracy\n(혁신·모험)"],
      series=[
          {"name": "Ballmer As-Is", "values": [85, 90, 20, 15]},
          {"name": "Nadella To-Be", "values": [30, 50, 80, 85]},
      ],
      source="Cameron & Quinn 경쟁가치모형 (CVF) / 분석자 매핑",
      footnote="Market 성과를 버린 게 아니라 Clan·Adhocracy 축을 보강해 균형 재편")

# ═══════════════════════════════════════════════════════════════
# Slide 20: Section — PART 5
# ═══════════════════════════════════════════════════════════════
b.add("section_divider",
      section_number="05",
      section_title="실행 메커니즘",
      subtitle="12.5만 명을 어떻게 움직였는가:\nKotter 변화관리 + Schein 문화 리더십")

# ═══════════════════════════════════════════════════════════════
# Slide 21: Kotter 8 Steps — Phases Table 4 (2 slides worth in 1)
# ═══════════════════════════════════════════════════════════════
b.add("phases_table_4",
      title="Kotter 변화관리 8단계 × Nadella 행보",
      phases=[
          {"name": "Phase 1\n위기감+연합",
           "description": "Kotter ①② 단계",
           "activities": [
               "① '잃어버린 10년' 직시 — Exhibit 3 조직도 공유",
               "② SLT 재구성: Nichols(비서실장), Hogan(CPO), Johnson(사업개발), DelBene(CSO)",
               "Culture Cabinet: 180명 임원 → 17개 팀",
           ],
           "outcomes": [
               "\"SLT를 나의 First Team으로 인식하라\"",
               "\"공통 세계관을 공유하는 응집력 있는 팀\"",
           ]},
          {"name": "Phase 2\n비전 수립·전파",
           "description": "Kotter ③④ 단계",
           "activities": [
               "③ 새 미션: \"To empower every person...to achieve more\"",
               "③ Growth Mindset 3 Pillar 정의",
               "④ 월간 CEO Top Learnings 영상",
               "④ 『히트 리프레시』 전 직원 배포 + 편지 동봉",
           ],
           "outcomes": [
               "Know-it-all → Learn-it-all 언어 확산",
               "\"Writing it was more for employees\" — Nichols",
           ]},
          {"name": "Phase 3\n장애제거·성과",
           "description": "Kotter ⑤⑥ 단계",
           "activities": [
               "⑤ Stack Ranking 폐지 → 상시 피드백",
               "⑤ 사일로 해체, 매니저 재량 보상",
               "⑥ Office on iOS 출시 — 즉각적 문화 시그널",
               "⑥ Linux 포용 — \"cancer\" → 파트너",
           ],
           "outcomes": [
               "\"행동이 말을 증명한다\" — 구체적 의사결정으로 비전 실현",
               "Windows 10 글로벌 론칭: 케냐 작은 마을에서 시작",
           ]},
          {"name": "Phase 4\n확산·정착",
           "description": "Kotter ⑦⑧ 단계",
           "activities": [
               "⑦ OneWeek 해커톤 정례화",
               "⑦ 고객 현장 방문 임원 의무화",
               "⑧ 넛지: 엘리베이터 '聽', 냅킨 '평생 학습자'",
               "⑧ 회의 마무리 리플렉션: Growth인가 Fixed인가?",
           ],
           "outcomes": [
               "\"존재의 방식\"으로 내재화",
               "\"변혁은 하나의 큰 조치가 아니라 수많은 것들이 강화\" — Nichols",
           ]},
      ],
      source="Kotter 8-Step Change Model (1996) / LBS128 Case p.4-10")

# ═══════════════════════════════════════════════════════════════
# Slide 22: Schein 3 Levels + Role Modeling
# ═══════════════════════════════════════════════════════════════
b.add("three_trends_table",
      title="Schein 문화 3수준 변혁 매핑 + CEO Role Modeling",
      trends=[
          {"name": "Artifacts\n(가시적 산물)",
           "description": [
               "As-Is: Stack Ranking 양식, 공격적 Precision Questioning 회의",
               "To-Be: 상시 피드백, OneWeek 해커톤, 넛지(聽·냅킨)",
           ],
           "examples": [
               "제도 + 물리적 환경 재설계",
               "\"We made big intentional changes that would grab people's attention\" — Hogan",
           ]},
          {"name": "Espoused Values\n(표방 가치)",
           "description": [
               "As-Is: \"가장 똑똑한 자가 이긴다\"",
               "To-Be: Growth Mindset 3 Pillar + 새 미션",
           ],
           "examples": [
               "Grace Hopper 사건: 실수를 공개 인정 → 자기 편향 탐구",
               "Tay 챗봇: \"Keep pushing, I am with you\" → 처벌 아닌 학습",
           ]},
          {"name": "Basic Assumptions\n(기본 가정)",
           "description": [
               "As-Is: 능력은 고정, 경쟁이 성과를 만듦",
               "To-Be: 누구나 성장 가능, 학습이 성과를 만듦",
           ],
           "examples": [
               "CEO Role Modeling — 취약성 공개가 가장 깊은 수준의 변혁 수단",
               "Hogan: \"신뢰가 줄지 않고 오히려 늘었다 — 누구도 비난하지 않았기에\"",
           ]},
      ],
      source="Edgar Schein, Organizational Culture & Leadership / LBS128 Case p.9-10",
      footnote="\"진정 훌륭한 리더의 가장 중요한 역할은 문화를 창조하고 관리하는 것\" — Schein")

# ═══════════════════════════════════════════════════════════════
# Slide 23: Section — PART 6
# ═══════════════════════════════════════════════════════════════
b.add("section_divider",
      section_number="06",
      section_title="성과·시사점·토론",
      subtitle="4년의 성과, 미해결 과제,\n그리고 우리에게 던지는 질문")

# ═══════════════════════════════════════════════════════════════
# Slide 24: 7S As-Is vs To-Be — Before/After 종합
# ═══════════════════════════════════════════════════════════════
b.add("overview_areas",
      title="7S 재정렬 종합: As-Is → To-Be",
      areas=[
          {"name": "Strategy",
           "bullets": ["Windows 방어 → Cloud-first, Mobile-first, AI"]},
          {"name": "Structure",
           "bullets": ["제품별 사일로 → One Microsoft (횡단 협업)"]},
          {"name": "Systems",
           "bullets": ["Stack Ranking → 상시 피드백, 매니저 재량 보상"]},
          {"name": "Style",
           "bullets": ["Precision Questioning → 경청·호기심·포용"]},
          {"name": "Staff",
           "bullets": ["정치적 생존자 → 다양성 + 학습 지향 인재"]},
          {"name": "Skills",
           "bullets": ["PC 소프트웨어 → Cloud·AI·파트너십"]},
          {"name": "Shared Values",
           "bullets": ["Know-it-all → Growth Mindset (Learn-it-all)"]},
      ],
      call_out="7요소를 'Cloud·Empowerment' 축으로 동시 재정렬",
      source="McKinsey 7S Framework / LBS128 Case 종합 분석")

# ═══════════════════════════════════════════════════════════════
# Slide 25: KPI Dashboard — 4-Year Results
# ═══════════════════════════════════════════════════════════════
b.add("kpi_dashboard",
      title="Nadella 4년차 성과 (2018 케이스 시점)",
      kpis=[
          {"label": "시가총액", "value": "$700B",
           "delta": "주가 사상 최고", "delta_dir": "up",
           "context": "10년 정체 → 급등"},
          {"label": "Azure 점유", "value": "95%+",
           "delta": "Fortune 500 사용", "delta_dir": "up",
           "context": "글로벌 50개 리전 발표"},
          {"label": "CEO 지지율", "value": "95%",
           "delta": "29% → 95%", "delta_dir": "up",
           "context": "Glassdoor 기준"},
          {"label": "인재 흐름", "value": "Top 5 AI",
           "delta": "유출 → 유입", "delta_dir": "up",
           "context": "최고 엔지니어 인재의 자석"},
          {"label": "외부 관계", "value": "Open",
           "delta": "Linux 포용", "delta_dir": "up",
           "context": "\"cancer\" → 파트너십"},
          {"label": "M&A", "value": "$26B",
           "delta": "LinkedIn 인수", "delta_dir": "up",
           "context": "5억 전문가 + Office 365 통합"},
      ],
      columns=3,
      source="LBS128 Case p.10-11")

# ═══════════════════════════════════════════════════════════════
# Slide 26: Missing Middle — Pros & Cons
# ═══════════════════════════════════════════════════════════════
b.add("pros_cons",
      title="미해결 과제: Missing Middle + Growth Mindset 오용 위험",
      pros_label="긍정적 성과",
      cons_label="미해결 과제",
      pros=[
          "직원들은 회사가 올바른 방향으로 가고 있다고 응답",
          "부서 간 협업이 늘었다는 인식 확산",
          "CEO 지지율 95%, 인재 유입 반전",
          "\"문화 쇄신을 위한 에너지는 우리 내부에 존재했다. 둑을 무너뜨려 변화가 흐르게 했다\" (p.162)",
      ],
      cons=[
          "Missing Middle: 중간관리자(VP/그룹 리더) 인재 이동·개발 지표 오히려 악화",
          "\"Employees and senior leaders were on board, but we had a missing link — middle management\" (Case p.11)",
          "Growth Mindset 오용: 한 매니저가 \"팀원 5명이 GM이 없다\"고 보고 → Nadella 일갈",
          "\"쓰레기통에서 보석을 찾아야 합니다\" — 새 언어가 오래된 정치 행동을 포장할 위험",
      ],
      source="LBS128 Case p.11 / 히트 리프레시 p.173-174")

# ═══════════════════════════════════════════════════════════════
# Slide 27: Discussion Topics — Five Key Areas
# ═══════════════════════════════════════════════════════════════
b.add("executive_summary_takeaways",
      title="토론 주제",
      sections=[
          {"takeaway": "Q1. 제도의 보편적 선악 vs 맥락 적합성",
           "bullets": [
               "Stack Ranking은 GE(Case #6)에서는 'A급 인재 육성 엔진'으로 작동",
               "같은 제도의 상반된 결과 — 제도 자체의 문제인가, 적용 맥락의 문제인가?",
           ]},
          {"takeaway": "Q2. Growth Mindset의 구호화(Lip-service) 위험",
           "bullets": [
               "좋은 문화 언어가 남을 비판하는 도구로 변질될 수 있다",
               "'말장난'으로 끝나지 않으려면 어떤 HRM 장치가 필요한가?",
           ]},
          {"takeaway": "Q3. CEO 카리스마 의존 변혁의 지속가능성",
           "bullets": [
               "12.5만 명 조직에서 리더 1인 모델링은 얼마나 확장 가능한가?",
               "Nadella 이후에도 문화가 유지될 수 있는가? 제도 vs 리더 개인?",
           ]},
          {"takeaway": "Q4. 한국 기업에의 적용",
           "bullets": [
               "한국 기업에 Growth Mindset을 이식한다면, 가장 먼저 바꿔야 할 HRM 제도는?",
               "위계적·통제 중심 문화에서 가장 큰 현실적 장벽은 무엇인가?",
           ]},
      ])

# ═══════════════════════════════════════════════════════════════
# Slide 28: Closing Quote
# ═══════════════════════════════════════════════════════════════
b.add("dark_navy_summary",
      body='[핵심 결론]: 전략·구조·문화·제도의 정합성(Alignment)이 조직 효과성을 결정한다.\n\nNadella는 미션(말) + 성과관리 개편(제도) + 솔선수범(행동) + 넛지(환경)를\n동시에 작동시켜 정합성을 확보했다.\n\n"문화는 아침 식사로 전략을 먹는다." — Peter Drucker\n(히트 리프레시 p.138)',
      eyebrow="Thank You")

# ═══════════════════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════════════════
output_dir = r"C:\Users\eykis\OneDrive\vrin_AI_hub\projects\P2026-009_MBA_Study\MBA_STUDY\인적자원관리_과제_MS 케이스스터디\output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "MS_CaseStudy_v2.pptx")
b.save(output_path)
print(f"Saved: {output_path}")
print("Done!")
