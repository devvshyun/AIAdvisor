# 클로드에 PDF 올리면 토큰 2배, 무료 마크잇다운으로 줄이는 법
- 원문: https://lazyowen.com/guides/markitdown-pdf-token-saver
- 도구·주제: Microsoft MarkItDown · markitdown-mcp · Claude Desktop · 토큰 절약 / 문서 변환 (비용 절약, 13분 읽기, STEP 5개, 약 22분 실습, 2026-09-28 공개, MarkItDown v0.1.8 기준)
- 한 줄 요약: PDF/Word/Excel/PowerPoint를 글자만 남긴 마크다운으로 변환해 Claude에 올려 토큰을 줄이고, MCP로 Claude Desktop 대화 안에서 바로 변환하게 연결한다.

## 언제 쓰나
- 표/그림/장식이 많은 PDF를 Claude에 자주 올려 사용량이 빨리 닳을 때
- 이유: 공식 PDF 문서상 PDF는 페이지마다 이미지로 바꾸고 페이지 글자도 따로 뽑아 함께 넣음. 글자 토큰은 페이지당 보통 1,500~3,000 + 이미지 토큰이 추가 → 같은 페이지를 글자와 그림으로 두 번 읽는 셈. 마크다운(#, -, | 기호로 제목·목록·표를 표시하는 글자 형식)으로 바꾸면 이미지 몫이 빠짐.

## 준비물 / 필요 도구
- MarkItDown(Microsoft, MIT, GitHub 스타 187,355개: 2026-09-28 확인): https://github.com/microsoft/markitdown · PyPI https://pypi.org/project/markitdown/
- markitdown-mcp: https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp
- Python 3.10~3.14 (https://www.python.org/downloads/). 맥 기본 3.9.6이면 새 버전을 먼저 설치(그대로 깔면 옛 시험판 0.0.1a1이 깔림)
- Claude Desktop https://claude.ai/download · Claude Code 설치 https://code.claude.com/docs/en/setup · Claude PDF 지원 문서 https://platform.claude.com/docs/en/build-with-claude/pdf-support · 로컬 MCP 연결 https://modelcontextprotocol.io/docs/develop/connect-local-servers · venv https://docs.python.org/3/library/venv.html · Docker(선택)
- 비용: 설치·변환 무료. 스캔본을 읽는 `markitdown-ocr` 플러그인은 무료지만 이미지 인식용 AI 모델 키가 별도로 필요.
- 명령은 맥 기준(윈도우 대응표는 아래).

## 단계별 방법
### 보조 프롬프트: 설치~첫 변환~연결 준비 위임 (프롬프트 뼈대, Claude Code용)
- 역할: MarkItDown 설치·첫 변환·Claude Desktop 연결 준비 담당. 슬롯: [변환할 파일 예: ~/Downloads/report.pdf]. OS·셸·파이썬 버전은 직접 확인.
- 작업: ① `python3 --version` 3.10 이상 확인, 3.9 이하면 설치 중단하고 python.org 안내(윈도우면 같은 순서를 윈도우 명령으로) ② `~/markitdown`에 가상환경이 없을 때만 mkdir → venv → activate → `pip install 'markitdown[all]'` ③ `markitdown --version` 후 변환하고 `ls -l report.pdf report.md`로 크기 비교 ④ 같은 venv에 `pip install markitdown-mcp`, `which markitdown-mcp` 전체 경로가 들어간 설정 조각을 만들고 쓰임새 안내.
- 제약: Claude Desktop 설정 파일은 직접 고치지 말고 넣을 내용만 표시, sudo·전역·venv 밖 설치는 사전 질문, 덮어쓰기·비밀키 출력 금지. 검증: `markitdown --version` 숫자 출력 + .md 크기 > 0, 실패 시 완료 보고 금지.

### Quick Start
먼저 `python3 --version`이 3.10 이상인지. 3.9 이하면 STEP 2부터.
```bash
mkdir -p ~/markitdown && cd ~/markitdown
python3 -m venv .venv
source .venv/bin/activate
pip install 'markitdown[all]'
markitdown --version
```
성공: 마지막 줄에 `markitdown 0.1.8` 같은 버전. (가상환경 = 이 도구 전용 작은 파이썬 방, 지워도 다른 곳에 영향 없음)

### STEP 1. PDF가 토큰을 두 배로 먹는 이유 (2분)
위 "언제 쓰나"의 설명. 표도 `|`로 옮겨지지만 칸이 합쳐질 때가 있어 STEP 4에서 답을 직접 비교.

### STEP 2. 설치 (5분)
1. 확인: `python3 --version` → 3.10~3.14면 진행, 3.9.6(맥 기본)이면 새 버전 먼저.
2. 설치:
```bash
mkdir -p ~/markitdown && cd ~/markitdown
python3 -m venv .venv
source .venv/bin/activate
pip install 'markitdown[all]'
```
   성공: 줄 앞에 `(.venv)`, 오류 없이 프롬프트 복귀. 이미 설치돼 있으면 건너뜀.
   - ❌ `pip install markitdown[all]` (맥 zsh에서 `no matches found`) ✅ `pip install 'markitdown[all]'` (작은따옴표)
3. 윈도우(명령 프롬프트) 대응:
| 맥 | 윈도우 |
|---|---|
| `python3` | `py` |
| `mkdir -p ~/markitdown && cd ~/markitdown` | `mkdir %USERPROFILE%\markitdown` 다음 `cd %USERPROFILE%\markitdown` |
| `source .venv/bin/activate` | `.venv\Scripts\activate.bat` |
| `pip install 'markitdown[all]'` | `pip install "markitdown[all]"` (큰따옴표) |
| `markitdown report.pdf \| pbcopy` | `markitdown report.pdf \| clip` |
| `which markitdown-mcp` | `where markitdown-mcp` |
   - 폴더 일괄 변환 `for` 명령은 맥 전용 → 윈도우는 파일마다 실행. 설정 파일 안 윈도우 경로의 역슬래시는 `\\`.

### STEP 3. 파일을 마크다운으로 변환 (3분)
새 터미널에서는 가상환경부터 켜고 파일 폴더로 이동:
```bash
source ~/markitdown/.venv/bin/activate
cd ~/Downloads
```
| 하고 싶은 것 | 명령 |
|---|---|
| 파일 하나를 .md로 저장 | `markitdown report.pdf -o report.md` |
| 결과를 바로 복사 | `markitdown report.pdf \| pbcopy` |
| 폴더 안 PDF 전부 | `for f in *.pdf; do markitdown "$f" -o "${f%.pdf}.md"; done` |
- 성공: 변환은 아무 메시지 없이 끝나고 같은 폴더에 `.md` 생성. `pbcopy`는 화면에 아무것도 안 나오고 클로드에 붙여넣으면 변환 글이 들어감.
- 다른 형식(파일명만 변경): `markitdown 계약서.docx -o 계약서.md`, `markitdown 매출.xlsx -o 매출.md`, `markitdown 발표.pptx -o 발표.md`
- ❌ `markitdown 내 보고서.pdf` (공백에서 끊김) ✅ `markitdown "내 보고서.pdf" -o "내 보고서.md"`

### STEP 4. 절약량 직접 재기 (2분)
```bash
ls -l report.pdf report.md
```
- 다섯 번째 칸이 바이트. 실측 예: 한 쪽짜리 표 보고서 PDF 47,045바이트 → .md 441바이트 (문서마다 크게 다름, 표·그림·장식 많을수록 큼).
- 파일 크기는 빠른 신호일 뿐 토큰 수와 같지 않음. 진짜 확인: 새 대화 1에 PDF 원본, 새 대화 2에 .md를 올리고 같은 질문("이 문서의 핵심 숫자 세 개는?")을 해 답이 같은지 비교. 표 문서는 .md를 열어 칸 합쳐짐·숫자 어긋남 확인.

### STEP 5. Claude Desktop에 MCP 연결 (10분)
MCP = 클로드가 내 컴퓨터 도구를 불러 쓰게 하는 연결 규격.
1. 설치와 경로 확인:
```bash
source ~/markitdown/.venv/bin/activate
pip install markitdown-mcp
which markitdown-mcp
```
   성공: `/Users/내이름/markitdown/.venv/bin/markitdown-mcp` 같은 전체 경로 → 복사.
2. Claude 메뉴 → `Settings…` → `Developer` 탭 → `Edit Config`로 `claude_desktop_config.json` 열기, 아래 내용 입력(`command`에 복사한 경로):
```json
{
"mcpServers": {
"markitdown": {
"command": "/Users/내이름/markitdown/.venv/bin/markitdown-mcp",
"args": []
}
}
}
```
   - 이미 `mcpServers`가 있으면 전체를 덮지 말고 `"markitdown": {...}`만 쉼표로 이어 붙이기.
3. 저장 후 Claude Desktop 완전 종료 → 재실행. 입력창 왼쪽 아래 버튼 → `Connectors` → `Manage connectors`에 markitdown이 보이면 성공. 안 보이면 빠진 쉼표·중괄호부터 확인.
4. 요청: `markitdown 도구로 file:///Users/내이름/Downloads/report.pdf 를 마크다운으로 바꿔서 보여 주세요.` → 도구 사용 허락 후 변환 글 표시.
   - ❌ PDF를 대화창에 첨부하고 "마크다운으로 바꿔 줘" (첨부 순간 PDF 원본이 그대로 들어감) ✅ 첨부하지 말고 파일 경로를 적어 도구로 변환 요청.
5. (선택) Docker 방식(Microsoft 권장). 도커=분리된 상자(컨테이너)에서 실행. 이름 충돌을 피해 `~/markitdown-src`로 받음:
```bash
git clone https://github.com/microsoft/markitdown.git ~/markitdown-src
cd ~/markitdown-src/packages/markitdown-mcp
docker build -t markitdown-mcp:latest .
```
   설정의 markitdown 항목을 교체(경로는 변환할 파일이 있는 내 폴더로):
```json
{
"mcpServers": {
"markitdown": {
"command": "docker",
"args": ["run", "--rm", "-i", "-v", "/Users/내이름/Downloads:/workdir", "markitdown-mcp:latest"]
}
}
}
```
   요청 경로는 `file:///workdir/report.pdf`.

## 핵심 팁 · 주의사항 (솔직한 한계)
- ⚠️ 스캔 PDF는 뽑을 글자가 없어 거의 비어 나옴. `markitdown-ocr` 플러그인은 AI 모델 키가 없으면 조용히 아무 일도 안 함.
- ⚠️ 다단 레이아웃·겹친 표는 읽는 순서가 틀어지거나 칸이 붙을 수 있음(실측에서도 두 칸이 한 칸에 붙음) → .md 확인.
- 머리글·꼬리말·페이지 번호는 글자라 남음 → 필요 없으면 직접 삭제.
- 도면·디자인 시안처럼 모양이 내용인 파일은 변환하지 말 것(시각 정보 소실).
- ⚠️ MCP 서버는 내 계정이 열 수 있는 파일을 모두 읽을 수 있음 → 내 컴퓨터 안에서만 쓰고 다른 기기 접속 허용 금지.
- 절감 폭은 문서마다 다르므로 같은 질문 비교로 검증.

## 바로 쓰는 체크리스트
- [ ] Python 3.10+ 확인 (3.9면 새 버전 설치)
- [ ] venv 생성 + `pip install 'markitdown[all]'` + `markitdown --version`
- [ ] 샘플 PDF 변환, `ls -l`로 크기 비교, 같은 질문으로 PDF vs .md 답변 비교
- [ ] 스캔본/다단 레이아웃/표 여부 확인 후 .md 내용 점검
- [ ] (선택) `pip install markitdown-mcp`, `which`로 얻은 전체 경로를 config에 등록, Claude Desktop 완전 재시작, Connectors 확인
