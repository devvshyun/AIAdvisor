# 링크드인 스킬 12개
- 도구·주제: Claude Code 플러그인(linkedin-skills) · Apify · 링크드인 그로스 / 반응자 분석
- 한 줄 요약: 링크드인 스킬 묶음을 설치해 프로필/콘텐츠/댓글 초안을 키 없이 쓰고, Apify 토큰을 연결해 내 포스트 반응자를 동료/윗선/잠재 고객 3그룹으로 나눈다. (4단계)

## 언제 쓰나
- 링크드인 포스트·댓글·답글·프로필·콘텐츠 계획·반응 분석을 클로드로 보조받고 싶을 때, 내 글 반응자 중 잠재 고객을 추리고 싶을 때
- 링크드인 계정에 로그인해 움직이는 봇이 아님. 모든 스킬은 초안을 먼저 보여 주고 승인을 기다림(올리는 건 내가 복사·붙여넣기)

## 준비물 / 필요 도구
- 저장소(MIT, 개인·상업 자유): https://github.com/sergebulaev/linkedin-skills (스타 약 4,000, 만든 곳 Creative Content Crafts / https://cccrafts.ai/)
- Claude Code(맥·윈도·리눅스) 또는 유료 플랜(Pro·Max·Team·Enterprise)의 데스크톱·웹 앱(설정에서 코드 실행 켜기). 반응 분석엔 Git + Python 3. STEP 3 명령은 맥 터미널 기준.
- Apify: https://console.apify.com/sign-up (월 $5 무료 크레딧, 초과 시 결과 1,000건당 $1~5; 반응자 50명 약 $0.25)
- 자동 발행용 Publora(선택, 무료 월 15개), 이미지 생성 Pixfaro(선택)
- 스킬은 무료, Claude 구독은 별도. 전체 스킬 이름 목록은 공개되지 않음. 키 없이 도는 4개: 프로필 다듬기, 콘텐츠 계획, AI 티 빼기, 인터뷰.
- README: https://github.com/sergebulaev/linkedin-skills#install , 문제 해결 `#troubleshooting`

## 단계별 방법
**Quick Start**
```
claude plugin marketplace add sergebulaev/linkedin-skills
claude plugin install linkedin-skills@linkedin-skills
```
성공: `✔ Successfully installed plugin: linkedin-skills@linkedin-skills`

1. **STEP 1 설치·켜짐 확인 (3분)**
   ```
   claude --version
   git --version
   claude plugin list
   ```
   - `linkedin-skills@linkedin-skills` 아래 `Status: ✔ enabled` 확인(이미 깔렸으면 설치 건너뜀). 이후 claude를 껐다 켜야 새 대화에서 스킬 인식.
   - 데스크톱 앱: 왼쪽 사용자 지정(Customize) > 플러그인(Plugins) > 우상단 Add > Add marketplace > Add from a repository > `sergebulaev/linkedin-skills` 붙여넣고 동기화 > 탐색(Discover) 탭 카드 우상단 `+` > 내 항목 탭에서 켜짐 확인. (README `#claude-desktop-mac--windows`)
2. **STEP 2 키 없이 써 보기 (5분)**: 프로필 스킬은 링크를 열지 못하므로 헤드라인·소개를 직접 붙여넣어야 함.
   - ❌ `linkedin.com/in/내이름 이 프로필 링크 열어서 고쳐줘`
   - ✅ 프롬프트 뼈대: "내 프로필을 인바운드 문의가 오도록 다시 써 달라" + 슬롯 `내 고객: <예: 직원 50명 이하 B2B SaaS 마케팅 팀장>`, `헤드라인: <붙여넣기>`, `소개(About): <붙여넣기>`. → 헤드라인·소개·대표 게시물(Featured) 개선안이 나오면 성공.
3. **STEP 3 Apify 토큰 연결 (10분)** — 데스크톱·웹 앱만 쓰면 건너뜀(STEP 4 요청 시 스킬이 반응자 목록을 직접 붙여넣으라고 안내).
   - Apify 가입 후 https://console.apify.com/settings/integrations 의 Personal API tokens에서 "Default API token created on sign up." 줄의 복사 아이콘으로 `apify_api_...` 토큰 복사(새로 만들 필요 없음).
   ```
   git clone https://github.com/sergebulaev/linkedin-skills.git
   cd linkedin-skills
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests python-dotenv
   nano .env
   ```
   - 성공: `Successfully installed ...`. `.env`에는 한 줄만 (`nano`: Ctrl+O, 엔터, Ctrl+X 로 저장):
   ```
   APIFY_TOKEN=복사한토큰
   ```
   ```
   python3 scripts/check_config.py --offline
   ```
   - 성공: `Effective behaviour` 아래 `reading backend apify (auto-fetch)`. `--offline`을 빼면 Apify에 실제로 질의해 토큰 유효성까지 확인.
   - 맥 기본 Python의 `NotOpenSSLWarning`, `[----]` 줄(미설정 선택 기능 Publora·Pixfaro)은 실패가 아님.
   - 플러그인 끄기 (폴더 안 스킬 12개와 중복 로딩 방지, 플러그인판 스킬은 이 폴더 `.env`를 못 읽음):
   ```
   claude plugin disable linkedin-skills@linkedin-skills
   claude plugin list
   ```
   - `Status: ✘ disabled` 확인. 다른 폴더에서 다시 쓰려면 `disable` 자리에 `enable`.
4. **STEP 4 반응자 3그룹 분류 (10분)**
   ```
   cd linkedin-skills
   source .venv/bin/activate
   claude
   ```
   - 프롬프트 뼈대: 이 링크드인 포스트의 좋아요·댓글 작성자를 가져와 동료/윗선/잠재 고객으로 분류. 슬롯 `포스트: <내 포스트 링크>`, `내 고객: <예: 직원 50명 이하 B2B SaaS 마케팅 팀장>`, `가져올 인원은 50명까지만`. 약 $0.25(50명). 결과: 사람별 그룹 표 + 그룹별 할 일.
   - 동료=비슷한 단계 회사 창업자·실무자(맞팔 대상) / 윗선=인접 분야 큰 회사 디렉터급 이상(그 사람 글 밑이 댓글 자리) / 잠재 고객=직함·회사가 고객 조건에 모두 일치(짧은 첫 메시지 초안 포함).
   - 여러 포스트를 주면 두 번 이상 반응한 사람을 따로 표시.
   - 주간 루틴: ① 같은 사람들의 새 글에 댓글(요청: "이 포스트에 댓글 써줘" + 링크) ② "내 댓글 중 작성자가 답한 스레드 찾아줘"로 확인(스킬이 6~24시간 내 스레드 표시) ③ 잠재 고객에게는 반응 당일을 피해 24~72시간 후 한 번만 메시지.

## 핵심 팁 · 주의사항
- ❌ `pip install -r requirements.txt` → 맥 기본 Python 3.9에서 `No matching distribution found for python-dotenv>=1.2.3`. ✅ `pip install requests python-dotenv`.
- ❌ `.env.example` 복사: 예시 값이 진짜 키처럼 검사를 통과해 버림. ✅ 빈 파일에 한 줄만.
- `.env`는 누구에게도 공유 금지.
- ❌ "업계 인기 포스트 아무거나 긁어서 고객 찾아줘" — 남의 글 반응자 대량 수집은 스킬 규칙이 말림. ✅ 내 포스트 링크 + 고객 조건 한 줄.
- 윈도는 가상환경 활성화·파일 편집 방법이 다름.
- 자동 발행은 Publora 연동(README `#optional-auto-post-with-publora`), Apify 연결 `#optional-read-linkedin-data-with-apify`.

## 바로 쓰는 체크리스트
- [ ] `claude --version` / `git --version` 확인
- [ ] 마켓플레이스 추가 + 플러그인 설치, `✔ enabled` 확인, claude 재시작
- [ ] 키 없이 프로필(헤드라인·소개 붙여넣기)/콘텐츠 계획 시험
- [ ] Apify 토큰을 `.env`에 저장 → `check_config.py --offline`에서 `reading backend apify (auto-fetch)` 확인 → 플러그인 disable
- [ ] 내 포스트 링크 + 고객 조건 + 인원 수로 3그룹 분류
- [ ] 주간 댓글/스레드(6~24시간) 확인, 잠재 고객 24~72시간 후 메시지 1회
