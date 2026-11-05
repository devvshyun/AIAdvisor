# 무료 AI 에이전트 일곱 자리
- 원문: https://lazyowen.com/guides/agency-agents-7seats
- 도구·주제: agency-agents(Claude Code 서브에이전트 등) · 에이전트 팀 구성
- 한 줄 요약: 279개 에이전트 명단에서 필수 7명만 골라 설치하고 총괄(orchestrator)에게만 목표를 주는 방식. (2026-09-13 공개, 읽는 데 13분, 6단계 약 20분)

## 언제 쓰나
- 혼자 만들 때 화면·디자인·검수·보안·성장·광고까지 챙기기 버거워, 서브에이전트 팀을 빠르게 구성하고 싶을 때
- 코딩 AI를 부를 때마다 역할을 말로 설명하는 번거로움을 없애고, 총괄 1명에게 목표만 던져 나머지가 돌아가게 하고 싶을 때

## 준비물 / 필요 도구 (이름 + 공식 링크)
- 명단 저장소: https://github.com/msitarzewski/agency-agents (MIT, 279개/18부서)
- 클릭 설치 공식 앱: https://agencyagents.app/ · 앱 저장소 https://github.com/msitarzewski/agency-agents-app (명령줄 방식이 어느 도구에서나 동일해 가이드는 CLI 기준)
- 병렬 실행 별도 앱: https://github.com/chaitanyagiri/munder-difflin
- 서브에이전트 문서: https://docs.claude.com/en/docs/claude-code/sub-agents
- 설명서 원문: https://github.com/msitarzewski/agency-agents/blob/main/specialized/agents-orchestrator.md , `.../testing/testing-reality-checker.md` , `.../security/security-ai-generated-code-auditor.md`
- `git`, `bash` (없으면 macOS는 `xcode-select --install`, Windows는 https://git-scm.com/downloads). 터미널: macOS는 Cmd+스페이스 → 터미널, Windows는 PowerShell
- 비용: 명단 무료(MIT), 계정·결제 불필요. 원래 쓰던 AI 도구 요금만 발생.

## 단계별 방법
**Quick Start**
```
git clone --depth 1 https://github.com/msitarzewski/agency-agents.git ~/agency-agents
cd ~/agency-agents
./scripts/install.sh --tool claude-code \
  --agent frontend-developer,ui-designer,reality-checker,ai-generated-code-security-auditor,growth-hacker,ad-creative-strategist,agents-orchestrator
```
성공: `[OK] Claude Code: 7 agents -> /Users/내이름/.claude/agents`

1. **STEP 1 준비물 확인 (2분)**
   ```
   git --version
   bash --version
   ```
2. **STEP 2 명단 받기 (3분)**: 저장소 복사(파일만 받음, 아직 설치 아님).
   ```
   git clone --depth 1 https://github.com/msitarzewski/agency-agents.git ~/agency-agents
   cd ~/agency-agents
   ./scripts/install.sh --list teams
   ```
   - 부서별 인원 출력 예: design 10, engineering 64, marketing 36, paid-media 7, security 12, specialized 59, testing 9 (18부서 합 279). 전부 깔면 누구를 불러야 할지 모르게 되므로 금지.
3. **STEP 3 일곱 자리 고르기 (5분)**: 기준 = 혼자 만들 때 실제로 비는 자리만 채우기.
   | 자리 | 하는 일 | 설치 이름 |
   |---|---|---|
   | 화면 만들기 | 버튼·페이지 구현 | frontend-developer |
   | 보기 좋게 | 색·간격·컴포넌트 정리 | ui-designer |
   | 다 됐다는 말 의심 | 증거 없으면 통과시키지 않음(기본값 "아직 아닙니다") | reality-checker |
   | 구멍 찾기 | AI 생성 코드 보안 점검(코드에 박힌 키, 아무나 볼 수 있게 열린 데이터, 남이 시킨 말을 그대로 따르는 통로) | ai-generated-code-security-auditor |
   | 사람 데려오기 | 유입 경로·실험 설계 | growth-hacker |
   | 광고 문구 | 같은 제품을 파는 문장으로 변환 | ad-creative-strategist |
   | 총괄 매니저 | 목표를 받아 나머지 여섯에게 분배, 불합격 조각 재투입 | agents-orchestrator |
   - 값이 제일 큰 건 검사 자리 둘(reality-checker, 보안 감사). 나머지 다섯은 모두 "다 됐습니다"라고 말하는 자리.
4. **STEP 4 설치·확인 (3분)**: 먼저 `--dry-run`으로 개수 확인.
   ```
   ./scripts/install.sh --tool claude-code \
     --agent frontend-developer,ui-designer,reality-checker,ai-generated-code-security-auditor,growth-hacker,ad-creative-strategist,agents-orchestrator \
     --dry-run
   ```
   - 정상 출력: `The Agency -- Dry run (nothing written)` ... `Agents:  7   Mode: copy`. 이름이 틀리면 설치를 시작하지 않고 `[ERR] Unknown agent '...'. Use --list agents to see the available roster.` (반쯤 설치된 상태가 안 생김) → `./scripts/install.sh --list agents`로 이름 확인.
   - 실제 설치: 위 명령에서 `--dry-run`만 제거 → `[OK] Claude Code: 7 agents -> ~/.claude/agents`
   ```
   ls ~/.claude/agents
   ```
   - 7개: `agents-orchestrator.md`, `design-ui-designer.md`, `engineering-frontend-developer.md`, `marketing-growth-hacker.md`, `paid-media-creative-strategist.md`, `security-ai-generated-code-auditor.md`, `testing-reality-checker.md`. 글자 파일이라 열어서 수정 가능, 지우면 제거(되돌리는 방법은 이게 전부).
   - 다른 도구: `--tool`을 cursor, codex, copilot, gemini-cli, opencode 등으로. 일부는 설치 전 변환 필요:
   ```
   ./scripts/convert.sh --tool cursor
   ```
   변환 후 `install.sh --tool cursor`.
5. **STEP 5 총괄에게 목표 던지기 (5분)** — 핵심. 여섯을 직접 부르면 총괄이 없는 것과 같음.
   - 프롬프트 뼈대(내 AI 도구 대화창): "`agents-orchestrator`로 일해 줘" + 슬롯 `목표: <끝났을 때 눈에 보이는 결과물 한 줄>`, `건드리면 안 되는 것: <바꾸면 안 되는 파일·동작>`, `통과 기준: <예: 검사역이 실제로 눌러 본 기록>`. 지시: 순서는 네가 정하고 필요한 자리만 부르기 / 만든 뒤 `reality-checker`가 통과 기준으로 검사 / 코드가 바뀌면 `ai-generated-code-security-auditor`도 한 번 / 불합격이면 고쳐 재검사, 3번 해도 안 되면 나에게 질문.
   - 정상 신호: 총괄이 몇 조각으로 나눴는지, 조각마다 어느 자리에 넘겼는지 먼저 보고.
   - ❌ "이 프로젝트 좀 좋게 만들어 줘" → 여섯이 제각각 고치고 통과 기준이 없어 검사 불가. ✅ "신청 폼을 두 단계로 나눠 줘. 보내는 주소와 저장되는 값은 그대로, 끝나면 검사역이 실제로 눌러 본 기록을 남겨 줘"처럼 결과물·금지선·통과 기준을 한 문단에.
6. **STEP 6 늘리기 (2분, 익숙해진 뒤)**: 실제로 막히는 자리가 생겼을 때만. 부서 통째 추가:
   ```
   ./scripts/install.sh --tool claude-code --division security --dry-run
   ```
   (예: `Agents: 12`) 괜찮으면 `--dry-run` 제거. 명단 최신화:
   ```
   cd ~/agency-agents && git pull
   ```
   받은 뒤 설치 명령을 다시 돌리면 기존 파일이 최신 내용으로 덮임.

**통합 설치 위임 프롬프트 뼈대(Claude Code)**: 역할=일곱 자리 설치·연결 검증 담당. 슬롯 `<운영체제와 셸>`, `<쓰는 AI 도구>`, `<목표 한 줄>`. 작업: ① `git --version`, `bash --version`, `ls ~/.claude/agents`(이미 7개면 재설치 말고 파일명만 보고) ② 위 clone + `--dry-run` 후 설치 ③ `ls ~/.claude/agents | wc -l`로 7개 확인, `./scripts/install.sh --list agents | grep agents-orchestrator`로 총괄 존재 확인, 총괄에게 작은 일 하나를 시켜 응답 확인 ④ 일곱 자리 역할과 호출 순서를 5줄 이내로 설명. 제약: 홈 폴더 밖·현재 프로젝트 폴더 쓰기 금지, 7개 밖 임의 설치 금지, sudo 금지. 검증: dry-run `Agents: 7`, 설치 후 파일 7개. 실패 시 완료 보고 금지.

## 핵심 팁 · 주의사항
- ❌ 279개 전부 설치 / ❌ 여섯을 직접 부르기 / ❌ 검사 역할(reality-checker, 보안 감사) 제거 / ❌ 목표 대신 방법 적기("이 파일 열어서 함수 고쳐 줘") / ❌ 진짜 프로젝트 폴더에 바로 적용.
- ✅ 첫 시도는 새 빈 폴더에서 한 시간쯤 보고 나서 실제 작업물로 이동.
- 일곱 명이 동시에 일하는 게 아니라 한 도구 안에서 역할이 번갈아 바뀌는 방식. 병렬은 Munder Difflin 같은 별도 앱.
- 에이전트 파일은 글자 파일일 뿐, 실제 파일을 바꾸는 건 사용 중인 AI 도구이며 그 도구의 권한 설정이 적용됨 → 불안하면 "변경 전 확인" 켜기.
- 총괄이 3회 실패하면 멈추고 나에게 올림. 대개 통과 기준이 모호했던 경우이므로 기준을 한 줄 더 구체화해 재요청.

## 문제 해결
- `install.sh`를 실행할 수 없음: `cd ~/agency-agents`로 폴더 안인지 확인, 그래도 안 되면 `bash scripts/install.sh ...`.
- 이름 오타: 아무것도 설치되지 않으니 틀린 이름만 고쳐 재실행.
- 삭제: `~/.claude/agents`에서 해당 파일 삭제(설정 파일 안 남음).

## 바로 쓰는 체크리스트
- [ ] `git --version` / `bash --version` 확인
- [ ] clone → `--dry-run`(`Agents: 7`) → 설치
- [ ] `ls ~/.claude/agents` 7개 확인
- [ ] 총괄에게만 목표 + 건드리면 안 되는 것 + 통과 기준 전달
- [ ] 검수·보안 에이전트 실행 지시(3회 실패 시 사용자에게 질문)
