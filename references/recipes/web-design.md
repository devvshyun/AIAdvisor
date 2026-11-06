# 레시피: AI 티 안 나는 랜딩·소개 페이지

정적 소개 페이지나 랜딩 페이지를 Claude Code로 만들거나 갈아엎을 때 쓴다. 이 저장소의 데모 페이지(`docs/index.html`)를 실제로 이 순서로 만들었고, 그때 겪은 일을 "써 보니"에 적었다. 대시보드·관리 화면처럼 기능 위주 화면에는 맞지 않는다.

도구 정보(설치 명령, 비용, 위험)는 `catalog/web-design.yaml`에서 id로 찾는다.

## 실행 규칙

- 한 단계씩 실행한다. 단계가 끝나면 **확인 기준**을 실제로 확인한 결과를 보여 주고, 다음 단계로 갈지 사용자에게 묻는다.
- 설치가 필요한 단계는 설치 명령과 위험을 먼저 보여 주고 승인을 받는다. 이미 깔린 도구는 다시 설치하지 않는다.
- 설치나 명령이 막히면(권한 정책, 네트워크) 우회하지 말고 사용자에게 알린 뒤, 그 단계의 원칙만 손으로 적용할지 묻는다.
- 역할이 같은 도구는 하나만 켠다. 생성 스킬(`taste-skill`, `frontend-design`, `superdesign`)을 같이 켜면 서로 다른 방향을 지시해 결과가 섞인다. 화면 확인 도구(`agent-browser`, `playwright-cli`, `playwright-mcp`)도 하나면 된다.

## 단계

### 1. 제품 맥락과 디자인 기준부터 (impeccable)
- 도구: `impeccable`, `awesome-design-md`(선택)
- 할 일: `/impeccable init`으로 `PRODUCT.md`(누가, 무엇을, 말투)와 `DESIGN.md`(색, 서체, 간격, 금지 목록)를 만든다. 기존 디자인을 갈아엎는 경우면 기존 모양은 "따라 하지 말 것"의 근거로만 쓴다.
- 넘길 것: `PRODUCT.md`, `DESIGN.md`
- 확인 기준: 두 파일이 있고, `DESIGN.md`에 주조색 1개, 서체 조합, 금지 목록이 있다.
- 참고할 분위기가 있으면 `awesome-design-md`에서 비슷한 DESIGN.md를 골라 출발점으로만 쓴다. 실제 회사 사이트를 분석한 파일이라 그대로 쓰면 남의 브랜드를 따라 한 페이지가 된다.
- 써 보니: 기준 파일 없이 바로 화면부터 만들면, 매번 크림색 배경, 명조와 이탤릭 같은 "무난한 고급" 쪽으로 돌아갔다.

### 2. 팔레트·서체·구성은 뽑기로 정한다 (taste-skill)
- 도구: `taste-skill` (가볍게 시작하려면 대신 `frontend-design`. Figma 시안이 있으면 `figma-mcp`, shadcn/ui 프로젝트면 `shadcn-mcp`를 더한다)
- 할 일: taste-skill 스크립트로 페이지 종류에 맞는 팔레트와 서체 조합, 히어로 구성을 뽑는다. 취향으로 고르지 않는다.
  ```bash
  node <skill>/assets/layout/deal.mjs --type software --has ui --history .taste-skill/layout-history.json
  node <skill>/scripts/start.mjs deal --page software --history .taste-skill/history.json
  node <skill>/scripts/start.mjs css --page software --palette <id> --type <id> --radius sharp --history .taste-skill/history.json
  ```
- 넘길 것: 뽑힌 팔레트·서체 `:root` 블록, 히어로 id, 내비게이션·꼬리말·버튼 종류. 결과를 `DESIGN.md`에 옮겨 적는다.
- 확인 기준: `DESIGN.md`의 색·서체가 뽑기 결과와 같다. 보라 계열이 없다.
- 써 보니: 처음엔 SKILL.md만 읽고 감으로 골랐다가 AI 톤이라는 평을 받았다. 스크립트와 참고 문서(`layout-v4.md`, `system.md`, `motion.md`, `copy.md`)를 끝까지 읽고 키트(시스템 CSS, 모션 레이어)를 그대로 쓴 뒤에야 나아졌다.
- 한국어 페이지: 뽑힌 라틴 서체 뒤에 Pretendard를 대체 서체로 붙인다. 안 붙이면 한글이 시스템 글꼴로 떨어진다. 제목·본문에 `word-break: keep-all`을 주고 행간도 따로 본다.
- 주의: `figma-mcp`는 Starter 플랜에서 월 6회로 제한된다. `superdesign`은 코드 맥락을 외부 서비스로 보내고 로그인이 필요해 기본 추천에서 뺐다.

### 3. 키트로 짓는다
- 도구: `taste-skill`
- 할 일: taste-skill 키트 파일(`assets/`)을 프로젝트로 복사하고 `starter.html`과 뽑힌 히어로 레시피에서 시작한다. 제품 화면이 있으면 키트의 app-frame 구성으로 크게 보여 준다.
- 넘길 것: 페이지 초안
- 확인 기준: 한 섹션이 정확히 한 화면이나 두 화면이다. 제목 위 영문 라벨, 01·02 번호, 큰 숫자 강조, 카드 안의 카드가 없다.
- 써 보니: 키트를 공개 저장소에 올리면 라이선스(MIT) 전문을 함께 넣는다. 데이터로 만든 부분(목록, 개수)은 빌드 스크립트로 생성해서 저장소 안에 둔다. 임시 폴더에 두면 다시 만들 수 없다.

### 4. 모션과 호버 (emil-design-eng)
- 도구: `emil-design-eng`, `impeccable`
- 할 일: 버튼 누름(`scale(0.97)`), 감속 곡선, 호버는 마우스 환경에서만, UI 반응은 300ms 이하. 섹션 단위로 `/impeccable critique` → `polish`·`quieter`처럼 좁혀서 고친다.
- 주의: impeccable live 모드의 Apply는 채팅 세션이 응답하지 않으면 다른 에이전트를 권한 확인 없이 띄울 수 있다. live 모드를 쓰면 `IMPECCABLE_LIVE_COPY_AGENT=chat`을 설정한다.
- 확인 기준: `prefers-reduced-motion`에서 이동이 꺼지고 내용은 처음부터 보인다. 스크립트가 없어도 내용이 보인다.
- 써 보니: 섹션마다 같은 페이드인을 반복하면 taste-skill과 impeccable 기준 모두에서 AI 티로 본다. 스크롤 연출은 한 곳(모먼트 하나)에 모은다. 스크롤에 고정되는 연출(pinned-chapters)은 "스크롤이 길다"는 평을 받아 클릭 탭으로 바꿨다.

### 5. 화면으로 확인한다 (브라우저)
- 도구: `agent-browser` 또는 `playwright-cli` (같은 브라우저 상태로 긴 흐름을 탐색해야 할 때만 `playwright-mcp`. 컨텍스트를 많이 쓴다)
- 할 일: 1440, 1024, 820, 768, 375px에서 캡처하고 taste-skill의 `layout-check.js`를 페이지 안에서 돌린다.
- 확인 기준: 모든 폭에서 발견 0건, 가로 스크롤 없음.
- 써 보니: 키트의 `check.mjs`·`consistency.mjs`는 헤드리스 Chrome을 띄우는데, 환경에 따라 응답 없이 멈췄다. 그럴 땐 `layout-check.js`를 앱 브라우저 페이지에서 직접 실행했다. 이 검사는 "히어로 창의 대화가 아래 흐림 구간에 들어가는지"는 보지 않는다. 화면 높이 900, 800, 768에서 버튼 위치를 따로 재야 한다.

### 6. 접근성·성능과 AI 티 검사
- 도구: `web-design-guidelines`, `impeccable`, `axe-cli`, `lighthouse-cli` (MCP로 붙이려면 `chrome-devtools-mcp`)
- 할 일: Web Design Guidelines 스킬로 포커스·라벨·대비·움직임 줄이기를 검사하고, `impeccable detect`로 AI 티를 검사한다. 수치는 `axe --exit`와 `lighthouse`로 잰다.
- 확인 기준: 라이트·다크 모두 글자 명암비 4.5:1 이상. detect 결과 0건. axe 위반 0건. 접근성 점수와 LCP를 README에 적는다.
- 주의: `web-design-guidelines`는 실행할 때마다 GitHub에서 규칙을 받아 그대로 따른다. `chrome-devtools-mcp`는 기본으로 사용 통계를 보내므로 `--no-usage-statistics`를 붙인다.
- 써 보니: `npx impeccable detect`는 권한 정책에 막힐 수 있다. 설치된 플러그인의 `detect.mjs`를 로컬로 돌리면 파서 모듈이 없어 축소 모드로 돌았고 그라데이션을 놓쳤다. 이 한계를 결과에 적는다.

### 7. 배포 (GitHub Pages)
- 도구: `github-pages-deploy`
- 할 일: `docs/`를 GitHub Actions로 배포한다(`automation` 레시피의 배포 단계). 데이터 생성 스크립트를 배포 전에 돌린다.
- 확인 기준: 배포 주소와 주요 자산 주소가 200을 돌려준다.
- 써 보니: Pages 소스를 "GitHub Actions"로 켜 두고 워크플로가 없으면 아무것도 배포되지 않는다. `.nojekyll`도 넣어 둔다.
