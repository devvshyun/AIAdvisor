# 마누스 AI로 모션 그래픽 누구나 만드는 법, 1분 세팅
- 원문: https://lazyowen.com/guides/manus-hyperframes-srt-motion
- 도구·주제: Manus AI · HyperFrames(HeyGen) 스킬 · SRT 자막 기반 모션 그래픽 MP4 생성
- 한 줄 요약: Manus에 HyperFrames 스킬("HTML 비디오 제작")을 한 번 추가해 두면, 자막(.srt)과 프롬프트만으로 문장 시간에 맞춰 장면이 바뀌는 1080×1920 세로 모션 그래픽 MP4를 받는다. (4단계, 약 11분, 2026-10-05 갱신)

## 언제 쓰나
- 자막은 뽑아 놨는데 문장마다 화면이 바뀌는 모션 그래픽을 편집 앱 없이 만들고 싶을 때
- 코딩 없이 자막 파일만으로 세로 영상(릴스류)을 만들고 싶을 때

## 준비물 / 필요 도구
- Manus AI 계정 (브라우저만 필요, 영상은 Manus 클라우드 작업 공간에서 생성, 내 컴퓨터에 설치 없음)
  - 사이트: https://manus.im/ · 앱: https://manus.im/app
  - 스킬 문서: https://manus.im/docs/features/skills
  - 요금: https://manus.im/pricing
- HyperFrames (HeyGen 공개, Apache-2.0, GitHub 스타 54,008): HTML로 장면을 짜 MP4로 렌더하는 오픈소스 영상 도구(편집 앱 아님). Manus 스킬은 그 사용법을 붙여 주는 설명서 묶음.
  - GitHub: https://github.com/heygen-com/hyperframes
  - 스킬 폴더(SKILL.md 포함): https://github.com/heygen-com/hyperframes/tree/main/skills/hyperframes
  - 빠른 시작: https://hyperframes.heygen.com/quickstart
  - 스킬 가이드: https://hyperframes.heygen.com/guides/skills
  - README(라이선스·요금): https://github.com/heygen-com/hyperframes#readme
- 내 컴퓨터에서 직접 돌릴 때만 Node.js 22 이상 필요
- 비용: HyperFrames 렌더당 요금 없음. Manus는 작업마다 크레딧 소모(자막이 길수록 증가), 유료 요금제는 매일 300 리프레시 크레딧, 무료 한도는 가격 페이지 확인
- 용어: 렌더 = 장면 파일을 실제 MP4로 뽑는 작업, 스킬 = AI에게 작업 방법을 알려 주는 설명서 폴더, SRT = 번호·시작/끝 시간·문장 한 줄이 한 블록인 자막 파일, npx = Node 도구를 설치 없이 바로 받아 실행하는 명령

## 단계별 방법
### Quick Start
manus.im/app 에 로그인한 뒤 왼쪽 메뉴 더보기 안에 스킬 항목이 보이면 준비 완료.

### STEP 1. HyperFrames 스킬 추가 (1분)
1. Manus 왼쪽 메뉴 아래쪽 더보기 → 옆 작은 메뉴에서 스킬
2. 스킬 화면 오른쪽 위 검색창에 `hyperframes`
3. 결과 맨 앞의 "HTML 비디오 제작" 카드(만든 곳 Manus, 표지 영문 HTML Video Production) 클릭
4. 열린 창에서 "+ 내 스킬에 추가"
5. 새 작업 입력창에 `/` → 스킬 → 내 스킬 목록에 "HTML 비디오 제작"이 보이면 끝
6. 검색에 안 나오면 스킬 화면의 "GitHub에서 가져오기(Import from GitHub)"에 아래 스킬 폴더 주소 입력
```
https://github.com/heygen-com/hyperframes/tree/main/skills/hyperframes
```
가져온 뒤 `/` → 스킬에 `hyperframes`가 보이는지 확인하고, 이 경우 이후 단계에서 "HTML 비디오 제작" 대신 `hyperframes`를 고른다. 이미 목록에 있으면 건너뜀.
7. 공개 스킬은 안에 명령이 들어 있을 수 있으니, 처음 쓰기 전 Manus에게 "hyperframes 스킬이 무슨 일을 하는지, 위험한 명령이 있는지 검토해 줘"라고 한 번 묻는다.

### STEP 2. 느낌만 적어서 첫 영상 받기 (3분)
새 작업 입력창에서 `/` → 스킬 → HTML 비디오 제작을 고르고 보낸다(따옴표 안 문장만 교체).
```
세로 1080x1920, 5초짜리 모션 그래픽을 만들어 주세요. 흰 배경에 "누구나 만들 수 있어요" 라는 굵은 검은 글자가 아래에서 올라오고, 마지막 1초는 멈춰 있게 해 주세요. 완성되면 MP4 로 렌더해서 보여 주세요.
```
몇 분 뒤 작업 결과에 MP4가 붙으면 성공. 크기·길이·배경·글자·움직임을 한 문장씩 적어야 값대로 나온다.

### STEP 3. 자막 파일로 문장별 타이밍 맞추기 (5분)
1. SRT 준비: 자막 편집 앱에서 내보낸 파일이 있으면 그대로, 없으면 텍스트 편집기에 아래처럼 적어 서식 없는 일반 텍스트로 `test.srt` 저장
```
1
00:00:00,000 --> 00:00:01,800
이런 모션 그래픽

2
00:00:01,800 --> 00:00:03,600
누구나 만들 수 있어요

3
00:00:03,600 --> 00:00:05,400
자막 시간에 맞춰서요
```
2. 새 작업에 `test.srt` 업로드 → `/` → 스킬 → HTML 비디오 제작 선택 → 아래 프롬프트를 붙여넣고 [원하는 느낌] 한 곳만 바꿔 전송
3. 장면별 시작·끝 시간표가 자막 시간과 같게 나오면 성공

프롬프트 뼈대 A. 자막 → 문장별 세로 모션 그래픽
- 목적: .srt 하나로 문장 타이밍에 맞춘 1080×1920 모션 그래픽 MP4 제작 + 렌더 검증
- 역할: HyperFrames 스킬로 자막 타이밍에 맞춘 모션 그래픽을 만들고 결과를 검증하는 담당. 사용자는 편집·코딩 초보
- 슬롯: [내 목표 = 원하는 느낌 한 줄] (예: 흰 배경에 굵은 검은 글자가 아래에서 올라오는 깔끔한 느낌)
- 작업: ① OS·Node.js 버전 확인 ② `npx -y hyperframes --version` 실행 확인(안 되면 필요한 것만 설치), 1080x1920 세로 프로젝트 생성, 자막 블록 1개 = 장면 1개(시작·길이는 자막 시간 그대로, 전체 길이 = 마지막 자막 끝 시간), 화면 글자는 자막 문장 그대로, 한글 글꼴은 `@font-face`로 직접 삽입 ③ `npx -y hyperframes lint`로 오류 제거 후 `npx -y hyperframes render -o out.mp4` 렌더, `ffprobe -v error -show_entries format=duration -of csv=p=0 out.mp4`로 길이 측정 ④ 초보자용 결과 설명과 다음에 느낌을 바꾸는 요청 문장 한 가지 안내
- 제약: 자막 문장·시간 변경 금지, 장면 임의 병합/분할 금지, 계정·키 값 출력 금지, 업로드 파일 덮어쓰기 금지(새 폴더에만 출력)
- 출력: 실행 명령, HyperFrames 버전, 장면별 시작·끝 시간표, out.mp4, 남은 오류
- 검증: lint 결과 `0 error(s)`, ffprobe 길이 = 마지막 자막 끝 시간(예: 5.4초 → 5.400000). 실패 시 완료 보고 금지, 실패 명령·원인·다음 조치 보고

### STEP 4. 결과 확인하고 다시 요청 (2분)
영상을 재생하며 문장이 바뀌는 순간 화면도 바뀌는지 본다. 숫자 확인은 Manus 작업 기록에서 하며(프롬프트대로면 Manus가 이미 실행), 아래는 직접 입력하지 않는다.
```bash
npx -y hyperframes --version
npx -y hyperframes lint
```
`0.8.91` 같은 버전과 마지막 줄 `0 error(s)`가 나오면 성공(경고 warning은 남아도 렌더됨).
```bash
npx -y hyperframes render -o out.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 out.mp4
```
`Render complete`가 뜨고 길이 값이 마지막 자막 끝 시간과 같아야 한다(예시 자막이면 5.400000).

## 핵심 팁 · 주의사항
- ❌ "멋진 모션 그래픽 만들어줘" → ✅ 크기, 길이, 배경, 글자, 움직임을 한 문장씩 (느낌만 던지면 길이·비율이 매번 다름)
- ❌ "자막에 맞춰서 적당히 만들어줘" → ✅ "자막 블록 하나를 장면 하나로, 시작과 길이는 자막 시간 그대로"
- 자막이 길수록 한 번에 드는 크레딧 증가
- 공개 스킬은 안에 명령이 있을 수 있으니 사용 전 검토

## 문제 해결
- 장면이 한쪽으로 몰림: "자막 시간을 한 칸도 바꾸지 말고 다시 렌더해 주세요"
- 느낌 변경: 목표 칸 한 줄만 고쳐 새로 요청
- 한글이 기본 글꼴로 나오거나 글꼴 오류: 프롬프트의 `@font-face` 문장이 남아 있는지 확인 후 재전송
- 장면은 맞는데 말과 어긋남: 자막 파일의 시간부터 수정 후 재전송
- 스킬 검색에 안 나옴: STEP 1-6의 GitHub 가져오기

## 바로 쓰는 체크리스트
- [ ] Manus에 "HTML 비디오 제작" 스킬 추가(`/` → 스킬에서 노출 확인)
- [ ] 텍스트 전용 5초 테스트로 MP4 생성 확인
- [ ] `test.srt` 준비 후 업로드, [내 목표] 한 줄만 바꿔 실행
- [ ] `0 error(s)` 및 영상 길이 = 마지막 자막 끝 시간 확인
- [ ] 크레딧 사용량 확인
