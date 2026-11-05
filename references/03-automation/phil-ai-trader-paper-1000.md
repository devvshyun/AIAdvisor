# 클로드 트레이더 Phil
- 도구·주제: Claude Code · Phil(오픈소스) · Polymarket · AI 모의 트레이딩 / 자기개선 전략
- 한 줄 요약: Claude Code가 가상 $1,000으로 Polymarket 단기 시장을 모의 거래하고, 결과마다 전략 파일을 고쳐 git 커밋으로 남기는 실험 저장소를 돌리는 4단계. (2026-10-08 갱신, 읽는 데 10분)

## 언제 쓰나
- AI 에이전트가 거래 결과로 스스로 전략을 개선하는지 연구/관찰하고 싶을 때. 돈을 벌어 준다고 검증된 프로그램이 아님(수익 보장 도구 아님).

## 준비물 / 필요 도구
- 저장소: https://github.com/bennyjo/phil (Apache-2.0, GitHub 스타 186개, 개인 개발자). 포크 https://github.com/bennyjo/phil/fork
- 맥/리눅스 터미널, Python 3, Git, 로그인된 Claude Code (https://docs.claude.com/en/docs/claude-code), GitHub 계정. 별도 파이썬 패키지·API 키 불필요
- Polymarket: https://polymarket.com/
- 비용: Phil/시장 데이터 무료. 단 거래 사이클마다 Claude Code가 돌아 내 Claude 요금제 사용량을 소모.

## 단계별 방법
**Quick Start**: 포크를 만든 뒤 `YOUR-USERNAME`만 내 GitHub 아이디로 바꿔 실행. 성공하면 `Cloning into 'phil'`.
```
GH_ID=YOUR-USERNAME && git clone "https://github.com/$GH_ID/phil.git" && cd phil
```

1. **STEP 1 준비물 확인·포크 (5분)**
   ```
   python3 --version
   git --version
   claude --version
   ```
   - `Python 3.`, `git version`, `(Claude Code)` 줄이 차례로 보여야 함. claude 없으면 공식 문서대로 설치·로그인. 맥에서 python3/git이 없으면 개발자 도구 설치 안내를 따름.
   - 포크 페이지에서 `Create fork` 클릭. Phil이 사이클마다 고친 전략을 내 저장소로 push하므로 원본이 아닌 내 사본 필요.
2. **STEP 2 내려받고 성적표 열기 (3분)** — 이미 받았으면 clone 생략. phil 폴더 안에서:
   ```
   GH_ID=YOUR-USERNAME && git clone "https://github.com/$GH_ID/phil.git" && cd phil
   python3 core/score.py
   ```
   - 출력 예(값은 달라짐):
   ```
   settled=55 win_rate=0.473 pnl=$-4.33 roi=-0.016
   brier: agent=0.2581 market=0.1855 delta=0.0725 (behind market)
   ```
   - settled=정산된 가상 거래 수, pnl=가상 손익(운 좋은 연승만으로도 플러스 가능), brier delta=Phil의 확률과 시장 가격 중 누가 결과를 더 잘 맞혔는지의 점수 차(마이너스면 Phil이 더 잘 맞힘, `behind market`이면 아직 시장보다 못함).
   - ❌ pnl이 플러스니 돈 버는 AI라고 판단 → ✅ pnl 옆에 delta를 놓고 마이너스로 내려가는지 확인.
   - 가상 시작 자금: `config/`의 protected 파일 `sim_bankroll_usd` = 1,000달러. 사람만 수정 가능.
3. **STEP 3 가상 거래 사이클 (사이클당 몇 분)** — 주의: Claude Code를 사람 확인 없이 돌림. Phil은 phil 폴더 안 전략 파일 수정, 웹 검색, git commit 후 내 포크로 push까지 스스로 수행(허용 명령은 `python3 core/*`와 git 일부로 제한). 중요한 파일 없는 이 폴더에서만 실행.
   ```
   ./loop.sh 1
   ./loop.sh 10 45
   git log --oneline -10
   ```
   - `./loop.sh 1`=1회(성공: `=== cycle 1/1` 시작 줄, 몇 분 뒤 종료). `./loop.sh 10 45`=45분 간격 10회. 중단은 Ctrl+C(터미널을 닫거나 컴퓨터가 잠들면 멈춤).
   - `NOTE ... PEARL_CONNECT_STORE is unset`은 실거래 도구 미연결이라는 정상 안내.
   - ❌ `./loop.sh 1 --real`(진짜 돈 거래 경로, 예측 시장이 제한/불법인 지역 있음) → ✅ `./loop.sh 1`.
   - `git log`에서 `cycle:`(한 사이클, placed=새 가상 거래 수, settled=정산 수), `retro:`(정산 거래에서 배운 점) 커밋 확인. `deep-retro:`는 원작자 운영 환경의 하루 회고라 `./loop.sh`로는 생기지 않음.
4. **STEP 4 100회 실험·전후 비교 (며칠)**
   - 매일 `python3 core/score.py`로 기록: 가상 잔고(시작 1,000달러), 정산 수(settled), 이긴/진 수, pnl, brier delta, 전략 변경 수(커밋 수). 100번 뒤와 비교.
   - 포크에는 원작자의 지난 거래 기록이 들어 있음. 0부터 시작하려면 phil 폴더에서 `claude`를 열고 프롬프트: 현재 가상 거래 기록(journal)을 보관 폴더로 옮기고 가상 잔고 1,000달러에서 새로 시작, `core`와 `config` 폴더는 건드리지 말 것.
     - ❌ "기록 다 지워 줘" → ✅ 보관 폴더로 옮기라고 하고 건드리면 안 되는 폴더를 명시.
   - 100번 쌓이면 `journal/ledger.jsonl`을 처음 20번 / 마지막 20번으로 나눠 달라고 Claude Code에 요청 → 가상 손익, brier delta, 평균 예상 우위, 큰 전략 변경을 비교.
   - 판정: 마지막 20번 delta가 더 낮으면 예측 실력 향상. 손익만 좋아지고 delta가 그대로/나쁘면 운일 가능성. 100회는 표본이 작아 운이 섞이므로 delta가 계속 같은 방향으로 움직이는지도 확인.

**Phil이 배우는 순서(사이클당)**: ① 단기 예측 시장 약 300개를 값싼 보조 AI들이 점수화 ② 시장 가격과 차이가 큰 곳을 조사해 확률 산정 ③ 실시간 가격으로 가상 거래(돈 이동 없음) ④ 결과가 나오면 Polymarket 공식 결과로 정산하고 자기 확률과 산 가격 비교 ⑤ 틀린 이유를 적고 플레이북·리스크 규칙·시장 고르는 규칙을 고쳐 커밋. Phil이 고치는 곳 = `strategy/`(플레이북·리스크 규칙·도구), 사람만 고치는 곳 = `core/`(거래 엔진)와 `config/protected.json`(거래 1건 최대 $10 등).

**설치·첫 성적표 위임 프롬프트 뼈대(Claude Code 첫 메시지)**: 역할=Phil 설치·첫 성적표 확인 담당, 맥락=초보자, bennyjo/phil을 이미 포크함. 슬롯 `내 GitHub 아이디 = <아이디>`. 작업: ① 세 도구 버전 확인 ② phil 폴더가 없을 때만 위 clone 실행 ③ phil 폴더에서 `python3 core/score.py` ④ 첫 줄(settled·win_rate·pnl)과 둘째 줄 brier delta 의미를 초보자용으로 설명하고 다음에 내가 실행할 `./loop.sh 1`을 안내. 제약: `./loop.sh`는 직접 실행하지 말고 안내만, `--real`은 어떤 경우에도 사용·권유 금지, core·config 수정 금지, 설치/시스템 변경 전 질문, 비밀키 출력 금지. 검증: 첫 줄이 `settled=`, 둘째 줄이 `brier:`로 시작.

## 핵심 팁 · 주의사항
- 사이클은 사람 확인 없이 전략 수정·웹 검색·git commit/push를 수행. 그만두려면 phil 폴더와 포크를 삭제.
- `--real`은 실제 돈 거래 경로 — 가상으로만, 쓰지 말 것.
- pnl만으로 실력 판단 금지, brier delta와 함께 볼 것.
- 사이클마다 Claude 요금제 사용량을 소모 → 한도에 걸리면 간격을 늘리거나 횟수를 줄임.

## 문제 해결
- `no such file or directory: ./loop.sh` / `can't open file ... core/score.py`: phil 폴더 밖에서 실행 → `cd phil` 후 재실행.
- `push rejected` / `push still failing`: 원본 저장소를 클론했거나 내 포크에 올릴 권한 없음. 커밋은 로컬에 남아 있으니 포크 주소로 다시 받았는지 확인.
- 사용량 한도로 멈춤: 간격 확대·횟수 축소.

## 바로 쓰는 체크리스트
- [ ] `python3` / `git` / `claude` 버전 확인
- [ ] 저장소 포크 후 내 계정 주소로 클론
- [ ] `python3 core/score.py`로 초기 성적 확인
- [ ] `./loop.sh 1`로 1회 시험, `git log --oneline -10`으로 커밋 확인
- [ ] `--real`은 쓰지 않기
- [ ] (선택) journal을 보관 폴더로 옮기고 새로 시작
- [ ] 100회 후 `journal/ledger.jsonl` 처음/마지막 20회의 brier delta 비교
