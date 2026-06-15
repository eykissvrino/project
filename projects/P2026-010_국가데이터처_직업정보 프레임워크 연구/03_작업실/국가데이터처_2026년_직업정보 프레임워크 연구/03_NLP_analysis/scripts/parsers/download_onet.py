"""O*NET Work Activities 위계(GWA/IWA/DWA) 참조 파일 다운로드 시도.

받는 것(텍스트 탭구분):
  - Content Model Reference.txt  → GWA 41개(Element ID 4.A.*) + 정의
  - IWA Reference.txt            → IWA ~332개
  - DWA Reference.txt            → DWA ~2,000개

여러 DB 버전을 순회하며 최초 성공본을 저장. 네트워크 차단 시 명확히 보고.
저장 위치: 01_data_collection/00_external_references/.../02_ONET_WorkActivities_DWA/onet_data/
"""
from __future__ import annotations

import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OUT_DIR = (Path(__file__).resolve().parents[2]
           / "01_data_collection" / "00_external_references"
           / "직업정보 관련 참고자료_해외" / "02_ONET_WorkActivities_DWA" / "onet_data")

FILES = ["Content Model Reference.txt", "IWA Reference.txt", "DWA Reference.txt"]
VERSIONS = ["29_3", "29_2", "29_1", "29_0", "28_3", "28_2", "28_1", "28_0"]
BASE = "https://www.onetcenter.org/dl_files/database/db_{ver}_text/{fname}"

UA = {"User-Agent": "Mozilla/5.0 (research; KSCO framework study)"}


def try_fetch(url: str, timeout: int = 30) -> bytes | None:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if r.status == 200:
                return r.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"   miss: {e}")
    return None


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for ver in VERSIONS:
        print(f"=== try O*NET db version {ver} ===")
        got = {}
        for fname in FILES:
            url = BASE.format(ver=ver, fname=urllib.parse.quote(fname))
            print(f" GET {url}")
            data = try_fetch(url)
            if data:
                (OUT_DIR / fname).write_bytes(data)
                got[fname] = len(data)
                print(f"   OK {len(data):,} bytes")
        if len(got) == len(FILES):
            print(f"\nSUCCESS version {ver}: {got}")
            print(f"saved to: {OUT_DIR}")
            # 간단 행수 보고
            for fname in FILES:
                n = sum(1 for _ in (OUT_DIR / fname).open(encoding="utf-8", errors="replace"))
                print(f"   {fname}: {n} lines")
            return 0
        else:
            print(f"   version {ver} 부분 실패({len(got)}/{len(FILES)}), 다음 버전 시도")
    print("\nFAILED — 모든 버전 다운로드 실패(네트워크 차단 또는 URL 변경). "
          "수동 다운로드: https://www.onetcenter.org/database.html")
    return 1


if __name__ == "__main__":
    sys.exit(main())
