# VRIN AI Hub — 43 에이전트 캐릭터 일러스트 프롬프트

> 시앤피컨설팅 대표(이석주)의 AI 컨설팅 회사 "VRIN AI Hub" 전속 AI 에이전트 43명의
> 캐릭터 일러스트 생성용 영문 프롬프트 모음. Midjourney / Google Antigravity / Gemini용.
> **저장 규칙**: 각 에이전트 이미지를 `public/avatars/<name>.png` 로 저장하면 대시보드가 자동 인식.

---

## 공통 아트 디렉션 (Shared Art Direction — 43장 전부 동일 적용)

모든 프롬프트는 아래 베이스 스타일을 전제로 작성되었습니다. AI 생성기에서 **시리즈 일관성**을 유지하려면
가능하면 같은 세션/같은 시드(`--seed`)를 사용하고, 아래 공통 토큰을 항상 포함하세요.

**Base style block (영문, 모든 프롬프트에 공통으로 녹아 있음):**

```
modern flat corporate mascot character, clean vector illustration, soft gradients,
semi-3D rounded shapes with subtle depth, friendly professional expression,
centered bust / upper-body portrait, facing forward, simple solid-color background
tinted to the agent's brand color, consistent line weight and soft studio lighting,
cohesive "dream team of specialists" series look, trustworthy competent approachable,
square 1:1 composition, transparent-friendly, no text, no letters, no logos, no watermark
```

**테크니컬 파라미터 규칙**
- Midjourney: 각 프롬프트 끝에 `--ar 1:1 --style raw` 부착. 시리즈 통일을 원하면 동일 `--seed 12345` 추가 권장.
- Gemini / Antigravity: 한 줄 자연어 영문 버전을 별도 제공. 배경색은 브랜드 컬러로 지정.

**브랜드 컬러 레퍼런스**
- 거버넌스: cos=slate gray, bar=red, clo=violet
- 전략기획부(STR)=deep blue · HR컨설팅부(HR)=teal/green · 리서치부(RES)=amber/orange
- 제품기술부(PT)=indigo/cyan · 그로스부(GTM)=magenta/pink · 딜리버리부(DEL)=purple
- 법무리스크부(LEG)=navy/bronze

---

# 거버넌스 (Governance) — 3명

### cos — 비서실장 / PMO 관제탑
- **파일명(저장 위치)**: `public/avatars/cos.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a calm composed chief-of-staff figure in a crisp slate-gray suit, headset and a floating holographic mission-control dashboard with orbiting task nodes behind one shoulder, conductor-like guiding gesture, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid slate-gray tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a calm chief-of-staff with a headset, standing before a floating mission-control dashboard of glowing task nodes, slate-gray suit, centered bust portrait on a solid slate-gray background, clean soft-gradient style, no text.

### bar — 품질검증관 (Bar Raiser)
- **파일명(저장 위치)**: `public/avatars/bar.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a sharp discerning quality-gatekeeper figure holding a glowing checklist and a raised quality bar / standard ruler, confident critical-but-fair expression, subtle red checkmark and shield motif, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid red tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a sharp quality inspector raising a glowing standard-bar and holding a checklist with a red checkmark shield, confident fair expression, centered bust portrait on a solid red background, clean soft-gradient style, no text.

### clo — 학습진화실장 (Chief Learning Officer)
- **파일명(저장 위치)**: `public/avatars/clo.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a wise mentor-scholar figure with a glowing growth-spiral and rising knowledge particles, an open book morphing into a sprouting plant, reflective evolving expression, violet aura, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid violet tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a wise learning officer with a glowing upward growth-spiral and an open book sprouting a small plant, reflective expression, centered bust portrait on a solid violet background, clean soft-gradient style, no text.

---

# 전략기획부 (Strategy — STR) — 4명 · 브랜드 컬러 deep blue

### str — 전략기획부장
- **파일명(저장 위치)**: `public/avatars/str.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a senior strategy department head, distinguished confident leader in a deep-blue blazer, standing before a large floating chessboard and a rising strategic roadmap arrow, commanding visionary expression, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered upper-body portrait facing forward, solid deep-blue tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a senior strategy chief in a deep-blue blazer standing before a floating chessboard and a rising roadmap arrow, visionary confident expression, centered upper-body portrait on a solid deep-blue background, clean soft-gradient style, no text.

### str-strategy — 사업전략가
- **파일명(저장 위치)**: `public/avatars/str-strategy.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a business strategist analyst holding a glowing SWOT / 2x2 matrix and a chess knight piece, focused analytical expression, deep-blue accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid deep-blue tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a business strategist holding a glowing 2x2 matrix and a chess knight, focused analytical expression, centered bust portrait on a solid deep-blue background, clean soft-gradient style, no text.

### str-finance — 재무모델러
- **파일명(저장 위치)**: `public/avatars/str-finance.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a financial modeler holding a glowing spreadsheet grid and a rising bar-and-line chart with coins and a calculator floating nearby, precise numerate expression, deep-blue and gold accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid deep-blue tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a financial modeler with a glowing spreadsheet grid, rising charts, coins and a calculator, precise expression, centered bust portrait on a solid deep-blue background with gold accents, clean soft-gradient style, no text.

### str-newbiz — 신사업기획가
- **파일명(저장 위치)**: `public/avatars/str-newbiz.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a new-business venture planner holding a glowing lightbulb launching like a rocket, fresh entrepreneurial energetic expression, floating idea-bubbles and a small launchpad, deep-blue with bright cyan spark accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid deep-blue tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a new-business planner holding a glowing lightbulb-rocket with floating idea bubbles, energetic entrepreneurial expression, centered bust portrait on a solid deep-blue background, clean soft-gradient style, no text.

---

# HR컨설팅부 (HR Consulting — HR) — 9명 · 브랜드 컬러 teal/green

### hr — HR컨설팅부장
- **파일명(저장 위치)**: `public/avatars/hr.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a senior HR consulting department head, warm authoritative leader in a teal blazer, standing before a glowing org-chart tree of connected people-nodes, caring yet decisive expression, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered upper-body portrait facing forward, solid teal tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a senior HR chief in a teal blazer before a glowing org-chart tree of people-nodes, warm decisive expression, centered upper-body portrait on a solid teal background, clean soft-gradient style, no text.

### hr-skills — 스킬 / 직무분석가
- **파일명(저장 위치)**: `public/avatars/hr-skills.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a job-and-skills analyst examining a glowing competency map made of interlocking skill-block icons and a magnifier over a role profile, methodical curious expression, teal-green accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a job-and-skills analyst with a glowing skill-block competency map and a magnifier over a role profile, methodical expression, centered bust portrait on a solid teal-green background, clean soft-gradient style, no text.

### hr-disability — 장애인고용전담
- **파일명(저장 위치)**: `public/avatars/hr-disability.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, an inclusive employment specialist with a glowing universal-accessibility motif (the round person-in-circle access symbol) and diverse abstract people-icons of different abilities held together, kind welcoming inclusive expression, teal-green with warm accent, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of an inclusive-employment specialist with a glowing universal-accessibility symbol and diverse people-icons of different abilities, kind welcoming expression, centered bust portrait on a solid teal-green background, clean soft-gradient style, no text.

### hr-culture — 조직문화 / 변화관리
- **파일명(저장 위치)**: `public/avatars/hr-culture.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, an organizational-culture and change-management facilitator holding a glowing compass and connected speech-bubble people forming a heart-shaped culture circle, empathetic motivating expression, teal-green accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a change-management facilitator holding a glowing compass with connected people forming a culture circle, empathetic motivating expression, centered bust portrait on a solid teal-green background, clean soft-gradient style, no text.

### hr-org — 조직설계
- **파일명(저장 위치)**: `public/avatars/hr-org.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, an organizational-design architect arranging floating modular org-structure blocks and a clean hierarchical org-chart blueprint, structured systematic expression, teal-green and blueprint-line accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of an org-design architect arranging floating modular structure blocks and a hierarchical org-chart blueprint, systematic expression, centered bust portrait on a solid teal-green background, clean soft-gradient style, no text.

### hr-perf — 성과보상
- **파일명(저장 위치)**: `public/avatars/hr-perf.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a performance-and-rewards specialist holding a glowing target with arrow in bullseye next to a coin-and-medal reward icon and a KPI gauge, fair motivating expression, teal-green with gold accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a performance-and-rewards specialist with a glowing bullseye target, a reward medal and a KPI gauge, fair motivating expression, centered bust portrait on a solid teal-green background with gold accents, clean soft-gradient style, no text.

### hr-learn — 역량개발 / 러닝
- **파일명(저장 위치)**: `public/avatars/hr-learn.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a learning-and-development coach holding a glowing open book and a graduation cap with rising skill-up arrows and play-button micro-lesson icons, encouraging mentor expression, teal-green accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a learning-and-development coach with a glowing open book, a graduation cap and rising skill-up arrows, encouraging expression, centered bust portrait on a solid teal-green background, clean soft-gradient style, no text.

### hr-analytics — 피플애널리틱스
- **파일명(저장 위치)**: `public/avatars/hr-analytics.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a people-analytics data scientist with glowing dashboards combining people-icons and scatter-plot data points, holding a tablet of HR metrics, insightful analytical expression, teal-green with data-cyan accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a people-analytics scientist with glowing dashboards merging people-icons and data points, holding an HR-metrics tablet, insightful expression, centered bust portrait on a solid teal-green background, clean soft-gradient style, no text.

### hr-aix — HR AI / AX전문가
- **파일명(저장 위치)**: `public/avatars/hr-aix.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, an HR-AI transformation specialist where a glowing neural-network brain merges with a people-network of HR-icons, sleek innovative expression, holding a small AI assistant orb, teal-green with electric-cyan AI accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid teal-green tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of an HR-AI/AX specialist with a glowing neural brain merging into an HR people-network and a small AI orb, innovative expression, centered bust portrait on a solid teal-green background with cyan accents, clean soft-gradient style, no text.

---

# 리서치부 (Research — RES) — 5명 · 브랜드 컬러 amber/orange

### res — 리서치부장
- **파일명(저장 위치)**: `public/avatars/res.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a senior research department head, sharp curious leader in an amber-toned blazer, standing before a constellation of connected source-documents and a large magnifier, knowing investigative expression, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered upper-body portrait facing forward, solid amber tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a senior research chief in an amber blazer before a constellation of connected documents and a large magnifier, investigative expression, centered upper-body portrait on a solid amber background, clean soft-gradient style, no text.

### res-web — 웹리서처 / 딥리서치
- **파일명(저장 위치)**: `public/avatars/res-web.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a deep-web researcher diving through a glowing globe-and-browser-window web of hyperlinks, holding a magnifier scanning floating search results, focused exploratory expression, amber-orange accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid amber-orange tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a deep-web researcher exploring a glowing globe-and-browser web of links with a magnifier over floating search results, focused expression, centered bust portrait on a solid amber-orange background, clean soft-gradient style, no text.

### res-market — 경쟁분석가
- **파일명(저장 위치)**: `public/avatars/res-market.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a competitive-market analyst studying a glowing market-landscape radar chart with competitor pins and a positioning quadrant, strategic perceptive expression, amber-orange accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid amber-orange tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a competitive-market analyst studying a glowing radar chart with competitor pins and a positioning quadrant, perceptive expression, centered bust portrait on a solid amber-orange background, clean soft-gradient style, no text.

### res-data — 데이터분석가
- **파일명(저장 위치)**: `public/avatars/res-data.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a data analyst surrounded by glowing charts, a pie chart, a trend line and floating data-point clusters, holding a tablet with a clean graph, sharp logical expression, amber-orange with data accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid amber-orange tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a data analyst surrounded by glowing pie charts, trend lines and data clusters, holding a graph tablet, logical expression, centered bust portrait on a solid amber-orange background, clean soft-gradient style, no text.

### res-wiki — 위키사서
- **파일명(저장 위치)**: `public/avatars/res-wiki.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a knowledge librarian curating a glowing wall of interconnected wiki-cards and tagged knowledge folders, holding an organized index, calm orderly helpful expression, amber-orange accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid amber-orange tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a knowledge librarian curating a glowing wall of interconnected wiki-cards and tagged folders with an index, calm orderly expression, centered bust portrait on a solid amber-orange background, clean soft-gradient style, no text.

---

# 제품기술부 (Product & Technology — PT) — 9명 · 브랜드 컬러 indigo/cyan

### pt — 제품기술부장 (CPO/CTO)
- **파일명(저장 위치)**: `public/avatars/pt.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a senior CPO/CTO product-and-tech department head, visionary leader in an indigo tech-jacket, standing before a glowing product-architecture hologram blending a UI screen and a circuit-network, decisive builder expression, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered upper-body portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a senior CPO/CTO in an indigo tech-jacket before a glowing product-architecture hologram blending a UI screen and a circuit network, visionary expression, centered upper-body portrait on a solid indigo background, clean soft-gradient style, no text.

### pt-pm — 제품기획 PM
- **파일명(저장 위치)**: `public/avatars/pt-pm.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a product manager holding a glowing roadmap timeline with sticky-note kanban cards and a user-story flow, organized collaborative expression, indigo-cyan accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a product manager holding a glowing roadmap timeline with kanban sticky-cards and a user-story flow, organized collaborative expression, centered bust portrait on a solid indigo background, clean soft-gradient style, no text.

### pt-ai — AI엔지니어
- **파일명(저장 위치)**: `public/avatars/pt-ai.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, an AI engineer with a glowing neural-network brain and floating model nodes and tensor cubes, holding a small chip, brilliant focused expression, indigo with electric-cyan neural accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of an AI engineer with a glowing neural-network brain, floating model nodes and a chip, brilliant focused expression, centered bust portrait on a solid indigo background with cyan accents, clean soft-gradient style, no text.

### pt-be — 백엔드 엔지니어
- **파일명(저장 위치)**: `public/avatars/pt-be.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a backend engineer with floating server-stack racks, a database cylinder and API connector pipes, holding a gear, reliable methodical expression, indigo with cyan accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a backend engineer with floating server racks, a database cylinder and API pipes, holding a gear, reliable methodical expression, centered bust portrait on a solid indigo background, clean soft-gradient style, no text.

### pt-fe — 프론트엔드 엔지니어
- **파일명(저장 위치)**: `public/avatars/pt-fe.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a frontend engineer arranging glowing UI component blocks and a responsive browser window with buttons and layout grids, creative precise expression, indigo-cyan accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a frontend engineer arranging glowing UI component blocks and a responsive browser window with buttons and grids, creative precise expression, centered bust portrait on a solid indigo background, clean soft-gradient style, no text.

### pt-mobile — 모바일 엔지니어
- **파일명(저장 위치)**: `public/avatars/pt-mobile.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a mobile engineer holding a glowing smartphone with floating app screens and touch-gesture ripples, agile friendly expression, indigo-cyan accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a mobile engineer holding a glowing smartphone with floating app screens and touch-gesture ripples, agile expression, centered bust portrait on a solid indigo background, clean soft-gradient style, no text.

### pt-devops — DevOps 엔지니어
- **파일명(저장 위치)**: `public/avatars/pt-devops.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a DevOps engineer with a glowing infinity CI/CD loop, floating container cubes, cloud and pipeline gears, calm reliable expression, indigo with cyan accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a DevOps engineer with a glowing infinity CI/CD loop, container cubes, cloud and pipeline gears, calm reliable expression, centered bust portrait on a solid indigo background, clean soft-gradient style, no text.

### pt-qa — QA 엔지니어
- **파일명(저장 위치)**: `public/avatars/pt-qa.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a QA engineer holding a glowing checklist with green checkmarks, a magnifier inspecting a bug icon caught in a net, meticulous vigilant expression, indigo-cyan accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a QA engineer with a glowing green-checkmark checklist and a magnifier inspecting a bug caught in a net, meticulous vigilant expression, centered bust portrait on a solid indigo background, clean soft-gradient style, no text.

### pt-game — 게임화 설계
- **파일명(저장 위치)**: `public/avatars/pt-game.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a gamification designer with floating game elements, achievement badges, a level-up progress bar, XP stars and a joystick, playful inventive expression, indigo-cyan with bright accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid indigo tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a gamification designer with floating achievement badges, a level-up progress bar, XP stars and a joystick, playful inventive expression, centered bust portrait on a solid indigo background, clean soft-gradient style, no text.

---

# 그로스부 (Growth — GTM) — 5명 · 브랜드 컬러 magenta/pink

### gtm — 그로스부장
- **파일명(저장 위치)**: `public/avatars/gtm.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a senior growth department head, charismatic energetic leader in a magenta blazer, standing before a glowing rising growth-funnel and a megaphone with upward arrows, bold persuasive expression, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered upper-body portrait facing forward, solid magenta tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a senior growth chief in a magenta blazer before a glowing rising growth-funnel and a megaphone with upward arrows, charismatic persuasive expression, centered upper-body portrait on a solid magenta background, clean soft-gradient style, no text.

### gtm-brand — 브랜드 / 카피
- **파일명(저장 위치)**: `public/avatars/gtm-brand.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a brand and copywriting creative holding a glowing quill-and-speech-bubble with a sparkle brand-mark gem and color-swatch palette, witty stylish expression, magenta-pink accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid magenta-pink tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a brand-and-copy creative holding a glowing quill-and-speech-bubble with a sparkling brand gem and color swatches, witty stylish expression, centered bust portrait on a solid magenta-pink background, clean soft-gradient style, no text.

### gtm-content — 콘텐츠
- **파일명(저장 위치)**: `public/avatars/gtm-content.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a content creator surrounded by floating media cards, a play-button video, an article card and social-post icons with engagement hearts, lively storytelling expression, magenta-pink accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid magenta-pink tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a content creator surrounded by floating media cards, a play-button video, an article card and social-post icons with hearts, lively storytelling expression, centered bust portrait on a solid magenta-pink background, clean soft-gradient style, no text.

### gtm-proposal — 제안서작성
- **파일명(저장 위치)**: `public/avatars/gtm-proposal.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a proposal writer presenting a glowing winning-proposal document with a checkmark seal, ribbon award and persuasive bullet-point cards, confident polished expression, magenta-pink accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid magenta-pink tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a proposal writer presenting a glowing winning-proposal document with a checkmark seal, award ribbon and bullet-point cards, confident polished expression, centered bust portrait on a solid magenta-pink background, clean soft-gradient style, no text.

### gtm-sales — B2B영업
- **파일명(저장 위치)**: `public/avatars/gtm-sales.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a B2B sales specialist with a confident handshake gesture, a glowing deal-pipeline funnel and a rising revenue arrow with a CRM card, persuasive trustworthy expression, magenta-pink accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid magenta-pink tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a B2B sales specialist with a handshake gesture, a glowing deal-pipeline funnel, a rising revenue arrow and a CRM card, persuasive trustworthy expression, centered bust portrait on a solid magenta-pink background, clean soft-gradient style, no text.

---

# 딜리버리부 (Delivery — DEL) — 4명 · 브랜드 컬러 purple

### del — 딜리버리부장 / 편집장
- **파일명(저장 위치)**: `public/avatars/del.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a senior delivery department head and editor-in-chief, refined leader in a purple blazer, standing before a glowing layout of polished report pages and a presentation deck, precise tasteful expression, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered upper-body portrait facing forward, solid purple tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a senior delivery chief and editor-in-chief in a purple blazer before a glowing layout of polished report pages and a presentation deck, refined tasteful expression, centered upper-body portrait on a solid purple background, clean soft-gradient style, no text.

### del-report — 보고서편집
- **파일명(저장 위치)**: `public/avatars/del-report.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a report editor holding a glowing well-structured document with neat headings, a red editing pen and tidy paragraph blocks, careful precise expression, purple accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid purple tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a report editor holding a glowing structured document with neat headings, a red editing pen and tidy paragraph blocks, careful precise expression, centered bust portrait on a solid purple background, clean soft-gradient style, no text.

### del-deck — 덱디자이너
- **파일명(저장 위치)**: `public/avatars/del-deck.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a presentation deck designer arranging glowing slide layouts with charts, hero slides and a slide-sorter strip, clean composed expression, purple accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid purple tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a presentation deck designer arranging glowing slide layouts with charts, hero slides and a slide-sorter strip, clean composed expression, centered bust portrait on a solid purple background, clean soft-gradient style, no text.

### del-visual — 비주얼아티스트
- **파일명(저장 위치)**: `public/avatars/del-visual.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a visual artist holding a glowing paintbrush and a color palette with floating shapes, gradient swatches and a vector-pen path, imaginative artistic expression, purple with vivid accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid purple tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a visual artist holding a glowing paintbrush and palette with floating shapes, gradient swatches and a vector-pen path, imaginative artistic expression, centered bust portrait on a solid purple background, clean soft-gradient style, no text.

---

# 법무리스크부 (Legal & Risk — LEG) — 4명 · 브랜드 컬러 navy/bronze

### leg — 법무리스크부장
- **파일명(저장 위치)**: `public/avatars/leg.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a senior legal-and-risk department head, dignified authoritative leader in a navy blazer, standing beside a glowing balanced scales of justice and a protective shield, principled composed expression, navy with bronze accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered upper-body portrait facing forward, solid navy tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a senior legal-and-risk chief in a navy blazer beside glowing balanced scales of justice and a protective shield, dignified principled expression, centered upper-body portrait on a solid navy background with bronze accents, clean soft-gradient style, no text.

### leg-contract — 계약검토
- **파일명(저장 위치)**: `public/avatars/leg-contract.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a contract-review specialist holding a glowing contract document with a signature line, a wax seal and a magnifier over clause cards, careful scrutinizing expression, navy with bronze accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid navy tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a contract-review specialist holding a glowing contract with a signature line, wax seal and a magnifier over clause cards, careful scrutinizing expression, centered bust portrait on a solid navy background with bronze accents, clean soft-gradient style, no text.

### leg-labor — 노무 / 노동법
- **파일명(저장 위치)**: `public/avatars/leg-labor.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a labor-law specialist holding a glowing law book with a balanced scale and worker-protection people-icons under a shield, fair protective expression, navy with bronze accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid navy tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a labor-law specialist holding a glowing law book with a balanced scale and worker-protection people-icons under a shield, fair protective expression, centered bust portrait on a solid navy background with bronze accents, clean soft-gradient style, no text.

### leg-compliance — 컴플라이언스
- **파일명(저장 위치)**: `public/avatars/leg-compliance.png`
- **Midjourney 프롬프트**: modern flat corporate mascot character, a compliance officer holding a glowing checklist with a green compliant-checkmark badge, a shield and a regulatory-rulebook with a gauge, vigilant principled expression, navy with bronze accents, clean vector illustration, soft gradients, semi-3D rounded shapes, friendly professional, centered bust portrait facing forward, solid navy tinted background, consistent line weight, soft studio lighting, trustworthy competent approachable, no text, no letters --ar 1:1 --style raw
- **Gemini/Antigravity 프롬프트**: A friendly semi-3D flat-vector corporate mascot of a compliance officer holding a glowing checklist with a green compliant-checkmark badge, a shield and a rulebook with a gauge, vigilant principled expression, centered bust portrait on a solid navy background with bronze accents, clean soft-gradient style, no text.

---

> **합계: 43명** — 거버넌스 3 · 전략기획부 4 · HR컨설팅부 9 · 리서치부 5 · 제품기술부 9 · 그로스부 5 · 딜리버리부 4 · 법무리스크부 4
