# Graphify 가이드
- 도구·주제: Graphify + Claude Code · 비용 절약 / 코드 지식 그래프 (원문 제목: 클로드 코드가 파일부터 뒤지지 않게 만드는 Graphify 가이드)
- 한 줄 요약: 함수·클래스·호출 관계를 그래프로 만들어 Claude Code가 파일을 뒤지기 전에 그래프부터 조회하게 하는 11단계. (갱신 2026-08-06, 읽는 데 14분)

## 언제 쓰나
- 큰 코드베이스에서 질문마다 검색·파일 열기가 늘어 컨텍스트가 커질 때, 탐색 범위를 좁히고 싶을 때
- 그래프는 소스 읽기를 대체하는 게 아니라 범위를 좁힌 뒤 근거 파일만 확인하게 하는 보조 수단
- 지식 그래프 = 함수·클래스·파일을 노드로, 호출·임포트·상속을 엣지로 저장한 지도. 흐름: 프로젝트 파일 → 로컬 AST 분석 → `graph.json` → query/path/explain으로 범위 축소 → 필요한 원문만 확인.

## 준비물 / 필요 도구
- Graphify: https://github.com/Graphify-Labs/graphify · PyPI https://pypi.org/project/graphifyy/ (패키지명은 y 두 개 `graphifyy`, 명령은 `graphify`) · 문서(v8 브랜치) README.md / docs/how-it-works.md / BENCHMARKS.md
- Python 3.10+, uv, Claude Code(로그인). Claude Code 안내: https://docs.anthropic.com/en/docs/claude-code/overview
- 무엇을 하나: 코드는 tree-sitter AST로 로컬 분석(코드 전용 실행은 LLM 호출·외부 전송 없음). 문서·PDF·이미지는 현재 Claude Code 세션 모델 또는 별도 설정 모델 사용. 영상·음성은 선택 기능(전사는 로컬, 의미 연결은 모델 가능). 관계에는 신뢰도 태그 EXTRACTED / INFERRED / AMBIGUOUS.

## 단계별 방법
1. **STEP 1 준비물 확인 (3분)**
   ```
   python3 --version
   uv --version
   claude --version
   ```
   - Windows PowerShell은 `python --version`. 설치: macOS `brew install python@3.12 uv` / Windows `winget install Python.Python.3.12`, `winget install astral-sh.uv` / Ubuntu·Debian:
   ```
   sudo apt update
   sudo apt install -y python3 python3-venv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   - 설치 후 터미널 재시작. 기준: Python 3.10+, uv·Claude Code 버전 문자열 출력.
2. **STEP 2 Graphify 설치 (2분)**
   ```
   uv tool install graphifyy
   graphify --version
   graphify install
   ```
   - `graphify install`은 Claude Code가 `/graphify`를 알아보도록 사용자 영역에 스킬 등록. 성공 시 `graphify 0.x.x`와 `Done. Open your AI coding assistant and type: /graphify .`
   - `command not found` → `uv tool update-shell` 후 터미널 완전 재시작, `graphify --version`, `graphify install` 재실행.
   - 팀과 버전 관리하려면 프로젝트 루트에서 `graphify install --project`(개인은 전역 `graphify install`이 가장 단순).
3. **STEP 3 그래프 대상 정리 (3분)**: 프로젝트 폴더로 `cd /path/to/your-project`. `.gitignore` 자동 준수. 프로젝트 루트에 `.graphifyignore`(문법은 `.gitignore`와 동일):
   ```
   # .graphifyignore
   node_modules/
   dist/
   build/
   coverage/
   .next/
   .venv/
   vendor/
   *.min.js
   ```
   - 제외 후보 프롬프트 뼈대: 이 저장소에서 **생성물·캐시·외부 의존성만** 골라 `.graphifyignore` 후보를 제안, 실제 소스·설정·마이그레이션·테스트는 임의 제외 금지, 파일 수정 말고 후보와 이유만.
   - O: `src/`, 설정, 마이그레이션, 필요한 테스트 / X: `node_modules/`, 빌드 결과물, 캐시, 번들. 소스 폴더를 무작정 제외하면 그래프가 틀어지고, 테스트는 처음부터 빼지 말 것(팩토리·목 객체가 핵심 노드를 도배할 때만 `tests/`·`__tests__/` 제외 검토).
4. **STEP 4 첫 그래프 (1~10분)**: 프로젝트 루트에서 `claude` 실행 후 입력창(슬래시 명령, 일반 터미널 명령 아님):
   ```
   /graphify .
   /graphify . --mode deep
   ```
   - 기본 실행부터 권장. `--mode deep`은 문서·코드 사이 추론 관계를 더 적극적으로 만들고 싶을 때만. 코드 전용은 로컬 AST라 API 키 불필요, 문서·PDF·이미지가 섞이면 현재 세션 모델이 의미 분석. 파일이 아주 많으면 상위 폴더별 파일 수를 보여주고 범위 축소를 물음(애플리케이션 소스 폴더부터 선택).
   - 결과 `graphify-out/`: `graph.html`(브라우저 시각화), `GRAPH_REPORT.md`(핵심 노드·커뮤니티·의외의 연결·추천 질문), `graph.json`(쿼리가 읽는 영속 그래프).
5. **STEP 5 결과 확인 (2분)**
   ```
   test -s graphify-out/graph.json && echo "graph.json OK"
   test -s graphify-out/GRAPH_REPORT.md && echo "report OK"
   test -s graphify-out/graph.html && echo "graph.html OK"
   open graphify-out/graph.html
   xdg-open graphify-out/graph.html
   start graphify-out/graph.html
   ```
   - (macOS `open` / Linux `xdg-open` / Windows PowerShell `start`) 리포트에서 노드·엣지·커뮤니티 수 확인. 핵심 노드가 테스트 헬퍼·생성 코드뿐이면 STEP 3 제외 목록을 고쳐 재빌드. 노드 하나를 소스와 대조:
   ```
   /graphify explain "실제 클래스나 함수 이름"
   ```
   - 소스 파일·줄 위치·연결 관계·신뢰도 태그가 나오면 정상.
6. **STEP 6 그래프 우선 조회 강제 (1분)**: 첫 그래프 생성 후 프로젝트 루트에서
   ```
   graphify claude install
   ```
   - 프로젝트의 Claude Code 지시 파일과 PreToolUse 훅을 구성. 파일 읽기를 막지 않고 `query/explain/path`로 먼저 범위를 좁히라는 순서만 추가. 구현·수정 지점은 마지막에 소스로 재확인. 프롬프트 캐시 무효화를 줄이려면 `.claudeignore`에 추가(Git 추적과 별개):
   ```
   # .claudeignore
   graph.json
   graphify-out/
   ```
   - 항상 그래프부터 보게 하는 프롬프트 뼈대: "이 질문은 먼저 Graphify로 범위를 좁혀라 → 관련 노드·경로 → 근거가 필요한 소스만 열고 파일·줄 위치를 붙여 답하라. 질문: [코드베이스 질문]".
7. **STEP 7 query / path / explain (5분)**
   | 명령 | 언제 | 결과 |
   |---|---|---|
   | query | 흐름·구조를 넓게 찾을 때 | 질문 근처 서브그래프 |
   | path | 두 클래스·함수 사이 연결 | 최단 연결 경로 |
   | explain | 노드 하나의 역할 | 소스 위치와 주변 연결 |
   ```
   /graphify query "인증 요청이 데이터베이스까지 가는 흐름"
   /graphify query "결제 실패가 재시도되는 흐름" --dfs --budget 1500
   /graphify path "AuthService" "UserRepository"
   /graphify explain "AuthService"
   ```
   - 이름(AuthService 등)은 예시, 실제 심볼로 교체. 깊은 체인은 `--dfs --budget 1500`.
   - 그래프 생성 후엔 터미널에서도: `graphify query "show the auth flow"`, `graphify path "AuthService" "UserRepository"`, `graphify explain "AuthService"`.
   - 한국어 질문이 노드를 못 찾으면 코드의 영문 심볼 병기: `/graphify query "로그인 인증 AuthService UserRepository"`.
   - 템플릿 프롬프트 뼈대: ① 온보딩 — 핵심 노드·커뮤니티 확인 후 진입점·주요 요청 흐름·데이터 저장 경로 설명, 각 설명에 근거 파일·줄 위치, INFERRED는 추론 표시 ② 변경 영향 — `[바꾸려는 클래스/함수]` 수정 전 연결된 호출자·의존 대상, 직접/간접 구분, 열어볼 파일 우선순위 ③ 버그 추적 — `[에러 증상]` 관련 노드를 query로 찾아 실패 지점까지 경로 추적, EXTRACTED 우선·INFERRED는 소스 재확인 ④ 설계 이유 — `[기능 이름]`과 연결된 NOTE/WHY/ADR/RFC 근거, 왜 그렇게 설계했는지 중심, 출처 파일 첨부.
8. **STEP 8 갱신 (1~5분)**: 코드가 바뀌면 그래프도 갱신.
   ```
   /graphify . --update
   graphify hook install
   graphify hook status
   /graphify . --watch
   uv tool install "graphifyy[watch]"
   uv tool upgrade graphifyy
   graphify install
   graphify hook install
   ```
   - `--update`=변경 파일만 재처리. Git 훅은 커밋 후 코드 변경을 AST로 재분석(문서·이미지 변경은 `--update` 직접 실행). `--watch`는 별도 터미널에서 저장 시마다 반영, 의존성 오류면 `graphifyy[watch]` 재설치. 업그레이드 후엔 스킬과 Git 훅도 새 경로로 맞춤(마지막 3줄 순서).
9. **STEP 9 개인정보·비용 범위 (2분)**
   | 입력 | 기본 처리 | 외부 모델 가능성 |
   |---|---|---|
   | 코드 | tree-sitter AST, 로컬 | 코드 전용 기본 경로에서는 없음 |
   | Markdown·텍스트 | 의미 분석 | 있음 |
   | PDF·이미지 | 변환·의미 분석 | 있음 |
   | 영상·음성 | 로컬 전사 후 의미 분석 | 전사문 분석에서 있음 |
   - 코드 전용 저장소는 API 키 불필요. 외부 전송이 금지된 문서·이미지는 넣지 말 것. `.env`·개인 키·고객 데이터는 `.gitignore`와 `.graphifyignore`로 재확인. 결과물은 로컬 `graphify-out/`에 저장, 텔레메트리 없음(프로젝트 주장). 사내 보안 정책이 우선.
10. **STEP 10 토큰 절감 이해 (2분)**: "설치하면 무조건 70% 절감"은 공식 자료에서 확인되지 않음. 공개 재현 예시: 52파일 혼합 코퍼스 쿼리당 71.5배 적은 토큰, 4파일 5.4배, 6파일 소형 Python 약 1배. 작은 저장소는 원래 컨텍스트에 들어가 이득이 거의 없고, 큰 저장소에서 약 2,000토큰 안팎 서브그래프를 꺼낼 때 차이가 큼. 내 절감은 같은 작업의 실행 전후 실사용량으로 실측. Graphify가 해결하는 건 "매번 모든 파일을 읽는 동작"이 아니라 넓은 검색·불필요한 파일 열기를 줄이는 것.
11. **STEP 11 문제 해결** — 아래 섹션 참고.

## 핵심 팁 · 주의사항
- INFERRED 관계는 소스에서 다시 확인, EXTRACTED 우선(추론을 사실처럼 섞지 않기 위한 태그).
- ❌ 소스 폴더를 광범위하게 제외 / 테스트를 처음부터 제외 / 설치만으로 70% 절감 확정. ✅ 필요한 곳만 좁게 제외, 전후 실측.
- PyPI 패키지명 혼동 주의: `graphifyy`(y 두 개).
- 그래프 갱신을 잊으면 결과가 오래됨 → `--update` 또는 Git 훅.

## 문제 해결
- `graphify: command not found` → `uv tool update-shell` → 터미널 재시작 → `graphify --version`
- `ModuleNotFoundError: No module named 'graphify'`(pip와 다른 Python 환경 혼재) →
  ```
  uv tool uninstall graphifyy
  uv tool install graphifyy
  graphify install
  ```
- `/graphify`를 Claude Code가 못 알아봄 → `graphify install` 후 Claude Code 완전 종료·재시작
- `graphify extract .` 후 `graph.json`만 생김(CI/헤드리스 경로) → `graphify cluster-only .` 이어 실행 (Claude Code 안에서 `/graphify .`를 쓰면 리포트·HTML까지 생성)
- 쿼리 결과 0개/엉뚱함 → 실제 함수·클래스명 포함 `/graphify query "한국어 질문 ActualClassName actual_function"`, 오래됐으면 `/graphify . --update`
- 테스트 헬퍼가 핵심 노드를 도배 → 문제 하위 폴더만 좁게 제외(예: `tests/fixtures/`, `tests/generated/`) 후
  ```
  graphify extract . --force
  graphify cluster-only .
  ```
- Windows PowerShell에서 `/graphify .`가 경로 오류 → PowerShell에선 `graphify .`, Claude Code 입력창에선 `/graphify .`
- 제거: `graphify claude uninstall`(프로젝트 연동만) / `graphify uninstall`(모든 플랫폼 스킬) / `graphify uninstall --purge`(결과물까지 삭제, 되돌리기 어려움)

## 바로 쓰는 체크리스트
- [ ] Python 3.10+, uv, Claude Code 버전 확인
- [ ] `uv tool install graphifyy` → `graphify --version` → `graphify install`
- [ ] `.graphifyignore` 작성(생성물·캐시·의존성만)
- [ ] `/graphify .` 실행, `graphify-out/` 3개 파일(graph.html, GRAPH_REPORT.md, graph.json) 생성 확인
- [ ] `/graphify explain "실제 심볼"`로 소스 위치·연결 확인
- [ ] `graphify claude install` 적용, `.claudeignore`에 `graph.json`, `graphify-out/` 추가
- [ ] 코드 변경 후 `--update` 또는 `graphify hook install`
- [ ] INFERRED 관계 소스 검증, 토큰 절감은 전후 실측
