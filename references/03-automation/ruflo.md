# Claude Code에 에이전트 팀 붙이는 Ruflo 입문 가이드
- 원문: https://lazyowen.com/guides/ruflo
- 도구·주제: Ruflo + Claude Code · 자동화 / 멀티 에이전트 (코딩, 8분 읽기, STEP 9개, 2026-08-06 갱신)
- 한 줄 요약: Claude Code 바깥에 에이전트 조율·메모리·작업 라우팅을 얹는 오픈소스 Ruflo를 연습 폴더에서 작은 팀(최대 8 에이전트)부터 단계적으로 써 보는 입문.

## 언제 쓰나
- 한 프로젝트에서 researcher/coder/tester/reviewer 같은 역할 분담과 프로젝트 메모리를 쓰고 싶을 때
- 에이전트 = 모델 자체가 아니라 모델에 역할·도구·메모리·실행 규칙을 묶은 작업 단위

## 준비물 / 필요 도구
- Ruflo: GitHub https://github.com/ruvnet/ruflo · npm https://www.npmjs.com/package/ruflo · 사용자 가이드 https://github.com/ruvnet/ruflo/blob/main/docs/USERGUIDE.md · 최신 릴리스 https://github.com/ruvnet/ruflo/releases/latest
- Node.js 20 이상, npm 9 이상, Claude Code
- 코드/CLI는 MIT 오픈소스. 단 Claude Code 구독료·외부 모델 API 요금·실행 장비 비용은 별도.

## 단계별 방법
### Quick Start (새 연습 폴더에서)
```bash
mkdir ruflo-starter
cd ruflo-starter
npx ruflo@latest init wizard
npx ruflo@latest doctor
claude
```
- 설치 후 `.claude/`, `.claude-flow/`, `CLAUDE.md`가 생김(역할 분담·작업 기억용 프로젝트 설정).
- Claude Code가 열리면 시작 프롬프트의 `<...>`만 바꿔 붙여넣기. 프롬프트 뼈대: 역할=Ruflo 계층형 스웜 코디네이터(researcher·coder·tester·reviewer 조정), 슬롯 <프로젝트 상황 한 줄>, <기술 스택>, <만들 기능 한 줄>, <수정하면 안 되는 파일·규칙>. 작업=애매하면 먼저 질문 → 조사·구현·테스트·리뷰 계획을 짧게 제시 → 구현. 제약=에이전트 최대 8개. 출력=바뀐 파일 목록, 테스트·빌드·린트 결과, 남은 위험. 검증=리뷰 역할이 점검하고 실제 실행 로그를 근거로 제시.

### STEP 1. 실행 환경 확인 (2분)
```bash
node --version
npm --version
claude --version
```
node가 v20 미만이거나 claude를 못 찾으면:
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```
세 명령이 오류 없이 버전을 출력하면 다음 단계.

### STEP 2. 전체 기능으로 초기화 (5분)
- 두 경로: 플러그인 설치 vs CLI 초기화. 플러그인만 설치하면 슬래시 명령과 일부 역할은 되지만 MCP 서버·훅·프로젝트 메모리는 붙지 않음 → 초보자는 CLI 초기화 권장.
- 기존 프로젝트면 먼저 변경 사항 확인(Ruflo가 설정 파일을 추가함):
```bash
git status --short
npx ruflo@latest init wizard
```
- 대화형이 부담스러우면: `npx ruflo@latest init`
- 상태 확인:
```bash
npx ruflo@latest init check
npx ruflo@latest doctor
```
`init check`가 초기화됨으로 표시하고 `doctor` 핵심 검사에 오류가 없으면 완료.

### STEP 3. Claude Code에 MCP 연결 (2분)
MCP = Claude Code가 Ruflo의 스웜·에이전트·메모리 도구를 호출하게 하는 규격.
```bash
claude mcp list
```
목록에 ruflo가 없으면 한 번만 등록:
```bash
claude mcp add ruflo -- npx -y ruflo@latest mcp start
claude mcp list
```
- 두 번째 목록에 ruflo가 보이면 연결 완료. 플러그인만 설치한 경우 이 연결이 자동으로 생기지 않을 수 있음.

### STEP 4. 작은 팀부터 시작 (3분)
100개 역할을 한꺼번에 띄우지 말 것. 공식 안티 드리프트 예시는 계층형 최대 8 에이전트 권장(Queen-led hierarchy: 코디네이터 하나가 분배·취합, 직접 다 하지 않음).
```bash
npx ruflo@latest swarm init \
  --topology hierarchical \
  --max-agents 8 \
  --strategy specialized
npx ruflo@latest swarm status
npx ruflo@latest agent list
```
`swarm status`가 계층형 스웜을 보여주면 준비 완료.

### STEP 5. 실제 작업 맡기기 (10분 이상)
프로젝트 루트에서 Claude Code를 열고 요청. 프롬프트 뼈대: `<기능>`을 구현. 진행 방식=관련 코드·기존 테스트 먼저 조사 → 계층형 스웜에서 researcher/coder/tester/reviewer만 사용 → 구현 전 변경 범위·검증 기준을 짧게 제시 → 구현 후 실제 테스트·린트 실행 → 실패하면 원인 수정 후 재검증 → 마지막에 바뀐 파일·테스트 결과·남은 위험만 보고.
- 좋은 요청은 완료 기준이 선명함: "로그인 기능을 만들어 줘"보다 "이메일 로그인, 잘못된 비밀번호 오류, 단위 테스트까지".
- 검증은 에이전트 수가 아니라 결과로:
```bash
npx ruflo@latest swarm status
npx ruflo@latest agent list
```
  그리고 Claude Code가 보고한 테스트 명령을 직접 재실행하고 `git diff`로 변경 범위 확인.

### STEP 6. 성공 패턴을 메모리에 남기기 (3분)
훅이 성공한 작업 패턴을 다음 요청에 재사용하도록 설계됨. 규칙을 직접 저장·검색해 연결 확인:
```bash
npx ruflo@latest memory store \
  --key "project/test-rule" \
  --value "기능 변경 뒤 단위 테스트와 린트를 모두 실행한다" \
  --namespace "project"
npx ruflo@latest memory search \
  --query "기능 변경 뒤 검증" \
  --namespace "project"
```
검색 결과에 방금 규칙이 나오면 메모리 정상. 비밀번호·API 키·고객 정보는 저장 금지.

### STEP 7. "100명 무료 고용" 정확히 이해 (2분)
- 100+는 에이전트 카탈로그 크기이지, 작업마다 모델 프로세스 100개가 동시 실행되는 게 아님. 기본 초기화는 약 24개 핵심 에이전트, `--all-agents`는 약 89개(릴리스마다 변동).
- 공식 문서의 "토큰 30~50% 절감", "Claude Code 사용량 최대 250%" 등은 WASM 변환·캐시·저비용 모델 라우팅이 잘 맞았을 때의 프로젝트 측 설명이지 보장값이 아님. 처음엔 에이전트 4~8개로 시작하고 실제 사용량 확인.

### STEP 8. 설치 직전 최신값 확인 (1분)
블로그의 버전 숫자보다 npm 레지스트리 기준으로:
```bash
npm view ruflo@latest version engines license --json
npx --yes ruflo@latest --version
```
`engines.node`가 내 Node 버전과 맞고 라이선스가 MIT인지 확인.

### STEP 9. 내 프로젝트에 안전하게 적용 (3분)
- 연습 폴더에서 먼저 성공 → 실제 프로젝트에 적용
- 초기화 전 `git status --short`로 작업 중 파일 확인
- 첫 스웜은 최대 4~8개 에이전트
- 프롬프트에 수정 가능한 경로와 완료 기준 명시
- 실행 후 테스트 결과와 `git diff` 직접 확인
- `.env`, API 키, 고객 데이터는 프롬프트·메모리에 넣지 않음
- 문제 시 자동 수정부터 누르지 말고 진단 먼저:
```bash
npx ruflo@latest doctor
npx ruflo@latest doctor --fix
```
  `doctor --fix`는 현재 CLI 기준 수정 명령을 출력만 하고 자동 적용하지 않음 → 읽고 필요한 것만 직접 실행.

## 문제 해결 (FAQ)
- node 버전이 낮다: Node.js 20 이상으로 올리고 터미널 재시작 후 `node --version`.
- Windows에서 bash 없음: `curl | bash` 대신 PowerShell/cmd에서 `npx ruflo@latest init wizard`.
- Claude Code에서 Ruflo 도구가 안 보임: 플러그인만 설치했거나 MCP 미등록 → `claude mcp add ruflo -- npx -y ruflo@latest mcp start` 후 `claude mcp list`.
- 초기화 후 파일이 많이 생김: 정상(`.claude/`, `.claude-flow/`, `CLAUDE.md` 등). 손으로 지우기 전에 `git diff`로 확인.
- 에이전트를 많이 띄우면 좋아지나: 아님. 역할이 겹치면 조정 비용·모델 사용량 증가. 작은 기능은 researcher·coder·tester·reviewer로 시작, 부족할 때만 추가.
- "무료"인데 사용량이 줄어드는 이유: Ruflo 자체만 MIT. 실제 추론은 Claude Code 구독/모델 API 한도·비용을 그대로 씀.

## 핵심 팁 · 주의사항
- ⚠️ 원문 수치 표기가 일부 불명확(범위 표기 대시가 빠져 "48", "3050%"로 보임). STEP 4 "최대 8", STEP 9 "4~8"을 따라 8 이하로 시작하는 게 안전.
- 에이전트 수가 많다고 좋은 게 아님 → 완료 기준과 수정 가능 경로를 명확히.
- 메모리·프롬프트에 비밀값 금지.
- 토큰 절감/사용량 증가 수치는 조건부 주장.
- 블로그 속 버전은 오래될 수 있음 → npm/릴리스로 확인.

## 바로 쓰는 체크리스트
- [ ] Node ≥ 20, npm ≥ 9, Claude Code 설치
- [ ] 연습 폴더에서 `init wizard` + `doctor`
- [ ] `claude mcp list`에 ruflo 확인 (없으면 `claude mcp add`)
- [ ] swarm 최대 8, 4개 역할부터
- [ ] 완료 기준·수정 경로를 프롬프트에 명시
- [ ] 결과는 테스트 + `git diff`로 확인
- [ ] 메모리에 규칙 저장/검색 테스트 (비밀값 제외)
