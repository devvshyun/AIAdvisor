# 구글이 무료로 푼 AI 도구 15개
- 원문: https://lazyowen.com/guides/google-aitool-free-15
- 도구·주제: Google AI 도구 모음 · 비용 절약 / 무료 도구
- 한 줄 요약: 구글이 열어 둔 무료(개인 무료 등급 포함) AI 도구 15개를 한 줄 설명과 주소로 정리하고, 내 상황에 맞는 것을 골라 열어 보고 접근 가능 여부까지 걸러 내는 방법. (2026-08-15 공개, 읽는 데 11분, 따라 하면 약 23분, STEP 5개)

## 언제 쓰나
- 디자인·마케팅·코딩 도구를 따로 결제하느라 매달 돈이 나가는데, 구글의 무료 도구 이름을 몰라 못 쓰고 있을 때
- 유료 도구 없이 화면 디자인·홍보물·자동화·자료 요약·학습·코딩을 시도해 보고 싶을 때

## 준비물 / 필요 도구
- 구글 계정 (15개 중 13개는 설치 없이 로그인만, 설치가 필요한 것은 2개: 하나는 프로그램 내려받기, 하나는 명령어 한 줄. 모두 Antigravity 관련)
- 공식 목록: Google Labs https://labs.google/ (실험 중인 AI 도구 모음)
- 터미널(macOS 터미널 앱 / 윈도우 PowerShell): 설치형 도구용
- 용어: 에이전트 = 사람이 한 단계씩 지시하지 않아도 스스로 순서를 정해 일하는 AI, 시안 = 확정 전에 보여 주는 초안 디자인

| 도구 | 주소 | 한 줄 설명 | 분류 |
|---|---|---|---|
| Stitch | https://stitch.withgoogle.com/ | 한 줄 설명이나 손그림으로 앱·웹 화면 디자인과 코드 생성 | 화면 디자인 |
| Pomelli | https://labs.google.com/pomelli/about | 사이트 주소를 넣으면 브랜드 톤을 읽어 SNS 홍보 콘텐츠 생성 | 마케팅 |
| Opal | https://opal.google/ | 코딩 없이 말로 여러 단계를 이어 붙여 자동화 미니앱 제작 | 자동화 |
| Antigravity | https://antigravity.google/ | 에이전트가 여러 파일을 고치고 검사까지 하는 개발 프로그램 | 코딩 |
| Mixboard | https://labs.google.com/mixboard/welcome | AI 이미지를 만들고 모아 무드보드 완성 | 이미지 |
| Disco | https://labs.google/disco | 열려 있는 브라우저 탭을 하나의 앱처럼 묶음 (현재 대기 신청 단계) | 브라우저 |
| Gemini Notebook (NotebookLM) | https://notebooklm.google/ | 넣은 문서·영상 안에서만 답하고 출처 표시 | 자료 정리 |
| Learn Your Way | https://learnyourway.withgoogle.com/ | 아무 주제를 맞춤 강의·퀴즈·오디오 설명으로 변환 | 학습 |
| Flow Music | https://www.flowmusic.app/ | 대화하듯 요청하면 곡과 뮤직비디오 생성 | 음악 |
| Google AI Studio | https://aistudio.google.com/ | 브라우저에서 AI 앱 시제품 제작·실행 | 시제품 |
| Jules | https://jules.google/ | 깃허브 연동으로 버그 수정·기능 추가 후 결과 업로드 | 코딩 |
| Gemini CLI | https://github.com/google-gemini/gemini-cli | 터미널용 오픈소스 AI 도구 (개인 무료 등급 종료) | 코딩 |
| Code Wiki | https://codewiki.google/ | 깃허브 저장소를 읽어 설명 문서와 그림으로 정리 | 코드 이해 |
| Firebase Studio | https://firebase.studio/ | 브라우저에서 앱·데이터·서버까지 개발 | 앱 개발 |
| Gemini Code Assist | https://codeassist.google/ | 에디터 안 코드 작성 보조 (개인 무료 등급 종료) | 코딩 |

- 추가 링크: Antigravity 다운로드 https://antigravity.google/download , 요금 https://antigravity.google/pricing , CLI 저장소 https://github.com/google-antigravity/antigravity-cli

## 단계별 방법
### 프롬프트 뼈대 A. 도구 선택·접속 확인 위임 (Gemini에 붙여넣기, 선택)
- 목적: 15개 중 내 상황에 맞는 도구 최대 3개를 고르고 실제로 열리는지 확인
- 역할: 구글 무료 AI 도구 추천·접속 확인 담당. 사용자는 한 번도 안 써 본 상태
- 슬롯: [운영체제(예: 윈도우 11)], [내가 하는 일(예: 1인 쇼핑몰)], [해결하고 싶은 것 한 줄(예: 인스타 홍보 문구가 막힘)]
- 작업: ① 목록에서 최대 3개 선택 + 이유 한 줄씩 ② 지금 내 계정으로 바로 쓸 수 있는지/대기 신청이 필요한지 확인 ③ 첫 도구에 넣을 첫 요청 문장을 내 상황에 맞게 완성 ④ 개발 경험 없는 사람 눈높이로 사용법 안내
- 제약: 유료 결제 필요한 도구 추천 금지, 목록에 없는 도구 날조 금지, 비밀번호·결제 정보 요구·저장 금지
- 출력: 도구 이름·주소, 선택 이유, 사용 가능 여부, 복사해서 쓸 첫 요청 문장
- 검증: 각 공식 주소의 접속 여부를 실제 확인. 접속 불가·대기 신청이면 완료 보고 금지하고 막힌 도구·이유·대체 도구 제시

### Quick Start
1. 설치 불필요 13개: 브라우저에 아래 주소를 넣고 구글 계정으로 로그인. 로그인 버튼이나 입력창이 보이면 성공. 안 열리면 브라우저 언어를 영어로 바꿔 재시도.
```
https://stitch.withgoogle.com
https://labs.google.com/pomelli
https://opal.google
https://labs.google.com/mixboard
https://notebooklm.google
```
2. 설치형(맥·리눅스): 설치 진행 표시 후 프롬프트가 돌아오면 성공, 이어서 `agy` 입력 시 도구 실행
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### STEP 1. 내 상황에 맞는 도구 고르기 (2분)
한 번에 여러 개를 열면 이름만 남고 손에 익지 않으니 지금 필요한 것만 고른다.
| 지금 상황 | 먼저 열 도구 | 이유 |
|---|---|---|
| 앱·웹 화면을 그려야 함 | Stitch | 한 줄만 적어도 화면이 나옴 |
| 올릴 홍보 글·이미지가 없음 | Pomelli | 사이트 주소만 넣으면 초안 작성 |
| 매번 같은 순서로 반복하는 일 | Opal | 코딩 없이 단계를 이어 붙임 |
| 코드를 고쳐야 하는데 버거움 | Antigravity | 에이전트가 고치고 검사까지 |
| 읽을 자료가 밀려 있음 | Gemini Notebook | 넣은 자료 안에서만 답 |
| 새 주제를 처음부터 배워야 함 | Learn Your Way | 주제를 내 강의로 변환 |
| 영상에 넣을 음악 필요 | Flow Music | 대화로 곡 생성 |

### STEP 2. 로그인만으로 쓰는 도구 열기 (5분)
1. 고른 도구 주소를 열고 구글 계정으로 로그인(예: 화면 디자인이면 https://stitch.withgoogle.com/)
2. Stitch 동작 확인용 요청(성공하면 화면 디자인 시안이 그림으로 나옴, 마음에 안 들면 같은 창에서 수정 요청)
```
카페 예약 화면을 만들어 주세요.
날짜 선택, 인원 선택, 예약 버튼이 있으면 됩니다.
색은 따뜻한 갈색 계열로 해 주세요.
```
3. Pomelli는 입력창에 사이트 주소만 넣으면 됨(성공하면 사이트에서 읽은 브랜드 정보와 홍보 문구 후보)
```
https://내-사이트-주소.com
```

### STEP 3. 자료를 넣어서 쓰는 도구 열기 (5분)
1. https://notebooklm.google/ 접속 → 새 노트 → PDF나 유튜브 주소 추가
2. 자료를 다 넣은 뒤 요청(성공하면 요약과 출처 표시가 붙고, 출처를 누르면 원문 해당 부분으로 이동)
```
넣은 자료만 근거로 답해 주세요. 핵심 내용을 다섯 줄로 정리하고, 각 줄이 어느 자료의 어느 부분에서 나왔는지 표시해 주세요.
```
3. 새 주제를 배우는 중이면 https://learnyourway.withgoogle.com/ 에서 주제를 고르면 강의·퀴즈·오디오 설명으로 변환
(결과 품질은 넣은 자료에 좌우됨)

### STEP 4. 설치가 필요한 도구 깔기 (8분, 코드를 다루는 사람만)
1. Antigravity 데스크톱: https://antigravity.google/download 에서 OS에 맞는 파일 선택. 개인 사용은 구독 없이 무료이며 주 단위 사용량 한도가 있음.
2. CLI(맥·리눅스): 설치 로그 후 프롬프트가 돌아오면 성공
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```
윈도우 PowerShell
```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```
3. 확인: 도구 화면과 무엇을 도울지 묻는 입력창이 뜨면 성공
```bash
agy
```
4. 깃허브를 쓴다면 https://jules.google/ : 저장소를 연결하고 할 일을 적으면 에이전트가 코드를 고쳐 올림. 무료로 하루 15개 작업, 동시 3개까지.
5. 남의 코드를 읽어야 하면 https://codewiki.google/ 에 저장소 주소를 넣어 구조 설명과 그림을 받음.

### STEP 5. 지금 상태 확인하고 헛걸음 줄이기 (3분)
실험 단계 도구는 나라·계정에 따라 화면이 다르다. 주소를 열었을 때:
| 화면 | 뜻 | 할 일 |
|---|---|---|
| 로그인 버튼이나 입력창 | 지금 바로 사용 가능 | 로그인하고 STEP 2로 |
| 대기 신청 양식 | 순서 대기 | 신청서만 넣고 다음 도구로 |
| 안내 문구만 있는 페이지 | 개인 무료 지원 종료 | 대체 도구 사용 |
- Disco는 현재 대기 신청 단계: https://labs.google/disco 에서 신청.
- Gemini Code Assist와 Gemini CLI의 개인 무료 등급은 2026-06-18 종료. 같은 일은 Antigravity가 이어받으니 코딩 도구가 필요하면 그쪽을 사용(회사 유료 라이선스는 유지).

## 핵심 팁 · 주의사항
- 한 번에 여러 도구를 열지 말고 상황별 1~3개만, 여기서 성공 경험을 하나 만들기
- Antigravity 개인 무료는 주간 사용량 한도가 있음, Jules 무료는 하루 15작업/동시 3개
- 실험 단계 도구라 지역·계정별로 화면과 이용 가능 여부가 다를 수 있음
- 결과가 엉뚱하면 요청이 너무 짧은 것: 원하는 것, 쓸 곳, 피할 것을 각각 한 줄씩 적기

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| 주소를 넣어도 페이지가 안 열림 | 서비스가 아직 열리지 않은 지역 | 브라우저 언어를 영어로 바꾸고 재시도 |
| 로그인은 됐는데 화면이 비어 있음 | 계정 연령 확인 미완료 | 구글 계정 설정에서 연령 확인 |
| 무료인데 결제를 요구 | 무료 한도 소진 | 하루 뒤 재확인하거나 다른 도구 사용 |
| `command not found` | 설치가 끝나지 않음 | 터미널을 완전히 껐다 켜기 |
| 결과가 엉뚱함 | 요청 문장이 너무 짧음 | 원하는 것·쓸 곳·피할 것을 한 줄씩 |

## 바로 쓰는 체크리스트
- [ ] 구글 계정으로 로그인 가능한가
- [ ] 상황에 맞는 도구 1~3개 선택
- [ ] 각 도구의 상태(바로 사용/대기/종료) 확인
- [ ] Stitch 또는 Pomelli로 첫 결과 확인
- [ ] Gemini Notebook에 자료를 올려 출처 달린 요약 받기
- [ ] (코딩 시) Antigravity 설치 후 `agy` 실행 확인, 필요시 Jules·Code Wiki
