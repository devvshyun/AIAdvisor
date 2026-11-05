# 클로드 세션 명령어 5개
- 원문: https://lazyowen.com/guides/claude-code-session-commands-5
- 도구·주제: Claude Code · 세션 관리 명령어 (/btw, /recap, ESC 두 번(/rewind), /branch, Ctrl+S)
- 한 줄 요약: 대화에 남기지 않는 질문, 한 줄 요약, 되감기, 갈림길, 프롬프트 보관 5가지와 git 저장 지점을 함께 쓰는 법. (2026-10-17 공개, 읽는 데 11분, 5단계 약 8분)

## 언제 쓰나
- 긴 Claude Code 작업 중 대화가 꼬였을 때 처음부터 다시 설명하지 않고 질문·복구·분기하고 싶을 때
- 모두 **터미널의 Claude Code 세션 입력창**에서만 동작(claude.ai 웹/앱 대화창에선 동작 안 함). 세션=켜서 끌 때까지 이어지는 대화 한 묶음.

## 준비물 / 필요 도구
- Claude Code (Anthropic 제작, 공식 저장소 https://github.com/anthropics/claude-code 스타 15만+, 오픈소스 아님·상용 약관). 문서: 명령어 https://code.claude.com/docs/en/commands · /btw·/recap https://code.claude.com/docs/en/interactive-mode · 되감기 https://code.claude.com/docs/en/checkpointing · 세션/분기 https://code.claude.com/docs/en/sessions · 단축키 https://code.claude.com/docs/en/keybindings · 설치 https://code.claude.com/docs/en/quickstart
- git (맥에서 없으면 개발자 도구 설치 창이 뜸 → 설치 후 재실행)
- macOS 13.0+, Windows 10 1809+, Ubuntu 20.04+, RAM 4GB+, Pro/Max/Team/Enterprise 구독 또는 Console 계정. 다섯 명령어는 기본 기능이라 추가 결제 없음.

## 단계별 방법
**설치·확인**
```bash
claude --version
curl -fsSL https://claude.ai/install.sh | bash     # macOS/Linux
# Windows PowerShell:
# irm https://claude.ai/install.ps1 | iex
```
설치 후 새 터미널에서 `claude --version`(예: `2.1.302 (Claude Code)`). `command not found`면 설치부터. 입력창 = 터미널에서 `claude` 실행 시 가로줄 두 개 사이 `>` 줄.

**시작 전 안전망: git 저장 지점** — 되감기로 돌아오지 않는 파일이 있어, 일 맡기기 전에 커밋 하나 만들어 두기.
```bash
git status
git init
git add .
git commit -m "되감기 전 저장"
git status
```
- `git status`에 `On branch main` 등이 보이면 저장소, `fatal: not a git repository`면 `git init`부터(이미 저장소면 `git add .`부터). 성공: `nothing to commit, working tree clean`.
- `Author identity unknown`이 나오면 이름·메일 등록 후 commit 재실행:
```bash
git config --global user.name "내 이름"
git config --global user.email "me@example.com"
```
- `.env` 같은 비밀키 파일은 커밋 전에 클로드에게 커밋에서 빼 달라고 할 것.

1. **STEP 1 `/btw` — 딴 질문 (1분)**
   - ❌ 그냥 "아까 그 설정 파일 이름 뭐였지?"를 보내면 질문·답이 대화 기록에 남음. ✅
   ```
   /btw 아까 그 설정 파일 이름 뭐였지?
   ```
   - 답이 터미널 위쪽 별도 오버레이에 뜨고 원래 대화에는 추가되지 않음. Space/Enter/Esc로 닫음. 클로드가 작업 중에도 입력 가능, 하던 작업은 멈추지 않음. 오버레이에서 `c`=답 복사. `/btw`는 이미 대화에 있는 내용으로만 답하므로, 파일을 새로 열거나 검색해야 하면 오버레이에서 `f`(대화를 이어받은 별도 작업(서브에이전트)이 도구를 써서 이어 감, 진행은 입력창 아래 패널). 질문 없이 `/btw`만 치면 닫은 답을 다시 봄.
2. **STEP 2 `/recap` — 돌아왔을 때 (1분)**
   ```
   /recap
   ```
   - 이번 세션에서 한 일을 400자 안쪽으로 요약. 마지막 답 이후 3분 지나고 터미널을 다른 창에 둔 채면 자동 표시(대화가 3번 이상 오간 세션만, 새 세션에서 안 보이는 건 정상). 거슬리면 `/config`에서 Session recap 끄기(명령은 계속 사용 가능).
3. **STEP 3 ESC 두 번 — 되감기 (3분)**: 요청을 보낼 때마다 직전 파일 상태가 저장됨.
   - ❌ "아까 거 취소하고 원래대로 해 줘"(그 말까지 대화에 쌓임) → ✅ 입력창을 **비운 뒤** ESC 두 번(글자가 남아 있으면 글자만 지워지며, 위 화살표로 복구). `/rewind`로도 같은 메뉴. 보낸 요청 목록에서 돌아갈 지점을 고르고:
   | 메뉴 | 하는 일 |
   |---|---|
   | Restore code and conversation | 파일·대화 둘 다 그 요청 전으로 |
   | Restore conversation | 대화만, 파일은 현재 그대로 |
   | Restore code | 파일만, 대화는 그대로 |
   | Summarize from here | 그 지점 이후 대화를 요약 압축 |
   | Summarize up to here | 그 지점까지를 요약 압축, 이후는 유지 |
   | Never mind | 변경 없이 나가기 |
   - 대화를 되돌리면 그때 보낸 요청이 입력창에 다시 들어옴 → 고쳐서 재전송.
   - 되감은 직후엔 클로드가 옛 파일 상태를 기억할 수 있음. 첫 메시지(프롬프트 뼈대): 방금 앞 지점으로 되감았으니 그 뒤에 시도한 방법은 잊을 것 / 파일을 고치기 전에 고칠 파일을 다시 읽을 것 / 지금 할 일·이미 끝난 것·다음에 바꿀 한 가지를 세 줄로 알릴 것 / 내가 확인하기 전에는 파일 수정 금지. → 파일을 다시 읽고 3줄 요약 후 대기하면 성공.
4. **STEP 4 `/branch` — 다른 방향 (2분)**: 현재 대화를 복사해 갈림길을 만들고 원래 대화는 보존.
   - ❌ 이름 없는 `/branch`(첫 요청 문장으로 이름이 붙어 헷갈림) → ✅
   ```
   /branch new-design
   ```
   - 성공: 세션 ID 두 개(새 갈림길 + 원래)가 보이고 이후 대화는 갈림길에서 진행. 원래로 돌아가려면 `/resume` → 목록에서 선택.
   - 갈라지기 전에 클로드에게 메모를 부탁하면 좋음(프롬프트 뼈대): 왜 갈라지는지 / 지금까지 안 된 이유 / 중요한 파일 / 다음에 해 볼 방법 두 개를 150단어 이내로, 파일은 수정 금지. 갈림길에서 그 메모부터 읽고 시작.
5. **STEP 5 `Ctrl+S` — 프롬프트 보관 (1분)**: 입력창에 글자가 있을 때 Ctrl+S → 글자가 사라지고 입력창이 빔 → 다른 질문/명령 처리 → 빈 입력창에서 Ctrl+S 한 번 더 → 쓰던 글·커서 위치·붙여넣은 내용까지 복원. 맥도 Cmd가 아니라 Ctrl. STEP 1과 조합: Ctrl+S로 치우고 `/btw` 질문 → 오버레이 닫기 → Ctrl+S로 복원하면 원래 대화에 흔적이 남지 않음.

**상황별 선택표(손대는 범위 작은 순)**
| 지금 상황 | 쓸 것 |
|---|---|
| 프롬프트 쓰다가 다른 걸 먼저 확인 | Ctrl+S |
| 대화에 안 남기고 하나만 질문 | `/btw 질문` |
| 자리 비웠다 와서 어디까지 했는지 모름 | `/recap` |
| 마지막 요청 결과가 마음에 안 듦 | 빈 입력창에서 ESC 두 번 |
| 지금 대화는 두고 다른 방법도 시도 | `/branch 이름` |
| 클로드가 터미널 명령·서브에이전트로 파일을 바꿈 | git 커밋으로 되돌리기 |

**학습·안전망 위임 프롬프트 뼈대(Claude Code 첫 메시지)**: 역할=세션 명령어 5개를 알려 주는 담당(초보자 대상), 맥락=되감기는 터미널 명령으로 바뀐 파일을 못 되돌린다고 들음. 슬롯 `내 작업 = <지금 하려는 일 한 가지>`. 작업: ① `claude --version`, `git status`로 저장소 여부 확인 ② 저장소가 아니거나 미저장 변경이 있으면 **먼저 물어본 뒤** `git init` 또는 `git add .` + `git commit -m "되감기 전 저장"` ③ `git status` 재확인 ④ 내 작업 기준으로 다섯 명령어를 언제 쓰는지 한 줄씩. 제약: 폴더를 바꾸는 명령은 실행 전 질문, `.env` 값 출력 금지·커밋에서 제외, 덮어쓰기/삭제 금지. 검증: 버전 숫자 + 마지막 `git status`가 `nothing to commit, working tree clean`. 실패 시 완료 보고 금지.

## 핵심 팁 · 주의사항
- 되감기는 클로드가 **파일 편집 기능**으로 고친 파일만 복원. ❌ `rm`/`mv`/`cp` 같은 터미널 명령으로 지우거나 옮긴 파일, 백그라운드 작업(서브에이전트)이 바꾼 파일은 대부분 복원 안 됨 → ✅ git 저장 지점으로 복구. 큰 작업 전에는 커밋을 한 번 더.
- ESC 두 번은 입력창이 비어 있어야 메뉴가 열림.
- 되돌리고 싶은 순간엔 저장하기 늦음 → 시작 전 커밋.

## 바로 쓰는 체크리스트
- [ ] 작업 폴더 git 저장 지점 커밋(`working tree clean` 확인)
- [ ] `claude --version` 확인
- [ ] `/btw`, `/recap`, `/branch 이름` 한 번씩 시험
- [ ] 빈 입력창에서 ESC 두 번(/rewind) 메뉴 옵션 확인
- [ ] Ctrl+S 보관/복원 시험
- [ ] 터미널 명령·서브에이전트로 바뀐 파일은 git으로 복구
