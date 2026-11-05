# Claude Code 스킬 TOP 5, 겹치지 않게 설치하는 가이드
- 원문: https://lazyowen.com/guides/claude-skills-top5
- 도구·주제: Claude Code 플러그인 (superpowers, ECC, karpathy-skills, awesome-claude-code, wshobson/agents) · 스킬/플러그인 선택·설치
- 한 줄 요약: 많이 깔지 말고 역할이 안 겹치게 하나씩 설치하고, `claude plugin details`로 고정(always-on) 토큰 비용까지 확인하라는 가이드.

## 언제 쓰나
- 인기 Claude Code 확장 중 무엇을 깔지, 겹침·토큰 비용 없이 고르고 싶을 때
- (갱신 2026-09-30, Star 조회 2026-07-27, 읽는 데 18분 / 따라 하면 약 32분, 8단계)

## 준비물 / 필요 도구
| 순위 | 저장소 | Star(07-27) | 역할 |
|---|---|---|---|
| 1 | https://github.com/obra/superpowers (마켓플레이스 https://github.com/obra/superpowers-marketplace) | 261,677 | 설계·계획·TDD·리뷰·완료 검증 방법론 |
| 2 | https://github.com/affaan-m/ECC (사이트 https://ecc.tools) | 233,723 | 스킬·에이전트·메모리·보안·규칙 통합 운영 환경 |
| 3 | https://github.com/multica-ai/andrej-karpathy-skills | 196,614 | 잘못된 가정·과잉 구현을 줄이는 행동 규칙 4가지 |
| 4 | https://github.com/hesreallyhim/awesome-claude-code | 51,024 | 큐레이션 목록(설치 대상 아님) |
| 5 | https://github.com/wshobson/agents | 38,266 | 전문가 플러그인 마켓플레이스(개별 선택) |
- Star는 원문 후보 10개 안에서의 비교이며 GitHub 전체 순위가 아니고 품질·안전 보증도 아님. 계속 변동.
- 문서: https://code.claude.com/docs/en/setup , https://code.claude.com/docs/en/discover-plugins , https://claude.com/plugins , GitHub REST 조회 https://docs.github.com/en/rest/repos/repos#get-a-repository
- 용어: 마켓플레이스=플러그인 목록 장터, 플러그인=규칙·기능 확장, always-on 토큰=대화 시작 때마다 자동으로 먼저 들어가는 분량, 훅=도구 사용 전후 자동 실행되는 점검 코드, TDD=실패하는 테스트를 먼저 쓰고 최소 수정으로 통과시키는 방식.

## 단계별 방법
**Quick Start** — Claude Code 설치
```
curl -fsSL https://claude.ai/install.sh | bash
```
(macOS/Linux/WSL, 설치 후 터미널 재시작) Windows PowerShell:
```
irm https://claude.ai/install.ps1 | iex
claude --version
```
Superpowers 최소 경로 + 연습 폴더에서 열기:
```
claude --version
claude plugin marketplace add obra/superpowers-marketplace --scope user
claude plugin install superpowers@superpowers-marketplace --scope user
claude plugin list --json
mkdir -p "$HOME/claude-skill-test"
cd "$HOME/claude-skill-test"
claude
```
성공 시 `✔ Successfully installed plugin: superpowers@superpowers-marketplace (scope: user)`와 목록에 `enabled: true`.
첫 확인 프롬프트(짧게): 작은 할 일 앱을 만들고 싶으니 파일은 수정하지 말고 질문으로 결과를 확인한 뒤 선택지·검증 기준이 있는 설계만 보여 달라. → 바로 코드를 쓰지 않고 목적·제약을 먼저 물으면 성공.

1. **STEP 1 Star 순위와 역할 구분 (3분)**: 위 표 참고. awesome-claude-code는 목록, wshobson/agents는 개별 플러그인 장터라 다섯 개가 같은 종류가 아님. 숫자만 보고 다 깔지 말 것.
2. **STEP 2 겹치지 않는 조합 고르기 (3분)**: always-on 토큰은 `claude plugin details <플러그인 ID>`의 `Projected token cost`에서 직접 확인(2026-07-27 실측).
   | 플러그인 ID | always-on 토큰 |
   |---|---|
   | superpowers@superpowers-marketplace | 584 |
   | ecc@ecc | 24,048 |
   | andrej-karpathy-skills@karpathy-skills | 66 |
   | unit-testing@claude-code-workflows | 111 |
   - Superpowers+ECC 동시=매 대화 24,632 토큰 고정. 처음엔 Superpowers 하나(설치 2줄, 584토큰). ECC는 더 넓은 구성이 필요할 때 Superpowers 대신. Karpathy는 짧은 규칙 4개만 원할 때. awesome-claude-code는 북마크, wshobson은 필요한 하나만.
   - 프롬프트 뼈대: `<하고 싶은 작업>`을 주고 Superpowers/ECC/Karpathy 중 기본 도구 하나만 추천(이유·달라지는 점·겹침 시 혼란), 설치·파일 변경 금지. → 추천 1개와 제외 2개의 이유가 나오면 성공.
3. **STEP 3 Superpowers (5분)**: 아이디어 확인→설계 승인→구현 계획→TDD→코드 리뷰→완료 검증 흐름. 관련 스킬은 상황에 맞춰 자동 선택. 제작자 운영 마켓플레이스라 등록을 건너뛰면 설치 실패.
   ```
   claude plugin marketplace add obra/superpowers-marketplace --scope user
   claude plugin install superpowers@superpowers-marketplace --scope user
   claude plugin list --json
   claude plugin details superpowers@superpowers-marketplace
   ```
   - 기대값: superpowers 6.2.0, Skills (14), `Always-on: ~584 tok`.
   - 첫 작동 프롬프트 뼈대: 현재 폴더에서 만들 수 있는 가장 작은 예제 제안, 파일 수정 금지, 요구사항 질문 먼저 + 승인용 설계·테스트 기준 제시. 바로 파일을 만들면 새 세션에서 목록 재확인.
4. **STEP 4 ECC 대안 (5분)**
   ```
   claude plugin marketplace add https://github.com/affaan-m/ECC --scope user
   claude plugin install ecc@ecc --scope user
   claude plugin list --json
   claude plugin details ecc@ecc
   ```
   - 기대값: ecc 2.0.0, Skills (375), Agents (67), Hooks (7), always-on 24,048.
   - 첫 계획 요청(파일 변경 없음):
   ```
   /ecc:plan "현재 폴더를 읽고 파일은 수정하지 말고, 할 수 있는 첫 작업 하나와 검증 방법만 알려줘"
   ```
   - 플러그인으로 깔았다면 `install.sh --profile full` / `npx ecc-install --profile full` 추가 실행 금지(명령·훅 중복).
5. **STEP 5 Karpathy Skills (4분)**: 코딩 전 생각 / 단순하게 / 필요한 줄만 변경 / 검증 가능한 목표로 끝내기. 옛 `forrestchang/` 주소는 이전됨 → 현재 이름 사용.
   ```
   claude plugin marketplace add multica-ai/andrej-karpathy-skills --scope user
   claude plugin install andrej-karpathy-skills@karpathy-skills --scope user
   claude plugin list --json
   claude plugin details andrej-karpathy-skills@karpathy-skills
   ```
   - 기대값: 1.0.0, Skills (1), 66 토큰(네 원칙이 스킬 하나에 들어 있음).
   - 확인 프롬프트 뼈대: "파일 이름만 보고 앱 구조를 전부 바꿔라"는 과한 요청 + 불확실한 가정은 먼저 밝히고 범위 밖 파일 금지, 수정 말고 최소 변경안·성공 기준만. → 모르는 부분을 밝히고 작은 변경안을 내면 성공.
6. **STEP 6 awesome-claude-code는 설치 말고 검색 (3분)**: `Start Here`, `From Anthropic`, `Security`, `Skills`, `Memory & Context Persistence` 섹션부터. 관심 항목은 해당 공식 저장소·설치 문서를 다시 확인.
   - 프롬프트 뼈대: 이 목록(https://github.com/hesreallyhim/awesome-claude-code) 기준으로 `<하고 싶은 작업>`에 맞는 자료 최대 3개, 각각 공식 저장소·최근 업데이트·설치 방식·필요 권한 확인, Star만 보고 고르지 말고 설치 금지.
7. **STEP 7 wshobson/agents에서 하나만 (5분)**: 공개 목록 94개 플러그인, 마켓플레이스 등록해도 전부 설치되지 않음.
   | 필요한 일 | 플러그인 ID |
   |---|---|
   | 단위·통합 테스트 | unit-testing |
   | 테스트 우선 개발 | tdd-workflows |
   | 백엔드 API | backend-development |
   | 보안 취약점 점검 | security-scanning |
   | Python 작업 | python-development |
   | JS·TS 작업 | javascript-typescript |
   ```
   claude plugin marketplace add wshobson/agents --scope user
   claude plugin install unit-testing@claude-code-workflows --scope user
   claude plugin list --json
   claude plugin details unit-testing@claude-code-workflows
   ```
   - 기대값: unit-testing 1.2.1, Agents (2), always-on 111. 다른 기능은 첫 줄 ID만 교체:
   ```
   PLUGIN_ID="security-scanning"
   claude plugin install "${PLUGIN_ID}@claude-code-workflows" --scope user
   claude plugin details "${PLUGIN_ID}@claude-code-workflows"
   ```
   - 목적을 설명할 수 없는 플러그인은 더 설치하지 말 것.
8. **STEP 8 검증·되돌리기 (4분)**
   ```
   claude plugin list --json
   claude plugin marketplace list
   /reload-plugins
   claude plugin uninstall superpowers@superpowers-marketplace --scope user
   claude plugin update superpowers@superpowers-marketplace
   claude plugin marketplace update superpowers-marketplace
   ```
   - `/reload-plugins`는 Claude Code 입력창(열린 세션)에서. 확인할 ID: `superpowers@superpowers-marketplace` / `ecc@ecc` / `andrej-karpathy-skills@karpathy-skills` / `unit-testing@claude-code-workflows`. 제거·업데이트는 정확한 ID로 교체. 업데이트 후 `claude plugin details`로 재확인.

**통합 점검 프롬프트 뼈대(Claude Code에 위임)**: 역할=확장 도구 설치·충돌 점검 담당. 슬롯 `<프로젝트 상황 한 줄>`, `<운영체제와 셸>`, `<프로젝트 폴더>`, `<주로 하고 싶은 작업>`. 작업: ① `claude --version`, `claude plugin list --json`, `claude plugin marketplace list` ② 미설치 시 설치(처음엔 Karpathy 또는 Superpowers 중 하나, 플러그인 ID는 README에서 확인 후 마켓플레이스 먼저 등록; Superpowers/ECC는 하나만, awesome은 목록으로만, wshobson은 하나만) ③ `list --json`과 `details`로 활성 상태·구성요소·Always-on 확인 ④ 초보자용 설명. 제약: 비밀키·자격증명 읽기/출력 금지, 존재하지 않는 마켓플레이스명 날조 금지, 기존 설정 덮어쓰기·설치 방식 중복 금지, 파일 변경·발행·커밋·푸시는 승인 전 금지. 출력: 실행 명령·버전·기존/신규 플러그인·변경 설정·검증 결과·남은 오류. 하나라도 실패하면 완료 보고 금지.

## 핵심 팁 · 주의사항
- ❌ `claude plugin install superpowers@claude-plugins-official` → `not found in marketplace "claude-plugins-official"`. ✅ 공식 마켓플레이스에는 Superpowers가 없으니 `obra/superpowers-marketplace`를 먼저 등록.
- ❌ 다섯 개 전부 설치. Superpowers와 ECC는 흐름이 겹치므로 둘 중 하나만(동시 켜면 24,632 토큰 고정 소모).
- ❌ ECC 플러그인 설치 후 `--profile full` 수동 설치 추가.
- Star ≠ 안전. 설치 전 소유자·최근 커밋·구성요소·훅·외부 연결 확인, 비밀키·파일·셸 권한을 요구하면 더 꼼꼼히.
- 이 명령들은 로컬 Claude Code 전용(ChatGPT에 붙여넣어도 플러그인이 로드되지 않음).
- 설치 후 답이 오히려 복잡해지면 규칙 겹침 의심 → `list --json`으로 확인, 하나 제거 후 새 세션에서 재시험, `details`의 always-on 토큰으로 비교.

## 문제 해결
- 현재 대화에서 안 보임: `/reload-plugins` → 안 되면 완전 종료 후 새 세션. `list --json`에 ID가 없으면 설치 미완.
- `Plugin not found`: 마켓플레이스 미등록 가능. README에서 주소·정확한 ID 재확인 후 `claude plugin marketplace list`, `claude plugin marketplace update superpowers-marketplace` 실행, 설치 재시도.

## 바로 쓰는 체크리스트
- [ ] `claude --version`
- [ ] 목적에 맞는 도구 하나만 선택 (기본 Superpowers)
- [ ] 마켓플레이스 등록 → 설치 → `list --json` → `details`
- [ ] Always-on 토큰 확인(superpowers 584 / ecc 24,048 / karpathy 66 / unit-testing 111)
- [ ] awesome-claude-code는 설치 말고 목록으로, wshobson은 플러그인 1개만
- [ ] 문제 시 `uninstall` 후 새 세션에서 재확인
