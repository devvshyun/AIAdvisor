# 클로드로 이력서를 탈락시키려는 채용 심사단 만드는 법
- 도구·주제: Claude Code 스킬 `hiring-panel` · 이력서 평가/개선
- 한 줄 요약: hiring-panel 스킬을 설치하면 자동 검사 1명 + 채용 관리자 1명 + 독립 평가자 5명이 이력서를 서로 다른 관점에서 심사해 탈락 사유 목록과 수정본을 만들어 준다.

## 언제 쓰나
- 수십 군데 지원해도 왜 탈락하는지 모를 때, 지원 전에 여러 관점으로 점검하고 개선본을 받고 싶을 때
- 공고가 있는 경우 / 회사 미정 / 분야 전환 / 첫 취업 / 클로드가 쓴 이력서 재평가 등 상황별로 평가받고 싶을 때

## 준비물 / 필요 도구
- hiring-panel-skill (MIT, 커뮤니티 프로젝트): https://github.com/alexyc9381/hiring-panel-skill
  - 평가 지침 SKILL.md: https://github.com/alexyc9381/hiring-panel-skill/blob/main/skills/hiring-panel/SKILL.md
  - 라이선스: https://github.com/alexyc9381/hiring-panel-skill/blob/main/LICENSE (재배포 시 저작권·허가 문구 유지)
- Claude Code (macOS 13+ / Windows 10 1809+ / Linux, 인터넷+로그인 계정)
  - 시작하기: https://code.claude.com/docs/en/quickstart
  - 환경 요건: https://code.claude.com/docs/en/setup
  - 터미널 안내: https://code.claude.com/docs/en/terminal-guide
  - 스킬 안내: https://code.claude.com/docs/en/skills
  - 권한 안내: https://code.claude.com/docs/en/permissions
  - Pro·Max 이용: https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- 비용: 스킬 파일 무료. Claude Code는 Pro·Max 등 이용 권한 또는 별도 사용량 결제. 평가 1회에 하위 에이전트 호출 8회 사용.
- 이력서 사본(PDF 또는 본문), 지원 공고(있으면)

심사단 구성(독립 평가자들은 서로의 의견을 보지 않고 이력서·공고를 읽음):
| 역할 | 먼저 보는 내용 |
|---|---|
| 자동 검사 | 글을 순서대로 읽을 수 있는지, 직무·날짜가 분명한지, 공고 핵심 기술이 있는지 |
| 채용 관리자 | 처음 10초에 면접 기회를 줄 이유가 보이는지 |
| 독립 평가자: 팀장 | 입사 직후 일을 맡길 수 있는지 |
| 독립 평가자: 다른 지원자 | 같은 자리 지원 이력서와 비교해 무엇이 약한지 |
| 독립 평가자: CEO | 어떤 변화를 만들었고 결과가 무엇인지 |
| 독립 평가자: 채용 담당자 | 30초 훑는 상단 3분의 1에 핵심이 있는지 |
| 독립 평가자: 동료 | 함께 일할 때 맡을 역할이 분명한지 |

## 단계별 방법
### 프롬프트 뼈대 A. 설치·준비 위임용 (선택)
- 목적: 설치와 시작 준비를 Claude Code에 맡기기
- 역할: 이력서 채용 심사단 설치·시작 준비 담당. 사용자는 개발 초보
- 슬롯: [내 목표] (예: 마케팅 직무 이력서의 탈락 사유 찾기), 운영체제·셸은 묻지 말고 직접 확인
- 작업: 작업 폴더와 `claude --version` 확인 → 공식 저장소를 읽고 `skills/hiring-panel`을 `~/.claude/skills/hiring-panel`에 설치 가능한지 확인(없을 때만 승인 받고 복사) → SKILL.md와 `name: hiring-panel` 존재 확인 → 일곱 관점 평가 설명과 새 세션에서 `/hiring-panel my-resume.pdf`로 시작하는 순서 안내
- 제약: sudo·전역 설치·설정 파일 수정 전 질문, 비밀키 출력·기존 파일 덮어쓰기 금지, 이력서 임의 탐색 금지, 평가 실행·결제는 승인 후, 자동 승인/권한 우회 모드 금지, 새 세션 확인 전엔 작동 확인 완료라 말하지 않기
- 출력: 실행 명령, 버전, 바뀐 파일, 남은 오류, 사용자가 새 세션에서 할 일
- 검증: 버전 숫자 + `(Claude Code)`, 설치 경로 SKILL.md에 `name: hiring-panel` 있어야 완료

### Quick Start (이미 Claude Code를 쓰는 경우)
실행 중인 Claude Code 입력창에 다음을 붙여넣는다(웹 채팅 아님).
```
https://github.com/alexyc9381/hiring-panel-skill Install this skill, then confirm /hiring-panel works.
```
성공하면 설치한 파일 경로를 안내받는다. 새 세션에서 `/hiring-panel`이 명령으로 인식되는지 확인.

### STEP 1. Claude Code에서 채용 심사단 설치
1. (이미 쓰고 있으면 생략) 맥은 Spotlight에서 터미널, 윈도우는 시작 메뉴에서 PowerShell을 연다. 회사 컴퓨터라면 설치 허가를 먼저 받고, 출처 모를 주소로 바꿔 실행하지 않는다.
맥:
```bash
curl -fsSL https://claude.ai/install.sh | bash
```
윈도우 PowerShell:
```powershell
irm https://claude.ai/install.ps1 | iex
```
2. 새 터미널 창에서 버전 확인
```bash
claude --version
```
`2.1.302 (Claude Code)`처럼 버전 뒤에 `(Claude Code)`가 붙으면 정상(숫자는 달라도 됨). 명령을 못 찾으면 Setup notes 확인 후 터미널 재시작.
3. 이력서 사본만 담을 새 폴더를 만들고 이동해서 실행(경로에 공백이 있으면 큰따옴표). PowerShell도 동일.
```bash
cd /path/to/your/project
claude
```
처음엔 브라우저 로그인. 구독으로 쓰려면 Pro·Max 등 이용 권한 계정 선택. 별도 API 결제는 구독과 따로 과금되며, 추가 비용을 원치 않으면 한도 도달 시 사용량 결제를 켜지 말고 초기화를 기다린다.
4. Quick Start의 두 줄을 보내 설치. 개인 스킬 위치는 `~/.claude/skills/hiring-panel/SKILL.md`. 같은 이름 스킬이 있으면 덮어쓰지 말고 기존 파일부터 확인.

### STEP 2. 새 세션에서 명령 확인
1. 현재 입력창에서 `Ctrl+D`를 두 번 눌러 종료
2. 같은 이력서 폴더에서 다시 실행
```bash
claude
```
3. `/hiring-panel`을 입력해 명령 후보에 뜨는지 확인(이력서는 아직 보내지 않아도 됨)
4. 안 보이면 설치 위치 점검
| 확인할 곳 | 맞는 상태 |
|---|---|
| 파일 이름 | 대문자 포함 `SKILL.md` |
| 개인 스킬 위치 | `~/.claude/skills/hiring-panel/SKILL.md` (폴더 바로 아래가 아니라 hiring-panel 폴더 안) |
| 파일 안 이름 설정 | `name: hiring-panel` |
| 실행하는 앱 | 터미널의 Claude Code |

### STEP 3. 개인정보와 파일 승인 범위 정하기
1. 이력서는 클로드로 전송된다. 주민등록번호·집 주소·실제 전화번호·회사 기밀은 사본에서 삭제. 연락처 칸 검사는 예시 값으로 대체.
2. 처음엔 작업을 직접 승인하는 Manual 모드. 파일 쓰기 전 경로가 현재 폴더 `.hiring-panel/` 아래인지 확인(점 때문에 탐색기에서 숨겨질 수 있음).
3. 승인 요청을 줄이려면 `acceptEdits` 모드(파일 수정, 폴더 생성·이동·복사 등 일부 명령 자동 허용). 범위를 이해한 뒤에만 입력창에서 `Shift+Tab`으로 전환하고, 끝나면 같은 키로 Manual 복귀. 중요한 파일과 분리하려면 별도 계정이나 가상 머신. 권한 확인을 전부 건너뛰는 모드는 선택 금지.

### STEP 4. 이력서와 채용 공고 넣기
1. 이력서 사본을 작업 폴더에 `my-resume.pdf`로 두기(다른 폴더면 전체 경로, 또는 본문을 명령 뒤에 붙여넣기)
```
/hiring-panel my-resume.pdf
```
지원 직무를 묻는 질문이 나오면 답한다.
2. 상황별 입력 중 하나만 고른다(평가 1회마다 사용량 소모). 대괄호는 내 내용으로 전부 교체.
- 공고 있을 때: 빠진 기술은 실제 경험이 있을 때만 보충
```
/hiring-panel [your resume file] for this job: [paste the posting]
```
- 회사 미정: 희망 직무에 도움이 되는 경력이 먼저 보이는지 확인
```
/hiring-panel [your resume file]. I am looking for [role] jobs at [kind of company].
```
- 분야 전환: 새 분야처럼 경력이 바뀌었다면 원래 사실로 되돌림
```
/hiring-panel [your resume file]. I am moving from [old field] to [new field]; judge whether my experience reads as relevant.
```
- 첫 취업(학생): 프로젝트·활동에서 맡은 역할이 드러나는지 확인, 학생이 아니면 문구 수정
```
/hiring-panel [your resume file]. I am a student with no full-time experience applying for [role].
```
- 클로드가 방금 쓴 이력서(같은 대화): 새 대화라면 이력서를 다시 전달
```
/hiring-panel The resume you just wrote me, for [role].
```

### STEP 5. 탈락 사유와 수정본 대조
결과는 현재 작업 폴더의 `.hiring-panel/날짜-이름/`에 저장된다.
| 결과에서 볼 것 | 읽는 방법 |
|---|---|
| PANEL.md | 일곱 평가와 중요도 순 문제 목록 |
| RESUME-IMPROVED.md | 문제 목록을 반영한 새 이력서, 원문과 대조 |
| 자동 검사 PASS / REJECT | 통과·탈락 판정, 수정 전후 비교 |
| 채용 관리자 INTERVIEW / NO | 면접 기회를 줄지 보는 모의 판단 |
| 독립 평가자 HIRE / MAYBE / PASS | 채용·유보·불채용 판단(자동 검사 통과와 혼동 금지) |
| `[ADD: ...]` | 내가 사실을 추가해야 하는 자리 |
| assumed | 평가자 추정 부분, 사실 확인 |

대조 절차:
1. 원문·수정본에서 같은 경력을 찾아 회사·직무·근무 기간 일치 확인
2. 새로 들어간 도구·업무를 표시하고 직접 써 봤거나 맡은 일만 남기기
3. 성과 숫자를 기록과 대조(모르면 추측 금지)
4. `[ADD: ...]` 칸은 확인한 사실로 채움. 알 수 없는 값이 필요하면 표현을 고치고, 빈칸 상태로 제출 금지
5. 자동 검사 결과가 안 바뀌었다면 남은 탈락 사유 문장을 다시 점검. 지원 전 공고의 제출 형식도 직접 확인.

스킬 삭제: 개인 스킬 폴더의 `hiring-panel`만 삭제(직접 고친 파일은 먼저 백업, 이미 만든 `.hiring-panel/` 결과물은 영향 없음).

## 핵심 팁 · 주의사항
- ❌ 일반 웹 채팅에 주소만 보내고 컴퓨터에도 설치됐다고 믿기 → ✅ 터미널의 Claude Code에서 Quick Start 두 줄을 보내고 설치 경로 확인
- ❌ 설치했다는 답만 보고 이력서부터 보내기 → ✅ 새 세션의 명령 후보와 스킬 파일 위치를 함께 확인
- ❌ 회사 문서가 섞인 폴더에서 자동 승인 켜기 → ✅ 이력서 사본만 둔 전용 폴더, 첫 실행은 직접 승인
- ❌ 이력서만 주고 어느 회사에나 맞게 고쳐 달라 하기 → ✅ 지원 공고를 함께 주고 필요 경험이 보이는지 확인
- ❌ 공고에 필요하단 이유로 써 본 적 없는 도구 추가 → ✅ 실제 경험만 구체적으로, 없는 경험이 추가됐다면 원래 사실로 되돌림
- 설치 파일이 있는 것과 실제 평가가 끝난 것은 별개
- 평가는 사용량을 쓰므로 상황별 프롬프트를 전부 실행하지 말고 하나만

## 바로 쓰는 체크리스트
- [ ] 개인정보를 지운 이력서 사본 전용 폴더 준비
- [ ] Claude Code 설치(`claude --version`에 `(Claude Code)`)·로그인
- [ ] 스킬 설치 요청 → `Ctrl+D` 두 번 후 새 세션에서 `/hiring-panel` 확인
- [ ] Manual 모드로 상황에 맞는 입력 하나 실행
- [ ] PANEL.md 검토, RESUME-IMPROVED.md를 원문과 대조
- [ ] `[ADD: ...]`·assumed 항목 사실 확인 후 제출 형식 점검
