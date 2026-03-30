# 워크스페이스 관리 스킬

## 목적
workspace/ 폴더 전체를 체계적으로 관리하는 실행 도구.
프로젝트, 스킬, 에이전트, 산출물의 생성·정리·점검을 수행한다.

## 적용 조건
아래 키워드가 포함된 요청 시 자동 적용:
- "폴더 정리", "파일 정리", "워크스페이스 점검"
- "프로젝트 만들어", "프로젝트 생성", "아카이빙"
- "스킬 추가", "에이전트 추가", "리소스 동기화"
- "산출물 정리", "outputs 정리"
- "헬스체크", "상태 보여줘"

## 워크스페이스 경로
```
기본 경로: ~/workspace/
```

## 실행 명령어 모음

### 🔍 조회 명령어

**프로젝트 목록 확인**
```bash
echo "=== 활성 프로젝트 ===" && ls -1 workspace/projects/ 2>/dev/null
echo "=== 아카이브 ===" && ls -1 workspace/archive/ 2>/dev/null
```

**리소스 인벤토리**
```bash
echo "스킬:" && ls -1 workspace/_shared/skills/ 2>/dev/null
echo "에이전트:" && ls -1 workspace/_shared/agents/ 2>/dev/null
echo "워크플로우:" && ls -1 workspace/_shared/workflows/ 2>/dev/null
echo "커맨드:" && ls -1 workspace/_shared/commands/ 2>/dev/null
```

**디스크 사용량**
```bash
du -sh workspace/ workspace/projects/ workspace/archive/ workspace/outputs/ workspace/_shared/ 2>/dev/null
```

### 🛠️ 프로젝트 관리

**새 프로젝트 생성** (Windows: `new-project.cmd`, Linux: `new-project.sh`)
```bash
cd workspace && bash new-project.sh "프로젝트명"
```

**프로젝트 아카이빙**
```bash
mv workspace/projects/P20XX-XXX_이름 workspace/archive/
```

**아카이브에서 복원**
```bash
mv workspace/archive/P20XX-XXX_이름 workspace/projects/
```

### 📦 산출물 관리

**산출물 유형별 분류 구조**
```
workspace/outputs/
├── documents/        ← .docx, .pdf, .md
├── presentations/    ← .pptx
├── data-analysis/    ← .xlsx, .csv
├── web-apps/         ← .html, .jsx, 웹 프로젝트
├── mobile-apps/      ← 모바일 프로젝트
├── services/         ← SaaS, 서비스
└── design/           ← .png, .svg, 디자인
```

**산출물 동기화** (프로젝트 → 전역)
```bash
for proj in workspace/projects/P*/; do
  code=$(basename "$proj" | cut -d'_' -f1)
  [ -d "$proj/outputs" ] && [ "$(ls -A $proj/outputs 2>/dev/null)" ] && \
    mkdir -p "workspace/outputs/$code" && \
    cp -r "$proj/outputs/"* "workspace/outputs/$code/"
done
```

### 🔄 리소스 동기화

**_shared/ → 모든 활성 프로젝트 배포**
```bash
for proj in workspace/projects/P*/; do
  mkdir -p "$proj/.claude/skills" "$proj/.claude/agents" "$proj/.claude/commands"
  mkdir -p "$proj/.agent/skills" "$proj/.agent/workflows"
  cp -r workspace/_shared/skills/* "$proj/.claude/skills/" 2>/dev/null
  cp -r workspace/_shared/skills/* "$proj/.agent/skills/" 2>/dev/null
  cp workspace/_shared/agents/*.md "$proj/.claude/agents/" 2>/dev/null
  cp workspace/_shared/workflows/*.md "$proj/.agent/workflows/" 2>/dev/null
  cp workspace/_shared/commands/*.md "$proj/.claude/commands/" 2>/dev/null
  echo "✅ $(basename $proj) 동기화 완료"
done
```

### 🏥 헬스체크

**전체 워크스페이스 점검 + 자동 수정**
```bash
echo "=== 워크스페이스 헬스체크 ==="

# 프로젝트 구조 점검 및 자동 수정
for proj in workspace/projects/P*/; do
  name=$(basename "$proj")
  echo "--- $name ---"
  for dir in .claude .agent docs data outputs; do
    if [ ! -d "$proj/$dir" ]; then
      mkdir -p "$proj/$dir"
      echo "  🔧 $dir/ 생성됨"
    else
      echo "  ✅ $dir/"
    fi
  done
  [ ! -f "$proj/CLAUDE.md" ] && cp workspace/_shared/templates/project-template/CLAUDE.md "$proj/" && echo "  🔧 CLAUDE.md 복사됨"
done

# 루트 미분류 파일
echo "--- 루트 파일 점검 ---"
find workspace/ -maxdepth 1 -type f ! -name "CLAUDE.md" ! -name "WORKSPACE_GUIDE.md" ! -name "new-project.*" ! -name ".*" -exec echo "⚠️  미분류: {}" \;

echo "=== 점검 완료 ==="
```

## 산출물 파일 명명 규칙

```
{프로젝트코드}_{산출물유형}_{날짜}_v{버전}.{확장자}

예시:
P2026-001_보고서_20260315_v1.docx
P2026-001_발표자료_20260320_v2.pptx
P2026-001_웹앱_20260401_v1/ (폴더)
```

## 주의사항
- 파일/폴더 삭제 전 반드시 사용자 확인
- 아카이빙은 보존이며 삭제가 아님
- 공유 리소스 수정 후 반드시 동기화 실행
- 프로젝트 코드 번호 중복 금지
