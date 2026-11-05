# 클로드 코드 돈 안 내고 쓰는 프리 LLM API 세팅법
- 도구·주제: Claude Code · Manifest(LLM 라우터) · awesome-free-llm-apis · 무료 모델로 Claude Code 돌리기
- 한 줄 요약: 계속 무료로 쓸 수 있는 LLM API 공급자 16곳 목록(+키 설정을 돕는 `free-llm-apis` 스킬)을 내려받고, 무료 키를 Manifest 라우터에 연결한 뒤, 테스트 폴더 하나의 `.claude/settings.json`에서만 Claude Code가 무료 모델을 쓰게 하고 되돌리는 4단계. (2026-10-08 갱신, 읽는 데 11분, 따라 하면 약 18분)

## 언제 쓰나
- 구독 결제가 망설여지거나, Claude 한도 소진 시 대안/연습용으로 비용 없이 Claude Code 흐름을 써 보고 싶을 때

## 준비물 / 필요 도구
- awesome-free-llm-apis (체험판이 아닌 계속 무료인 공급자 16곳 + 스킬 1개, CC0-1.0, GitHub 스타 9,057, Manifest 팀 mnfst 관리): https://github.com/mnfst/awesome-free-llm-apis
- Manifest (오픈소스 LLM 라우터, MIT; 요청을 어느 모델로 보낼지 정하는 중간 관리자)
  - 사이트·무료 모델 연결: https://manifest.build/free-models/
  - 가입: https://app.manifest.build/register
  - Claude Code 연결 안내: https://manifest.build/agents/claude-code/
  - 셀프 호스팅(Docker): https://manifest.build/llm-gateway/docs/self-hosted
  - 가격: https://manifest.build/pricing/
- Claude Code: https://code.claude.com/docs/en/setup · git: https://git-scm.com/downloads
- 무료 키(카드 불필요): Gemini https://aistudio.google.com/app/apikey · Groq https://console.groq.com/keys
- 환경: 맥·리눅스는 기본 터미널, 윈도는 Git Bash(PowerShell·CMD에서는 STEP 2·4 명령이 그대로 안 돌아감)
- 비용: 목록·스킬 무료. 각 공급자는 분당·하루 요청 한도 안에서 무료. Manifest 클라우드 무료 플랜은 월 10,000 요청, 직접 띄워 쓰면(셀프 호스팅) 요청 제한 없음.
- 용어: LLM API = AI 모델을 내 프로그램에서 부르는 창구, API 키 = AI 서버에 보여 주는 비밀번호, 게이트웨이 = 여러 모델 앞의 공용 입구, curl = 터미널에서 주소로 요청을 보내 보는 명령, 스킬 = 클로드에게 작업 방법을 알려 주는 설명서 폴더
- 흐름: Claude Code → Manifest로 요청 → 연결해 둔 무료 모델 중 하나로 전달

## 단계별 방법
### 프롬프트 뼈대 A. 스킬 설치·무료 응답 검증 위임 (터미널에서 `claude` 실행 후 첫 메시지, 선택)
- 목적: `free-llm-apis` 스킬 설치와 무료 모델 응답 확인
- 역할: 무료 LLM API 목록의 스킬 설치·검증 담당. 사용자는 초보
- 슬롯: [내 목표 = 무료 모델로 하고 싶은 일(예: 간단한 코드 질문)]. OS·셸·설치 프로그램은 직접 확인
- 작업: ① `claude --version`과 git 확인 ② `ls ~/.claude/skills/free-llm-apis`로 확인, 없을 때만 `git clone --depth 1 https://github.com/mnfst/awesome-free-llm-apis.git`과 `mkdir -p ~/.claude/skills && cp -R awesome-free-llm-apis/free-llm-apis ~/.claude/skills/` ③ 다시 `ls`로 설치 확인 후, 키 없이 쓸 수 있는 무료 모델 응답을 STEP 2의 curl로 확인 ④ 스킬 설명, 내 목표에 맞는 무료 공급자 1~2곳, 다음 할 일을 초보 눈높이로
- 제약: `~/.claude/settings.json` 같은 전역 설정 수정 금지, sudo·전역 설치·설정 수정 전 질문, API 키 값 출력 금지, 기존 파일 덮어쓰기 금지
- 출력: 실행 명령, Claude Code 버전, 새 폴더, 응답한 무료 모델 이름, 남은 오류
- 검증: `ls ~/.claude/skills/free-llm-apis`에 `references`와 `SKILL.md`, curl 응답 JSON에 `"choices"`와 `:free`로 끝나는 모델 이름. 실패 시 완료 보고 금지

### Quick Start. 스킬 설치
```bash
git clone --depth 1 https://github.com/mnfst/awesome-free-llm-apis.git
mkdir -p ~/.claude/skills && cp -R awesome-free-llm-apis/free-llm-apis ~/.claude/skills/
```
`Cloning into 'awesome-free-llm-apis'...`가 보이고 오류 없이 끝나면 성공. 확인(`2.1.288 (Claude Code)` 같은 버전과 그 아래 `references`, `SKILL.md`가 보여야 함. `command not found`면 Claude Code를, git이 없다고 나오면 git부터 설치):
```bash
claude --version
ls ~/.claude/skills/free-llm-apis
```

### STEP 1. 스킬에게 내 무료 공급자 고르게 하기 (3분)
Claude Code에 요청(프롬프트 뼈대 B): "free-llm-apis 스킬로, 카드 등록 없이 쓸 수 있는 무료 공급자 중 코딩 질문에 쓸 만한 곳 2개만 골라 달라. 각각의 키 발급 페이지 주소와 분당·하루 요청 한도도 알려 달라."
- ❌ "무료 모델 전부 연결해 줘" → ✅ "코딩 질문용 무료 공급자 2개만 골라서 키 발급 주소와 한도를 알려 줘"
- 공급자마다 가입 절차·한도가 다르고 카드나 본인 확인을 요구하는 곳도 있으니 처음엔 2곳이면 충분. 고르기 어렵다면 Gemini(카드 없이 무료 키)·Groq(빠른 응답)·Kilo Code(키 없이 바로 테스트) 중 두 곳.
- 영상에서 언급된 모델 위치: GLM = Z AI 무료 모델, Kimi = Ollama Cloud, ChatGPT 계열 = 같은 회사의 오픈 모델 gpt-oss를 Groq 등에서 무료 사용.

### STEP 2. 키 없이 무료 모델 불러 보고, 무료 키 받기 (5분)
1. Kilo Code 무료 게이트웨이는 키 없이 응답한다. `"choices"`가 든 JSON이 나오고 `"model"`에 `:free`로 끝나는 모델 이름이 보이면 성공(어떤 무료 모델이 대답할지는 요청마다 바뀜).
```bash
curl -sS https://api.kilo.ai/api/gateway/chat/completions -H "Content-Type: application/json" -d '{"model": "openrouter/free", "messages": [{"role": "user", "content": "Say hello in one sentence."}], "max_tokens": 300}'
```
2. STEP 1에서 고른 곳의 키 발급 페이지에서 무료 키 받기(카드 없이 가능한 두 곳)
   - Gemini: https://aistudio.google.com/app/apikey
   - Groq: https://console.groq.com/keys
3. 키는 메모장에 잠깐만 두고 화면 캡처·공유 문서에 넣지 말 것.
4. Gemini 무료 등급, Mistral 무료 모드, OpenRouter·Kilo의 일부 무료 공급자는 보낸 내용을 기록하거나 학습에 쓸 수 있으므로 회사 코드·개인정보 금지.

### STEP 3. Manifest에 무료 키를 연결하고 대비 순서 정하기 (5분)
1. https://app.manifest.build/register 에서 가입 → 설정 안내 첫 화면 `Create your first harness`의 `Harness name`에 이름을 적고 `Create harness`
2. `mnfst_`로 시작하는 키는 설정 안내 마지막 단계 `Connect harness & go live`에서 복사
3. 로그인한 채로 https://manifest.build/free-models/ 를 열어 고른 공급자 카드의 `Connect` → Manifest가 그 공급자가 설정된 상태로 열리면 STEP 2의 키를 붙여넣어 저장
4. 저장한 무료 모델이 Manifest의 라우팅 선택지에 나타남. 키를 하나 더 연결했다면 첫 모델 뒤에 대비(폴백) 모델로 줄 세움(등급마다 최대 5개)
5. 한도 예: Groq `gpt-oss-120b` 분당 30회·하루 1,000회, OpenRouter 무료 모델은 모델당 하루 50회 → 앞 모델이 한도에 걸리면 다음 모델이 이어받도록 설정
6. "클로드 한도가 차면 다음 모델로 넘어가기"는 Manifest에 Claude 구독도 함께 연결해 맨 앞에 두고 무료 모델을 그 뒤 대비로 줄 세우는 방식
7. Manifest 클라우드를 쓰면 요청이 Manifest 서버를 거침. 내 컴퓨터 안에서만 돌리려면 셀프 호스팅 문서대로 Docker로 직접 띄움.

### STEP 4. 테스트 폴더 하나에서만 Claude Code 연결 (5분)
`mnfst_여기에_내_키`를 STEP 3에서 복사한 키로 바꿔 실행(주소는 그대로 `https://app.manifest.build`). 출력은 없고 `free-claude/.claude/settings.json`이 생기면 성공.
```bash
mkdir -p ~/free-claude/.claude && cd ~/free-claude
cat > .claude/settings.json <<'EOF'
{
  "model": "auto",
  "env": {
    "ANTHROPIC_BASE_URL": "https://app.manifest.build",
    "ANTHROPIC_AUTH_TOKEN": "mnfst_여기에_내_키"
  }
}
EOF
```
- ❌ 전역 `~/.claude/settings.json`에 바로 넣기(모든 폴더의 Claude Code가 무료 모델로 바뀜) → ✅ 테스트 폴더의 `.claude/settings.json`에만
1. 같은 폴더에서 `claude` 실행
2. "한 문장으로 인사해 줘" 전송
3. 답이 오면 Manifest 왼쪽 메뉴 `Requests`를 열어 `Model` 칸에 STEP 3에서 연결한 무료 모델 이름이 보이는지 확인
4. 되돌리기(출력 없음, 이 폴더에서 `claude`를 다시 켜면 평소 설정):
```bash
rm ~/free-claude/.claude/settings.json
```
5. 나중에 무료 모델이 대답하지 않을 때: 그 모델이 목록에서 빠졌거나 한도가 바뀐 경우가 대부분 → GitHub 목록에서 현재 열린 모델을 골라 STEP 3의 대비 순서를 다시 맞춘다.

## 핵심 팁 · 주의사항
- 전역 설정 수정 금지, 테스트 폴더의 설정만 사용
- 무료 모델은 수시로 바뀌므로 응답이 없으면 목록 재확인 후 대비 순서 갱신
- 한도 예: Groq gpt-oss-120b 분당 30/하루 1,000, OpenRouter 무료 모델 모델당 하루 50
- 개인정보·회사 데이터 입력 금지(일부 무료 공급자는 로깅·학습 가능)
- Manifest 클라우드 무료 플랜은 월 10,000 요청, 셀프 호스팅은 제한 없음
- 키(`mnfst_` 및 공급자 키)는 캡처·공유 문서에 넣지 않기

## 바로 쓰는 체크리스트
- [ ] Claude Code, git 확인(윈도는 Git Bash)
- [ ] `free-llm-apis` 스킬 설치(`references`, `SKILL.md` 확인)
- [ ] Kilo curl 테스트로 무료 응답(`:free`) 확인
- [ ] Gemini 또는 Groq 무료 키 발급
- [ ] Manifest harness 생성, `mnfst_` 키 확보, 공급자 Connect, 대비 순서 설정
- [ ] `~/free-claude/.claude/settings.json` 작성(전역 설정은 건드리지 않기)
- [ ] `Requests` 페이지에서 무료 모델 사용 확인, 필요시 `rm`으로 되돌리기
