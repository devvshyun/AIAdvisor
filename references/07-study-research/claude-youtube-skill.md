# 유튜브 튜토리얼을 클로드가 실행하는 스킬로 바꾸는 세 가지 세팅
- 도구·주제: Claude Code + claude-video(watch 스킬) + Gemini + skill-creator · 영상 학습 → 재사용 스킬
- 한 줄 요약: 클로드에게 영상을 보는 눈(watch 스킬)을 달고, 같은 영상을 Gemini가 두 번째 눈으로 따로 읽게 한 뒤, 두 기록을 SPEC.md로 합쳐 skill-creator로 실제 실행되는 스킬로 굽는 순서. (2026-09-10 공개, 읽는 데 16분, 따라 하면 약 54분, STEP 9개)

## 언제 쓰나
- 클로드에게 유튜브 주소를 줘도 영상을 본 게 아니라 제목만 보고 짐작해서 답하는 문제를 해결하고 싶을 때
- 좋은 튜토리얼의 절차를 사람이 받아 적지 않고, 클로드가 언제든 반복 실행하는 스킬로 만들고 싶을 때

## 준비물 / 필요 도구
- claude-video(watch 스킬): https://github.com/bradautomates/claude-video · 최신 릴리스(watch.skill) https://github.com/bradautomates/claude-video/releases/latest
- skill-creator 플러그인(`anthropics/claude-plugins-official` 마켓플레이스): 스킬 저장소 https://github.com/anthropics/skills · 스킬 문서 https://code.claude.com/docs/en/skills
- Gemini API 키(Google AI Studio): https://aistudio.google.com/apikey · 영상 이해 문서 https://ai.google.dev/gemini-api/docs/video-understanding
- yt-dlp https://github.com/yt-dlp/yt-dlp · ffmpeg https://ffmpeg.org/ (영상 받기·화면 자르기는 AI가 아니라 이 두 프로그램이 함)
- Python 3.10 이상: https://www.python.org/downloads/
- 터미널(macOS 터미널 / Windows PowerShell), Claude Code(또는 Codex·Cursor·Copilot·Gemini CLI·웹 Claude)
- 비용: 이 자료의 순서만 따르면 거의 없음(영상 받기·자르기·자막 무료, Gemini 무료 등급은 하루 8시간 분량까지, 비공개·일부 공개 영상은 불가). Claude 사용량은 요금제에 따름.
- 용어: 스킬 = AI에게 새 능력을 추가하는 설명서 묶음, API 키 = 서비스 접속용 긴 비밀번호(남에게 노출 금지)

## 단계별 방법
### 프롬프트 뼈대 A. 세 세팅 설치·검증 위임 (Claude Code 첫 메시지, 선택)
- 목적: watch 스킬·Gemini 키·skill-creator 설치와 연결 검증
- 역할: 세 가지 세팅의 설치·연결 검증 담당
- 슬롯: [운영체제와 셸], [내가 쓰는 AI 도구], [목표 한 줄(예: 유튜브 튜토리얼을 스킬로 만들기)]
- 작업 4단계: ① `ffmpeg -version`, `yt-dlp --version`, `python3 --version` 확인 + watch·skill-creator 설치 여부(이미 있으면 버전만) ② 미설치 시 설치: Claude Code면 `/plugin marketplace add bradautomates/claude-video`, `/plugin install watch@claude-video`, 다른 도구면 `npx skills add bradautomates/claude-video -g`, 이어서 `/plugin install skill-creator@claude-plugins-official`, 빠진 프로그램은 macOS `brew install ffmpeg yt-dlp` ③ 짧은 공개 영상으로 `/watch <영상 주소> 30초 지점에 화면에 뭐가 보여?` 실행(프레임 몇 장·자막 출처 보고), `python3 -c "import google.genai"` 확인 ④ 세 가지의 역할과 사용 순서를 5줄 이내로 설명
- 제약: API 키 값 출력 금지(키는 파일에만), 임의 sudo 금지, 작업 중인 프로젝트 폴더 건드리지 않기(설정은 홈 폴더 안에만)
- 출력: 실행 명령, 버전, 설치한 스킬, 변경한 파일 경로, 남은 오류
- 검증: `/watch`가 프레임 목록과 자막을 함께 반환, `python3 -c "import google.genai"`가 오류 없이 종료. 실패 시 완료 보고 금지

### Quick Start
Claude Code 대화창에 한 줄씩:
```
/plugin marketplace add bradautomates/claude-video
/plugin install watch@claude-video
```
`watch` 스킬 설치 안내가 나오면 성공. Cursor·Codex·Gemini CLI 등은 터미널에서:
```bash
npx skills add bradautomates/claude-video -g
```
확인(짧은 공개 영상이면 됨, 프레임 여러 장을 읽었다는 표시와 화면 설명이 오면 성공):
```
/watch <유튜브 영상 주소> 30초 지점에 화면에 뭐가 보여?
```

### STEP 1. 준비물 확인 (3분)
```bash
ffmpeg -version
yt-dlp --version
python3 --version
```
ffmpeg·yt-dlp는 버전 숫자가 나오면 OK. `command not found`여도 당장 고칠 필요 없음: macOS에서는 처음 `/watch` 때 스킬이 알아서 `brew install ffmpeg yt-dlp`를 실행하고, 리눅스·윈도우는 붙여넣을 명령을 화면에 출력해 준다. 미리 깔려면(macOS):
```bash
brew install ffmpeg yt-dlp
```
Python은 3.10 이상(두 번째 세팅에서 사용).

### STEP 2. 세팅 ① 클로드에게 영상 보는 눈 달아주기 (5분)
| 어디서 쓰나 | 설치 방법 |
|---|---|
| Claude Code | 대화창에 `/plugin marketplace add bradautomates/claude-video` → `/plugin install watch@claude-video` |
| Codex, Cursor, Copilot, Gemini CLI 등 | 터미널에 `npx skills add bradautomates/claude-video -g` |
| 웹 브라우저의 Claude | 공식 저장소 최신 릴리스에서 `watch.skill` 파일을 받아 설정 → Capabilities → Skills → `+` |
웹에서 쓰려면 같은 설정 화면의 "Code execution and file creation"을 먼저 켜야 한다(안 켜면 업로드는 되지만 실행마다 실패). 설치 후 위 확인 명령으로 검증: 프레임 몇 장을 골랐고 자막을 어디서 가져왔는지 알려준 뒤 화면 내용을 설명하면 정상. 첫 실행에서 음성 받아쓰기 키를 물으면 없어도 되니 건너뛰거나 명령 끝에 `--no-whisper`(공개 유튜브는 대부분 자막이 있음). 동작 원리: 자막을 먼저 받고 → 필요한 만큼만 영상을 내려받고 → 장면이 바뀌는 지점을 사진으로 잘라 클로드에게 넘김(들은 것과 본 것을 함께 가짐).

### STEP 3. 세팅 ② 화면 읽기 옵션 정하기 (3분)
프레임 수는 `--detail`로 정한다(수치는 공식 저장소의 49분 8초 화면 녹화 실측).
| 모드 | 프레임 수 | 언제 |
|---|---|---|
| transcript | 0장 | 말하는 영상, 화면 불필요 |
| efficient | 50장 | 긴 영상을 처음 훑을 때 |
| balanced | 100장 | 기본값, 화면을 읽어야 할 때 |
| token-burner | 116장 | 장면이 자주 바뀌어 100장으로 부족할 때 |
터미널·코드가 나오는 튜토리얼(화면 글씨를 크게):
```
/watch <유튜브 영상 주소> --detail balanced --resolution 1024
```
긴 영상은 필요한 구간만(40분을 얇게 훑는 것보다 6분을 촘촘히 보는 쪽이 정확):
```
/watch <유튜브 영상 주소> --start 12:30 --end 18:00 --resolution 1024
```

### STEP 4. 세팅 ③ 제미나이 키 받기 (5분)
Gemini는 유튜브 주소를 구글 쪽에서 직접 읽어 앞 스킬과 증거가 겹치지 않는 두 번째 눈이 된다.
1. https://aistudio.google.com/apikey 에서 키 발급(무료 등급으로 하루 8시간 분량까지, 공개 영상만)
2. 키 저장(첫 줄은 지금 터미널, 둘째 줄은 다음에도 유지)
```bash
export GEMINI_API_KEY="<발급받은 키>"
echo 'export GEMINI_API_KEY="<발급받은 키>"' >> ~/.zshrc
```
3. 파이썬 패키지 설치(`Successfully installed google-genai`)
```bash
pip install google-genai
```
4. `gemini_review.py` 저장 (원문 스크립트의 구조. 코드 상수와 흐름은 그대로이고 영상 분석 프롬프트 본문은 아래 뼈대로 대체)
```python
#!/usr/bin/env python3
import argparse, os, sys
from google import genai

MODELS = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash"]
PROMPT = """..."""   # 아래 '프롬프트 뼈대 B' 참고. {focus} 자리에 --focus 값이 들어감

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="유튜브 주소")
    ap.add_argument("--focus", default="처음부터 끝까지 전체 과정")
    ap.add_argument("--samples", type=int, default=2)
    args = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY가 없습니다. 키를 먼저 저장하세요.")
    client = genai.Client(api_key=key)
    prompt = PROMPT.format(focus=args.focus)
    for i in range(args.samples):
        for model in MODELS:
            try:
                result = client.models.generate_content(
                    model=model,
                    contents=[{"file_data": {"file_uri": args.url}}, {"text": prompt}],
                )
            except Exception as error:
                print(f"[{model}] 실패, 다음 모델로: {error}", file=sys.stderr)
                continue
            print(f"\n===== 읽기 {i + 1}/{args.samples} ({model}) =====")
            print(result.text)
            break
        else:
            print(f"[읽기 {i + 1}] 모든 모델 실패", file=sys.stderr)

if __name__ == "__main__":
    main()
```
프롬프트 뼈대 B. gemini_review.py 내부 영상 분석 프롬프트
- 목적: 영상이 가르치는 것을 그대로 다시 만들 수 있는 설명서를 쓰게 함(읽는 쪽은 영상을 볼 수 없으니 이 글이 전부)
- 슬롯: {focus} = 집중할 부분
- 6항목 출력: ① 무엇을 만드는가(홍보 문구 말고 실제 결과물, 한 문단) ② 필요한 것(화면·말로 나온 도구·패키지·모델·계정, 보이는 버전 그대로, 돈 드는 것 표시) ③ 명령과 설정을 글자 그대로(못 읽으면 짐작하지 말고 UNREADABLE) ④ 실제 만든 순서(되돌린 부분 포함, 완성 화면으로 건너뛴 지점 명시) ⑤ 함정(화면 오류, 말로 한 경고, 곁말) ⑥ 영상이 보여 주지 않은 것(사전 준비, 붙여 넣은 값, 말만 한 단계)
- 규칙: 이 영상에 있는 것만 쓰고 없으면 채우지 말고 "없다"고, 화면 글자가 요약보다 우선, 시간 표시는 대략적으로만
5. 실행(결과는 파일로, 설명서 두 벌이 들어 있으면 성공)
```bash
mkdir -p notes
python3 gemini_review.py "<유튜브 영상 주소>" --focus "<내가 궁금한 부분>" > notes/gemini-pass.md
```
같은 영상을 두 번 읽히는 이유: 두 번 다 나온 내용은 실제 화면에 있던 것이고 한 번만 나온 내용은 모델이 지어낸 쪽에 가깝다.

### STEP 5. 세팅 마무리: 스킬 만드는 스킬 설치 (3분)
Claude Code 대화창에서(마켓플레이스가 이미 등록돼 있으면 첫 줄 생략):
```
/plugin marketplace add anthropics/claude-plugins-official
/plugin install skill-creator@claude-plugins-official
```
skill-creator 설치 안내가 나오면 세 세팅이 모두 끝.

### STEP 6. 영상 한 편을 첫 번째 눈으로 읽히기 (10분)
만들고 싶은 것이 담긴 튜토리얼 하나를 고른다.
1. 영상을 보게 함(프레임 목록과 자막을 읽었다는 표시가 나오면 다음으로)
```
/watch <유튜브 영상 주소> --detail balanced --resolution 1024
```
2. 이어서 아래 지시 전송

프롬프트 뼈대 C. Claude 1차 읽기 (결과를 `notes/claude-pass.md`로 저장)
- 목적: 방금 본 튜토리얼을 그대로 재현할 다른 AI(영상을 못 봄)에게 줄 설명서 작성
- 슬롯: [내가 이 영상에서 원하는 것: 전체 과정 / X 부분만 / 방법이 말이 되는지만], [내가 만들려는 것: 예 클로드 스킬 하나]
- 6항목 순서: 뼈대 B와 동일(무엇을 만드는가 / 필요한 것 / 명령과 설정 인용·못 읽으면 UNREADABLE / 만드는 순서 / 함정 / 영상이 안 보여 준 것) — 이 영상에 있는 것만, 없으면 "없다"고
- 5·6번이 핵심: "미리 해 두셨어야 해요" 같은 한마디가 나머지 전체보다 시간을 아낌
- 순서 주의: 이 파일을 먼저 저장하고 나서 STEP 4의 Gemini 결과를 볼 것(남의 답을 먼저 보면 끌려감)

### STEP 7. 두 기록을 합쳐 설계도 만들기 (5분)
프롬프트 뼈대 D. 두 읽기 병합 → SPEC.md
- 입력: 읽기 A = `notes/claude-pass.md`(직접 프레임·자막을 본 기록), 읽기 B = `notes/gemini-pass.md`(Gemini가 영상을 직접 읽은 기록, 두 벌), [내가 만들려는 것]
- 지시: 어느 쪽도 정답이 아니며 `SPEC.md`를 만들고 모든 줄에 딱지 하나 부착 — 확인됨(두 기록 일치, 그대로 믿고 만들어도 됨) / 한쪽만(한 기록에만 있음, 어느 쪽 출처인지 표시) / 충돌(두 기록이 다름, 평균 내지도 더 자신 있어 보이는 쪽을 고르지도 말고 두 내용을 다 적은 뒤 해당 장면을 다시 확인해 무엇을 봤는지 기록)
- 규칙: 두 기록의 시간 표시·길이·개수는 전부 삭제(둘 다 시계가 없어 초 단위로 틀림), 명령어·패키지 이름·설정값·오류 메시지는 글자 그대로, 설명서에서 베낀 듯 매끄러운 줄은 의심(영상만의 특이한 단계가 일반 설명으로 뭉개진 지점), 마지막에 "남은 질문" 목록(어느 기록도 못 본 것과 아직 충돌인 것)
- 성공: `SPEC.md`가 생기고 줄마다 딱지가 붙음. 한 AI의 요약은 화면에서 읽은 것과 지어낸 것이 똑같은 말투라 구분이 안 되는데, 두 번 읽고 딱지를 붙이면 확인할 곳이 서너 줄로 줄어든다.

### STEP 8. 스킬로 굽고 한 번 돌려보기 (10분)
프롬프트 뼈대 E. 스킬 제작 요청
- 지시: skill-creator로 `SPEC.md`에서 스킬 생성. 이 설계도는 영상에서 복원한 것이라 딱지를 진짜로 취급 — 확인됨은 그대로 사용, 한쪽만은 미검증이므로 조용히 넘어가지 말고 실패하게 만들기, 남은 질문 항목은 만들지 말고 나에게 물어보기
몇 가지 질문 후 스킬 폴더가 만들어진다. 반드시 한 번은 실제로 실행:
```
방금 만든 스킬을 <실제 입력>으로 한 번 실행해 줘. 깨지는 부분은 고쳐 줘.
```
보통 한 번의 수정으로 돌아간다. 이 한 번을 건너뛴 스킬은 영상 요약본일 뿐. `SPEC.md`와 `notes/`는 스킬 폴더 안에 보관(나중에 스킬이 이상할 때 어느 줄이 확인됨/한쪽만이었는지 추적).

### STEP 9. 매번 반복하지 않게 한 줄로 묶기 (10분, 선택)
위 과정을 두어 번 손으로 해 본 뒤, 아래를 `~/.claude/skills/youtube-to-agent/SKILL.md`로 저장하면 새 대화에서 `/youtube-to-agent <유튜브 주소>`로 전체가 실행된다. frontmatter(원문 그대로):
```
---
name: youtube-to-agent
description: 유튜브 튜토리얼을 실제로 돌아가는 스킬로 바꾼다. watch로 영상을 보고, 제미나이에게 같은 영상을 따로 읽히고, 두 기록을 합쳐 설계도를 만든 뒤 skill-creator에 넘긴다. 사용자가 유튜브 링크를 주면서 "이거 만들어 줘", "스킬로 만들어 줘"라고 할 때 쓴다.
argument-hint: "<유튜브 주소> [원하는 것]"
allowed-tools: Bash, Read, Write, Skill, AskUserQuestion
user-invocable: true
---
```
본문 뼈대(5단계 + 안 될 때):
- 개념: 두 눈이 같은 영상을 본다(watch는 프레임·자막을 대화로 가져오고 Gemini는 구글 쪽에서 직접 읽음). 서로 다르게 틀리므로 어긋나는 지점이 확인할 곳.
- 1단계 범위 정하기: 원하는 것을 안 말했으면 먼저 묻고, 영상이 20분을 넘으면 구간 지정 제안
- 2단계 첫 번째 읽기: `/watch` 실행(말하는 영상은 transcript, 긴 화면 녹화 훑기는 efficient, 화면 읽기는 balanced, 터미널·코드는 `--resolution 1024`, 구간은 `--start`/`--end`). 프레임을 다 읽은 뒤 Gemini 결과 보기 전에 6항목 설명서를 `notes/claude-pass.md`에 먼저 작성
- 3단계 두 번째 읽기: `python3 gemini_review.py "<주소>" --focus "<사용자가 원한 것>" > notes/gemini-pass.md`
- 4단계 설계도 병합: 모든 줄에 확인됨/한쪽만/충돌 딱지, 충돌은 직접 재확인(평균 금지), 시간·개수 버리고 명령어는 글자 그대로, 매끄러운 줄은 학습 데이터에서 온 것일 수 있으니 의심
- 5단계 만들고 확인: SPEC.md를 skill-creator에 넘기며 한쪽만 줄은 미검증이라고 명시, 새 스킬을 진짜 입력으로 한 번 돌려 깨진 것 수정
- 안 될 때: 자막 없음 → watch는 프레임만, Gemini는 소리를 직접 들으니 말한 내용은 남음 / Gemini 계속 실패 → 무료 한도 소진, 첫 번째 읽기만으로 진행하고 설계도 전체를 한쪽만으로 표시 / 두 기록이 거의 다 어긋남 → 구간이 너무 넓음, 좁혀서 둘 다 재실행

## 핵심 팁 · 주의사항
- ❌ Gemini 결과를 먼저 열어 보기(첫 읽기가 따라가 두 번째 의견의 값어치 소멸) → ✅ Claude 읽기를 저장한 뒤 Gemini 결과 확인
- ❌ 긴 영상(40분)을 통째로 시키기(두 기록이 거의 모든 지점에서 어긋남) → ✅ 범위를 좁혀 다시 돌리기
- ❌ 시간·개수를 그대로 믿기(AI는 시계가 없어 시간을 재구성) → ✅ 도구 이름·명령어·오류 메시지를 증거로, 시간과 개수는 참고만
- ❌ 만들고 안 돌려 보기 → ✅ 실제 입력으로 1회 실행·수정해야 비로소 스킬
- 스크립트 속 모델명(`gemini-3.8-flash`, `gemini-flash-latest`, `gemini-3.5-flash`)이 실제로 존재하는지는 사용 시점의 공식 문서로 확인(실패하면 다음 모델로 넘어가는 구조)
- 토큰은 프레임 수에 비례(사진 한 장 값) → `--detail efficient`나 `--start`/`--end`
- 비공개 영상은 불가(Gemini는 공개 영상만, 영상 받는 도구도 로그인 안 함) → 공개로 바꾸거나 파일을 직접 내려받아 사용
- 코드 없이 두 번째 읽기: Google AI Studio 화면에 유튜브 링크를 붙여 같은 질문(반복할 거면 파일화 추천)

## 문제 해결
- `/plugin` 명령이 없다고 나옴: Claude Code가 아닌 도구일 가능성 → `npx skills add bradautomates/claude-video -g`
- 첫 실행에서 API 키를 물음: 자막 없는 영상용 음성 받아쓰기 키라 없어도 됨, 건너뛰기 또는 `--no-whisper`
- 자막이 없는 영상: 첫 읽기는 프레임만, Gemini가 소리를 직접 듣고 말한 내용을 보완 → 설명서에 "자막 없음"을 적어 둘 것
- Gemini가 계속 실패: 무료 한도 소진 또는 키 오류 → `echo $GEMINI_API_KEY`로 확인, 값이 있으면 하루 지나 재시도
- 만든 스킬이 이상하게 동작: SPEC.md의 해당 줄 딱지 확인(확인됨이면 내 구현 문제, 한쪽만이면 영상이 원래 안 보여 준 부분)

## 바로 쓰는 체크리스트
- [ ] ffmpeg / yt-dlp / Python 3.10+ 확인
- [ ] watch 스킬 설치 + 짧은 영상으로 `/watch` 검증
- [ ] Gemini 키 발급·저장 + `pip install google-genai` + `gemini_review.py` 저장
- [ ] skill-creator 설치
- [ ] Claude 읽기(`notes/claude-pass.md`) 저장 → Gemini 읽기(`notes/gemini-pass.md`) → `SPEC.md` 병합(딱지)
- [ ] 스킬 생성 후 실제 입력으로 실행·수정, SPEC.md·notes 보관
- [ ] (선택) `youtube-to-agent` 통합 스킬 저장
