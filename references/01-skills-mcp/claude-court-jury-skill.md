# 아이디어를 클로드 12명 재판에 세우는 스킬
- 원문: https://lazyowen.com/guides/claude-court-jury-skill
- 도구·주제: Claude Code (court-skill, `/court`) · 의사결정 검증 / 멀티에이전트 (스킬·MCP, 비즈니스, 10분, STEP 4개, 2026-10-08 공개)
- 한 줄 요약: `/court` 스킬이 검사, 변호인, 배심원 12명, 판사 역할의 에이전트를 돌려 내 아이디어에 유죄/무죄 표결과 "무죄가 되는 조건"을 알려 준다.

## 언제 쓰나
- 퇴사, 창업, 큰 구매, 글 발행, 코드 설계 같은 결정 전에, 듣기 좋은 말만 하는 클로드 대신 반대 시각 포함 두 번째 의견이 필요할 때

## 준비물 / 필요 도구
- Claude Code (Pro 이상 유료 플랜 또는 콘솔 계정), git, python3 (가이드 명령은 macOS 터미널 기준)
- 스킬 저장소: https://github.com/alexyc9381/court-skill (MIT, 개인 개발자 제작, Anthropic 공식 아님)
- 공식 문서: https://code.claude.com/docs/en/skills
- 스킬은 무료, 가입·API 키 불필요. 재판 1회가 하위 에이전트 17회 호출이라 플랜 사용량이 소모됨.
- 스킬 = 클로드 코드가 읽는 설명서 폴더. 별도 앱/웹사이트 없이 입력창에서 `/court`로 호출.

## 단계별 방법
### Quick Start. 설치
```bash
mkdir -p ~/.claude/skills
git clone https://github.com/alexyc9381/court-skill
cp -r court-skill/skills/court ~/.claude/skills/
```
- 성공하면 `Cloning into 'court-skill'...` 출력. 이미 깔려 있으면 건너뜀.
- `No such file or directory`로 멈추면 `~/.claude/skills`가 없는 것이니 `mkdir -p`부터 다시.
- 터미널이 낯설면 클로드 코드에 이렇게 맡겨도 됨: `Install the skill from https://github.com/alexyc9381/court-skill, then confirm /court works.`
- 클로드가 `court.py`, `jurors.json`, `SKILL.md` 세 파일과 `jury of 12 … 17 sub-agent calls`를 확인했다고 보고하면 성공.

### STEP 1. 스킬 설치 확인 (3분)
1. 도구 확인:
```bash
git --version
python3 --version
```
   - 버전 숫자 두 줄이 나오면 성공. 맥에서 개발자 도구 설치 창이 뜨면 설치 후 재실행.
2. 스킬 파일과 재판 규모 확인:
```bash
ls ~/.claude/skills/court
python3 ~/.claude/skills/court/court.py plan
```
   기대 출력:
```
court.py
jurors.json
SKILL.md
jury of 12: 2 opening statements, 2 rebuttals, 12 jurors, 1 judge = 17 sub-agent calls
```
3. 클로드 코드를 켜 둔 채 `~/.claude/skills`를 처음 만들었다면 입력창에 `/reload-skills`. 복사 끝난 `court-skill` 폴더는 지워도 됨.
4. 되돌리기(삭제): `rm -rf ~/.claude/skills/court` 후 `ls ~/.claude/skills`에 court가 안 보이면 삭제된 것.

### STEP 2. 첫 재판 열기 (5분)
1. 기록은 클로드 코드를 켠 폴더의 `.court`에만 쌓이므로 빈 폴더에서 시작:
```bash
mkdir -p ~/court-trials && cd ~/court-trials && claude
```
2. 입력창 아래에 `accept edits on`이 보일 때까지 `Shift+Tab`. 아니면 배심원이 파일 쓸 때마다 승인해야 함.
   - 누를 때마다 상태 줄이 순환. `auto mode on`에서 시작하면 한 번에 `manual mode on`(파일마다 승인), 한 번 더 누르면 `accept edits on`. 지나쳐 `plan mode on`이 되면 `accept edits on`이 다시 나올 때까지 계속 누름.
3. 배심원은 내가 쓴 내용만 안다(이 대화도 내 사정도 모름). 질문 대신 숫자가 든 주장으로 제출:
   - ❌ `/court 캔들 사업 어때?`
   - ✅ `/court 회사를 그만두고 엣시에서 수제 캔들을 전업으로 팔겠습니다. 모아 둔 돈은 8,000달러이고, 지금까지 40건 팔았습니다.`
4. 클로드가 "12 jurors, 17 sub-agent calls" 같은 규모를 한 줄로 알리고 시작하면 성공.
5. 사용량이 빠듯하면 `/court` 바로 뒤, 사건 문장 앞에 옵션:
   - `--quick`: 배심원 6명, 호출 11번 (예: `/court --quick 회사를 그만두고 …`)
   - `--jury 3`: 배심원 3명, 호출 8번 (3~12 지정)
   - 옵션 없음: 배심원 12명, 호출 17번

### STEP 3. 판결문 읽기 (3분)
재판이 끝나면 `.court` 안 실행 폴더에 `VERDICT.md`가 생기고 화면에도 나옴. 영어 제목 대응:

| 제목 | 뜻 | 먼저 볼 것 |
|---|---|---|
| The verdict | 평결 | GUILTY 9 to 3 같은 표 수 |
| How the jury voted | 배심원별 표 | 한 줄 이유 |
| Charges that stuck | 남은 혐의 | 여러 명이 짚은 약점 (괄호에 짚은 배심원 수) |
| What the defense got right | 변호인이 맞힌 점 | 지켜야 할 강점 |
| Conditions for acquittal | 무죄 조건 | 바로 할 변경점 (핵심 산출물) |
| The sentence | 판사의 선고 | 지금 할지 말지 |

- 영어로 나오면 같은 대화에서 "이 판결문을 한국어로 옮겨 줘".
- 저장소 예제(배심원 3명, 간호사 퇴사 후 캔들 전업): 유죄 3 대 0. 통계학자는 석 달 40건 합계 하나로 판매가 4배 뛴다고 건 점을, 부모는 월 매출 약 373달러로 월세 1,600달러를 못 감당하는 점을, 변호사는 보험·집주인 허락 없는 화재/임대 위험을 지적.
- 무죄 조건 3개: 월 판매가 5개월 안에 약 57건까지 오르는지 확인 / 회사에서 휴직·재고용 약속을 서면으로 받기 / 집주인 동의 + 제조물 책임 보험. 선고: 사표 내지 말고 갖춘 뒤 다시 가져오라.
- 조건을 채웠다면 바뀐 내용을 사건에 적어 재심. 판결이 싫다고 뒤집어 달라 하지 말고 무죄 조건을 반영한 새 사건으로 제출.

### STEP 4. 상황별 재판 프롬프트 7개 (2분)
사건은 질문이 아니라 주장으로(유죄/무죄 가를 대상이 있어야 투표). 대괄호를 채워 붙여넣기:
1. 사업 아이디어: `/court [고객]을 위한 [사업]을 시작하겠습니다. 가진 것은 [돈·시간]이고, 지금까지 [해 본 일]을 했고, 가격은 [가격]으로 받겠습니다.`
2. 퇴사: `/court [직업]을 그만두고 [계획]을 전업으로 하겠습니다. 저축은 [금액], 지금까지 번 돈은 [수입], 한 달 생활비는 [비용]입니다.`
3. 올리기 전 게시물: `/court 이 게시물은 평소 게시물보다 반응이 더 좋을 겁니다: [게시물 붙여넣기]. 평소 게시물은 [숫자]를 받습니다.` (❌ `/court 이 게시물 괜찮아?`)
4. 큰 지출: `/court [물건]을 [가격]에 사겠습니다. [이유]에 쓸 겁니다. 대안은 [대안]입니다.`
5. 코드 계획: `/court [앱의 어느 부분]을 [지금 방식] 대신 [새 방식]으로 다시 짜겠습니다. 이유는 [이유]입니다.`
6. 내가 믿는 주장: `/court [주장]. 근거는 [근거]입니다.`
7. 클로드 답의 두 번째 의견: `/court 방금 제안한 계획이 맞는 계획입니다.` (클로드가 뭔가 제안한 직후 같은 대화에서. 빠뜨린 점을 가장 빨리 확인하는 방법)

### 보조 프롬프트: 설치+재판 준비 위임 (프롬프트 뼈대)
- 목적: 초보자가 클로드 코드에 court 스킬 설치와 첫 재판 준비를 맡김.
- 역할: court 스킬 설치·첫 재판 준비 담당. 슬롯: [재판에 올릴 내 결정(한 문장+숫자)].
- 작업: git/python3 버전 확인 → `ls ~/.claude/skills/court`로 설치 여부 확인 후 없을 때만 mkdir/clone/cp → `court.py plan` 검증 → 스킬 설명과 `/court` 제출법을 5줄 이내 안내. 재판은 열지 않음.
- 제약: sudo·전역 설치·설정 수정은 먼저 질문, 비밀키 출력 금지, 기존 court 폴더 덮어쓰기 금지.
- 출력/검증: 실행 명령, 버전, 새 폴더, 남은 오류. 세 파일과 `jury of 12 … 17 sub-agent calls`가 나와야 완료, 실패 시 명령·원인·다음 조치 보고.

## 재판 진행 방식
1. 검사 클로드: 지금 모습 그대로면 실패한다는 가장 강한 주장.
2. 변호인 클로드: 된다는 가장 강한 주장, 이후 쌍방 반박.
3. 배심원 12명: 기록 전체를 읽고 서로의 표를 못 본 채 유무죄 투표 (회계사, 처음 사는 고객, 경쟁자, 은퇴한 판사, 십대, 엔지니어, 소상공인, 통계학자, 부모, 투자자, 디자이너, 변호사).
4. 판사: 평결, 남은 혐의, 변호인이 맞힌 점을 읽고 무죄 조건 결정. 무죄 조건 = 표를 가장 많이 뒤집을 구체적 변경점.

## 핵심 팁 · 주의사항
- 배심원은 언어 모델이므로 법률/재무 조언이 아니라 두 번째 의견으로만 사용.
- 질문형 ❌, 숫자·사실이 담긴 주장형 ✅.
- 사용량 소모: 처음엔 `--quick`나 `--jury 3` 권장.
- 개인 개발자의 비공식 스킬. 삭제는 `rm -rf ~/.claude/skills/court`.
- 터미널 낯설면 클로드 코드에 설치를 맡길 것.

## 바로 쓰는 체크리스트
- [ ] claude, git, python3 설치 확인
- [ ] 스킬 설치 + `court.py plan` 출력 확인
- [ ] 빈 폴더에서 claude 실행, accept edits on
- [ ] 숫자 포함 주장 한 문장 작성 후 `/court` (처음엔 `--quick`)
- [ ] VERDICT.md의 무죄 조건을 반영해 새 사건으로 재제출
