# P2026-001 장애인 B2B 사업

## 개요
- 클라이언트: 대기업 표준사업장 (장애인 고용 의무 기업)
- 기간: 2026년~
- 목적: 시앤피컨설팅 장애인 근로자 HR 솔루션 B2B 사업 기획 및 영업

## 주요 산출물
- [x] 시앤피컨설팅_장애인HR솔루션_소개서.docx (사업 소개 문서 V2)
- [ ] 추가 산출물 TBD

## 작업 규칙
- 모든 문서는 한국어로 작성
- 최종 산출물은 프로젝트 루트에 저장
- 참고 자료는 `data/` 폴더에 저장
- 작업 기록/메모는 `docs/` 폴더에 저장

## 폰트 (.fonts/ 폴더)
프로젝트 내 `.fonts/` 폴더에 한글 폰트가 저장되어 있음.
문서 작성, 이미지 생성 등에 활용 가능.

### 사용 가능한 폰트
| 폰트명 | 파일 | 굵기 |
|--------|------|------|
| **Paperlogy (페이퍼로지)** | Paperlogy-1Thin.ttf | Thin (1) |
| | Paperlogy-2ExtraLight.ttf | ExtraLight (2) |
| | Paperlogy-3Light.ttf | Light (3) |
| | Paperlogy-4Regular.ttf | Regular (4) |
| | Paperlogy-5Medium.ttf | Medium (5) |
| | Paperlogy-6SemiBold.ttf | SemiBold (6) |
| | Paperlogy-7Bold.ttf | Bold (7) |
| | Paperlogy-8ExtraBold.ttf | ExtraBold (8) |
| | Paperlogy-9Black.ttf | Black (9) |
| **Gmarket Sans (G마켓 산스)** | GmarketSansLight.otf | Light |
| | GmarketSansMedium.otf | Medium |
| | GmarketSansBold.otf | Bold |

### 폰트 사용법 (PIL/Pillow)
```python
from PIL import ImageFont
# 프로젝트 폰트 경로
FONT_DIR = "/sessions/kind-trusting-lamport/mnt/P2026-001_장애인_B2B사업/.fonts"
font = ImageFont.truetype(f"{FONT_DIR}/Paperlogy-4Regular.ttf", 40)
```

### 폰트 시스템 설치 (세션 시작 시)
```bash
mkdir -p ~/.local/share/fonts
cp /sessions/kind-trusting-lamport/mnt/P2026-001_장애인_B2B사업/.fonts/* ~/.local/share/fonts/
fc-cache -f
```

## 컨텍스트
- 브랜드명: 시앤피컨설팅
- 3단계 서비스: STEP 1 직무 발굴 워크샵 → STEP 2 HR 체계 구축 컨설팅 → STEP 3 위탁 관리 BPO
- SaaS HR 대시보드는 STEP 3 Enterprise 티어 전용
- 기획 문서 8종이 data/ 폴더에 있음 (01~08)
