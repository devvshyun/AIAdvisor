# 고객 유치만을 위한 클로드 에이전트(하비/Harvey) 세팅하는 법
- 도구·주제: Harvey (ethanplusai/harvey) + Claude Code · 영업 이메일 자동화 / 리드 발굴 (비즈니스, 자동화, 16분 읽기, STEP 5개, 약 28분 실습, 2026-10-23 공개)
- 한 줄 요약: 오픈소스 Harvey를 설치해 내 제품 홈페이지로 학습시키고, 조건에 맞는 업체를 찾아 사이트에서 본 사실로 콜드메일 초안을 쓰고, 내 승인 후 발송·회신 처리를 이어 가게 한다. 영어 메일 기준이라 해외 업체 영업에 적합.

## 언제 쓰나
- 고객 유치는 해야 하는데 어떤 업체에 무슨 말로 연락할지 막막할 때. 제품/서비스를 영문 콜드메일로 소규모 유치하고 싶을 때.
- 하비가 일하는 순서: ① 업종·도시로 업체 목록 수집(기본 소스 무료 지도 데이터) ② 업체 홈페이지·robots.txt·sitemap.xml·팀/채용 페이지를 읽어 사실 수집(모델 호출 없이 무료) ③ 메일 주소 규칙을 찾아 한 주소만 검증, `verified`/`risky`/`guess` 표시 ④ 사이트에서 찾은 사실 하나로 시작하는 3통짜리 메일 시퀀스 작성 ⑤ 답장을 읽고 의도 분류 후 답장 초안을 같은 승인 줄에 올림.
- 신호(signal) = 하비가 업체에서 찾는 사실("온라인 예약 없음", "블로그 멈춤", "구글 광고 집행" 등). 23가지이며 내가 확정하기 전엔 하나도 모으지 않음. 메일은 기본값으로 전부 내 승인을 기다리고 승인 전엔 아무것도 나가지 않음.

## 준비물 / 필요 도구
- Harvey(MIT, GitHub 스타 2,000+, 비공식=Anthropic 공식 아님): https://github.com/ethanplusai/harvey · MS365 연결 https://github.com/ethanplusai/harvey/blob/main/docs/microsoft365.md · 변경 기록 https://github.com/ethanplusai/harvey/blob/main/CHANGELOG.md
- macOS 또는 Linux, Python 3.11+ (자료는 3.13, 맥 기본 3.9는 불가), 로그인된 Claude Code(Pro/Max), 발송용 메일함(Gmail/Microsoft 365/SMTP). 내 컴퓨터에서 도는 프로그램(클라우드 아님).
- 보조 도메인 + Google Workspace(약 월 $7~, https://workspace.google.com/), Google Cloud 콘솔 https://console.cloud.google.com/ 과 Gmail API https://console.cloud.google.com/apis/library/gmail.googleapis.com , 주소 검증 Reoon https://reoon.com/email-verifier (월 600건 무료) 또는 ZeroBounce https://zerobounce.net (월 100건 무료)
- 비용: 메일 작성·답장 판단은 Claude 구독 사용량에서 나감(API 요금 없음). 지도 소스 OpenStreetMap 무료. 도메인 구입비, Workspace, 유료 신호, 검증 키 무료 한도 초과분은 별도. 탐색 비용 상한 기본 $1.00.

## 단계별 방법
### 보조 프롬프트: 설치~연결 확인 위임 (프롬프트 뼈대, Claude Code용)
- 역할: Harvey 설치·연결 확인 담당. 슬롯: [내 상품 사이트 주소와 원하는 고객]. OS·셸·파이썬 버전은 직접 확인.
- 작업: `python3.13 --version`, `claude --version`, git 확인 → 없는 것만 설치(파이썬 3.13이 없으면 먼저 질문), clone + venv + `pip install -e .` → `harvey --help`, `harvey status --check` → 하비의 역할과 다음 단계(상품 학습, 메일함 연결 이유)를 초보자용으로 설명, 상품 학습은 내가 동의할 때만.
- 제약: sudo·전역·셸 설정 수정 전 질문, `.env` 키·대시보드 토큰 출력 금지, 덮어쓰기 금지, 하비 상시 실행·메일 승인 금지. 검증: `harvey --help` 첫 줄 `usage: harvey`, `harvey status --check` Brain 줄에 `Claude CLI isolation flags present`. 실패 시 완료 보고 금지.

### Quick Start. 설치 한 줄
```bash
git clone https://github.com/ethanplusai/harvey.git
cd harvey
python3.13 -m venv .venv && source .venv/bin/activate && pip install -e .
harvey --help
```
성공: `usage: harvey [-h]`로 시작하는 명령 목록과 `Harvey — Autonomous AI Sales Agent. Always Be Closing.`

### STEP 1. 준비물 확인 (3분)
```bash
python3.13 --version
claude --version
```
- 파이썬이 없으면 `brew install python@3.13`. 클로드 코드가 오래됐다면(STEP 2의 `harvey status --check` Brain 줄이 `present`로 끝나지 않으면) `claude update`. 로그인 안 됐다면 `claude`를 한 번 실행해 Pro/Max 계정으로 로그인.

### STEP 2. 하비 설치 (5분)
Quick Start 명령 실행 후:
```bash
harvey status --check
```
- 성공: 맨 아래 `Brain:` 줄에 `Claude CLI isolation flags present`. 같은 화면의 `Postal address: MISSING`은 STEP 5 전까지 정상.
- `command not found: harvey` → `source .venv/bin/activate` 먼저(새 터미널마다 필요).
- 설치가 어려우면 harvey 폴더에서 `claude` 실행 후 첫 메시지 `set up Harvey for me` (저장소 안내 파일이 클로드를 설치 도우미로 바꿔 빠진 것만 채움).

### STEP 3. 내 상품 가르치기 (5분)
```bash
harvey train https://your-company.com
```
- 성공: `harvey.local.yaml`, `skills/product_knowledge.md` 생성/갱신(둘 다 내 컴퓨터에만 남고 GitHub 업로드에서 제외됨). 클로드를 부르므로 구독 사용량이 조금 나감.
- ❌ 상품 소개 없는 블로그 글 주소 ✅ 상품·가격·고객 사례가 이어진 홈페이지 주소
- `open -e harvey.local.yaml`로 `icp:` 아래를 수정(들여쓰기 유지, 어긋나면 설정을 못 읽음):
  - `industries`: 가게가 있는 업종 단어 하나(dentist, lawyer, plumb, hvac)
  - `geography`: 기본 `United States` → `Austin, TX`처럼 도시로 좁히기
- 메일 규칙·예시가 영어 기준이라 해외 업체 영어 영업에 최적.

### STEP 4. 고객 신호 고르고 업체 찾기 (5분)
```bash
harvey signals
```
성공: `Signals — 0 confirmed, 23 awaiting you, 0 off`와 비용 포함 목록.
- ❌ `harvey signals --confirm all` (유료 신호까지 한꺼번에) ✅ 무료 신호만 먼저, 유료(`SERP_RANK` 등)는 필요할 때 이름으로 하나씩
```bash
harvey signals --confirm free
harvey discover --estimate
```
성공: 쿼리 목록과 `Estimated cost: $0.0000 (cap: $1.00)` (0이면 무료 소스).
```bash
harvey discover --limit 5
harvey profile
```
- `discover` 성공: `DISCOVER — 5 results across 1 queries`. `profile` 성공: `Read … sites → … observations (free)`.
- `Nothing to profile.`: 읽을 사이트가 없음 — 무료 지도 데이터는 웹사이트 칸이 빈 경우가 많고 그런 업체엔 `NO_WEBSITE` 신호가 붙음.
- `OpenStreetMap has no category for 'SaaS'`: 업종 단어를 STEP 3의 가게 업종으로 변경.
- `502 Bad Gateway`: 무료 공공 서버 혼잡 → 몇 분 뒤 재실행.
- 더 많은 업체가 필요하면 `harvey discover --providers`로 유료 소스 가격 비교.
- 웹사이트 제작 판매라면 내 상품이 바로 해결하는 신호로: 첫 후보 `NO_WEBSITE`, 그다음 `NO_ONLINE_BOOKING`, `BLOG_STALE`.

### STEP 5. 메일함 연결하고 첫 초안 승인 (10분)
SPF·DKIM·DMARC = 내 도메인의 메일이 진짜임을 증명하는 설정 3가지(없으면 스팸함).
1. 발송용 메일함: 평소 도메인 말고 새 보조 도메인(예: acme.com 대신 getacme.com)을 구입 → Google Workspace 가입·도메인 연결·메일함 생성 → 관리 콘솔 안내대로 SPF·DKIM·DMARC 등록. (본 도메인이 스팸으로 찍히면 평소 메일도 막힘)
2. Gmail API 키: Google Cloud 콘솔에서 새 프로젝트 → Gmail API 사용 설정 → API 및 서비스 → 사용자 인증 정보 → OAuth 클라이언트 ID 만들기, 유형은 맨 위 웹 애플리케이션이 아니라 맨 아래 `데스크톱 앱` → 클라이언트 ID·시크릿 복사.
3. 주소 검증 키: Reoon 또는 ZeroBounce 가입 후 API 키(키가 없으면 주소가 전부 `guess`로 남아 한 통도 안 나감).
4. 값 넣기:
```bash
cp .env.example .env
open -e .env
```
| 준비물 | 넣는 곳 |
|---|---|
| Gmail API 클라이언트 ID·시크릿 | `.env`의 `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET` |
| 주소 검증 키(둘 중 하나) | `.env`의 `REOON_API_KEY` 또는 `ZEROBOUNCE_API_KEY` |
| 내 우편 주소 | `harvey.local.yaml`의 `compliance.postal_address` (`open -e harvey.local.yaml`, `compliance:` 아래 `postal_address: ""` 따옴표 안, 들여쓰기 유지) |
   - `.env`는 숨김 파일 → Finder에서 `Cmd+Shift+.`. 모든 콜드메일 아래에 수신 거부 문장과 이 주소가 붙음. 키는 남에게 보이지 말 것.
5. `.env` 저장 후 로그인·발송 준비 점검:
```bash
harvey gmail auth
harvey warmup
```
   성공: 브라우저 구글 로그인 → 터미널에 `Gmail authorized`. `warmup`은 SPF/DKIM/DMARC, 도메인 나이, 차단 목록을 `[OK]`/`[WARN]`/`[FAIL]`로 점검하고 마지막 `NOT READY` 줄이 고칠 FAIL 개수를 알림. FAIL이 있으면 고친 뒤 2~4주 워밍업 후 발송(첫날부터 많이 보내면 스팸함).
   - 한국 업체 대상: 광고성 메일은 수신자 사전 동의가 필요할 수 있음 → KISA 불법스팸대응센터 https://spam.kisa.or.kr 안내 확인.
6. 대시보드와 하비 켜기:
```bash
harvey dashboard
```
   성공: `Harvey Dashboard running` + 잠금 해제 링크 `http://127.0.0.1:5555/#token=…` (이 링크로 열어야 잠금이 풀림, 토큰 비공개). Today 화면 → 왼쪽 메뉴 `Outbox` 또는 `Needs you`의 `Open the decisions desk`에서 승인, 답장은 `Conversations`.
   새 터미널(harvey 폴더, 가상환경 재활성화)에서 본체 실행:
```bash
cd harvey
source .venv/bin/activate
harvey run
```
   성공: `Harvey is online.` 줄과 활동 기록. 켜 둔 동안 15분마다 답장을 읽고 초안을 써 둠.
   - 상시 가동: 쉬는 시간 기본값 미국 동부 22:00~07:00 → `harvey.local.yaml`의 `usage.quiet_hours`로 줄이고 `caffeinate -i harvey run`으로 실행(노트북 덮개를 닫으면 멈춤). 사용량 상한 `max_daily_claude_percent: 80`(기본)으로 구독 사용량 20%는 내 작업용으로 남김.
7. Outbox에서 한 통씩 읽고 키 하나로 결정: `A` 승인(발송 대기) / `E` 수정 후 승인 / `R` 거절. 초안 옆 `Email` 줄이 `verified`인지, `Signals` 줄에 그 업체에서 찾은 사실이 있는지 확인.
   - 첫 메일은 상품을 팔지 않고 관찰 하나와 질문 하나로 끝나야 정상.
   - ❌ 첫날 `harvey outbox --approve-all` ✅ 첫 문장이 그 업체에서 본 사실인지, 주소가 verified인지 보고 한 통씩 승인
8. 답장 처리: 답장은 Conversations에 쌓이고 하비가 쓴 초안은 Outbox에서 같은 방식으로 승인. 계약서 요구처럼 하비가 안전하게 답할 수 없는 대화는 맨 위로 넘어오니 내 메일함에서 직접 답한 뒤 대화 아래 `Hand back to Harvey` 또는 `Close`. 관심을 보인 답장엔 구체적 시간 2~3개를 제안하는 초안이 나오므로 내 일정과 맞는지 보고 승인.
9. 비상 제어:
```bash
harvey sending pause
harvey sending resume
```
   `pause` 성공: `Sending paused. Nothing will leave the outbox.` 하비 전체 끄기: `harvey run` 창에서 `Ctrl+C`.
10. 튜닝: 메일이 너무 세게 나오면 `skills/email_frameworks.md`, 특정 반론 답이 이상하면 `skills/objection_handling.md`를 수정(다음 실행부터 반영).

## 핵심 팁 · 주의사항
- ⚠️ 스팸 위험: 본 도메인이 아닌 보조 도메인 사용, SPF/DKIM/DMARC 필수, 2~4주 워밍업, 첫 배치는 소량.
- ⚠️ 한국 수신자는 사전 동의 규제 가능성 확인.
- ⚠️ 무료 지도 데이터는 웹사이트 누락이 많아 업종·지역에 따라 결과 차이가 큼.
- ⚠️ 주소 검증 키가 없으면 메일이 하나도 나가지 않음. 무료 한도 초과 시 유료.
- `.env` 키와 대시보드 토큰은 비공개.
- 유료 신호는 하나씩 확정하고 `--confirm all` 금지, 승인도 `--approve-all` 금지.
- 비공식 오픈소스(Anthropic 공식 아님).

## 바로 쓰는 체크리스트
- [ ] Python 3.13, Claude Code 로그인 확인
- [ ] harvey 설치, `harvey status --check` Brain 줄 OK
- [ ] `harvey train <URL>`, `icp`(industries/geography) 수정
- [ ] 무료 신호만 확정 → `discover --estimate` → `--limit 5` → `profile`
- [ ] 보조 도메인 SPF/DKIM/DMARC, Gmail OAuth(데스크톱 앱), 검증 키, `postal_address`
- [ ] `harvey gmail auth`, `harvey warmup` FAIL 해소, 2~4주 워밍업
- [ ] `harvey dashboard` + `harvey run`, 초안은 한 통씩 승인, 필요 시 `harvey sending pause`
