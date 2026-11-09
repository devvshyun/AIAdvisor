# 레시피: 웹 화면 디자인 (방향은 한 곳에서만)

랜딩·소개 페이지, 앱·대시보드 화면을 Claude Code로 만들거나 고칠 때 쓴다. 핵심 규칙은 하나다. **디자인 방향은 생성 스킬 하나(또는 레퍼런스 하나)에서만 가져온다.** 여러 생성 스킬을 순서대로 엮으면 뒤 스킬이 앞 스킬의 결정을 자기 기준으로 다시 고쳐서, 누구의 디자인도 아닌 평균이 나온다. 이 저장소의 데모 페이지가 그렇게 만들어졌다가 다시 고쳐졌다(아래 "써 보니").

도구 정보(설치 명령, 비용, 위험)는 `catalog/web-design.yaml`에서 id로 찾는다.

## 실행 규칙

- 한 단계씩 실행한다. 단계가 끝나면 **확인 기준**을 실제로 확인한 결과를 보여 주고, 다음 단계로 갈지 사용자에게 묻는다.
- 설치가 필요한 단계는 설치 명령과 위험을 먼저 보여 주고 승인을 받는다. 이미 깔린 도구는 다시 설치하지 않는다.
- 설치나 명령이 막히면(권한 정책, 네트워크) 우회하지 말고 사용자에게 알린 뒤, 그 단계의 원칙만 손으로 적용할지 묻는다.

## 도구의 역할

| 역할 | 도구 | 같이 써도 되나 |
|---|---|---|
| **생성**: 색·서체·구성 같은 방향을 정한다 | `taste-skill`, `impeccable`(init·craft·polish·bolder·quieter), `frontend-design`, `superdesign` | **하나만.** 나머지는 끈다(2단계) |
| **움직임**: 이징, 지속 시간, 누름·호버 | `emil-design-eng` | 생성 스킬 하나에 덧붙여도 된다. 방향을 정하지 않는다 |
| **검사**: 결함만 찾는다 | `axe-cli`, `lighthouse-cli`, `web-design-guidelines`, `impeccable detect`, `chrome-devtools-mcp` | 여러 개 써도 된다. 결과로 결함만 고치고 방향은 바꾸지 않는다 |
| **화면 확인** | `playwright-cli`, `agent-browser`, `playwright-mcp` | 하나면 된다 |

`impeccable`은 두 역할을 다 한다. 다른 생성 스킬을 골랐다면 `impeccable`은 규칙 기반 탐지(`detect`)만 쓰고, 미감을 바꾸는 `critique`·`polish`는 쓰지 않는다.

## 단계

### 1. 상황을 보고 생성 스킬 하나를 고른다
- 할 일: 프로젝트를 읽고 아래 표에서 상황 하나를 고른다. 추천은 하나, 대안은 하나만 보여 준다.

| 상황 | 고를 것 | 이유 | 대안 |
|---|---|---|---|
| 새 랜딩·소개 페이지를 처음부터, 빨리 완성도 있게 | `taste-skill` | 팔레트·서체·히어로를 뽑고 자체 CSS 키트로 구조까지 정한다 | `frontend-design` |
| 이미 있는 화면을 고치거나, 디자인 기준을 문서로 남기고 싶다 | `impeccable` | 제품 맥락(PRODUCT.md)과 기준(DESIGN.md)을 만들고 섹션 단위로 다듬는다 | 레퍼런스 경로 |
| 앱·대시보드·관리 화면, 컴포넌트가 많은 업무용 화면 | `impeccable` (shadcn/ui 프로젝트면 `shadcn-mcp`를 더함) | 제품 UI와 앱 화면을 대상으로 하고, `quieter`로 차분하게 맞출 수 있다 | 레퍼런스 경로 |
| 틀에 얽매이지 않은 과감한 시안을 빨리 보고 싶다(이벤트 페이지, 프로토타입) | `frontend-design` | 지시문만 있는 가벼운 스킬이라 키트 구조 없이 브리프에 맞춰 대담하게 고른다. 보수적인 업무 화면에는 맞지 않는다 | `taste-skill` |
| 마음에 든 사이트가 있다, 또는 생성 스킬 결과가 계속 마음에 안 든다 | 레퍼런스 경로(3d) | 이미 완성된 시스템 하나를 따른다 | 비교 모드 |
| 어느 쪽인지 모르겠다 | 비교 모드(3e) | 따로 만든 결과를 보고 고른다 | |

- 넘길 것: 고른 스킬 하나, 고른 이유, 끌 스킬 목록
- 확인 기준: 사용자가 고른 스킬과 끌 목록을 승인했다.
- `superdesign`은 코드 맥락을 외부 서비스로 보내고 로그인이 필요해 기본 추천에서 뺀다. `figma-mcp`는 Figma 시안이 이미 있을 때만, Starter 플랜은 월 6회 제한이다.

### 2. 고르지 않은 생성 스킬을 끈다
- 할 일: 설치돼 있어도 요청이 설명에 맞으면 스킬이 저절로 끼어든다. 작업하는 동안 고르지 않은 생성 스킬을 끈다. 프로젝트의 `.claude/settings.local.json`(커밋하지 않는 로컬 설정)에 넣는다.
  ```json
  {
    "enabledPlugins": { "impeccable@impeccable": false },
    "permissions": { "deny": ["Skill(design-taste-frontend)", "Skill(frontend-design)"] }
  }
  ```
  - 플러그인으로 깔린 스킬은 `enabledPlugins`에서 `false`로 끈다. 이름은 `claude plugin list`에 나온 `<플러그인>@<마켓플레이스>`.
  - 폴더로 깔린 스킬(`~/.claude/skills/`, 프로젝트 `.claude/skills/`)은 `permissions.deny`에 `Skill(<스킬 이름>)`을 넣는다.
  - 한 번만 돌릴 때는 `claude -p ... --settings '<위 JSON>'`으로 그 실행에만 적용해도 된다.
  - `--settings`의 `enabledPlugins`에 플러그인 일부만 적으면 프로젝트 설정에서 켜 둔 플러그인이 안 보일 수 있다. 쓸 플러그인은 `true`로 같이 적는다.
- 넘길 것: 로컬 설정 파일
- 확인 기준: 새 세션에서 "쓸 수 있는 디자인 스킬 이름을 나열해" 또는 끈 스킬을 직접 불러 봤을 때 목록에 없거나 "blocked by permission rules"가 나온다.
- 써 보니(2026-11-09): `--settings '{"enabledPlugins":{"impeccable@impeccable":false}}'`로 실행하자 스킬 목록에서 impeccable이 빠졌다. `permissions.deny`의 `Skill(design-taste-frontend)`는 직접 불러도 "Skill execution blocked by permission rules"로 막았다. 프로젝트 범위로 설치한 frontend-design은 `--settings`에 impeccable·superpowers만 `false`로 적었을 때 목록에서 사라졌고, `"frontend-design@claude-plugins-official": true`를 같이 적자 보였다.
- 작업이 끝나면 로컬 설정에서 지워서 다시 켠다.

### 3a. taste-skill 경로
- 할 일: 스크립트로 페이지 종류에 맞는 팔레트, 서체 조합, 히어로 구성을 뽑고 키트 파일(`assets/`)과 `starter.html`에서 짓는다. 취향으로 고르지 않는다.
  ```bash
  node <skill>/assets/layout/deal.mjs --type software --has ui --history .taste-skill/layout-history.json
  node <skill>/scripts/start.mjs deal --page software --history .taste-skill/history.json
  node <skill>/scripts/start.mjs css --page software --palette <id> --type <id> --radius sharp --history .taste-skill/history.json
  ```
- 넘길 것: 페이지 초안, 뽑힌 조합을 적은 `DESIGN.md`
- 확인 기준: 한 섹션이 한 화면이나 두 화면이다. 제목 위 영문 라벨, 01·02 번호, 큰 숫자 강조, 카드 안의 카드가 없다.
- 써 보니: SKILL.md만 읽고 감으로 골랐을 때는 AI 톤이라는 평을 받았다. 스크립트와 참고 문서(`layout-v4.md`, `system.md`, `motion.md`, `copy.md`)를 끝까지 읽고 키트를 그대로 쓴 뒤에야 나아졌다. 키트를 공개 저장소에 올리면 라이선스(MIT) 전문을 함께 넣는다.

### 3b. impeccable 경로
- 할 일: `/impeccable init`으로 `PRODUCT.md`(누가, 무엇을, 말투)와 `DESIGN.md`(색, 서체, 간격, 금지 목록)를 만든 뒤, 섹션 하나씩 `critique` → `polish`·`bolder`·`quieter`로 좁혀 고친다. 기존 디자인을 갈아엎는 경우면 기존 모양은 "따라 하지 말 것"의 근거로만 쓴다.
- 넘길 것: `PRODUCT.md`, `DESIGN.md`, 고친 화면
- 확인 기준: `DESIGN.md`에 주조색 1개, 서체 조합, 금지 목록이 있고, 고친 섹션이 그 기준을 따른다.
- 주의: live 모드의 Apply는 채팅 세션이 응답하지 않으면 다른 에이전트를 권한 확인 없이 띄울 수 있다. live 모드를 쓰면 `IMPECCABLE_LIVE_COPY_AGENT=chat`을 설정한다.
- 써 보니: 기준 파일 없이 바로 화면부터 만들면 크림색 배경, 명조와 이탤릭 같은 "무난한 고급" 쪽으로 돌아갔다.

### 3c. frontend-design 경로
- 언제: 과감한 시안을 빨리 볼 때. 차분한 업무용 화면이면 3b로 간다.
- 할 일: 누가 쓰는지, 어떤 일을 하는 화면인지, 피하고 싶은 느낌을 짧은 브리프로 주고 한 번에 짓게 한 뒤, 고칠 점을 말로 짚어 반복한다. 스킬이 고른 방향(색·서체)을 `DESIGN.md`에 적어 두고 이후 수정도 그 기준으로 한다.
- 넘길 것: 화면 초안, `DESIGN.md`
- 확인 기준: 화면이 브리프의 톤을 따르고, 수정할 때 방향이 바뀌지 않는다.

### 3d. 레퍼런스 경로 (생성 스킬 없음)
- 할 일:
  1. 프로젝트를 요약한다: 누가 보는지, 말투, 콘텐츠 모양(긴 글·표·제품 화면), 꼭 필요한 섹션, 제약(한글, 다크 테마 등).
  2. 큐레이션 사이트(Godly, Land-book, SiteInspire, Awwwards 등)와 비슷한 제품군의 실제 사이트에서 후보를 찾고, 반드시 화면을 캡처한다. 글만 보고 고르지 않는다. `awesome-design-md`(실제 서비스의 디자인 언어를 DESIGN.md로 정리한 모음)도 후보 출처로 쓸 수 있다. 다만 그대로 쓰면 남의 브랜드를 따라 한 페이지가 된다.
  3. 후보 3개를 캡처와 함께 보여 준다. 각각 이 프로젝트에 맞는 이유와, 그대로 가져오기 어려운 부분(직접 그린 일러스트, 사진, 3D)을 적는다.
  4. 사용자가 **하나만** 고른다.
  5. 고른 레퍼런스에서 서체 크기 단계, 색의 역할, 그리드와 여백, 정보 밀도, 움직임 정도를 `DESIGN.md`로 옮기고 그 기준으로 짓는다.
- 섞기 규칙: 서체·색·레이아웃은 고른 하나만 따른다. 다른 레퍼런스에서는 부품 하나(예: 요금표 구조)만 빌리고, 빌린 부품도 고른 레퍼런스의 서체와 색으로 다시 칠한다. 빌리는 부품은 두 개까지.
- 넘길 것: 고른 레퍼런스와 캡처, `DESIGN.md`, 화면 초안
- 확인 기준: 초안을 레퍼런스 캡처와 나란히 놓았을 때 같은 시스템(서체 단계, 색 역할, 여백)으로 보인다. 그 회사의 로고, 고유 색 조합, 문구는 가져오지 않았다.

### 3e. 비교 모드
- 할 일: 같은 브리프로 생성 스킬 2~3개를 **각각 따로** 돌린다. 폴더를 나누고, 실행마다 2단계처럼 다른 생성 스킬은 끈다. 결과를 같은 폭으로 캡처해 나란히 보여 주고 하나를 고르게 한다. 고른 뒤에는 나머지를 버린다. 결과를 합치지 않는다.
- 넘길 것: 고른 결과와 그 스킬 이름
- 확인 기준: 사용자가 하나를 골랐고, 이후 단계는 그 스킬 경로(3a~3c)로 이어 간다.
- 써 보니(2026-11-09): 같은 페이지를 세 스킬에 따로 고치게 했더니 차분한 SaaS풍(taste-skill), 원색 포스터풍(impeccable), 큰 활자 편집풍(frontend-design)으로 완전히 갈렸고, 각각은 일관됐다. 비용은 frontend-design이 가장 가벼웠다(5턴, 입력 약 14만 토큰, 나머지 둘은 열 배 가까이). taste-skill은 "문구를 유지했다"고 답했지만 실제로는 제목과 기능 이름을 지웠다. 고른 뒤 결과 파일을 직접 확인한다. 결과: `showcase/web-generators/`.

### 4. 움직임과 호버 (emil-design-eng)
- 도구: `emil-design-eng`
- 할 일: 버튼 누름(`scale(0.97)`), 감속 곡선, 호버는 마우스 환경에서만, UI 반응은 300ms 이하. 색·서체·배치는 바꾸지 않는다.
- 확인 기준: `prefers-reduced-motion`에서 이동이 꺼지고 내용은 처음부터 보인다. 스크립트가 없어도 내용이 보인다.
- 써 보니: 섹션마다 같은 페이드인을 반복하면 AI 티로 보인다. 스크롤 연출은 한 곳에 모은다. 스크롤에 고정되는 연출은 "스크롤이 길다"는 평을 받아 클릭 탭으로 바꿨다.

### 5. 화면으로 확인한다
- 도구: `playwright-cli` 또는 `agent-browser` (같은 브라우저 상태로 긴 흐름을 탐색할 때만 `playwright-mcp`. 컨텍스트를 많이 쓴다)
- 할 일: 1440, 1024, 820, 768, 375px에서 캡처한다. taste-skill 경로였다면 키트의 `layout-check.js`를 페이지 안에서 돌린다.
- 확인 기준: 모든 폭에서 겹침·잘림·가로 스크롤이 없다.
- 써 보니: 키트의 `check.mjs`·`consistency.mjs`는 헤드리스 Chrome을 띄우는데 환경에 따라 응답 없이 멈췄다. 그럴 땐 `layout-check.js`를 브라우저 페이지에서 직접 실행했다.

### 6. 결함 검사
- 도구: `axe-cli`, `lighthouse-cli`, `web-design-guidelines`, `impeccable`(detect만), (MCP로 붙이려면 `chrome-devtools-mcp`)
- 할 일: 접근성, 성능, AI 티 패턴을 검사하고 **결함만** 고친다. 검사 도구가 방향을 바꾸자고 하면(다른 색, 다른 서체) 따르지 않고 1단계에서 고른 기준을 지킨다.
- 확인 기준: 라이트·다크 모두 글자 명암비 4.5:1 이상. axe 위반 0건. 접근성 점수와 LCP를 기록한다.
- 주의: `web-design-guidelines`는 실행할 때마다 GitHub에서 규칙을 받아 그대로 따른다. `chrome-devtools-mcp`는 기본으로 사용 통계를 보내므로 `--no-usage-statistics`를 붙인다.
- 써 보니: `npx impeccable detect`는 권한 정책에 막힐 수 있다. 설치된 플러그인의 `detect.mjs`를 로컬로 돌리면 파서 모듈이 없어 축소 모드로 돌았고 그라데이션을 놓쳤다. 반대로 축소 모드는 CSS로 그린 작은 삼각형(`border-left` + 위아래 투명 테두리)을 "한쪽 굵은 테두리(side-tab)"로 잘못 잡았다(2026-11-09, 컨셉 B). 결과를 그대로 고치지 말고 해당 줄을 확인한다. 대비는 브라우저에서 axe-core를 직접 돌리면 ChromeDriver 없이 잴 수 있었다.

### 7. 배포 (GitHub Pages)
- 도구: `github-pages-deploy`
- 할 일: `docs/`를 GitHub Actions로 배포한다(`automation` 레시피의 배포 단계). 데이터 생성 스크립트를 배포 전에 돌린다.
- 확인 기준: 배포 주소와 주요 자산 주소가 200을 돌려준다.
- 써 보니: Pages 소스를 "GitHub Actions"로 켜 두고 워크플로가 없으면 아무것도 배포되지 않는다. `.nojekyll`도 넣어 둔다.

## 써 보니: 섞어서 만든 데모 페이지

이 저장소 데모 페이지는 처음에 impeccable(기준) → taste-skill(뽑기·키트) → emil(움직임) → impeccable(검사)을 차례로 엮어 만들었다. 사용자는 "레퍼런스와 스킬을 다 섞으니 이상해진다"고 평했다. 이 레시피를 "생성 스킬 하나 + 움직임 + 검사"로 바꾼 이유다.

한국어 페이지 공통: 라틴 서체 뒤에 Pretendard를 대체 서체로 붙인다. 안 붙이면 한글이 시스템 글꼴로 떨어진다. 제목·본문에 `word-break: keep-all`을 주고 행간도 따로 본다.
