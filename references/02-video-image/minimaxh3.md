# 미니맥스 H3 (무료 영상+소리 생성 AI)
- 원문: https://lazyowen.com/guides/minimaxh3
- 도구·주제: MiniMax H3 · 영상·소리 동시 생성
- 한 줄 요약: 영상과 효과음/대사/배경음을 한 번에 만드는 옴니 모델을 무료 체험판으로 써보고, 프롬프트 스킬과 로컬 실행(Pinokio+Wan2GP)까지 안내한다. (갱신 2026-08-27, 읽는 데 11분, 5단계 약 56분)

## 언제 쓰나
- 영상 AI는 화면만 만들어 소리를 따로 얹어야 했는데, 소리 포함 4~15초 영상을 한 번에 무료로 시험하고 싶을 때
- 사양: 4~15초, 24 FPS, 32kHz 스테레오, 효과음·대사·배경음 동시 생성, 대사 11개 언어 안정 지원(한국어 포함, 립싱크 맞음). 입력: 텍스트, 첫/끝 장면 이미지, 참고 영상·음성
- 옴니 모델 = 글·이미지·영상·소리를 한 모델이 같이 이해하고 만드는 모델

## 준비물 / 필요 도구 (이름 + 공식 링크)
- 공식 GitHub https://github.com/MiniMax-AI/MiniMax-H3 · 모델 가중치 https://huggingface.co/MiniMaxAI/MiniMax-H3
- 웹앱 https://hailuoai.video/tools/minimax-h3 · API 문서 https://platform.minimax.io/docs/api-reference/video-generation-v2-create
- 무료 체험판(Hugging Face Space): https://huggingface.co/spaces/multimodalart/minimax-h3 · https://huggingface.co/spaces/mrfakename/minimax-h3-ultra-fast
- 로컬(선택): Pinokio https://pinokio.computer/ · Wan2GP 앱 페이지 https://pinokio.co/apps/github-com-6morpheus6-wan2gp · Wan2GP https://github.com/deepbeepmeep/Wan2GP · ComfyUI https://docs.comfy.org/tutorials/video/minimax/minimax-h3
- 라이선스(MiniMax H3 Community License): https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE
- 스킬 설치용 Node.js 18 이상(위임 프롬프트 기준)

## 단계별 방법
**Quick Start**: 설치 없이 체험판 링크를 열고 프롬프트 입력. 예시 프롬프트 뼈대(영어): 비 오는 서울 밤거리, 젖은 아스팔트에 네온 반사 → 베이지 코트 여성이 검은 우산을 펴고 카메라 쪽으로 걸어옴 → 카메라는 눈높이에서 천천히 밀고 들어감 → 소리는 우산에 떨어지는 빗소리, 먼 차 소리, 물웅덩이 발소리. 성공하면 몇 분 안에 영상이 나오고 빗소리·발소리가 같이 들림.
스킬 한 줄 설치:
```
npx skills add https://github.com/MiniMax-AI/MiniMax-H3 --skill h3-prompt-writing
```
→ `.claude/skills/h3-prompt-writing` 생성.

1. **STEP 1 모델 이해 (2분)**: 위 "언제 쓰나"의 사양 참고. 소리를 따로 구해 편집 프로그램에 얹는 과정이 사라짐.
2. **STEP 2 브라우저 첫 영상 (5분)**: 체험판 두 곳 중 아무 데나. 무료 계정 로그인 시 일일 사용량 부여, 사람이 몰리면 대기, 소진 시 다음 날까지 대기(브라우저 방식의 유일한 한계). 보통 길이·화면 비율·첫 장면 이미지·생성 단계 수 설정 가능. 처음엔 **5초**로 여러 번 돌려 감을 잡고 길이를 늘리기.
3. **STEP 3 프롬프트 쓰는 법 (6분)** — 화면만 적으면 소리 자리가 비어 모델이 아무거나 채움. 4덩어리:
   | 덩어리 | 적을 것 | 예시 |
   |---|---|---|
   | 장면 | 어디에 무엇이 있는지 | 창가 자리 카페, 오후 햇빛 |
   | 인물 | 나이대·옷·표정·동작 | 베이지 코트를 입은 30대 여성이 컵을 내려놓는다 |
   | 카메라 | 다가가기/회전/고정 | 정면에서 천천히 다가간다 |
   | 소리 | 효과음·대사·배경음 | 창밖 빗소리, 잔이 접시에 닿는 소리 |
   - "멋있게", "감성적으로" 같은 형용사는 줄이고 눈에 보이고 귀에 들리는 것만. 요청 길이와 묘사 분량을 맞출 것(공식 가이드).
   - 참고 이미지·영상·음성은 `<Picture 1>`, `<Video 1>`, `<Audio 1>` 이름표를 쓰고 문단이 바뀌어도 같은 이름표 유지.
   - 스킬 설치 시 `h3-prompt-writing/references/`에 `base-en.txt`, `ref-en.txt` 생성. 이후 AI에게: "h3-prompt-writing 스킬을 따라 `<만들고 싶은 영상 한 줄>`을 5초짜리 H3 프롬프트로, 화면 설명과 소리 설명을 모두 넣어서".
4. **STEP 4 내 PC에서 돌리기 (선택, 40분)** — 브라우저 한도 없이 쓰고 싶을 때만. NVIDIA GPU 필수.
   ```
   nvidia-smi
   ```
   - 우측 상단 `MiB / MiB`로 VRAM 확인(8192MiB=8GB). `command not found`면 NVIDIA GPU/드라이버 없음.
   - 최적화 배포판 기준 5초 영상 VRAM 56GB, 15초 89GB. 원본 가중치는 한 종류만 받아도 140GB+, 다중 고성능 GPU 전제라 비권장.
   - 순서: Pinokio 설치·실행 → 앱 목록에서 Wan2GP 설치 → Start로 브라우저 화면 → 모델 목록에서 H3 선택: **FL2VA**(글/이미지로 새 장면) / **Ref2VA**(특정 인물·목소리 유지). 첫 실행은 다운로드 때문에 30분~수 시간. 흐리면 생성 단계 수 최소 15~20 확인.
5. **STEP 5 쓰기 전 확인 (3분)**
   - 주소: 모델 파일은 MiniMax-AI/MiniMax-H3(GitHub) 또는 MiniMaxAI/MiniMax-H3(HF)에서만. `.exe`/`.7z` 설치 파일을 받으라는 곳은 비공식.
   - 라이선스: 커뮤니티 라이선스의 적용 지역에서 한국·EU·영국·미국이 제외됨. 광고·판매 등 상업 사용 계획이면 원문 직접 확인.
   - 공식 API 영상은 자동 검수로 불법/권리 침해 요청이 차단될 수 있음.

**스킬 설치·검증 위임 프롬프트 뼈대(Claude Code)**: 역할=H3 프롬프트 스킬 설치·연결 검증 담당. 슬롯 `<운영체제와 셸>`, `<쓰는 AI 도구>`, `<목표 한 줄>`. 작업: ① `node --version` 18 이상 확인, `ls .claude/skills`로 `h3-prompt-writing` 존재 확인(있으면 재설치 말고 상태 보고) ② 없을 때만 위 `npx skills add ...` 실행 ③ `ls .claude/skills/h3-prompt-writing`에 SKILL.md, `references`에 `base-en.txt`·`ref-en.txt` 확인 후 스킬로 5초 예시 프롬프트 1개 생성 ④ H3가 무엇이고 어떤 순서로 쓰는지 5줄 이내 설명. 제약: 덮어쓰기/삭제 금지, 중복 설치 금지, `.env` 읽기·출력 금지, 예시에 소리 설명 필수. 출력: 실행 명령·Node 버전·새 폴더/파일·남은 오류·예시 프롬프트. 검증: references에 두 파일이 출력돼야 함, 실패 시 완료 보고 금지.

## 핵심 팁 · 주의사항
- 비용: 체험판 무료(일일 한도/대기), 로컬 소프트웨어 무료이나 고성능 GPU 필요, API 가격은 페이지에 없음(공식 문서 확인).
- ❌ 비공식 저장소/설치 파일 다운로드, ❌ 라이선스 확인 없이 상업 사용 — 무료 다운로드 가능 ≠ 내 지역에서 마음대로 사용 가능.
- 메모리 부족 시 길이·해상도부터 축소(15초→5초, 480p).

## 문제 해결
- 영상은 나오는데 소리 없음: 프롬프트에 소리 설명이 없는 경우가 대부분 → 화면 뒤에 소리 한 줄 추가.
- 체험판 계속 대기: 무료 GPU 공유 때문 → 다른 체험판으로 이동하거나 한가한 시간대.
- 같은 프롬프트인데 결과가 매번 다름: 짧을수록 모델이 채움 → 4덩어리 모두 작성.
- 한국어 대사 발음 이상: 대사를 따옴표로 감싸고 언어 명시, 한 영상에 2~3문장 이내.
- 로컬 메모리 부족 오류: 5초·480p로 먼저, 나중에 화질 상승.
- 설치 중간 멈춤: 모델 파일이 커서 네트워크 끊기면 정지 → 설치 재실행하면 대부분 이어받기.

## 바로 쓰는 체크리스트
- [ ] 체험판에서 5초 시험
- [ ] 장면/인물/카메라/소리 4부분 프롬프트
- [ ] (선택) `h3-prompt-writing` 스킬 설치, references 파일 2개 확인
- [ ] 로컬은 `nvidia-smi`로 VRAM(56GB/89GB 이상) 확인 후 판단
- [ ] 공식 저장소 주소만 사용
- [ ] 상업 사용 전 라이선스 지역 조건 확인
