# AIAdvisor

Claude Code 사용자를 위한 도구 추천 스킬입니다.

프로젝트와 이미 깔린 MCP·스킬·플러그인을 먼저 읽은 다음, 스킬에 들어 있는 가이드 82편 중에서 지금 필요한 것만 골라 우선순위와 실행 계획으로 정리합니다. 사용자가 번호를 고르기 전에는 아무것도 설치하지 않습니다.

**[데모 페이지](https://devvshyun.github.io/AIAdvisor/)** · [설치](#설치) · [쓰는 법](#쓰는-법) · [가이드 목록](references/README.md)

## 이렇게 답합니다

프로젝트 폴더에서 Claude Code를 열고 이렇게 물으면,

```
> 토큰이 너무 빨리 닳는데 뭐 깔면 좋을까
```

스킬이 CLAUDE.md, package.json, git log, `claude mcp list`를 읽고 이런 형식으로 답합니다.

```
A. 진단 요약   파일을 넓게 읽고, 기획 PDF를 그대로 첨부하고 있음

B. 추천 작업 표
   1  토큰 절약 도구 3개    탐색량·전송량 줄이기      중 · 30분   무료
   2  MarkItDown           PDF를 마크다운으로 변환   하 · 10분   무료
   3  세션 명령어 5개       되감기·요약               하 · 10분   없음
   4  9Router 폴백         한도에 걸리면 백업 모델   중 · 30분   백업 키 필요

C. 상위 3개 실행 계획   지금 OS에 맞춘 설치 명령과 완료 확인 방법
D. 하지 말 것          9Router와 OmniRoute 함께 설치 (역할이 같음)
E. 다음 질문           첨부하는 PDF가 매번 같은 문서인가요?

진행할 번호를 골라 주세요.
```

다른 상황의 예시 다섯 가지는 [데모 페이지](https://devvshyun.github.io/AIAdvisor/#demo)에서 눌러 볼 수 있습니다.

## 설치

스킬 폴더 이름이 곧 스킬 이름이라서 `project-upgrade-advisor` 폴더로 받아야 합니다. 받은 뒤 Claude Code 세션을 새로 열면 스킬이 잡힙니다.

**macOS · Linux · Git Bash**

```bash
git clone https://github.com/devvshyun/AIAdvisor.git ~/.claude/skills/project-upgrade-advisor
```

**Windows PowerShell**

```powershell
git clone https://github.com/devvshyun/AIAdvisor.git "$env:USERPROFILE\.claude\skills\project-upgrade-advisor"
```

**클라우드 세션 (claude.ai/code)**: 클라우드 환경 설정 스크립트에 넣으면 세션마다 최신 버전을 받습니다. 네트워크 접근에서 GitHub가 허용돼 있어야 합니다.

```bash
git clone --depth 1 https://github.com/devvshyun/AIAdvisor.git ~/.claude/skills/project-upgrade-advisor
```

| 하려는 일 | 명령 |
|---|---|
| 설치 확인 | `ls ~/.claude/skills/project-upgrade-advisor` (SKILL.md가 보이면 끝) |
| 업데이트 | `cd ~/.claude/skills/project-upgrade-advisor && git pull` |
| 삭제 | `~/.claude/skills/project-upgrade-advisor` 폴더를 지우면 끝. 다른 설정은 건드리지 않습니다 |

## 쓰는 법

| 상황 | 이렇게 물어보세요 |
|---|---|
| 토큰이나 사용 한도가 빨리 바닥남 | "토큰이 너무 빨리 닳는데 뭐 깔면 좋을까" |
| 만든 화면이 AI가 만든 티가 남 | "UI가 너무 AI 같은데 보완할 방법 추천해줘" |
| 반복 작업을 줄이고 싶음 | "이 프로젝트에서 자동화할 만한 부분 찾아줘" |
| 남이 만든 레포를 넘겨받음 | "인수받은 레포인데 구조 파악부터 도와줄 도구 있어?" |
| 새 프로젝트를 시작함 | "가계부 웹앱 새로 만들 건데 뭐 세팅하면 좋아?" |
| 딱히 떠오르지 않음 | "프로젝트에서 보완할 부분 추천해줘" |

`/project-upgrade-advisor`로 직접 불러도 됩니다.

스킬은 말한 내용과 폴더 상태를 보고 두 모드 중 하나를 고릅니다.

- **보완 모드** (코드가 있는 프로젝트): 진단 요약 → 추천 작업 표 → 상위 3개 실행 계획 → 하지 말 것 → 다음 질문
- **신규 모드** (빈 폴더나 아이디어만 있을 때): 빠진 정보만 묻고 요약과 가정 → 단계별 시작 도구(지금 / 나중에) → 첫 주 세팅 계획 → 아직 이른 것 → 다음 질문

## 동작 원칙

- 추천 단계에서는 읽기만 합니다. 설치, 설정 변경, 파일 수정은 번호를 고른 다음에 시작합니다.
- 이미 깔린 도구는 추천에서 뺍니다. 9Router와 OmniRoute처럼 역할이 같은 도구는 하나만 남깁니다.
- API 키, 계정 연결, 유료 플랜이 필요한 항목에는 따로 표시를 붙입니다. 자동매매는 모의 계좌 범위 안에서만 다룹니다.
- 가이드는 2026-11-05 기준입니다. 버전, 무료 한도, 가격은 바뀔 수 있어서 실행 전에 공식 문서를 확인하라고 안내합니다.

## 가이드 라이브러리

`references/`에 82편이 주제별로 들어 있습니다. 모두 `언제 쓰나 → 준비물 → 단계별 방법 → 팁·주의사항 → 체크리스트` 순서로 쓰여 있고, 상황별로 찾으려면 [references/README.md](references/README.md)의 "상황별 빠른 찾기" 표를 보면 됩니다.

| 주제 | 편수 | 예시 |
|---|---:|---|
| [스킬·MCP](references/01-skills-mcp/) | 12 | 필수 MCP 5개, ECC 에이전트 팀 |
| [영상·이미지](references/02-video-image/) | 14 | Higgsfield 명령어, 모션 그래픽 프롬프트 |
| [자동화](references/03-automation/) | 16 | 메일 답장 위임, n8n 첫 에이전트 |
| [프롬프트](references/04-prompts/) | 8 | 발표 자료 프롬프트, 아첨 줄이는 설정 |
| [코딩](references/05-coding/) | 4 | 세션 명령어 5개, 바이브 코딩 도구 |
| [비용 절약](references/06-cost-saving/) | 11 | 토큰 절약 도구, 모델 폴백, 무료 서버 |
| [공부·리서치](references/07-study-research/) | 5 | NotebookLM 세컨드 브레인 |
| [비즈니스](references/08-business/) | 4 | 아이디어 검토 에이전트, 연락처 수집 |
| [웹 디자인](references/09-web-design/) | 4 | AI 티 안 나는 웹사이트, 디자인 스킬 5개 |
| [글쓰기](references/10-writing/) | 2 | AI 표식 지우기 |
| [기타](references/99-etc/) | 2 | 무료 LLM API 연결 |

## 저장소 구조

```
SKILL.md          스킬 정의: 모드 판단, 진행 순서, 출력 형식, 규칙
PRODUCT.md        데모 페이지의 제품 맥락 (누가, 무엇을, 어떤 말투로)
references/       가이드 82편과 목차
docs/             데모 페이지 (GitHub Pages)
  index.html
  DESIGN.md       데모 페이지의 디자인 기준과 뽑은 조합
  assets/         taste-skill 키트 파일 (MIT)
```

## 데모 페이지

[devvshyun.github.io/AIAdvisor](https://devvshyun.github.io/AIAdvisor/)는 이 스킬이 추천하는 웹 디자인 가이드대로 만들었습니다. AIAdvisor에게 먼저 조언을 받고, 추천된 taste-skill 키트의 스크립트로 팔레트, 서체 조합, 히어로 구성을 뽑았습니다. 무엇을 어떻게 뽑았는지는 [docs/DESIGN.md](docs/DESIGN.md)에 있습니다.

로컬에서 보려면 저장소 폴더에서 아래 명령을 실행하고 `http://localhost:8000`을 엽니다.

```bash
python -m http.server 8000 --directory docs
```

## 라이선스

`docs/assets/`의 키트 파일은 [taste-skill](https://github.com/Leonxlnx/taste-skill)(MIT, © 2026 Leonxlnx)에서 가져왔고, 라이선스 전문은 [docs/assets/LICENSE-taste-skill.txt](docs/assets/LICENSE-taste-skill.txt)에 있습니다.
