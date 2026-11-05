# 그록 봇 6개 트레이딩 팀, 클로드 코드로 그대로 만드는 법
- 원문: https://lazyowen.com/guides/grok-six-bot-paper-trading-team
- 도구·주제: Claude Code + Grok API(xAI) + DexScreener + Solana RPC · 솔라나 신규 토큰 모의(paper) 트레이딩 봇 (자동화, 코딩, 16분 읽기, STEP 5개, 2026-10-27 공개)
- 한 줄 요약: Claude Code 프롬프트 한 번으로 grok-trader 프로젝트를 만들고, 발굴·뉴스·여론·차트·리스크·결정 6개 봇 지시문으로 후보를 거르고 가상 잔고로만 매매하는 대시보드까지 돌린다. 실제 주문·지갑 연결 없음.

## 언제 쓰나
- 내 돈을 넣기 전에, 판단을 봇 6개로 나눈 Grok 기반 파이프라인을 모의로 실험하고 싶을 때
- 용어: 모의 매매 = 실제 돈 없이 "이때 샀다면"을 가상 잔고로 기록만 하는 연습 매매

## 준비물 / 필요 도구
- Claude Code: https://code.claude.com/docs/en/quickstart (Claude Pro/Max/Team/Enterprise 구독 또는 Console 계정 필요)
- Python 3 (https://www.python.org/downloads/), 터미널(맥 '터미널', 윈도우 PowerShell)
- Grok API: https://docs.x.ai/docs/overview · 키 발급 https://console.x.ai/ (선불 크레딧 충전 후 키 생성) · 모델 grok-4.7 https://docs.x.ai/developers/grok-4-7 · X 검색 https://docs.x.ai/developers/tools/x-search · 요금 https://docs.x.ai/developers/pricing
- DexScreener API: https://docs.dexscreener.com/api/reference (무료)
- Solana RPC: https://solana.com/docs/rpc (공개 RPC 무료, 기본 `https://api.mainnet.solana.com`)
- 비용: grok-4.7 입력 100만 토큰당 $2, 출력 100만 토큰당 $6, 웹 검색 1,000회당 $5, X 검색은 게시물 1,000개당 $5. Grok/Claude Code는 오픈소스 아닌 유료 서비스, 생성된 봇 코드는 내 코드.
- 용어: RPC=솔라나 블록체인에 직접 질문하는 주소(누가 얼마 쥐었나 조회) / 풀=토큰과 다른 코인을 넣어 두고 교환하는 돈 통 / 러그=만든 사람이 유동성을 빼거나 물량을 던져 가격을 0 근처로 만드는 수법 / LP=풀에 돈을 넣었다는 증서 토큰(잠겨 있어야 한 번에 못 뺌) / 슬리피지=주문 순간 가격과 실제 체결 가격 차이

## 봇 6개가 일하는 순서
리스크 1차 검사는 코드가 공짜 데이터로 먼저 돌려 탈락 후보에는 Grok 비용을 쓰지 않음.
1. 발굴: 거래량이 평소보다 튄 새 솔라나 토큰 최대 5개
2. 리스크 1차(코드): 유동성·지갑 집중·발행 권한·동결 권한 검사, 하나라도 걸리면 바로 패스
3. 뉴스: 웹 검색으로 최근 호재·악재·시장 흐름
4. 여론: X 게시물로 상승 기대/하락 걱정/과열 판별
5. 차트: 추세와 진입가·손절가·목표가 사전 결정
6. 리스크 2차: 비중을 잔고 2% 이내로 줄이거나 거절
7. 결정: 매수/대기/패스 중 하나 + 이유 기록

| 봇 | 보는 데이터 | 내는 것 |
|---|---|---|
| 1 발굴 | DexScreener 새 토큰 목록·풀 데이터 | 후보 최대 5개와 이유 |
| 2 뉴스 | Grok 웹 검색 | 호재·악재·시장 흐름과 출처 |
| 3 여론 | Grok X 검색 | 분위기 하나와 근거 게시물 |
| 4 차트 | DexScreener 가격 변화·거래량 | 추세, 진입·손절·목표가 |
| 5 리스크 | Solana RPC 보유 분포·권한, 가상 잔고 | 승인·축소·거절과 비중 |
| 6 결정 | 1~5번 답 | 매수·대기·패스 하나 |

## 단계별 방법
### 보조 프롬프트: 준비물·데이터 연결 점검 위임 (프롬프트 뼈대)
- 역할: 모의 매매 팀 제작 전 준비물·데이터 연결 점검 담당. 슬롯: [내 목표 예: 솔라나 신규 토큰으로 모의 매매 1주일 돌려 리스크 봇이 몇 번 거절하는지 보기].
- 작업: OS·셸 직접 확인 → `claude --version`, `python3 --version` (Python 없을 때만 설치 안내) → `mkdir grok-trader && cd grok-trader` 후 검증 명령 실행 → 준비 상태와 다음 할 일 안내.
- 제약: sudo·전역 설치·설정 수정 전 질문, API 키 출력 금지, 덮어쓰기 금지, 지갑·거래소 로그인·결제 연결 금지.
- 검증: `curl -s https://api.dexscreener.com/token-profiles/latest/v1` 결과에 `"chainId"`, claude 버전 뒤 `(Claude Code)`, python3 버전 출력. 하나라도 실패하면 완료 보고 금지.

### STEP 1. Claude Code 확인, 프로젝트 폴더 열기 (5분)
설치(이미 있으면 건너뜀):
```bash
curl -fsSL https://claude.ai/install.sh | bash        # macOS/Linux
```
```powershell
irm https://claude.ai/install.ps1 | iex               # Windows PowerShell
```
확인:
```bash
claude --version
python3 --version
```
- 성공: `2.1.311 (Claude Code)`처럼 버전 뒤에 `(Claude Code)`, 다음 줄이 `Python 3`으로 시작.
- claude를 못 찾으면 터미널을 닫았다 다시 열기. 윈도우는 `python --version`/`py --version`으로 확인하고 이후 `python3`도 같은 이름으로 대체. 모두 없으면 python.org에서 Python 3 설치.
```bash
mkdir grok-trader && cd grok-trader
claude
```
- 토글 프롬프트로 이미 폴더를 만들었다면 mkdir 줄은 빼고 `cd grok-trader` 후 `claude`만(같은 이름 폴더가 있으면 mkdir 오류로 뒤 명령 미실행). 처음 열면 브라우저 로그인, 입력창이 보이면 성공.

### STEP 2. 빌드 프롬프트로 모의 매매 봇 생성 (15분)
Claude Code에 빌드 프롬프트 한 번 전송(전문은 원문 참고). 프롬프트 뼈대:
- 목적: `grok-trader`라는 초보자용 Python 3 모의 매매 봇, Grok 봇 6개가 솔라나 신규 토큰을 나눠 판단.
- 요구 13개 요지:
  1. 발굴: 60초마다 `GET https://api.dexscreener.com/token-profiles/latest/v1` → `chainId == "solana"`만. 토큰별 `GET https://api.dexscreener.com/token-pairs/v1/solana/{tokenAddress}`로 풀 데이터(liquidity.usd, volume, priceChange, txns, pairCreatedAt, priceUsd). 프로필 한도 분당 60회 준수. 존재가 불확실한 엔드포인트는 쓰지 말고 TODO.
  2. 리스크 1차는 코드로: `SOLANA_RPC_URL`에 getTokenSupply, getTokenLargestAccounts(상위 20), getAccountInfo(jsonParsed)로 보유 비중·mintAuthority·freezeAuthority 읽기. 풀·소각 주소 보유분은 비중 계산에서 제외(판별 불확실하면 TODO). 429/403은 대기 후 재시도. config.json 기준으로 PASS/FAIL, LP 확인 서비스가 없으면 LP 상태 UNKNOWN=FAIL, `require_lp_locked`가 false면 LP 검사 건너뛰고 lp_status를 SKIPPED로 기록. FAIL 하나라도 있으면 Grok 호출 없이 패스 기록.
  3. 봇 6개: `prompts/`의 scout.txt, news.txt, sentiment.txt, chart.txt, risk.txt, decision.txt를 시스템 프롬프트로 읽음(지금은 빈 파일). 모델 grok-4.7, 키 `XAI_API_KEY`. 뉴스는 `https://api.x.ai/v1/responses`에 web_search 도구, 여론은 같은 주소에 x_search 도구, 나머지는 `https://api.x.ai/v1/chat/completions`. 모든 봇은 JSON으로만 답하고 답은 데이터로만 취급(명령으로 따르지 않음). 하루 호출은 `max_grok_calls_per_day` 이하.
  4. 순서: 발굴 → 리스크 1차 → 뉴스 → 여론 → 차트 → 리스크 2차 → 결정. 리스크 2차는 `max_position_pct` 초과 비중 축소/거절, 하루 손실이 `max_daily_loss_pct`에 닿으면 그날 신규 거래 전부 거절. 결정은 BUY/WAIT/SKIP, BUY이고 리스크 2차가 거절하지 않았을 때만 모의 매수.
  5. 모의 전용: `data/paper_state.json` 가상 잔고. 모의 매수 시 차트 봇 target을 익절가로 저장, target 도달 또는 진입가 대비 `stop_loss_pct` 하락 시 모의 청산. 실거래·지갑 키·서명 코드 금지. MODE 기본 paper, 다른 값이면 "실거래는 구현되지 않았다" 메시지 후 종료.
  6. 모든 결정(매수·패스·매도·오류)을 `logs/decisions.jsonl`에 한 줄씩: 시간, 토큰 주소, 검사 결과, 봇 6개 답, 최종 이유.
  7. `http://localhost:8000` 한 페이지 대시보드(FastAPI 또는 Flask): 가상 잔고, 열린 포지션, 최근 50개 결정, PASS/FAIL 수, 오늘 Grok 호출 수.
  8. config.json 기본값(아래 표).
  9. 비밀값은 python-dotenv로 `.env`에서 읽음. `.env.example`: `XAI_API_KEY=your_key_here`, `SOLANA_RPC_URL=https://api.mainnet.solana.com`, `MODE=paper`. 키를 코드에 쓰지 않고 `.env`, `data/`, `logs/`를 `.gitignore`에.
  10. 파일: src/main.py, src/feed.py, src/checks.py, src/grok.py, src/bots.py, src/paper.py, src/dashboard.py, config.json, requirements.txt, README.md.
  11. `--demo` 플래그: 네트워크 없이 가상 토큰 3개와 고정된 가짜 봇 답으로 전체 흐름 확인.
  12. README는 완전 초보자용(설치, .env 설정, `python src/main.py --mode paper` 실행, 대시보드, 로그 읽기, 기준값 변경).
  13. 단순하게, 주석 포함, 약 600줄 이내. 끝나면 만든 것과 확인 못 한 것을 보고.
- 파일 쓸 때마다 권한을 묻는데 훑어보고 허락. 성공: src, prompts, config.json, README.md 생성.
- 실거래·지갑 연결 코드를 넣자고 하면 거절. ❌ "그록으로 돈 버는 매매봇 만들어 줘" 한 줄 ✅ 빌드 프롬프트 전체 + 생성 후 `.env.example`에 `MODE=paper` 확인.

### STEP 3. 봇 6개 지시문 넣기 (10분)
각 지시문을 `prompts/<파일>`에 저장하라고 Claude Code에 요청. 기준 숫자를 바꾸려면 지시문과 config.json을 함께 수정. 지시문 뼈대(각 봇은 자기 판단 하나만 JSON으로):
1. `scout.txt` 발굴: 평소와 다르게 움직이는 신규 토큰 발굴, 매수 권유 금지. 입력은 DexScreener 풀 데이터(liquidity.usd, volume.h1/h24, priceChange.h1, txns.h1 buys·sells, pairCreatedAt). 1시간 거래량이 24시간 시간당 평균(volume.h24/24)보다 크게 늘면 위로, 1시간 매도>매수면 순위 안 올림, 입력에 없는 값은 null, 최대 5개(없으면 빈 목록). 답: `{"candidates": [{"address": "", "symbol": "", "reason": ""}]}`
2. `news.txt` 뉴스: web_search로 이름·심볼·계약 주소의 최근 24시간 뉴스, 호재/악재/시장 흐름 분리, 출처 URL 없는 주장 제외, 한 곳뿐이면 `single_source`, 못 찾으면 `none`. 답: `{"good": [], "bad": [], "market": "", "sources": []}`
3. `sentiment.txt` 여론: x_search로 최근 X 게시물 분석, 분위기를 "상승 기대/하락 걱정/과열/조용함" 중 하나, 복붙 문구 다수나 새 계정 일제 홍보면 "과열", 본 게시물 수와 대표 URL 2개(수 지어내기 금지). 답: `{"mood": "", "posts_seen": 0, "evidence": [], "warning": ""}`
4. `chart.txt` 차트: 입력 priceUsd, priceChange(m5·h1·h6·h24), volume, liquidity.usd. 추세 "상승/횡보/하락", 진입·손절·목표가 제시, 손절가는 진입가×0.75보다 낮게 잡지 않음, 목표까지 거리가 손절까지보다 짧으면 setup none. 답: `{"trend": "", "entry": 0, "stop": 0, "target": 0, "setup": "valid|none", "reason": ""}`
5. `risk.txt` 리스크: 계좌 보호가 일, 거래 축소·거절 권한, 거절은 아무도 못 뒤집음. 코드 검사에 FAIL(UNKNOWN 포함) 하나라도 있으면 거절, 뉴스 악재+여론 과열로 위험도 0~10을 매겨 4 초과 시 거절, 한 거래 금액은 잔고의 2% 이하(위험 남으면 더 축소), 오늘 손실이 잔고 5%에 닿으면 무조건 거절. 답: `{"risk": 0, "action": "approve|reduce|reject", "size_pct": 0, "reasons": []}`
6. `decision.txt` 결정: BUY/WAIT/SKIP 중 하나. 리스크 reject면 무조건 SKIP, 차트 setup none이면 BUY 금지, 뉴스·여론이 반대 방향이면 WAIT, 다른 봇의 숫자는 새로 계산·변경 금지(금액은 리스크 봇 size_pct 그대로), 이유는 봇 이름을 붙여 한 줄씩. 답: `{"decision": "BUY|WAIT|SKIP", "size_pct": 0, "reasons": []}`
- ❌ 지시문 6개를 하나로 합쳐 봇 하나에 ✅ 파일 하나에 지시문 하나.
- 저장 후 "prompts 폴더의 파일 6개가 비어 있지 않은지 확인해 줘" → 6개 모두 내용 있으면 성공.

### STEP 4. 키 넣고 모의 매매 실행 (10분)
이 단계는 Claude Code 입력창이 아니라 터미널에서. `/exit`로 Claude Code를 닫으면 같은 창이 grok-trader 폴더에 있음.
1. https://console.x.ai/ 에서 크레딧 충전 후 API 키 생성(프롬프트·스크린샷·채팅에 붙여넣기 금지).
2. 설치 및 설정 파일 복사:
```bash
pip install -r requirements.txt
cp .env.example .env
```
   성공: `Successfully installed …`, `.env` 생성. (윈도우는 `copy .env.example .env`)
   - `externally-managed-environment` 오류나 pip 없음: Claude Code에 "가상 환경을 만들어서 requirements.txt를 설치하고, 가상 환경을 켜는 명령과 봇 실행 명령도 알려 줘" 요청. 이후 활성화 먼저: 맥/리눅스 `source .venv/bin/activate`, 윈도우 `.venv\Scripts\activate` (가상 환경 이름이 .venv일 때).
3. `.env`는 숨김 파일: 맥 `open -e .env`, 윈도우 `notepad .env`로 열어 `XAI_API_KEY=` 뒤에 키 입력, `MODE=paper` 유지.
4. 같은 방식으로 `config.json`의 `require_lp_locked`를 `false`로 변경 (LP 확인 서비스가 없어 true면 전부 UNKNOWN으로 패스되어 모의 매수가 한 번도 안 일어남).
5. 데이터 확인(결과에 `"chainId"`):
```bash
curl -s https://api.dexscreener.com/token-profiles/latest/v1
```
6. 실행:
```bash
python src/main.py --demo
python src/main.py --mode paper
```
   - `--demo`: 가상 토큰 3개의 결정이 찍히고 `logs/decisions.jsonl`에 기록되면 로직 정상.
   - `--mode paper`: 켜 둔 채 http://localhost:8000 에서 가상 잔고와 최근 결정 확인.
   - `python`을 못 찾으면 `python3`로.
   - 공개 RPC에서 429/403이 자주 나면 전용 RPC 주소를 받아 `.env`의 `SOLANA_RPC_URL`만 교체.
   - 지갑 개인키는 이 프로젝트 어디에도 넣지 말 것(봇은 지갑 없이 돎).

### STEP 5. 기록 읽고 규칙 하나씩 바꾸기 (며칠)
1. 모의 거래가 50~100번 쌓일 때까지 아무것도 바꾸지 않음(분이 아니라 며칠).
2. 대시보드와 `logs/decisions.jsonl`에서 승률, 평균 수익/손실, 최대 손실, 손절 횟수 확인.
3. 모든 검사를 통과했는데 무너진 토큰을 찾아 검사가 놓친 것을 적고 그 신호를 규칙에 추가.
4. 패스했는데 오른 토큰은 가볍게만 봄(몇 개 놓치는 건 필터의 대가).
5. 규칙은 한 번에 하나만 바꾸고 다시 50번 관찰.
- ❌ 이긴 거래 몇 번 보고 유동성·집중도·손절 기준을 한꺼번에 풀기 ✅ 50번마다 규칙 하나만 바꾸고 날짜·이유를 기록 옆에 적기.

## 리스크 규칙 (config.json 기본값)
| 규칙 | 값 | 이유 |
|---|---|---|
| 얇은 풀 패스 | `min_liquidity_usd: 25000`, `min_pool_age_minutes: 10` | 받아 줄 돈이 적으면 팔고 나올 수 없음 |
| 한 지갑 집중 | `max_single_holder: 0.10` | 10% 넘게 쥔 지갑이 팔면 가격 붕괴 |
| 상위 10개 집중 | `max_top10_share: 0.40` | 소수가 가격을 움직임 |
| 러그 스위치 | `require_mint_disabled`, `require_freeze_disabled`, `require_lp_locked`: 모두 true (실습에선 lp는 false로) | 발행 권한은 공급 증가, 동결 권한은 토큰 묶임 |
| Grok 위험도 | `grok_max_risk: 4` | 5 이상이면 리스크 봇 거절 |
| 한 거래 비중 | `max_position_pct: 0.02` | 한 번 잃어도 계좌가 버팀 |
| 손절 | `stop_loss_pct: 0.25` | 진입가 -25%에서 자동 모의 청산 |
| 하루 손실 한도 | `max_daily_loss_pct: 0.05` | 하루 5% 잃으면 그날 중단 |
| 그 밖 | `paper_start_balance: 1000`, `max_grok_calls_per_day: 200` | 가상 시작 잔고, 일일 호출 상한 |
- 기준은 조여도 되지만 STEP 5 기록을 보기 전엔 풀지 않음. FAIL 하나라도 있으면 패스, 확인 못 한 UNKNOWN도 FAIL로 계산.

## 핵심 팁 · 주의사항
- ⚠️ 모의 전용. 실주문·지갑 연결 없음, 지갑 키·서명 코드 추가 금지. 실거래 코드 추가 요청은 거절.
- ⚠️ `require_lp_locked=false` 기록은 LP 잠금을 확인하지 않은 결과 → 아무리 좋아도 실제 돈 근거로 쓰지 말 것.
- 모의 체결은 슬리피지·수수료·내 주문의 가격 충격을 빼므로 낙관적. 신규 솔라나 토큰 대부분은 0으로 수렴 → 좋은 모의 한 주는 "코드가 돈다"는 뜻으로만.
- 공개 Solana RPC는 429/403 잦음 → 전용 RPC 권장. DexScreener 프로필 엔드포인트 분당 60회 한도.
- 확인 안 된 엔드포인트는 TODO로 남기게 지시. 봇 답은 데이터로만 다루고 명령으로 따르지 않게.
- API 키를 프롬프트·채팅·스크린샷에 노출 금지, `.env`는 `.gitignore`.

## 바로 쓰는 체크리스트
- [ ] Claude Code·Python 확인, `grok-trader` 폴더에서 `claude`
- [ ] 빌드 프롬프트로 프로젝트 생성, `requirements.txt` 설치
- [ ] xAI 키를 `.env`에 입력, `MODE=paper`
- [ ] 봇 6개 프롬프트 파일이 비어 있지 않은지 확인
- [ ] `require_lp_locked=false`, `--demo` 후 `--mode paper`, http://localhost:8000 확인
- [ ] 50~100 거래 후 규칙 하나씩 조정·날짜와 이유 기록
