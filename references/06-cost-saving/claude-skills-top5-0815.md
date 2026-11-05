# 클로드 코드를 쓰기 전에 깔아야 하는 플러그인 5개
- 원문: https://lazyowen.com/guides/claude-skills-top5-0815
- 도구·주제: Claude Code · 비용 절약 / 스킬·MCP (2026-08-26 갱신, STEP 6개 · 약 36분)
- 한 줄 요약: 한도 소진·맥락 망각을 막는 무료 도구 5개(OmniRoute, Headroom, Claude-mem, Claude Code Setup, Task Observer)를 하나씩 설치하고 진짜 붙었는지 확인한다.

## 언제 쓰나
- Claude Code 한도가 금방 차서 작업이 통째로 멈추거나, 긴 세션에서 앞 맥락을 잊거나, 매번 프로젝트 구조를 다시 설명해야 할 때
- 모델이 약해서가 아니라 "한도가 끝났을 때 넘어갈 곳"과 "지난 작업을 적어 둘 곳"이 없어서 생기는 문제를 메꾸고 싶을 때
- 전부 필요하진 않음: 한도 문제는 STEP 2·3, 반복 설명 문제는 STEP 4부터

## 준비물 / 필요 도구
- Node.js v22.22.2 이상(`node --version`) — https://nodejs.org/ / Python 3.10 이상(`python3 --version`) — https://www.python.org/downloads/ (다섯 개 중 세 개가 이 위에서 동작, 버전이 낮으면 설치 명령이 실패)
- OmniRoute(MIT, 로컬 모델 라우팅 게이트웨이): https://omniroute.online/ · https://github.com/diegosouzapw/OmniRoute
- Headroom(입력 압축 프록시): https://github.com/headroomlabs-ai/headroom · 문서 https://headroom-docs.vercel.app/docs
- Claude-mem(세션 기억, Node 20+): https://claude-mem.ai/ · https://github.com/thedotmack/claude-mem
- Claude Code Setup(앤트로픽 공식 플러그인): https://claude.com/plugins/claude-code-setup · https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup
- Task Observer(CC BY 4.0): https://www.rebelytics.com/task-observer/ · https://github.com/rebelytics/one-skill-to-rule-them-all
- 용어: 게이트웨이=여러 AI 서비스로 가는 길을 하나로 모으는 중간 서버(내 컴퓨터 안) / 토큰=AI가 글을 세는 단위 / 훅=특정 순간에 자동 실행되는 동작 / 스킬=AI에게 미리 알려 두는 작업 설명서
- 비용: 모두 무료로 소개됨(OmniRoute 무료 제공자 연결에 API 키가 필요한지는 명시 없음). 기존 Claude 구독은 그대로 사용

## 단계별 방법
**Quick Start** — 터미널에서 설치하는 3개를 한 줄씩:
```bash
npm install -g omniroute
pip install "headroom-ai[all]"
npx --yes claude-mem@latest install
```
Claude Code 안에서 설치하는 1개(5번째 Task Observer는 파일 배치 방식이라 STEP 6):
```
/plugin install claude-code-setup@claude-plugins-official
```
설치 확인:
```bash
omniroute --version && headroom --version
```

**설치·검증 위임 프롬프트 뼈대 (Claude Code)**
- 역할: 확장 도구 5개 설치·연결 검증 담당. 맥락: 아직 미설치일 수 있고 지금은 한도가 끝나면 멈추고 세션이 바뀌면 기억을 잃는 상태
- 채울 곳: [OS와 셸], [기술 스택], [목표 한 줄 — 예: 한도가 끝나도 작업을 이어가고 지난 맥락을 유지]
- 작업 4단계: ① `node --version`≥22.22.2, `python3 --version`≥3.10 확인 후 `omniroute --version`, `headroom --version`, `npx --yes claude-mem@latest --version`으로 설치 여부 확인(있으면 버전만 보고) ② 없는 것만 `npm install -g omniroute`, `pip install "headroom-ai[all]"`, `npx --yes claude-mem@latest install` 실행. `/plugin install claude-code-setup@claude-plugins-official`과 Task Observer 폴더 배치는 사용자가 직접 해야 하므로 안내만 ③ 검증: `omniroute` 실행 후 `curl http://localhost:20128/v1/models`가 목록 반환, `headroom doctor` 정상 종료, `ls ~/.claude/plugins`에 claude-mem ④ 5개 각각의 역할과 사용법을 5줄 이내로 설명
- 제약: 기존 설정 파일 덮어쓰기·삭제 금지, 이미 설치된 항목 중복 설치 금지, 키·토큰 출력 금지, 한 번에 하나씩 설치·검증
- 출력/검증: 실행 명령 목록, Node·Python 버전, 새 폴더/파일, 남은 오류. 하나라도 실패하면 완료 보고 금지

**STEP 1. 준비물 확인 (3분)**
```bash
node --version      # v22.22.2 이상
python3 --version   # 3.10 이상
```
낮거나 `command not found`면 nodejs.org / python.org에서 최신 설치 후 터미널 재시작. (원문 그림: 설치 방식 세 가지 — 터미널 npm / 터미널 pip·npx / Claude Code 안 `/plugin` + 파일 배치)

**STEP 2. OmniRoute: 한도가 끝나도 멈추지 않기 (10분)**
- 공식 문서 기준 339개 제공사·1,200개+ 모델, 그중 90개+ 무료 등급, 무료 약 매달 15억 토큰(첫 달 가입 크레딧 포함 약 21억). 자체 주장이며 검증되지 않음
```bash
npm install -g omniroute
omniroute            # 로컬 서버 실행. 이 터미널 창은 켜 둔 채 유지
```
- 브라우저에서 `http://localhost:20128` 대시보드 → Providers 메뉴에서 무료 제공사 하나 연결(가입 없이 쓸 수 있는 항목 있음)
- 새 터미널에서:
```bash
omniroute setup-claude    # 모델별 설정 파일 생성
omniroute launch          # 설정을 붙인 채로 Claude Code 실행
curl http://localhost:20128/v1/models    # 모델 목록이 나오면 성공. 비어 있으면 서버 터미널이 닫힌 것
```

**STEP 3. Headroom: 보내는 양 줄이기 (8분)**
- 파일 내용·명령 결과·로그 같은 덩치 큰 입력을 모델에 넘기기 전에 압축. 공식 문서 기준 코딩 15~20%, JSON 60~95% 토큰 절감(자체 주장). 원본은 컴퓨터에 남아 모델이 필요하면 다시 꺼냄
```bash
pip install "headroom-ai[all]"    # 마지막 줄에 Successfully installed headroom-ai
headroom wrap claude              # 압축 서버를 띄우고 그 서버를 거치는 Claude Code 실행
headroom doctor                   # 점검 통과하면 성공
headroom dashboard                # 얼마나 줄었는지 확인
```
- ❌ `npm install headroom-ai` → 개발자용 라이브러리만 깔리고 `headroom` 명령이 없음. 반드시 pip
- OmniRoute와 Headroom은 둘 다 Claude Code가 바라보는 주소를 바꾸므로 한 번에 하나씩 켜서 확인한 뒤 합치기
- 되돌리기: `headroom unwrap claude`

**STEP 4. Claude-mem: 지난 세션 기억 (5분)** — 세션 동안의 일을 자동 기록·요약해 다음 세션 시작 때 다시 넣어 줌(Node 20+)
```bash
npx --yes claude-mem@latest install
```
- 또는 Claude Code 안에서:
```
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
```
- ❌ `npm install -g claude-mem` → 라이브러리만 깔리고 기억 기능이 연결 안 됨
- 설치 후 Claude Code를 완전히 껐다 다시 켜기. 새 세션에서 지난 작업 요약이 자동으로 올라옴

**STEP 5. Claude Code Setup: 프로젝트 맞춤 추천 (3분)** — 앤트로픽 공식, 프로젝트 폴더를 읽기만 하고 고치지 않음. 공식 마켓플레이스는 기본 등록이라 별도 추가 불필요
```
/plugin install claude-code-setup@claude-plugins-official
```
- 작업 중인 프로젝트 폴더에서: `이 프로젝트에 맞는 자동화를 추천해 줘` → 프로젝트 종류를 파악해 MCP 서버, 스킬, 훅, 서브에이전트, 슬래시 명령어 5갈래로 추천

**STEP 6. Task Observer: 스스로 자라는 메타 스킬 (7분)** — 작업 중 내가 고쳐 준 부분·선호를 모아 어떤 스킬을 어떻게 바꿀지 제안(자기 자신도 관찰 대상)
```bash
git clone https://github.com/rebelytics/one-skill-to-rule-them-all.git   # git이 없으면 GitHub에서 Code → Download ZIP
mkdir -p .claude/skills/task-observer
cp one-skill-to-rule-them-all/SKILL.md .claude/skills/task-observer/
cp -r one-skill-to-rule-them-all/references .claude/skills/task-observer/
ls .claude/skills/task-observer      # SKILL.md 와 references 가 보이면 성공 (복사는 조용히 끝나는 게 정상)
```
- SKILL.md만 넣어도 돌아가지만 references까지 넣어야 제 성능
- 사용: 작업을 마칠 때 `기록된 관찰 있어?`라고 물으면 쌓인 개선안을 정리

**다섯 개 한 번에 확인**
```bash
omniroute --version
headroom doctor
ls ~/.claude/plugins
ls .claude/skills/task-observer
```
각각 버전 번호 / 점검 통과 / 플러그인 목록 / 스킬 파일 목록이 나오면 완료.

## 핵심 팁 · 주의사항
- 위 절감 수치(OmniRoute 339 제공자·1,200+ 모델·월 15억 토큰, Headroom 15~20%·60~95%)는 각 도구 자체 주장
- 다섯 개를 한꺼번에 깔지 말고 하나 설치→확인→다음. 어디서 막혔는지 알 수 없게 됨
- 기존 구독은 그대로. OmniRoute는 한도가 끝났을 때 다른 곳으로 넘기는 우회로 — 되돌리려면 `omniroute launch` 대신 그냥 `claude`로 실행
- OmniRoute 서버 터미널을 닫으면 요청이 갑자기 실패 → 서버 창은 켜 두고 새 터미널에서 작업
- `npm install -g`에서 권한 오류(회사 노트북 등): 관리자 권한 필요. 못 받으면 Claude Code 안에서 설치하는 STEP 5부터 먼저
- npm 의존성 경고는 대부분 무시 가능. 마지막에 설치 완료가 뜨고 버전 확인이 통과하면 정상

## 문제 해결
| 실수 | 증상 | 해결 |
|---|---|---|
| `npm install headroom-ai`로 설치 | `headroom` 명령 없음 | `pip install "headroom-ai[all]"` |
| `npm install -g claude-mem`으로 설치 | 새 세션에 기억이 안 올라옴 | `npx --yes claude-mem@latest install` |
| 다섯 개를 한 번에 설치 | 막힌 곳을 모름 | 하나씩 설치·확인 |
| OmniRoute 터미널 창을 닫음 | 요청이 갑자기 실패 | 서버 창 유지 |
| Task Observer에 SKILL.md만 복사 | 기능 일부만 동작 | `references`까지 복사 |

## 바로 쓰는 체크리스트
- [ ] `node --version` ≥ 22.22.2, `python3 --version` ≥ 3.10
- [ ] `omniroute --version` 출력, `curl http://localhost:20128/v1/models`가 목록 반환
- [ ] `headroom doctor` 실패 없음
- [ ] `ls ~/.claude/plugins`에 claude-mem, claude-code-setup 확인
- [ ] `ls .claude/skills/task-observer`에 `SKILL.md`, `references`
- [ ] 한 번에 하나씩 설치·검증했는가
- [ ] (선택) 설치·검증을 Claude Code에 위임하는 프롬프트 사용
