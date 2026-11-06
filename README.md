# AIAdvisor

Claude Code 사용자를 위한 도구 추천 스킬입니다.

프로젝트와 이미 깔린 MCP·스킬·플러그인을 먼저 읽은 다음, 지금 필요한 것만 골라 우선순위와 실행 계획으로 정리합니다. 자동화·코딩·웹 디자인은 공식 문서와 GitHub로 확인한 도구 카탈로그(46개)와 단계별 레시피를 근거로 하고, 그 밖의 주제는 가이드 82편을 봅니다. 사용자가 번호를 고르기 전에는 아무것도 설치하지 않고, 고른 뒤에는 한 단계씩 확인하며 진행합니다.

**[데모 페이지](https://devvshyun.github.io/AIAdvisor/)** · [설치](#설치) · [쓰는 법](#쓰는-법) · [카탈로그와 레시피](#도구-카탈로그와-레시피) · [가이드 목록](references/README.md)

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
| 배포·점검을 자동으로 돌리고 싶음 | "배포랑 링크 점검 자동으로 돌게 하고 싶어" |
| 남이 만든 레포를 넘겨받음 | "인수받은 레포인데 구조 파악부터 도와줄 도구 있어?" |
| 새 프로젝트를 시작함 | "가계부 웹앱 새로 만들 건데 뭐 세팅하면 좋아?" |
| 딱히 떠오르지 않음 | "프로젝트에서 보완할 부분 추천해줘" |

`/project-upgrade-advisor`로 직접 불러도 됩니다.

스킬은 말한 내용과 폴더 상태를 보고 모드를 고릅니다.

- **보완 모드** (코드가 있는 프로젝트): 진단 요약 → 추천 작업 표 → 상위 3개 실행 계획 → 하지 말 것 → 다음 질문
- **신규 모드** (빈 폴더나 아이디어만 있을 때): 빠진 정보만 묻고 요약과 가정 → 단계별 시작 도구(지금 / 나중에) → 첫 주 세팅 계획 → 아직 이른 것 → 다음 질문
- **갱신 모드** ("카탈로그 갱신해줘"): 그날을 기준일로 도구를 다시 조사해 카탈로그를 바꿉니다. 절차는 [references/catalog/REFRESH.md](references/catalog/REFRESH.md)에 있습니다.

번호를 고르면 레시피를 한 단계씩 실행합니다. 단계마다 설치 명령과 위험을 먼저 보여 주고 승인을 받으며, 끝나면 확인 기준(파일, 명령 결과, 검사 0건 등)을 실제로 확인한 결과를 보여 준 뒤 다음 단계로 갈지 묻습니다.

## 동작 원칙

- 추천 단계에서는 읽기만 합니다. 설치, 설정 변경, 파일 수정은 번호를 고른 다음에 시작합니다.
- 이미 깔린 도구는 추천에서 뺍니다. 9Router와 OmniRoute처럼 역할이 같은 도구는 하나만 남깁니다.
- API 키, 계정 연결, 유료 플랜이 필요한 항목에는 따로 표시를 붙입니다. 자동매매는 모의 계좌 범위 안에서만 다룹니다.
- 카탈로그 항목마다 확인한 날짜가 있습니다. 30일이 넘은 항목은 버전, 무료 한도, 가격이 바뀌었을 수 있다고 표시합니다. 가이드는 2026-11-05 기준입니다.
- 관리가 멈춘 도구(`maintained: false`)는 추천하지 않습니다. 남이 만든 스킬은 Claude와 같은 권한으로 돌기 때문에, 처음 설치하는 것은 출처와 위험을 먼저 보여 줍니다.

## 도구 카탈로그와 레시피

자동화·코딩·웹 디자인 세 분야는 2026-11-06에 공식 문서와 GitHub를 직접 확인해 만든 카탈로그로 추천합니다.

| 분야 | 카탈로그 | 레시피 |
|---|---:|---|
| 웹 디자인 | [15개](references/catalog/web-design.yaml) | [AI 티 안 나는 랜딩·소개 페이지](references/recipes/web-design.md) |
| 코딩 | [19개](references/catalog/coding.yaml) | [기능 하나를 계획부터 병합까지](references/recipes/coding.md) |
| 자동화 | [12개](references/catalog/automation.yaml) | [배포·월간 건강 검사, 매주 리뷰하는 Claude](references/recipes/automation.md) |

- **카탈로그**는 도구 하나가 항목 하나입니다. 설치·확인 명령, 비용, 역할이 겹치는 도구, 권한·외부 전송 같은 위험, 관리 상태, 확인 날짜가 들어 있습니다. 형식은 [SCHEMA.md](references/catalog/SCHEMA.md), 바뀐 내용은 [CHANGELOG.md](references/catalog/CHANGELOG.md)에 있습니다.
- **레시피**는 도구를 엮는 순서입니다. 단계마다 넘길 것과 확인 기준, 그리고 이 저장소에서 직접 해 보며 겪은 일("써 보니")을 적었습니다. 웹 디자인 레시피는 데모 페이지를 실제로 그 순서대로 만들면서 썼습니다.
- 매달 1일 GitHub Actions가 카탈로그 도구들의 저장소가 보관되거나 오래 멈췄는지 확인하고, 문제가 있으면 이슈를 엽니다.

## 가이드 라이브러리

카탈로그에 없는 주제(영상, 프롬프트, 공부·리서치 등)는 `references/`의 가이드 82편을 봅니다. 모두 `언제 쓰나 → 준비물 → 단계별 방법 → 팁·주의사항 → 체크리스트` 순서로 쓰여 있고, 상황별로 찾으려면 [references/README.md](references/README.md)의 "상황별 빠른 찾기" 표를 보면 됩니다.

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
references/
  INDEX.md        스킬이 먼저 읽는 색인 (레시피, 카탈로그 id, 가이드 상황별 표)
  catalog/        도구 카탈로그, 형식, 갱신 절차, 변경 기록
  recipes/        분야별 레시피
  01-skills-mcp/… 가이드 82편 (README.md가 전체 목차)
scripts/
  build_demo.py   INDEX.md와 데모 페이지의 가이드 탐색기를 다시 만듦 (--check로 어긋남만 확인)
  check_catalog.py  카탈로그 형식 검사(--validate), 저장소 관리 상태 확인(--freshness)
evals/            스킬 평가 케이스 (skill-creator 형식)
.github/workflows/  데모 배포, 월간 카탈로그 점검
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
