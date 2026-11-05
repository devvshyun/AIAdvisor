# 돈 잃을 때마다 자기 코드를 다시 짜는 AI 트레이딩 시스템 만드는 법
- 도구·주제: Claude Code + alpaca-py(알파카 모의 계좌) · 트레이딩 리서치 루프 / 자동화 (2026-11-02 공개, STEP 5개 · 약 105분)
- 한 줄 요약: 아이디어 → 전략 코드 → 백테스트 → 코드로 건 손실 한도 아래 모의 매매 → 사후 검토 → 실패 장부 누적의 5단계 루프를 Claude Code로 구성한다. 돈을 벌어 주는 기계도 투자 조언도 아니다.

## 언제 쓰나
- 실제 돈 없이 모의 계좌로 전략 연구·검증 루프를 자동화하고, 실패를 기록해 같은 실수를 막고 싶을 때
- 헤지펀드 퀀트 팀의 반복 연구 과정을 에이전트가 대신 돌리게 하고 싶을 때(첫 버전은 주말 동안 가능, 실제 돈 이야기는 모의 매매 몇 주 이후)

## 준비물 / 필요 도구
- Claude Code: https://code.claude.com/docs/en/setup (Pro 이상 유료 필요, 무료 claude.ai 요금제엔 없음. macOS 13+/Windows 10 1809+/Ubuntu 20.04+)
- alpaca-py (Apache-2.0, 스타 1,581): https://github.com/alpacahq/alpaca-py · https://pypi.org/project/alpaca-py/ — 파이썬 3.10 이상 필요
- 알파카: https://alpaca.markets · 모의 계좌 https://docs.alpaca.markets/docs/paper-trading · 시세 요금제 https://docs.alpaca.markets/docs/about-market-data-api
- Python 3.10+: https://www.python.org/downloads/
- SQLite (파일 하나 DB, 별도 설치 불필요) → `memory/ledger.db`
- 비용: 알파카 모의 전용 계정은 이메일만으로 무료, 무료 IEX 실시간 시세(IEX 거래소 한 곳). 과거 시세는 무료 요금제로 2016년부터 미국 주식·ETF 수신 가능
- 용어: 모의 계좌=진짜 시세로 주문을 흉내내는 연습 계좌 / 백테스트=과거 데이터에 전략을 돌려 보는 시험 / 포지션=보유 종목·수량 / 청산=보유분을 팔아 정리 / 손절선=산 가격에서 몇 % 하락하면 손해 보고도 파는 선

## 단계별 방법
**Quick Start: Claude Code 설치** (이미 설치돼 있으면 생략)
```bash
curl -fsSL https://claude.ai/install.sh | bash        # macOS
```
```powershell
irm https://claude.ai/install.ps1 | iex              # Windows PowerShell
```
- 새 터미널에서 `claude --version` → `2.1.316 (Claude Code)` 같은 버전이 나오면 성공. 모든 명령은 macOS 터미널 기준

**위임 프롬프트 뼈대 (프로젝트 + 손실 한도 검증)** — 터미널에서 `claude` 실행 후 첫 메시지
- 역할: AI 트레이딩 연구 루프 프로젝트 설치와 손실 한도 검증 담당. 맥락: 초보, 파이썬 도구가 없을 수 있음, 알파카 모의 계좌로만 운영
- 채울 곳: [내 목표 — 예: SPY로 20일 평균 전략을 모의 계좌에서 시험]
- 작업: ① `python3 --version` 3.10 이상 확인, 낮으면 설치 전 질문 ② `trading-loop` 폴더 생성, `python3 -m venv .venv`, `.venv/bin/pip install alpaca-py`, 폴더 7개 생성(research/ strategies/ backtests/ journal/ memory/ config/ data/), config/·data/는 `.gitignore`, `config/.env`에는 `ALPACA_API_KEY=`·`ALPACA_SECRET_KEY=` 두 줄을 값 없이 생성. `check_order(order, account)`가 든 `risk.py` 작성(5개 한도는 `config/risk.json`에서 읽음). `memory/ledger.db`의 `hypotheses` 테이블 생성 ③ 검증 명령 실행 ④ 목표를 `research/first-idea.md`에 아이디어 한 문장 + 틀렸다고 볼 결과로 저장하고 각 폴더·파일의 역할과 다음 할 일을 초보자 눈높이로 설명
- 제약: 실제 돈 계좌 연결·주문 금지, 알파카 키를 묻거나 출력 금지(키는 사용자가 `config/.env`에 직접 기입), sudo·전역 설치·설정 수정 전 질문, 기존 파일 덮어쓰기 금지
- 검증: `.venv/bin/pip show alpaca-py`에 `Name: alpaca-py`; 아래 check_order 명령이 `(False, 'Daily loss limit hit. Trading stopped.')`; 빈 장부 조회가 `(0,)`

**STEP 1. 모의 계좌 프로젝트 만들기 (20분)**
1. 알파카에 이메일로 모의 전용 계정 생성. 대시보드 왼쪽 위 계좌 번호가 모의(Paper)인지 확인한 뒤 그 화면에서 API 키 신규 생성(키 ID와 시크릿). 모의 키는 실제 돈 계좌 키와 별개이며 서로 바꿔 쓸 수 없음. 시크릿은 화면을 벗어나면 사라지므로 바로 메모장에 옮김(① API Key ID → `ALPACA_API_KEY`, ② Secret Key → `ALPACA_SECRET_KEY`)
2. 파이썬 확인과 환경 구성
```bash
python3 --version          # 3.10 이상. 맥 기본 3.9.6이면 오류 없이 구 alpaca-py(0.43.5)가 깔림 → python.org에서 새 버전 설치 후 새 터미널
mkdir trading-loop && cd trading-loop
python3 -m venv .venv
.venv/bin/pip install alpaca-py
.venv/bin/pip show alpaca-py   # Name: alpaca-py, Version: 0.44.0 등이 보이면 성공
claude
```
   - 윈도우는 `python`, `.venv\Scripts\`로 바꿔야 함(막히면 Claude Code에 윈도우용으로 변환 요청). 가상환경(.venv)=이 폴더 안에만 도구를 설치하는 칸
3. 프로젝트 구조 프롬프트 뼈대: 모의 매매 전용 AI 트레이딩 연구 루프. 폴더 구조를 만들고 승인 대기 — `research/` 아이디어 메모 / `strategies/` 전략 파일(전략당 파일 하나, 파일마다 버전 번호) / `backtests/` 결과 / `journal/` 모의 매매 결정과 이유 전부 / `memory/` 가설 장부(SQLite) / `config/` 손실 한도와 API 키(gitignore) / `data/` 과거 가격(gitignore). 모의 매매는 alpaca-py, 실제 돈 계좌 절대 연결 금지, `config/.env`에 키 두 줄을 값 없이 만들고 키 값은 사용자가 직접 기입·출력 금지. 성공 표시: 폴더 7개를 만들었다며 승인을 기다린다는 답
4. 실패 장부 프롬프트 뼈대: `memory/ledger.db` SQLite의 `hypotheses` 테이블 하나. 열: id, 아이디어(한 문장), 제안한 에이전트, 시장, 테스트한 날짜, 전략 파일과 버전, 시도한 변형 수, 테스트 기간의 시장 국면(상승 추세·하락 추세·횡보·고변동성), 백테스트 결과, 봉인 구간 결과, 모의 매매 결과, 상태(미테스트·실패·백테스트만 통과·모의 매매 통과·일시 중지·폐기), 배운 점. 새 아이디어를 내기 전에 시장·국면·상태로 과거 아이디어를 검색하는 작은 도우미도 만들고, 백테스트·모의 매매 검토·비평 보고가 끝날 때마다 장부 자동 갱신
```bash
.venv/bin/python -c 'import sqlite3; print(sqlite3.connect("memory/ledger.db").execute("select count(*) from hypotheses").fetchone())'   # (0,) 이면 빈 장부 생성
```
5. 알파카 키 기입(대화창에 붙여넣지 말고 파일에 직접). Claude Code를 닫은 터미널 또는 새 터미널에서 `cd trading-loop` 후:
```bash
open -e config/.env
```
   `ALPACA_API_KEY=<모의 계좌 키>` / `ALPACA_SECRET_KEY=<모의 계좌 시크릿>` 형태로 `=` 바로 뒤에 붙여넣고 저장. Finder에서 점 파일은 숨겨져 있어 Command+Shift+. 로 표시. 실제 돈 계좌 키는 이 폴더에 두지 말 것. 새 터미널은 홈에서 시작하므로 항상 `cd trading-loop` 후 `claude`

**STEP 2. 아이디어를 전략 코드로 (20분)**
- 아이디어가 있으면 `research/`에 한 문장으로(예: "SPY 종가가 20일 평균 위로 올라서면 사고, 아래로 내려가면 판다") 적고 코드 프롬프트로
- 아이디어 탐색은 관점 하나만 보는 리서치 에이전트: 가격 분석가(가격·거래량 패턴) / 실적 리더(실적 발표·공시) / 거시 관찰자(금리·경제 지표·업종 흐름) / 회의론자(아이디어마다 실패 이유만 따짐). 역할마다 터미널 창을 새로 열어 `cd trading-loop` + `claude`로 따로 실행(서로의 메모를 먼저 읽으면 첫 의견에 끌려가 여러 명을 둔 의미가 사라짐)
- 리서치 프롬프트 뼈대: 당신은 [역할]. [볼 관점]만 보고 [시장/종목]을 살핌. 제안 전에 `memory/ledger.db`에서 이 시장의 기존 테스트 아이디어를 조회하고, 실패한 아이디어는 시장 상황이 분명히 바뀌지 않았다면 재제안 금지. 테스트 가능한 아이디어 최대 3개: 한 문장 설명, 통할 이유, 필요한 정확한 시장 조건, 틀렸다고 판정할 결과. 외부 숫자(실적·금리)는 출처·날짜 표기, 못 찾으면 지어내지 말고 `[출처 없음]`. `research/<역할>-<날짜>.md`에 저장, 다른 에이전트 메모는 읽지 말 것
- 전략 코드 프롬프트 뼈대: `research/<메모>.md`의 아이디어를 `strategies/`에 전략으로 작성. 공통 구조는 진입 규칙·청산 규칙·포지션 크기·손실 한도. 파일 맨 위에 버전 번호와 가설 한 줄. 진입·청산이 정확히 그 조건에서만 발동하는지 단위 테스트를 쓰고 실행해 실패는 수정. 백테스트는 아직 돌리지 말 것. 성공: 버전 번호가 붙은 파일 + 테스트 전부 통과
- ❌ "돈 되는 전략 하나 짜 줘" → ✅ 아이디어 한 문장 + 틀렸다고 볼 결과를 먼저 적고 그 메모를 코드로

**STEP 3. 백테스트하고 돈 잃은 거래만 고치기 (30분)**
- 반복 루프는 언젠가 통과함(진짜를 찾아서가 아니라 버전을 많이 시도해서) → 과적합 방지 5규칙: ① 예상부터 적기(수익률·승률·실패 기준을 저장, 결과 후 수정 금지) ② 봉인 구간 남기기(가장 최근 20~30% 데이터는 끝까지 사용 금지, 아이디어당 딱 한 번만 테스트) ③ 워크포워드(한 구간으로 맞추고 다음 구간으로 시험, 앞으로 밀며 반복) ④ 시도 횟수만큼 기준 올리기(변형 500개면 하나는 운으로 좋아 보임) ⑤ 깨뜨리기(거래 비용 2배, 그 시장 최악 구간, 늦은 체결)
- 용어: 샤프 지수=수익/수익의 흔들림, 디플레이티드 샤프=시도 횟수만큼 성과를 깎아 본 지표(장부가 시도 횟수를 셈), 과적합=고치다 보니 과거 데이터에만 우연히 맞은 상태, 최대 낙폭=계좌 고점 대비 최대 하락 비율
- 아이디어 메모 맨 아래 예상 기록 형식 예시: `아이디어: SPY 종가가 20일 평균 위로 올라서면 사고, 아래로 내려가면 판다` / `예상: 연 수익률 10% 안팎, 승률 45% 이상` / `실패 기준: 승률 40% 미만이거나 최대 낙폭 15% 초과`
- 백테스트(자동 수정 루프) 프롬프트 뼈대: `strategies/<파일>.py` 백테스트. 먼저 예상을 `backtests/<전략>-prediction.md`로 저장하고 이후 수정 금지. 가격은 alpaca-py 과거 시세로 [기간, 예: 최근 5년] 일봉을 받아 `data/`에 저장(있으면 재사용). 개발 구간만 사용, 마지막 [봉인 비율, 예: 30]%는 봉인. 워크포워드 → 스트레스(거래 비용 2배 + 시장 역대 최악 구간 5개). 수익률·최대 낙폭·승률·거래 수·샤프, 그리고 장부의 전체 변형 수로 계산한 디플레이티드 샤프 보고, 예상과 비교하고 `backtests/`에 저장. 실패 기준에 걸리면 묻지 말고 반복: 돈 잃은 거래만 골라 공통점(시장 국면·진입 시점·청산 이유) → 사고파는 규칙 하나만 바꿔 새 버전 번호로 저장 → 장부의 변형 수 +1 → 같은 개발 구간으로 재백테스트·예상 비교. 수정이 [수정 한도, 예: 3]번(아이디어당 3~5번 권장)에 닿으면 중단하고 장부에 실패 기록. `risk.py`, `config/risk.json` 수정 금지
- 수동 수정 프롬프트 뼈대(중간에 멈췄을 때): 최신 결과가 실패 기준에 걸림 → 전략을 통째로 버리지 말고 돈 잃은 거래의 공통점 설명, 개선안은 하나만, 규칙 그 하나만 바꿔 새 버전 저장·같은 백테스트 재실행·예상 비교, 장부 변형 수 +1, 봉인 구간 금지, 이미 한도만큼 수정했다면 고치지 말고 실패로 기록
- 한도만큼 써도 실패 기준에 걸리면 접고 실패 장부에 남김("40번 고쳐야 통과하는 전략이라면 그 자체가 답")
- 결과가 지나치게 좋아 보이면 점검: 미래 데이터가 과거에 섞이지 않았는지 / 봉인 구간을 여러 번 쓰지 않았는지 / 거래 비용을 빼고 계산하지 않았는지
- ❌ "테스트 통과할 때까지 계속 고쳐 줘" → ✅ 수정 한도를 정하고 고칠 때마다 장부 변형 수를 1씩 올림

**STEP 4. 손실 한도를 코드로 걸고 모의 매매 (20분)**
- 올릴 전략: STEP 3 통과 + 봉인 구간도 한 번 깨끗하게 통과한 것만. 대부분의 전략(AI 전략 포함)은 돈을 잃음
- 한도를 프롬프트에만 쓰면 AI가 상황을 따지다 스스로 선을 넘을 수 있음 → 코드로 걸면 어떤 말에도 주문이 증권사로 가지 않음
- Claude Code에 "아래 코드를 risk.py로 그대로 저장해 줘"라고 요청 (모든 주문이 거치는 검사, 주문마다 `stop_loss_pct`를 같이 넘겨야 함)
```python
import json
from pathlib import Path

LIMITS = json.loads(Path("config/risk.json").read_text())

def check_order(order, account):
    if account["daily_loss_pct"] >= LIMITS["max_daily_loss_pct"]:
        return False, "Daily loss limit hit. Trading stopped."
    if account["drawdown_pct"] >= LIMITS["max_drawdown_pct"]:
        return False, "Max drawdown hit. Trading stopped."
    if "stop_loss_pct" not in order:
        return False, "Order has no stop loss."
    if order["stop_loss_pct"] > LIMITS["max_loss_per_trade_pct"]:
        return False, "Stop loss is wider than the per-trade limit."
    if order["value"] > account["equity"] * LIMITS["max_position_pct"]:
        return False, "Order is larger than the position limit."
    if account["open_positions"] >= LIMITS["max_open_positions"]:
        return False, "Too many open positions."
    return True, "OK"
```
(원문 복사본은 들여쓰기가 사라져 있어 위는 표준 파이썬 들여쓰기로 복원)
- "아래 내용을 config/risk.json으로 그대로 저장해 줘" (값은 예시, 내 기준으로 변경; `max_position_pct`만 비율 0.10, 나머지는 % 단위)
```json
{
  "max_daily_loss_pct": 2.0,
  "max_drawdown_pct": 8.0,
  "max_loss_per_trade_pct": 5.0,
  "max_position_pct": 0.10,
  "max_open_positions": 5
}
```
  의미: 하루 손실 2.0% / 최대 낙폭 8.0% / 거래당 손절선 5.0% / 주문당 자산의 10% / 동시 포지션 5개
- 검증(하루 손실 2.5% 가짜 계좌):
```bash
.venv/bin/python -c 'from risk import check_order; print(check_order({"value": 50, "stop_loss_pct": 3.0}, {"daily_loss_pct": 2.5, "drawdown_pct": 1.0, "equity": 1000, "open_positions": 0}))'
# (False, 'Daily loss limit hit. Trading stopped.')
```
- 한도 파일 잠그기(에이전트가 고치려 하면 막히고 내 허락 필요):
```bash
chmod 444 risk.py config/risk.json     # ls -l risk.py 가 -r--r--r-- 이면 잠금. 수정 시 chmod 644 로 풀고 고친 뒤 다시 잠금
```
- 모의 연결 프롬프트 뼈대: 백테스트 통과 전략을 alpaca-py로 알파카 모의 계좌에 연결. 주문마다 전략 파일의 손실 한도를 `stop_loss_pct`로 함께 넘기고, 먼저 `risk.py`의 `check_order`를 `config/risk.json` 한도로 실행. 걸리면 주문 차단하고 이유 기록. `risk.py`/`risk.json`은 읽기만. 모든 결정을 `journal/`에 기록(시각, 전략·버전, 시장 상황, 결정, 이유). 모의 계좌만 사용
- 연결 확인: `journal/`에 기록이 쌓이고 알파카 대시보드 모의 계좌 주문 내역에 같은 주문이 보임
- 실제 돈 차단: `TradingClient`는 `paper=True`가 기본. 코드에 `paper=False`가 보이면 실거래 설정이니 즉시 제거
- 한도를 넘는 주문이 한 번이라도 통과했다면 `check_order`가 주문마다 돌지 않는 것 → 다른 일보다 먼저 수정
- ❌ 프롬프트에 "하루 2% 넘게 잃으면 멈춰"만 쓰기 → ✅ `config/risk.json`에 숫자로 두고 모든 주문이 `check_order`를 거치게

**STEP 5. 사후 검토하고 실패를 장부에 쌓기 (15분)**
- 매주 일요일: `cd trading-loop` → `claude` → 비평가 프롬프트
- 비평가 프롬프트 뼈대: 당신은 비평가. `journal/`의 지난 7일 기록을 전부 읽고, 전략마다 모의 매매 결과를 백테스트·처음 적은 예상과 비교. 테스트보다 실전이 나쁜 전략과 그 차이, 돈 잃은 거래들의 공통 시장 조건, 반복 실수, 멈출 전략 여부를 돌려 말하지 말고 보고. `journal/review-<날짜>.md`에 저장하고 발견 내용을 모두 `memory/ledger.db`에 기록
- 백테스트는 좋았는데 모의에서 무너진 전략=과적합 → 장부에 실패로 표시하고 통과시키려 시도한 변형 수도 확인
- 루프가 닫힘: 리서치 에이전트가 장부부터 보고 실패 아이디어를 건너뜀 → 백테스트 시도가 전부 세어져 기준이 오름 → 비평가가 배운 점을 장부에 다시 기록 → 다음 주 리서치가 실패와 시장 조건을 알고 시작
- 확인: 위의 장부 count 명령이 `(0,)`이 아니라 `(3,)`처럼 늘어 있으면 쌓이는 중
- 같은 아이디어가 반복되면 리서치 에이전트가 장부를 조회하지 않거나 갱신이 안 되는 것 — 둘 다 점검. 전부 손실이어도 가짜 돈으로 싸게 알게 된 결과이니 장부에 남길 것
- ❌ 실패한 전략 파일 삭제 후 새로 시작 → ✅ 실패 이유와 시장 국면을 장부에 남기고 새 아이디어 전에 검색

## 핵심 팁 · 주의사항
- 투자 조언이 아님. 대부분의 트레이딩 전략(AI 전략 포함)은 손실
- 모의 전용: 코드에 `paper=False`가 있으면 실거래 → 즉시 제거. 실제 돈 계좌 키는 이 폴더에 두지 않음
- 주문이 `check_order`를 거치지 않으면 한도는 무의미. 한도 파일은 `chmod 444`로 잠금
- 키는 `config/.env`에 직접 기입, 채팅에 붙이지 말 것(`config/`·`data/`는 gitignore)
- 통과할 때까지 반복하면 과적합: 수정 횟수 상한, 장부에 변형 수 기록, 봉인 구간은 아이디어당 한 번만
- 리서치 에이전트는 서로의 메모를 읽지 않게 따로 실행. 외부 숫자는 출처·날짜 필수(없으면 `[출처 없음]`)
- 맥 기본 파이썬 3.9는 오류 없이 구버전 alpaca-py(0.43.5)가 깔림 → 3.10+ 확인

## 바로 쓰는 체크리스트
- [ ] Python 3.10+ 확인, `trading-loop` 폴더 + `.venv` + alpaca-py 설치(`pip show` 확인)
- [ ] 알파카 모의(Paper) 계좌 키 발급, `config/.env`에 직접 기입
- [ ] 폴더 7개와 gitignore(config/, data/), 빈 장부 `(0,)` 확인
- [ ] 아이디어 한 문장 + 틀렸다고 볼 결과 + 예상 기록
- [ ] 백테스트: 예상 저장, 최근 20~30% 봉인, 워크포워드, 스트레스, 수정 한도 설정
- [ ] `risk.py` + `config/risk.json` 저장, 가짜 계좌 검증, `chmod 444`
- [ ] 모든 주문이 `check_order`를 거치는지, `paper=False`가 없는지 확인
- [ ] 매주 일요일 비평가 프롬프트로 사후 검토, 장부 행 증가 확인
