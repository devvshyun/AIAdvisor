# 클로드로 업체 연락처 수천 개를 무료로 모으는 법
- 도구·주제: ScrapeGraphAI + Ollama + Claude Code · 공개 연락처 수집 / 영업 리스트
- 한 줄 요약: 무료 오픈소스 ScrapeGraphAI와 내 컴퓨터에서 도는 무료 로컬 모델(Ollama)로 웹페이지의 공개 업체 연락처만 골라 CSV로 모으고, 매일 아침 자동 실행되게 한다. (2026-08-19 공개, 읽는 데 10분, 따라 하면 약 58분, STEP 7개)

## 언제 쓰나
- 영업할 곳을 찾으려 업체 홈페이지를 하나씩 열어 이메일·전화번호를 옮겨 적는 일(하루를 통째로 소모)을 대신 시키고 싶을 때
- 업종별 공개 업체 목록 페이지에서 회사명/담당자/이메일/전화/홈페이지/지역을 표로 쌓고 싶을 때
- 활용 예: 업종별 협회 회원사 목록·산업 디렉터리, 지역·업종별 지역 업체 목록, 박람회 참가사·발표자 페이지, 오픈마켓·대행사의 제휴사 목록, 내가 파는 문제로 사람을 뽑고 있는 회사를 찾는 채용 공고

## 준비물 / 필요 도구
- ScrapeGraphAI: https://scrapegraphai.com/ · GitHub https://github.com/ScrapeGraphAI/Scrapegraph-ai · 문서 https://docs.scrapegraphai.com/introduction · PyPI https://pypi.org/project/scrapegraphai/
- just-scrape(터미널 명령어 도구): https://github.com/ScrapeGraphAI/just-scrape
- Ollama(AI 모델을 내 컴퓨터에서 돌리는 무료 프로그램, 인터넷 회사 서버 미경유): https://ollama.com/
- Python 3.12 이상(낮으면 설치 명령이 실패): https://www.python.org/downloads/
- Playwright(브라우저 조종, `playwright install`로 설치 — 글자가 나중에 그려지는 사이트를 읽으려면 브라우저를 직접 띄워야 함)
- Claude Code(스크립트 생성용, 선택)
- 비용: 로컬 모델이라 건당 비용 0(컴퓨터 자원·시간만). 클라우드 모델을 쓰면 별도 과금.
- 용어: 가상환경(venv) = 이 폴더 전용 설치 공간(다른 프로그램과 충돌 방지)

## 단계별 방법
### 프롬프트 뼈대 A. 설치·검증 위임 (Claude Code, 선택)
- 목적: ScrapeGraphAI·Ollama 설치와 동작 검증
- 역할: ScrapeGraphAI 설치·연결 검증 담당. 사용자는 초보
- 슬롯: [운영체제와 셸], [기술 스택(예: 파이썬만 쓰는 빈 폴더)], [목표 한 줄(예: 업체 목록에서 이메일·전화를 표로 모으기)]
- 작업 4단계: ① `python3 --version`(3.12+), `pip show scrapegraphai`, `ollama --version` 확인(이미 있으면 버전만) ② 새 폴더에 가상환경 후 `pip install scrapegraphai`, `playwright install`, Ollama가 없으면 공식 사이트 설치 안내 후 `ollama pull llama3.1` ③ `ollama serve`를 켠 상태에서 공개 페이지 하나를 대상으로 한 테스트 스크립트를 실행해 빈 값이 아닌 실제 데이터인지 확인 ④ 도구와 사용법을 5줄 이내로 설명
- 제약: 시스템 전체가 아니라 반드시 가상환경 안에 설치, 기존 파일·설정 덮어쓰기 금지, API 키 값 출력 금지, 공개된 연락처만 대상으로 이용약관·robots.txt 준수
- 출력: 실행 명령, 파이썬·패키지 버전, 새 폴더·파일, 남은 오류
- 검증: `pip show scrapegraphai`가 버전을 출력, `curl http://localhost:11434/api/tags`가 모델 목록 반환, 테스트 스크립트가 실제 데이터를 출력. 하나라도 실패하면 완료 보고 금지

### Quick Start
수집 도구와 브라우저 조종 프로그램 설치
```bash
pip install scrapegraphai
playwright install
```
오류 없이 프롬프트가 돌아오면 성공(브라우저 다운로드로 몇 분 소요). 이어서 무료 모델 준비(serve 창은 켜 둔 채로 유지, 꺼지면 수집 실패)
```bash
ollama pull llama3.1
ollama serve
```
새 터미널 창에서 확인(첫 줄은 버전, 둘째 줄은 모델 목록)
```bash
pip show scrapegraphai
curl http://localhost:11434/api/tags
```

### STEP 1. 준비물 확인 (3분)
1. 버전 확인(3.12 이상이어야 함. 낮거나 `command not found`면 python.org에서 설치 후 터미널 재시작)
```bash
python3 --version
```
2. 작업 폴더와 가상환경 생성. 성공하면 터미널 줄 맨 앞에 `(venv)`가 붙음.
```bash
mkdir lead-scraper && cd lead-scraper
python3 -m venv venv
source venv/bin/activate
```
윈도우는 마지막 줄 대신 `venv\Scripts\activate`.

### STEP 2. 설치 (10분)
설치 방법은 세 가지(파이썬이 있으면 pip, 클로드 코드를 쓰면 위임이 편함). 가상환경이 켜진 상태에서:
```bash
pip install scrapegraphai
playwright install
```
`Successfully installed scrapegraphai...`가 나오고 브라우저 다운로드가 끝나면 프롬프트가 돌아온다.

Claude Code에 맡기는 방법(가상환경 생성부터 테스트까지 자동):
프롬프트 뼈대 B. 저장소 설치 위임
- 요청: https://github.com/ScrapeGraphAI/Scrapegraph-ai 저장소를 새 폴더에 설치, 가상환경 생성, 패키지와 playwright 브라우저까지 설치, 페이지 하나를 실제로 긁어 보는 테스트 스크립트를 만들어 실행
- 성공: 만든 테스트 스크립트가 실제 웹페이지 내용을 글자로 출력

### STEP 3. 무료 모델 연결 (8분)
수집한 줄마다 돈이 나가면 목록을 크게 만들 수 없으므로 비용을 0으로 만드는 핵심 단계.
1. https://ollama.com/ 에서 설치 후 모델을 받고 켠다. 내려받기 진행 막대가 차고, serve는 로그가 흐르며 창이 계속 켜져 있어야 한다. 작업은 새 터미널에서.
```bash
ollama pull llama3.1
ollama serve
```
2. 새 창에서 연결 확인: 목록에 `llama3.1`이 보이면 성공(아무것도 안 나오면 serve 창이 꺼진 것)
```bash
curl http://localhost:11434/api/tags
```

### STEP 4. 한 페이지로 시험 (10분)
진짜 수집 전에 페이지 하나로 동작을 확인한다. `test.py`로 저장:
```python
from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "model": "ollama/llama3.1",
        "model_tokens": 8192,
        "base_url": "http://localhost:11434",
    },
    "verbose": True,
    "headless": True,
}

scraper = SmartScraperGraph(
    prompt="회사 이름, 담당자 이름, 공개된 이메일, 전화번호, 홈페이지 주소, 지역을 모두 뽑아 줘.",
    source="https://scrapegraphai.com/",
    config=graph_config,
)

print(scraper.run())
```
`prompt`에는 뽑을 항목을 한국어로, `source`에는 읽을 페이지 주소를 넣는다.
```bash
python test.py
```
중괄호로 둘러싸인 결과가 찍히면 성공. 빈 값만 나오면 대부분 STEP 2의 `playwright install`을 건너뛴 경우.
용도별 그래프 종류(`SmartScraperGraph` 자리를 교체):
| 종류 | 하는 일 |
|---|---|
| SmartScraperGraph | 페이지 한 개에서 원하는 항목 추출 |
| SearchGraph | 웹을 검색한 뒤 상위 결과들을 읽음 |
| SmartScraperMultiGraph | 주소 여러 개에 같은 지시 적용 |
| ScriptCreatorGraph | 다시 쓸 수 있는 수집 스크립트를 대신 생성 |

### STEP 5. 연락처 목록 만들기 (15분)
프롬프트 뼈대 C. 연락처 수집기 작성 (Claude Code)
- 목적: 이 폴더의 ScrapeGraphAI로 업체 목록 페이지에서 연락처를 모아 `leads.csv`로 저장하는 수집기 작성
- 슬롯: [업체 목록 페이지 주소]
- 업체별 추출 항목: 회사 이름, 담당자 이름, 직함, 공개 이메일, 전화번호, 홈페이지, 지역, 출처 주소
- 규칙: 목록 1페이지만 보지 말고 마지막 페이지까지 넘겨 가며 수집 / 공개된 연락처만 수집하고 이메일 없는 줄은 건너뜀 / 홈페이지 주소가 같으면 중복으로 보고 하나만 유지 / `leads.csv`에 이어쓰기(없으면 새로 생성) / 새로 넣은 줄 수와 중복으로 건너뛴 줄 수를 화면에 출력
- 설정: 로컬 Ollama 모델을 써서 실행 비용이 들지 않게
- 성공: 스크립트를 만들어 실행하고 마지막에 몇 줄을 넣었는지 숫자로 보고

재사용 저장 요청(성공하면 `daily_leads.py` 생성):
```
이걸 daily_leads.py라는 이름으로 저장해서 다음에 다시 만들지 않고 바로 돌릴 수 있게 해 줘.
```

### STEP 6. 매일 아침 자동 실행 (7분)
Claude Code에 예약을 요청:
```
daily_leads.py를 매일 아침 8시에 실행해서 leads.csv에 이어쓰고,
실패하면 errors.log에 기록하도록 예약을 걸어 줘.
```
직접 등록하려면 맥·리눅스 터미널에서 `crontab -e` 후 아래 한 줄을 붙여넣는다(`0 8`이 아침 8시). `crontab -l`에 이 줄이 보이면 성공.
```
0 8 * * * cd ~/lead-scraper && ./venv/bin/python daily_leads.py >> run.log 2>&1
```
다른 업종은 대상 주소만 바꿔 다시 돌리면 됨.

### STEP 7. 결과 확인 (5분)
```bash
head -5 leads.csv
```
맨 윗줄에 항목 이름, 아래로 업체 정보가 쉼표로 구분돼 나오면 성공. 엑셀·구글 시트에서 바로 열린다.

## 핵심 팁 · 주의사항
- 지켜야 할 선: 공개된 연락처만 수집, 각 사이트의 이용약관과 robots.txt 준수, 한꺼번에 몰아치지 말고 요청 속도를 낮출 것, 메일을 보내기 시작하면 수신 거부 요청은 즉시 반영. 도구는 순식간에 커지지만 내 발신 평판은 그렇지 않다.
- `ollama serve` 창은 닫지 말 것(작업은 새 창에서)
- 글자가 나중에 그려지는 페이지는 Playwright 브라우저가 필요하므로 `playwright install` 완료 확인
- 복잡하거나 정리가 안 된 페이지는 큰 클라우드 모델이 더 정확할 수 있으나 건당 과금

## 문제 해결
- 결과가 계속 빈 값: 글자가 나중에 그려지는 페이지 → `playwright install`이 끝났는지 재확인
- 502 오류: `ollama serve` 창이 꺼졌거나 설정에서 `base_url` 줄이 빠진 경우
- `model not found`: `ollama list`의 이름과 설정의 모델 이름이 정확히 같아야 함, 먼저 `ollama pull`
- 정리가 뒤죽박죽인 페이지에서 값이 엉성: `model_tokens`를 올리거나, 그 페이지만 큰 클라우드 모델로 돌리고 나머지는 무료 모델 유지
- 설치 시 다른 프로그램과 충돌: 가상환경 밖에서 설치한 경우 → STEP 1로 돌아가 `(venv)`가 붙은 상태에서 재설치

## 바로 쓰는 체크리스트
- [ ] Python 3.12+ 확인, `lead-scraper` 폴더와 venv 생성(`(venv)` 확인)
- [ ] `pip install scrapegraphai` + `playwright install`
- [ ] Ollama `llama3.1` pull + serve(창 유지), `curl .../api/tags` 확인
- [ ] `test.py`로 단일 페이지 검증
- [ ] 수집기 생성(페이지네이션·중복 제거·이메일 필수) 후 `daily_leads.py`로 저장
- [ ] cron 등록(`crontab -l` 확인), `head -5 leads.csv` 확인
- [ ] 약관·robots.txt·요청 속도 제한·수신 거부 반영 준비
