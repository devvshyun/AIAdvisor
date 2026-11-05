# 클로드 코드에 무료 프롬프트 라이브러리 연결하는 법
- 원문: https://lazyowen.com/guides/hani-prompt
- 도구·주제: Claude Code + prompts.chat 플러그인(MCP) · 프롬프트 라이브러리 (2026-09-20 공개, STEP 5개 · 약 15분)
- 한 줄 요약: prompts.chat(2,300개+ 공개 프롬프트)을 플러그인으로 연결해, 요청 문장에 검색 지시를 넣으면 클로드가 필요한 프롬프트를 찾아 적용하게 한다.

## 언제 쓰나
- 코드 리뷰, 글쓰기, 이미지, 영상, 리서치 등 이미 검증된 프롬프트를 클로드 코드 안에서 바로 검색해 쓰고 싶을 때
- 한 줄짜리 요청이라 결과가 밋밋할 때. 연결 전은 검색→블로그 비교→복사→붙여넣기, 연결 후는 "prompts.chat에서 찾아서 적용해" 한 문장
- prompts.chat은 프롬프트를 대신 써 주는 AI가 아니라 이미 있는 프롬프트를 찾는 곳. 프롬프트 2,300개+와 스킬, 이를 찾아 주는 에이전트 2개가 함께 설치됨

## 준비물 / 필요 도구 (이름 + 공식 링크)
- Claude Code: https://claude.com/claude-code (확인 환경 v2.1.274)
- Node.js(독립 실행 `npx prompts.chat`에만 필요): https://nodejs.org/ LTS
- prompts.chat: https://prompts.chat/ · https://github.com/f/prompts.chat (스타 17만+ / 2026-09-20, 2022년 12월 공개, 구 이름 Awesome ChatGPT Prompts)
- 플러그인 문서: https://github.com/f/prompts.chat/blob/main/CLAUDE-PLUGIN.md · 셀프호스팅 https://github.com/f/prompts.chat/blob/main/SELF-HOSTING.md
- 지원 OS: macOS 13.0+, Windows 10 1809+ (화면은 맥에서 확인, 플러그인 v1.0.0)
- 라이선스: 소스 MIT, 프롬프트 데이터 CC0 1.0
- 비용: 검색·열람·사용 무료. 내 프롬프트를 계정에 저장(`save_prompt`)하려면 prompts.chat 가입 후 설정 화면에서 API 키 발급 필요(발급 비용은 문서에 명시 없음)
- 용어: 플러그인=기능을 덧붙이는 확장 / 마켓플레이스=플러그인 목록(먼저 등록해야 설치 가능) / MCP=AI가 외부 서비스에 접속하는 규격

## 단계별 방법
**연결 검증 위임 프롬프트 뼈대** (터미널에서 `claude` 실행 후 첫 메시지. 터미널을 못 여는 경우 prompts.chat 사이트에서 직접 복사해 쓰기)
- 역할: 프롬프트챗 플러그인 설치·연결 검증 담당. 맥락: 초보, 터미널은 처음
- 채울 곳: [내 목표 — 예: 내가 쓴 코드 리뷰받기 / 블로그 초안 잡기]
- 작업: ① `node --version` 확인 ② `claude plugin list`로 설치 여부 확인, 없을 때만 `claude plugin marketplace add f/prompts.chat`과 `claude plugin install prompts.chat@prompts.chat` ③ `claude plugin list`·`claude mcp list`로 검증 ④ 프롬프트챗이 무엇이고 목표를 이루려면 어떤 문장으로 요청할지 예시 문장 2개와 함께 설명
- 제약: sudo·전역 설치·설정 수정 전 질문, 비밀키 출력 금지, 기존 파일 덮어쓰기 금지
- 검증: `claude plugin list`에 `Status: ✔ enabled`, `claude mcp list`에 `✔ Connected`. 하나라도 실패하면 완료 보고 금지

**STEP 1. 준비물 확인 (2분)**
```bash
claude --version     # 예: 2.1.274 (Claude Code). command not found면 claude.com/claude-code에서 설치
node --version       # v로 시작하는 숫자. 터미널 도구(npx)까지 쓸 때만. 플러그인만 쓰면 생략
```
(확인 화면의 Node는 v26.8.1이었음. 이 가이드의 용도로는 무관하며 LTS 설치 권장)

**STEP 2. 클로드 코드에 연결 (3분)**
```bash
claude
```
대화창에서 한 줄씩 입력:
```
/plugin marketplace add f/prompts.chat
/plugin install prompts.chat@prompts.chat
```
- 성공: `✔ Successfully added marketplace: prompts.chat`, `✔ Successfully installed plugin: prompts.chat@prompts.chat (scope: user)`
- 대안: 대화창을 열지 않고 터미널에서
```bash
claude plugin marketplace add f/prompts.chat
claude plugin install prompts.chat@prompts.chat
```
- 회사/학교망에서 SSH가 막혀 등록에서 멈추면 HTTPS 전체 주소로:
```bash
claude plugin marketplace add https://github.com/f/prompts.chat.git
```
- 이미 설치돼 있으면 생략

**STEP 3. 붙었는지 확인 (2분)** — 대화창을 닫고 터미널에서
```bash
claude plugin list    # ❯ prompts.chat@prompts.chat 아래 Status: ✔ enabled
claude mcp list       # plugin:prompts.chat:prompts.chat: https://prompts.chat/api/mcp (HTTP) - ✔ Connected
```
- `✕ Failed`는 인터넷/방화벽 문제 → 다른 네트워크에서 재확인

**STEP 4. 실제로 쓰기 (5분)** — 연결만으로 자동 동작하지 않음. 요청에 "찾을 곳 + 검색어 + 시킬 일" 세 가지를 넣어야 검색 도구가 켜짐
- ❌ `코드 리뷰 좀 해줘` → ✅ `prompts.chat에서 code review 프롬프트를 검색해서, 제일 잘 맞는 걸로 이 폴더 코드를 리뷰해줘`
- ❌ `prompts.chat에서 좋은 거 아무거나 찾아줘` → ✅ `prompts.chat에서 blog writing 프롬프트를 3개만 찾아서 차이를 비교해줘`
- 등록 프롬프트 제목이 대부분 영어 → 요청은 한국어, 검색어만 영어로
- 직접 검색만 하려면 대화창에서:
```
/prompts.chat:prompts code review
```
  (결과 목록이 뜨면 하나 골라 이어서 시킴)

**STEP 5. 클로드 코드 밖에서 꺼내 쓰기 (3분)** — ChatGPT/Gemini 웹 등 클로드 코드 밖에서 같은 프롬프트를 쓰고 싶을 때만
```bash
npx prompts.chat
```
- Node.js 필요(별도 설치는 없고 명령이 그때그때 내려받아 실행)
- 목록 화면: `/` 검색 · `j` `k` 또는 방향키 이동 · `Enter` 선택 · `n` `p` 다음·이전 페이지 · `c` 카테고리 · `q` 종료
- 프롬프트 화면: `c` 복사 · `o` 브라우저로 열기 · `r` 실행 · `b` 뒤로 · `q` 종료
- 프롬프트에 빈칸이 있으면 `c`를 누를 때 값을 먼저 물어보고 채운 내용으로 복사. 복사본은 ChatGPT·Gemini 등 어디든 붙여넣기

**되돌리기**
```bash
claude plugin uninstall prompts.chat@prompts.chat    # ✔ Successfully uninstalled plugin: prompts.chat (scope: user)
```

## 핵심 팁 · 주의사항
- 검색 지시 없이는 클로드가 라이브러리를 쳐다보지 않음 — "prompts.chat에서 ~ 검색해서"가 핵심
- 품질이 고르지 않음(누구나 업로드): 1번 결과를 그대로 믿지 말고 2~3개 비교
- 한국어 검색어는 결과가 적음 → 검색어는 영어
- MCP 주소 `https://prompts.chat/api/mcp`를 브라우저에 넣으면 `Method not allowed`가 뜨는 것은 정상(프로그램끼리 쓰는 주소)
- 프롬프트 저장(`save_prompt`)만 가입+API 키 필요, 나머지는 무료

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| `/plugin` 입력해도 반응 없음 | 터미널에 그냥 침 | 먼저 `claude`로 켠 뒤 대화창에 입력 |
| 마켓플레이스 등록에서 멈춤 | 회사망 SSH 차단 | `claude plugin marketplace add https://github.com/f/prompts.chat.git` |
| `claude mcp list`에 `✕ Failed` | 인터넷·방화벽 차단 | 다른 네트워크에서 재시도, 안 되면 플러그인 재설치 |
| 검색 결과가 적음 | 한국어 검색어 | 검색어만 영어로 |
| 연결했는데 답이 똑같음 | 요청에 검색 지시 없음 | "prompts.chat에서 ~ 검색해서"를 문장에 넣기 |

## 바로 쓰는 체크리스트
- [ ] `claude --version` 확인
- [ ] marketplace add + plugin install
- [ ] `claude plugin list` = enabled, `claude mcp list` = Connected
- [ ] 요청에 "prompts.chat에서 (영어 키워드) 검색해서 ~" 포함
- [ ] 결과 여러 개 비교 후 선택
- [ ] (선택) 클로드 밖에서는 `npx prompts.chat`
