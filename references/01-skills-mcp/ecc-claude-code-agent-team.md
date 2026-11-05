# ECC 하나 설치해서 클로드에 엔지니어 전부를 맡기는 법
- 도구·주제: Claude Code 플러그인 ECC · 에이전트/스킬/명령 번들, 설계-TDD-테스트-보안 점검 워크플로
- 한 줄 요약: ECC 플러그인 하나(명령 두 줄)를 설치해 planner·security-reviewer 등 에이전트와 `/ecc:plan`, `/ecc:test-coverage`, `/ecc:security-scan` 명령으로 기능 하나를 설계부터 보안 점검까지 한 줄씩 맡긴다. (2026-09-30 갱신, 약 25분, 검증 기준: ECC v2.2.2 / Claude Code 2.1.283)

## 언제 쓰나
- Claude Code에 기능을 부탁하면 계획도 테스트도 없이 코드부터 쏟아질 때
- 설계, 테스트 커버리지, 보안 점검을 Claude Code 안에서 표준화된 흐름으로 돌리고 싶을 때

## 준비물 / 필요 도구
- ECC (MIT, 무료, 개발자 1명 제작 오픈소스, GitHub 스타 268,665개 / 2026-09-28 확인)
  - GitHub: https://github.com/affaan-m/ECC
  - 사이트: https://ecc.tools/
  - npm 대안 패키지: https://www.npmjs.com/package/ecc-universal
- Claude Code 2.1 이상: https://code.claude.com/docs/en/setup
- Git: https://git-scm.com/downloads
- 플러그인 공식 문서: https://docs.claude.com/en/docs/claude-code/plugins
- 환경: 맥·리눅스·윈도(PowerShell). npm 경로로만 설치할 때 Node.js 18 이상 추가 필요
- 비용: 플러그인 무료, 사용량은 현재 Claude 요금제에서 차감
- 용어: 에이전트 = 한 가지 일만 맡는 AI 역할(설계는 planner, 보안은 security-reviewer), 스킬 = 특정 작업 요령 지침서, 마켓플레이스 = 플러그인 목록이 든 저장소 주소(먼저 등록해야 설치 가능). ECC는 새 AI 모델이 아니라 Claude Code에 더하는 꾸러미.

## 단계별 방법
### 프롬프트 뼈대 A. 설치·첫 설계 준비 위임용 (선택)
- 목적: ECC 설치·검증을 Claude Code에 맡기기(터미널에서 `claude` 실행 후 첫 메시지)
- 역할: ECC 플러그인 설치·연결 확인 담당, 사용자는 개발 초보
- 슬롯: [내 목표 = ECC로 처음 만들 기능 한 줄] (OS·셸·프로젝트 종류는 직접 확인)
- 작업: `claude --version`·`git --version` 확인 → `claude plugin list`로 `ecc@ecc` 유무 확인, 없을 때만 marketplace add / install 실행 → `claude plugin list`로 검증 → ECC 설명과 재실행 후 `/ecc:plan` 뒤에 목표를 넣는 법 안내
- 제약: 설정을 바꾸는 명령·sudo·전역 설치는 실행 전 질문, 비밀키 출력·덮어쓰기 금지, 목표 코드는 아직 작성 금지
- 출력: 실행 명령, 버전, 바뀐 파일, 남은 오류
- 검증: `ecc@ecc`와 `Status: ✔ enabled`가 보여야 완료

### Quick Start
```bash
claude plugin marketplace add affaan-m/ECC
claude plugin install ecc@ecc
```
성공 시 `✔ Successfully added marketplace: ecc (declared in user settings)`, `✔ Successfully installed plugin: ecc@ecc (scope: user)`. 이 두 줄을 실행했다면 STEP 2의 설치는 건너뛰고 확인만 한다. Claude Code 입력창에서는 `/plugin marketplace add affaan-m/ECC` 와 `/plugin install ecc@ecc`를 차례로 넣어도 같지만 한 가지 방법만 쓴다.

### STEP 1. 준비물 확인 (2분)
1. 버전 확인
```bash
claude --version
git --version
```
`2.1.283 (Claude Code)`처럼 2.1 이상, `git version 2.50.1` 같은 줄이 나오면 통과(숫자는 달라도 됨). `command not found`면 위 공식 링크로 설치 후 터미널을 새로 연다.
2. 2.1 미만이면 업데이트 후 다시 확인
```bash
claude update
```

### STEP 2. 플러그인 설치하고 확인 (3분)
1. 설치 전 알아둘 것: ECC에는 Claude Code가 일할 때 내 컴퓨터에서 자동 실행되는 스크립트(훅)가 있고 내 계정 권한으로 돈다. 공식 저장소 `affaan-m/ECC`에서만 받고, 처음엔 중요한 파일 없는 연습 폴더에서 쓴다.
2. 마켓플레이스 등록
```bash
claude plugin marketplace add affaan-m/ECC
```
3. 플러그인 설치
```bash
claude plugin install ecc@ecc
```
"2 userConfig options not yet set" 안내는 훅 켤지/강도를 아직 안 골랐다는 뜻이며 기본값(훅 켜짐, standard)이 있어 넘어가도 된다.
4. 확인
```bash
claude plugin list
```
`ecc@ecc`, `Version: 2.2.2`(이상), `Status: ✔ enabled`가 보이면 성공.
5. 되돌리기
```bash
claude plugin uninstall ecc@ecc
```
`✔ Successfully uninstalled plugin: ecc (scope: user)`.

### STEP 3. 설계 받고 코드 짜게 하기 (10분)
1. Claude Code를 완전히 껐다가 내 프로젝트 폴더에서 다시 켠다(플러그인은 켤 때 로드). 앱이 없으면 연습 폴더를 만들고 그 안에서 실행(처음 여는 폴더 확인 창은 허용). 이때 목표는 "할 일을 적고 지우는 간단한 웹페이지 만들기"처럼 새로 만들 것으로 적는다.
```bash
mkdir ecc-practice
cd ecc-practice
claude
```
2. 설계 요청
```
/ecc:plan "설정 화면에 다크 모드 켜고 끄는 버튼 추가"
```
응답 순서: 요구사항을 쉬운 말로 재정리 → 단계별 계획·위험 요소·난이도 → 코드를 건드리기 전에 진행해도 될지 묻고 멈춤.
3. 계획이 맞으면 구현 요청
```
계획대로 진행해 줘. tdd-workflow 스킬로 실패하는 테스트를 먼저 쓰고 구현해 줘.
```
`tdd-workflow` = 실패하는 테스트를 먼저 쓰는 ECC 스킬. 순서: 테스트 실패 확인 → 통과할 만큼만 수정 → 정리. 성공하면 테스트 파일이 먼저 생기고 그다음 기능 코드가 바뀐다.

### STEP 4. 테스트와 보안 점검 (10분)
1. 커버리지(테스트가 실제 실행해 본 코드 비율, 80%면 열 줄 중 여덟 줄) 점검
```
/ecc:test-coverage
```
테스트 도구를 찾아 파일별 커버리지를 재고, 80% 미만 파일을 낮은 순으로 보여 주며 빠진 테스트를 만든다. 테스트 도구가 없는 연습 폴더에선 못 잰다는 답이 올 수 있으니 이렇게 보낸다.
```
이 프로젝트에 맞는 테스트 도구를 추천하고, 설치하기 전에 먼저 물어봐 줘
```
2. 보안 점검
```
security-review 스킬로 방금 만든 코드 보안 점검 진행해 줘. 고치기 전에 무엇을 바꿀지 먼저 보여 줘.
```
코드에 박힌 비밀키, 그대로 믿는 사용자 입력 등 체크리스트 항목별 결과와 고칠 곳 목록이 나온다.
3. 에이전트 설정·훅·권한까지 넓게 보려면 `/ecc:security-scan`을 따로 보낸다.

## 핵심 팁 · 주의사항
- ❌ "앱 좋게 만들어 줘" → ✅ `/ecc:plan "설정 화면에 다크 모드 켜고 끄는 버튼 추가"` (넓게 부탁하면 계획이 흐려지고 여러 파일이 한꺼번에 바뀜)
- ❌ "테스트 다 됐어?" → ✅ `/ecc:test-coverage`
- 훅이 내 계정 권한으로 자동 실행: 공식 저장소만, 연습 폴더에서 먼저
- 사람 검토는 그대로 필요(무엇을 합칠지는 읽고 승인하는 사람이 결정)
- 보안 점검은 보장이 아님: 체크리스트·스캐너로 흔한 실수를 찾는 도구이며 모든 취약점을 막아 준다고 약속 못 함
- 사용량이 빨리 닳음: 에이전트를 여러 번 부르면 모델 호출이 늘어나므로 작은 작업 하나로 시작
- 도구마다 기능이 다름: Claude Code가 가장 완전, Cursor·Codex·OpenCode는 핵심 에이전트·스킬 위주(설치 경로가 다르니 GitHub의 Install ECC 절 참고)
- 규모 수치는 계속 변함: 영상은 v2.0.0 기준 에이전트 63·스킬 249·명령 84, v2.2.2는 에이전트 68·스킬 292·명령 94

## 문제 해결
- `plugin not found`: 이름을 정확히 `ecc@ecc`로 입력(옛 글의 긴 이름은 더 이상 안 됨)
- 마켓플레이스 등록 실패: `claude update`로 최신화 후 재시도, 그래도 안 되면 아래 npm 경로
- 설치했는데 `/ecc:plan`이 안 보임: Claude Code를 완전히 끄고 다시 켠다
- Cursor/Codex 사용: 설치 경로가 다르니 GitHub의 Install ECC 절 확인
- npm 대안(두 줄 설치가 끝내 안 될 때만; 이미 설치했다면 사용 금지: 스킬·명령이 두 번 들어감; 시스템 전체에 `ecc` 명령이 추가되는 전역 설치; Node.js 18+ 필요)
```bash
npm i -g ecc-universal
ecc setup
```
  - 설치 범위: 모든 프로젝트는 `user`, 같은 저장소 동료와 공유는 `project`, 지금 폴더만은 `local`
  - 훅 강도: 처음엔 기본 `standard`, `off`는 끔, `minimal`은 가볍게, `strict`는 더 깐깐하게

## 바로 쓰는 체크리스트
- [ ] `claude --version`이 2.1 이상, `git --version` 확인(필요시 `claude update`)
- [ ] 마켓플레이스 등록 + `ecc@ecc` 설치, `claude plugin list`에서 enabled 확인
- [ ] Claude Code 완전 재시작(연습 폴더에서)
- [ ] `/ecc:plan "..."` → 계획 확인 → tdd-workflow로 구현
- [ ] `/ecc:test-coverage` → security-review → 필요시 `/ecc:security-scan`
- [ ] 변경 사항은 직접 리뷰 후 머지
