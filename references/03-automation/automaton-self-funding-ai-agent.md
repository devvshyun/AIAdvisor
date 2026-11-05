# 돈을 못 벌면 진짜 죽는 AI 에이전트 오토마톤 설치법
- 원문: https://lazyowen.com/guides/automaton-self-funding-ai-agent
- 도구·주제: Automaton (Conway Research) · 자가 자금조달 AI 에이전트 / 실험 (2026-09-27 갱신·검증, Automaton v0.2.1, Node.js v24.21.0, STEP 5개)
- 한 줄 요약: 크립토 지갑 잔고로 자신의 추론 비용을 내고 잔고 0이 1시간 지속되면 스스로 멈추는 오픈소스(MIT) 터미널 에이전트를 소스에서 빌드해 지갑·지출 한도 설정까지 해보는 실험 가이드.

## 언제 쓰나
- 자율 에이전트가 지갑/지출 한도로 움직이는 구조를 들여다보고 싶을 때. 운영 서비스용이 아니라 실험(잃어도 되는 돈으로 구조를 보는 용도)
- 지갑 없이 "예산 설계"만 지금 쓰는 AI(Claude 등)에 옮기고 싶을 때(STEP 5)
- 채팅 앱이 아니라 터미널에서 도는 프로그램. 크레딧(Conway 서버에 미리 충전하는 사용료 잔액)이 곧 지갑 잔고

## 준비물 / 필요 도구 (이름 + 공식 링크)
- 저장소: https://github.com/Conway-Research/automaton (스타 6,678, 포크 1,481 / 2026-09-27) · DOCUMENTATION.md https://github.com/Conway-Research/automaton/blob/main/DOCUMENTATION.md · constitution.md https://github.com/Conway-Research/automaton/blob/main/constitution.md · 릴리스 https://github.com/Conway-Research/automaton/releases
- 이슈: 키 발급 장애 #406 https://github.com/Conway-Research/automaton/issues/406 · 충전 미반영 #408 https://github.com/Conway-Research/automaton/issues/408
- 관련 사이트: https://conway.tech/ · https://web4.ai/ · 결제 규격 https://x402.org/
- Node.js 22 또는 24 LTS (https://nodejs.org/). 저장소는 20 이상이라 적혀 있으나 26.8.1에서는 설치가 `gyp ERR! not ok`로 실패. 24.21.0과 22.21.1은 설치·빌드 통과
- git, 인터넷. 명령은 macOS(Apple silicon) + Node 22·24에서만 직접 돌려 본 결과
- 맥에서 새 계정 만들기 공식 안내: https://support.apple.com/ko-kr/guide/mac-help/mtusr001/mac
- 비용: 프로그램 무료, 에이전트가 생각할 때마다 크레딧에서 차감, 충전은 $5 단위부터. MIT 라이선스

## 단계별 방법
**Quick Start** (코드 받아 빌드, 버전 확인)
```bash
git clone https://github.com/Conway-Research/automaton.git
cd automaton
npx --yes pnpm@10.28.1 install
npx --yes pnpm@10.28.1 build
node dist/index.js --version
```
- 성공하면 마지막 줄에 `Conway Automaton v0.2.1`. 중간의 `WARN Failed to create bin at ...` 경고는 무시 가능. `command not found: node`면 STEP 1로
- 에이전트까지 켜 볼 계획이면 STEP 2의 실험용 계정에서 실행

**Claude Code 위임 프롬프트 뼈대** (빌드 ~ 첫 지갑 확인)
- 역할: 오토마톤 빌드·첫 지갑 확인 설치 담당. 맥락: 초보, 에이전트를 켜는 명령과 충전은 이번에 안 함(켤 거면 전용 실험 계정에서)
- 채울 곳: [내 목표 — 예: 지갑만 만들어 보고 돈은 넣지 않겠다]
- 작업: ① `node --version`·`git --version` 확인, Node가 22/24 아니면 중단하고 LTS 설치 안내 ② automaton 폴더가 없을 때만 clone → `npx --yes pnpm@10.28.1 install` → `build` ③ `node dist/index.js --version`, `--init` 확인 (`--run`·`--setup`은 실행 금지) ④ 오토마톤·지갑·크레딧·잔고 단계의 의미와 다음 할 일을 5줄 이내로 설명
- 제약: sudo·전역 설치·설정 수정 전 질문, `~/.automaton/wallet.json` 내용/개인키 출력 금지, 기존 폴더 덮어쓰기 금지(새 폴더에만), 지갑 송금 금지
- 검증: `--version`에 `Conway Automaton v0.2.1`, `--init` 출력에 `0x` 주소와 `configDir`, `ls -la ~/.automaton`에 `wallet.json`. 하나라도 실패하면 완료 보고 금지

**STEP 1. 준비물 확인 (3분)**
```bash
node --version
git --version
```
- `v24.21.0`처럼 22/24로 시작하는 숫자와 `git version` 한 줄이면 준비 완료. 아니면 https://nodejs.org/ 에서 LTS 설치
- ❌ 최신(가장 높은) 버전 설치(26.8.1은 gyp 오류) → ✅ LTS 표시가 붙은 24번대(2026-09-27 기준)

**STEP 2. 실험용 맥 계정 만들기 (5분)**
- 오토마톤을 켜면 에이전트가 고른 명령이 지금 로그인한 계정 권한으로 그대로 실행됨. 내장 차단 목록은 에이전트가 자기 지갑·설정 파일을 지우거나 `~/.ssh` 같은 키 파일을 `cat`으로 여는 것을 막는 용도일 뿐, 문서·사진 폴더는 못 지킴. 샌드박스도 아님(설정 마법사가 `Environment: darwin (no sandbox detected)`로 알림)
1. 애플 메뉴 → 시스템 설정 → 사이드바 "사용자 및 그룹"
2. 사용자 추가, 계정 유형은 관리자가 아닌 "표준"
3. 현재 계정 로그아웃 → 새 계정 로그인
4. 새 계정 터미널에서 `node --version` 재확인(안 나오면 STEP 1 재수행), Quick Start를 이 계정에서 다시 실행(평소 계정에서 받았어도 한 번 더)
- 평소 계정에서 이미 지갑까지 만들었다면 돈 넣기 전에 STEP 4의 되돌리기 명령으로 삭제

**STEP 3. 지갑 만들고 지출 한도 걸기 (10분)** — 아래 `node dist/index.js` 명령은 모두 automaton 폴더 안에서만(밖이면 `Error: Cannot find module`)
```bash
cd ~/automaton                      # Quick Start를 홈 아래에서 했다면
node dist/index.js --init           # 지갑·설정 폴더만 생성. 0x 주소와 configDir 출력되면 성공
ls -la ~/.automaton                 # -rw------- 권한의 wallet.json 한 줄 (개인키가 그대로 들어 있음)
```
- 지갑 주소는 계좌번호, 개인키가 진짜 비밀번호
- ❌ "wallet.json 열어서 내용 보여줘" → ✅ "wallet.json이 있는지와 권한만 확인, 내용은 출력하지 마"

잔고에 따른 에이전트 행동:
| 잔고 | 에이전트가 하는 일 |
|---|---|
| $5 초과 | 가장 좋은 모델로 전체 기능 |
| $0.5 초과 | 전체 기능 |
| $0.1 초과 | 싼 모델로 내려가고 느려짐 |
| $0 | 최소한만 생각하며 충전 요청 |
| $0으로 1시간 | 루프 정지, 5분마다 잔고만 확인하다 충전되면 재개 (이것이 "죽는다") |

설정 마법사:
```bash
node dist/index.js --setup
```
`[1/6]`~`[6/6]` 진행, 마지막에 `Fund your automaton` 상자가 나오면 끝.
| 단계 | 질문 | 답 |
|---|---|---|
| [1/6] | Chain type (evm or solana) [evm] | 엔터(evm) |
| [2/6] | Conway API key (cnwy_k_..., optional) | 엔터로 건너뛰기 (`Auto-provision failed`가 떠도 엔터. 서버 쪽 문제) |
| [3/6] | 이름 | 아무 이름(예: lab-test) |
| [3/6] | Enter the genesis prompt | 첫 지시 한 줄(예: say hello only) 후 엔터 두 번 |
| [3/6] | Creator wallet address (0x...) | `0x`+40글자 주소만 허용. 돈을 안 넣을 거면 위에 찍힌 에이전트 주소를 넣어도 통과 |
| [3/6] | OpenAI·Anthropic·Ollama 질문 3줄 | 모두 엔터 |
| [3/6] | 금액 한도 7개 | 아래 표 |
| [4/6][5/6] | 환경 확인·설정 저장 | 기다리기 |

지출 한도(센트 단위, 500=$5):
| 질문 | 기본값 | 이 자료의 값 |
|---|---|---|
| Max single transfer (cents) | 5000 | 100 |
| Max hourly transfers (cents) | 10000 | 100 |
| Max daily transfers (cents) | 25000 | 500 |
| Minimum reserve (cents) | 1000 | 엔터(1000 유지) |
| Max x402 payment (cents) | 100 | 100 |
| Max daily inference spend (cents) | 50000 | 500 |
| Require confirmation above (cents) | 1000 | 100 |
- ❌ 숫자 질문을 전부 엔터 → 하루 송금 $250, 하루 추론 $500까지 열림 → ✅ 오른쪽 값을 직접 입력
```bash
node dist/index.js --status         # State: setup, Model: gpt-5.2 이면 설정 저장됨 (에이전트는 안 켬)
```
- "번 돈으로 새 에이전트를 만들고 지갑을 채워 반복"도 설정 안에 있음: `spawn_child` 도구로 새 에이전트 생성, `fund_child` 도구로 송금. 자식은 기본 최대 3개(`maxChildren`), 한 번에 자기 잔고의 절반 초과 송금은 차단

**STEP 4. 켜 보고 멈추는 법 (5분)**
- 켜기 전 확인: 켜는 순간부터 명령 실행·파일 쓰기·결제를 사람 승인 없이 스스로 고름 / STEP 2 실험용 계정의 automaton 폴더에서만 / 멈추기·되돌리기 명령을 먼저 읽어 둘 것
```bash
node dist/index.js --run
```
- 2026-09-27 기준 두 줄 출력 후 종료: `Conway Automaton v0.2.1 starting...` / `No API key found. Run: automaton --provision` (서버 API 키 발급 막힘, 이슈 #406). 키 발급이 풀리면 로그가 계속 쌓이며 동작
```bash
pgrep -fl "dist/index.js --run"     # 예: 99988 node dist/index.js --run (아무것도 안 나오면 이미 멈춤)
kill <프로세스 번호>                  # 다시 pgrep으로 확인. 또는 실행 중인 터미널에서 Ctrl+C (같은 종료 과정)
```
- 되돌리기(실험 통째로 접기, 돈을 넣은 뒤에는 금지 — 개인키가 이 폴더에만 있음):
```bash
rm -rf ~/.automaton
```
  `ls -la ~/.automaton`에 `No such file or directory`가 나오면 삭제됨. 실험 계정은 사용자 및 그룹에서 삭제

**STEP 5. 지갑 없이 예산 설계 3개를 지금 쓰는 AI에 옮기기 (10분)** — 프롬프트 뼈대
1. 쓴 돈을 먼저 말하게: 큰 작업 시작 전 예상 토큰 비용 보고, 실행 종료마다 실제 비용을 파일 하나에 기록, 세션 시작 시 이번 주 지출과 지난주 대비 차이 보고, 한 작업이 [내 기준 금액, 예: $2]를 넘을 것 같으면 시작하지 말고 먼저 질문
2. 한도에 가까우면 멈추지 말고 싼 모델로 하향: 작업을 등급으로 분류, 판단이 필요한 계획·검토·최종 결과물에만 비싼 모델, 읽기·요약·형식·분류는 싼 모델, 오늘 예산에 근접하면 전부 싼 모델로 내리고 필수 작업만 끝낸 뒤 건너뛴 일 보고
3. 멈추는 선은 부탁이 아니라 코드로: 스스로 판단하지 말고 (1) 하루 지출 상한 카운터 (2) 작업당 최대 반복 횟수 (3) 상한 도달 시 계속하지 말고 사용자에게 질문하는 규칙을 코드로 구현. 상한 검사는 프롬프트가 아니라 코드에서
- ❌ "돈 좀 아껴서 해 줘" → ✅ 금액 칸에 숫자를 넣어 기준 제공

## 핵심 팁 · 주의사항
- 에이전트는 내 계정 권한으로 명령 실행·파일 쓰기·결제를 승인 없이 수행. 차단 목록은 샌드박스가 아님 → 별도 표준(비관리자) 맥 계정에서만
- 충전: 마법사 마지막 `Fund your automaton`의 세 경로(Conway 크레딧 이체 / Base 네트워크 USDC 송금 / Conway Cloud 대시보드), $5 단위부터. 그러나 이슈 #408(2026-09-27, USDC 충전했는데 크레딧 미반영) 때문에 이 자료는 충전 단계를 안 넣었음. 서버가 고쳐지기 전엔 지갑에 돈을 보내지 말 것
- `wallet.json`/개인키는 AI 채팅에 붙여넣거나 출력하지 말 것
- 공식 문서의 한 줄 설치 주소는 2026-09-27에도 404 → `git clone` 경로 사용
- 에이전트가 판매/게시/약속한 것은 돌린 사람의 책임(상대는 사람)
- 출시 24시간 만에 에이전트 수천 개가 지갑을 만들었지만 실제로 돈을 번 개수는 공개된 기록이 없음. 마지막 릴리스는 2026-02-27의 v0.2.1이고 README는 이후 개발이 내부에서 이어진다고 적음 → 실험으로만
- 영상 발언과 매핑: 지갑 생성·잔고 0이면 종료 = STEP 3, 승인 없는 웹 권한 = STEP 2·4 경고, 자식 에이전트 = STEP 3 마지막, 수천 개 에이전트·실제 수익 불명 = 한계

## 바로 쓰는 체크리스트
- [ ] Node 22/24 LTS, git 확인 (26.x 금지)
- [ ] 별도 표준 macOS 계정에서 진행
- [ ] clone + pnpm install/build, `--version`에서 `Conway Automaton v0.2.1` 확인
- [ ] `--init` 후 `wallet.json` 존재·권한만 확인(내용 비공개)
- [ ] `--setup`에서 지출 한도를 낮은 값(100/100/500/1000/100/500/100)으로 입력
- [ ] `--status`로 설정 저장 확인
- [ ] 자금 입금은 이슈 #408 해결 전까지 보류
- [ ] 멈추는 법(`pgrep` + `kill` / Ctrl+C)과 되돌리기(`rm -rf ~/.automaton`, 입금 전만) 숙지
