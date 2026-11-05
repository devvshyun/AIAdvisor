# 프롬프트 마스터 (Prompt Master 스킬)
- 도구·주제: Claude Code / claude.ai + prompt-master 스킬 · 재요청 줄여 사용량 절약
- 한 줄 요약: 한도를 갉아먹는 건 긴 요청 한 번이 아니라 재요청 — 대충 쓴 한 줄을 결과 모양·범위·종료 조건이 채워진 완성 프롬프트로 바꿔주는 오픈소스(MIT) 스킬을 설치한다. (2026-08-29 공개, 읽는 데 11분, 7단계 약 13분)

## 언제 쓰나
- 한 줄 요청이 자꾸 어긋나 "아니 그게 아니라"를 서너 번 더 치게 될 때(작업 하나에 요금을 서너 번 내는 셈)
- 결과 모양 / 건드릴 파일 범위 / 멈출 시점 / 앞서 정한 결정이 빠진 프롬프트를 보강하고 싶을 때

## 준비물 / 필요 도구 (이름 + 공식 링크)
- prompt-master (MIT, 계정 없이 다운로드): https://github.com/nidhinjs/prompt-master · SKILL.md https://github.com/nidhinjs/prompt-master/blob/main/SKILL.md
- Claude 스킬 설정 화면 https://claude.ai/customize/skills · 기능 설정 https://claude.ai/settings/capabilities
- 문서: https://code.claude.com/docs/en/skills · https://support.claude.com/en/articles/12512180-using-skills-in-claude-ai
- Claude Code를 쓰려면 `git`과 터미널(macOS 터미널 / Windows PowerShell). 스킬은 무료 요금제 포함 대부분의 요금제에서 가능, 스킬 자체는 무료(프롬프트 생성 대화는 평소 사용량 소모).
- 용어: 스킬 = AI가 필요할 때 꺼내 읽는 설명서 묶음, `SKILL.md` = 언제 이 스킬을 꺼낼지 판단하는 설명서 파일.

## 단계별 방법
**Quick Start**
- 클로드 웹: GitHub의 초록색 Code → Download ZIP → 스킬 설정 화면에 업로드.
- 클로드 코드:
  ```
  mkdir -p ~/.claude/skills
  git clone https://github.com/nidhinjs/prompt-master.git ~/.claude/skills/prompt-master
  ls ~/.claude/skills/prompt-master/SKILL.md
  ```
  `Cloning into ...` 후 프롬프트가 돌아오면 성공. 경로가 한 줄 출력되면 설치 확인, `No such file or directory`면 위 두 줄 재실행.

1. **STEP 1 한도가 닳는 이유 (2분)**: 흐름 = 대충 한 줄 → 클로드가 쓴 대로만 수행 → 의도와 달라 재요청 반복. 프롬프트 마스터는 일 시작 전에 요청을 다시 써서 이 반복을 시작 지점에서 끊음. 채워 주는 네 가지: 결과 모양, 건드릴 파일 범위, 멈출 시점, 앞에서 이미 정한 것들.
2. **STEP 2 압축 파일 받기 (1분)**: github.com/nidhinjs/prompt-master 오른쪽 위 초록색 `Code` → 맨 아래 `Download ZIP` → `prompt-master-main.zip`. ❌ 받은 ZIP을 풀었다가 다시 압축 — `SKILL.md`가 압축 최상위 폴더에 있어야 인식됨(다시 묶으면 업로드는 되지만 동작 안 함). ✅ 손대지 말고 그대로 업로드.
3. **STEP 3 클로드 웹에 올리기 (2분)** (클로드 코드만 쓰면 STEP 4로)
   - `claude.ai/settings/capabilities`에서 "코드 실행 및 파일 생성"을 켬(꺼져 있으면 스킬 항목이 회색으로 잠김).
   - 경로: claude.ai → 설정 → Customize(사용자 설정) → Skills, 또는 `claude.ai/customize/skills` 직접 접속 → `+` → `Create skill` → `Upload a skill` → ZIP 업로드 → 목록의 `prompt-master` 옆 스위치가 켜졌는지 확인.
   - 업로드한 스킬은 내 계정에만 적용. 회사 계정은 관리자가 스킬 기능을 잠가 업로드 버튼이 안 보일 수 있음.
4. **STEP 4 클로드 코드에 설치 (1분)** (브라우저만 쓰면 STEP 5로)
   ```
   mkdir -p ~/.claude/skills
   git clone https://github.com/nidhinjs/prompt-master.git ~/.claude/skills/prompt-master
   ls ~/.claude/skills/prompt-master
   ```
   - `SKILL.md`, `README.md`, `references` 세 가지가 보이면 성공(`SKILL.md`가 없으면 읽지 못함). 설치 후 Claude Code를 껐다 다시 켜고 `/` 입력 시 목록에 `/prompt-master`가 보여야 함.
5. **STEP 5 실제로 써보기 (3분)**: 새 대화에서 일부러 대충, 원하는 것을 한 문장으로.
   - 요청 뼈대: "클로드 코드한테 줄 프롬프트를 써 줘. 우리 회사 소개 페이지를 만들고 싶은데 예약 문의 칸도 있으면 좋겠어." → 복사해 바로 쓸 수 있는 프롬프트 한 덩어리(결과 모양·범위·멈출 시점 포함)가 돌아옴. Claude Code, ChatGPT, Cursor 어디든 붙여넣기 가능.
   - 정보가 부족하면 질문을 **최대 3개**까지만 한 뒤 프롬프트를 만들어 줌.
   - ❌ 받은 프롬프트를 확인 없이 붙여넣기 — 범위·종료 조건 두 줄(약 10초)을 눈으로 확인(내 프로젝트와 경로가 다르면 엉뚱한 파일이 바뀜).
6. **STEP 6 이미 쓴 프롬프트 고치기 (2분)**: 요청 뼈대: "이 프롬프트를 썼는데 결과가 자꾸 빗나가. 뭐가 빠졌는지 찾아서 고쳐 줘. `<안 먹혔던 프롬프트 그대로 붙여넣기>`" → 빠진 조건을 채운 새 버전 + 어디를 왜 고쳤는지 한 줄.
   - 크레딧 낭비 37가지 패턴을 대조한다고 설명(예: 범위 없는 요청 "내 앱 고쳐 줘" → "이 파일의 이 부분만 고치고 다른 건 건드리지 마" / 완료 조건 없는 "더 좋게 만들어 줘" → "이 조건을 통과하면 끝" / 한 번에 두 가지 시키기 "설명하고 또 고쳐 줘" → 설명 먼저, 수정은 그다음). 37개라는 수치는 직접 검증되지 않음.
   - 미드저니(이미지)·소라(영상)·커서(코딩) 등 대상 도구별 형태로도 써 주므로 어떤 도구에 쓸지만 알려 주면 됨.
7. **STEP 7 새 대화마다 다시 설명하지 않기 (2분)**: 앞서 정한 결정(쓰기로 한 도구, 이미 실패한 방식)을 프롬프트에 함께 넣어 줘서 클로드가 접은 방식을 다시 제안하는 일이 줄어듦. 요청 뼈대: "아까 정한 대로 `<쓰기로 한 도구나 규칙>`은 그대로 가고, `<이번에 하려는 것>`을 위한 프롬프트를 써 줘."

**설치·검증 위임 프롬프트 뼈대(Claude Code)**: 역할=prompt-master 설치·연결 검증 담당. 슬롯 `<운영체제와 셸>`, `<쓰는 도구(클로드 웹/코드)>`, `<목표 한 줄>`. 작업: ① 클로드 코드면 `ls ~/.claude/skills`에 prompt-master가 있는지, `claude --version` 확인(웹이면 자동 설치하지 말고 화면 순서만 안내, 이미 있으면 상태만 보고) ② 없으면 `mkdir -p ~/.claude/skills`와 git clone 실행(웹은 ZIP 업로드 단계 안내) ③ `ls ~/.claude/skills/prompt-master/SKILL.md` 확인 후 새로 연 클로드 코드에서 `/prompt-master` 노출 확인 ④ 스킬이 하는 일과 사용법을 5줄 이내로 설명. 제약: 기존 스킬 폴더·설정 덮어쓰기/삭제 금지, 중복 설치 금지, `.env`와 API 키 값 읽기·출력 금지, 한 번에 하나씩 실행·확인. 검증: SKILL.md 경로 출력 + `/prompt-master` 노출. 실패하면 완료 보고 금지. (에이전트가 명령을 대신 실행하므로 실행 전 명령 검토)

## 핵심 팁 · 주의사항
- ZIP 재압축 금지(SKILL.md가 최상위에 있어야 함).
- 스킬은 **새 대화부터** 적용(쓰던 대화에서는 안 먹을 수 있음). 그래도 안 되면 "프롬프트 마스터로 프롬프트를 써 줘"처럼 이름을 직접 부르기.
- 프롬프트가 길수록 좋은 게 아님 — 빠진 조건이 채워졌는지가 핵심. 너무 빡빡하면 "이 부분은 좀 느슨하게 해 줘"라고 조정.
- 절약 효과는 재요청 감소에서 나옴(프롬프트 생성 대화도 사용량 소모). 설치는 클로드에, 만들어진 프롬프트는 ChatGPT·Cursor·Midjourney 등 어디에나 사용 가능.

## 문제 해결
- ZIP 업로드 후 목록에 안 보임 → 재압축 의심, 내려받은 ZIP 그대로 업로드.
- 스킬 항목이 회색 잠금 → `claude.ai/settings/capabilities`에서 코드 실행 및 파일 생성 켜고 새로고침(회사 계정은 관리자가 꺼 뒀을 수 있음).
- 설치했는데 클로드가 안 씀 → 새 대화에서 재시도 / 스킬 이름 직접 호출.
- 클로드 코드에서 `/prompt-master` 안 보임 → `ls ~/.claude/skills/prompt-master/SKILL.md`로 파일 확인, 경로가 나오는데도 안 보이면 Claude Code를 완전 종료 후 재실행(실행 중에는 새 스킬을 못 읽음).

## 바로 쓰는 체크리스트
- [ ] clone 또는 ZIP 업로드(웹은 코드 실행·파일 생성 ON, 스킬 토글 ON)
- [ ] 재시작/새 대화에서 `/prompt-master` 확인
- [ ] 한 줄 요청 → 완성 프롬프트 확인(범위·종료 조건 두 줄 점검)
- [ ] 실패한 프롬프트는 붙여서 결함 진단 요청
- [ ] 새 대화에서는 앞 결정을 한 줄 맥락으로 이어 붙이기
