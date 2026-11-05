# 클로드 코드에 무조건 깔아야 하는 MCP 5개
- 원문: https://lazyowen.com/guides/mcps
- 도구·주제: Claude Code + MCP (Perplexity, Playwright, Firecrawl, Glif, Chrome DevTools) · MCP 연결 (스킬·MCP, 13분 읽기, 약 38분 실습, STEP 8개, 2026-08-06 갱신)
- 한 줄 요약: 검색·브라우저 조작·크롤링·이미지 생성·내 탭 점검 능력을 `claude mcp add` 한 줄씩으로 붙이고 실제 연결을 확인하는 가이드.

## 언제 쓰나
- 기본 Claude Code는 인터넷, 브라우저, 이미지 생성이 없어 아는 것만으로 답해 옛날 정보로 틀릴 때
- MCP = 클로드를 바깥 도구에 연결하는 규격(콘센트-플러그 비유). 꽂으면 클로드가 그 도구를 직접 씀.

## 준비물 / 필요 도구
- Claude Code (https://claude.com/claude-code, 설치·로그인), Node.js LTS (https://nodejs.org/) — 5개 모두 Node 위에서 동작
- 터미널: macOS 터미널 / Windows PowerShell
| 도구 | 채우는 구멍 | 키 |
|---|---|---|
| Perplexity | 실시간 웹 검색 | 필요 (https://www.perplexity.ai/settings/api) |
| Playwright | 브라우저 직접 조작·테스트 | 불필요 |
| Firecrawl | 사이트 통째 수집 | 무료 원격 주소는 불필요, 키는 https://www.firecrawl.dev/app/api-keys (`fc-`로 시작) |
| Glif | 이미지·영상 생성(수백 모델) | 브라우저 로그인 |
| Chrome DevTools | 내가 보는 화면 확인 | 불필요 |
- 공식: https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server · https://github.com/perplexityai/modelcontextprotocol · https://playwright.dev/mcp/introduction · https://github.com/microsoft/playwright-mcp · https://docs.firecrawl.dev/mcp-server · https://github.com/firecrawl/firecrawl-mcp-server · https://glif.app/mcp · https://github.com/glifxyz/glif-mcp-server · https://github.com/ChromeDevTools/chrome-devtools-mcp · https://developer.chrome.com/docs/devtools/agents/get-started
- 가격 정보는 본문에 없음 (Perplexity·Firecrawl은 키/가입 필요, 요금제 별도 확인).

## 단계별 방법
### 보조 프롬프트: 설치~검증 위임 (프롬프트 뼈대)
- 목적: 클로드 코드에 5개 MCP 설치와 연결 검증을 맡김. 역할=MCP 설치·검증 담당.
- 슬롯: [운영체제·셸], [기술 스택], [목표 한 줄].
- 작업 4단계: ① `claude --version`/`node --version`/`claude mcp list`로 확인, 이미 있으면 재등록 금지 ② 없는 것만 아래 명령으로 설치, 키 필요한 2개는 사용자에게 키를 받고 못 받으면 건너뛰며 이유 설명 ③ `claude mcp list` 결과를 그대로 보고, Connected 아닌 건 원인 수정(glif는 인증 대기가 정상) ④ 5개 역할을 5줄 이내로 설명.
- 제약: 키 값 출력 금지, `.env` 읽기 금지, 기존 설정 삭제/덮어쓰기 금지, 중복 등록 금지. 출력: 실행 명령, list 결과, 신규 서버, 남은 오류. 검증: playwright/chrome-devtools(+키 넣은 perplexity/firecrawl)가 Connected, 실패 시 완료 보고 금지.

### STEP 1. 준비물 확인 (2분)
```bash
claude --version
node --version
```
둘 다 숫자가 나오면 OK. `command not found`만 설치 (claude는 터미널을 완전히 닫았다 다시 열기).

### STEP 2. MCP 개념 (1분)
위 표의 5개는 서로 겹치지 않고 막는 구멍이 각각 다름.

### STEP 3. 키 없이 되는 3개 설치 (3분)
```bash
claude mcp add playwright -- npx @playwright/mcp@latest
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
claude mcp add --transport http glif "https://glif.app/api/mcp"
```
- 성공 예: `Added stdio MCP server playwright with command: npx @playwright/mcp@latest to local config` / glif는 `Added HTTP MCP server glif with URL: https://glif.app/api/mcp`
- 기본은 local 범위(현재 폴더에서만). 모든 폴더에서 쓰려면 명령 뒤에 `--scope user`.

### STEP 4. 키 필요한 2개 설치 (5분)
API 키는 비밀번호와 같음. 화면 공유·영상에 노출 금지.
```bash
claude mcp add perplexity --env PERPLEXITY_API_KEY="여기에_내_키_붙여넣기" -- npx -y @perplexity-ai/mcp-server
claude mcp add firecrawl --env FIRECRAWL_API_KEY="fc-여기에_내_키_붙여넣기" -- npx -y firecrawl-mcp
```
키 없이 Firecrawl(공식 무료 주소, 양 제한, 검색·페이지 읽기만, 전체 크롤링은 키 필요):
```bash
claude mcp add --transport http firecrawl "https://mcp.firecrawl.dev/v2/mcp"
```

### STEP 5. 연결 확인 (2분)
"추가됨"은 등록일 뿐, 실제 통신은 따로 확인.
```bash
claude mcp list
```
```
perplexity: npx -y @perplexity-ai/mcp-server - ✔ Connected
playwright: npx @playwright/mcp@latest - ✔ Connected
firecrawl: npx -y firecrawl-mcp - ✔ Connected
chrome-devtools: npx chrome-devtools-mcp@latest - ✔ Connected
glif: https://glif.app/api/mcp (HTTP) - ! Needs authentication
```
- glif의 `! Needs authentication`은 정상(로그인 전). 클로드 코드 안에서 `/mcp` → glif 선택 → 브라우저에서 승인.

### STEP 6. 5개 실사용 테스트 (10분)
도구를 지정 안 해도 클로드가 알아서 고름.
1. Perplexity: `Perplexity로 Next.js 최신 버전에서 바뀐 점을 찾아서 3줄로 정리해줘. 출처 링크도 같이 줘.` → 최신 날짜와 링크가 나오면 성공.
2. Playwright: `Playwright로 https://demo.playwright.dev/todomvc 를 열고 "장보기"를 추가한 다음, 목록에 잘 들어갔는지 확인해줘.` → 브라우저 창이 뜨고 입력됨. 안 보이게 하려면 `--headless`.
3. Firecrawl: `Firecrawl로 https://docs.firecrawl.dev 문서를 긁어서 핵심 기능 목록만 뽑아줘.`
4. Glif: `Glif로 "노란 헬멧 쓴 게으른 로봇" 이미지를 만들어줘.` → 번호표 받고 몇 초 뒤 이미지 링크 반환.
5. Chrome DevTools: `Chrome DevTools로 지금 열려 있는 탭 목록을 보여주고, 첫 번째 탭에서 콘솔 에러가 있는지 확인해줘.` → 기본은 클로드 전용 크롬을 새로 띄움.

### STEP 7. (선택) 내가 보는 탭 연결 (5분)
1. 크롬 주소창: `chrome://inspect/#remote-debugging` → 연결 허용.
2. 기존 등록 삭제 후 `--autoConnect`로 재등록:
```bash
claude mcp remove chrome-devtools
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest --autoConnect
```
3. `claude mcp list`로 Connected 확인. 원격 디버깅이 켜진 동안 클로드가 그 창을 볼 수 있으니 민감한 탭은 닫기.

### STEP 8. 조합 워크플로 (10분)
- 개발 흐름 프롬프트 뼈대: 1) Perplexity로 [내 라이브러리]의 최신 사용법 검색 2) Firecrawl로 공식 문서 페이지에서 실제 코드 예시 수집 3) 프로젝트에 기능 구현 4) Playwright로 브라우저에서 눌러 확인하고 안 되면 수정.
- 콘텐츠 흐름: 1) Firecrawl로 [참고 사이트 주소]의 문구 분석 2) 그 톤으로 내 서비스 소개 문구 5개 작성 3) Glif로 가장 나은 문구에 맞는 대표 이미지 생성.

## 문제 해결 (FAQ)
- `command not found: claude`: 미설치 또는 터미널 미재시작 → 공식 페이지에서 설치 후 터미널 완전히 닫고 다시 열기.
- `✘ Failed to connect`: 대부분 키 오류·따옴표 누락 → `claude mcp remove <이름>` 후 STEP 4 재실행, 키 앞뒤 공백 확인.
- Playwright가 브라우저를 못 엶: `npx playwright install chrome` 한 번 실행 후 재시도.
- 다른 폴더에서 MCP가 사라짐: local 범위 때문 → `--scope user`로 재등록.
- Glif가 계속 `Needs authentication`: `/mcp`에서 glif 선택해 브라우저 승인. 예전 `npx @glifxyz/glif-mcp-server`+토큰 방식은 중단, URL 방식 사용.
- 5개 다 깔면 느려지나: 안 쓰는 서버는 대기만 하지만 도구 목록을 매번 읽으므로 `claude mcp remove <이름>`으로 정리 권장.

## 핵심 팁 · 주의사항
- 유용한 명령: `claude mcp list`, `claude mcp remove <이름>`, `/mcp`, `npx playwright install chrome`.
- ❌ API 키를 화면 공유·영상·로그에 노출 ✅ 키는 따옴표 안에만 넣고 AI에게 출력시키지 말 것.
- Firecrawl 무료 원격은 크롤링 양 제한.
- 원격 디버깅(`--autoConnect`)은 민감 탭 노출 위험.

## 바로 쓰는 체크리스트
- [ ] `claude --version`, `node --version` 확인
- [ ] 키 없는 3개(playwright, chrome-devtools, glif) 등록
- [ ] Perplexity·Firecrawl 키 발급 후 등록
- [ ] `claude mcp list` 전부 Connected (Glif는 `/mcp`로 인증)
- [ ] 각 MCP로 작은 테스트 1건씩
- [ ] 필요하면 `--scope user`로 전역 등록
- [ ] 안 쓰는 서버 제거
