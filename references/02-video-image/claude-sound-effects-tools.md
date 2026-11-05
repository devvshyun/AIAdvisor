# 클로드 효과음 도구 3개 (오픈버스 API · 리얼 SFX · 이어샷)
- 도구·주제: Claude Code + Openverse API / real-sfx 스킬 / earshot · 영상 효과음 (STEP 3개)
- 한 줄 요약: 공개 효과음 검색(Openverse), 영상에 실제 녹음 효과음을 맞는 프레임에 삽입(real-sfx), 맞는 소리가 없을 때 코드로 생성(earshot) 세 도구를 설치해 Claude Code에 연결한다. 모두 무료, 코드는 MIT.

## 언제 쓰나
- 클로드가 모션그래픽·영상 편집은 잘하는데 효과음이 아쉬울 때: 영상에 맞는 효과음을 찾아 넣거나, 맞는 소리가 없을 때 새로 만들고 싶을 때

## 준비물 / 필요 도구
- Claude Code, Python 3.9+ (earshot은 3.10+, 없으면 https://www.python.org/downloads/), ffmpeg(ffprobe 포함, https://ffmpeg.org/download.html), Node.js(real-sfx `--uisfx` 쓸 때만)
- Openverse API: https://api.openverse.org/v1/ · https://github.com/WordPress/openverse (워드프레스 운영, 스타 423개). 키 없이 익명 한도 내 사용, 공개 오디오 500만+ (Freesound, Wikimedia 등)
- real-sfx: https://github.com/Clipwing/skills/tree/main/skills/real-sfx (Clipwing 제작)
- earshot: https://github.com/Leonxlnx/earshot (스타 3,100여 개 오픈소스)
- 코드는 모두 MIT, 받는 소리 파일 라이선스는 파일마다 다름(CC0, CC BY 등). 비용 모두 무료.
- 용어: API=프로그램끼리 정보 주고받는 창구 / 스킬=`~/.claude/skills`에 넣으면 클로드가 꺼내 쓰는 방법 폴더 / venv=폴더 전용 파이썬 환경 / torch=earshot의 판단용 계산 라이브러리 / MCP=클로드 코드가 외부 도구를 부르는 방식 / CC0=출처 표시 없이 자유 이용

## 단계별 방법
### 보조 프롬프트: 3개 일괄 설치 (프롬프트 뼈대)
- 역할: 효과음 도구 3개 설치·연결 검증 담당. 맥락: 초보자, 아무것도 없을 수 있음. 슬롯: [효과음 넣을 영상]. OS·파이썬·ffmpeg는 묻지 말고 직접 확인.
- 작업: `python3 --version`, `ffmpeg -version` 확인 → 없는 것만 설치(오픈버스는 `mkdir -p ~/sounds`만, real-sfx는 아래 복사+init, earshot은 README 순서+`claude mcp add`) → 명령으로 검증 → 각 도구 역할 안내.
- 제약: sudo·brew·전역 설정 수정 전 질문, 비밀키 출력 금지, 덮어쓰기 금지. 출력: 실행 명령·버전·바뀐 파일·남은 오류. 검증: curl 결과에 `result_count`, `setup.py check`에 `uisfx ok`, `earshot doctor`에 `earshot looks healthy`. 하나라도 실패하면 완료 보고 금지.

### Quick Start. Openverse 동작 테스트
응답까지 1분 가까이 걸릴 수 있음.
```bash
curl -s "https://api.openverse.org/v1/audio/?q=whoosh&source=freesound&license=cc0&page_size=3"
```
`{"result_count":`로 시작하는 결과가 보이면 성공.

### STEP 0/1. 환경 확인 + Openverse로 효과음 받기
```bash
python3 --version
ffmpeg -version
node -v
mkdir -p ~/sounds
```
- Node 없으면 아래 init 명령에서 `--uisfx`를 뺀다. ffmpeg 없으면 먼저 설치.
- 검색·다운로드는 클로드에게 맡김. 프롬프트 뼈대: `https://api.openverse.org/v1/audio/`로 검색, 슬롯 [소리가 필요한 장면], 조건 source=freesound·license=cc0, 장면보다 긴 소리 제외, 후보 3개의 제목·길이·라이선스·원작자·원본 링크를 표로 → 내가 고른 1개만 `~/sounds`에 다운로드 → 라이선스·원작자를 `~/sounds/LICENSES.md`에 한 줄씩 기록.
- 성공: 후보 표가 나오고 `~/sounds`에 파일과 `LICENSES.md` 생성.
- 30초 넘게 걸리거나 오류면 잠시 뒤 재시도.

### STEP 2. real-sfx 스킬 설치
이미 `~/.claude/skills/real-sfx`가 있으면 복사 블록 생략.
```bash
git clone https://github.com/Clipwing/skills ~/clipwing-skills
mkdir -p ~/.claude/skills
cp -R ~/clipwing-skills/skills/real-sfx ~/.claude/skills/real-sfx
ls ~/.claude/skills/real-sfx        # SKILL.md가 보이면 OK
```
`~/sounds`를 라이브러리로 연결:
```bash
cd ~/.claude/skills/real-sfx
python3 scripts/setup.py init --library main="$HOME/sounds" --uisfx --index
python3 scripts/setup.py check
```
- 성공: `config written: … (1 libraries)` 와 `uisfx ok`. `--uisfx`는 인터페이스 효과음 78개(CC0)를 함께 받음(뺐다면 config written만 확인).
- (선택, 맥) 프레임 시트·음높이 조절까지 쓰려면 ffmpeg-full. brew 없으면 https://brew.sh. export는 이 터미널 창에서만 유효하니 같은 창에서 claude 실행, 새 창이면 재실행.
```bash
brew install ffmpeg-full
export PATH="$(brew --prefix ffmpeg-full)/bin:$PATH"
which ffmpeg
```
- 설치 후 클로드 코드를 다시 열고 "이 영상에 효과음 넣어 줘".

### STEP 3. earshot 설치·연결
1~2분 소요. 파이썬 3.10+ 필요.
```bash
git clone https://github.com/Leonxlnx/earshot ~/earshot
cd ~/earshot
python3 -m venv .venv
.venv/bin/python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -e ".[mcp,llm,dev]"
.venv/bin/python -m earshot doctor     # 첫 줄 끝 "earshot looks healthy"
```
MCP 등록 + 스킬 복사:
```bash
claude mcp add earshot --scope user -e EARSHOT_THREADS=3 -- "$HOME/earshot/.venv/bin/python" -m earshot mcp
mkdir -p ~/.claude/skills
cp -R ~/earshot/skills/earshot ~/.claude/skills/earshot
claude mcp list        # earshot 보이면 등록됨 → 이후 Claude Code 재시작
```
테스트 렌더:
```bash
cd ~/earshot
.venv/bin/earshot sfx render whoosh_fast/whip -o whoosh.wav
```
성공: `wrote whoosh.wav: whoosh_fast/whip` … `checks: clean`. `~/earshot/whoosh.wav` 재생하면 휙 소리.

## 핵심 팁 · 주의사항
- ⚠️ earshot 첫 실행 시 판단 모델 약 1.1GB 다운로드 → 디스크 여유 확인
- ❌ CC BY 소리를 출처 없이 사용 ✅ 영상 설명에 원작자 표기, `LICENSES.md`에 기록
- 파이썬 3.9 이하면 earshot용 3.10+ 별도 설치
- Node 없으면 `--uisfx` 제외
- Openverse는 키 없이 쓰면 익명 사용 한도 적용

## 바로 쓰는 체크리스트
- [ ] Python/ffmpeg(/Node) 확인
- [ ] Openverse curl 테스트, `~/sounds` 생성
- [ ] real-sfx 복사 후 `setup.py init`/`check` (`uisfx ok`)
- [ ] earshot venv 설치, `doctor` 통과
- [ ] `claude mcp add earshot` 후 Claude Code 재시작, `claude mcp list` 확인
- [ ] 테스트 렌더 성공, 라이선스 기록
