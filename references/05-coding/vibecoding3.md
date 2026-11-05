# 클로드 코드로 바이브 코딩한다면 깔아야 하는 3개
- 도구·주제: Claude Code + ECC / Context7 / Strix · 바이브 코딩 품질·최신 문서·보안
- 한 줄 요약: 클로드가 중간에 길을 잃고, 옛 문법으로 코드를 쓰고, 보안 구멍을 모르는 문제를 무료 도구 세 개(ECC=검증된 작업 방식, Context7=최신 문서, Strix=AI 모의 해킹)로 메우고, 계획 → 구현 → 테스트 → 보안 점검 흐름을 만든다. (2026-08-28 공개, 읽는 데 12분, 따라 하면 약 36분, STEP 6개)

## 언제 쓰나
- 클로드 코드로 서비스를 만들 때 계획·테스트·자기 검토, 최신 라이브러리 문법, 배포 전 취약점 점검을 갖추고 싶을 때
- 혼자 만든 서비스의 개인정보 유출 같은 구멍을 배포 전에 찾고 싶을 때

## 준비물 / 필요 도구
- Node.js v18 이상(LTS): https://nodejs.org/ — 확인 `node --version`
- Claude Code: https://claude.com/product/claude-code — 확인 `claude --version`
- 터미널(macOS는 터미널 앱, Windows는 PowerShell)
- Docker Desktop(STEP 4 Strix에서만 필요, 없어도 STEP 2·3은 진행 가능) — 확인 `docker info`
- ECC(Claude Code용 스킬·작업 규칙 무료 플러그인, GitHub 스타 24만+): https://ecc.tools · https://github.com/affaan-m/ECC
- Context7(최신 라이브러리 문서 연결): https://context7.com · https://github.com/upstash/context7
- Strix(AI 모의 해킹): https://strix.ai · https://github.com/usestrix/strix · 문서 https://docs.strix.ai
- (선택, STEP 6) Playwright CLI https://github.com/microsoft/playwright-cli · Supabase 플러그인 https://supabase.com/docs/guides/ai-tools/plugins · Skill UI https://github.com/amaancoderx/npxskillui
- 비용: 세 도구 모두 오픈소스 무료. 단 Strix는 AI 모델을 직접 호출하므로 그 모델 사용료가 별도(OpenAI·Anthropic·Google 키 가능)
- 용어: 스킬 = AI가 필요할 때 꺼내 읽는 설명서 묶음, 라이브러리 = 남이 만든 코드 묶음, 모의 해킹 = 진짜 해커처럼 공격해 뚫리는 곳을 미리 찾는 작업, Docker = 격리된 방에서 프로그램을 돌리는 도구(Strix가 내 컴퓨터를 건드리지 않고 공격 테스트하려고 사용)

## 단계별 방법
### 프롬프트 뼈대 A. 세 도구 설치·검증 위임 (Claude Code 첫 메시지, 선택)
- 목적: ECC·Context7·Strix 설치 여부 확인 → 없는 것만 설치 → 연결 검증
- 역할: 세 도구 설치·연결 검증 담당
- 슬롯: [운영체제와 셸], [기술 스택(예: Next.js+타입스크립트)], [목표 한 줄(예: 혼자 만든 웹서비스를 안전하게 배포)]
- 작업 4단계: ① `node --version`(18+), `claude --version`, `docker info`, `ls ~/.claude/plugins`(ecc 유무), `ctx7 --version`, `strix --version` 확인(이미 있으면 재설치 말고 상태만 보고) ② 없는 것만 설치 — ECC는 Claude Code 대화창에서 `/plugin marketplace add https://github.com/affaan-m/ECC`, `/plugin install ecc@ecc`를 실행해야 하므로 터미널 자동 설치 대신 사용자에게 직접 입력하라고 안내, Context7은 `npx ctx7 setup --claude`, Strix는 `curl -sSL https://strix.ai/install | bash` ③ `ctx7 library next.js routing` 목록, `strix --version` 번호, `/plugin`에서 ecc 활성 확인 ④ 세 도구의 역할과 사용 순서를 5줄 이내로 설명
- 제약: 기존 파일·설정 덮어쓰기/삭제 금지, 중복 설치 금지, `.env` 등 비밀 파일 읽기·출력 금지, API 키 값 출력 금지, 한 번에 하나씩 설치·확인
- 출력: 실행 명령 목록, Node 버전·Docker 상태, 새로 생긴 폴더·파일, 남은 오류
- 검증: 위 3가지(ctx7 목록, strix 버전, ecc 목록)가 모두 되어야 완료, 실패 시 완료 보고 금지

### Quick Start
1. Claude Code를 켜고 대화창(터미널 아님)에 한 줄씩 입력. 성공하면 설치된 스킬·명령어 목록과 재시작 안내
```
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```
2. 터미널: Context7 연결(브라우저 로그인 승인 시 키 자동 생성, 설치 완료 메시지)
```bash
npx ctx7 setup --claude
```
3. 터미널: Strix 설치(진행 표시 후 프롬프트가 돌아오면 끝)
```bash
curl -sSL https://strix.ai/install | bash
```
4. 한 번에 확인(둘 다 버전 번호가 나오면 성공, ECC는 Claude Code에서 `/plugin` 목록에 ecc가 보이는지로 확인)
```bash
ctx7 --version && strix --version
```

### STEP 1. 준비물 확인 (3분)
```bash
node --version
claude --version
docker info
```
- Node: v18 이상. 낮거나 `command not found`면 nodejs.org에서 LTS 설치 후 터미널 새로 열기
- Claude Code: 버전 번호가 나와야 하며 없으면 claude.com/product/claude-code에서 먼저 설치
- Docker: 서버 정보가 나오면 켜진 상태, `Cannot connect to the Docker daemon`이면 Docker Desktop 실행 후 재시도

### STEP 2. ECC 설치 (5분)
클로드가 바로 코딩부터 하는 대신 계획 → 테스트 검증 → 자기 검토를 하게 만드는 작업 방식을 통째로 넣는다. 반드시 터미널이 아닌 Claude Code 대화창에 입력.
1. 마켓플레이스 등록(성공하면 `Marketplace added` 같은 메시지와 설치 가능한 플러그인 목록)
```
/plugin marketplace add https://github.com/affaan-m/ECC
```
2. 플러그인 설치(스킬·에이전트·명령어 개수 표시 후 재시작 안내 → 창을 닫았다 다시 열기)
```
/plugin install ecc@ecc
```
3. 확인: 목록에 ecc가 보이고 활성 표시면 성공
```
/plugin
```
주의: 공식 경로(위 GitHub 주소 + `ecc@ecc`)에서만 설치. 비슷한 이름의 복사본은 관리되지 않는다.

### STEP 3. Context7 연결 (3분)
클로드는 학습 시점까지의 지식만 있어 이후 바뀐 라이브러리 문법을 모르고 없는 기능을 지어내거나 옛 버전 문법을 쓴다. Context7이 진짜 최신 문서를 그때그때 대화창에 꽂아 준다.
1. 터미널에서 설치(브라우저 로그인 → 승인 → 무료 키 자동 생성)
```bash
npx ctx7 setup --claude
```
2. 연결 확인: `/vercel/next.js` 같은 라이브러리 아이디 목록이 나오면 성공
```bash
ctx7 library next.js routing
```
3. 사용: 문장 끝에 `use context7`
```
쿠키에 든 로그인 토큰을 검사해서 로그인 안 한 사람을 /login으로 보내는
Next.js 미들웨어를 만들어 줘. use context7
```
4. 버전 지정도 가능
```
Next.js 14 미들웨어는 어떻게 설정해? use context7
```
5. 매번 붙이기 귀찮으면 프로젝트 폴더의 `CLAUDE.md`에 규칙 한 줄
```
라이브러리나 API 문서가 필요한 작업은 내가 말하지 않아도 항상 Context7을 먼저 사용해.
```

### STEP 4. Strix로 보안 점검 (10분)
AI가 진짜 해커처럼 서비스를 실행해 보고 뚫리는 지점과 실제로 뚫리는 증거까지 만들어 준다. 배포 전에 돌려 개인정보 탈취 같은 사고를 막는 용도. Docker가 필요하다.
1. 설치 및 확인
```bash
curl -sSL https://strix.ai/install | bash
strix --version
```
2. AI 모델 키 등록(Strix는 스스로 판단해야 해서 모델이 필요, 출력이 없으면 정상, OpenAI 대신 Anthropic·Google 키도 가능). 터미널을 새로 열면 사라지니 매번 입력하거나 셸 설정 파일에 넣는다. 키는 화면 공유·GitHub에 노출 금지.
```bash
export STRIX_LLM="openai/gpt-5.4"
export LLM_API_KEY="여기에-내-키를-붙여넣기"
```
3. 프로젝트 점검(경로를 내 폴더로 교체). 첫 실행은 격리용 Docker 이미지를 자동으로 받는다. 끝나면 취약점과 수정법이 정리되고 결과는 `strix_runs` 폴더에 저장.
```bash
strix --target ./내-프로젝트-폴더
```
4. Claude Code가 직접 Strix를 돌리게 하려면 스킬로도 설치(보안 점검·취약점 수정·자동 재검사까지 진행)
```bash
npx skills add usestrix/strix
```

### STEP 5. 세 개를 한 흐름으로 쓰기 (5분)
순서: 만들기 전 ECC가 계획 → 만드는 동안 Context7이 최신 문서 → 다 만든 뒤 Strix가 공격. 따로 쓰면 효과가 반으로 준다.

프롬프트 뼈대 B. 계획 → 최신 문서 → 테스트 → 보안 점검 한 번에
- 슬롯: [만들려는 것] (예: 이메일 로그인 할 일 목록 앱)
- 순서 4단계: ① 먼저 계획을 세우고 만들 파일을 알려 달라 ② 라이브러리 문법은 `use context7`으로 최신 문서를 확인하고 쓸 것 ③ 다 만들면 테스트를 돌려 실제 동작 확인 ④ 마지막에 `strix --target .`을 실행해 보안 문제를 점검하고, 나온 문제를 고친 뒤 다시 점검
- 추가 요구: 각 단계가 끝날 때마다 한 일을 한 줄로 보고. 중간에 막히면 어디서 왜 막혔는지 알림.

### STEP 6. 여유가 되면 추가할 도구 3개 (10분, 선택)
1. Playwright CLI: 클로드가 진짜 브라우저를 열어 내가 만든 화면을 클릭하며 테스트. 첫 줄은 도구, 둘째 줄은 클로드용 사용법 설치. `playwright-cli --help`에 명령어 목록이 나오면 성공.
```bash
npm install -g @playwright/cli@latest
playwright-cli install --skills
```
2. Supabase 플러그인: DB를 쓰는 서비스에서 클로드가 데이터를 직접 조회·관리. 설치된 AI 도구를 자동으로 찾아 연결. 확인 질문을 건너뛰려면 `--yes`.
```bash
npx plugins add supabase-community/supabase-plugin
```
3. Skill UI: 웹사이트 주소를 넣으면 색·폰트·간격을 뽑아 클로드가 읽을 형태로 폴더에 정리. 그 폴더에서 Claude Code를 열면 비슷한 결의 화면을 만들어 줌.
```bash
npm install -g skillui
skillui --url https://notion.so
```

## 핵심 팁 · 주의사항
- `/plugin` 계열 명령은 Claude Code 대화창에서만 동작(터미널 입력 시 무반응)
- ECC는 공식 경로만 사용
- Strix는 Docker 필수, 키 노출 주의, 모델 사용료 별도
- 세 개를 다 깔아도 평소 속도에는 영향 없음: ECC는 필요할 때만 스킬을 읽고, Context7은 요청할 때만 문서를 가져오고, Strix는 따로 실행하는 도구
- 폴더 전체 대신 문제가 될 만한 폴더만 지정하면 Strix 점검이 더 빠름

## 문제 해결
- `/plugin` 입력해도 반응 없음: 터미널에 입력했을 가능성. `claude`로 대화창을 연 뒤 입력
- `npx ctx7 setup --claude`에서 브라우저가 안 열림(원격 서버·브라우저 없는 환경): 터미널에 뜬 주소를 다른 컴퓨터 브라우저에 붙여넣어 로그인
- `use context7`을 붙여도 문서를 안 가져옴: `ctx7 library next.js routing`으로 목록 확인, 안 나오면 `npx ctx7 setup --claude` 재실행
- Strix에서 `Cannot connect to the Docker daemon`: Docker Desktop 실행 후 `docker info` 정상 확인하고 재실행
- Strix가 오래 걸림: 첫 실행은 이미지 다운로드 때문에 느리고 두 번째부터 빠름

## 바로 쓰는 체크리스트
- [ ] Node 18+ / Claude Code / (Strix용) Docker 확인
- [ ] ECC 설치(`/plugin marketplace add ...`, `/plugin install ecc@ecc`) + 재시작 + `/plugin`에서 ecc 활성 확인
- [ ] `npx ctx7 setup --claude` + `ctx7 library next.js routing` 확인 + `use context7` 습관(또는 CLAUDE.md 규칙)
- [ ] Strix 설치 + `STRIX_LLM`/`LLM_API_KEY` 설정
- [ ] 완성 후 `strix --target` 점검 → 수정 → 재점검
- [ ] (선택) Playwright CLI / Supabase 플러그인 / Skill UI
