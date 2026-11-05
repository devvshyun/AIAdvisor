# 9Router 백업 모델 설정
- 도구·주제: 9Router + Claude Code · 비용 절약 / 한도 이후 무료 폴백
- 한 줄 요약: 로컬 라우터 9Router의 Fallback Combo로, Claude Code 한도 소진 시 무료 모델로 자동 이어가는 9단계 설정. (갱신 2026-08-19, 읽는 데 11분)

## 언제 쓰나
- Claude Code가 한도에 걸린 뒤에도 Kiro AI / OpenCode Free 등 무료 모델로 계속 코딩하고 싶을 때
- 구조: Claude Code는 `http://localhost:20128/v1` 한 곳으로만 요청 → 9Router가 Combo(`claude-backup`)의 첫 모델이 한도 초과/공급자 오류를 내면 다음 모델을 순서대로 시도, 성공한 공급자·모델은 Usage에 기록. Claude Code 프로세스와 로컬 대화는 유지되지만 모델이 바뀌면 품질·도구 호출 방식·지원 기능이 달라질 수 있음.

## 준비물 / 필요 도구
- 9Router: https://github.com/decolua/9router (README `#-quick-start`) · 사이트 https://9router.com/ · npm https://www.npmjs.com/package/9router · Docker https://github.com/decolua/9router/blob/master/DOCKER.md · 이슈 https://github.com/decolua/9router/issues (MIT 오픈소스)
- Claude Code: npm 패키지 `@anthropic-ai/claude-code`
- Node.js 18 이상 (설치 오류 시 20 이상 LTS로 올린 뒤 재시도)
- 공급자: Claude Code(기존 Pro/Max 구독, OAuth) / OpenCode Free(무인증, 현재 제공 모델 자동 로드) / Kiro AI(AWS Builder ID·Google·GitHub 로그인) / GLM·Kimi(직접 API 키) / Vertex AI(신규 크레딧 조건 확인)
- 무료 경로 판단표: 9Router 프로그램=MIT 무료 / OpenCode Free=무인증 무료(모델 변동) / Kiro `kr/`=무료 경로(실제 할당량·약관은 공급자 정책 확인) / Claude Code `cc/`=기존 구독 필요 / GLM `glm/`·Kimi `kimi/`=직접 API 키·과금 조건 확인 / Vertex AI=신규 계정 크레딧 조건·만료 확인. 무료 모델 이름을 외우기보다 대시보드에서 현재 활성 모델을 확인.

## 단계별 방법
1. **설치·실행 (3분)**
   ```
   node --version
   npm --version
   npm install -g 9router
   9router
   ```
   - 터미널에 `Server: http://localhost:20128`이 나오고 대시보드가 열리면 성공. 자동으로 안 열리면 직접 접속:
   ```
   http://localhost:20128/dashboard
   ```
   - 옵션: `9router --no-browser`(브라우저 자동 열기 없이), `npx 9router`(전역 명령 문제 우회), `9router --port 8080`(이 경우 Claude Code Endpoint도 `http://localhost:8080/v1`로).
2. **대시보드 비밀번호 변경 (2분)**: 초기 비밀번호 `123456`. 로그인 후 `Profile` → `Security`에서 변경, 로그아웃 후 재로그인으로 확인. OAuth 토큰·API 키가 로컬 DB에 저장되므로 포트 20128을 인터넷에 열지 말 것.
3. **공급자 연결 (5분)**: `Providers` → 기존 구독이면 Claude Code(OAuth 로그인), 무료 백업으로 `OpenCode Free` 또는 `Kiro AI` 연결. 카드가 `ACTIVE`이고 모델 선택 창에 해당 모델이 보이면 성공.
4. **로컬 API 키 (2분)**: `Endpoint` → `API Keys` → `Create Key`, 이름 예:
   ```
   claude-local
   ```
   - 비밀번호처럼 취급(GitHub·캡처·공유 문서 금지).
5. **Fallback Combo (5분)**: `Combos` → `Create Combo`, 이름(영문·숫자·`.`·`_`·`-`만):
   ```
   claude-backup
   ```
   - 모델 순서: ① Claude Code 공급자의 현재 Sonnet ② Kiro AI의 현재 Claude 또는 GLM 코딩 모델 ③ OpenCode Free의 현재 코딩 모델. 공식 문서 ID 예: `cc/claude-sonnet-4-6`, `kr/claude-sonnet-4.5`, `kr/glm-5`, `oc/`로 시작하는 현재 OpenCode Free 코딩 모델. 선택 창에 없는 ID를 억지로 입력하지 말고 표시된 모델에서 고를 것.
   - 전략은 `Fallback — try in order`. (Round Robin=요청마다 시작 모델을 돌려 씀, 한도 소진 후에만 넘기려는 목적과 다름 / Fusion=여러 모델 동시 호출 후 판정 모델이 합침, 호출량 증가로 무료 백업에 부적합.) 확인: 카드에 순서가 보이고 전략이 Fallback.
6. **Claude Code 설치 (3분)**
   ```
   npm install -g @anthropic-ai/claude-code
   claude --version
   ```
7. **Claude Code를 Combo에 연결 (5분)**: 대시보드 `CLI Tools` → `Claude Code`: Select Endpoint에서 `http://localhost:20128/v1`, API Key는 `claude-local`, Claude 모델 매핑을 전부 `claude-backup`으로 → `Apply`. 9Router가 `~/.claude/settings.json`의 `env`에 병합 저장하므로 적용 전 백업:
   ```
   cp ~/.claude/settings.json ~/.claude/settings.json.backup
   ```
   - 자동 적용이 안 될 때만 수동(기존 항목이 있으면 파일 전체를 교체하지 말고 `env`만 병합, 완성 파일 공유 금지):
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
   - 확인: Claude Code 카드 `Connected`, Endpoint가 `/v1`로 끝남.
8. **연결·Fallback 테스트 (3분)**: 9Router 터미널은 유지하고 새 터미널에서 `claude` 실행 후 짧은 읽기 전용 요청 — 요지: 현재 폴더 파일은 수정하지 말고 "9Router 연결 성공"이라고 한 줄만 답하라. 응답 후 대시보드 `Usage`에서 사용된 공급자·모델 확인. Fallback 확인: `Providers`에서 주 공급자만 잠시 비활성화하고 같은 요청 재전송 → Usage에 Combo의 다음 모델이 찍히면 정상 → 테스트 후 주 공급자 재활성화.
9. **업데이트·종료 (1분)**
   ```
   npm install -g 9router@latest
   ```
   - 종료는 실행 중인 터미널에서 `Ctrl+C` (9Router가 꺼지면 Claude Code도 `localhost:20128`에 연결 불가). 장시간 실행은 공식 Docker 문서 참고.

## 핵심 팁 · 주의사항
- ❌ 9Router가 Claude 구독/유료 API를 무료로 바꿔 준다고 기대: 아님. Combo에 무료 공급자 모델을 넣은 경로만 무료. Usage의 비용 표시는 비교용 추정치일 수 있고, `glm/`·`kimi/` 같은 직접 API 모델은 공급자 요금이 발생할 수 있음(실제 청구는 공급자 계정에서 확인).
- ❌ 9Router 터미널을 닫기 / 포트 20128 인터넷 공개 / 초기 비밀번호 방치 / 키·settings 파일 공유.
- 키/OAuth 토큰 저장 위치(macOS·Linux): `~/.9router/db/data.sqlite` — 이 파일과 백업본을 공개 저장소·공유 폴더에 올리지 말 것.
- Fallback은 한도·라우팅 가능한 오류용. 잘못된 API 키, 깨진 설정, 지원하지 않는 도구 호출은 직접 수정해야 함. 첫 설정 후 반드시 Usage로 실제 경로 확인.
- 무료 모델·할당량은 공급자 정책에 따라 변동, 각 공급자 약관 확인.

## 문제 해결
- `9router: command not found`: `npm prefix -g`, `npm list -g 9router --depth=0` 확인 → 없으면 `npm install -g 9router`, 또는 `npx 9router`.
- 대시보드가 안 열림: 실행 중인지 확인 후 `http://localhost:20128/dashboard` 직접 접속(포트 변경 시 Endpoint도 변경).
- Claude Code 401: `~/.claude/settings.json`의 `ANTHROPIC_AUTH_TOKEN`이 대시보드 API 키와 같은지, 앞뒤 공백 제거.
- 모델을 찾을 수 없음: Combo 저장 모델이 현재 공급자 목록에 있는지 확인, 선택 창에서 다시 고름.
- 한도 후 무료로 안 넘어감: 전략이 Fallback인지 / 매핑이 단일 모델이 아니라 `claude-backup`인지 / 다음 공급자 카드가 ACTIVE인지 / Usage에서 첫 모델 오류와 실제 선택 모델 확인.
- OAuth 만료: `Providers`에서 해당 공급자 열고 `Reconnect`(자동 갱신 실패/재로그인 요구 시 직접 인증).

## 바로 쓰는 체크리스트
- [ ] Node 18+ 확인, `npm install -g 9router` 후 `9router` 실행
- [ ] 대시보드 초기 비밀번호 `123456` 변경
- [ ] 주 공급자 + 무료 백업 1개 이상 `ACTIVE`
- [ ] API 키(`claude-local`) 생성, Combo(`claude-backup`) 전략 = Fallback
- [ ] `settings.json` 백업 후 Apply, `Connected` 확인
- [ ] Usage로 실제 경로 확인, 주 공급자 끄고 폴백 시험 후 재활성화
- [ ] 9Router 터미널 계속 실행
