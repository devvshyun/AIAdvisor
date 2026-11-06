# 레시피: 저장소 자동화 두 가지

1. **push하면 페이지가 다시 배포되고, 한 달에 한 번 건강 검사 이슈가 열린다.** 문서·데모 페이지가 있는 저장소용.
2. **매주 Claude가 저장소를 훑고 보고서를 남긴다.** 리뷰·정리를 정기적으로 맡기고 싶을 때.

도구 정보(설치 명령, 비용, 위험)는 `catalog/automation.yaml`에서 id로 찾는다.

## 실행 규칙

- 한 단계씩 실행한다. 단계가 끝나면 **확인 기준**을 실제로 확인한 결과를 보여 주고, 다음 단계로 갈지 사용자에게 묻는다.
- 비밀값(API 키, 토큰)은 사용자가 직접 저장소 Secrets에 넣게 안내한다. 대신 입력하지 않고, 명령줄·파일에 평문으로 쓰지 않는다.
- 저장소 설정 변경, push, 예약 작업 생성은 바깥에 영향을 주는 일이라 매번 승인을 받는다.
- 워크플로의 액션 버전은 예시를 그대로 믿지 않고 실행 전에 최신 태그를 확인한다(`git ls-remote --tags https://github.com/<owner>/<action>`).

## 레시피 1. 배포와 월간 건강 검사

### 1. Pages 소스를 GitHub Actions로
- 도구: `github-pages-deploy`
- 할 일: Settings → Pages → Build and deployment → Source를 **GitHub Actions**로 바꾼다(사용자가 직접).
- 확인 기준: Settings → Environments에 `github-pages`가 보인다(첫 배포 뒤에 생길 수 있다). 생기면 배포 브랜치를 `main`만 허용한다.
- 써 보니: 소스만 GitHub Actions로 켜 두고 워크플로가 없으면 아무것도 배포되지 않고 오류도 안 뜬다.

### 2. 배포 워크플로
- 도구: `github-pages-deploy`
- 할 일: `.github/workflows/pages.yml`에 checkout → (생성 스크립트·빌드) → configure-pages → upload-pages-artifact → deploy-pages를 둔다. 최상단 권한은 `contents: read`, Pages 권한(`pages: write`, `id-token: write`)은 배포 잡에만 준다. 정적 HTML이면 `.nojekyll`을 함께 넣는다.
- 넘길 것: 워크플로 파일
- 확인 기준: Actions 탭에서 배포 잡이 초록이고, 페이지 주소와 주요 자산 주소가 `curl -sI`로 200을 돌려준다.
- 써 보니: 목록·개수처럼 데이터에서 나오는 부분은 생성 스크립트를 저장소에 두고 배포 전에 돌렸다(`--check` 옵션으로 CI에서 어긋남도 잡는다). 업로드 아티팩트는 심볼릭 링크가 있으면 실패한다.

### 3. 월간 건강 검사
- 도구: `lychee-action`, `claude-code-hooks`
- 할 일: `schedule`(예: `17 3 1 * *`, 정각은 몰리니 피한다)과 `workflow_dispatch`로 도는 워크플로를 만든다. 링크 검사(`lychee-action`)나 프로젝트 고유 검사 스크립트를 돌리고, 실패하면 `gh issue`로 같은 제목의 열린 이슈가 있으면 댓글, 없으면 새 이슈를 연다. 권한은 `contents: read`, `issues: write`.
- 넘길 것: 워크플로 파일
- 확인 기준: 수동 실행이 한 번 통과한다. 일부러 깨진 링크를 넣은 브랜치에서 수동 실행해 이슈가 실제로 열리는지 보고, 확인 뒤 닫는다.
- 써 보니: 이 저장소는 카탈로그 도구들의 저장소가 보관되거나 오래 멈췄는지를 `scripts/check_catalog.py --freshness`로 매달 검사해 이슈를 연다. GitHub API 익명 한도에 금방 걸려서 `GITHUB_TOKEN`을 넘긴다.
- 주의: 공개 저장소는 60일 동안 활동이 없으면 `schedule` 워크플로가 꺼진다. 이슈가 안 열린 게 건강해서인지 꺼져서인지는 Actions 탭의 마지막 실행 날짜로 구분한다. `schedule`은 기본 브랜치의 파일만 돈다.

## 레시피 2. 매주 리뷰하고 보고하는 Claude

먼저 방식을 고른다. 기준은 "PC가 꺼져 있어도 돌아야 하나", "로컬 파일이 필요한가", "누가 비용을 내나"다.

| 방식 | id | 어디서 | 주의 |
|---|---|---|---|
| 클라우드 예약 작업 (`/schedule`) | `claude-cloud-scheduled-tasks` | Anthropic 클라우드 | 구독 사용량 차감, 기본이 auto mode, 연결된 커넥터로 쓰기도 한다 |
| GitHub Actions + cron | `claude-code-action` | Actions 러너 | Actions 분 + API 토큰 이중 과금 |
| 데스크톱 로컬 예약 | `claude-local-scheduling` | 내 PC | 앱이 켜져 있고 PC가 깨어 있어야 한다 |

### 1. 보고서 범위를 정한다
- 할 일: 무엇을 읽고(지난 7일 병합된 PR, 열린 이슈 등) 무엇을 남길지(이슈 댓글 1개, 알림 1개) 정한다. 프롬프트에 "읽기만 한다. 코드 변경·push 금지. 결과는 한 곳에 한 번만 보낸다"를 넣는다. 날짜 기준은 "오늘 기준 지난 7일"처럼 프롬프트에 박는다(건너뛴 회차가 몰아서 돌 수 있다).
- 넘길 것: 프롬프트(또는 `.claude/skills/weekly-review` 스킬)
- 확인 기준: 사용자가 범위와 보고 위치를 승인했다.

### 2. 고른 방식으로 만든다
- 도구: `claude-cloud-scheduled-tasks`, `claude-code-action`, `claude-local-scheduling` 중 하나
- 할 일:
  - 클라우드: `/schedule`로 만든다. `ANTHROPIC_API_KEY`가 잡혀 있으면 `/schedule`이 안 보인다. 커넥터는 보고에 필요한 것만 남긴다. 브랜치 보호 규칙을 건다.
  - Actions: `schedule` + `workflow_dispatch` 워크플로에 `anthropics/claude-code-action`을 두고 `--max-turns`, `timeout-minutes`, `--allowedTools`(필요한 도구만)를 모두 건다. 토큰은 사용자가 Secrets에 넣는다.
  - 로컬: Code 탭 → Scheduled → New task에서 폴더·주기·권한 모드를 고른다.
- 넘길 것: 예약 작업 또는 워크플로 파일
- 확인 기준: 비용 상한(최대 턴, 제한 시간)과 권한 범위가 설정에 보인다.

### 3. 한 번 돌려 본다
- 할 일: Run now(또는 `workflow_dispatch`)로 1회 실행한다. 로컬 예약은 이때 뜨는 권한 요청에 "항상 허용"을 줘야 다음 회차가 멈추지 않는다.
- 확인 기준: 실행 기록이 성공이고, 보고가 목적지에 정확히 한 번 도착했다. "성공"이어도 네트워크 차단·도구 누락은 실행 기록(transcript, 로그)에만 남으니 직접 읽는다.

### 4. 알림 (선택)
- 도구: `ntfy`, `claude-code-hooks`
- 할 일: 끝났을 때 휴대폰으로 받고 싶으면 `ntfy`로 한 줄 보낸다. 본문엔 링크만 넣는다.
- 확인 기준: 알림이 한 번 온다.
- 주의: 공개 서버 토픽 이름은 사실상 비밀번호다. 추측하기 어렵게 짓는다.

### 5. 2~3주 운영 후 비용 확인
- 확인 기준: 사용량 페이지나 Actions 사용 시간이 예상 범위 안이다. 넘으면 주기를 늘리거나 범위를 줄인다.

## 공통 함정

- 기본 `GITHUB_TOKEN`으로 만든 커밋은 다른 워크플로를 트리거하지 않는다. "Claude가 push했는데 CI가 안 돈다"의 흔한 원인이다.
- 공개 저장소에서 포크 PR은 비밀값을 받지 못한다. `pull_request_target`으로 우회하지 않는다.
- Secrets에서 지워도 키는 살아 있다. 키 자체를 발급처에서 폐기한다.
- 훅은 사용자 권한으로 임의 명령을 실행한다. 남의 저장소를 열기 전에 프로젝트 `.claude/settings.json`의 훅을 확인한다.
- Zapier(`zapier-mcp`), Make(`make-mcp`), n8n(`n8n-mcp`)은 역할이 거의 같다. 이미 쓰는 플랫폼 하나에만 붙인다. Zapier는 도구 호출마다 작업 2개를 쓰고, Make의 로컬 npx 서버는 legacy이며, n8n은 npm 설치 운영이 deprecated다.
- 세션 안 `/loop`은 장기 스케줄러가 아니다. 세션이 닫히면 멈추고 7일 뒤 만료된다.
