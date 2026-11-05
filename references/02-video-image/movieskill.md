# AI 냄새 줄이는 영상 만들기: Banana Pro Director 2.0 + Cinema Worldbuilder Pro 2.0
- 원문: https://lazyowen.com/guides/movieskill
- 도구·주제: Claude Skills + Higgsfield(Seedance 2.0, Nano Banana Pro) · AI 영상 제작 파이프라인 (영상·이미지, 16분 읽기, STEP 9개, 2026-08-06 갱신)
- 한 줄 요약: 두 스킬은 영상을 직접 만들지 않고 Claude가 이미지·영상 프롬프트를 제작 규칙대로 쓰게 하는 지침. 얼굴 잠금 → 의상 → 6패널 시트 → 장면 플레이트 → 움직임 설계 → Seedance 생성 → 부분 수정 → 편집.

## 언제 쓰나
- AI 영상 특유의 얼굴·의상 흔들림, 인물 위치 뒤바뀜, 플라스틱 피부를 줄이고 싶을 때
- 역할: Banana Pro Director 2.0 = 캐릭터·의상·6패널 시트·장면 플레이트 설계 / Cinema Worldbuilder Pro 2.0 = 그 기준 이미지를 Seedance 2.0 영상 프롬프트로 변환
- 본문 대본의 `Chinema World Build`는 실제 이름과 다름. 실제 파일: `banana-pro-director-2.0.zip`, `cinema-worldbuilder-pro-2.0.zip`

## 준비물 / 필요 도구
- Claude Skills 안내: https://support.claude.com/en/articles/12512180-use-skills-in-claude · 개념: https://support.claude.com/en/articles/12512176-what-are-skills
- Higgsfield: Seedance 2.0 https://higgsfield.ai/seedance/2.0 (영상 https://higgsfield.ai/ai/video?model=seedance_2_0), Nano Banana Pro https://higgsfield.ai/ai/image?model=nano-banana-pro, 가격 https://higgsfield.ai/pricing
- Nano Banana Pro(= Gemini 3 Pro Image): https://blog.google/innovation-and-ai/products/nano-banana-pro/ · Seedance 2.0(ByteDance): https://seed.bytedance.com/seedance2_0 , https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0
- 스킬 배포처(GitHub 아님): 제작자 Notion https://pyrite-mallow-3b0.notion.site/The-Claude-skills-that-run-my-AI-Cinema-workflow-got-an-UPGRADE-Here-s-Why-36d49da027d780ff928ef70a16148369 , Dropbox 폴더 https://www.dropbox.com/scl/fo/26qrwypqx58627600ewc8/AHQV00wVPD7YByPktuPwGX0?rlkey=gdgvq8t4mqpj9pi0wyyqd0jvb&st=wm3jasqg&dl=0 , 소개 영상 https://www.youtube.com/watch?v=0YhhPQVXA7c
- 비용: 스킬 파일 무료, 이미지·영상 생성은 Higgsfield 요금제/크레딧(가격은 변동, 생성 전 확인)

## 단계별 방법
### Quick Start. 다운로드·설치 명령
Dropbox 폴더를 통째로 받아(URL 끝 `dl=1`) 안쪽 파일명만 꺼냄. 폴더 ZIP에 빈 최상위 경로가 있어 일부 `unzip`이 경고 종료되므로 Python으로 해제:
```bash
curl -L "https://www.dropbox.com/scl/fo/26qrwypqx58627600ewc8/AHQV00wVPD7YByPktuPwGX0?rlkey=gdgvq8t4mqpj9pi0wyyqd0jvb&st=wm3jasqg&dl=1" \
  -o claude-video-skills.zip
python3 - <<'PY'
from pathlib import Path
from zipfile import ZipFile
out = Path("claude-video-skills")
out.mkdir(exist_ok=True)
with ZipFile("claude-video-skills.zip") as archive:
    for item in archive.infolist():
        name = Path(item.filename).name
        if name:
            (out / name).write_bytes(archive.read(item))
PY
```
Claude Code는 안쪽 ZIP 두 개를 스킬 폴더에 풀기:
```bash
mkdir -p "$HOME/.claude/skills"
unzip claude-video-skills/banana-pro-director-2.0.zip \
  -d "$HOME/.claude/skills"
unzip claude-video-skills/cinema-worldbuilder-pro-2.0.zip \
  -d "$HOME/.claude/skills"
```
최소 실행 문장(뼈대): "Banana Pro Director 2.0을 사용해 주세요. 새 캐릭터를 만든다. 중간 회색 스튜디오 배경에서 얼굴·정체성을 먼저 잠그고 싶다. 전체 프롬프트 전에 레퍼런스·캐릭터·배경·프레이밍을 짧게 확인해 달라." / 영상은 "Cinema Worldbuilder Pro 2.0을 사용해 주세요. 첨부한 시트와 플레이트로 8초 원테이크 설계, 인물은 왼쪽 3분의 1 고정, 카메라 천천히 전진, Higgsfield 레퍼런스 순서와 Seedance 영어 프롬프트 요청."
정상 동작 신호: 긴 프롬프트 대신 먼저 `Pre-prompt check` 제시 / 이미지 스킬은 캐릭터가 이미 있는지부터 질문 / 영상 스킬은 런타임을 묻고 레퍼런스를 번호 순서로 정리 / 영상 프롬프트는 영어 코드 블록.

### STEP 1. 스킬 2개 설치 (5분)
웹·데스크톱 Claude는 ZIP을 풀지 않고 하나씩 업로드:
1. `Settings → Capabilities`에서 `Code execution and file creation` 켜기
2. `Customize → Skills`
3. `+ → Create skill → Upload a skill`
4. `banana-pro-director-2.0.zip` 업로드
5. `cinema-worldbuilder-pro-2.0.zip` 업로드
6. 두 스킬이 켜졌는지 확인 (예전 화면은 Settings → Capabilities → Skills 안에 업로드 버튼)
Claude Code 확인:
```bash
test -f "$HOME/.claude/skills/banana-pro-director-2.0/SKILL.md" \
  && printf 'Banana Pro Director: OK\n'
test -f "$HOME/.claude/skills/cinema-worldbuilder-pro-2.0/SKILL.md" \
  && printf 'Cinema Worldbuilder: OK\n'
```
새 세션에서: `설치된 Banana Pro Director 2.0과 Cinema Worldbuilder Pro 2.0의 역할을 한 줄씩 알려주세요. 아직 프롬프트를 만들지는 마세요.` → 이미지 기준점 / Seedance 영상 프롬프트 담당이라 답하면 정상.
- 외부 스킬은 켜기 전에 내용을 읽을 것. 공식 2.0 배포본은 각 폴더에 `SKILL.md`만 있고 실행 스크립트 없음. 배포본 갱신 시 재확인.

### STEP 2. 역할 분담 (3분)
| 단계 | 담당 | 결과 |
|---|---|---|
| 얼굴 잠금 | Banana Pro Director | 기준 얼굴 이미지 |
| 의상 기준점 | Banana Pro Director | 중간 회색 배경 전신 의상 |
| 각도 기준점 | Banana Pro Director | 3×2 6패널 시트 |
| 환경 기준점 | Banana Pro Director | 장면 플레이트 |
| 움직임 설계 | Cinema Worldbuilder | 레퍼런스 순서+Seedance 영어 프롬프트 |
| 영상 생성 | Higgsfield Seedance 2.0 | 최대 15초 클립 |
| 편집·색보정 | 영상 편집기 | 최종 숏폼 |
- 용어: 얼굴 잠금=얼굴·피부톤·머리·체형·고유 표식을 기준 이미지 한 장으로 고정 / 장면 플레이트=인물 배치 전 환경·조명·구도 확인용 정지 이미지
- 2.0 변경점 3가지: ① 캐릭터 기본 배경 순백 → 중간 회색(얼굴 가장자리 날아감·플라스틱 피부 완화) ② 공기층·안개·입자·빛 감쇠로 전경/배경 깊이 분리 ③ 카메라 브랜드 나열 대신 화각·보케·입자·움직임 서술
- 한 스킬에 이미지와 움직임을 다 맡기지 않고 정지 이미지로 정체성·의상·환경을 잠근 뒤 영상으로.

### STEP 3. 얼굴·의상 기준 이미지 (10분)
- 새 캐릭터 얼굴 잠금 (Nano Banana Pro 단일 패스 권장). 프롬프트 뼈대: Banana Pro Director 2.0 지정 + 캐릭터 설명 슬롯(머리, 피부톤, 턱선, 표정/시선, 고유 점 등) + 중간 회색 심리스 배경 + 부드러운 측면광 + 의상은 검은 기본 상의로 제한 + 전체 프롬프트 전에 확인 목록 요청. 확인 목록에서 잘못 읽은 외형만 고치고, 승인 뒤 받은 영어 프롬프트를 Higgsfield의 Nano Banana Pro에 붙여 생성.
- 기존 캐릭터 의상 입히기: 얼굴 기준 이미지 첨부, 첨부 이미지를 얼굴·피부톤·머리·체형 기준으로 잠금 + 새 의상 목록 슬롯(재킷, 팬츠, 액세서리, 신발) + 중간 회색 심리스 배경 전신 단일 의상 기준 이미지 + Banana Pro 경로 + 확인 목록 먼저.
- 복잡한 의상은 Soul Cinema 2단계 경로: 일반 모델로 의상만 입힌 레퍼런스 생성 → 그것과 잠긴 캐릭터 이미지를 합침. 얼굴과 스타일링을 한 번에 만들지 않는 게 핵심.
- 점검: 얼굴 이미지에 환경·화려한 의상이 섞이지 않음 / 의상 이미지는 머리~신발 전체 / 배경은 중간 회색 / 피부가 번들거리지 않고 미세 질감과 자연스러운 명암.

### STEP 4. 6패널 캐릭터 시트 (5분)
승인된 단일 의상 이미지를 만든 뒤에만 요청(그 전에 6패널부터 요청 금지).
- 프롬프트 뼈대: Banana Pro Director 2.0 지정 + 첨부한 의상 기준 이미지로 16:9 한 장 3×2 시트. 패널: 전신 정면 / 전신 후면 / 왼쪽 얼굴 측면 / 오른쪽 얼굴 측면 / 얼굴 정면 클로즈업 / 목걸이와 손 디테일(소품은 내 캐릭터에 맞게). 모든 패널에서 얼굴·머리·의상·체형 동일, 중간 회색 배경·동일 조명, 확인 목록 먼저.
- 점검: 여섯 패널이 한 장의 16:9에 들어 있음 / 정면·후면·양측면·얼굴·디테일 빠짐없음 / 패널마다 얼굴·의상 색 불변. 잘못된 패널은 전체 재설계보다 문제를 먼저 설명.

### STEP 5. 장면 플레이트 잠그기 (5분)
비싼 영상 생성 전에 환경과 인물 배치를 정지 이미지로 확인. 캐릭터 없는 환경 플레이트 먼저, 또는 캐릭터 들어간 첫 프레임 바로 가능.
- 프롬프트 뼈대: Banana Pro Director 2.0 + 6패널 시트를 정체성 기준으로 첨부 + 장면 슬롯(예시: 비 온 뒤 지하 주차장, 새벽 직전 차가운 주변광, 인물 왼쪽 3분의 1, 오른쪽 빈 공간과 멀리 주황 실용 조명, 얕은 물과 옅은 안개로 깊이 분리) + 16:9 영화 스틸 + 전체 프롬프트 전에 레퍼런스·인물 위치·조명·프레이밍 확인.
- 점검: 인물과 환경 광원 방향 일치 / 스티커처럼 붙어 보이지 않음 / 전경·중경·배경 대비가 다름 / 유지할 차량·소품은 별도 기준 이미지.

### STEP 6. Cinema Worldbuilder로 움직임 설계 (7분)
시트+플레이트 첨부. 레퍼런스 순서, 화면 위치, 움직임, 마지막 프레임, 현장음, 카메라 특성을 하나의 Seedance 프롬프트로 묶음.
| 모드 | 쓰는 장면 |
|---|---|
| M1 Narrative | 거리·집·차량 등 현실 서사 |
| M2 Studio | 스튜디오, 패션 필름, 인공 세트 |
| M3 Action | 추격·전투·스턴트·파괴 |
| M4 Performance | 콘서트·무대·관객 있는 공연 |
| M5 Atmospheric | 인물 없는 환경·날씨·분위기 |
- 처음엔 한 영상에 중심 행동 하나. 런타임 가이드: 4~8초=강한 행동 하나+고정 구도 / 8~12초=행동 하나+드러남이나 짧은 정지 / 12~15초=단순한 2~3비트+명확한 컷 / 복잡한 다중 행동은 프롬프트 분리.
- 프롬프트 뼈대: Cinema Worldbuilder Pro 2.0 + 레퍼런스 목록(첨부1=6패널 시트, 첨부2=장면 플레이트) + 모드(M1 등), 길이(8초 원테이크), 인물 고정 위치, 시간대별 행동(처음 2초 정면, 이후 천천히 오른쪽을 보며 한 걸음), 카메라(50mm 느낌 중간 숏, 아주 천천히 전진), 사운드(빗물·옷 스침·환풍기만), 음악·화면 속 글자 없음 지시 + Pre-prompt check 먼저, 승인 뒤 Higgsfield 레퍼런스 번호 순서와 Seedance용 영어 프롬프트 요청.
- 최종 답변에 10블록이 이 순서로 있어야 함:
```
Scene & Mood
Frame Map
Subject Lock
Cross-Frame Rules
Movement
Last Frame
World Plate
Sound Bed
Capture Realism
Camera Capture
```
- `@image1`, `@image2` 번호는 Claude가 준 목록과 정확히 일치해야 함. Seedance 2.0 공식 사양은 이미지 9·영상 3·오디오 3까지 참조, 이 스킬은 영상 프롬프트의 이미지 레퍼런스를 최대 9장으로 제한.

### STEP 7. Higgsfield에서 Seedance 2.0 실행 (5분)
1. Higgsfield에서 Seedance 2.0 선택
2. Claude 목록 1번 이미지부터 같은 순서로 첨부
3. 영어 코드 블록을 번역 없이 프롬프트 칸에 붙여넣기
4. 런타임·화면비 재확인 (릴스 9:16, 가로 16:9)
5. 생성 후 첫 프레임과 마지막 프레임부터 비교
- Seedance 2.0은 텍스트·이미지·오디오·영상 입력, 최대 15초 멀티샷. 15초를 채우는 게 목표가 아님 — 처음엔 4~8초 한 행동으로 테스트.
- 생성 전 확인 프롬프트 뼈대: 방금 받은 Seedance 프롬프트를 실행 전 검사. 레퍼런스 번호 불일치, 런타임 불일치, 인물 위치 교차, 음악 지시, 화면 속 글자 지시만 확인, 문제 없으면 수정하지 말고 `PASS`.
- 점검: 시작~끝 같은 얼굴·의상 / `@imageN`이 실제 첨부 순서와 일치 / 프롬프트 제목의 초 수 = Camera Capture 초 수 / Movement 구간 합 = 전체 런타임 / 마지막 프레임이 Last Frame 설명에 가까움.

### STEP 8. 실패한 부분만 다시 설계 (5분)
첫 결과가 완벽하지 않은 건 정상. 제작자 개인 기록: 직접 프롬프트 시 한 숏 8~10번 생성 → 스킬 적용 후 2~3개 후보 중 선택 (보장값 아님).
- 얼굴 흔들림: 시트는 그대로, Subject Lock에 얼굴·머리·의상·실루엣이 전체 런타임 동안 동일하다는 양의 제약을 강화해 달라 요청(다른 장면·카메라 설정은 변경 금지).
- 인물 위치 뒤바뀜: Cross-Frame Rules만 강화 — 왼쪽 인물은 왼쪽 3분의 1, 오른쪽 인물은 오른쪽 3분의 1에 전체 런타임 동안 고정, 중앙선 넘지 않게 양의 제약으로 재작성.
- 플라스틱 피부/평면 배경: Capture Realism에서 이마·콧대·광대·턱의 과한 반사를 줄이고 전경/배경 사이 옅은 공기층 강화, 구도·움직임 유지.
- 확인: 수정본에서 요청한 변수 하나만 바뀌어야 함. 작은 수정에 전체가 다시 쓰였다면 잠금이 풀린 것. 한 번에 변수 하나만.

### STEP 9. 편집 마무리 (프로젝트에 따라 다름)
스킬과 Seedance가 주는 건 편집 전 클립. 컷 연결, 색 통일, 사운드, 자막, 속도 조절은 편집기에서. 좋은 영상은 여러 번의 생성과 편집이 여전히 필요.
- 장면마다 얼굴·의상 동일 / 숏 간 색온도·검은색 농도 차이 없음 / 이야기에 불필요한 구간 컷 / 현장음·음악 따로 정리해 믹스 / 릴스 화면비·안전영역 확인 후 자막 / 실존 인물 레퍼런스는 본인 동의와 사용 권리 확인.

## 문제 해결 (FAQ)
- 스킬이 자동 실행 안 됨: Customize → Skills에서 두 스킬 켜짐 + Settings → Capabilities 코드 실행 켜짐 확인, 새 세션에서 "Banana Pro Director 2.0을 사용해 주세요"처럼 스킬 이름을 직접 적기.
- 두 ZIP을 한 번에 올려도 되나: 안 됨. Dropbox 묶음 ZIP이 아니라 안쪽 두 ZIP을 각각 업로드.
- "Cinema World Build"로 검색해도 안 나옴: 정확한 이름은 Cinema Worldbuilder Pro 2.0 (`cinema-worldbuilder-pro-2.0.zip`).
- 프롬프트가 왜 영어: 최종 Seedance 프롬프트는 영어 출력으로 잠겨 있음. 대화는 한국어 가능, 코드 블록은 번역하지 말 것.
- 레퍼런스 최대: 이미지 9장(캐릭터·차량·소품처럼 유지할 대상은 플레이트에 보여도 별도 기준 이미지 권장).
- 긴 영상: 1회 최대 15초. 짧은 숏으로 나눠 같은 시트·플레이트를 반복 참조하고 편집기에서 연결.

## 핵심 팁 · 주의사항
- ⚠️ 실존 인물 사진은 사전 동의·사용 권리 필요 (ByteDance도 신원 확인이나 사전 법적 허가가 필요할 수 있다고 안내).
- 생성 비용은 별도(Higgsfield 크레딧). 스킬은 무료.
- 프롬프트 초 수 = Camera Capture 초 수 = Movement 구간 합 = 전체 런타임.
- 한 번에 변수 하나만 수정, 기준 시트는 함부로 바꾸지 않음.
- ❌ 얼굴과 스타일링을 한 번에 생성 ✅ 얼굴 잠금 → 의상 → 시트 순서
- Dropbox 등 외부에서 받은 스킬은 열기 전에 SKILL.md 확인.

## 바로 쓰는 체크리스트
- [ ] 두 스킬 업로드/설치 후 역할 설명 확인
- [ ] 얼굴·의상 기준 이미지 승인 (중간 회색 배경, 전신)
- [ ] 6패널 시트 + 장면 플레이트 생성
- [ ] Cinema Worldbuilder 출력의 10블록, 초 수, `@imageN` 번호 검증
- [ ] Seedance 생성 후 첫/마지막 프레임 비교
- [ ] 실패 요소 하나씩만 수정
- [ ] 편집기에서 연결·색보정·사운드·자막
- [ ] 실존 인물 사용 시 동의 확보
