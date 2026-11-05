# 오퍼스 프롬프트 하나로 15초 모션 영상
- 원문: https://lazyowen.com/guides/claude-opus-motion-design-prompts
- 도구·주제: Claude Code(Opus 5.5) · ffmpeg · 코드로 15초 모션그래픽 MP4 생성
- 한 줄 요약: Claude Code를 `--model claude-opus-5-5 --effort max`로 열어 영어 프롬프트 하나로 15초 모션 쇼릴 코드를 만들게 하고 ffmpeg로 MP4 렌더한다. (원문 2026-10-05 갱신, 읽는 데 10분, 4단계)

## 언제 쓰나
- 영상 편집 툴 없이 프롬프트만으로 모션 디자인 쇼릴/UI 마이크로 인터랙션 영상을 만들고 싶을 때
- 카드뉴스 속 모션 영상에 쓰인 영어 원문 프롬프트(카드엔 한국어 번역만 있음)를 얻고 싶을 때
- Claude Code는 영상 생성 AI가 아니라, 클로드가 애니메이션을 코드로 짜고 그 화면을 영상 파일로 렌더하는 방식

## 준비물 / 필요 도구
- Claude Code (https://claude.com/claude-code , 퀵스타트 https://code.claude.com/docs/en/quickstart , 문서 https://code.claude.com/docs)
- Claude Opus 5.5 (https://www.anthropic.com/claude-opus-5-5), 모델/추론 강도 설정 https://code.claude.com/docs/en/model-config
- ffmpeg(별도 설치, 무료. ffprobe 포함) — 없으면 STEP 4에서 Claude에게 설치 맡김(허락 후)
- 구독: Pro/Max/Team/Enterprise 또는 Claude Console 계정 (요금 https://claude.com/pricing)
- 선택: GPT-6 아스트라 비교용. 채팅 모델 목록에서 "GPT-6 Pro"로 보임. Pro/Business/Enterprise는 채팅에서, Plus는 ChatGPT의 Work·Codex에서 사용 (https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt)
- 환경: macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+, 메모리 4GB+
- 터미널: 맥은 Spotlight에서 '터미널', 윈도는 PowerShell

## 단계별 방법
**Quick Start — 설치** (이미 있으면 건너뜀)
```
curl -fsSL https://claude.ai/install.sh | bash
```
(macOS/Linux) Windows PowerShell:
```
irm https://claude.ai/install.ps1 | iex
```
새 터미널에서 `claude --version` 시 버전 뒤에 `(Claude Code)`. 못 찾으면 창을 닫고 새로 열기.

1. **STEP 1 오퍼스 5.5를 max로 열기 (2분)**
   ```
   claude --version
   ffmpeg -version
   mkdir motion-reel
   cd motion-reel
   claude --model claude-opus-5-5 --effort max
   ```
   - 추론 강도(effort)는 low~max 5단계. 첫 실행: ① 브라우저 로그인(한 번만) ② 폴더 신뢰 확인 수락 ③ 파일 생성·명령 실행 권한 질문엔 내용을 읽고 괜찮을 때만 Yes. `max`는 이번 세션에만 적용.
   - ❌ `claude`만 치고 바로 붙여넣기 → 따로 안 정하면 Opus 5.5는 medium. ✅ `--effort max`로 카드뉴스 1·6번 영상과 같은 조건.
2. **STEP 2 한 줄 쇼릴 프롬프트 (1·3·4·6번 영상)**: 영어 원문을 그대로 붙여넣기. (설정: 1번 Opus 5.5 Max, 3번 Opus 5.5 Max vs GPT-6 아스트라 Max, 4번 표기 없음, 6번 Opus 5.5 MAX)
   - 프롬프트 뼈대(영어 한 줄): "너는 대단한 모션 디자이너다" 입증용 **15초 역동적 모션그래픽 영상**, 이력서에 붙이는 **쇼릴**처럼, 마지막에 "Go all out"(전부 쏟아부어). 슬롯 없음, 길이·용도·태도 세 조건만. 시작 어구는 `make a dynamic 15-second motion graphics video ...`.
   - claude.ai 채팅창에도 붙일 수 있지만 MP4가 필요하면 Claude Code. 3번처럼 비교하려면 같은 원문을 GPT-6 아스트라에도 넣고, 둘을 MP4로 비교하려면 Codex에서 STEP 4 렌더 요청을 이어서 보냄.
   - ❌ "멋진 모션 영상 만들어줘"(길이·용도 없음) → ✅ 원문 한 줄 그대로. 같은 원문도 매번 결과가 다르니 마음에 안 들면 재실행.
3. **STEP 3 연출 지시형 프롬프트 (5번 영상)**: 한 줄 결과가 밋밋할 때 교체. 한 줄 원문에 없는 지시 4가지 추가.
   - 프롬프트 뼈대: 역할=세계 최고 수준 모션 디자이너, 산출물=15초 이력서 릴. 요구: 역동적이고 자신감 있게 / **첫 1초 강한 훅** / 타이포그래피·도형 놀이·카메라 움직임·색 전환을 서로 다른 기법으로 순서대로 쌓기 / **깔끔하고 기억에 남는 마지막 프레임** / 음악에 맞춰 자른 듯한 속도감 / 마지막은 "Go crazy"(마음껏).
   - UI 애니메이션 예(한국어 장면 묘사 방식): 흰 정사각형 캔버스 가운데 검정 알약형 `Generate` 버튼 → 커서가 누르면 부드럽게 늘어나 `Day / Week / Month` 토글로 변했다가 버튼으로 복귀하는 15초 UI 마이크로 인터랙션, After Effects 없이 전부 코드로.
4. **STEP 4 MP4로 뽑고 말로 고치기 (5분)**: 코드만 만들고 멈췄으면 같은 대화에서 렌더 요청.
   - 프롬프트(요지): 방금 만든 애니메이션을 1920x1080, 30fps, 15초 MP4 `showreel.mp4`로 렌더. 필요한 도구가 없으면 무엇을 설치할지 먼저 알리고 허락 후 설치. (1920x1080은 16:9)
   ```
   ffprobe -v error -show_entries format=duration -of csv=p=0 showreel.mp4
   ```
   - `15.000000`처럼 15 안팎이면 정상. 장면 수(타이포·도형·카메라가 다른 장면인지), 마지막 프레임에서 글자 잘림·겹침 확인.
   - 클로드가 화면 캡처용 브라우저 도구 설치를 제안하면 무엇인지 먼저 묻고 괜찮을 때만 허락.
   - ❌ "다시 만들어줘"(좋던 장면까지 바뀜) → ✅ "세 번째 장면 전환만 0.5초 느리게 바꿔 줘"처럼 고칠 곳만 지정(영상이 코드라서 가능).

**통합 위임 프롬프트 뼈대(Claude Code 첫 메시지)**: 역할=모션그래픽 코드 제작·MP4 렌더 검증 담당, 맥락=개발 초보자·빈 폴더·렌더 도구 미설치 가능. 슬롯 `쓸 프롬프트 = <STEP 2·3에서 고른 영어 원문 통째로>`(OS·셸·도구는 묻지 말고 직접 확인). 작업: ① `claude --version`/`ffmpeg -version` 실행·표시 ② ffmpeg 없으면 설치 방법을 먼저 알리고 허락 후 설치 ③ 쓸 프롬프트를 한 글자도 바꾸지 말고 영상 코드로 만들어 1920x1080·30fps·15초 `showreel.mp4` 렌더 ④ 장면 수와 한 장면만 고치는 법을 초보자 눈높이로 설명. 제약: sudo·전역 설치·설정 수정 전 질문, 폴더 밖 파일 생성/덮어쓰기 금지, 비밀키 출력 금지. 출력: 명령·버전·파일 목록·영상 길이·남은 오류. 검증: 위 `ffprobe` 결과가 15 안팎. 실패 시 완료 보고 금지.

## 핵심 팁 · 주의사항
- 비용/한도: max는 오래 걸리고 사용량을 많이 써서 구독 한도에 빨리 닿을 수 있음.
- 같은 프롬프트도 결과가 매번 다름 → 재실행 활용.
- 시스템 변경(설치) 전에는 Claude가 먼저 묻게 하고, 폴더 안에서만 작업.
- 클로드 코드는 앤트로픽 이용약관을 따르는 상용 제품.

## 바로 쓰는 체크리스트
- [ ] `claude --version`, `ffmpeg -version` 확인 (ffmpeg 없으면 렌더 단계에서 설치)
- [ ] 빈 폴더 `motion-reel`에서 `claude --model claude-opus-5-5 --effort max`
- [ ] 로그인·폴더 신뢰 처리
- [ ] 영어 원문 프롬프트 붙여넣기(밋밋하면 연출 지시형으로 교체)
- [ ] 1920x1080 / 30fps / 15초 / `showreel.mp4` 렌더
- [ ] ffprobe로 길이 확인, 장면·마지막 프레임 점검
- [ ] 장면별로 구체적 수정 요청
