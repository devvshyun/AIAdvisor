# 맥용 자비스 아티커스(Atticus) 설치하고 세팅하는 법
- 원문: https://lazyowen.com/guides/atticus-mac-voice-assistant-setup
- 도구·주제: Atticus (macOS) + Claude Code · 음성 비서 / 맥 제어 (자동화, 4분 읽기, 2026-10-28 공개)
- 한 줄 요약: 단축키를 누른 채 영어로 말하면 앱 실행, 창 이동, 파일 찾기를 해 주는 무료 오픈소스(MIT) 앱을 명령 한 줄로 설치하고 권한을 세팅한다.

## 언제 쓰나
- 맥을 음성 명령으로 조작하고 싶을 때 (맥용 자비스)

## 준비물 / 필요 도구
- macOS 26 이상 (사과 메뉴 → 이 Mac에 관하여에서 확인)
- Atticus: https://github.com/SaarthurR/atticus-mac (MIT 오픈소스, 무료) · 다른 AI 연결(로컬 모델): https://github.com/SaarthurR/atticus-mac#use-a-local-model
- AI 연결: 기본은 Claude Pro 또는 Max 구독 + Claude Code (https://claude.com/claude-code). Devin·Pi나 로컬 모델로도 연결 가능하나 로컬 모델 연결 때도 Claude Code는 필요.
- 애플 커맨드라인 도구(앱 빌드용 기본 개발 도구): 없으면 설치 중 안내 창이 자동으로 뜸

## 단계별 방법
### Quick Start. 설치
1. `⌘ command + space` → "터미널" 검색해 열기
2. 아래 명령 붙여넣고 return:
```bash
curl -fsSL https://raw.githubusercontent.com/SaarthurR/atticus-mac/main/install.sh | bash
```
   (맥 확인 → 다운로드 → 앱 빌드 → 실행까지 자동)
3. 설치가 끝나면 Atticus 셋업 창이 저절로 열림.
- `Atticus needs macOS 26 or later.` → 맥 버전이 낮은 것.
- 커맨드라인 도구 설치 창이 뜨면 설치 → 끝난 뒤 같은 명령 한 번 더 실행.

### 세팅
1. 셋업 창이 AI 연결(기본 Claude 구독)을 확인. 로그인 안 돼 있으면 여기서 로그인.
2. 권한 목록에서 Microphone(마이크) → Speech Recognition(음성 인식) 순서로 허용.
3. Accessibility(손쉬운 사용): 시스템 설정 → 개인정보 보호 및 보안 → 손쉬운 사용에서 Atticus 스위치 켜기.
4. 화면을 보고 답하게 하려면 Screen Recording도 허용(선택).
5. 테스트: `⌃ control + ⌥ option + space`를 누른 채로 "Open Calculator"라고 말하고 손 떼기 → 계산기가 열리면 완료.
- 이후 Atticus는 메뉴 막대에 상주하고 맥을 켤 때마다 자동 실행.
- ❌ 단축키를 톡 한 번 누르고 말하기 ✅ 누른 채로 말하고 말이 끝나면 손 떼기

## 핵심 팁 · 주의사항
- 음성 명령은 영어로 인식 → "Open Safari"처럼 짧은 영어 문장.
- 반응이 없으면 시스템 설정 → 개인정보 보호 및 보안에서 Atticus의 마이크·음성 인식·손쉬운 사용이 모두 켜져 있는지 확인.
- 꾹 누르기가 불편하면 Atticus 설정 → General → Shortcut behavior → `Press to toggle` (한 번 눌러 시작, 다시 눌러 전송).
- 사용자 단축어: `When I say focus mode, close Slack and open my to-do list.`처럼 한 번 설명해 두면 이후 "focus mode" 두 단어로 실행.
- 파일 삭제, 메일 발송, 결제처럼 되돌리기 어려운 일은 실행 전에 먼저 물어봄.
- 앱은 무료이나 Claude Pro/Max 구독 필요(로컬 모델 제외 기본 경로).
- 참고: 설치 명령은 원격 스크립트를 바로 실행(`curl | bash`)하는 방식이므로, 신뢰할 수 있는 저장소인지 확인하고 싶으면 스크립트를 먼저 내려받아 읽어 볼 것.

## 바로 쓰는 체크리스트
- [ ] macOS 26+ 확인
- [ ] Claude Pro/Max + Claude Code 준비
- [ ] 설치 명령 실행 (커맨드라인 도구 창이 뜨면 설치 후 재실행)
- [ ] 마이크·음성 인식·손쉬운 사용(·화면 기록) 권한 허용
- [ ] "Open Calculator" 테스트
- [ ] 필요 시 Press to toggle / 사용자 단축어 설정
