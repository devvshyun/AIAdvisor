# 메일 답장, 이제 클로드한테 맡기는 세팅법
- 원문: https://lazyowen.com/guides/inbox-zero-claude-email-setup
- 도구·주제: Inbox Zero · Claude Code(또는 Claude 앱 커넥터) · 이메일 분류/답장 초안 자동화 (2026-10-08 갱신, STEP 5개 · 약 60분)
- 한 줄 요약: Gmail/Outlook 위에서 동작하는 오픈소스 AI 메일 비서 Inbox Zero로 분류·답장 초안·후속 연락 추적을 켜고, API 키+CLI(또는 커넥터)로 Claude가 규칙과 통계를 읽기 전용으로 점검하게 하는 5단계.

## 언제 쓰나
- 메일 분류, 답장 초안 작성, 답장 대기 추적, 뉴스레터 정리를 자동화하되 발송은 직접 통제하고 싶을 때
- 보내기 전에는 내 승인을 기다리게(초안은 임시보관함에만 저장) 하고 싶을 때
- Inbox Zero는 새 메일 앱이 아니라 지메일·아웃룩 메일함 뒤에서 일하는 AI 비서

## 준비물 / 필요 도구
- Inbox Zero: https://www.getinboxzero.com · 로그인/가입 https://www.getinboxzero.com/login · GitHub https://github.com/elie222/inbox-zero (스타 12,390, 만든 곳 Inbox Zero Inc.)
- 라이선스: AGPL-3.0 + 추가 조건. 개인·교육용, 업무 사용자 5명 미만 조직은 제약 없음, 5명 이상이 업무에 쓰면 기업 라이선스 필요
- 메일 계정: Gmail(Google Workspace 포함) 또는 Outlook(Microsoft 365 포함) + 웹 브라우저
- 터미널 점검 단계(STEP 3~4) 전용: 맥/리눅스 터미널, Claude Code(Pro·Max 등 유료, 설치 https://code.claude.com/docs/en/setup), Node.js 18 이상(https://nodejs.org/), npm 패키지 `@inbox-zero/api`
- Claude 앱 커스텀 커넥터 MCP URL: `https://www.getinboxzero.com/mcp` (커넥터 칸에 붙여넣는 주소, 브라우저로 여는 주소 아님)
- 비용: 모든 요금제 7일 무료 체험. Starter 사용자당 월 $20~, Plus 월 $35(Slack 연동, 첨부 자동 정리는 Plus부터)
- Windows: `read -s`, `export`, `test`가 PowerShell에서 안 되므로 WSL 또는 Claude 앱 커넥터 경로 사용
- 문서: 시작 https://docs.getinboxzero.com/essentials/getting-started · 규칙 https://docs.getinboxzero.com/essentials/email-ai-personal-assistant · 설정 https://docs.getinboxzero.com/essentials/assistant-settings · 콜드메일 https://docs.getinboxzero.com/essentials/cold-email-blocker · 뉴스레터 https://docs.getinboxzero.com/essentials/bulk-email-unsubscriber · 캘린더 https://docs.getinboxzero.com/essentials/calendar-integration · 미팅 브리핑 https://docs.getinboxzero.com/essentials/meeting-briefs · 첨부 정리 https://docs.getinboxzero.com/essentials/auto-file-attachments · API https://docs.getinboxzero.com/api-reference/introduction · CLI https://docs.getinboxzero.com/api-reference/cli · MCP https://docs.getinboxzero.com/essentials/mcp · 요금 https://www.getinboxzero.com/pricing

## 단계별 방법
**Quick Start**: https://www.getinboxzero.com 가입 → 관리할 Gmail/Outlook 계정 하나 연결 → 왼쪽 사이드바에 `Assistant` 메뉴가 보이면 성공(기본 규칙 안내가 나옴)

**규칙 점검 위임 프롬프트 뼈대 (Claude Code)** — STEP 1 메일함 연결, STEP 3 키 입력 후 같은 터미널에서 `claude` 실행하여 첫 메시지로
- 역할: Inbox Zero API CLI 설치·연결 확인 + 메일 규칙 점검 담당. 맥락: 웹에서 메일 연결은 끝남, CLI는 미설치일 수 있음, 초보
- 채울 곳: [내 목표 — 예: 지난주 통계로 답장이 밀린 이유와 고칠 규칙 3개 찾기]
- 작업: ① `node --version`이 18 이상인지 확인(미달이면 설치 중단하고 nodejs.org 안내) ② `inbox-zero-api --version` 실패 시에만 질문 후 `npm install -g @inbox-zero/api`. EACCES면 sudo 금지, `npx -y @inbox-zero/api --version` 방식으로 전환하고 이후 명령도 같은 방식 ③ `test -n "$INBOX_ZERO_API_KEY" && echo 설정됨`으로 값 노출 없이 확인 후 `inbox-zero-api rules list --json`, `inbox-zero-api stats by-period --period week --json` 실행 ④ 겹치는 규칙·잘못 걸릴 규칙·놓친 후속 연락을 찾아 가장 효과 큰 개선 3가지를 설명
- 제약: 이번엔 아무것도 변경 금지(`rules create/update/delete`, `senders unsubscribe` 실행 금지, 바꿀 내용만 제시), 전역 설치 전 질문·sudo 금지, 키를 채팅에 요구하거나 출력 금지, 메일 보내기 규칙 생성 금지
- 출력/검증: 실행 명령, Node·CLI 버전, 현재 규칙 이름 목록, 개선안 3개(바꿀 규칙·문장), 남은 오류. `--version`이 숫자를 내고 `rules list --json`이 "rules" 항목의 JSON을 내야 함. `[object Object]` 한 줄이면 키 오류=실패

**STEP 1. 메일함 하나 연결하고 지켜보기 (10분)**
1. 공식 사이트에서 계정 생성
2. 관리할 Gmail/Outlook 하나만 연결(회사 메일 전체가 아니라 내 메일함 하나부터). 권한 승인 화면은 읽기·정리, 초안 만들기, 보내기 권한을 요청함
3. 최근 메일이 분류될 때까지 기다리고, 자동화를 켜기 전에 분류 결과를 훑어봄
4. 연결 직후 Assistant에서 Cold Email 규칙을 열어 `Notify sender`(걸러진 메일 발신자에게 자동 알림 메일 발송, Gmail 기본값)를 휴지통으로 제거. 메일함에 그대로 두려면 `Archive`도 제거 → `Save`
5. 기본 규칙 확인(왼쪽 스위치로 켜고 끔): To Reply(답장 필요) · Awaiting Reply(답장 대기) · Newsletter · Calendar · Notification · Cold Email. 메일별 매칭 규칙은 History 탭에서 확인
- 라벨 이름 제안: 급함 · 답장 필요 · 답장 대기 / 고객 · 리드 · 팀 / 일정 · 뉴스레터 · 알림 · 콜드메일 (콜드메일 = 주고받은 적 없는 사람의 영업 메일)

**STEP 2. 열 가지 업무를 규칙으로 나누기 (20분)**
- 규칙 만들기: Assistant → 오른쪽 위 `Add Rule` → 입력칸에 처리 방식을 문장으로 → `Create rules`. 저장 후 `Test` 탭에서 최근 메일 선택 → `Test All`: 실제 동작 없이 어떤 규칙에 걸리는지만 표시
| # | 업무 | 켜는 곳 | 설정 |
|---|---|---|---|
| 1 | 콜드메일 걸러내기 | Assistant의 Cold Email 규칙 | 처음엔 `Notify sender`·`Archive` 빼고 저장(라벨만 붙고 메일함은 그대로) |
| 2 | 급한 메일 표시 | Assistant 규칙 | 예: "오늘 안에 답이 필요한 고객 메일에 급함 라벨" |
| 3 | 내 말투로 답장 초안 | Assistant → Settings | `Auto draft replies` 켜기 + `Writing style`에 말투 (임시보관함에 저장만, 자동 발송 안 함) |
| 4 | 후속 연락 시점 추적 | Assistant → Settings | `Follow-up reminders` 켜고 `Configure`에서 며칠 뒤 알릴지 |
| 5 | 돈 되는 리드 분류 | Assistant 규칙 | 예: "견적·도입 문의 메일에 리드 라벨" |
| 6 | 미팅 전 고객 브리핑 | 사이드바 Meeting Briefs | 캘린더 연결 후 `Enable Meeting Briefs` |
| 7 | 일정 잡기 답장 | 사이드바 Calendars | 캘린더 연결 → 가능한 시간을 넣은 초안 |
| 8 | 첨부파일 폴더 정리 | 사이드바 Attachments | Google Drive/OneDrive 연결 (Plus 요금제) |
| 9 | 뉴스레터 정리 | 사이드바 Bulk Unsubscribe | 안 읽는 발신자를 골라 구독 해지·보관 |
| 10 | 메일 통계로 규칙 개선 | 터미널·클로드 | STEP 3~4 |
- Starter 요금제는 8번을 건너뛰고 나머지 9개로 시작
- 규칙 문장은 범위를 구체적으로. 예시 뼈대: "답이 필요한 고객 메일에만 짧은 초안을 쓰고 저장만 해. 날짜·가격·약속은 지어내지 마."
- ❌ "고객 메일은 알아서 처리해 줘"(어디까지인지 없어 엉뚱한 메일에 동작) → ✅ 위처럼 범위+금지 조건 명시
- 규칙 동작에 `Send replies`·`Forward`·`Send email`(Available Actions)을 넣지 말 것: 승인 없이 메일이 나갈 수 있음
- 콜드메일 차단은 켠 뒤 새로 들어오는 메일부터 걸러짐 → 켠 다음 들어온 메일로 확인

**STEP 3. API 키 넣고 점검 도구 설치 (15분)** — 아래는 맥·리눅스 터미널 기준(맥은 ⌘+스페이스 → 터미널). API 키 = 다른 프로그램이 내 계정에 들어올 때 쓰는 비밀번호
1. API 키 생성: Inbox Zero `Settings` → 아래쪽 `API Keys` → `Create New Secret Key`
   - 권한은 필요한 것만: 읽기 점검은 `RULES_READ` + `STATS_READ`, 규칙 수정은 `RULES_WRITE`
   - 만료 기간 설정. 키는 비밀번호 관리자에 보관(채팅·노션·코드에 붙이지 말 것)
2. 키를 터미널에 넣기 — **한 줄씩** 실행(두 줄을 한꺼번에 붙여넣으면 둘째 줄이 키 자리에 들어가고 이어 붙인 진짜 키가 명령으로 실행돼 기록에 남을 수 있음)
```bash
read -s INBOX_ZERO_API_KEY && export INBOX_ZERO_API_KEY
# 아무것도 안 보이는 게 정상. 키를 붙여넣고 Enter
test -n "$INBOX_ZERO_API_KEY" && echo 설정됨
```
   - 이 터미널을 닫으면 키도 사라지므로 같은 창에서 `claude` 실행
   - ❌ 키를 클로드 대화창에 붙여넣기(기록에 남음) → ✅ 터미널 `read -s`로 넣고 클로드에는 "키가 들어 있는지만 확인해"
3. 점검 도구 설치(위 위임 프롬프트가 대신 확인함)
```bash
node --version                 # v18 이상
npm install -g @inbox-zero/api
inbox-zero-api --version       # 예: 2.29.2
```
   - 이미 깔려 있으면 생략. `EACCES`/permission denied가 나면 sudo 대신:
```bash
npx -y @inbox-zero/api --version
```
   - 이 경로로 왔다면 이후 명령의 `inbox-zero-api`를 `npx -y @inbox-zero/api`로 바꿔 사용

**STEP 4. 클로드에게 규칙 점검 맡기기 (10분)** — 클로드는 아무것도 바꾸지 않고 읽기만
```bash
inbox-zero-api rules list --json
inbox-zero-api stats by-period --period week --json
claude
```
- `rules list --json` 성공: `{`로 시작하고 `"rules"` 아래 규칙 이름 나열. `Missing API key` → STEP 3 키 넣기 재수행. `[object Object]` 한 줄 → 키가 틀렸거나 만료, 새 키로 재입력
- `stats by-period`(STATS_READ 필요): 기간별 전체·보낸·읽은·안 읽은·보관한 메일 수 JSON
- 프롬프트 뼈대 ① 검토: 내 규칙과 이번 주 메일 통계를 점검, 아무것도 바꾸지 말 것, 겹치는 규칙·잘못 걸릴 규칙·놓친 후속 연락을 찾아 가장 효과 큰 개선 3가지를 정확한 변경안과 함께 제시하고 승인 대기
- 프롬프트 뼈대 ② 적용(고른 것만): 승인한 변경만 적용, 규칙은 한 번에 하나씩 바꾸고 결과 확인 후 전후 요약, 메일 보내기 규칙 생성·권한 확대 금지
- 규칙 수정에는 `RULES_WRITE` 권한 필요. 실수 줄이기: 점검용 키와 수정용 키를 따로 생성
- ❌ "규칙 알아서 다 고쳐 줘" → ✅ 읽기만 → 제안 확인 → 고른 것만 하나씩 적용
- 터미널 없이 Claude 앱 커넥터 경로:
  1. Settings(설정) → Connectors(커넥터) (왼쪽 아래 프로필 → 설정 → 사용자 지정 아래 커넥터)
  2. 오른쪽 위 Add → Add custom connector
  3. 이름 `Inbox Zero`, MCP 서버 URL `https://www.getinboxzero.com/mcp` → Continue → Inbox Zero 로그인 → Allow
  4. 대화창 `+` → Connectors에서 Inbox Zero 켜기
  - 메일 검색·초안 만들기·규칙 관리는 되지만 메일 발송은 불가

**STEP 5. 첫 주는 하루에 하나씩 켜기 (5분)**
| 날짜 | 할 일 |
|---|---|
| 1일 | 연결하고 분류만 지켜보기 |
| 2일 | 답장 초안·후속 연락 알림 켜기 |
| 3일 | 콜드메일·뉴스레터 정리 (Plus면 첨부파일 정리도) |
| 4일 | API 키 만들고 클로드로 읽기 점검 |
| 5일 | 승인한 규칙만 고치기 |
- 롤백:
```bash
npm uninstall -g @inbox-zero/api    # 성공하면 removed 2 packages
```
  API 키는 Settings → API Keys에서 삭제

## 핵심 팁 · 주의사항
- 규칙 동작에 답장 보내기·전달·메일 보내기를 넣지 말 것(승인 없이 발송 가능). 초안은 임시보관함에만 저장
- Gmail 기본 Cold Email 규칙의 `Notify sender`는 즉시 제거
- 직접 처리할 것(초안만 맡기고 발송은 직접): 가격·범위 변경, 계약·법률 문구, 환불·결제 분쟁, 민감한 고객 문제, 채용 결정, 보안 사고
- 매주 점검: 내가 답해야 할 메일/상대 답을 기다리는 메일, 콜드메일로 잘못 빠진 고객 메일, 많이 고쳐 쓴 초안, 안 쓰는 API 키·연결 앱
- 키는 비밀번호 관리자에 보관, 필요 권한만, 만료일 설정

## 바로 쓰는 체크리스트
- [ ] 개인 메일함 하나만 연결
- [ ] Cold Email 규칙의 `Notify sender`(와 필요시 `Archive`) 제거
- [ ] 규칙에 Send replies/Forward/Send email 동작이 없는지 확인, `Test All`로 매칭 확인
- [ ] 필요 권한만 가진 API 키 생성(만료일 설정), `read -s`로 입력
- [ ] `inbox-zero-api rules list --json` 성공 확인
- [ ] 검토 프롬프트 → 상위 3개 변경안 → 승인 후 적용 프롬프트
- [ ] 하루 한 기능씩 켜고 주간 점검
