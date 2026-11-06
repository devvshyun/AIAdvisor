# 레시피: 기능 하나를 계획부터 병합까지

기존 저장소에 기능을 더하거나 버그를 고칠 때, Claude가 즉흥적으로 고치지 않고 계획 → 테스트 → 검증 → 리뷰 순서를 지키게 만드는 흐름이다. 한 줄 수정이나 탐색성 질문에는 맞지 않는다(절차가 더 무겁다).

도구 정보(설치 명령, 비용, 위험)는 `catalog/coding.yaml`과 `catalog/automation.yaml`에서 id로 찾는다.

## 실행 규칙

- 한 단계씩 실행한다. 단계가 끝나면 **확인 기준**을 실제로 확인한 결과(명령 출력)를 보여 주고, 다음 단계로 갈지 사용자에게 묻는다.
- "통과했을 것"은 증거가 아니다. 테스트·타입체크·린트는 실제로 돌린 출력만 증거로 친다.
- 설치가 필요한 단계는 설치 명령과 위험을 먼저 보여 주고 승인을 받는다. 이미 깔린 도구는 다시 설치하지 않는다.
- `--no-verify`, 훅 끄기, 테스트 건너뛰기로 막힌 단계를 넘기지 않는다. 막히면 사용자에게 알린다.

## 처음 한 번: 최소 스택

역할마다 하나만 고른다. 같은 역할 도구를 둘 켜면 지시가 부딪치고 컨텍스트만 는다.

| 역할 | 고를 것 | 같이 켜지 말 것 |
|---|---|---|
| 계획·TDD·검증 습관 | `superpowers` | `ecc` (꼭 쓰려면 `--profile minimal`로 훅 없이) |
| 최신 라이브러리 문서 | `context7` (CLI+스킬 방식이 상시 토큰이 적다) | |
| 코드 내비게이션 | `lsp-plugins` (큰 저장소에서 심볼 단위 편집이 필요할 때만 `serena`로 바꾼다) | `serena`·`graphify`·`understand-anything`을 동시에 상시로 |
| 리뷰 | `builtin-code-review` | 같은 이름의 `code-review` 플러그인 |
| 보안 | `builtin-security-review` + `security-guidance` | `security-guidance`와 `semgrep-guardian`을 둘 다 편집 훅으로 |
| 결정적 안전장치 | `claude-code-hooks` + `gitleaks` pre-commit | |
| PR·이슈 | `gh` CLI (MCP가 꼭 필요할 때만 `github-mcp`) | `gh`와 `github-mcp`를 둘 다 상시로 |
| 웹 E2E (웹일 때만) | `playwright-cli` (탐색형 작업일 때만 `playwright-mcp`) | 둘 다 |

- 세션 기억은 내장 auto-memory, `claude-mem`, Serena memory 중 하나만 쓴다. 셋이 따로 쌓이면 서로 어긋난다.
- 출력 압축(`caveman`)은 리뷰·보안 단계에서 끈다. 근거와 재현 절차가 빠지기 쉽다.

## 단계

### 1. 브랜치를 나눈다
- 도구: `superpowers`
- 할 일: `git switch -c feat/<이름>` 또는 superpowers `using-git-worktrees`로 워크트리를 만든다.
- 넘길 것: 작업 브랜치
- 확인 기준: `git status`가 깨끗하고, 현재 브랜치가 기본 브랜치가 아니다.

### 2. 요구사항을 좁힌다
- 도구: `superpowers`, `lsp-plugins`
- 할 일: superpowers `brainstorming`으로 무엇을 만들지, 무엇은 안 만들지 정한다. 낯선 코드베이스면 먼저 LSP(정의 이동·참조 찾기)로 관련 모듈을 좁힌다. 아주 크고 처음 보는 저장소일 때만 `graphify`나 `understand-anything`을 한 번 돌린다.
- 넘길 것: 설계 요약(바꿀 파일, 바꾸지 않을 것)
- 확인 기준: 사용자가 설계 요약을 승인했다.

### 3. 계획을 쓴다
- 도구: `superpowers`, `context7`
- 할 일: plan 모드나 superpowers `writing-plans`로 작업 단위와 테스트 목록을 쓴다. 외부 라이브러리를 쓰면 Context7로 지금 쓰는 버전의 문서를 확인한다.
- 넘길 것: 계획 파일
- 확인 기준: 계획의 작업마다 "어떤 테스트가 실패하다가 통과해야 하는지"가 적혀 있다.

### 4. 테스트부터 구현한다
- 도구: `superpowers`, `claude-code-hooks`
- 할 일: superpowers `test-driven-development`로 실패하는 테스트 → 최소 구현 → 정리 순서로 간다. PostToolUse 훅(matcher `Edit|Write`)으로 포매터와 린터가 편집마다 돌게 해 둔다.
- 넘길 것: 코드와 테스트
- 확인 기준: 테스트 러너 출력에서 새 테스트가 처음엔 실패했고 지금은 통과한다.

### 5. 끝났다고 말하기 전에 검증한다
- 도구: `superpowers`
- 할 일: superpowers `verification-before-completion`. 전체 테스트, 타입체크, 린트를 실제로 돌린다.
- 넘길 것: 명령 출력
- 확인 기준: 세 명령의 출력이 모두 통과다.

### 6. 코드 리뷰
- 도구: `builtin-code-review`
- 할 일: `/code-review high`. 정리할 게 많으면 `/simplify`를 먼저 돌린다. 지적을 반영한다.
- 넘길 것: 반영한 수정
- 확인 기준: 높은 신뢰도 지적이 0건이거나, 남긴 건마다 사유가 적혀 있다.

### 7. 보안 리뷰
- 도구: `builtin-security-review`, `claude-security`
- 할 일: `/security-review`(origin 원격이 있어야 한다). 인증·입력 처리·비밀값을 건드린 변경이면 `claude-security`로 변경분을 한 번 더 깊게 본다.
- 넘길 것: 발견 목록과 조치
- 확인 기준: 높음 이상 발견이 0건이다.

### 8. 커밋
- 도구: `gitleaks`, `security-guidance`
- 할 일: 커밋한다. gitleaks pre-commit과 security-guidance 커밋 점검이 자동으로 돈다.
- 넘길 것: 커밋
- 확인 기준: 훅이 통과했다. `SKIP=gitleaks`로 건너뛸 수 있으니 CI에서도 한 번 더 돌린다.

### 9. PR과 CI
- 도구: `commit-commands`, `claude-code-security-review-action`
- 할 일: `gh pr create`(또는 commit-commands). CI에서 테스트와, 쓰고 있다면 Semgrep이나 보안 리뷰 액션을 돌린다. `claude-code-security-review-action`은 `maintained: false`라 새로 붙이기 전에 저장소 상태를 확인한다.
- 넘길 것: PR 주소
- 확인 기준: CI가 초록이고 사람 리뷰어 1명이 승인했다.

### 10. 병합과 정리
- 도구: `superpowers`
- 할 일: superpowers `finishing-a-development-branch`로 병합 방식을 고르고 워크트리와 브랜치를 지운다.
- 확인 기준: 기본 브랜치에서 테스트가 다시 통과한다.

## 써 보니

- 이 저장소에서 스킬 자체를 고칠 때는 2~5단계를 skill-creator의 평가 루프(테스트 케이스 → 이전 버전과 비교 → 채점)로 바꿔 썼다. 문서·프롬프트가 산출물이면 "테스트"는 평가 케이스가 된다. 키워드로 채점하면 오탐이 나서 결과 글을 직접 읽어 고쳤다.
- Windows에서 Python 스크립트가 한글을 출력하다 cp949 오류로 멈췄다. `PYTHONUTF8=1`을 붙여 돌린다.
