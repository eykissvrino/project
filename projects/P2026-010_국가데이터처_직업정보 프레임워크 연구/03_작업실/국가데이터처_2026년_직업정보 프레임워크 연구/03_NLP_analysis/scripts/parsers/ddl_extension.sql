-- DDL 보강 (사양서 §10 + 설계서 D0/D1) — Sprint 1 Step 2
-- 적용: python parsers/apply_ddl_extension.py  (또는 kfw init 이후 1회)
-- idempotent: IF NOT EXISTS 로 반복 적용 안전.

-- ── 도구 인벤토리 (§1, §7, D1 도구 차원) ──────────────────────────────
CREATE TABLE IF NOT EXISTS tool_inventory (
    tool_id         VARCHAR PRIMARY KEY,
    ksco_code       VARCHAR REFERENCES ksco_occupation(ksco_code),  -- 세세분류 5자리
    name            VARCHAR NOT NULL,        -- 원문 도구명
    canonical_name  VARCHAR,                 -- 정규화 후 표준명(§7.2)
    category        VARCHAR,                 -- HW/SW/도구/장비/시스템
    evidence_span   VARCHAR,                 -- 근거 스팬(필수, D1)
    extraction_runs INTEGER,
    confidence      DOUBLE
);
CREATE INDEX IF NOT EXISTS idx_tool_ksco ON tool_inventory(ksco_code);
CREATE INDEX IF NOT EXISTS idx_tool_canonical ON tool_inventory(canonical_name);

-- ── 작업 환경 (§1, §7, D1 환경 차원) ──────────────────────────────────
CREATE TABLE IF NOT EXISTS work_context (
    context_id      VARCHAR PRIMARY KEY,
    ksco_code       VARCHAR REFERENCES ksco_occupation(ksco_code),  -- 세세분류 5자리
    category        VARCHAR NOT NULL,        -- 장소/위험/사회적/신체적/시간적
    value           VARCHAR NOT NULL,
    standardized    VARCHAR,                 -- §7.3 표준 카테고리
    evidence_span   VARCHAR,                 -- 근거 스팬(필수, D1)
    confidence      DOUBLE
);
CREATE INDEX IF NOT EXISTS idx_context_ksco ON work_context(ksco_code);
CREATE INDEX IF NOT EXISTS idx_context_cat ON work_context(category);

-- ── 한국 GWA 매핑 라벨 (§2.2) ─────────────────────────────────────────
ALTER TABLE gwa ADD COLUMN IF NOT EXISTS kr_label VARCHAR;
ALTER TABLE gwa ADD COLUMN IF NOT EXISTS kr_definition VARCHAR;

-- ── task: 부모 세분류 추적 (D0 세세분류 단위 + 상속) ──────────────────
ALTER TABLE task ADD COLUMN IF NOT EXISTS parent_code VARCHAR;  -- 부모 세분류 4자리
ALTER TABLE task ADD COLUMN IF NOT EXISTS low_signal BOOLEAN;   -- 정의 빈약(이름만) 플래그
