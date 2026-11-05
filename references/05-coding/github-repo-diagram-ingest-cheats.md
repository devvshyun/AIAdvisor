# GitHub 레포를 한눈에 읽는 치트키 사이트 2곳
- 도구·주제: GitDiagram · GitIngest (+ ChatGPT/Claude) · 낯선 레포 빠르게 파악 (코딩, 12분 읽기, STEP 4개, 약 14분 실습, 2026-10-08 갱신)
- 한 줄 요약: GitHub 주소의 `hub` 세 글자만 바꿔(`github` → `gitdiagram`/`gitingest`) 레포 구조를 그림(GitDiagram)으로 보고, 전체를 AI용 텍스트(GitIngest)로 묶어 ChatGPT/Claude에 붙여 질문한다.

## 언제 쓰나
- 처음 보는 오픈소스 레포의 구조를 빠르게 파악하거나, AI에게 레포 전체를 읽혀 질문하고 싶을 때
- 도구는 코드를 대신 고쳐 주지 않음. 레포=프로젝트 하나의 코드·파일이 모인 GitHub 저장소.

## 준비물 / 필요 도구
- GitDiagram: https://gitdiagram.com (구조를 상자·화살표로, GitHub https://github.com/ahmedkhaleel2004/gitdiagram, 스타 17.7k, MIT)
- GitIngest: https://gitingest.com (레포를 AI용 텍스트 하나로, GitHub https://github.com/coderamp-labs/gitingest, 스타 15.8k, MIT, coderamp-labs 관리) · PyPI https://pypi.org/project/gitingest/
- ChatGPT 또는 Claude (새 대화창)
- 터미널 버전만 Python 3.8+ (https://www.python.org/downloads/), pipx (https://pipx.pypa.io/stable/how-to/install-pipx.html)
- 웹 브라우저만 있으면 맥·윈도·폰 어디서나 가능, 공개 레포는 로그인 없이 무료
- GitHub 토큰 만들기(비공개 레포용): https://github.com/settings/personal-access-tokens

## 단계별 방법
### Quick Start. 바로 열어 보기
- 구조 그림: https://gitdiagram.com/coderamp-labs/gitingest
- AI용 텍스트: https://gitingest.com/coderamp-labs/gitingest
- 성공: 첫 주소는 상자·화살표 그림, 둘째 주소는 파일 수(Files analyzed)·예상 토큰 수(Estimated tokens, AI가 글을 자르는 단위) 요약 칸.

### STEP 1. GitDiagram으로 구조 그림 (2분)
1. 궁금한 레포 첫 화면을 열기 (`github.com/만든사람/레포이름`).
2. 주소창에서 `github`의 `hub` 세 글자를 `diagram`으로 교체 → 엔터.
   - ❌ `diagram.com/coderamp-labs/gitingest` (github 전체를 지움) ✅ `gitdiagram.com/coderamp-labs/gitingest` (hub 세 글자만 바꿈)
3. 폴더 묶음별 상자·화살표 그림이 나옴. 그림 위 `Info`에서 `21 components · 25 connections`처럼 부품·연결 수 확인.
4. 상자 클릭 → 연결된 파일/폴더로 이동(예: main.py). `Export`에서 `Download PNG` 또는 `Copy Mermaid`(그림을 글자로 적은 형식).
- Info의 Connections 옆 `not checked`는 AI가 만든 그림이라 연결을 검증하지 않았다는 표시 → 큰 흐름 파악용.

### STEP 2. GitIngest로 텍스트 하나로 묶기 (2분)
1. 같은 레포 주소에서 `hub`를 `ingest`로 교체: `gitingest.com/coderamp-labs/gitingest` → 엔터 → 몇 초 대기.
2. 요약 칸 예(레포가 바뀌면 숫자는 달라도 정상):
```
Repository: coderamp-labs/gitingest
Commit: 4e259a02fe72115bee538271622f1234a81c8e1a
Files analyzed: 109

Estimated tokens: 99.4k
```
3. 버튼/옵션:
   - `Copy all`: 요약·폴더 구조·파일 내용을 한 번에 복사
   - `Download`: 텍스트 파일로 받기(대화창 첨부용)
   - `Include files under: 50kB`(기본): 이보다 큰 파일은 제외 → 큰 파일이 핵심이면 값을 올리거나 터미널 버전 사용
   - `Exclude`: `tests/`, `docs/`처럼 뺄 폴더를 적고 `Ingest`를 다시 눌러 토큰 수 줄이기
- 요약 칸이 낮아 Estimated tokens 줄은 칸 안을 아래로 내려야 보임.

### STEP 3. ChatGPT/Claude에 붙여 질문 (5분)
1. STEP 2에서 `Copy all`.
2. ChatGPT나 Claude 새 대화창을 열고, 안내 프롬프트를 먼저 붙인 뒤 그 아래에 복사한 텍스트를 붙임. 회사 코드면 외부 AI에 넣기 전 사내 규칙 확인.
3. 안내 프롬프트 뼈대: 역할=처음 보는 레포를 초보자에게 설명하는 안내자. 맥락=아래에 GitIngest 텍스트(Summary → Directory structure → 파일 내용)가 붙어 있음. 슬롯=[내 목표 한 줄]. 작업=① Summary·Directory structure를 읽고 레포가 하는 일을 3문장으로 ② 처음 실행되는 파일과 핵심 폴더 3곳을 경로로 ③ 목표에 맞는 읽기 순서 5개 이내 ④ 모르는 용어 한 줄 풀이와 다음 할 일. 제약=텍스트에 없는 경로 지어내기 금지, 불확실하면 추정이라고 표시, 코드 수정 금지, 비밀키처럼 보이는 값 출력 금지. 출력=한 줄 요약, 핵심 폴더 3곳(경로·역할), 읽는 순서, 용어 풀이. 검증=답의 모든 경로를 `Directory structure:` 트리와 하나씩 대조, 없으면 완료 보고 금지.
4. 질문 하나만 할 때 짧은 형태: `아래는 GitIngest 로 묶은 레포 전체입니다. 이 레포에서 처음 실행되는 파일이 어디인지 경로로 알려 주고, 그 파일이 하는 일을 세 문장으로 설명해 줘. 아래 텍스트에 없는 경로는 쓰지 마.`
   - ❌ `이 코드 설명해 줘` (README 재낭독 수준) ✅ `처음 실행되는 파일이 어디인지 경로로 알려 줘` (직접 대조 가능)
5. 경로 확인: 답의 경로를 텍스트의 `Directory structure:` 트리에서 찾기. 지어냈다면 Exclude로 범위를 줄여 다시 묶고 새 대화에서 재질문.

### STEP 4. 터미널 묶기·비공개 레포 (5분, 선택)
웹으로 충분하면 건너뜀. `python3 --version`이 3.8 이상인지 확인.
```bash
pipx install gitingest
```
- 성공 시 마지막 줄 `done! ✨ 🌟 ✨`. 이미 설치돼 있으면 생략.
- pipx 없음(맥): `brew install pipx` (brew 없으면 https://brew.sh/ 의 설치 명령 먼저)
- pipx 없음(윈도): PowerShell에서 `py -m pip install --user pipx` → 경고에 나온 설치 폴더에서 `.\pipx.exe ensurepath` 실행 후 창 새로 열기
- PATH 경고: `pipx ensurepath` 한 번 실행 후 터미널 재시작
```bash
gitingest --help
gitingest https://github.com/octocat/Hello-World
```
- `--help` 첫 줄에 `Usage: gitingest [OPTIONS] [SOURCE]`. 실행 성공: `Analysis complete! Output written to: digest.txt`, 현재 폴더에 `digest.txt` 생성.
- 터미널 버전은 폴더 주소(`/tree/main/폴더`)만 넣어 묶을 수도 있음.
- 비공개 레포: GitIngest 웹은 `Private Repository`를 켜고 GitHub 토큰 입력(사이트는 토큰을 저장하지 않는다고 밝힘). GitDiagram은 `Private Repos` 버튼 → `Use a personal access token instead` → 토큰 입력. 토큰은 읽기 권한만, 회사 코드면 사내 규칙 확인. (GitHub 토큰은 AI의 "토큰"과 이름만 같은 별개.)

### 주소 바꾸기 사이트 4곳 더
- ExplainGitHub: `github.com` → `explaingithub.com` (https://explaingithub.com/)
- GitReverse: `hub` → `reverse`로 바꾸면 레포가 AI에 줄 프롬프트로 변환 (https://www.gitreverse.com/)
- Uithub: `github.com` → `uithub.com` 예: `uithub.com/octocat/Hello-World` (https://uithub.com/)
- github.dev: 주소의 `.com` → `.dev`, 또는 레포 화면에서 키보드 `.`(마침표) → 브라우저 코드 편집기 (https://github.dev/)

## 문제 해결
- 주소를 바꿨는데 GitHub 화면 그대로: 주소창 자동 완성이 되돌린 것 → 바꾼 뒤 끝에 커서를 두고 엔터.
- 파일 화면에서 바꾸면 엉뚱한 결과: 레포 첫 화면 주소에서 바꾸는 게 가장 확실.
- 토큰 수가 너무 큼: Exclude로 테스트·문서 폴더 제외 후 재묶기(터미널은 폴더 주소만).
- AI가 일부만 읽은 듯함: Download한 파일을 첨부하거나 범위를 줄여 다시 묶기.

## 핵심 팁 · 주의사항
- ⚠️ GitDiagram 그림은 AI 생성이라 연결이 검증되지 않음(`not checked`) → 큰 흐름용.
- ⚠️ GitIngest는 기본 50kB 초과 파일을 제외.
- ⚠️ AI가 없는 경로를 지어낼 수 있음 → 경로를 `Directory structure`로 대조.
- ⚠️ 회사/비공개 코드를 외부 사이트·AI에 넣기 전 사내 규칙 확인, 토큰은 읽기 권한만.

## 바로 쓰는 체크리스트
- [ ] 대상 레포 첫 화면 URL 복사
- [ ] `hub`→`diagram`으로 바꿔 구조 그림 확인 (Info 확인)
- [ ] `hub`→`ingest`로 바꿔 Copy all, 토큰 수 확인 (필요시 Exclude)
- [ ] 새 AI 대화에 안내 프롬프트+텍스트 붙이고 질문, 경로는 Directory structure로 대조
- [ ] 필요 시 `pipx install gitingest`로 로컬 `digest.txt`
