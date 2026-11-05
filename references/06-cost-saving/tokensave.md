# 클로드 코드 토큰 3배로 오래 쓰는 무료 도구 3개
- 원문: https://lazyowen.com/guides/tokensave
- 도구·주제: Ponytail · Graphify · Headroom (Claude Code) · 비용 절약 / 토큰 절약 (2026-08-06 갱신, STEP 7개 · 약 17분)
- 한 줄 요약: 토큰이 새는 세 지점(AI가 쓰는 코드량, 찾느라 읽는 파일량, 모델에 실제로 보내는 양)을 각각 막는 무료 도구 3개를 함께 설치하고, `headroom savings`로 실제 절감을 확인한다.

## 언제 쓰나
- 클로드 사용량이 며칠 만에 바닥나는 원인이 "많이 써서"가 아니라 안 봐도 될 파일 탐색, 원본 로그 전송, 과한 코드 생성이라고 의심될 때
- 셋은 막는 지점이 달라 기능이 겹치지 않고 같이 켜도 충돌하지 않음. 하나만 깔면 나머지 구간으로 토큰이 계속 샘

## 준비물 / 필요 도구
| 도구 | 설치되는 곳 | 막는 지점 | 링크 |
|---|---|---|---|
| Ponytail | Claude Code 플러그인 | AI가 쓰는 양: 이미 있는 코드부터 쓰게 해 결과물을 짧게 | https://ponytail.dev/ · https://github.com/DietrichGebert/ponytail |
| Graphify | Claude Code 스킬 | AI가 찾느라 읽는 양: 파일 관계 지도를 만들어 넓게 뒤지지 않게 | https://www.graphify.com/ · https://github.com/Graphify-Labs/graphify |
| Headroom | 내 컴퓨터의 로컬 프록시 | 실제로 보내는 양: 모델로 넘어가기 직전 압축 | https://docs.headroomlabs.ai/docs · https://github.com/headroomlabs-ai/headroom · 설치 https://headroom-docs.vercel.app/docs/installation |
- Claude Code(https://claude.com/claude-code, 로그인까지), Node.js LTS(https://nodejs.org/), uv(https://docs.astral.sh/uv/ — 파이썬 프로그램 설치 도구, Graphify·Headroom 설치에만 사용)
- 비용: 도구는 무료. Claude Code 사용 자체는 구독/API 비용
- 용어: 플러그인 사용자 범위(`--scope user`)=모든 프로젝트에서 자동 동작 / 토큰=구독 사용량이 깎이는 글자 단위 / 프록시=내 컴퓨터와 AI 서버 사이에서 오가는 내용을 손보는 중계 프로그램

## 단계별 방법
**Quick Start** — 터미널에 통째로 붙여넣기(세 도구 순서대로 설치)
```bash
claude plugin marketplace add DietrichGebert/ponytail --scope user
claude plugin install ponytail@ponytail --scope user
uv tool install graphifyy && graphify install
uv tool install --python 3.13 "headroom-ai[proxy,mcp]"
```
- 성공 시 세 줄: `✔ Successfully installed plugin: ponytail@ponytail`, `Done. Open your AI coding assistant and type: /graphify .`, `Installed 1 executable: headroom`
- 이후 `claude` 대신 항상:
```bash
headroom wrap claude      # 프록시가 함께 뜨고 Claude Code가 열림
```

**설치·검증 위임 프롬프트 뼈대 (Claude Code)**
- 역할: Ponytail·Graphify·Headroom 설치·연결 검증 담당. 맥락: 미설치일 수 있고 사용량이 빨리 소진되는 상태
- 채울 곳: [OS·셸], [기술 스택], [목표 — 예: 같은 구독으로 더 오래 쓰기]
- 작업 4단계: ① `claude --version`, `node --version`, `uv --version`(uv 없으면 `curl -LsSf https://astral.sh/uv/install.sh | sh`), `claude plugin list`, `graphify --version`, `headroom --version`으로 기설치 확인(있으면 재설치 금지, 상태만 보고) ② 미설치분 설치: Ponytail marketplace add→install(`--scope user`), `uv tool install graphifyy`+`graphify install`, `uv tool install --python 3.13 "headroom-ai[proxy,mcp]"` ③ 검증: `claude plugin list`에 ponytail@ponytail enabled, 두 버전 출력, `headroom proxy --port 8787`을 백그라운드로 띄워 `headroom doctor`의 proxy가 pass인지 확인 후 프록시 종료 ④ 세 도구의 역할·사용법을 5줄 이내 설명
- 제약: 기존 설정·프로젝트 파일 덮어쓰기/삭제 금지, `npm install -g` 금지, `.env`·키 파일 읽기/출력 금지, 프록시는 띄운 뒤 반드시 종료
- 출력/검증: 실행 명령, 세 도구 버전, 새 파일·폴더, 남은 오류. 하나라도 실패하면 완료 보고 금지

**STEP 1. 준비물 확인 (2분)**
```bash
claude --version
node --version
uv --version
```
- 세 줄 모두 숫자가 나오면 준비 완료. `command not found`만 설치(uv는 위 curl 스크립트 후 터미널을 완전히 닫았다 다시 열어 `uv --version` 재확인)

**STEP 2. 세 도구의 역할 파악 (2분)** — 위 표 참고. 셋 다 켜져 있는지가 설치 순서보다 중요

**STEP 3. Ponytail 설치 (2분)**
```bash
claude plugin marketplace add DietrichGebert/ponytail --scope user     # ✔ Successfully added marketplace: ponytail (declared in user settings)
claude plugin install ponytail@ponytail --scope user                    # ✔ Successfully installed plugin: ponytail@ponytail (scope: user)
```
- Claude Code 안에서 하려면 `/plugin marketplace add DietrichGebert/ponytail`과 `/plugin install ponytail@ponytail`을 각각 따로 입력(한 번에 보내면 설치 안 됨)
- 열려 있던 세션은 재시작해야 반영

**STEP 4. Graphify 설치 (3분)** — 패키지명 `graphifyy`(y 두 개), 실행 명령은 `graphify`
```bash
uv tool install graphifyy
graphify install      # Installed 2 executables: graphify, graphify-mcp / Done. Open your AI coding assistant and type: /graphify .
uv tool update-shell  # graphify: command not found 일 때 실행 후 터미널 재시작
```
- 지도는 프로젝트마다 한 번: 작업 폴더에서 Claude Code를 열고 (터미널이 아니라 Claude Code 안에서)
```
/graphify .
```
  → 프로젝트에 `graphify-out/`(graph.json, GRAPH_REPORT.md, graph.html) 생성
- 코드를 고친 뒤 갱신(바뀐 파일만 재독):
```
/graphify . --update
```

**STEP 5. Headroom 설치 (3분)**
```bash
uv tool install --python 3.13 "headroom-ai[proxy,mcp]"    # Installed 1 executable: headroom
headroom --version                                         # 예: headroom, version 0.33.0
headroom wrap claude                                       # 앞으로 claude 대신 사용
headroom wrap claude --resume                              # 기존 옵션은 뒤에 그대로 (예: 이전 대화 이어가기)
```
- 대괄호 `[proxy,mcp]`를 빼면 명령은 깔리지만 프록시를 켤 때 `Proxy dependencies not installed` 오류 → 대괄호 포함해 재실행

**STEP 6. 진짜 적용됐는지 확인 (3분)** — 설치 로그가 좋아도 프록시를 거치지 않는 경우가 많음
```bash
headroom doctor       # proxy 항목이 ✓ pass, running at http://127.0.0.1:8787 이면 정상. ✗ fail이면 headroom wrap claude 로 다시 열기
headroom savings      # 예: Today 49.2% saved 3,080 / 6,260 tokens. 계속 no tokens saved yet이면 프록시 없이 claude를 열고 있는 것
claude plugin list    # ponytail@ponytail 이 Status: ✔ enabled
```
- doctor의 savings 항목 `warn`은 고장이 아님: 아직 요청을 한 번도 안 보냈다는 뜻이라 작업 몇 번 후 재확인

**STEP 7. 절감 수치 이해 (2분)** — 모두 조건부 수치, 무조건 보장은 없음
- Ponytail: 기능 작업 12개 × Haiku 4.5 × 4회 공식 측정, 코드 줄 수 -54%, 입력 토큰 -22%, 비용 -20%, 시간 -27%. 이미 짧은 코드는 거의 안 줄어듦
- Graphify: 파일 52개 코퍼스에서 질문당 약 71.5배, 파일 4개 5.4배, 파일 6개 소형 프로젝트는 약 1배(작은 프로젝트는 원래 전체가 들어가서 이득 없음)
- Headroom: 코드 검색(100건) 92%, 장애 로그 분석 92%, 이슈 분류 73%, 코드베이스 탐색 47% 절감. 표준 정확도 평가에서 정답률은 유지되거나 소폭 상승
- 내 프로젝트의 실제 절감은 `headroom savings`로만 정확히 확인. 같은 작업을 전후로 비교

## 핵심 팁 · 주의사항
- 하나만 설치하면 다른 구간이 샘. Ponytail만 있으면 코드는 짧아져도 파일은 넓게 뒤지고, Graphify까지 있어도 명령 결과·로그는 원본으로 전송됨
- 마지막 확인 단계를 건너뛰면 설치했다고 착각함 → `headroom savings`에 숫자가 쌓이는지가 유일한 증거
- 효과는 보장되지 않음(작업·모델·프로젝트 크기에 따라 다름)
- `npm install -g`가 아니라 `uv tool install`/플러그인 방식. Headroom은 `claude` 대신 `headroom wrap claude`로 실행해야 적용

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| `command not found: uv` | uv 미설치 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` 후 터미널 재시작 |
| `graphify: command not found` | 실행 경로 미등록 | `uv tool update-shell` 후 터미널 재시작 |
| `Proxy dependencies not installed` | 대괄호 없이 설치 | `uv tool install --python 3.13 "headroom-ai[proxy,mcp]"` 재실행 |
| doctor의 proxy가 fail | 프록시 꺼짐 | `headroom wrap claude`로 열기 |
| savings가 계속 비어 있음 | 프록시를 거치지 않음 | `claude` 대신 `headroom wrap claude` |
| 플러그인이 현재 세션에 안 보임 | 설치 전부터 열린 세션 | Claude Code 완전 종료 후 재실행 |
| `/graphify`를 못 알아들음 | 스킬 미등록 | `graphify install` 후 Claude Code 재시작 |
| 쿼리 결과가 엉뚱함 | 지도가 오래됨 | `/graphify . --update` |

## 바로 쓰는 체크리스트
- [ ] `claude`, `node`, `uv` 버전 확인(없으면 설치)
- [ ] Ponytail 설치, `claude plugin list`에서 enabled
- [ ] Graphify 설치, 프로젝트에서 `/graphify .` 실행(코드 변경 후 `--update`)
- [ ] Headroom 설치(`[proxy,mcp]` 포함), `headroom wrap claude`로 실행
- [ ] `headroom doctor` proxy pass, `headroom savings` 숫자 누적 확인
- [ ] 같은 작업을 전후로 비교해 실제 절감 측정
