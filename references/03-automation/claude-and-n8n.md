# 클로드로 첫 n8n 에이전트 만드는 6단계
- 도구·주제: Claude(프로젝트) + n8n · 노코드 자동화 워크플로 생성 (2026-09-19 공개·검증, n8n v2.39.8, 본문 STEP 4개 · 약 23분)
- 한 줄 요약: Claude 프로젝트에 지시문과 샘플 워크플로 JSON을 넣어 두고, 만들고 싶은 자동화를 말로 적으면 n8n에 붙여넣을 JSON을 받는 방식으로 첫 자동화를 만든다.

## 언제 쓰나
- 메일 라벨링, 텔레그램 비서, 문서 기반 Q&A(RAG) 같은 자동화를 코딩 없이 n8n에서 만들고 싶을 때
- n8n 화면의 수백 개 노드에 압도되어 무엇을 어디에 놓을지 모를 때
- 영상의 "6단계"는 본문에서 준비(STEP 1~2) · 요청(STEP 3) · 붙여넣기(STEP 4) 세 덩어리로 묶여 있음(빠진 단계 없음)

## 준비물 / 필요 도구 (이름 + 공식 링크)
- n8n: https://n8n.io/ · 저장소 https://github.com/n8n-io/n8n (스타 205,300 / 2026-09-19, 독일 n8n GmbH) · 템플릿 https://n8n.io/workflows/
- 라이선스: Sustainable Use License(내 일·사내 업무는 허용, n8n 자체 재판매·호스팅 서비스화 불가) https://docs.n8n.io/n8n-community-license
- Claude 프로젝트: https://claude.ai/projects · 생성·관리 https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects · 소개 https://support.claude.com/en/articles/9517075-what-are-projects
- (선택) Claude Code 등 터미널 AI: 샘플 다운로드/검증 위임용
- 문서: 워크플로 내보내기·가져오기 https://docs.n8n.io/build/manage-workflows/export-and-import · npm 실행 https://docs.n8n.io/hosting/installation/npm/ · 요금 https://n8n.io/pricing/
- 환경: Claude 계정 + n8n 화면(클라우드 또는 로컬). 로컬 실행에는 Node.js 24 이상(첫 `npx n8n` 설치 실측 약 11분)
- 비용: Claude 무료 계정은 프로젝트 5개까지, Pro는 월 $20~. n8n은 직접 호스팅 무료(Community Edition), 클라우드는 연간 결제 기준 월 $20(Starter)~. 외부 API(OpenAI 등) 요금은 별도
- 용어: JSON=워크플로 설계도를 글자로 적은 파일 / 노드=n8n의 상자 하나 / 트리거=워크플로를 시작시키는 첫 상자 / 자격증명=내 계정(Gmail·Telegram 등)에 접속하는 열쇠

## 단계별 방법
**Quick Start: 샘플 워크플로 3개 받기**
- 브라우저(맥·윈도우 공통): https://n8n.io/workflows/ → 검색창에 `gmail labelling`, `telegram assistant`, `RAG starter`를 하나씩 검색 → 템플릿 화면의 Download → `.json` 3개
- 터미널(맥·리눅스):
```bash
mkdir -p ~/n8n-samples
curl -s https://api.n8n.io/workflows/templates/2740 -o ~/n8n-samples/gmail-labelling.json
curl -s https://api.n8n.io/workflows/templates/2462 -o ~/n8n-samples/telegram-assistant.json
curl -s https://api.n8n.io/workflows/templates/5010 -o ~/n8n-samples/rag-starter.json
```
  파일 3개가 생기고 메시지가 없으면 성공
- 검증(다운로드 버튼으로 받았다면 생략, 또는 편집기로 열어 맨 앞이 `{`이고 `"nodes"`가 보이는지 확인)
```bash
curl -s https://api.n8n.io/health     # {"status":"OK"}
python3 -c "import json;d=json.load(open('$HOME/n8n-samples/gmail-labelling.json'));print(d['name'], len(d['workflow']['nodes']))"
```
  이름과 노드 수가 나오면 됨(예: `Basic automatic Gmail email labelling with OpenAI and Gmail API 13`). python3이 없으면 편집기로 확인

**Claude Code 등 터미널 AI 위임 프롬프트 뼈대** (샘플 선택·다운로드·검증)
- 역할: 클로드 프로젝트에 올릴 n8n 샘플 워크플로를 고르고 내려받아 검증하는 담당. 맥락: 초보
- 채울 곳: [내가 만들고 싶은 자동화 한 줄 — 예: 매일 아침 AI 뉴스를 모아 메일로 받기]
- 작업: ① OS·Node.js 설치 여부 확인 보고 ② `mkdir -p ~/n8n-samples` ③ `curl -s --get "https://api.n8n.io/templates/search" --data-urlencode "search=<검색어>" --data "rows=5"`로 목표와 가까운 템플릿 검색, 제목 제시 후 3개 선택해 `curl -s "https://api.n8n.io/workflows/templates/<번호>" -o ~/n8n-samples/<이름>.json`으로 다운로드 ④ 각 파일이 진짜 워크플로인지 확인하고 claude.ai 프로젝트 파일 칸에 올리는 법과 다음 할 일을 안내
- 제약: sudo·전역 설치·설정 수정 전 질문, n8n 설치 금지(불필요), 키·비밀번호 출력 금지, 기존 파일 덮어쓰기 금지
- 검증: health가 `{"status":"OK"}`, 파일마다 `python3 -c "import json;d=json.load(open('<파일>'));print(len(d['workflow']['nodes']))"`가 1 이상(python3 없으면 직접 nodes 개수 세기). 하나라도 실패 시 완료 보고 금지

**STEP 1. 클로드 프로젝트 만들기 (3분)** — 프로젝트=방마다 규칙·파일을 넣어 두는 작업방
1. https://claude.ai/projects 열기 (데스크톱 앱은 왼쪽 사이드바 Projects)
2. `+ New Project`
3. 이름 `n8n workflows` → `Create project`
- 이름·설명 칸은 나중에 찾기 쉬우라는 용도. 규칙은 다음 단계 지시문 칸에. 무료 계정은 5개까지(차면 안 쓰는 방 삭제/보관)

**STEP 2. 규칙 한 칸, 샘플 한 칸 채우기 (10분)**
1. 지시문: 프로젝트 화면 `Set project instructions` → 붙여넣기 → `Save instructions`. 저장하면 그 방의 모든 대화에 자동 적용
   - 프롬프트 뼈대(영어+한글 혼합): 핵심 줄은 `Always reference the "n8n-io/n8n" GitHub repo before building anything.` + `Never invent nodes or features that don't exist.` / 이어서 한국어로 — 워크플로는 업로드된 샘플 JSON 형식을 그대로 따른다, 노드 type과 파라미터는 샘플이나 공식 저장소에 실제 있는 것만 쓴다, 불확실하면 지어내지 말고 먼저 질문한다, 결과는 설명 없이 바로 복사할 수 있는 JSON 한 벌로 준다
   - 이 줄이 없으면 그럴듯한 가짜 노드가 섞여 n8n 캔버스에 붙여넣는 순간 빨간 표시가 뜸
2. 파일: 프로젝트의 파일(지식) 칸 `+` → 샘플 JSON 올리기
| 파일 (라이브러리 원제목) | 기능 | 노드 |
|---|---|---|
| gmail-labelling.json (Basic automatic Gmail email labelling with OpenAI and Gmail API) | 새 메일을 AI가 읽고 라벨링 | 13 |
| telegram-assistant.json (Angie, personal AI assistant with Telegram voice and text) | 텔레그램 음성·문자를 받아 비서처럼 응답 | 15 |
| rag-starter.json (RAG Starter Template using Simple Vector Stores, Form trigger and OpenAI) | 올려 둔 문서만 근거로 답변 | 12 |
- 2~3개면 충분. 많으면 따를 형식이 헷갈림
- ❌ 만들고 싶은 자동화를 길게 설명한 문서 업로드 → ✅ 남이 만든 워크플로 JSON 실물 업로드
- 내 주제에 맞는 샘플 검색(결과의 `"id"` 숫자가 템플릿 번호):
```bash
curl -s --get "https://api.n8n.io/templates/search" --data-urlencode "search=daily AI news email" --data "rows=5"
```

**STEP 3. 원하는 자동화를 적고 파일 받기 (5분)**
1. 프로젝트 안에서 새 대화, 모델은 빠르고 저렴한 것이면 충분(영상은 Sonnet 4.5; 목록에서 이름에 Sonnet이 든 것 선택, 이름은 계정·시기마다 다름)
2. 요청문에 언제(트리거)/무엇을(작업·도구)/어디로(결과) 세 가지를 모두 적기
   - ❌ "유튜브 자동화 워크플로 하나 만들어 줘" → ✅ "매일 아침 9시에 돌면서 AI 도구 뉴스를 모으고, 요약해서 영상 아이디어 5개를 내 메일로 보내 줘"
   - 요청 틀 뼈대: 아래 자동화를 프로젝트 샘플과 같은 형식의 JSON 한 벌로 / 언제: [...] / 무엇을: [...] / 어디로: [...] / 노드는 샘플이나 n8n-io/n8n 저장소에 실제 있는 것만 / 계정 연결 노드는 자격증명 이름만 비우고 표시
3. 클로드가 JSON 한 벌을 통째로 반환 → 코드 블록의 복사 버튼으로 전체 복사(내용은 읽지 않아도 됨)

**STEP 4. n8n에 붙여넣고 확인 (5분)**
1. n8n 열기: 클라우드는 https://n8n.io/ 로그인, 로컬은
```bash
npx n8n
```
   `Editor is now accessible via: http://localhost:5678/` 같은 줄이 나오면 그 주소를 브라우저로. 첫 실행은 내려받을 게 많아 오래 걸림(창을 닫지 말 것). 이미 n8n을 쓰면 생략
2. 새 워크플로 생성 → 빈 캔버스 클릭 → `Cmd+V`(윈도우 `Ctrl+V`). 파일로 올리려면 오른쪽 위 점 세 개 메뉴 → `Import from File`
3. 상자와 연결선이 한 번에 뜨면 성공. 남은 일은 계정 연결이 필요한 상자를 눌러 내 자격증명 선택
4. 빨간 표시/느낌표는 오류 문구를 그대로 클로드에 붙여 수정 요청. 프롬프트 뼈대: "n8n에 붙여넣었더니 아래 오류가 떴어. 실제 존재하는 노드로 고쳐서 JSON 전체를 다시 줘" + [오류 문구]
5. 되돌리기:
```bash
rm -rf ~/n8n-samples
```
   (이후 `ls ~/n8n-samples`에 `No such file or directory`). `npx`로 띄운 n8n은 Ctrl+C로 종료, 프로젝트에 올린 파일은 파일 옆 ✕로 삭제

## 핵심 팁 · 주의사항
- 클로드는 n8n을 직접 조작하지 않음. 결과는 JSON 텍스트이고 붙여넣기·계정 연결은 사람 몫(클로드가 n8n 안에 바로 만들게 하려면 별도 연결 설정이 필요하며 이 자료 범위 밖)
- 한 번에 되는 경우는 드묾. 노드가 많을수록 두세 번 왕복 전제
- 큰 자동화는 노드 5~8개 단위로 쪼개 요청하고, 먼저 붙여넣어 확인한 뒤 이어서 요청
- 워크플로를 받는 것과 돌리는 것은 별개 비용: OpenAI 노드 등은 그쪽 요금이 따로 나감
- 무료 Claude는 대화량 제한이 빨리 찰 수 있음(긴 JSON). 막히면 시간을 두거나 Pro(월 $20~)
- n8n 클라우드는 체험 후 월 $20~. 계속 무료로 쓰려면 내 컴퓨터/서버에 직접 호스팅(관리 품 필요)
- 프로젝트 밖에서 대화하면 지시문이 적용되지 않음 → 사이드바에서 프로젝트로 들어가 새 대화 시작

## 문제 해결
| 증상 | 원인과 해결 |
|---|---|
| 붙여넣었더니 빨간 노드 | 존재하지 않는 노드 이름. 지시문 저장·샘플 업로드 여부 확인, 둘 다 있으면 오류 문구를 붙여 수정 요청 |
| JSON이 중간에 끊김 | 너무 큰 자동화. 노드 5~8개로 쪼개 요청 |
| 계정 연결에서 막힘 | Gmail/Telegram 등은 클로드가 연결 불가. n8n에서 상자를 열고 자격증명을 직접 선택 |
| 같은 설명을 매번 다시 함 | 프로젝트 밖 대화일 가능성. 프로젝트로 들어가 새 대화 |
| 템플릿 번호로 빈 파일이 받아짐 | 번호가 틀렸거나 비공개. 검색 명령으로 번호 재확인 |

## 바로 쓰는 체크리스트
- [ ] 프로젝트 `n8n workflows` 생성
- [ ] 지시문(n8n-io/n8n 저장소 참조, 노드 지어내기 금지, JSON 한 벌 출력) 저장
- [ ] 샘플 JSON 2~3개 업로드
- [ ] 요청문에 언제/무엇을/어디로 명시
- [ ] 받은 JSON을 n8n에 붙여넣기 또는 Import from File
- [ ] 자격증명을 n8n에서 직접 연결하고 테스트 실행
- [ ] 오류는 문구 그대로 클로드에 전달
