"""pytest 루트 conftest — scripts/ 를 sys.path 에 올려 `import utils` 가능하게 한다."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
