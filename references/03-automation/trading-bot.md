# 클로드 코드로 만드는 5자산 자동매매 봇
- 원문: https://lazyowen.com/guides/trading-bot
- 도구·주제: Claude Code + Alpaca(alpaca-py) · 자동매매 봇 제작 (교육용)
- 한 줄 요약: Claude Code로 SPY·QQQ·BTC/USD·GLD·USO 5자산 봇을 만들고 백테스트 → 2주 모의투자 → 손실 한도 → 아침저녁 리포트 → 실계좌 순서로 8단계에 걸쳐 검증하며 넘어가는 방법. (2026-08-06 갱신, 약 23분, STEP 8개)

## 언제 쓰나
- 자동매매 봇이 어려운 건 코딩이 아니라 순서라서, 안전한 순서(모의 우선)로 만들어 보고 싶을 때
- 면책: 투자 선택은 본인 책임이고 이 문서는 손실을 책임지지 않으며 투자 자문이 아님. 원본 캐러셀의 "월 3,000달러(약 400만 원)"는 한 사람의 사례일 뿐 보장 금액이 아니다. 실계좌는 원금 전액 손실 가능.

## 준비물 / 필요 도구
- Claude Code: https://code.claude.com/docs/en/setup — 여러 파일짜리 시스템을 한 번에 만드니 상위 코딩 모델 유리(원본은 Claude Fable, Opus 5로도 충분, Sonnet 계열도 가능). 모델 개요 https://platform.claude.com/docs/en/about-claude/models/overview
- Alpaca (수수료 무료 증권사, 모의·실거래 API 지원): https://alpaca.markets/ , 가입 https://app.alpaca.markets/signup , 모의투자 문서 https://docs.alpaca.markets/us/docs/paper-trading , 암호화폐 문서 https://docs.alpaca.markets/us/docs/crypto-trading
  - 모의 계좌는 이메일만으로 전 세계 누구나 만들 수 있고 기본 잔고 $100,000
- alpaca-py SDK: https://github.com/alpacahq/alpaca-py , 설치 가이드 https://alpaca.markets/sdks/python/getting_started.html
- Python 3.10 이상
- 24시간 켜진 컴퓨터 또는 VPS (월 $5~10, DigitalOcean·Railway). 모의 단계까지는 내 컴퓨터로 가능
- 하루 두 번 브리핑 수단: Telegram BotFather https://t.me/BotFather (원본은 Claude Cowork로 텔레그램·슬랙 전송). Cowork 예약 작업 안내 https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- 월 비용: Alpaca 무료, Claude 구독 월 $20 또는 API 종량제, VPS $5~10, 시세 데이터 무료(Alpaca 기본 피드) → 합계 월 $25~30(약 3.5만~4.2만 원). 모의 단계(STEP 7까지)는 더 낮음.
- 용어: 모의투자(페이퍼 트레이딩) = 실시세로 주문을 가상 체결하는 연습 환경, 가상환경(venv) = 폴더 안에서만 쓰는 도구 상자, VPS = 항상 켜진 빌린 컴퓨터, 백테스트 = 과거 데이터로 전략 재실행(규칙의 구멍 찾기, 미래 예측 아님), 슬리피지 = 기대 가격과 실제 체결가 차이, ATR = 최근 평균 가격 변동폭(변동성 지표)

## 단계별 방법
### 프롬프트 뼈대 A. 개발환경 설치·연결 검증 위임 (선택)
- 목적: Python/alpaca-py 설치와 모의계좌 잔고 조회까지 확인
- 역할: 파이썬 트레이딩 봇 프로젝트의 개발 환경 설치·연결 검증 담당. 사용자는 초보
- 슬롯: [운영체제와 셸], [기술 스택: Python 3.10+, alpaca-py], [목표: Alpaca 모의계좌에 연결해 잔고 읽기]
- 작업: ① `python3 --version`, `pip show alpaca-py`로 확인 ② 없으면 가상환경 만들고 `pip install alpaca-py python-dotenv` ③ `.env`의 모의계좌 키로 잔고를 실제로 한 번 조회 ④ Alpaca가 무엇이고 모의/실계좌 차이를 3줄로 설명
- 제약: 키·시크릿을 화면/로그에 출력 금지, 실계좌 주소(api.alpaca.markets) 접속 금지, 주문 0건
- 출력: 실행 명령, 버전, 만든 파일, 연결 결과, 남은 오류
- 검증: `python -c "import alpaca; print(alpaca.__version__)"`가 버전을 출력, 모의 잔고 조회 성공 + 계좌 상태 `ACTIVE`. 하나라도 실패하면 완료 보고 금지

### Quick Start (맥·리눅스 터미널)
```bash
mkdir paper-trading-bot && cd paper-trading-bot
python3 -m venv .venv && source .venv/bin/activate
pip install alpaca-py pandas python-dotenv pytest
```
마지막 줄에 `Successfully installed alpaca-py-...`, 프롬프트 앞에 `(.venv)`가 붙으면 정상. 이어서 Claude Code 설치·실행(화면이 열리면 준비 끝, 여기에 STEP 2 프롬프트를 붙임):
```bash
curl -fsSL https://claude.ai/install.sh | bash
claude
```

### 원본 사례 개요 (참고)
한 여성이 클로드로 5개 시장 24시간 매매 봇을 만들어 하루 두 통(아침 시장 상황, 밤 봇 활동) 메시지만 받는 구조. 시장별 전략이 다름: 지수는 평균 회귀, 암호화폐는 모멘텀 돌파, 원자재는 추세 추종. 포지션 크기는 변동성에 따라 자동 조절해 어느 자산에서나 감수 위험이 같다. 순서는 백테스트 → 2주 모의투자 → 실계좌이며 앞 두 단계를 건너뛰고 실계좌로 가지 않는다.

### STEP 1. 모의계좌와 키 준비하기 (10분)
1. https://app.alpaca.markets/signup 에서 이메일로 가입, 로그인 후 왼쪽 위에서 Paper(모의) 계정 선택
2. 모의계좌 대시보드에서 API 키와 시크릿 발급(시크릿은 발급 순간 한 번만 보이니 복사). 실계좌 키와 모양이 같아 눈으로 구분 불가 → 접속 주소로 구분(모의는 `paper-api.alpaca.markets`)
3. 프로젝트 폴더에 `.env` 생성(성공해도 출력 없음)
```bash
cat > .env << 'EOF'
ALPACA_API_KEY=여기에_모의계좌_키
ALPACA_SECRET_KEY=여기에_모의계좌_시크릿
ALPACA_PAPER=true
TELEGRAM_DRY_RUN=true
EOF
```
4. 키 로드 확인(값은 출력하지 않음). `키 있음: True`, `모의 모드: true`가 나와야 함.
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('키 있음:', bool(os.getenv('ALPACA_API_KEY'))); print('모의 모드:', os.getenv('ALPACA_PAPER'))"
```

### STEP 2. 프롬프트 하나로 봇 만들기 (15분)
자산 5개 × 전략 3개 구조(시장마다 움직임이 달라 같은 규칙을 쓰면 한쪽이 손해). 금·원유는 선물이 아니라 ETF 대리 자산(Alpaca가 주식·ETF·암호화폐를 다루기 때문, ETF는 가격이 1:1로 붙어 움직이지 않음, README에 명시시킬 것). Claude Code에 아래 명세를 통째로 붙이면 파일만 만들고 주문은 넣지 않는다.

프롬프트 뼈대 B. 5자산 봇 생성 명세
- 목적: Python 3.10+ / alpaca-py 기반 5자산 봇 생성(기본 동작은 모의투자)
- 전략 명세
| 자산 | 주기 | 전략 | 핵심 규칙 |
|---|---|---|---|
| SPY | 15분봉 | 평균 회귀 | 20기간 SMA·표준편차, -1.5σ 롱 / +1.5σ 숏, 평균 복귀 시 청산 |
| QQQ | 15분봉 | 평균 회귀 | 변동성이 커서 기준만 1.8σ |
| BTC/USD | 1시간봉 | 돌파 | 20기간 최고가 돌파 + 거래량이 20기간 평균의 1.5배 이상이면 롱, 같은 거래량 조건으로 최저가 이탈 시 숏 또는 롱 청산, 2×ATR 트레일링 스톱 |
| GLD, USO | 4시간봉 | 추세 추종 | 50 EMA가 200 EMA 상향 돌파 시 롱, 하향 돌파 시 청산 또는 숏, 3×ATR 트레일링 스톱 |
- 사이징·기록: 14기간 ATR로 1ATR 역행 시 손실이 자기자본의 정확히 1%가 되도록 수량 결정(조용한 자산은 크게, 변동성 큰 자산은 작게), 모든 거래에 자기자본 1% 하드 스톱(예외 없음), 상관 필터(SPY·QQQ 둘 다 롱이면 BTC/USD 신규 롱 금지), 모든 체결을 `trades.csv`(시각·자산·방향·진입가·청산가·손익·수량), 일별 손익을 `daily_pnl.csv`, 전략별 주기로 신호를 확인하는 연속 루프(API 끊김·휴장 처리)
- 안전 규칙 12개(하나도 빠뜨리지 말 것): ① 기본값은 모의, 환경변수가 하나도 없으면 무조건 모의 엔드포인트(`paper-api.alpaca.markets`) ② 실계좌는 ALPACA_PAPER=false + ALPACA_LIVE_CONFIRM=I_UNDERSTAND_REAL_MONEY + 명령에 `--live` 플래그, 셋 동시 충족 시에만, 하나라도 빠지면 모의로 강등하고 이유 출력 ③ 실계좌 시작 시 맨 위 경고 배너·현재 잔고·한 번 매매 최대 손실액 출력 후 10초 카운트다운, 로그에 매 줄 실계좌 여부 기록 ④ 한 번 매매 위험은 잔고의 1%, 수량 = (잔고×0.01) ÷ 손절 거리, 거리 ≤ 0이면 주문 건너뜀 ⑤ 잔고 최고점 대비 10% 하락 시 신규 주문 차단·열린 주문 취소·보유 포지션 정리 후 `STOPPED` 상태 파일 저장 ⑥ STOPPED는 사람이 `resume` 입력 전까지 유지 ⑦ 주문 전 거래 가능 여부·장 운영 시간·최소 수량·중복 주문·보유 현금 검사 ⑧ 주식 ETF는 미국 장중만, BTC/USD는 24시간으로 일정 분리 ⑨ API 키는 `.env`에서만 읽고 로그·예외·리포트에 출력 금지 ⑩ 백테스트는 신호 봉 종가 체결 금지, 다음 봉부터 체결 ⑪ 수수료·슬리피지 가정값을 `config.yaml`에 두고 결과에 함께 출력 ⑫ 텔레그램 전송은 기본 dry-run, 토큰이 없으면 오류 대신 콘솔 미리보기
- 만들 파일: `main.py`, `config.yaml`, `.env.example`, `requirements.txt`, `README.md`, `data.py`, `backtest.py`, `broker.py`, `portfolio.py`, `report.py`, `strategies/mean_reversion.py`, `strategies/breakout.py`, `strategies/trend_following.py`, `risk/manager.py`, `tests/test_risk.py`, `tests/test_live_requires_triple_confirm.py`, `tests/test_no_lookahead.py` (삼중 잠금 테스트는 하나라도 빠지면 모의로 강등되고, 셋 다 있을 때만 실계좌 경로가 열림을 모두 검증)
- 명령 규격
```
python main.py backtest --months 6
python main.py paper --dry-run
python main.py paper --once
python main.py live --once
python main.py status
python main.py stop --close-all
python main.py resume
python report.py morning --dry-run
python report.py evening --dry-run
```
- 진행 방식: 먼저 파일 트리와 구현 계획을 보여 주고 내가 확인한 뒤 파일 생성, 완료 후 pytest 실행·실패 수정·요약, 어떤 주문도 실제로 실행하지 않음

완료 후 확인 3가지: `tests/test_live_requires_triple_confirm.py` 존재 / 환경변수가 없을 때 모의로 붙는 분기가 `broker.py`에 있음 / `.env.example`에 예시값만 있고 진짜 키 없음.

### STEP 3. 실행 전에 코드 검수 시키기 (10분)
건너뛰기 쉽지만 가장 값싼 안전장치. 수정하지 말고 보고만 시키는 것이 핵심.

프롬프트 뼈대 C. 읽기 전용 코드 검수
- 지시: 프로젝트를 수정하지 말고 검수만, 각 항목을 파일명·줄 번호로 보고
- 항목: 환경변수 없을 때 모의 엔드포인트로만 붙는 기본값 분기 위치 / 세 조건 중 하나라도 빠졌을 때 모의 강등 위치 / 주문을 보내는 모든 위치 / dry-run에서 주문이 막히는 근거 / 키·시크릿이 로그에 노출될 수 있는 위치 / 거래당 1% 위험 계산식 / 10% 하락 정지 장치와 재시작 후 상태 보존 방식 / 백테스트가 다음 봉 가격으로 체결하는지 / 수수료·슬리피지 결과 반영 / 3중 잠금 없이 실계좌로 전환될 수 있는 경로 / 실계좌 모드에서 경고 배너·잔고·최대 손실액·카운트다운 실제 출력
- 출력: 마지막 줄에 "통과" 또는 "차단" 판정, 하나라도 불명확하면 차단 + 수정 제안만

차단이 나오면 멈추고 지적 부분부터 고친다. 통과여도 테스트는 직접 돌려 `N passed`로 전부 통과해야 하며 하나라도 실패하면 다음 단계 금지.
```bash
python -m pytest -q
```

### STEP 4. 6개월 백테스트 (15분)
```bash
python main.py backtest --months 6
```
결과 표와 `results/`의 CSV·그래프. 수익률보다 먼저 볼 것:
- 거래가 실제로 발생했는지(0건이면 신호 조건 오류)
- 수수료·슬리피지가 0으로 빠지지 않았는지
- 최대 낙폭이 15%를 넘으면 파라미터 조정, 샤프 지수 마이너스 전략은 다음 단계 금지
- 자산 하나가 수익을 거의 다 만들었다면 분산이 아니라 편중
리포트에는 자산별 총 거래 수·승률·평균 수익/손실·손익비·최대 낙폭·샤프·총 수익률, 상관 필터 켠 포트폴리오 합산 성과, 자산곡선 차트(`backtest_results.png`)가 있어야 한다. 슬리피지 기본 가정은 거래당 0.05%, 수수료 0(Alpaca 무료). 슬리피지를 0으로 두면 결과가 과대평가된다. 가정값을 바꿔 두 번 더 돌려 수익률 차이가 크지 않아야 한다(한쪽만 좋으면 운에 기댄 전략).
```bash
python main.py backtest --months 6 --slippage-bps 5
python main.py backtest --months 6 --slippage-bps 10
```
이후 누수 감사를 시킨다.

프롬프트 뼈대 D. 백테스트 누수 감사
- 지시: `results` 폴더의 CSV를 읽고 누수만 감사
- 확인할 것: 미래 가격 참조, 신호와 같은 봉에서의 체결, 수수료·슬리피지 누락, 자산별 거래시간 혼합, 빈 구간을 0으로 채운 부분, 같은 기간으로 파라미터를 맞추고 같은 기간으로 평가한 과최적화
- 제약: 수익 아이디어 금지, 오류 가능성만 높음/중간/낮음으로 보고

6개월은 모든 시장 국면을 담기에 짧아 이 검사는 합격증이 아니라 1차 걸러내기다.

### STEP 5. 2주간 모의투자 (하루 5분)
1. 주문 없이 계획만 출력(모의 모드 표시, 대상 자산, 예상 수량, 손절 거리, 위험 예산, "주문 건너뜀" 문구가 보여야 함)
```bash
python main.py paper --dry-run
```
2. 계획이 맞으면 모의계좌에서 한 번만 실행하고 상태 확인(포지션·잔고)
```bash
python main.py paper --once
python main.py status
```
3. 2주 동안 매일 확인: 같은 신호로 주문 두 번 들어가지 않았는지 / 미국 장 닫힌 시간에 ETF 주문이 막혔는지 / 비트코인과 ETF가 다른 일정으로 도는지 / 주문 거절·부분 체결·네트워크 재시도가 기록에 남는지 / 프로그램을 껐다 켜도 같은 신호를 다시 보내지 않는지 / 봇 포지션과 Alpaca 화면 포지션 일치
4. Alpaca 문서도 모의투자는 시장 충격, 지연으로 생기는 체결 차이, 주문 대기 순서, 규제 수수료, 배당을 반영하지 않는다고 명시 → 통과는 "수익이 난다"가 아니라 "코드가 안 깨진다"는 증거.

### STEP 6. 손실 한도 확인 (10분)
양보할 수 없는 5가지:
1. 거래당 최대 1%: 수량은 손절 폭이 정한다(수량을 먼저 정하고 손절을 끼워 맞추면 1% 한도가 깨짐)
```
위험 예산 = 현재 잔고 × 1%
주문 수량 = 위험 예산 ÷ (진입 가격 − 손절 가격)
```
2. ATR 기반 사이징: 조용한 날 포지션은 크고 요동치는 날 작게 → 잃을 금액은 일정
3. 상관 필터: SPY·QQQ가 둘 다 롱인데 BTC까지 롱을 열면 같은 방향 베팅을 세 배로 한 것
4. 하드 스톱, 예외 없음: 진입 시 손절이 정해지고 뒤로 옮기거나 없애거나 "조금만 더 버텨보자"로 여유를 주지 않음
5. 최대 낙폭 정지(서킷 브레이커): 고점 대비 10% 하락 시 전량 정리 후 사람이 수동 검토 전까지 정지. 잔고 최고점은 실행마다 파일에 저장(안 하면 재시작 때 기준이 초기화돼 무력화)
정지 장치 테스트(테스트 통과 + 정지 명령 뒤 상태가 `STOPPED`, 자동 재시작되면 안 됨):
```bash
python -m pytest tests/test_risk.py -q
python main.py stop --close-all
python main.py status
```

### STEP 7. 아침저녁 리포트 자동화 (15분)
1. 텔레그램 BotFather(https://t.me/BotFather)에서 `/newbot`으로 봇 생성·토큰 수령, 그 봇에 아무 메시지나 한 번 보낸 뒤 대화 ID 확인
2. `.env`에 두 줄 추가
```
TELEGRAM_BOT_TOKEN=여기에_봇_토큰
TELEGRAM_CHAT_ID=여기에_대화_ID
```
3. 전송 없이 미리보기
```bash
python report.py morning --dry-run
python report.py evening --dry-run
```
4. 내용이 비거나 두루뭉술하면 Claude Code에 항목을 채우게 한다.

프롬프트 뼈대 E. 리포트 내용 채우기
- 지시: `report.py`의 아침 브리핑·저녁 리포트를 항목대로 채울 것
- 아침 브리핑(7시, 200단어 이하): 5개 자산 오픈 포지션과 진입가·미실현 손익 / 어제 총 손익과 자산별 손익 / 시장 상황(VIX 수준, 지수 추세·횡보, 암호화폐 거래량 이상) / 최근 7일 승률 / 리스크 플래그(1% 손절 근접 포지션, 상관 필터가 신규 매매를 막는지, 고점 대비 낙폭 5% 초과)
- 저녁 리포트(21시, 200단어 이하): 오늘 체결 수와 자산 / 오늘 손익(금액과 자기자본 대비 %) / 베스트·워스트 거래 상세 / 현재 잔고 / 백테스트 기대치와 일치 여부 / 손절 걸린 거래와 작동 여부
- 제약: 숫자는 계산해서 넣고 지어내지 않음, 두 리포트 모두 200단어 이하

5. 내용이 맞으면 `.env`의 `TELEGRAM_DRY_RUN`을 `false`로 바꿔 실제 전송 1회. 텔레그램에 도착하면 성공.
```bash
python report.py morning
```
6. 예약 방법 1 — 서버 cron(컴퓨터/서버가 계속 켜져 있어야 함, 시간은 서버 기준이라 `date`로 확인). `crontab -e`에 입력, 저장 시 `crontab: installing new crontab`
```
0 8 * * * cd /절대경로/paper-trading-bot && .venv/bin/python report.py morning
0 20 * * * cd /절대경로/paper-trading-bot && .venv/bin/python report.py evening
```
7. 예약 방법 2 — Claude(Cowork) 예약 작업: 유료 플랜, 컴퓨터가 꺼져 있어도 원격 실행, 단 로컬 파일 접근 불가 → 봇 기록 파일을 읽어야 하면 cron
8. 주문 실행 자체는 예약에 넣지 않는다(예약은 리포트만). 주문 루프는 2주 수동 확인 뒤 따로 설계.

### STEP 8. 실계좌로 넘어가기 (20분)
전제(하나라도 비면 앞 단계로): 모의투자 2주 이상, 모의 결과가 백테스트 기대치에서 크게 벗어나지 않음, 최종 체크리스트 전부 체크, 정지 명령이 실제 작동함을 눈으로 확인.
1. `.env`를 실계좌 키로 바꾸고 3중 잠금을 연다(저장해도 출력 없음)
```
ALPACA_API_KEY=여기에_실계좌_키
ALPACA_SECRET_KEY=여기에_실계좌_시크릿
ALPACA_PAPER=false
ALPACA_LIVE_CONFIRM=I_UNDERSTAND_REAL_MONEY
```
2. 첫 실행은 한 사이클만(경고 배너, 현재 잔고, 한 번 매매 최대 손실액, 10초 카운트다운이 순서대로 나와야 함. 하나라도 안 나오면 STEP 2로 복귀)
```bash
python main.py live --once
```
3. 금액: Alpaca는 최소 입금액이 없다. 전부 잃어도 생활에 지장 없는 금액으로. 1% 룰이라 1,000만 원 계좌면 한 번에 최대 10만 원(원문 기준 $10,000 계좌에 $100).
4. 24시간 가동: VPS(월 $5~10, DigitalOcean·Railway)
5. 자동 재시작 — PM2: `pm2 list`에 `trading-bot`이 online이면 정상
```bash
npm install -g pm2
pm2 start .venv/bin/python --name trading-bot -- main.py live
pm2 save && pm2 startup
```
 또는 systemd: `/etc/systemd/system/trading-bot.service`
```
[Unit]
Description=Trading Bot
After=network.target

[Service]
WorkingDirectory=/절대경로/paper-trading-bot
ExecStart=/절대경로/paper-trading-bot/.venv/bin/python main.py live
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
등록 후 `systemctl status trading-bot`에 `active (running)`
```bash
sudo systemctl enable --now trading-bot
```
6. 첫 주는 축소 운영: 자산 1~2개로 시작해 리포트 숫자와 Alpaca 화면이 매일 일치하는지 확인 후 확대
7. 멈추는 법을 먼저 익힘: 실계좌에서도 정지 명령을 눌러 상태가 `STOPPED`, 포지션 0이 되는지 확인
```bash
python main.py stop --close-all
python main.py status
```

## 핵심 팁 · 주의사항
- 삼중 잠금(`ALPACA_PAPER=false` + `ALPACA_LIVE_CONFIRM=I_UNDERSTAND_REAL_MONEY` + `--live`) 중 하나라도 없으면 모의로 폴백
- 중단 기준: 최대 낙폭 15% 초과, 샤프 음수, 한 자산이 수익 독점. 지표 하나로 전략을 승인하지 말 것(샤프가 양수여도 낙폭·미래 데이터 참조·수수료 누락·과최적화 확인)
- 모의투자는 시장 충격·체결 지연·주문 대기 순서·규제 수수료·배당이 재현되지 않음 → 통과를 성과 인증으로 읽지 말 것
- 이 전략은 단순화된 교육용 예시(실제 퀀트 회사는 수년간 팀으로 다듬음). 빌린 돈으로 매매 금지, 손절 제거·포지션 임의 확대 금지, 전부 잃어도 되는 금액만, 세금·수수료는 본인 확인
- 키 값은 어디에도 출력·붙여넣기 금지(텔레그램 토큰 포함)
- 프로그래밍을 몰라도 되지만 읽고 판단은 필요(STEP 3 검수). 모르는 파일은 "이 파일이 무슨 일을 하는지 초보자 눈높이로 설명해줘"라고 질문
- 텔레그램이 안 올 때: 봇에게 직접 메시지를 보냈는지 → 대화 ID가 맞는지 → `TELEGRAM_DRY_RUN`이 false인지 순서로 확인

## 바로 쓰는 체크리스트
최종:
- [ ] 모의계좌 키만 넣었다 / 환경변수 없을 때 모의 기본값이 코드에 있다
- [ ] 실계좌 전환은 3중 잠금 뒤에만 열린다 / `.env`가 git 추적에서 빠졌다
- [ ] 테스트 전부 통과 / 백테스트에 수수료·슬리피지 포함
- [ ] 최대 낙폭 15% 이하 / 샤프 음수 전략은 중단
- [ ] 2주 모의에서 중복 주문·거래시간·재시작 문제 확인
- [ ] 거래당 1%와 고점 대비 10% 정지 장치 테스트
- [ ] 리포트 숫자 = Alpaca 화면 숫자
실계좌 전:
- [ ] 모의투자 2주 완주, 결과가 백테스트와 크게 어긋나지 않음
- [ ] 정지 명령이 실제 작동하는 것 확인
- [ ] 전부 잃어도 되는 금액으로 시작
- [ ] VPS와 자동 재시작 설정
- [ ] 첫 주 자산 1~2개로 축소 운영
- [ ] 손절을 옮기거나 없애지 않기로 결정
