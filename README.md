# AIAdvisor

**Claude Code에 이제 뭘 더 깔지 고민될 때, 내 프로젝트를 먼저 읽고 필요한 것만 골라 주는 스킬입니다.**

AI 도구 가이드 82편을 주제별로 정리해 스킬 안에 넣어 두었습니다. 기존 프로젝트를 열어 두고 물어보면 약점을 찾아 우선순위를 매겨 주고, 새 프로젝트라면 처음부터 갖출 도구와 첫 주 세팅 계획을 짜 줍니다. 추천만 하고, 항목을 고르기 전에는 아무것도 설치하거나 바꾸지 않습니다.

[데모 페이지](https://devvshyun.github.io/AIAdvisor/) · [설치](#설치) · [가이드 목록](references/README.md)

---

## 이런 때 씁니다

| 상황 | 이렇게 말하면 됩니다 |
|---|---|
| 토큰이나 사용 한도가 빨리 바닥남 | "토큰이 너무 빨리 닳는데 뭐 깔면 좋을까" |
| 만든 화면이 AI가 만든 티가 남 | "UI가 너무 AI 같은데 보완할 방법 추천해줘" |
| 반복 작업을 줄이고 싶음 | "이 프로젝트에서 자동화할 만한 부분 찾아줘" |
| 새 프로젝트를 시작함 | "가계부 웹앱 새로 만들 건데 뭐 세팅하면 좋아?" |
| 딱히 떠오르지 않음 | "프로젝트에서 보완할 부분 추천해줘" (프로젝트를 읽고 알아서 진단) |

`/project-upgrade-advisor`로 직접 불러도 됩니다.

## 두 가지 모드

스킬이 상황을 보고 모드를 고릅니다. 애매하면 어느 모드로 진행할지 먼저 한 줄로 밝힙니다.

### 보완 모드: 기존 프로젝트
1. `CLAUDE.md`, README, 의존성 파일, git log, 지금 깔려 있는 MCP·스킬·플러그인을 읽습니다.
2. 사용자가 말한 고민을 1순위로 두고, 없으면 근거를 붙여 약점을 찾습니다.
3. 관련 있는 가이드만 열어 보고, 이미 설치됐거나 역할이 겹치는 도구는 걸러냅니다.
4. 결과를 아래 형식으로 정리합니다.

```
A. 진단 요약
B. 추천 작업 표 (보완 포인트 · 가이드 · 기대 효과 · 난이도 · 비용·리스크)
C. 상위 3개 실행 계획 (지금 OS에 맞춘 명령 + 완료 확인 방법)
D. 하지 말 것 / 보류할 것
E. 다음에 물어볼 것
```

### 신규 모드: 새 프로젝트
1. 무엇을 만드는지, 누가 쓰는지, 형태, 스택, 예산·기간 중 빠진 것만 한 번에 묻습니다.
2. 기획·검증 → 개발 환경 → 디자인·콘텐츠 → 배포·운영 단계로 도구를 묶고, 각각 "지금 필요"와 "나중에 필요하면"으로 나눕니다.
3. 결과를 아래 형식으로 정리합니다.

```
A. 프로젝트 요약과 가정
B. 단계별 시작 도구 세트
C. 첫 주 세팅 계획 (1일차부터, 설치 명령 + 확인 방법)
D. 처음부터 깔 필요 없는 것
E. 다음에 물어볼 것
```

두 모드 모두 "진행할 번호를 골라 주세요"로 끝납니다. 실제 설치는 그다음부터입니다.

## 설치

스킬 폴더 이름이 곧 스킬 이름이라서, 반드시 `project-upgrade-advisor` 폴더로 받아야 합니다.

**macOS · Linux · Git Bash**
```bash
git clone https://github.com/devvshyun/AIAdvisor.git ~/.claude/skills/project-upgrade-advisor
```

**Windows PowerShell**
```powershell
git clone https://github.com/devvshyun/AIAdvisor.git "$env:USERPROFILE\.claude\skills\project-upgrade-advisor"
```

설치한 뒤 Claude Code 세션을 새로 열면 스킬이 잡힙니다.

**클라우드 세션 (claude.ai/code)**: 클라우드 환경 설정의 설정 스크립트에 아래 한 줄을 넣으면 세션마다 최신 버전을 받습니다. 환경의 네트워크 접근에서 GitHub가 허용돼 있어야 합니다.
```bash
git clone --depth 1 https://github.com/devvshyun/AIAdvisor.git ~/.claude/skills/project-upgrade-advisor
```

### 업데이트
```bash
cd ~/.claude/skills/project-upgrade-advisor && git pull
```

## 동작 원칙

- **추천과 실행을 나눕니다.** 스킬은 설치, 설정 변경, 파일 수정을 하지 않습니다. 실행은 사용자가 번호를 고른 뒤에 시작합니다.
- **겹치지 않게 고릅니다.** 9Router와 OmniRoute처럼 역할이 같은 도구는 하나만 추천합니다.
- **이미 있는 건 뺍니다.** 설치된 MCP·스킬·플러그인을 먼저 확인합니다.
- **위험한 작업은 따로 표시합니다.** API 키, 계정 연결, 유료 플랜이 필요한 항목에 표시를 붙입니다. 자동매매 관련 내용은 모의 계좌 범위 안에서만 다룹니다.
- **날짜를 밝힙니다.** 가이드는 2026-11-05 기준입니다. 버전, 무료 한도, 가격은 바뀌었을 수 있어서 실행 전에 공식 문서를 확인하라고 안내합니다.

## 가이드 라이브러리

`references/`에 주제별로 82편이 들어 있습니다. 모든 가이드는 `언제 쓰나 → 준비물 → 단계별 방법 → 팁·주의사항 → 체크리스트` 구조입니다.

| 주제 | 편수 | 예시 |
|---|---:|---|
| [스킬·MCP](references/01-skills-mcp/) | 12 | 필수 MCP 5개, 스킬 TOP 5, ECC 에이전트 팀 |
| [영상·이미지](references/02-video-image/) | 14 | Higgsfield 명령어, 모션 그래픽, 무료 영상 AI |
| [자동화](references/03-automation/) | 16 | 메일 답장 위임, n8n 첫 에이전트, 업무를 파일로 옮기기 |
| [프롬프트](references/04-prompts/) | 8 | 발표 자료 프롬프트, 아첨 줄이는 설정 |
| [코딩](references/05-coding/) | 4 | 세션 명령어 5개, 바이브 코딩 필수 도구 |
| [비용 절약](references/06-cost-saving/) | 11 | 토큰 절약 도구, Graphify, 모델 폴백, 무료 서버 |
| [공부·리서치](references/07-study-research/) | 5 | NotebookLM 세컨드 브레인, 유튜브를 스킬로 |
| [비즈니스](references/08-business/) | 4 | 아이디어 검토 에이전트, 연락처 수집 |
| [웹 디자인](references/09-web-design/) | 4 | AI 티 안 나는 웹사이트, 디자인 스킬 5개 |
| [글쓰기](references/10-writing/) | 2 | AI 표식 지우기, 이야기 구조로 본 AI 글 |
| [기타](references/99-etc/) | 2 | 무료 LLM API 연결 |

상황별로 찾으려면 [references/README.md](references/README.md)의 "상황별 빠른 찾기" 표를 보세요.

## 저장소 구조

```
SKILL.md        스킬 정의: 모드 판단, 진행 순서, 출력 형식, 규칙
references/     가이드 82편과 목차
docs/           데모 페이지 (GitHub Pages)
```

스킬을 쓸 수 없는 환경에서는 `SKILL.md` 본문을 대화에 붙여넣고 `references/` 경로를 실제 위치로 바꿔서 쓰면 됩니다.
