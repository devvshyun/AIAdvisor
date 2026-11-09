# 카탈로그 변경 기록

갱신할 때마다 맨 위에 한 덩어리씩 더한다. 절차는 `REFRESH.md`.

## 2026-11-09 쓰지 않는 항목 정리 (46 → 41개, 가이드 82 → 78편)

평가 답변 24개, 레시피 사용 여부, 써 본 기록, 겹침을 근거로 정리했다.
- 뺀 도구 5개
  - `claude-code-security-review-action`: 관리 중단·유료라 규칙상 추천하지 않는데 자리만 차지했다.
  - `inbox-zero`: 메일함 도구라 프로젝트 보완과 거리가 멀다. 레시피에 없고 평가 추천 0회.
  - `pr-review-toolkit`: 내장 `/code-review`와 같은 일. 레시피에 없고 언급 0회.
  - `feature-dev`: `superpowers` 흐름과 같은 일. 레시피에 없고 언급 1회.
  - `commit-commands`: `gh` CLI로 충분. 언급 0회.
- 웹 디자인 가이드 4편을 `references/_archive/09-web-design/`으로 옮겼다. 디자인 스킬을 차례로 엮으라는 내용이 "생성 스킬은 하나만" 레시피와 충돌했다.
- 데모 기본 페이지의 "UI가 AI 티 나요" 예시 답변도 새 레시피(생성 스킬 하나, 나머지 끄기, 움직임·결함 검사)에 맞게 고쳤다.
- 남긴 것 중 다시 볼 후보: `semgrep-guardian`(계정 필요, 언급 0회), `claude-security`(언급 0회), `agent-browser`(`playwright-cli`와 같은 일).

## 2026-11-06 직접 써 본 기록(`hands_on`) 추가

- 항목에 `hands_on`을 더했다. 이 저장소 작업에서 실제로 써 본 도구만 적고, 나머지는 "문서로만 확인"으로 둔다.
- 써 본 도구 8개: taste-skill, impeccable, emil-design-eng(데모 페이지), github-pages-deploy(데모 배포), superpowers, builtin-code-review, builtin-security-review, gitleaks(연습용 저장소에서 코딩 레시피 1~10단계).
- 코딩 레시피 "써 보니"에 실행 결과를 적었다. 그중 레시피를 바꿀 만한 것: 실제 프로세스로 돌리는 테스트가 필요했다(Windows 파이프 출력 인코딩), `/security-review`는 origin 원격이 있어야 돈다, pre-commit 로컬 훅의 실행 파일은 Windows에서 `language: script`로 건다.

## 2026-11-06 첫 카탈로그

- 세 분야를 처음 조사했다: 웹 디자인 15개, 코딩 19개, 자동화 12개(모두 46개).
- 여러 분야에 걸친 도구는 한 파일에만 두고 `also`로 다른 분야를 적었다.
  - `gitleaks`: coding (also automation)
  - `playwright-mcp`: web-design (also coding, automation)
  - `playwright-cli`: web-design (also automation)
  - `github-mcp`: automation (also coding). 자동화 조사의 `github-mcp-server`와 합쳤다.
  - `claude-code-hooks`: automation (also coding). 코딩 조사의 `hooks`와 합쳤다.
- 조사에서 나온 주의점
  - impeccable live 모드의 Apply는 승인 없이 다른 에이전트를 띄울 수 있다(`IMPECCABLE_LIVE_COPY_AGENT`).
  - chrome-devtools-mcp는 기본으로 사용 통계를 보낸다(`--no-usage-statistics`로 끔).
  - web-design-guidelines는 실행할 때마다 GitHub에서 규칙을 받아 따른다.
  - Figma MCP Starter 플랜은 월 6회로 제한된다.
  - gitleaks는 유지보수 모드이고 후속작은 Betterleaks다.
  - claude-code-security-review 액션은 `maintained: false`.
