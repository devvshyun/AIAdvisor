# 카탈로그 변경 기록

갱신할 때마다 맨 위에 한 덩어리씩 더한다. 절차는 `REFRESH.md`.

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
