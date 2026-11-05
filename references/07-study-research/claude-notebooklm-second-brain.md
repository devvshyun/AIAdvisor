# 클로드에게 절대 안 잊는 두 번째 뇌 붙이기 (NotebookLM)
- 도구·주제: Claude Code + NotebookLM(Gemini Notebook) + notebooklm-mcp · 장기 기억 / 리서치 (2026-08-06 갱신, STEP 5개 · 약 11분)
- 한 줄 요약: NotebookLM을 MCP로 연결하고 저장용 스킬을 만들어 대화 요약을 `Claude Memory` 노트북에 쌓고, `CLAUDE.md` 규칙으로 다음 세션에서 먼저 검색하게 하는 5단계.

## 언제 쓰나
- 매 세션을 "배경 다시 설명"으로 시작하는 장기 프로젝트(효과 가장 큼), 자료가 많은 리서치(같은 노트북이 보고서·인포그래픽도 생성)
- 기억할 게 없는 단발성 질문엔 불필요
- 원리: 대화창은 길어지면 앞부분이 밀려나므로 기억을 밖(노트 도구)에 두고 필요한 조각만 검색해 가져옴. NotebookLM은 내가 넣은 자료 안에서만 답하고 출처를 붙임
- 클로드 기본 메모리는 규칙을 담고, 이 방식은 실제 작업 기록을 담음

## 준비물 / 필요 도구
- Claude Code(터미널 실행 가능), Node.js 18 이상, 크롬 브라우저(연결 도구가 크롬 창을 열어 로그인), 무료 구글 계정 1개 — 연결 도구가 브라우저를 조작하므로 평소 계정 대신 전용 구글 계정 권장
- NotebookLM: https://notebooklm.google.com/ (2026년 7월부터 공식 이름이 Gemini Notebook, 같은 제품·기존 노트북 그대로)
- notebooklm-mcp (MIT): https://github.com/PleasePrompto/notebooklm-mcp · 문제 해결 https://github.com/PleasePrompto/notebooklm-mcp/blob/main/docs/troubleshooting.md
- 요금제 https://notebooklm.google/plans · 무료 한도표 https://support.google.com/gemininotebook/answer/16213268?hl=ko
- Claude Code 문서: MCP https://code.claude.com/docs/en/mcp · 스킬 https://code.claude.com/docs/en/skills
- 비용: 무료(무료 한도 안에서). 용어: MCP=AI 도구에 외부 앱을 꽂는 표준 규격, 스킬=특정 요청에 따를 순서를 적어둔 설명서 파일

## 단계별 방법
**Quick Start**
```bash
claude mcp add notebooklm -- npx notebooklm-mcp@latest    # 성공하면 Added ... 한 줄 (아직 로그인 전)
claude mcp list                                            # notebooklm 줄이 보이면 OK. 초록색이 아니어도 정상
```

**설치·검증 위임 프롬프트 뼈대 (Claude Code)**
- 역할: NotebookLM 연결 도구 설치·연결 검증 담당. 맥락: 미설치일 수 있고 클로드가 매 대화마다 배경을 다시 묻는 상태
- 채울 곳: [OS·셸], [도구: Claude Code], [목표: 대화 기록을 NotebookLM에 저장하고 다음 대화에서 검색해 쓰기]
- 작업: ① `claude mcp list`로 notebooklm 등록 여부 확인 ② 없으면 `claude mcp add notebooklm -- npx notebooklm-mcp@latest` ③ 노트북 목록을 실제로 불러와 연결 검증 ④ 이 도구가 무엇이고 앞으로 어떻게 쓰는지 3줄 설명
- 제약: 구글 비밀번호·토큰 출력 금지, 기존 MCP 설정·다른 서버 삭제/덮어쓰기 금지
- 검증: `claude mcp list`에 notebooklm 줄과 Connected, 그리고 노트북 목록에 내 노트북 이름이 나와야 함. 하나라도 실패하면 완료 보고 금지

**STEP 1. 기억 창고 만들기 (3분)**
1. https://notebooklm.google.com/ 접속 → 구글 로그인
2. 새로 만들기(Create new) → 노트북 생성
3. 이름을 정확히 `Claude Memory`로 (뒤의 스킬이 이 이름으로 노트북을 찾음)
- 지금은 자료를 안 넣어도 됨. 화면 상단에 이름이 보이고 자료 목록이 비어 있으면 통과

**STEP 2. 클로드와 노트북 연결 (5분)**
- Quick Start에서 이미 했다면 생략. 아니면 위 `claude mcp add ...` 실행
- 설정 파일 직접 편집 방식: `~/.claude.json`에 아래를 넣고 Claude Code 재시작 (위 명령과 동일하게 등록됨)
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "npx",
      "args": ["notebooklm-mcp@latest"]
    }
  }
}
```
- Claude Code를 완전히 껐다 켠 뒤 대화창에 `내 노트북 목록 보여줘` → 처음 한 번 크롬 창이 뜨면 STEP 1의 계정으로 로그인(이후 재요청 없음)
- 클로드가 목록에서 `Claude Memory`를 읽어주면 완료. 로그인 정보는 내 컴퓨터에만 저장

**STEP 3. "대화 끝나면 저장" 스킬 만들기 (5분)** — 연결만 해두면 클로드는 알아서 저장하지 않음
```bash
mkdir -p ~/.claude/skills/memory-save
```
- 그 폴더에 `SKILL.md` 작성 후 Claude Code 재시작. 구조(뼈대):
  - frontmatter `description`: 대화가 끝날 때 이번 세션의 결정·맥락을 요약해 NotebookLM의 "Claude Memory"에 저장하는 스킬이며, "기억 저장", "오늘 내용 저장해줘", "wrap up" 같은 말에 사용
  - 순서: ① 지금까지의 대화를 아래 형식으로 요약 ② notebooklm 도구의 `add_source`를 `type: "text"`로 호출해 저장 — 노트북은 `Claude Memory`(활성 노트북이 다르면 먼저 `select_notebook`), 제목은 `세션 YYYY-MM-DD — <한 줄 주제>` ③ 저장 후 자료 개수가 몇 개에서 몇 개로 늘었는지 보고
  - 요약 항목: 날짜 / 주제 / 결정한 것 / 아직 안 끝난 것 / 다음에 할 것 / 기억할 사실(파일 경로·이름·숫자·사용자 선호)
  - 규칙: 사실만 기록(추측·각색 금지), 비밀번호·API 키·토큰 값은 본문에 쓰지 않고 위치만("키는 설정 파일에 있음"), 저장에 실패하면 완료라고 하지 말고 오류 내용을 그대로 보고
- 사용: 대화를 마칠 때 `기억 저장`이라고 한마디
- 확인: 아무 대화 후 `기억 저장` → Claude Memory 노트북을 새로고침했을 때 자료가 1개 늘면 통과

**STEP 4. 검색 규칙 박기 (3분)**
- 작업 폴더의 `CLAUDE.md`(없으면 새로 생성) 맨 위에 "기억 라우팅" 3줄(뼈대): 세션을 시작하면 사용자에게 다시 설명해 달라고 하기 전에 notebooklm 도구로 `Claude Memory` 노트북을 먼저 검색 / 전체 기록이 아니라 지금 질문에 필요한 부분만 가져옴 / 노트북에 없으면 없다고 말하고 지어내지 않음
- 규칙이 아래쪽에 묻히면 놓치므로 반드시 최상단. 저장하면 다음 대화부터 적용
- 확인: 새 대화에서 `지난번에 뭘 정했는지 기억 노트북에서 찾아줘`라고 물었을 때 다시 설명 없이 과거 결정을 읊으면 통과

**STEP 5. (선택) 무료로 딸려오는 것들**
- Claude Memory 노트북에서 버튼으로 인포그래픽(기록을 한 장 이미지로), 동영상 오버뷰(내레이션 영상), 보고서(문서 요약), Deep Research(넣은 자료 안에서만 근거를 찾는 심층 조사) 생성. 모두 무료 한도 안

## 핵심 팁 · 주의사항
- 무료 한도(페이지 기준): 노트북 100개, 노트북당 자료 50개, 하루 채팅 50개 → 저장 50번≈대화 50회 분량. 차면 오래된 요약 삭제 또는 기간별 노트북(예: `Claude Memory 2026`). 수치는 바뀔 수 있으니 공식 페이지 확인
- 노트북은 내가 저장한 시점까지만 앎 → 자주 저장
- 비밀번호·키·토큰 값은 저장 본문에 넣지 말 것(위치만 기록)
- 연결 도구가 브라우저를 조작하므로 전용 구글 계정 권장
- 흔한 방식과 차이: 수동 붙여넣기 → 노트북 저장·검색 / 생각날 때만 저장 → 대화 끝에 `기억 저장` / 긴 대화로 앞부분이 밀림 → 필요한 조각만 오감 / 기억을 지어냄 → 내 자료 안에서만 답

## 문제 해결
- 클로드가 notebooklm 도구를 못 봄: 등록 누락 또는 재시작 안 함 → `claude mcp list` 확인, 없으면 STEP 2 명령 재실행 후 Claude Code 완전 재시작
- 구글 로그인이 계속 돌거나 인증이 자꾸 풀림: 로그인 상태를 지우고 재로그인(처음부터 전용 계정을 쓰면 거의 없음)
- `기억 저장`해도 안 쌓임: 스킬 파일이 `~/.claude/skills/memory-save/SKILL.md`에 있는지, 노트북 이름이 `Claude Memory`와 정확히 같은지 확인
- 여전히 처음부터 설명하라고 함: `CLAUDE.md`에 규칙이 없거나 아래쪽에 묻힘 → 3줄을 맨 위로
- 꺼내온 기억이 옛날 것뿐: 저장 빈도를 높임
- 자료를 더 못 넣음: 노트북당 50개 한도 → 오래된 요약 삭제 또는 기간별 노트북

## 바로 쓰는 체크리스트
- [ ] `claude mcp list`에 notebooklm 보임, 클로드가 내 노트북 목록을 읽어준다
- [ ] `Claude Memory` 노트북 생성(이름 정확히)
- [ ] `~/.claude/skills/memory-save/SKILL.md` 작성, 재시작
- [ ] `기억 저장` 후 `Claude Memory` 자료가 1개 늘어난다
- [ ] `CLAUDE.md` 맨 위에 기억 라우팅 3줄
- [ ] 새 대화가 설명 없이 과거 맥락을 꺼낸다
- [ ] 비밀값은 저장 본문에 넣지 않기
