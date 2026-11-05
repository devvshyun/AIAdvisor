# Claude Code 한도 뒤에도 계속 코딩하는 9Router 설정
- 도구·주제: 9Router + Claude Code · 비용 절약 / 한도 이후 자동 폴백 (10분 읽기, STEP 10개, 2026-08-06 갱신판)
- 한 줄 요약: 주 모델과 백업 모델을 9Router의 Fallback Combo로 묶어 Claude Code 한도 초과나 라우팅 가능한 오류 때 자동으로 다음 모델로 넘기고, Cursor 등 다른 도구에도 같은 엔드포인트를 쓴다.
- 참고: 같은 주제의 2026-08-19판은 `9router-free-fallback.md`.

## 언제 쓰나
- 한도에 걸릴 때마다 도구를 닫고 모델을 수동 교체하는 대신 자동 폴백을 원할 때
- 개념: Router = 코딩 도구의 요청을 받아 설정된 공급자 중 하나로 전달하는 로컬 중간 서버. Claude Code는 `http://localhost:20128/v1` 한 곳에만 요청하고, 9Router가 Combo 순서·공급자 상태·오류 종류를 보고 모델을 고르며 OAuth 토큰 갱신, 형식 변환, 사용량 기록도 처리. Fallback은 대화를 새로 만들지 않고 Claude Code 프로세스는 그대로, 다음 요청만 다른 모델이 처리(모델이 바뀌면 답변 품질·도구 사용 방식이 달라질 수 있음).

## 준비물 / 필요 도구
- 9Router: GitHub https://github.com/decolua/9router · 사이트 https://9router.com/ · 설치 https://github.com/decolua/9router#-quick-start · Docker https://github.com/decolua/9router/blob/master/DOCKER.md · 이슈 https://github.com/decolua/9router/issues
- Node.js 18+, npm, Claude Code (`@anthropic-ai/claude-code`)
- 비용 구분:
| 경로 | 비용 판단 |
|---|---|
| 9Router 프로그램 | MIT 오픈소스, 무료 |
| OpenCode Free | 공식 문서상 인증 없는 무료 경로, 모델은 변동 가능 |
| Kiro의 `kr/` 모델 | 공식 문서상 무료 경로, 실제 할당량·약관은 공급자 정책 확인 |
| Claude Code의 `cc/` 모델 | Claude Pro/Max 같은 기존 구독 필요 |
| GLM의 `glm/` | 직접 API 키·과금 조건 확인 |
| Kimi의 `kimi/` | 직접 API 키·요금제 확인 |
| Gemini 계열 | 연결 방식별 무료 할당량·현재 정책 확인 |
- 핵심은 무료 모델 이름 암기가 아니라 대시보드에서 지금 활성화된 공급자와 할당량을 확인하고 Combo 순서를 정하는 것.

## 단계별 방법
### STEP 1. 9Router 설치 (3분)
```bash
node --version
npm --version
npm install -g 9router
9router
```
브라우저가 안 열리면 `http://localhost:20128/dashboard` 직접 열기. 성공: 터미널에 서버 주소, 대시보드에 `Providers`, `Combos`, `CLI Tools` 메뉴.

### STEP 2. 대시보드 잠그기 (2분)
로그인 화면이 나오면 초기 비밀번호(공식 문서상 별도 설정 없을 때 `123456`)로 접속 후 `Profile` → `Security`에서 즉시 변경. 공급자 로그인 토큰·API 키가 로컬 DB에 저장되므로 처음엔 localhost에서만 쓰고 20128 포트를 인터넷에 열지 말 것. 확인: 새 비밀번호로 재로그인.

### STEP 3. 백업 공급자 연결 (5분)
`Providers`에서 연결:
- 가장 빠른 시작: `OpenCode Free` (공식 문서상 무인증, 모델 목록 자동)
- Claude 계열 무료 백업: `Kiro AI` (AWS Builder ID / Google / GitHub 중 선택)
- 기존 Claude 구독을 먼저 쓰려면 `Claude Code`도 연결(OAuth)
- 9Router가 유료 API를 무료로 바꾸지는 않음. `glm/`, `kimi/` 직접 연결은 유료 백업, 무료 GLM 예시는 Kiro 경로 `kr/glm-5`. 확인: 공급자 카드가 활성화되고 모델 선택 창에 모델이 나타남.

### STEP 4. API 키 만들기 (2분)
`Endpoint` → `API Keys` → `Create Key`, 이름 예: `claude-local`. 키는 비밀번호처럼 다루고 문서·공개 저장소에 넣지 말 것. 확인: 목록에 보이고 복사 버튼 동작.

### STEP 5. Fallback Combo 만들기 (5분)
`Combos` → `Create Combo`. 이름은 영문·숫자·마침표·밑줄·하이픈만: `claude-backup`
구독 먼저 쓰고 무료로 넘길 때 모델 순서:
```
1. cc/claude-sonnet-4-6
2. kr/claude-sonnet-4.5
3. kr/glm-5
4. OpenCode Free에서 현재 제공되는 코딩 모델
```
- `cc/claude-sonnet-4-6`이 없으면 `cc/`로 시작하는 현재 Sonnet 모델 선택. OpenCode Free 모델 ID는 바뀔 수 있으니 직접 입력하지 말고 선택 창에서.
- 구독 없이 무료만: 첫 `cc/` 모델을 빼고 Kiro/OpenCode Free부터.
- 전략은 `Fallback — try in order`. (Round Robin은 요청마다 돌려 써 목적과 다름, Fusion은 여러 모델+판정 모델을 한 번에 호출해 무료 백업용 아님.) 확인: `claude-backup` 카드에 순서와 Fallback 전략 표시.

### STEP 6. Claude Code 설치 (3분)
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### STEP 7. Claude Code를 9Router에 연결 (5분)
`CLI Tools` → `Claude Code`:
1. Endpoint: `http://localhost:20128/v1`
2. API Key: `claude-local`
3. Sonnet / Opus / Haiku 매핑 모두 `claude-backup`
4. `Apply`
- Apply는 `~/.claude/settings.json` 기존 값을 읽어 9Router 항목을 합쳐 저장 → 원본 보존하려면 Apply 전에 직접 백업. 자동 적용이 안 될 때만 수동 저장:
```json
{
"hasCompletedOnboarding": true,
"env": {
"ANTHROPIC_BASE_URL": "http://localhost:20128/v1",
"ANTHROPIC_AUTH_TOKEN": "<대시보드에서 만든 API 키>",
"ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-backup",
"ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-backup",
"ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-backup"
}
}
```
확인: Claude Code 카드에 `Connected`와 현재 Endpoint 표시.

### STEP 8. 연결 테스트 (2분)
9Router 실행 터미널은 그대로 두고 새 터미널에서:
```bash
claude
```
요청: `현재 폴더의 파일은 수정하지 말고 “9Router 연결 성공”이라고 한 줄만 답해주세요.` 응답 후 대시보드 `Usage`에서 실제 사용된 공급자·모델 확인. 모든 오류가 fallback 대상은 아니며 인증 실패·잘못된 설정은 직접 고쳐야 함.

### STEP 9. Cursor 등 다른 도구 연결 (3분)
사용자 지정 OpenAI Endpoint를 받는 도구(Cursor, Cline, Continue):
```
Base URL: http://localhost:20128/v1
API Key: <대시보드에서 만든 API 키>
Model: claude-backup
```
Codex·Antigravity 등은 대시보드 `CLI Tools` 안내를 따름. IDE 트래픽을 가로채는 MITM 기능은 고급 설정 → 사용 전 해당 도구의 정책·계정 조건 확인. 짧은 테스트 후 `Usage`에 기록이 생기면 성공.

### STEP 10. 업데이트·재실행 (1분)
```bash
npm install -g 9router@latest
9router --no-browser
```
끄기: 실행 터미널에서 `Ctrl+C` (서버를 끄면 Claude Code도 로컬 엔드포인트에 연결 불가).

## 문제 해결
- `9router: command not found`: 터미널 재시작 후 `npm prefix -g`, `npm list -g 9router --depth=0`. 없으면 `npm install -g 9router` 재실행.
- 대시보드가 안 열림: 실행 중인지 확인 후 `http://localhost:20128/dashboard` 직접. 포트 변경: `9router --port 8080` (엔드포인트도 `http://localhost:8080/v1`로).
- Claude Code 401: `~/.claude/settings.json`의 `ANTHROPIC_AUTH_TOKEN`이 대시보드 API 키와 같은지, 앞뒤 공백 확인.
- 한도 후에도 모델이 안 바뀜: Combo 전략이 Fallback인지, 모델 매핑에 단일 모델이 아니라 Combo 이름 `claude-backup`이 들어갔는지, 다음 모델 공급자가 활성인지 확인.
- OAuth 만료: `Providers`에서 해당 공급자 `Reconnect`.
- "무료"인데 비용 표시: Usage 비용은 비교용 추정치일 수 있음, 실제 청구는 공급자 계정에서 확인. `glm/`, `kimi/` 직접 API 경로는 무료가 아닐 수 있음.

## 핵심 팁 · 주의사항
- ⚠️ 9Router를 깔아도 Claude 구독/유료 API 비용이 없어지지 않음. 무료 공급자를 Combo에 넣었을 때 그 경로만 무료.
- ⚠️ 9Router 터미널을 닫으면 연결이 끊김. 장시간 사용은 Docker나 OS 서비스로 실행(공식 문서 참고).
- ⚠️ 공급자 키는 `~/.9router/db/data.sqlite`(macOS/Linux 기본 경로)에 저장 → 이 파일과 계정 백업을 공개 저장소·공유 폴더에 올리지 말 것.
- ⚠️ 초기 비밀번호 즉시 변경, 20128 포트 비공개.
- Fallback 후 모델이 바뀌어 답변 품질이 달라질 수 있음. Claude 한도가 끝나도 Claude Code 프로세스와 로컬 대화는 유지.

## 바로 쓰는 체크리스트
- [ ] 비밀번호 변경, 포트 비공개
- [ ] 백업 공급자 연결, API 키 `claude-local` 생성
- [ ] Combo `claude-backup` = Fallback 전략, 매핑 `claude-backup`
- [ ] `~/.claude/settings.json` 백업 후 Apply
- [ ] 테스트 요청 후 Usage로 경로 확인
- [ ] (선택) Cursor 등에 Base URL/키/모델 입력
