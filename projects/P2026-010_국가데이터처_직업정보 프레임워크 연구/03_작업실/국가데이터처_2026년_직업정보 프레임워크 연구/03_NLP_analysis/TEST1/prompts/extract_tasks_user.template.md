[세세분류 코드] {ksco_code}
[세세분류 명칭] {name}
[위계] {major_code} {major_name} > {mid_code} {mid_name} > {minor_code} {minor_name} > {broad_code} {broad_name}
[Layer] {layer}    [source] {source}    [source_subject] {source_subject}
[low_signal(정의빈약)] {low_signal}
[주요업무 출처] {main_tasks_source}

[추출컨텍스트 — 세세정의 + 조상정의(세>소>중>대)]
{extraction_context}

[상속 적용된 주요업무]
{main_tasks_text}

[세세분류 직업 예시]
{examples_text}

[추출 지시]
- 위 정보에서 직무활동(TASK)·도구·작업환경 3차원을 시스템 규약대로 **JSON만** 출력하라.
- **출처 분기에 따라 추출 방식이 다르다 — 「주요업무 출처」를 보고 판단하라:**
  - "세세분류 자체보유" 또는 "세분류 상속" → **2-pass**: (1) 상속 주요업무를 활동 골격으로 삼고 (2) 세세분류 정의·예시로 목적어를 구체화하고 고유활동을 추가하며 무관한 상속활동은 제거한다.
  - "없음" → 주요업무 골격이 없으므로 **추출컨텍스트(세세+조상 정의)에서 직접** 활동을 도출한다.
- `low_signal`이 TRUE(세세정의 빈약)이면 세세정의 단독으로 추출하지 말고 **반드시 추출컨텍스트의 조상정의를 함께 근거로** 삼는다. 특화 신호가 약하면 상속 골격을 보존하되 confidence를 낮춘다.
- 각 task의 `source_sentence`(원문 근거)와 `derived_from`(도출 출처·경로)를 빠짐없이 채워라.
