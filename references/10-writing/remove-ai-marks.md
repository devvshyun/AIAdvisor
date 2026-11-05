# 클로드가 남기는 표식 지우기
- 원문: https://lazyowen.com/guides/remove-ai-marks
- 도구·주제: watermarks-remover (Guillaume Meyer, MIT) · AI 생성물 표식 점검/제거
- 한 줄 요약: 글 속 안 보이는 문자와 이미지/PDF 메타데이터는 도구로 제거·검증할 수 있고, 단어 선택 패턴은 검증 방법이 없다는 한계를 안내한다. (2026-08-21 공개, 읽는 데 12분, 6단계 따라 하면 약 53분)

## 언제 쓰나
- AI 생성 글/파일에 남은 비가시 문자와 출처 메타데이터를 점검하고 정리하고 싶을 때. 안 보이는 문자는 블로그/코드 편집기에 붙여넣을 때 줄이 깨지는 원인이 되기도 함.
- 배경(앤트로픽 공식 안내 인용): 클로드가 만든 콘텐츠에 기계가 읽는 표식을 넣으며 2026-08-02 이후 출시 모델부터, 이전 모델에도 순차 적용 중. 적용 범위는 API·클로드 앱·Claude Code·Cowork·Tag 전부, 지역 제한 없음.

## 준비물 / 필요 도구 (이름 + 공식 링크)
- 도구: https://github.com/guillaumemeyer/watermarks-remover (MIT, 무료 오픈소스)
- Python 3.10+ (핵심 기능은 기본 기능만 사용 — 추가 라이브러리 불필요), `git`. 설치 https://www.python.org/downloads/
- PDF 완전 제거는 `exiftool`, `qpdf` 별도 설치(없으면 결과가 불완전하다고 리포트에 표시)
- 앤트로픽 안내: https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content · 스킬 만들기 https://support.claude.com/en/articles/12512180-how-to-create-custom-skills
- 용어: 표식(워터마크)=사람 눈엔 안 보이지만 기계가 알아보는 흔적(반투명 로고와 다름), 메타데이터=파일 내용 외의 정보(촬영 날짜·만든 프로그램 등).

## 단계별 방법
**표식 종류(STEP 1, 3분)**: ① 글의 **단어 선택 패턴** — 비슷한 뜻의 단어 중 고르는 선택이 한쪽으로 쏠려 수백 단어에 걸쳐 패턴이 됨(파일에 저장된 게 아니라 문장 안에 있어 복사해도 따라감) ② **안 보이는 문자**(폭 0 공백 등) ③ **파일 메타데이터**(`.svg`, `.png`, `.jpg` 등에 붙는 서명된 출처 정보, 떼어낼 수 있음). 메모장 재붙여넣기·형식 변환·제목 수정은 "표식이 파일에 저장돼 있다"는 가정에서 나온 방법이라 효과 없음.

**Quick Start / STEP 2 도구 내려받기 (5분)**
```
python3 --version
git clone https://github.com/guillaumemeyer/watermarks-remover.git ~/watermarks-remover
ls ~/watermarks-remover/service/scripts/inspect_text.py
```
- Python 3.10 이상(없으면 설치 후 터미널 재시작). `ls`가 경로를 한 줄 출력하면 준비 완료, `No such file`이면 clone 재실행.

**STEP 3 글에서 안 보이는 문자 지우기 (10분)** — 숫자로 검증 가능한 유일한 부분.
```
python3 ~/watermarks-remover/service/scripts/inspect_text.py 내글.md
python3 ~/watermarks-remover/service/scripts/clean_text.py 내글.md -o 내글.cleaned.md --stats
python3 ~/watermarks-remover/service/scripts/inspect_text.py 내글.cleaned.md
```
- 검사 출력 예: `Length: 66 chars` / `Suspicious: 7` / `[zwj_family/probable] U+200B ZERO WIDTH SPACE (Cf) x3 @ [18, 63, 64]` / `[space/informational] U+00A0 NO-BREAK SPACE (Zs) x1` / `[bidi/probable] U+200E LEFT-TO-RIGHT MARK (Cf) x1` / `[space/informational] U+202F ...` / `[zwj_family/probable] U+2060 WORD JOINER (Cf) x1` (대괄호 숫자=글자 위치).
- 청소는 원본 유지, 새 파일 생성. `--stats` 출력 예: `"removed_count": 4`, `"replaced_count": 2` (U+200B 3개, U+2060 1개 제거 / U+202F, U+00A0 대체).
- 재검사에서 `Suspicious`가 7→1처럼 줄면 성공. 0이 아니어도 정상 — 글 방향 지정 등 실제 역할이 있는 문자는 일부러 남김.

**STEP 4 이미지·문서 메타데이터 (10분)** — 로컬 전용 서버 방식. 서버 창은 켜 두고 새 터미널에서 실행.
```
python3 ~/watermarks-remover/service/scripts/server.py --host 127.0.0.1 --port 8765
curl -s http://127.0.0.1:8765/health
```
- `{"ok": true, "version": "..."}`면 성공, 무응답이면 서버 창의 오류 확인. 검사/제거(파일은 base64로 전송, `/inspect`를 `/clean`으로 바꾸면 제거):
```
curl -s -X POST "http://127.0.0.1:8765/inspect" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 -w0 < shot.png)\", \"name\": \"shot.png\"}"
curl -s -X POST "http://127.0.0.1:8765/clean" -H 'Content-Type: application/json' \
  -d "{\"file\": \"$(base64 -w0 < shot.png)\", \"name\": \"shot.png\"}"
```
- 검사 결과 예: `"has_ai_metadata": true`, `"findings": ["PNG iTXt: AI generated, Claude", "PNG tEXt: Claude"]`. 제거 결과 예: `"actions": ["drop chunk iTXt", "drop chunk tEXt"]`, `"bytes_in": 412`, `"bytes_out": 74`, **`"still_has_ai_metadata": false`**면 다 떼어진 것(그림은 그대로, 정보만 삭제). 응답에는 청소된 파일 내용도 함께 돌아옴.
- PDF는 `exiftool`+`qpdf`가 깔려 있어야 제대로 제거.

**STEP 5 단어 선택 패턴 흐트러뜨리기 (선택, 15분)**
- 방법은 글 **통째 재작성**뿐 — 제목만 바꾸거나 문단 순서 이동은 효과 없음(패턴이 문장 안에 흩어져 있어 단어를 실제로 바꿔야 함). **클로드가 쓴 글은 클로드로 다시 쓰지 말고** 다른 AI로(같은 모델은 같은 선택이 다시 들어감).
- 도구가 권장하는 프롬프트 뼈대: 아래 글을 단어 단위에서 완전히 다른 표현으로 재작성 / 절 순서·접속어·연결 표현 변경 / 문장 끊김 지점과 길이를 다양하게 / 뜻이 허락하는 한 내용어·기능어 모두 교체 / **사실·숫자·이름·기술 용어는 유지**, 없던 주장 추가·있던 주장 삭제 금지 / 재작성한 글만 출력 / 끝에 `---` 구분 후 `[글 붙여넣기]`.
- 재작성본은 STEP 3 검사·청소를 한 번 더 (재작성한 AI도 새 문자를 남김). 순서: **청소 → 재작성 → 청소**.
- 대가: 표현과 리듬이 그 AI의 것으로 바뀜(잘 쓴 글일수록 손해). 품질 우선이면 건너뛰고 STEP 3·4만.

**STEP 6 클로드 스킬로 쓰기 (선택, 10분)**
```
cd ~/watermarks-remover/skills && zip -r ~/remove-ai-marks.zip remove-ai-marks
```
- 홈 폴더에 `remove-ai-marks.zip` 생성 → 클로드에서 Customize → Skills → `+` → `Create skill` → `Upload a skill` → zip 업로드(목록에서 켜고 끌 수 있음).
- **코드 실행을 켜야 함**(꺼져 있으면 업로드돼도 무반응 — 스킬 고장처럼 보이지만 설정 문제). 스킬 자체에는 삭제 코드가 없고 서버에 일을 시키는 설명서만 있으므로 **STEP 4 서버가 켜져 있어야 동작**. 터미널만 쓸 거면 건너뛰어도 됨.

**설치·검증 위임 프롬프트 뼈대(Claude Code)**: 역할=watermarks-remover 설치·동작 검증 담당. 슬롯 `<운영체제와 셸>`, `<기술 스택>`, `<목표 한 줄>`. 작업: ① `python3 --version` 3.10+ 확인, `ls ~/watermarks-remover/service/scripts/inspect_text.py` 존재 확인(있으면 재다운로드 말고 경로 보고) ② 없을 때만 git clone ③ 샘플 파일을 만들어 inspect → clean(`-o`, `--stats`) → 출력 파일 재 inspect, 숫자 감소 확인 ④ 도구가 지우는 것/못 지우는 것/사용법을 5줄 이내로 설명. 제약: 원본 덮어쓰기 금지(항상 새 파일), 이미지·PDF를 텍스트 도구에 넣지 말 것, `--force-text` 금지, API 키·토큰 출력 금지. 검증: 청소 후 `Suspicious`가 청소 전보다 작고 `--stats`의 `removed_count` > 0. 실패 시 완료 보고 금지.

## 핵심 팁 · 주의사항
- **성공을 증명하지 못함**(만든 사람도 문서에 명시): 수치로 확인되는 건 지운 비가시 문자 수와 뗀 메타데이터 항목뿐. 단어 선택 패턴이 지워졌는지는 확인할 방법이 없음(앤트로픽이 검사 기능을 예고했으나 미공개).
- AI 탐지기 상당수는 숨은 신호가 아니라 문체로 판정 → 표식을 다 지워도 걸릴 수 있음. 이미지 픽셀 자체에 심은 표식, 소리·영상 표식은 이 도구의 범위 밖.
- 저자 당부: AI 사용이 문제되는 상황이라면 표식을 지울 일이 아니라 상황 자체를 다시 생각해 볼 신호일 수 있음. 이 도구는 내 콘텐츠를 내 이유로 정리할 때 쓰는 것.
- ❌ 원본에 덮어쓰기 / 이미지를 텍스트 명령에 넣기 / 서버를 외부에 노출(`--host 127.0.0.1` 로컬 전용 유지).

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| 스킬 올렸는데 무반응 | 코드 실행 꺼짐 | 설정에서 코드 실행 켜고 재시도 |
| 청소 후 `Suspicious`가 0이 아님 | 역할 있는 문자는 일부러 남김 | 정상(줄었으면 성공) |
| 검사에 아무것도 안 나옴 | 안 보이는 문자가 없음 | 단어 선택 패턴은 STEP 5(검증 불가) |
| 이미지를 텍스트 명령에 넣으니 거부 | 텍스트 도구는 이미지 불가 | STEP 4 서버 방식 |
| PDF 결과가 불완전 | `exiftool`·`qpdf` 없음 | 설치하거나 결과를 그대로 수용 |
| 서버 확인(health)이 무응답 | 서버 창이 꺼졌거나 포트 불일치 | 서버를 켠 터미널 창 확인 |

## 바로 쓰는 체크리스트
- [ ] Python 3.10+ 확인 / 저장소 clone 및 `inspect_text.py` 경로 확인
- [ ] inspect → clean(`-o`, `--stats`) → inspect로 비가시 문자 감소 확인
- [ ] 이미지/PDF는 로컬 서버(`127.0.0.1:8765`)로 inspect/clean (PDF는 exiftool+qpdf)
- [ ] `still_has_ai_metadata: false` 확인
- [ ] 단어 선택 패턴 제거는 가능 여부를 확인할 수 없음을 인지(재작성은 다른 AI로, 청소→재작성→청소)
