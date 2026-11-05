# 클로드가 유튜브·레딧·깃허브를 무료로 긁어오게 만드는 도구
- 원문: https://lazyowen.com/guides/agent-reach
- 도구·주제: Agent Reach(CLI) + Claude Code · 리서치용 데이터 수집
- 한 줄 요약: 클로드가 기본 상태에선 못 읽는 유튜브 자막·레딧·엑스 등의 통로를 무료 도구 하나로 열어 주고, 어떤 통로가 열렸는지 점검한 뒤 여러 통로를 엮은 조사를 시키는 방법. (2026-09-04 공개, 읽는 데 11분, 따라 하면 약 36분, STEP 8개)

## 언제 쓰나
- 클로드가 유튜브 자막을 못 받고, 레딧은 접근이 막히고, 엑스는 유료 API를 요구하는 문제를 해결하고 싶을 때
- 여러 채널을 묶어 조사하고 출처 주소가 붙은 요약·비교표·콘텐츠 소재 발굴을 하고 싶을 때

## 준비물 / 필요 도구
- Agent Reach: https://github.com/Panniantong/Agent-Reach (플랫폼마다 지금 가장 잘 되는 방법을 골라 설치하고 상태를 점검해 주는 도구. 직접 긁어오는 것이 아님)
  - 한국어 설명서: https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_ko.md
  - 영어 설명서: https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md
  - 설치 안내: https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md
  - 문제 해결: https://github.com/Panniantong/Agent-Reach/blob/main/docs/troubleshooting.md
  - 쿠키 내보내기: https://github.com/Panniantong/Agent-Reach/blob/main/docs/cookie-export.md
- Python 3.10 이상: https://www.python.org/downloads/
- pipx(파이썬 명령어 도구를 서로 안 부딪치게 따로 설치): https://pipx.pypa.io/stable/installation/
- 내부 도구 참고: yt-dlp(유튜브 자막) https://github.com/yt-dlp/yt-dlp · jina-ai/reader(웹페이지 읽기) https://github.com/jina-ai/reader · GitHub CLI https://cli.github.com
- Claude Code 또는 커서 등 AI 도구, 터미널(macOS 터미널 / Windows PowerShell)
- 용어: 채널 = 도구가 관리하는 플랫폼 하나하나, 쿠키 = 브라우저가 "이미 로그인한 사람"이라고 기억하는 값(비밀번호와 같은 힘)
- 통로 묶음
| 묶음 | 어디까지 되나 | 준비물 |
|---|---|---|
| 깔면 바로 | 유튜브 자막, 깃허브, 웹페이지, RSS | 없음 |
| 로그인 필요 | 레딧, 엑스, 링크드인 | 내 계정 로그인 또는 쿠키 |

## 단계별 방법
### 프롬프트 뼈대 A. 설치·검증 위임 (Claude Code에 붙여넣기, 선택)
- 목적: Agent Reach 설치 여부 확인 → 설치 → `doctor`로 통로 검증
- 역할: Agent Reach 설치·연결 검증 담당
- 슬롯: [운영체제와 셸], [내가 쓰는 AI 도구], [목표 한 줄(예: 유튜브·깃허브 조사)]
- 작업 4단계: ① `agent-reach --version`, `python3 --version` 확인(이미 있으면 재설치 말고 버전만, 파이썬이 3.10 미만이면 중단) ② 미설치 시 `pipx install https://github.com/Panniantong/agent-reach/archive/main.zip`(pipx가 없으면 `python3 -m venv ~/.agent-reach-venv`로 가상환경 후 그 안에서 pip), 이어서 검사만 하는 `agent-reach install --env=auto` ③ `agent-reach doctor` 출력을 그대로 보고하고 맨 아래 "Status: N/9 channels available"의 숫자와 막힌 통로의 원인·해결을 정리(시스템을 바꾸는 `--system` 옵션은 먼저 묻고 승인 후에만) ④ 도구 설명과 사용법을 5줄 이내로
- 제약: 임의 sudo 금지, 쿠키·토큰 값 출력 금지, 작업 중인 프로젝트 폴더 안에 저장소 복제·파일 생성 금지(설정은 `~/.agent-reach/`에만)
- 출력: 실행 명령 목록, `doctor` 결과 그대로, 사용 가능한 통로 개수, 남은 오류
- 검증: `doctor`에서 유튜브·깃허브·웹페이지·RSS가 ✅. 하나라도 실패하면 완료 보고 금지, 실패한 명령·원인·다음 조치 제시

### Quick Start
1. 설치
```bash
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
```
마지막 줄에 `installed package agent-reach`가 보이면 성공.
2. 환경 검사(시스템은 바뀌지 않음, 빠진 프로그램이 있으면 목록으로 안내)
```bash
agent-reach install --env=auto
```
3. 열린 통로 확인: `✅ Ready to use` 아래에 깃허브·유튜브·RSS·웹페이지가 뜨면 준비 끝
```bash
agent-reach doctor
```

### STEP 1. 준비물 확인 (2분)
```bash
python3 --version
pipx --version
```
Python 3.10 이상, pipx 버전 숫자가 나오면 준비 끝. `command not found`면 python.org 또는 pipx 공식 안내로 먼저 설치.

### STEP 2. 이 도구가 하는 일 알기 (1분)
클로드는 원래 배운 내용만으로 답한다. 이 도구는 플랫폼마다 가장 잘 되는 방법을 골라 깔아 주고 상태를 점검한다(위 통로 묶음 표 참고).

### STEP 3. 설치하기 (3분)
1. 공식 저장소에서 설치(이름이 같은 다른 패키지가 파이썬 저장소에 있으니 위 주소 그대로)
```bash
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
```
`installed package agent-reach`와 `agent-reach` 명령 추가 줄이 나오면 성공.
2. 맥에서 `externally-managed-environment` 오류(파이썬이 스스로를 보호하는 상태)면 가상환경으로 설치. 프롬프트 앞에 `(.agent-reach-venv)`가 붙으면 가상환경 안.
```bash
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
```
3. 상태 검사(검사만 함)
```bash
agent-reach install --env=auto
```

### STEP 4. 열린 통로 확인 (2분)
설치 메시지는 "깔렸다"일 뿐이라 실제 통신은 따로 본다.
```bash
agent-reach doctor
```
출력 예(목록과 숫자는 환경에 따라 다름):
```
👁️  Agent Reach Status
========================================

✅ Ready to use:
✅ GitHub repos and code
✅ YouTube video subtitles
✅ Bilibili search & video detail
✅ RSS/Atom feeds
✅ Web pages (any URL)

🔍 Search:
⬜ Web semantic search

🔧 Configurable:
⚠️  Twitter/X — needs credentials
⬜ Reddit posts and comments — needs login

Status: 6/9 channels available
```
✅ = 지금 사용 가능, ⬜ = 아직 안 켠 것, ⚠️ = 설정 덜 됨. ⬜가 많아도 고장이 아니며 안 쓰는 통로는 안 켜도 된다.

### STEP 5. 유튜브 영상부터 시켜 보기 (5분)
유튜브는 로그인이 필요 없어 첫 시도로 가장 좋다. Claude Code(또는 커서)에 붙여넣고 꺾쇠를 내 영상 주소로 교체.

프롬프트 뼈대 B. 유튜브 자막 요약 + 도구 목록
- 슬롯: [유튜브 영상 주소]
- 요청: 자막을 받아 핵심 다섯 개로 정리, 영상에서 실제로 쓰라고 한 도구 이름만 목록으로 추출, 자막을 못 받으면 이유를 알려 달라
- 자막이 비었다고 나오면 그 영상에 자막이 없는 것 → 자동 자막이 켜진 다른 영상으로 재시도

깃허브(로그인 없이 가능) 저장소 비교 요청 예:
```
<깃허브 저장소 주소> 이 저장소가 뭘 하는 도구인지 읽어 보고,
비슷한 도구 세 개를 검색해서 별 개수와 최근 업데이트 날짜로 비교표를 만들어 줘.
```

### STEP 6. 로그인이 필요한 통로 열기 (10분, 선택)
커뮤니티 반응이나 엑스 글이 필요한 사람만. 계정이 잠길 위험이 있으니 주계정 말고 별도 계정을 쓴다(플랫폼이 자동 접근을 감지하면 계정을 막을 수 있음).
1. 레딧(익명 접근 불가, 로그인 상태 필수). 데스크톱이면 브라우저에 이미 로그인한 상태를 빌려 쓰는 쪽이 간단. 시스템을 바꾸는 명령이므로 승인 후에만. 끝나면 화면에 안내가 나오며, 데스크톱이면 크롬 확장을 깔고 레딧에 로그인하는 것까지.
```bash
agent-reach install --env=auto --system --channels=reddit
```
2. 엑스: 브라우저에서 꺼낸 쿠키 값 필요(입력 칸에 값이 표시되지 않음). 꺼내는 법은 쿠키 안내 문서(docs/cookie-export.md). 쿠키는 비밀번호와 같은 힘이라 남에게 보내면 안 된다.
```bash
agent-reach configure twitter-cookies
```
3. 설정이 끝나면 `agent-reach doctor`를 다시 실행해 ✅로 바뀌었는지 확인.

### STEP 7. 조사 한 번에 끝내기 (10분)
프롬프트 뼈대 C. 통합 조사 브리핑
- 슬롯: [유튜브 영상 주소], [내 주제 또는 제품 이름]
- 단계 5개: ① 영상 자막을 받아 핵심 다섯 개로 정리 ② 주제에 대해 사람들이 실제로 불평하는 내용을 커뮤니티에서 찾아 주제별로 묶기 ③ 같은 주제의 최근 글 세 개를 찾아 다수 의견과 반대 의견 구분 ④ 위 셋을 합쳐 브리핑 하나로, 문장마다 출처 주소 부착 ⑤ 막힌 통로가 있으면 다른 통로로 대체하고 어디를 썼는지 표시
- 팁: 마지막 5번이 핵심. 없으면 한 곳이 막혔을 때 빈손으로 돌아옴.

콘텐츠 소재 찾기 조합:
```
1. <내 분야> 관련해서 최근에 사람들이 가장 많이 묻는 질문을 커뮤니티에서 찾아 줘.
2. 그중 답이 애매하거나 의견이 갈리는 질문 다섯 개만 골라 줘.
3. 각 질문마다 왜 헷갈리는지 한 줄로 설명해 줘.
```
실제 사람들이 쓴 문장에서 뽑은 목록이라 소재로 바로 사용 가능.

### STEP 8. 상태 유지하기 (3분, 한 달에 한 번)
플랫폼이 접근 방식을 바꾸면 잘 되던 통로가 막힐 수 있다. 문제 없으면 정상이라는 짧은 줄, 막힌 통로가 있으면 무엇이 왜 막혔는지 안내.
```bash
agent-reach watch
```
업데이트가 필요하면 AI에게 아래를 그대로 전달(AI가 문서를 읽고 진행)
```
Agent Reach를 최신 버전으로 업데이트해 줘:
https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md
```

## 핵심 팁 · 주의사항
- 레딧·엑스·링크드인은 별도 계정 사용, 쿠키는 비밀번호와 같으니 공유 금지, `--system` 명령은 승인 후에만
- 쿠키가 불안하면 안 넣어도 됨: 유튜브·깃허브·웹페이지·RSS 넷만으로 조사 대부분 가능
- AI가 도구를 안 쓰고 아는 내용만 말하면 문장에 주소·플랫폼 이름을 넣기("유튜브 자막을 받아서", "커뮤니티에서 찾아서")
- 이름이 같은 다른 패키지가 있으니 지정 URL로만 설치
- 도구 제거: `agent-reach uninstall`(설정·저장값 정리) 후 `pipx uninstall agent-reach`

## 문제 해결
- `command not found: agent-reach`: 터미널을 완전히 닫았다 다시 열기, 그래도 안 되면 `pipx ensurepath` 실행 후 새 터미널
- `externally-managed-environment`: 파이썬이 시스템 보호 중, pipx 또는 STEP 3의 가상환경 방법 사용
- 유튜브 자막이 비어서 옴: 대부분 자막이 없는 영상, 자동 자막이 있는 다른 영상으로 시도하거나 AI에게 "다른 통로로 대체해 줘"
- 레딧이 계속 ⬜: 익명 접근이 막혀 있어 STEP 6으로 로그인 상태 연결 필요

## 바로 쓰는 체크리스트
- [ ] Python 3.10+ / pipx 확인
- [ ] 지정 URL로 pipx 설치 → `agent-reach install --env=auto`
- [ ] `agent-reach doctor`에서 유튜브·깃허브·웹페이지·RSS ✅ 확인
- [ ] 유튜브 영상 하나로 요약 테스트
- [ ] 필요한 통로만 추가 설정(별도 계정 사용)
- [ ] 프롬프트에 "어디서 볼지 + 출처 URL 첨부 + 막히면 대체" 명시
- [ ] 월 1회 `agent-reach watch`
