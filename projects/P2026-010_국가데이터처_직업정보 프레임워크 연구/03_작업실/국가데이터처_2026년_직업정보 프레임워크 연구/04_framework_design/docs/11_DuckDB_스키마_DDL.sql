-- ========================================================================
-- 직업정보 프레임워크 연구 (v1.4) — DuckDB 스키마 DDL
-- 단일 파일: 03_NLP_analysis/results/pipeline.duckdb
-- 작성: 2026-05-29 (v1.4 기준)
-- ========================================================================

-- 1) Job Family (KECO 중분류 단위, v1.4 권장)
CREATE TABLE IF NOT EXISTS job_family (
    job_family_id   VARCHAR PRIMARY KEY,
    name            VARCHAR NOT NULL,
    source          VARCHAR NOT NULL,          -- 'KECO_mid' / 'KSCO_mid'
    occupation_count INTEGER
);

-- 2) KSCO 직업 (8차, 495 세분류 + 1,270 세세분류)
CREATE TABLE IF NOT EXISTS ksco_occupation (
    ksco_code           VARCHAR PRIMARY KEY,   -- 4 or 5 자리
    name                VARCHAR NOT NULL,
    name_en             VARCHAR,
    code_length         INTEGER NOT NULL,      -- 4 (세분류) or 5 (세세분류)
    parent_code         VARCHAR,
    major_class         VARCHAR,                -- 대분류 1자리
    mid_class           VARCHAR,                -- 중분류 2자리
    job_family_id       VARCHAR REFERENCES job_family(job_family_id),
    definition_text     VARCHAR,                -- 세분류 정의 원문
    main_tasks_text     VARCHAR,                -- "주요 업무" 섹션 원문
    examples_text       VARCHAR,                -- 직업 예시
    has_main_tasks      BOOLEAN,                -- 주요업무 섹션 존재 여부 (L1 보강 트리거)
    v8_change_flag      VARCHAR                 -- 8차 분리신설/이동/명칭변경
);

-- 3) Task (Layer 0/1/2 통합, 본 연구 핵심 입력)
CREATE TABLE IF NOT EXISTS task (
    task_id             VARCHAR PRIMARY KEY,
    ksco_code           VARCHAR REFERENCES ksco_occupation(ksco_code),
    verb                VARCHAR NOT NULL,
    object              VARCHAR NOT NULL,
    full_statement      VARCHAR NOT NULL,
    source_sentence     VARCHAR,                -- 원문 문장
    layer               VARCHAR NOT NULL,       -- 'L0' / 'L1' / 'L2'
    source              VARCHAR NOT NULL,       -- 'KSCO_HS' / 'KJD_GROUP' / 'NCS'
    source_subject      VARCHAR,                -- 직업사전 원 직업명 (L1)
    primary_gwa_id      VARCHAR,                -- Step 3b GWA 1:1 할당 결과
    confidence          DOUBLE,
    extraction_runs     INTEGER,                -- self-consistency 횟수
    cross_consistency   DOUBLE                  -- 2회 일치율
);

-- 4) DWA (한국형, 목표 1,500–2,000)
CREATE TABLE IF NOT EXISTS dwa (
    dwa_id              VARCHAR PRIMARY KEY,
    label               VARCHAR NOT NULL,
    definition          VARCHAR,
    job_family_id       VARCHAR REFERENCES job_family(job_family_id),
    cluster_size        INTEGER,
    mean_cosine         DOUBLE,
    is_cross_family     BOOLEAN DEFAULT FALSE,  -- Step 4a Cross-Family
    legacy_match_ref    VARCHAR,                -- 워크피디아·KNOW·NCS legacy 매칭
    onet_match_id       VARCHAR,                -- ONET DWA 매칭 (참고)
    qc_passed           BOOLEAN,                -- QC 4기준 통과
    eight_rules_passed  BOOLEAN                  -- DWA Writing 8조항 통과
);

-- 5) IWA (한국형, 목표 250–330)
CREATE TABLE IF NOT EXISTS iwa (
    iwa_id              VARCHAR PRIMARY KEY,
    label               VARCHAR NOT NULL,
    definition          VARCHAR,
    onet_match_id       VARCHAR,                -- ONET IWA 332 매칭
    is_kr_unique        BOOLEAN DEFAULT FALSE,  -- 코사인 < 0.55 → 한국 신규
    cosine_to_onet      DOUBLE
);

-- 6) GWA (한국형, ONET 41 + 한국 신규 1–4)
CREATE TABLE IF NOT EXISTS gwa (
    gwa_id              VARCHAR PRIMARY KEY,
    label               VARCHAR NOT NULL,
    definition          VARCHAR,
    onet_match_id       VARCHAR,                -- ONET GWA 41 (1:1 권장)
    is_kr_unique        BOOLEAN DEFAULT FALSE
);

-- 7) 매핑 — Task → DWA (Multiple Linkage, ≤3)
CREATE TABLE IF NOT EXISTS task_to_dwa (
    task_id         VARCHAR REFERENCES task(task_id),
    dwa_id          VARCHAR REFERENCES dwa(dwa_id),
    link_order      INTEGER NOT NULL CHECK (link_order BETWEEN 1 AND 3),
    confidence      DOUBLE,
    PRIMARY KEY (task_id, link_order)
);

-- 8) 매핑 — DWA → IWA (1:N 허용)
CREATE TABLE IF NOT EXISTS dwa_to_iwa (
    dwa_id  VARCHAR REFERENCES dwa(dwa_id),
    iwa_id  VARCHAR REFERENCES iwa(iwa_id),
    PRIMARY KEY (dwa_id, iwa_id)
);

-- 9) 매핑 — IWA → GWA (1:N 허용)
CREATE TABLE IF NOT EXISTS iwa_to_gwa (
    iwa_id  VARCHAR REFERENCES iwa(iwa_id),
    gwa_id  VARCHAR REFERENCES gwa(gwa_id),
    PRIMARY KEY (iwa_id, gwa_id)
);

-- 10) Responsibility 3축 점수 (본 연구 차별화)
CREATE TABLE IF NOT EXISTS responsibility (
    ksco_code           VARCHAR PRIMARY KEY REFERENCES ksco_occupation(ksco_code),
    mgmt_score          INTEGER CHECK (mgmt_score BETWEEN 0 AND 3),
    supervisory_score   INTEGER CHECK (supervisory_score BETWEEN 0 AND 3),
    safety_score        INTEGER CHECK (safety_score BETWEEN 0 AND 3),
    total_score         INTEGER,                -- 합 0–9
    evidence_spans      JSON,                   -- 근거 스팬 JSON
    llm_consistency     DOUBLE,                 -- 2회 self-consistency
    flagged_for_review  BOOLEAN
);

-- 11) ISCO-28 SLF 4차원 슬롯
CREATE TABLE IF NOT EXISTS slf_4dim (
    ksco_code           VARCHAR PRIMARY KEY REFERENCES ksco_occupation(ksco_code),
    education_isced     INTEGER,                -- ISCED-11 1~8
    education_source    VARCHAR,                -- 'KSCO' / 'KECO' / '임금직업포털'
    responsibility_ref  VARCHAR,                -- responsibility 테이블 참조
    experience_years    DOUBLE,                 -- 직업사전 숙련기간
    wbl_type            VARCHAR,                -- '일학습병행' 등
    slf_decision        VARCHAR,                -- SL1~4 최종 판정 (best fit)
    decision_rationale  JSON
);

-- 12) Cross-Family DWA 분석 (직업 전환 가능성)
CREATE TABLE IF NOT EXISTS cross_family_link (
    dwa_id              VARCHAR REFERENCES dwa(dwa_id),
    job_family_from     VARCHAR REFERENCES job_family(job_family_id),
    job_family_to       VARCHAR REFERENCES job_family(job_family_id),
    shared_task_count   INTEGER,
    PRIMARY KEY (dwa_id, job_family_from, job_family_to)
);

-- 13) 전문가 검토 (CBM intervention 기록)
CREATE TABLE IF NOT EXISTS expert_review (
    review_id           VARCHAR PRIMARY KEY,
    target_type         VARCHAR NOT NULL,       -- 'task' / 'dwa' / 'iwa' / 'gwa' / 'resp'
    target_id           VARCHAR NOT NULL,
    decision            VARCHAR NOT NULL,       -- 'accept' / 'reject' / 'merge' / 'split' / 'edit'
    reviewer_id         VARCHAR NOT NULL,
    reviewer_role       VARCHAR,                -- 학계·고용정보원·통계청·산업계
    reviewed_at         TIMESTAMP,
    comment             VARCHAR,
    before_value        JSON,
    after_value         JSON
);

-- 14) Round-Robin QC 로그
CREATE TABLE IF NOT EXISTS qc_log (
    qc_id               VARCHAR PRIMARY KEY,
    target_type         VARCHAR NOT NULL,
    target_id           VARCHAR NOT NULL,
    round1_model        VARCHAR,
    round1_result       VARCHAR,
    round2_model        VARCHAR,
    round2_result       VARCHAR,
    final_status        VARCHAR,                -- pass / flagged / rejected
    flagged_reasons     JSON
);

-- 15) 동의어 사전 (정규화 1차)
CREATE TABLE IF NOT EXISTS lexicon (
    term                VARCHAR PRIMARY KEY,
    canonical           VARCHAR NOT NULL,
    source              VARCHAR,                -- 'KECO' / 'KJD' / 'manual'
    notes               VARCHAR
);

-- 16) 매핑 — KSCO 세분류 ↔ 한국직업사전 직업명 (N:1)
CREATE TABLE IF NOT EXISTS mapping_ksco_kjd (
    ksco_code       VARCHAR REFERENCES ksco_occupation(ksco_code),
    kjd_job_name    VARCHAR NOT NULL,
    PRIMARY KEY (ksco_code, kjd_job_name)
);

-- 17) 매핑 — KSCO 세분류 ↔ KECO 세분류 (1:1)
CREATE TABLE IF NOT EXISTS mapping_ksco_keco (
    ksco_code   VARCHAR REFERENCES ksco_occupation(ksco_code),
    keco_code   VARCHAR NOT NULL,
    PRIMARY KEY (ksco_code, keco_code)
);

-- 18) ONET 참조 (Step 4d 매핑용)
CREATE SCHEMA IF NOT EXISTS external_ref;

CREATE TABLE IF NOT EXISTS external_ref.onet_gwa (
    onet_gwa_id VARCHAR PRIMARY KEY,
    label       VARCHAR,
    description VARCHAR
);

CREATE TABLE IF NOT EXISTS external_ref.onet_iwa (
    onet_iwa_id VARCHAR PRIMARY KEY,
    label       VARCHAR,
    onet_gwa_id VARCHAR REFERENCES external_ref.onet_gwa(onet_gwa_id)
);

CREATE TABLE IF NOT EXISTS external_ref.onet_dwa (
    onet_dwa_id VARCHAR PRIMARY KEY,
    label       VARCHAR,
    onet_iwa_id VARCHAR REFERENCES external_ref.onet_iwa(onet_iwa_id)
);

-- 19) LLM 호출 캐시 (재현성 보장)
CREATE TABLE IF NOT EXISTS llm_call_log (
    call_id         VARCHAR PRIMARY KEY,
    model           VARCHAR NOT NULL,
    prompt_hash     VARCHAR NOT NULL,
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    temperature     DOUBLE,
    seed            INTEGER,
    called_at       TIMESTAMP,
    cached          BOOLEAN
);

-- ========================================================================
-- 인덱스 (성능)
-- ========================================================================
CREATE INDEX IF NOT EXISTS idx_task_ksco ON task(ksco_code);
CREATE INDEX IF NOT EXISTS idx_task_layer ON task(layer);
CREATE INDEX IF NOT EXISTS idx_task_gwa ON task(primary_gwa_id);
CREATE INDEX IF NOT EXISTS idx_dwa_family ON dwa(job_family_id);
CREATE INDEX IF NOT EXISTS idx_resp_score ON responsibility(total_score);

-- ========================================================================
-- 초기 view (직무기술 정의서 즉시 조회용)
-- ========================================================================
CREATE OR REPLACE VIEW job_definition_view AS
SELECT
    o.ksco_code,
    o.name AS ksco_name,
    o.definition_text,
    COUNT(DISTINCT t.task_id)               AS task_count,
    COUNT(DISTINCT td.dwa_id)               AS dwa_count,
    r.mgmt_score, r.supervisory_score, r.safety_score, r.total_score,
    s.slf_decision
FROM ksco_occupation o
LEFT JOIN task t              ON o.ksco_code = t.ksco_code
LEFT JOIN task_to_dwa td      ON t.task_id = td.task_id
LEFT JOIN responsibility r    ON o.ksco_code = r.ksco_code
LEFT JOIN slf_4dim s          ON o.ksco_code = s.ksco_code
GROUP BY o.ksco_code, o.name, o.definition_text,
         r.mgmt_score, r.supervisory_score, r.safety_score, r.total_score,
         s.slf_decision;

-- ========================================================================
-- END
-- ========================================================================
