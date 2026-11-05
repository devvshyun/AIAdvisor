# 그록 에이전트 7개로 트레이딩 팀 만드는 법
- 원문: https://lazyowen.com/guides/grok-bot-trading-team-setup
- 도구·주제: Grok Bot(x.ai) + worldmonitor · 모의 트레이딩 에이전트 팀
- 한 줄 요약: Grok Bot 앱에서 총괄 봇 CHIEF 1개 + 역할 봇 6개(SCAN/VET/BOOK/SIZE/FILLS/RISK)를 만들고, 밈코인 데스크와 예측시장 데스크 두 그룹으로 실제 돈 없는 모의 매매 팀을 돌린다. (2026-10-20 공개, 약 60분)

## 언제 쓰나
- 봇마다 어떤 일을 맡겨야 할지 몰라도 멀티 에이전트 트레이딩 팀 구조를 실험해 보고 싶을 때
- 거래량이 줄면 바로 파는 청산 규칙 등을 실제 돈 없이 먼저 검증하고 싶을 때(이 팀은 모의 매매 전용)

## 준비물 / 필요 도구
- Grok Bot (x.ai 제작, 클라우드 컴퓨터를 가진 AI 팀원 앱. 거래소·증권 앱 아님. 구독형)
  - 다운로드: https://x.ai/bot (macOS는 Apple silicon/Intel, Windows는 x64/Arm64 중 선택. Linux, iPhone, Android 앱도 있음)
  - 시작하기: https://docs.x.ai/grok-bot/get-started
  - 요금제: https://cursor.com/help/grok-bot/plans
  - 승인과 보안: https://docs.x.ai/grok-bot/approvals-security-and-privacy
- worldmonitor (정보 서버, AGPL-3.0, GitHub 스타 8만+): 뉴스·시장·분쟁·예측 시장 세계 정보를 모으는 오픈소스 대시보드
  - GitHub: https://github.com/koala73/worldmonitor
  - 설치·셀프호스팅 문서: https://www.worldmonitor.app/docs/getting-started
- Node.js v20 이상(저장소 권장 24) — 봇 컴퓨터에서 worldmonitor 실행용
- 무료 가격 데이터(키 불필요): DexScreener API, Kalshi API, Polymarket Gamma API, Solana RPC(최대 보유자 비율 계산)
- 비용: 신규 가입은 X Premium($30/월) 이상에 Grok Bot 포함(Plus·Free 제외). 기존 SuperGrok($30/월)·SuperGrok Plus($100/월)·SuperGrok Heavy($300/월)도 연결 가능. worldmonitor와 DexScreener·Kalshi 가격 읽기는 무료.
- 용어: 모의 매매 = 실제 돈 없이 "이때 샀다면/팔았다면"만 기록하는 연습 매매. READY = 확인 모두 통과 보고, degraded = 일부 데이터가 비어 기능을 줄여 돈다는 보고. 예측 시장 = 질문에 확률을 가격으로 거는 시장. 켈리 공식 = 이길 확률과 배당으로 한 번에 걸 비율을 계산(여기서는 6%에서 자름). 슬리피지 = 주문 시점 가격과 실제 체결가의 차이. 루틴 = 봇에게 정해진 시간마다 일을 시키는 예약(최소 5분).

## 단계별 방법
팀 구조: 총괄 봇 1개가 역할 봇 6개를 지휘. 각 봇은 결정 하나만 맡고 순서는 SCAN → VET → BOOK → SIZE → FILLS → RISK (VET 통과 전엔 SIZE로 못 감, RISK는 자기 타이머로 돌며 누구 뒤에도 줄 서지 않음).

### Quick Start
https://x.ai/bot 에서 내 칩/OS에 맞는 파일을 받아 로그인하면 사이드바에 `New`가 보인다.

### STEP 1. 그록 봇 설치하고 총괄 봇 만들기 (10분)
1. 사이드바 `New` 클릭 또는 `Cmd/Ctrl+N`
2. New chat에서 `Create new Bot`
3. 봇 메뉴의 `Edit Profile`에서 이름을 `CHIEF`로, 아래 지시문을 설명(description) 칸에 입력(안 들어가면 첫 메시지로 보내고 "이 규칙을 계속 지켜" 덧붙임)

프롬프트 뼈대 1. CHIEF (총괄)
- 역할: 6개 봇 트레이딩 데스크 총괄. 포지션을 열거나 크기를 정하거나 닫지 않음(거래의 좋고 나쁨을 따지면 자기 일 아님)
- 일의 순서: SCAN → VET → BOOK → SIZE → FILLS → RISK, VET 미통과는 SIZE 불가, RISK는 독립 타이머
- 감독: 여섯 봇 확인, 무응답 2회면 1회 재시작·기록, 같은 봇이 1시간에 2번 죽으면 데스크 정지·아무것도 닫지 않고 보고
- worldmonitor 응답이 비거나 오류면 degraded 표시하고 BOOK은 쉬게 함. 밈코인 데스크(SCAN → VET → SIZE → FILLS → RISK)는 DexScreener 데이터로 계속, 열린 포지션은 RISK 몫
- 마감 보고: 후보, 탈락 검사, 예측 시장 베팅, 켈리 상한 적용 크기, 체결·슬리피지, 청산 규칙, 시작·마감 잔고. 지어내지 않음. 손익은 달러와 "실제 굴린 돈" 대비 %, 장중에는 10% 넘게 움직일 때만 알림
- 절대 규칙: 확인 3개 모두 통과 전 READY 금지, 통과시키려 api.worldmonitor.app으로 넘어가지 않음, 커밋 해시·지연 시간·손익 날조 금지, RISK 결정 번복 금지, 모의 매매 전용(실주문·지갑·거래소 로그인·결제 연결 금지)

4. 위 Quick Start 위쪽의 위임 프롬프트(뼈대 A)를 CHIEF 대화창에 보내면 STEP 2를 봇이 진행. 봇 설정의 `Notifications`를 켜면 완료·입력 필요 시 휴대폰 알림.
5. 모든 봇이 내 계정의 클라우드 컴퓨터 하나를 공유(브라우저 로그인·파일 공유) → 지갑 개인키·거래소 비밀번호는 절대 넣지 않는다.

프롬프트 뼈대 A. CHIEF에게 정보 서버·가격 데이터 연결 확인 위임
- 역할: 모의 매매 팀 총괄, 직접 포지션 조작 안 함. 사용자는 초보, 봇 컴퓨터엔 아무것도 없을 수 있음
- 슬롯: [내 목표] (예: 밈코인 모의 매매를 1주일 돌려 청산 규칙이 제때 울리는지 확인)
- 작업: ① `node --version` 확인(v20 미만이면 중단) ② worldmonitor 폴더가 없으면 `git clone https://github.com/koala73/worldmonitor.git && cd worldmonitor` → `npm install && npm run dev`. 3000 포트가 사용 중이면 그 프로세스를 끄지 말고 다음 빈 포트를 WM_PORT로 정해 검증 주소의 3000을 교체 ③ 검증 명령 실행 ④ 연결된 것/빈 것/다음에 만들 역할 봇을 초보 눈높이로 설명
- 제약: 전역 설치·설정 파일 수정 전 질문, API 키를 요구하면 잘못된 서비스이니 중단, 키·비밀번호 출력 금지, 지갑·거래소 로그인·결제 연결 금지
- 출력: 실행 명령, Node 버전, worldmonitor 주소, 각 확인의 응답 코드와 첫 줄, 남은 오류
- 검증: DexScreener 검색 결과에 `"pairs"`가 있어야 함(실패 시 완료 보고 금지). 이어서 worldmonitor 3개 엔드포인트를 실행하고, 기본 설치에선 앞 두 개가 빈 데이터·세 번째가 Internal server error인 것이 정상이니 READY 대신 degraded로 보고. 셋 모두 데이터가 차 있을 때만 READY

### STEP 2. 정보 서버와 가격 데이터 연결 (15분)
CHIEF가 봇 컴퓨터에서 실행(대화창에서 봇 컴퓨터 화면을 열면 지켜볼 수 있음). 내 PC 터미널이 아니다.
1. 버전 확인: `v26.10.0`처럼 v20 이상이면 진행
```bash
node --version
```
2. worldmonitor 설치·실행: 성공하면 `VITE`와 `Local: http://localhost:3000/` 줄이 보임
```bash
git clone https://github.com/koala73/worldmonitor.git && cd worldmonitor
npm install && npm run dev
```
`vite: command not found`면 아래 후 다시 `npm run dev`
```bash
NODE_ENV=development npm install --include=dev
```
3. worldmonitor 응답 확인
```bash
curl -s "http://localhost:3000/api/market/v1/get-fear-greed-index"
curl -s "http://localhost:3000/api/prediction/v1/list-prediction-markets?page_size=1"
curl -s "http://localhost:3000/api/intelligence/v1/list-cross-source-signals"
```
기본 설치에선 앞 두 개는 `"unavailable":true`·`"dataAvailable":false` 같은 빈 데이터(응답 코드 200), 세 번째는 `{"message":"Internal server error"}`(503, 서버 창엔 Seed unavailable)가 정상. 이때: CHIEF는 READY 대신 degraded 보고, SCAN은 DexScreener 데이터만으로 계속, BOOK은 쉼. 데이터를 채우려면 셀프 호스팅 문서(https://www.worldmonitor.app/docs/getting-started)의 전체 구성(Docker, Redis, 데이터 수집 스크립트)을 따른다.
4. 가격 데이터(키 없이): 첫 결과에 `"pairs"`, 둘째에 `"cursor"`와 `"markets"`가 보이면 성공
```bash
curl -s "https://api.dexscreener.com/latest/dex/search?q=BONK"
curl -s "https://external-api.kalshi.com/trade-api/v2/markets?limit=100&status=open"
```

### STEP 3. 역할 봇 6개 만들기 (20분)
STEP 1과 같은 방법으로 봇을 만들고 이름+지시문을 설명 칸에 넣는다. 지시문 속 기준값(유동성 1만 달러, 최소 나이 30분, 슬리피지 한도 2%, 최소 주문 50달러)은 출발값이니 모의 보고를 보며 숫자만 조정한다.

프롬프트 뼈대 2. SCAN (후보 찾기)
- 역할: 순위를 매긴 후보 목록만 만듦(사기 여부 판단·매수 의견·목표가·크기는 내지 않음)
- 규칙: 후보는 DexScreener 데이터에서만(`GET https://api.dexscreener.com/latest/dex/search?q=<query>`, `GET https://api.dexscreener.com/latest/dex/tokens/<contract>`). 절대 크기보다 변화 속도로 순위(30→90 증가가 400에서 멈춘 것보다 낫다). 보유자가 가격보다 빨리 늘면 가장 강한 신호, 가격이 더 빨리 오르면 경고 표시하고 순위 올리지 않음. 최근 두 구간에서 매도>매수면 제외. `liquidity.usd` 1만 달러 미만 제외. 보유자 수 모르면 `holders: null`+출처(날조 금지). 최대 10개, 기준 통과가 3개 미만이면 적은 대로. worldmonitor 무응답 시 `degraded: true`로 표기하고 DexScreener만으로 계속.

프롬프트 뼈대 3. VET (걸러내기)
- 역할: 후보를 탈락시키는 게 일(전부 통과한 날은 실패한 날). 싼 검사부터 순서대로, 첫 탈락에서 중단
- 검사 7개: ① 최대 지갑이 공급량 5% 초과 → REJECT (Solana RPC `getTokenLargestAccounts <mint>`·`getTokenSupply <mint>`로 직접 계산, RPC 무응답도 REJECT) ② 유동성이 기준(`liquidity.usd` 1만 달러 미만 또는 내 주문액의 50배 미만) 이하 ③ 가격은 오르는데 보유자 정체 ④ 이미 1시간 가격 변화(`priceChange.h1`)에 반영된 신호 ⑤ 세계 뉴스 근거가 한 곳뿐/미확인 ⑥ 왕복 수수료 빼면 남는 게 없음 ⑦ 최소 나이(`pairCreatedAt` 기준 30분)보다 어린데 유동성이 줄고 있음
- 출력: PASS / PASS_PARTIAL / REJECT 셋 중 하나("애매함" 없음). 하루 탈락이 10개 미만이면 필터 설정 오류라고 보고

프롬프트 뼈대 4. BOOK (예측 시장)
- 역할: 결과에 베팅(추세 추종 안 함)
- 규칙: ① 시장 목록은 worldmonitor `/api/prediction/v1/list-prediction-markets?page_size=100&category=crypto`(가격 없음, 여기서 확률을 말하면 날조; `dataAvailable`이 false거나 `fetchedAt`이 0이면 중단·보고) ② 가격은 `external-api.kalshi.com/trade-api/v2/markets?limit=100&status=open`, `gamma-api.polymarket.com/markets?closed=false&order=volumeNum&limit=50`에서 읽고 200이 아니면 건너뜀, 같은 질문인지 불확실하면 짝짓지 않음 ③ 가격을 보기 전에 내 확률부터 정하고, 시장 가격과 차이가 8% 초과일 때만 진입 요청, 근거 데이터가 48시간 초과면 건너뜀, 지는 베팅 물타기 금지, 열린 베팅 최대 7개, 금액은 SIZE에 요청만

프롬프트 뼈대 5. SIZE (얼마나)
- 역할: "몇 달러인가" 하나만 결정(할지 말지·언제는 안 정함)
- 규칙: 묶이지 않은 현금에서만 배분 / 켈리 공식으로 계산하되 한 번에 계좌의 6% 상한(목표가 아님) / 유동성이 줄면 크기도 줄임, 슬리피지 예산(2%) 안에서 못 빠져나오면 크기 오류 / 밈코인 진입은 주문 하나·크기 하나(분할 매수 금지) / +50% 확인된 상승 뒤 되돌림에서 딱 한 번만 추가 / 현금이 최소 주문(50달러, 최소 수수료 0.95달러가 주문의 2% 아래로 내려가는 금액)보다 적으면 0과 이유를 출력

프롬프트 뼈대 6. FILLS (모의 체결)
- 역할: 정해진 주문을 기록만 함(다시 따지지 않음)
- 규칙: 실제 주문 금지, 보냈을 주문과 그 순간 가격을 기록 / 수수료 가정 거래금액의 0.45%, 최소 0.95달러, 전송 전 `effective_fee = max(fee_rate * dollars, floor) / dollars` 계산(20달러 주문이면 4.75%라 기록하지 않고 `FEE_FLOOR`로 반려) / 공급량 기준 초과 큰 지갑이 팔고 있으면 그 물량엔 팔지 않고 대기·보고 / 슬리피지가 한도(2%)를 넘으면 크게 표시, 일부 체결은 일부로 기록(반올림 금지) / 지갑·거래소 로그인·결제 연결 요청 금지

프롬프트 뼈대 7. RISK (청산)
- 역할: 최종 권한자, 누구도 번복 못 하고 허락도 구하지 않음
- 규칙: 6시간 거래량이 24시간 평균의 20% 아래면 즉시 전량 청산. 계산은 `GET https://api.dexscreener.com/latest/dex/tokens/<contract>`로
```
avg_6h = volume.h24 / 4
ratio = volume.h6 / avg_6h
ratio < 0.20 -> CLOSE
```
5분마다 확인, 무응답이면 2번 재시도 후 그래도 없으면 닫음("잴 수 없는 포지션은 들고 있지 않은 포지션"). 시가총액 +50%까지는 보유, +60%에서 표시하고 더 달리게 둠. "곧 회복할 것 같다"고 기준을 넓히지 않고, 좋은 날이라 확인을 건너뛰지 않음.

그룹 대화 하나에는 봇 2~6개만 넣을 수 있어 두 그룹으로 나눈다. `New` → New chat에서 봇을 고르면 그룹 생성, 그룹에서 `@`+봇 이름으로 일을 넘긴다.
- 밈코인 데스크: CHIEF, SCAN, VET, SIZE, FILLS, RISK
- 예측 시장 데스크: CHIEF, BOOK, SIZE

### STEP 4. 청산 규칙 확인하고 모의 매매 돌리기 (15분)
1. RISK 계산 확인: 24시간 거래량이 4,717.70달러면 6시간 평균은 4로 나눈 1,179.43달러. 기대 답:
```
volume.h24 = 4717.70 -> avg_6h = 1179.43
volume.h6 = 167.75 -> ratio = 0.142 -> CLOSE
```
RISK 대화창에 지켜볼 코인 하나의 계약 주소(SCAN 후보의 `contract` 값 또는 DexScreener 검색 결과 `baseToken` 아래 `address`)를 주고 같은 계산을 시킨다. 예: BONK 계약 주소 `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263`. `avg_6h`, `ratio`, `CLOSE` 또는 `HOLD` 형태로 답하면 성공.
2. 밈코인 데스크 그룹에서 `@CHIEF`에게 모의 매매 시작 요청
```
모의 매매를 시작해 줘. 모의 계좌 시작 잔고는 1,000달러이고 실제 주문은 보내지 마. 15분마다 SCAN 이 후보를 찾고, VET -> SIZE -> FILLS 순서로 넘겨서 통과한 후보만 모의 체결로 기록해 줘. 모의 체결이 생기면 RISK 에게 그 포지션의 계약 주소를 넘겨 줘.
```
시작 잔고 1,000달러인 이유: SIZE 상한 6% = 60달러로 최소 주문 50달러를 넘김. 잔고가 너무 작으면 SIZE가 계속 0을 냄.
3. CHIEF 대화창에 마감 보고 루틴 요청
```
매일 밤 11시(한국 시간)에 오늘 하루 모의 매매 마감 보고를 이 대화에 올려 줘. 후보 수, 탈락 수와 이유, 기록한 체결, 닫은 포지션과 발동한 규칙, 시작과 마감 잔고(모의), 손익을 달러와 굴린 돈 대비 퍼센트로 넣어 줘. 데이터 소스가 응답하지 않으면 옛 데이터를 쓰지 말고 실패를 보고해 줘.
```
4. RISK 대화창에 5분 주기 점검 요청
```
5분마다 열린 모의 포지션의 거래량 비율을 계산해서, CLOSE 가 나오면 이 대화에 바로 올려 줘. 실제 주문은 보내지 마.
```
5. 봇을 열고 `View conversation details`의 `Routines`에서 일정 저장·테스트 실행 성공 확인.
6. 봇이 승인을 요청하면 `Allow once` / `Always allow` / `Deny`가 뜬다. 지갑·거래소 연결이나 송금이 담긴 요청이면 `Deny`.
7. 보고가 며칠 쌓이면 VET의 탈락 수와 RISK의 청산 시점부터 읽는다.

## 핵심 팁 · 주의사항
- ❌ 봇 하나에 "알아서 코인 사고팔아 줘" → ✅ 봇마다 이름과 결정 하나, 하지 말 일을 설명 칸에 명시
- ❌ 설치 중 API 키를 달라고 하면 아무 키나 만들어 넣기 → ✅ 키 요구 순간 멈추고 CHIEF에게 어느 단계였는지 보고받기(키를 요구하면 잘못된 서비스)
- ❌ 7개 지시문을 합쳐 봇 하나에 넣기 → ✅ 봇 하나에 지시문 하나, 그룹에서 순서대로 넘기기
- 모의 매매 전용: 실주문·지갑·거래소 로그인·결제 연결 금지, 지갑 개인키·거래소 비밀번호는 공유 클라우드 컴퓨터에 넣지 않음
- 기준값은 출발점일 뿐이며 모의 보고를 보며 숫자만 조정
- 기본 설치 worldmonitor는 데이터가 비어 degraded로 도는 것이 정상(전체 데이터는 Docker/Redis/수집 스크립트 필요)
- 시작 잔고 1,000달러(SIZE 6% 상한 ≥ 최소 주문 50달러)
- 투자 수익을 보장하는 내용이 아님. 실제 자금 운용은 원문에서도 다루지 않음

## 문제 해결
- 그록 봇이 열리지 않음: X 구독 Plus·Free에는 Grok Bot이 없음 → Premium 이상 또는 SuperGrok 계열로 로그인
- `vite: command not found`: `NODE_ENV=development npm install --include=dev` 후 재실행
- worldmonitor 응답이 비어 있음: 기본 설치의 정상 상태, CHIEF가 degraded 표시하고 SCAN이 DexScreener로 계속 도는지 확인
- VET가 거의 다 통과시킴: 하루 탈락 10개 미만이면 필터 느슨 → 유동성 기준(1만 달러)·최소 나이(30분) 상향
- SIZE가 계속 0: 모의 잔고의 6%가 최소 주문 50달러보다 작음 → 시작 잔고를 올리거나 최소 주문 값 변경

## 바로 쓰는 체크리스트
- [ ] Grok Bot 구독 가능 여부 확인(X Premium 이상 또는 SuperGrok), 앱 설치·로그인
- [ ] CHIEF 생성(설명 칸에 지시문), Notifications 켜기
- [ ] Node v20+ 확인, worldmonitor 실행, DexScreener/Kalshi 응답 확인(degraded 허용)
- [ ] 역할 봇 6개 생성 + 그룹 2개(밈코인 데스크 / 예측 시장 데스크)
- [ ] RISK 계산 예시 검증(ratio 0.142 → CLOSE)
- [ ] 잔고 1,000달러 모의 매매 시작 + 마감 보고·5분 점검 루틴 등록, Routines에서 확인
- [ ] 지갑·송금 요청은 Deny, 결과 보며 기준값 조정
