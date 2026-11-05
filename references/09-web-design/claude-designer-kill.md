# 클로드로 전문가가 만든 것 같은 웹사이트 만드는 법 (디자인 스킬 3개 + 연결 도구 2개)
- 도구·주제: Claude Code + emil-design-eng / Impeccable / Taste(design-taste-frontend) + Playwright MCP / Figma MCP · AI 웹디자인 품질 향상 (웹 디자인, 스킬·MCP, 16분 읽기, STEP 5개, 약 20분 실습, 2026-09-19 갱신)
- 한 줄 요약: 디자인 기준(스킬 3개)과 확인 도구(MCP 2개)를 설치하고 구체적인 브리프를 줘서 보라색 그라데이션·똑같은 카드 세 장 같은 "AI 티" 나는 사이트에서 벗어난다.

## 언제 쓰나
- 클로드로 만든 웹사이트가 다 비슷하고 밋밋할 때. 원인 3가지: 따를 디자인 기준 없음 / 참고할 화면 없음 / 결과를 직접 볼 눈 없음. 스킬·MCP가 각각을 메움.
- 스킬 = AI에게 미리 읽히는 작업 지침서 파일, MCP = AI가 바깥 프로그램에 연결하는 공통 규격. 별도 디자인 앱 없이 Claude Code 안에서 동작.

## 준비물 / 필요 도구
- Node.js v22.20.0+ (https://nodejs.org LTS), Claude Code (https://claude.com/product/claude-code). 명령은 macOS 터미널 기준, Windows는 WSL/Git Bash 같은 리눅스식 터미널 권장.
- emilkowalski/skills (`emil-design-eng`, MIT, 스타 38.8k): https://github.com/emilkowalski/skills · 문서 https://github.com/emilkowalski/skills/blob/main/skills/emil-design-eng/SKILL.md
- Impeccable (Apache 2.0, 스타 69.0k): https://impeccable.style/ · https://github.com/pbakaus/impeccable · 시작 가이드 https://impeccable.style/tutorials/getting-started/
- Taste Skill (`design-taste-frontend`, MIT, 스타 88.3k): https://tasteskill.dev/ · https://github.com/Leonxlnx/taste-skill
- Playwright MCP (Apache 2.0, 스타 37.3k): https://github.com/microsoft/playwright-mcp · https://playwright.dev/docs/getting-started-mcp
- Figma MCP: `https://mcp.figma.com/mcp` · 안내 https://help.figma.com/hc/en-us/articles/39888612464151-Claude-Code-and-Figma-Set-up-the-MCP-server
- 비용: 스킬 3개와 Playwright는 무료. Figma MCP는 베타 기간 무료지만 공식 문서에 추후 사용량 기반 유료 전환 예고. (스타 수는 2026-09-19 확인값. 검증: impeccable 4.1.0 · skills 1.7.0 · @playwright/mcp 0.0.82)

## 단계별 방법
### 보조 프롬프트: 5개 설치·검증 위임 (프롬프트 뼈대, Claude Code용)
- 역할: 디자인 스킬 3개와 MCP 2개 설치·검증 담당. 슬롯: [만들고 싶은 웹사이트 한 줄].
- 작업: `node --version` 확인(v22.20.0 미만이면 설치 안내) → `ls .claude/skills`, `claude mcp list`로 이미 있는지 보고 없는 것만 아래 명령으로 설치 → 설치 후 폴더 3개와 playwright 연결 확인(figma는 브라우저 로그인 승인 전엔 목록에 안 나오는 것이 정상) → 5개의 역할과 다음 할 일을 5줄 이내로 안내.
- 제약: sudo·전역 설치·설정 수정 전 질문, 이미 있는 항목 재설치·덮어쓰기·삭제 금지, `.env` 등 비밀 파일 읽기/출력 금지. 검증: `ls .claude/skills`에 `design-taste-frontend`·`emil-design-eng`·`impeccable`, `claude mcp list`에 `playwright: npx @playwright/mcp@latest - ✔ Connected`. 실패 시 완료 보고 금지.

### Quick Start
웹사이트용 새 폴더(이름 자유):
```bash
mkdir my-site
cd my-site
```
설치 4줄을 한 줄씩:
```bash
npx --yes skills@latest add emilkowalski/skills --skill "emil-design-eng" --agent claude-code --yes --copy
npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend" --agent claude-code --yes --copy
npx --yes impeccable@latest install --providers=claude --scope=project
claude mcp add playwright npx @playwright/mcp@latest
```
성공: 줄마다 `✓ emil-design-eng (copied)` 같은 표시, 마지막에 `Added stdio MCP server playwright`. 확인:
```bash
ls .claude/skills
claude mcp list
```
폴더 3개 + `playwright: npx @playwright/mcp@latest - ✔ Connected`.

### STEP 1. 준비물 확인 (2분)
```bash
node --version
claude --version
```
- Node v22.20.0 이상(스킬 설치 도구의 최소 버전; 낮으면 명령이 실패), Claude Code는 버전 숫자만 나오면 OK. 없으면 nodejs.org LTS 설치 후 터미널 새로 열기, Claude Code는 설치 먼저.

### STEP 2. 디자인 스킬 두 개 (4분)
기준이 없으면 클로드는 학습된 기본값(흔한 템플릿)으로 돌아감.
| 스킬 | 하는 일 | 강점 |
|---|---|---|
| Emil Kowalski Design | 타이포그래피·간격·레이아웃·애니메이션 기준 | 버튼 눌리는 느낌, 팝업 뜨는 방향 |
| Impeccable | AI 티 나는 곳을 규칙으로 잡아냄 | 검사 명령이 있어 눈대중 불필요 |
```bash
npx --yes skills@latest add emilkowalski/skills --skill "emil-design-eng" --agent claude-code --yes --copy
npx --yes impeccable@latest install --providers=claude --scope=project
```
- 성공: `✓ emil-design-eng (copied)`와 `→ ./.claude/skills/emil-design-eng`, `Installed impeccable into: .claude (project)`, 끝에 `/impeccable init` 안내. 이미 설치돼 있으면 생략.
- Claude Code를 완전히 종료했다 다시 켠 뒤(재시작해야 새 스킬을 읽음) Claude Code 안에서:
```
/impeccable init
```
  무엇을 만드는 서비스인지, 누구에게 보여줄 건지를 묻고 `PRODUCT.md`를 생성. 이후 새 대화에서도 클로드가 이 파일을 먼저 읽음.

### STEP 3. Taste 스킬 추가 (3분)
앞의 둘이 "무엇을 피할지"를 알려 준다면 Taste는 기준이 될 대상 자체를 바꿈: 뻔한 배치 대신 잘 만든 사이트의 구조·분위기를 가져옴. 랜딩/소개 사이트처럼 보이는 게 중요한 화면용.
```bash
npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend" --agent claude-code --yes --copy
```
- 성공: `✓ design-taste-frontend (copied)`. 저장소에 스킬 13개가 있어 `--skill`로 하나만 골라야 함(없이 설치하면 쓰지 않을 스킬이 한꺼번에 들어옴).
- 다이얼 3개(1~10, 요청 때 숫자로 말하면 반영):
| 다이얼 | 낮추면 | 올리면 |
|---|---|---|
| VARIANCE | 반듯한 대칭 배치 | 과감한 비대칭 |
| MOTION | 거의 안 움직임 | 스크롤·물리 효과 |
| DENSITY | 여백 넓은 화면 | 정보 빽빽한 화면 |
- 결과가 그대로라면 참고 대상을 안 준 것 → 참고 사이트 이름 한두 개를 적어 줄 때 일함.

### STEP 4. 확인 도구 두 개 연결 (5분)
없으면 클로드는 코드만 쓰고 화면은 못 본 채 "다 됐다"고 보고함.
```bash
claude mcp add playwright npx @playwright/mcp@latest
claude mcp add --transport http figma https://mcp.figma.com/mcp
```
- 성공: `Added stdio MCP server playwright with command: npx @playwright/mcp@latest`, `Added HTTP MCP server figma with URL: https://mcp.figma.com/mcp to local config`. 이미 있으면 생략.
- 추가 후 Claude Code 재시작 → `/mcp` 입력 → 피그마 계정 로그인 승인 → 연결됨. 승인 전엔 `claude mcp list`에 figma가 안 보이는 게 정상(playwright 한 줄만 있어도 OK), 승인 후 다시 실행하면 figma 줄이 늘어남.
```bash
claude mcp list
```
- 사용 요청 뼈대: 만든 사이트를 로컬에서 실행해 주소 알려 주기 → Playwright로 데스크톱·모바일 두 크기로 캡처 → 간격 어긋남/글자 넘침/줄 안 맞음을 찾아 고친 뒤 다시 캡처해 비교.
- 피그마 파일을 쓰지 않으면 Figma 연결은 건너뛰어도 됨.

### STEP 5. 결과를 바꾸는 브리프 쓰기 (6분)
스킬은 기준만 알려 줄 뿐 무엇을 만들지는 모름 → 감독처럼 지시.
- ❌ `우리 회사 웹사이트 만들어 줘. 깔끔하고 예쁘게 해 줘.`
- ✅ 브리프 뼈대: [업종]의 소개 사이트, 디자인 스킬과 Taste 스킬 사용 / 대상 [누가 볼지] / 느낌 [예: 차분하고 믿음직한] / 참고 분위기 [좋아하는 사이트 1~2곳] / 페이지 홈·서비스·소개·문의 / 홈 구성 = 약속 한 줄이 든 첫 화면, 장점 3개, 후기, 자주 묻는 질문, 버튼 1개 / 브랜드 색 [색상 코드], 글꼴 [글꼴 이름] / 완성 후 Playwright로 데스크톱·모바일 캡처하고 간격·넘침·정렬 수정 후 보여 주기.
- 차이는 길이가 아니라 판단 재료(대상·느낌·참고 대상)로 선택지가 좁아지는 것.
- 첫 결과는 완성이 아님. 한 번 더 다듬기:
  - ❌ `좀 더 세련되게 바꿔 줘.`
  - ✅ 뼈대: 첫 화면 정리(여백 더, 제목 키우기, 버튼 하나만), 섹션 사이 간격 96픽셀 통일, 모바일 메뉴 넘침 수정, 고치기 전/후 캡처 둘 다 보여 주기.

## 설치 확인과 문제 해결
```bash
ls .claude/skills
npx --yes impeccable@latest detect <검사할 HTML 파일이나 폴더>
claude mcp list
```
- 첫 줄: `design-taste-frontend`, `emil-design-eng`, `impeccable` 3개 / 둘째 줄: 검사 결과 / 셋째 줄: 연결 도구 목록.
- `detect`는 HTML 파일/폴더를 대상으로 함(CSS 파일만 주면 아무것도 안 나옴). 결과 예: `[overused-font] Primary font: inter`, `[ai-color-palette] Purple/violet accent colors detected`, `13 anti-patterns found.` 걸린 항목이 있으면 오류처럼 끝나지만 고장이 아니라 찾았다는 뜻. 빈 출력은 통과가 아니라 무엇을 검사했는지부터 확인. 뜻이 모호하면 결과를 클로드에 그대로 붙여 고치게 함.
- 되돌리기(프로젝트 폴더에서):
```bash
rm -rf .claude/skills/emil-design-eng .claude/skills/design-taste-frontend .claude/skills/impeccable
claude mcp remove playwright
claude mcp remove figma
```
  이후 `ls .claude/skills`가 비고 `claude mcp list`에서 두 줄이 사라지면 원복(사이트 파일·Claude Code는 그대로).
| 증상 | 원인 | 해결 |
|---|---|---|
| `command not found: npx` | Node.js 없음 | nodejs.org LTS 설치 후 터미널 재시작 |
| 설치 명령이 버전 오류 | Node < 22.20 | LTS로 올리고 터미널 재시작 후 재실행 |
| 설치했는데 클로드가 모름 | 재시작 전 | Claude Code 완전 종료 후 재실행 |
| 쓰지 않을 스킬까지 설치됨 | `--skill` 미지정 | 이름 지정 재설치, 남는 폴더 삭제 |
| 검사 명령이 아무것도 안 보임 | CSS만 검사 | HTML 파일/폴더 지정 |
| `/impeccable`을 못 알아들음 | 재시작 전이거나 설치 범위 다름 | 재시작 후 `ls .claude/skills` 확인 |
| 스킬 깔았는데 결과 그대로 | STEP 5 생략 | 대상·느낌·참고 사이트 적어 재요청 |
| 피그마 연결 안 됨 | 로그인 승인 안 함 | `/mcp` 입력 후 브라우저에서 승인 |

## 핵심 팁 · 주의사항 (솔직한 한계)
- ⚠️ 스킬은 취향을 만들어 주지 않음 → 참고 사이트 1~2개를 안 주면 3개를 깔아도 결과가 크게 안 바뀜.
- ⚠️ 첫 결과는 완성본이 아님. `detect`로 걸린 항목을 짚어 가며 1~2회 더 수정.
- ⚠️ AI 생성 이미지는 레이아웃이 좋아도 티가 남. 브랜드 방향은 직접 정해야 함(디자이너 대체 아님, 출발점을 올려 주는 도구).
- ⚠️ Figma MCP는 현재 무료 베타, 이후 유료 전환 예고.
- 이미 설치된 항목은 건너뛰기, 설치는 프로젝트 범위(`--scope=project`).

## 바로 쓰는 체크리스트
- [ ] Node 22.20+ / `claude --version` 확인
- [ ] 스킬 3개 설치 + Claude Code 완전 재시작 + `/impeccable init`
- [ ] Playwright, Figma MCP 연결 + `/mcp`에서 Figma 승인
- [ ] 브리프에 대상·느낌·참고 사이트·색·글꼴·구성 포함
- [ ] Playwright 캡처 기반 수정 요청 + `impeccable detect` 실행
