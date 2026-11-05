# AI 티 안 나는 웹사이트, 클로드로 만드는 법
- 원문: https://lazyowen.com/guides/designskill
- 도구·주제: Claude Code + taste-skill + impeccable (+ 선택: Claude Design) · 웹 디자인 (2026-08-06 갱신, STEP 6개 · 약 10분)
- 한 줄 요약: 스킬 2개 설치 → `/impeccable init`으로 디자인 기준 파일(PRODUCT.md, DESIGN.md) 저장 → 빌드 요청에 가드레일 추가 → `impeccable detect`로 AI 티를 자동 검사.

## 언제 쓰나
- Claude가 만든 UI가 매번 같은 글꼴, 보라색 그라데이션, 카드 안의 카드로 뻔하게 나올 때
- AI 티는 취향이 아니라 거의 정해진 목록으로 나타나므로, 기준을 파일로 남기고 기계로 검사하고 싶을 때

## 준비물 / 필요 도구
- taste-skill(스킬 이름 `design-taste-frontend`, 배치·움직임 기준을 바꿈): https://tasteskill.dev/ · https://github.com/Leonxlnx/taste-skill
- impeccable(디자인 기준 생성 + 어긋난 곳 검출): https://impeccable.style/ · https://github.com/pbakaus/impeccable · 검사 규칙 https://impeccable.style/docs/detector
- Node.js 22 이상(프롬프트는 22.12 이상 안내) — https://nodejs.org/ LTS. 두 스킬 모두 Node로 동작, 버전이 낮으면 설치 실패
- (선택) Claude Design: https://claude.ai/design · https://claude.com/product/design — Pro/Max/Team/Enterprise에서만(무료 불가), 사용량은 채팅·Claude Code와 공유, Enterprise는 기본 꺼짐이라 관리자가 조직 설정에서 켜야 함
- 가격: 두 스킬의 요금 언급 없음. 용어: 스킬=AI가 미리 읽는 작업 지침서 파일, DESIGN.md=색·글꼴 등 디자인 규칙 메모(AI가 화면 만들 때마다 먼저 읽음)

## 단계별 방법
**Quick Start** — 작업 프로젝트 폴더에서
```bash
npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill \
  --skill "design-taste-frontend" --agent claude-code --yes --copy
npx --yes impeccable@latest install --providers=claude --scope=project
ls .claude/skills     # design-taste-frontend 와 impeccable 두 폴더가 보이면 성공
```
- 성공 출력 예: `design-taste-frontend (copied)`, `Installed impeccable into: .claude (project)`, `Installed hooks into: .claude`

**설치·검증 위임 프롬프트 뼈대 (Claude Code)**
- 역할: 디자인 스킬 2개의 설치·연결 검증 담당. 맥락: 스킬 미설치일 수 있고 만든 화면에 AI 티가 남는 상태
- 채울 곳: [OS·셸], [기술 스택 — 예: HTML과 CSS만], [목표 — 예: AI 티 없는 랜딩 페이지]
- 작업 4단계: ① `node --version` 22.12 이상, `.claude/skills`에 두 스킬 존재 여부 확인(있으면 재설치 금지) ② 프로젝트 루트에서 위 두 설치 명령 ③ `ls .claude/skills`로 폴더 2개 확인 + 아무 CSS/HTML 하나로 `npx --yes impeccable@latest detect <파일경로>` 실행 ④ 두 스킬의 역할과 사용법을 5줄 이내 설명
- 제약: 기존 파일·설정 덮어쓰기/삭제 금지, `npm install -g` 금지, `.env`·키 파일 읽기/출력 금지, 중복 설치 금지. 검증: 폴더 2개 + detect 오류 없이 종료. 하나라도 실패하면 완료 보고 금지

**STEP 1. 준비물 확인 (2분)**
```bash
node --version    # v22.12.0 처럼 v22 이상. 낮거나 command not found면 nodejs.org LTS 설치 후 터미널 재시작
```

**STEP 2. 스킬 두 개 설치 (3분)** — 반드시 프로젝트 폴더 안에서 실행해야 그 프로젝트에만 설치
```bash
cd <프로젝트 폴더 경로>
npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill \
  --skill "design-taste-frontend" --agent claude-code --yes --copy
#   → ✓ design-taste-frontend (copied), → ./.claude/skills/design-taste-frontend
npx --yes impeccable@latest install --providers=claude --scope=project
#   → 마지막에 /impeccable init 을 실행하라는 안내
```
- 설치 후 Claude Code를 완전히 종료했다 다시 켜야 스킬을 읽음

**STEP 3. 디자인 기준 만들기 (5분) — 가장 중요**: 스킬만 깔고 멈추면 AI가 학습된 무난한 기본값으로 돌아가 결과가 거의 안 바뀜
```
/impeccable init
```
- 이 화면이 브랜드용인지 제품용인지, 대상 독자, 색, 글꼴, 분위기를 묻고 답하면 `PRODUCT.md`, `DESIGN.md`를 생성. 이후 새 대화에서도 AI가 매번 이 파일을 읽음
- 기준을 함께 정하는 프롬프트 뼈대: 내 브랜드는 [브랜드 한 줄 설명], 주 고객은 [고객층]. 경쟁사와 겹치지 않게 ① 주조색 1개 + 배경색 + 본문 글자색, 각각 이유 한 줄 ② 제목용·본문용 글꼴 각 1개 추천(Inter, Roboto, 시스템 기본 제외) ③ 이 브랜드에서 쓰지 말아야 할 시각 요소 3가지 → 결과를 DESIGN.md에 반영

**STEP 4. AI 티 다섯 가지 알아두기 (3분)**
| 자주 나오는 기본값 | 대신 요청할 것 |
|---|---|
| 글꼴이 늘 Inter/시스템 기본값 | 브랜드에 맞는 글꼴 지정 |
| 보라→파랑 그라데이션 | 의도해서 정한 주조색 한 가지 |
| 카드 안에 카드 안에 카드 | 여백과 선으로 나눈 납작한 구조 |
| 색 있는 배경 위 회색 글자 | 대비를 확보한 본문 색 |
| 튕기는 바운스 효과 | 짧고 자연스럽게 멈추는 움직임 |
- 빌드 요청 가드레일 뼈대: [만들 화면 설명]을 만들되, DESIGN.md의 색·글꼴을 그대로 사용. 금지: Inter/Roboto/시스템 기본 글꼴, 보라·파랑 계열 그라데이션 배경, 카드 안의 카드, 색 있는 배경 위 회색 본문, 튕기는 바운스. 다 만든 뒤 위 5항목을 하나씩 점검해 결과 보고

**STEP 5. 검사로 확인하기 (3분)** — 규칙 약 60개를 기계가 자동 확인
```bash
npx --yes impeccable@latest detect <검사할 폴더>
```
- 문제가 있으면 규칙 ID와 이유 출력. 예: `[overused-font] Primary font: inter`, `[ai-color-palette] Purple/violet accent colors detected`, 끝에 `2 anti-patterns found.`
- 출력이 없으면 통과(고칠 곳 없어 조용히 종료)
- 수정 프롬프트 뼈대: `npx --yes impeccable@latest detect <검사할 폴더>`를 실행해 나온 항목을 하나씩 수정, 고칠 때마다 DESIGN.md 기준 유지, 전부 고친 뒤 같은 명령을 재실행해 아무것도 나오지 않는지 확인

**STEP 6. (선택) 화면 보면서 다듬기 (Claude Design)**
- 대화로 시안을 만들고 요소를 눌러 글자·간격을 직접 수정, 결과를 PPTX/PDF/HTML로 내보내거나 Claude Code로 넘겨 개발 계속
- STEP 3에서 정한 색·글꼴을 그대로 넣어야 일관됨. 시작은 https://claude.ai/design
- 용어: 디자인 시스템=브랜드의 색·글꼴·버튼 모양을 묶은 규칙 모음

## 핵심 팁 · 주의사항
- 순서: 스킬 설치 → 기준 작성(`/impeccable init`) → 화면 제작 → 검사. 하나만 빠져도 AI 티가 남음
- 눈으로 보면 놓치는 것을 detect의 규칙 60개가 매번 같은 곳에서 잡아 줌
- 슬래시 명령은 `/impeccable init`만 명시됨

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| `command not found: npx` | Node.js 없음 | nodejs.org LTS 설치 후 터미널 재시작 |
| `Invalid agents: claude` | 도구 이름 축약 | `--agent claude-code`로 입력 |
| 스킬을 깔았는데 결과가 그대로 | STEP 3 누락 | `/impeccable init`으로 기준 파일 먼저 생성 |
| `/impeccable`을 못 알아들음 | 재시작 전 | Claude Code 완전 종료 후 재실행 |
| detect가 아무것도 출력하지 않음 | 문제 없음 | 정상 |
| Claude Design 메뉴가 안 보임 | 무료 요금제이거나 조직 설정 꺼짐 | 유료 요금제로 변경, 회사 계정이면 관리자에게 요청 |

## 바로 쓰는 체크리스트
- [ ] Node ≥ 22 확인
- [ ] 프로젝트 폴더에서 두 스킬 설치, `ls .claude/skills`로 확인, Claude Code 완전 재시작
- [ ] `/impeccable init`으로 `PRODUCT.md`·`DESIGN.md` 생성
- [ ] 빌드 요청에 DESIGN.md 참조 + 금지 5항목 + 셀프 체크 포함
- [ ] `npx --yes impeccable@latest detect <폴더>` 결과 0건 확인
- [ ] (선택) Claude Design에서 시각 조정
