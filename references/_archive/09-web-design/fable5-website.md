# 스크롤할 때마다 영상이 움직이는 웹사이트, 한 줄로 만드는 세팅
- 도구·주제: Claude Code + Higgsfield(CLI / 커넥터) · 스크롤 연동 영상 웹사이트 제작·배포
- 한 줄 요약: AI가 만든 웹사이트가 밋밋한 이유는 넣을 영상·이미지가 없어서다. 힉스필드를 클로드에 연결하면 클로드가 사이트에 필요한 영상까지 직접 생성해 붙이고 배포까지 한다. 모델은 Fable 5, 추론은 max로 올려 한 문단 주문으로 사이트를 통째로 만든다. (2026-08-30 공개, 읽는 데 11분, 따라 하면 약 20분, STEP 8개)

## 언제 쓰나
- 애플 홈페이지처럼 스크롤에 맞춰 장면이 바뀌는 브랜드/랜딩 사이트를 한 번의 주문으로 만들고 싶을 때
- AI로 만든 사이트가 글자와 회색 네모뿐이라 다 비슷하게 보이는 문제를 풀고 싶을 때

## 준비물 / 필요 도구
- Higgsfield(영상·이미지 생성 AI 서비스, 시댄스·클링·소라 등 수십 개 모델): 계정 로그인만 필요, 별도 API 키 불필요
  - CLI 안내: https://higgsfield.ai/cli · GitHub https://github.com/higgsfield-ai/cli
  - 스킬: https://github.com/higgsfield-ai/skills (사이트를 만들고 배포하는 `higgsfield-websites` 포함) · 웹사이트 소개 https://higgsfield.ai/skills/website
  - 커넥터 안내: https://higgsfield.ai/mcp · 커넥터 설정 https://claude.ai/customize/connectors
- Claude Code + Node.js/npm(터미널; macOS 터미널 / Windows PowerShell). 모델·추론 설정 문서 https://code.claude.com/docs/en/model-config
- 비용: 가격 명시 없음. 힉스필드 요금제의 크레딧이 모델·화질·길이에 따라 차감. Fable 5 사용분은 요금제에 따라 별도 사용량 크레딧으로 청구될 수 있음(모델 목록에 "Requires usage credits" 표시)
- 연결 방식 선택(STEP 2): 브라우저 클로드 = 커넥터(이미지·영상 생성까지만, 사이트 제작 설명서가 안 붙음), 터미널 클로드 코드 = 명령어 도구(생성 + 사이트 제작 + 배포) → 사이트를 통째로 만들어 배포하려면 반드시 명령어 도구 방식

## 단계별 방법
### 프롬프트 뼈대 A. 힉스필드 설치·로그인·연결 검증 위임 (Claude Code, 선택)
- 목적: CLI 설치, 스킬 설치, 로그인, 모델 목록 확인
- 역할: 힉스필드 CLI·스킬의 설치·로그인·연결 검증 담당
- 슬롯: [운영체제와 셸], [내가 쓰는 도구], [목표 한 줄(예: 영상이 들어간 웹사이트를 한 번에)]
- 작업 4단계: ① `higgsfield version`과 `ls ~/.claude/skills`의 higgsfield 폴더 확인(있으면 재설치 말고 상태만) ② 미설치 시 `npm install -g @higgsfield/cli`, `npx skills add higgsfield-ai/skills`, `higgsfield auth login`(브라우저 로그인은 사용자가 하므로 화면 주소를 알려주고 대기) ③ `higgsfield version`, `higgsfield model list`가 모델 목록을 출력하는지 확인 ④ 5줄 이내 설명
- 제약: 중복 설치 금지, 기존 설정 덮어쓰기·삭제 금지, 토큰·로그인 정보 출력 금지, `.env` 같은 비밀 파일 읽기 금지, 한 번에 하나씩
- 출력: 실행 명령, 버전, 설치된 스킬 이름, 남은 오류
- 검증: `higgsfield version`이 버전 문자열, `higgsfield model list`가 모델 이름 목록을 출력해야 완료. 실패 시 완료 보고 금지

### Quick Start (클로드 코드 사용 시 세 줄)
```bash
npm install -g @higgsfield/cli
npx skills add higgsfield-ai/skills
higgsfield auth login
```
마지막 줄에서 브라우저가 열리고 힉스필드 로그인 후 터미널에 완료 메시지. 확인(쓸 수 있는 모델 목록):
```bash
higgsfield model list
```
`seedance_2_0`, `kling3_0`, `nano_banana_2` 같은 이름이 출력되면 성공. `Not authenticated`가 나오면 `higgsfield auth login` 재실행. 이후 클로드 코드에서 한국어로 주문:
```
원두 브랜드 소개 사이트를 만들어 줘.
색은 흙갈색, 크림, 짙은 초록. 챕터는 여섯 개.
영상은 시댄스 2.0으로 전부 생성해서 넣어 주고, 배포까지 해 줘.
```

### STEP 1. 왜 AI 웹사이트가 밋밋해지는지 (2분)
AI는 코드는 잘 쓰지만 안을 채울 재료(영상·사진)가 없어 회색 네모와 글자로 때운다. 스크롤 장면 전환 사이트는 코드가 특별한 게 아니라 영상이 있느냐의 차이. 힉스필드를 붙이면 클로드가 영상 모델을 직접 불러 필요한 장면을 생성해 붙인다.

### STEP 2. 두 가지 연결 방식 중 고르기 (1분)
위 "연결 방식 선택" 참고. 웹사이트 제작·배포 목적이면 명령어 도구(STEP 4), 터미널을 안 쓰면 커넥터(STEP 3, 생성만 가능).

### STEP 3. 브라우저 클로드에 커넥터 붙이기 (2분, 터미널 안 쓰는 경우만)
1. https://claude.ai/customize/connectors 열기
2. 커스텀 커넥터 추가 → 이름 `Higgsfield`, 주소 칸에 아래 입력
```
https://mcp.higgsfield.ai/mcp
```
3. 연결 → 힉스필드 로그인·승인 → 목록에 Higgsfield가 초록색으로 붙음
4. 새 대화에서 확인(모델 이름과 크레딧 숫자가 오면 연결됨, "연결할 수 없다"면 주소 재확인)
```
힉스필드에서 쓸 수 있는 모델 목록과 지금 남은 크레딧을 보여 줘.
```

### STEP 4. 클로드 코드에 명령어 도구 설치 (3분)
1. 도구 설치(`added ... packages` 줄 후 프롬프트 복귀)
```bash
npm install -g @higgsfield/cli
```
2. 사용법 스킬 설치(없으면 도구는 있어도 클로드가 부를 줄 모름. 설치된 스킬 이름 목록에 사이트 제작·배포용 `higgsfield-websites`가 포함)
```bash
npx skills add higgsfield-ai/skills
```
3. 로그인(승인하면 터미널에 완료 메시지)
```bash
higgsfield auth login
```
4. 전체 확인(버전과 모델 목록이 이어 출력되면 준비 끝, `Session expired`면 토큰 만료이니 `higgsfield auth login` 재실행)
```bash
higgsfield version && higgsfield model list
```

### STEP 5. 모델을 Fable 5로, 추론을 max로 (1분)
클로드 코드에서:
```
/model fable
```
화면 위쪽 모델 이름이 Fable 5로 바뀐다(안 보이면 버전이 낮은 것이니 터미널에서 `claude update` 후 재실행). Fable 5는 클로드 모델 중 가장 큰 작업(여러 시간짜리)을 끝까지 맡기도록 만든 모델.
```
/effort max
```
화면 아래 모델 이름 옆에 `max`가 붙는다. max는 현재 창에서만 유지되므로 새 창에서는 다시 입력(지속하려면 환경 변수 `CLAUDE_CODE_EFFORT_LEVEL`에 `max`).

### STEP 6. 한 줄로 주문하기 (3분)
짧게 쓰라는 것이 아무 말이나 쓰라는 뜻은 아니다. 안 적은 것은 클로드가 상상한다. 다섯 가지를 넣는다: 브랜드 이름, 색 세 개(+포인트 색 하나), 챕터 수, 필요한 기능, 영상 모델.
```
<브랜드 이름> 웹사이트를 만들어 줘.
색은 <색 1>, <색 2>, <색 3>을 쓰고 포인트 색은 <포인트 색> 하나만.
<보여 주고 싶은 흐름 한 줄>을 챕터 <숫자> 개로 나눠서 스크롤에 맞춰 넘어가게 해 줘.
<필요한 기능, 예: 문의 폼, 장바구니, 로그인>을 넣고 휴대폰 화면도 되게 해 줘.
사이트에 들어갈 영상과 이미지는 시댄스 2.0으로 전부 생성해 줘.
```
클로드가 구조를 잡고 영상을 만들기 시작하며 완성될 때까지 알아서 기다렸다 붙인다. 시댄스 2.0은 소리(효과음)까지 같이 만드는 영상 모델.

### STEP 7. 만들어진 사이트 배포하기 (5분)
가장 쉬운 방법은 주문 끝에 한 줄 추가:
```
다 만들었으면 배포까지 하고 열리는 주소를 알려 줘.
```
직접 확인하고 싶다면 클로드가 실행하는 세 명령(사이트 생성 → 코드 저장소 접근 → 배포). 첫 명령이 성공하면 사이트 번호·미리보기 주소·공개 주소가 표로 출력되고, 배포가 끝나면 공개 주소에서 실제 화면이 열린다.
```bash
higgsfield website create --type website --category other --subdomain <내-사이트-이름>
higgsfield website repo-access <website_id>
higgsfield website deploy <website_id>
```
- `--subdomain`은 주소가 되는 이름: 영문 소문자·숫자·하이픈만, `api`·`www` 같은 이름은 거절
- 수정 후에는 배포를 다시 해야 함(코드만 올리고 배포를 건너뛰면 주소에는 옛 화면)

### STEP 8. 마음에 안 드는 부분 고치기 (3분)
같은 대화에서 고칠 곳만 말한다(클로드가 앞서 만든 코드·영상을 들고 있음).
```
첫 화면 영상이 너무 빨라. 느리게 다시 만들고,
두 번째 챕터 글자는 더 크게 해 줘. 그리고 다시 배포해 줘.
```
바뀐 부분만 재생성하고 배포까지 이어지므로 크레딧도 덜 쓴다. 색·분위기를 통째로 바꾸려면 색만 새로 지정해 다시 부탁(구조는 유지).

## 핵심 팁 · 주의사항
- 웹사이트 제작·배포는 명령어 도구 방식만 가능(브라우저 커넥터는 이미지·영상 생성까지)
- `/effort max`는 창마다 다시 입력
- Fable 5 사용분이 별도 사용량 크레딧일 수 있으니 모델 목록의 "Requires usage credits" 확인
- 배포 후 수정은 반드시 재배포
- 영상 생성은 길이·모델에 따라 시간이 걸리므로 창을 닫지 말 것(이미지는 몇 초)

## 문제 해결 / FAQ
- `higgsfield` 명령을 못 찾음: `npm install -g @higgsfield/cli` 재실행 후 터미널 창 재시작
- 모델 목록은 나오는데 영상이 안 만들어짐: 대부분 크레딧 부족 → 힉스필드 계정 화면에서 잔여 크레딧 확인(모델·화질별 차감량 상이)
- `/model fable`이 안 보임: `claude update` 후 클로드 코드를 완전히 껐다 다시 열기
- `/effort max`가 다음 날 풀려 있음: 창 단위 설정이므로 재입력 또는 환경 변수 `CLAUDE_CODE_EFFORT_LEVEL`에 `max`
- 커넥터로 붙였는데 사이트 제작 불가: 커넥터는 생성까지만 → STEP 4 방식으로 설치
- API 키가 필요한가: 아님, 계정 로그인만
- 배포 주소 변경: 가능(만들 때 `--subdomain`, 이후 `higgsfield website` 명령으로 이름 변경, 이미 쓰는 이름은 거절)

## 바로 쓰는 체크리스트
- [ ] 연결 방식 선택(사이트 제작이면 CLI)
- [ ] CLI 설치 + 스킬 설치 + `higgsfield auth login`
- [ ] `higgsfield version && higgsfield model list` 확인
- [ ] `/model fable`, `/effort max`
- [ ] 브랜드·색 3개(+포인트)·챕터 수·기능·영상 모델을 담은 주문 + 배포 요청
- [ ] `--subdomain` 규칙에 맞춰 배포 확인
- [ ] 수정 후 반드시 재배포
