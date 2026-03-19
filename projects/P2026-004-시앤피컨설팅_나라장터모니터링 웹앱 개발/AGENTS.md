# AGENTS.md — 나라장터 모니터링 v2.0

> oh-my-openagent 패턴 기반 에이전트팀 구성
> 시앤피컨설팅 | Next.js 16 + React 19 + Tailwind CSS 4 + Prisma (libsql) + Railway

---

## PROJECT CONTEXT

- **회사**: 시앤피컨설팅 (HR컨설팅) — 용역 분야 전문
- **서비스**: 나라장터 용역 입찰공고 모니터링 + 수주 분석 웹앱
- **사용자**: 관리자(대표) 1명 + 10개 본부별 계정
- **API**: 공공데이터포털 6종 모두 승인 완료
- **배포**: Railway (auto-deploy on main push)

---

## AGENT TEAM (6 에이전트)

### 🧠 Sisyphus (오케스트레이터)
- **역할**: 전체 Phase 조율, 작업 분배, 의존성 관리, 결과 검증
- **행동 원칙**:
  - Phase 순서 엄수 (1A → 1B → 1C → 2 → 3 → 4)
  - 독립적 작업은 반드시 병렬 위임 (Agent tool 동시 호출)
  - 위임 후 반드시 결과 검증 (빌드, 타입체크, 로직)
  - 같은 파일 동시 수정 방지 (파일 충돌 사전 차단)
- **위임 프롬프트 구조** (MANDATORY):
  ```
  1. TASK: 구체적 단일 목표
  2. EXPECTED OUTCOME: 완료 기준 + 산출물
  3. CONTEXT: 관련 파일 경로, 기존 패턴, 제약사항
  4. MUST DO: 필수 요구사항 (빠짐없이)
  5. MUST NOT DO: 금지 사항
  6. VERIFICATION: 검증 방법
  ```

### 🧹 Cleaner (코드 정리 전문가)
- **모드**: subagent (Phase 1A 전담)
- **역할**: 불필요 코드 제거, 의존성 정리, 스키마 정리
- **담당 파일**:
  - 삭제: `lib/notify.ts`, `app/api/notify/`, `app/api/subscribers/`, `app/api/settings/`, `app/(dashboard)/settings/`, `components/Subscriber*.tsx`
  - 수정: `lib/scheduler.ts`, `instrumentation.ts`, `prisma/schema.prisma`, `package.json`, `components/Sidebar.tsx`
- **행동 원칙**:
  - 삭제 전 import 의존성 역추적 필수
  - 한 영역씩 정리 (삭제 → 참조 제거 → 검증)
  - 삭제 후 `npx tsc --noEmit` 통과 확인
- **트리거**: 알림 기능 제거, 패키지 정리, 사전규격 용역 전용화

### 🔐 Guardian (인증/권한 전문가)
- **모드**: subagent (Phase 1B 주담당)
- **역할**: 관리자 시스템, 인증 강화, 접근 제어, 접속 로그
- **담당 파일**:
  - 수정: `middleware.ts`, `lib/auth.ts`, `prisma/schema.prisma`, `prisma/seed.ts`
  - 신규: `app/api/admin/users/route.ts`, AccessLog 모델
- **행동 원칙**:
  - role="admin"만 /admin/* 접근 허용
  - middleware에서 x-user-id, x-username 헤더 패턴 유지
  - 세션 쿠키 "narajan-session" 패턴 유지
  - 비밀번호는 sha256 해싱 (기존 패턴 유지)
  - 모든 인증 실패는 한글 에러 메시지
- **트리거**: 관리자 페이지, 사용자 관리, 접근 제어, 로그인 강화

### 🔧 Hephaestus (백엔드 딥워커)
- **모드**: subagent (Phase 1C, 2 주담당)
- **역할**: API 연동, DB 로직, 크롤링, 서버사이드 비즈니스 로직
- **담당 파일**:
  - 수정: `lib/narajan-api.ts`, `lib/scheduler.ts`, `types/narajan.ts`, `app/api/search/route.ts`, `app/api/dashboard/route.ts`, `app/api/keywords/route.ts`
  - 신규: 낙찰정보/계약정보 API 함수, BidResult/Company 모델
- **행동 원칙**:
  - 기존 `fetchWithRetry()`, `parseItems()` 패턴 100% 재활용
  - API 호출 간 200~300ms 간격 (rate limit)
  - 크롤링 청크 패턴 유지 (3일 단위)
  - UnifiedResult 타입 확장 (기존 호환 유지)
  - DB upsert 패턴 (bidNumber 기준 중복 방지)
- **API 연동 패턴**:
  ```typescript
  // 이 패턴을 반드시 따를 것
  const data = await fetchWithRetry<ApiResponse<T>>(
    `${BASE_URL}/ServiceName/endpointName`,
    { serviceKey: apiKey, type: "json", numOfRows: "100", pageNo: String(page), ...params }
  );
  const items = parseItems<T>(data?.response?.body?.items);
  ```
- **트리거**: API 연동, DB 스키마, 크롤링, 서버 로직

### 🎨 Athena (프론트엔드 구현자)
- **모드**: subagent (Phase 1B~3 UI 담당)
- **역할**: 페이지 UI, 컴포넌트, 레이아웃, 차트
- **담당 파일**:
  - 수정: `components/Sidebar.tsx`, `app/(dashboard)/page.tsx`, `app/(dashboard)/layout.tsx`
  - 신규: `app/(admin)/`, `app/(dashboard)/analytics/`, 차트 컴포넌트
- **행동 원칙**:
  - shadcn/ui 컴포넌트 우선 (Button, Card, Table, Dialog, Sheet, Tabs, Badge, Input, Select)
  - Tailwind CSS 4 유틸리티 클래스
  - "use client" 명시 + React hooks (useState, useCallback, useEffect)
  - lucide-react 아이콘
  - Recharts 차트 (PieChart, BarChart, LineChart, ResponsiveContainer)
  - 반응형: 모바일 Sheet 사이드바 패턴 유지
  - 에러/로딩 상태 일관성 (Skeleton, Loader2 아이콘)
  - toast 알림은 sonner 사용
- **UI 패턴 참고**: 기존 `app/(dashboard)/page.tsx`의 Card + Tabs + ResultTable 구조
- **트리거**: 페이지 UI, 컴포넌트, 차트, 레이아웃

### 📊 Oracle (분석/자문 전문가)
- **모드**: subagent (Phase 3 주담당, 읽기 전용 자문)
- **역할**: 수주 분석 로직 설계, 데이터 집계 쿼리, 분석 API
- **담당 파일**:
  - 신규: `app/api/analytics/**`, `lib/analytics.ts`
- **행동 원칙**:
  - Prisma `groupBy`, `aggregate`, `count` 활용
  - 날짜 범위 필터 필수 (최근 30일/90일/전체)
  - 응답은 Recharts 데이터 형식 (`[{name, value}]`)
  - 기업별/기관별/키워드별 3축 분석
  - 대량 데이터 처리 시 `take` 제한
- **분석 카테고리**:
  - 기업별 수주 현황: 기업명 → 수주 건수/금액/주요 기관
  - 기관별 발주 패턴: 기관명 → 발주 건수/평균 예산/주요 낙찰 기업
  - 키워드별 트렌드: 월별 공고/낙찰 건수 추이
  - 이용 현황: 사용자별 접속/검색 통계
- **트리거**: 분석 API, 데이터 집계, 통계 로직

---

## PHASE EXECUTION PLAN

### Phase 1A: 알림 제거 & 코드 정리
```
담당: 🧹 Cleaner (단독)
병렬: 불가 (의존성 체인)
산출물: 알림 관련 코드 전부 제거, 빌드 통과
검증: npx tsc --noEmit 통과
```

### Phase 1B: 관리자 시스템 + 인증
```
담당: 🔐 Guardian (API/미들웨어) + 🎨 Athena (UI)
병렬: 가능! (Guardian=API, Athena=UI 동시 작업)
  - Guardian: middleware.ts role 체크 + /api/admin/users CRUD + AccessLog 모델
  - Athena: /admin 페이지 UI + Sidebar role 분기
산출물: 관리자가 사용자 생성/관리 가능, role 기반 접근제어
검증: 관리자 로그인 → 사용자 생성 → 일반 사용자 로그인 → /admin 접근 차단
```

### Phase 1C: 본부별 키워드
```
담당: 🔧 Hephaestus (API) + 🎨 Athena (UI)
병렬: 가능!
  - Hephaestus: /api/keywords userId 필터 + /api/dashboard userId 필터
  - Athena: 키워드 페이지 (관리자=할당, 사용자=조회)
산출물: 본부별 키워드 격리, 관리자 키워드 할당
검증: 본부A 키워드 ≠ 본부B 키워드 확인
```

### Phase 2: 낙찰정보 & 계약정보
```
담당: 🔧 Hephaestus (API/DB) + 🎨 Athena (UI)
병렬: 가능! (선행: Hephaestus가 API+DB 먼저 → Athena UI)
  - Hephaestus: ScsbidInfoService 연동 + BidResult/Company 모델 + 크롤링
  - Athena: 개찰결과 탭 + 상세보기 낙찰자 표시
산출물: 개찰결과 검색/크롤링/표시 동작
검증: 키워드 검색 → 개찰결과 탭에 낙찰자/순위 표시
```

### Phase 3: 수주 분석 + 관리자 대시보드
```
담당: 📊 Oracle (분석 API) + 🎨 Athena (차트 UI)
병렬: 가능!
  - Oracle: /api/analytics/* 4개 엔드포인트
  - Athena: /analytics 페이지 + /admin/analytics 페이지 (Recharts)
산출물: 기업별/기관별/트렌드 분석, 이용현황 대시보드
검증: 차트 렌더링 + 데이터 정합성
```

### Phase 4: 최적화
```
담당: 🧹 Cleaner + 🔧 Hephaestus
병렬: 가능!
  - Cleaner: 사전규격 물품/공사/외자 엔드포인트 제거
  - Hephaestus: 크롤링 기간 확대 (7일→90일)
산출물: API 호출 75% 감소, 장기 데이터 축적
검증: 크롤링 동작 확인
```

---

## STRUCTURE

```
app/
├── (dashboard)/              # 일반 사용자
│   ├── page.tsx              # 대시보드 (모니터링 + 검색)
│   ├── analytics/page.tsx    # 🆕 수주 분석
│   ├── keywords/page.tsx     # 내 키워드
│   └── layout.tsx
├── (admin)/                  # 🆕 관리자 전용
│   └── admin/
│       ├── page.tsx          # 사용자 관리
│       ├── analytics/page.tsx # 이용 현황
│       └── layout.tsx
├── api/
│   ├── auth/                 # 인증 (login, logout, me)
│   ├── search/               # 통합 검색 (입찰+사전규격+발주+개찰)
│   ├── keywords/             # 키워드 CRUD (userId 필터)
│   ├── cron/                 # 크롤링 (외부 스케줄러)
│   ├── dashboard/            # 대시보드 데이터
│   ├── export/               # 엑셀 내보내기
│   ├── admin/                # 🆕 관리자 API
│   │   ├── users/route.ts
│   │   └── analytics/route.ts
│   └── analytics/            # 🆕 분석 API
│       ├── companies/route.ts
│       ├── agencies/route.ts
│       └── trends/route.ts
├── login/page.tsx
└── layout.tsx

lib/
├── narajan-api.ts            # 나라장터 API 연동 (6종)
├── scheduler.ts              # 크롤링 스케줄러 (알림 제거됨)
├── auth.ts                   # 인증 유틸리티
├── db.ts                     # Prisma 클라이언트
├── analytics.ts              # 🆕 분석 유틸리티
├── excel.ts                  # 엑셀 생성
├── rate-limit.ts             # Rate limit
├── utils.ts                  # 공통 유틸
└── validators.ts             # Zod 검증

components/
├── Sidebar.tsx               # 사이드바 (role 기반 메뉴)
├── ResultTable.tsx            # 결과 테이블
├── ResultDetailSheet.tsx      # 상세보기 시트
├── CrawlProgress.tsx          # 크롤링 진행률
├── ExportButton.tsx           # 엑셀 내보내기
├── DeleteConfirmDialog.tsx    # 삭제 확인
└── ui/                        # shadcn/ui 컴포넌트
```

---

## API REFERENCE (6종 승인 완료)

| API | Base URL | 용역 엔드포인트 |
|-----|----------|----------------|
| 입찰공고정보 | `.../1230000/ad/BidPublicInfoService` | `getBidPblancListInfoServc` |
| 사전규격정보 | `.../1230000/ao/HrcspSsstndrdInfoService` | `getPublicPrcureThngInfoServc` |
| 발주계획현황 | `.../1230000/ao/OrderPlanSttusService` | `getOrderPlanSttusListServcPPSSrch` |
| **낙찰정보** | `.../1230000/as/ScsbidInfoService` | `getOpengResultListInfoServc` (예상) |
| **계약정보** | `.../1230000/as/ContractInfoService` | `getContractListInfoServc` (예상) |
| **표준서비스** | `.../1230000/as/StndrdInfoService` | 통합 표준 데이터 |

---

## CONVENTIONS

### 코딩
- TypeScript strict (.ts/.tsx)
- 한글 주석 (`// 키워드 매칭 후 DB 저장`)
- 한글 에러 메시지 (사용자 노출용)
- `as any`, `@ts-ignore` 금지
- 빈 catch 블록 금지 (최소 `// 중복 무시` 주석)

### Git
- Phase별 커밋: `feat: Phase 1A - 알림 기능 제거`
- 빌드 깨지지 않는 단위로 커밋
- 에이전트 세션 중 `npm run build` 금지 (HMR 깨짐)

### 파일 명명
- kebab-case (route.ts, page.tsx)
- 컴포넌트: PascalCase (ResultTable.tsx)

### DB
- 마이그레이션: `npx tsx prisma/migrate.ts`
- seed: `npx tsx prisma/seed.ts`
- upsert 패턴으로 중복 방지

---

## ENV VARS

```
DATABASE_URL=        # libsql DB
NARAJAN_API_KEY=     # 공공데이터포털 API 키
AUTH_SECRET=         # 세션 서명
CRON_SECRET=         # 크롤링 보호
```

---

## ANTI-PATTERNS

- 알림 코드 재도입 금지 (nodemailer, @slack/web-api)
- 물품/공사/외자 데이터 수집 금지 (용역만!)
- `npm run build` 에이전트 세션 중 실행 금지
- 기존 API 패턴 무시하고 새 패턴 도입 금지
- 사용자 비밀번호 평문 저장 금지
- API 키 하드코딩 금지
