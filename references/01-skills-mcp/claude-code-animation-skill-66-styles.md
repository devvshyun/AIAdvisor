# 클로드 코드로 66가지 스타일의 바이럴 애니메이션 만드는 법
- 원문: https://lazyowen.com/guides/claude-code-animation-skill-66-styles
- 도구·주제: Claude Code (lemo-opuscar 스킬) · 코드 기반 영상/애니메이션 생성
- 한 줄 요약: lemo-opuscar 스킬 하나를 설치하면 클로드가 스토리·나레이션·음악·효과음을 만들고 영상을 코드로 한 프레임씩 렌더링한다(영상 생성 AI·스톡 영상 미사용). 66가지 스타일 중 고르거나 나만의 스타일을 만들 수 있다.

## 언제 쓰나
- 30~60초짜리 설명/숏폼 영상을 66가지 스타일 중 골라 자동 제작하고 싶을 때
- 릴스·쇼츠용 세로 영상(1080×1920)이 필요할 때
- 브랜드 로고/컬러를 담은 나만의 스타일을 저장해 재사용하고 싶을 때

## 준비물 / 필요 도구
- Claude Code + 유료 요금제(Pro 이상, 무료 요금제 불가) — https://code.claude.com/docs/en/setup
- Node 20 이상 — https://nodejs.org/
- ffmpeg 7 이상 — https://ffmpeg.org/download.html
- Python 3.11 이상 또는 uv — https://docs.astral.sh/uv/ (맥 기본 Python이 3.11 미만이어도 uv가 있으면 통과)
- Homebrew(맥, 도구 일괄 설치용)
- lemo-opuscar (LemoLab 제작, GitHub 스타 약 1.2만, 코드·문서 MIT)
  - GitHub: https://github.com/lemomo-ai/lemo-opuscar
  - 공식 사이트·데모 갤러리: https://lemomo-ai.github.io/lemo-opuscar/
  - 스타일 목록: https://github.com/lemomo-ai/lemo-opuscar/blob/main/styles/README.md
  - 나만의 스타일 안내: https://github.com/lemomo-ai/lemo-opuscar/blob/main/MY-STYLES.md
  - 문제 신고: https://github.com/lemomo-ai/lemo-opuscar/issues
- 환경: 맥(애플 실리콘)에서 개발, 윈도우는 WSL에서 사용
- 용어: 스킬 = 클로드 코드에 새 작업 방법을 가르치는 설명서 묶음(여기서는 플러그인 형태). 마켓플레이스 = 플러그인을 받는 목록.

## 단계별 방법
### 프롬프트 뼈대 A. 설치 점검 위임용 (선택)
- 목적: 환경 확인부터 스킬 설치·검증까지 Claude Code에 맡기기. 터미널에서 `claude` 실행 후 첫 메시지로 사용.
- 역할: lemo-opuscar 설치·연결 확인 담당
- 슬롯: [내 첫 영상 주제] (예: 동네 빵집의 하루를 수채화로)
- 작업 순서: 버전 5종 직접 확인 → 빠진 프로그램 보고, 스킬이 없을 때만 marketplace add / plugin install 실행 → `claude plugin list`로 검증 → 스킬 설명과 첫 영상 주문 문장 안내
- 제약: brew 같은 시스템 설치 명령은 실행 전 먼저 묻기, 비밀키 출력 금지, 기존 파일 덮어쓰기 금지
- 출력: 실행 명령, 확인된 버전, 설치된 스킬 이름, 남은 오류
- 검증: `lemo-opuscar@lemolab` 과 `Status: ✔ enabled`가 보여야 완료, 실패하면 완료 보고 금지

### Quick Start
```bash
claude plugin marketplace add lemomo-ai/lemo-opuscar
claude plugin install lemo-opuscar@lemolab
```
성공 시 `✔ Successfully installed plugin: lemo-opuscar@lemolab (scope: user)`.

### STEP 1. 준비물 확인 (3분)
1. 버전 확인
```bash
claude --version
node --version
ffmpeg -version
python3 --version
uv --version
```
| 확인할 것 | 통과 기준 |
|---|---|
| Node | v20 이상 |
| ffmpeg | ffmpeg version 7 이상 |
| Python 또는 uv | Python 3.11 이상, 아니면 uv 버전 숫자 |

2. 하나라도 빠졌으면(맥) 한 줄로 설치, 이미 있으면 건너뜀. 확인 명령을 다시 실행해 버전이 나오는지 본다. 홈브루가 없으면 위 공식 링크에서 각각 받는다.
```bash
brew install node ffmpeg uv
```

### STEP 2. 스킬 설치 (2분)
1. 마켓플레이스 등록 + 설치 (첫 줄이 가게 등록, 둘째 줄이 설치)
```bash
claude plugin marketplace add lemomo-ai/lemo-opuscar
claude plugin install lemo-opuscar@lemolab
```
`✔ Successfully added marketplace: lemolab` 과 `✔ Successfully installed plugin: lemo-opuscar@lemolab (scope: user)` 두 줄이 나오면 성공.
2. 설치 확인
```bash
claude plugin list
```
`lemo-opuscar@lemolab` 아래 `Status: ✔ enabled`가 보이면 끝. 앞에 나오는 "SSH not configured" 안내는 오류가 아니다.
3. 클로드 코드가 켜져 있었다면 종료 후 재실행.
4. 첫 주문 때 스킬이 스타일 설명서와 도구를 `~/lemo-opuscar`에 받고 렌더링 패키지를 설치한다(처음 한 번 몇 분).
5. 영상 제작 시 `/model`로 Opus 5.5 선택(스타일이 이 모델에 맞춰 제작됨).

### STEP 3. 스타일 고르고 첫 영상 주문 (5분)
1. 영상 전용 폴더에서 시작(프로젝트 폴더가 실행한 폴더 안에 생김)
```bash
mkdir -p ~/films && cd ~/films && claude
```
직접 녹음한 나레이션 파일은 주문 전에 이 폴더에 넣어 둔다.
2. 스타일 선택: 11개 분류 총 66가지
| 분류 | 개수 | 예시 |
|---|---|---|
| 손그림·회화 | 8 | Whiteboard Explainer, Watercolor Brush, Chalkboard |
| 편집·다큐 | 8 | Caption News, Broadcast News Package |
| 실증 영상 | 8 | Satellite Briefing, Exploded Teardown |
| 정보·발표 | 8 | Data Storytelling, Dark Tech Keynote |
| 그래픽·타이포 | 7 | Swiss Motion Graphics, Blueprint |
| 재질·3D | 7 | Brick Toy, Tilt-Shift Miniature |
| 인쇄·판화 | 6 | Risograph Print, Woodcut Print |
| 카툰·애니메 | 4 | 1930s Rubber Hose Cartoon, 80s Cel Anime |
| 동양 전통 | 4 | Ukiyo-e, Shadow Puppetry |
| 게임 | 4 | 16-bit Pixel RPG, HD-2D |
| 영화·시대 | 2 | 1920s Silent Film |
3. 주문 예시(스타일 영어 이름 + 주제 한 줄 + 길이 + 비율을 한 문장에)
```
Watercolor Brush 스타일로 우리 동네 빵집의 하루를 40초 영상으로 만들어 줘. 세로 1080×1920 으로, 나레이션은 films 폴더에 넣어 둔 내 녹음 파일을 쓸게. 스토리보드 먼저 보여 줘.
```
4. 클로드가 한 번에 묻는 3가지: 주제에서 못 정한 것 / 내 목소리·음악·소재 유무 / 스토리보드를 먼저 볼지. 답하면 스토리 → 나레이션 → 음악·효과음 → 프레임 렌더링 → 믹싱까지 이어진다.
5. 스타일을 모를 때
```
/lemo-opuscar:lemo-opuscar 한국어로 진행해 줘
```
6. 결과 파일: `<이름>.mp4`·`poster.jpg`(영상·표지), `<이름>.srt`(자막), `TREATMENT.md`(스토리), `CREDITS`(외부 음악·폰트 등 소재와 라이선스)

### STEP 4. 나만의 스타일 만들기 (30분)
1. 방법 두 가지: (a) 라이브러리 스타일을 내 버전으로 바꾸기(컬러·로고·분위기), (b) 빈 페이지에서 시작(좋아하는 그림·영상을 레퍼런스로 주면 가장 가까운 스타일을 근거와 함께 골라 줌). 공식 예시는 Swiss Motion Graphics의 격자·박자·글자는 두고 도형만 점토·플라스틱·펠트 재질로 바꿔 "Material Grid"로 저장.
2. 준비: `logo.png`와 레퍼런스 이미지 `refs` 폴더를 films 폴더에 넣고, films 폴더에서 클로드 코드를 실행.
3. 주문 예시
```
Swiss Motion Graphics 스타일을 내 버전으로 바꾸고 싶어. 릴스용 세로 영상에 쓸 거고, 브랜드 컬러는 #FF6A2B, 로고는 films 폴더의 logo.png 야. 레퍼런스 이미지는 films 폴더 안 refs 폴더에 넣어 뒀어.
```
4. 진행 5단계: ① 추천 답이 맨 위에 있는 질문 약 10개에 답("알아서 해 줘"라고 하면 나머지는 추천대로) ② 바꿀 부분의 전/후 요약 확인·동의 ③ 코드로 그린 한 장면을 원본 스타일과 나란히 비교 ④ 15~30초 데모 영상(음악·효과음 포함) 수령 ⑤ 마음에 들면 내 스타일로 저장.
5. 저장 위치 `~/lemo-my-styles/<이름>/`. 다음 영상에서는 이름으로 호출("내 오렌지 스위스 스타일로 30초 영상 만들어 줘"). 스타일 선택 목록 맨 위에 내 스타일이 나오고, 스킬 업데이트·삭제 후에도 폴더는 남는다.

### 업데이트와 삭제
```bash
claude plugin marketplace update lemolab && claude plugin update lemo-opuscar@lemolab
```
업데이트 후 클로드 코드 재실행. `~/lemo-opuscar` 스타일 설명서는 다음 영상 제작 때 스스로 갱신된다. 최신이면 "is already at the latest version".
```bash
claude plugin uninstall lemo-opuscar@lemolab
```
`✔ Successfully uninstalled plugin: lemo-opuscar (scope: user)`. 받아 둔 라이브러리까지 지우려면 `~/lemo-opuscar`를 직접 삭제. `~/lemo-my-styles/`는 원할 때만 직접 삭제.

## 핵심 팁 · 주의사항
- 비용: 스킬은 무료지만 영상 한 편에 클로드 코드 사용량이 많이 들어 요금제 한도 안에서 써야 함
- 소요: 한 편에 30~60분 → 처음엔 30~45초짜리로 시작
- 화면 비율 기본은 가로 1920×1080, 릴스·쇼츠는 주문에 "세로 1080×1920" 명시
- 한국어 나레이션: 기본 음성은 영어·중국어. 직접 녹음한 파일을 films 폴더에 넣고 "내 녹음 파일을 쓸게"라고 적기
- ❌ 클로드 대화창에 "lemo-opuscar 설치해 줘"만 적기 → ✅ 두 줄을 터미널에 붙여넣고 `claude plugin list`로 눈으로 확인
- ❌ "애니메이션 하나 만들어 줘" → ✅ 스타일 영어 이름 + 주제 + 길이(초) + 화면 비율
- ❌ "내 브랜드 느낌으로 알아서"(로고·컬러 파일 없이) → ✅ 기준 스타일, 사용처, 브랜드 컬러 값, 로고·레퍼런스 위치를 한 번에
- 공유 전 `CREDITS`로 음악·폰트 등 외부 소재 라이선스 확인(영상 자체는 내 것이며 LemoLab 출처 표기 불필요)

## 바로 쓰는 체크리스트
- [ ] Pro 이상 요금제 + Node 20+/ffmpeg 7+/Python 3.11+(또는 uv) 확인
- [ ] 마켓플레이스 등록 → 스킬 설치 → `claude plugin list`에서 enabled 확인
- [ ] `/model`로 Opus 5.5 선택
- [ ] `~/films`에서 `claude` 실행, 녹음 파일·logo.png·refs 배치
- [ ] 스타일명·주제·길이·비율을 넣어 주문(처음엔 30~45초)
- [ ] 한국어 나레이션은 직접 녹음 파일 지정
- [ ] CREDITS 확인 후 공유
- [ ] 마음에 드는 커스텀 스타일은 `~/lemo-my-styles/`에 저장
