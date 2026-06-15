[세세분류 코드] {ksco_code}
[세세분류 명칭] {name}
[부모 세분류] {parent_code} {parent_name}
[Layer] {layer}
[source] {source}
[source_subject] {source_subject_or_null}

[부모 세분류 정의]
{parent_definition_text}

[부모 세분류 주요 업무]
{parent_main_tasks_text}

[세세분류 정의]
{definition_text}

[세세분류 직업 예시]
{examples_text}

위 정보를 분석하되, 부모 세분류 주요 업무를 활동 골격으로 삼고 세세분류 정의·예시로 특화하여 시스템 규약대로 JSON을 출력하라. 해당 세세분류와 무관한 상속 활동은 제외한다. 세세분류 정의가 이름·영문만 있어 특화 신호가 약하면, 상속 골격을 보존하고 confidence를 낮춰 출력한다.
