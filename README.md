# AIAdvisor (project-upgrade-advisor 스킬)

Claude Code 스킬입니다. `references/`에 정리해 둔 AI 도구 가이드 82편을 근거로 두 가지 모드로 동작합니다.

- **보완 모드**: 지금 작업 중인 프로젝트를 점검하고, 필요한 도구와 작업을 우선순위 목록으로 정리합니다.
- **신규 모드**: 새로 만들 프로젝트의 아이디어를 듣고, 단계별 시작 도구 세트와 첫 주 세팅 계획을 짜 줍니다.

## 설치 (새 PC)

스킬 폴더 이름이 곧 스킬 이름이라서, 반드시 `project-upgrade-advisor` 폴더로 받아야 합니다.

macOS / Linux / Git Bash:
```bash
git clone https://github.com/devvshyun/AIAdvisor.git ~/.claude/skills/project-upgrade-advisor
```

Windows PowerShell:
```powershell
git clone https://github.com/devvshyun/AIAdvisor.git "$env:USERPROFILE\.claude\skills\project-upgrade-advisor"
```

설치한 뒤에는 Claude Code 세션을 새로 열어야 스킬이 잡힙니다.

## 업데이트

```bash
cd ~/.claude/skills/project-upgrade-advisor && git pull
```

어느 PC에서 고쳤든 `git commit` → `git push`로 올리고, 다른 PC에서는 `git pull`로 받으면 됩니다.

## 사용법

아무 세션에서 이렇게 말하면 됩니다. `/project-upgrade-advisor`로 직접 불러도 됩니다.

**보완 모드** (기존 프로젝트 폴더에서)
- "나 지금 프로젝트에서 보완하고 싶은 부분이 있는데, 추천해줘"
- "토큰이 너무 빨리 닳는데 뭐 깔면 좋을까"

결과: 진단 요약 → 추천 작업 표 → 상위 3개 실행 계획 → 하지 말 것 → 추가로 물어볼 것

**신규 모드** (빈 폴더에서, 또는 아이디어만 있을 때)
- "새 프로젝트 시작하는데 뭐 세팅하면 좋아? 가계부 웹앱 만들 거야"
- "유튜브 쇼츠 자동으로 만드는 걸 해보려는데 도구 추천해줘"

결과: 요약과 가정 → 단계별 시작 도구 세트(지금 / 나중에) → 첫 주 세팅 계획 → 처음부터 깔 필요 없는 것 → 추가로 물어볼 것

두 모드 모두 항목을 고르기 전에는 아무것도 설치하거나 바꾸지 않습니다.

스킬을 쓸 수 없는 환경에서는 `SKILL.md` 본문을 붙여넣고, `references/` 경로를 실제 위치로 바꿔서 쓰면 됩니다.

## 구성

```
SKILL.md          스킬 정의 (진행 순서, 출력 형식, 규칙)
references/
  README.md       상황별 빠른 찾기, 반복해서 나오는 도구, 전체 목차
  01-skills-mcp/ ... 99-etc/   가이드 82편 (주제별)
```

## 출처

가이드는 [lazyowen.com/guides](https://lazyowen.com/guides)의 내용을 개인 참고용으로 요약·재구성한 것입니다. 기준일은 2026-11-05입니다.
