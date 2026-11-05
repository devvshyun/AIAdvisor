# 클로드 코드 필수 스킬 5개
- 도구·주제: Claude Code · 스킬 설치 (브라우저/탐색/디자인/MCP/작업 관리)
- 한 줄 요약: agent-browser, find-skills, design-taste-frontend, mcp-builder, GSD 5개를 npx 한 줄씩 설치하고 `ls`로 확인한 뒤 작은 요청으로 실사용 점검.

## 언제 쓰나
- Claude가 만든 화면을 직접 확인 못 하고, 긴 대화에서 앞 내용을 놓치고, 디자인이 매번 비슷하게 나올 때
- 모델 탓이 아니라 붙어 있는 기능이 없어서 생기는 문제를 무료 스킬로 메우는 가이드
- (갱신 2026-08-13, 읽는 데 13분, 7단계 약 21분. 스킬 설치 자체에 추가 구독료 없음)

## 준비물 / 필요 도구
| 도구 | 역할 | 링크 |
|---|---|---|
| agent-browser | 브라우저 자동화(열기·클릭·입력·캡처) | https://agent-browser.dev/ · https://github.com/vercel-labs/agent-browser |
| find-skills | 공개 스킬 검색·추천·설치 | https://github.com/vercel-labs/skills · 검색 https://skills.sh/ |
| design-taste-frontend | 프론트 디자인 기준 | https://github.com/Leonxlnx/taste-skill · https://tasteskill.dev/ |
| mcp-builder | MCP 서버 생성 | https://github.com/anthropics/skills |
| GSD (gsd-core) | 큰 작업 단계화·결정 기록·단계별 새 대화 실행 | https://opengsd.net/ · https://github.com/open-gsd/gsd-core |
- Node.js 22.20 이상(https://nodejs.org/ LTS), Claude Code(https://claude.com/claude-code), 터미널(macOS 터미널 / Windows PowerShell)
- 스킬 문서: https://code.claude.com/docs/en/skills , agent-browser 스킬 문서 https://agent-browser.dev/skills

## 단계별 방법
**Quick Start**: 작업할 프로젝트 폴더로 이동해 아래 4줄(스킬 4개)을 붙여넣고, GSD는 따로 설치. 성공하면 `✓ agent-browser (copied)`처럼 항목별 한 줄씩 나옴.
```
npx --yes skills@latest add vercel-labs/agent-browser --agent claude-code --yes --copy
npx --yes skills@latest add vercel-labs/skills --skill find-skills --agent claude-code --yes --copy
npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend --agent claude-code --yes --copy
npx --yes skills@latest add anthropics/skills --skill mcp-builder --agent claude-code --yes --copy
npx --yes @opengsd/gsd-core@latest --claude --global
```

1. **STEP 1 준비물 확인 (2분)**
   ```
   node --version
   claude --version
   ```
   - `v22.20.0`처럼 v로 시작, 앞자리 22 이상이어야 함. 낮거나 없으면 nodejs.org LTS 설치. claude 명령이 없으면 claude.com/claude-code에서 설치.
2. **STEP 2 스킬 개념 (2분)**: 스킬 = 폴더 하나에 `SKILL.md` 하나가 든 작업 지침서. 매번 붙여넣는 프롬프트가 아니라 설치해 두면 Claude가 필요할 때 꺼내 읽음.
   | 설치 위치 | 명령어 | 범위 |
   |---|---|---|
   | 이 프로젝트만 | 옵션 없음(`.claude/skills`) | 지금 폴더에서만 |
   | 계정 전체 | `-g` 추가(`~/.claude/skills`) | 어느 폴더든 |
   - 처음엔 프로젝트 설치로 시작, 마음에 들면 `-g`로 재설치.
3. **STEP 3 agent-browser (3분)** — 스킬(안내문) + 명령줄 도구 둘 다 필요
   ```
   npx --yes skills@latest add vercel-labs/agent-browser --agent claude-code --yes --copy
   npm install -g agent-browser
   agent-browser install
   agent-browser --version
   ```
   - 성공 시 `→ ./.claude/skills/agent-browser` 경로 표시. `agent-browser install`은 자동화 전용 크롬을 따로 내려받음(평소 크롬의 로그인·북마크에 영향 없음).
   - 리눅스에서 시스템 파일 부족으로 실패 시: `agent-browser install --with-deps`
   - 사용 예 요청: 로컬 개발 서버를 띄우고 agent-browser로 첫 화면 열기 → 회원가입 폼을 실제로 채워 제출 → 막히면 캡처해서 원인 보고.
4. **STEP 4 나머지 세 스킬 (4분)** (MCP = Claude가 외부 서비스와 대화하는 공통 규격, 그 연결 프로그램 = 서버)
   ```
   npx --yes skills@latest add vercel-labs/skills --skill find-skills --agent claude-code --yes --copy
   npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend --agent claude-code --yes --copy
   npx --yes skills@latest add anthropics/skills --skill mcp-builder --agent claude-code --yes --copy
   ```
   - 각각 `✓ 이름 (copied)` 확인. Taste는 저장소에 비슷한 스킬이 여럿이라 `--skill`로 하나만 지정.
5. **STEP 5 GSD (3분)** — 스킬만이 아니라 명령어·작업 기록 폴더까지 넣는 전용 설치 프로그램
   ```
   npx --yes @opengsd/gsd-core@latest --claude --global
   npx --yes @opengsd/gsd-core@latest --claude --global --profile=core
   ```
   - 첫 줄=전체, 둘째 줄=가벼운 구성. 현재 프로젝트에만 넣으려면 `--global` 대신 `--local`. 마지막에 `Done!`.
   - Claude Code를 완전히 종료 후 재시작, 그다음 입력:
   ```
   /gsd-new-project
   ```
   - 무엇을 만들지 묻는 질문이 나오면 성공. 기존 프로젝트에는 `/gsd-onboard`.
   - 예전 저장소는 2026-06 보관(archive) 처리 → 현재는 `@opengsd/gsd-core`가 이어받음.
6. **STEP 6 설치 확인 (2분)** — 스킬은 조용히 설치되므로 목록을 직접 확인
   ```
   ls .claude/skills
   ls ~/.claude/skills
   npx --yes @opengsd/gsd-core@latest --help
   ```
   - 첫 줄(프로젝트 설치) 또는 둘째 줄(계정 전체)에서 `agent-browser`, `design-taste-frontend`, `find-skills`, `mcp-builder` 4개가 보이면 정상. GSD는 `--help`에서 버전 번호·사용법 출력.
   - 빠진 이름이 있으면 그 줄만 재실행(설치된 건 유지됨).
7. **STEP 7 실사용 점검 (5분)** — Claude Code에서 작은 요청부터. 요청 뼈대:
   - 스킬 목록 점검: 설치된 스킬 목록을 확인해 각각 한 줄 설명, 파일 수정 금지.
   - 브라우저: `agent-browser로 [확인할 주소]` 열어 첫 화면 캡처, 버튼·링크 실제 동작 확인, 문제 위치 보고.
   - 스킬 탐색: `[하고 싶은 작업]`용 기존 스킬이 있는지 찾고 설치 수·제작자까지 알려 달라.
   - 디자인: `[만들 화면 설명]`을 디자인 스킬 기준으로 만들되 보라·파랑 그라데이션 배경, 카드 안의 카드, 바운스 효과는 금지.
   - MCP: `[연결할 서비스]`의 공식 API 문서 주소 `[문서 주소]`를 주고 MCP 서버 생성 후 실제 연결 확인.

**설치·검증 위임용 프롬프트 뼈대(Claude Code에 붙여넣기)**
- 역할: 스킬 5개 설치·연결 검증 담당. 맥락: 아직 미설치일 수 있음.
- 입력 슬롯: `<운영체제와 셸>`, `<기술 스택>`, `<목표 한 줄>`
- 작업 4단계: ① `node --version` 22.20 이상 확인, `ls .claude/skills`·`ls ~/.claude/skills`로 4개 스킬 존재 확인, `ls ~/.claude/commands/gsd-help.md`로 GSD 확인(있으면 재설치 말고 상태만 보고) ② 없는 것만 위 설치 명령 실행 ③ `ls .claude/skills` 4개 이름 + GSD `--help` 버전 출력 확인, agent-browser CLI는 `npm install -g agent-browser && agent-browser install` 후 `--version` ④ 다섯 개가 각각 무엇을 하는지 초보자용 5줄 이내 설명
- 제약: 기존 파일·설정 덮어쓰기/삭제 금지, 중복 설치 금지, `.env` 등 비밀키 파일 읽기·출력 금지, 스킬 원본 임의 수정 금지
- 출력: 실행한 명령 목록, Node 버전, 새로 생긴 폴더·파일, 남은 오류. 하나라도 실패하면 완료로 보고하지 말고 실패 명령·원인·다음 조치 제시.

## 핵심 팁 · 주의사항
- ❌ Taste 저장소를 `--skill` 없이 설치하면 비슷한 스킬 4개가 한꺼번에 설치됨 → ✅ `--skill design-taste-frontend` 로 하나만 재설치.
- ❌ 이름만 쓰면 못 찾음 → ✅ `owner/repo` 형식 + `--skill`로 이름 지정.
- agent-browser는 스킬 파일만으론 동작 안 함. npm 패키지(`npm install -g agent-browser`)와 `agent-browser install` 필수.
- 설치 후 Claude Code를 완전히 종료했다 다시 켜야 인식. `/gsd-` 미인식 = GSD 미설치 또는 재시작 전.
- 다섯 개는 역할이 겹치지 않아 함께 깔아도 충돌하지 않음: 브라우저=확인, 탐색=찾는 시간 단축, GSD=긴 대화에서 결정을 파일로 보존, 디자인=AI 기본값 탈피, MCP=외부 서비스 연결.
- 구 GSD 저장소는 갱신 중단 — `@opengsd/gsd-core` 사용.

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| `command not found: npx` | Node.js 없음 | nodejs.org LTS 설치 후 터미널 재시작 |
| 설치됐는데 Claude가 모름 | 재시작 전 | Claude Code 완전 종료 후 재실행 |
| 스킬을 찾을 수 없음 | 저장소 주소 없이 이름만 입력 | `owner/repo` + `--skill` |
| Taste 후 비슷한 스킬 여러 개 | 저장소 통째 설치 | `--skill design-taste-frontend`로 재설치 |
| `/gsd-` 명령 못 알아들음 | GSD 미설치/재시작 전 | `npx @opengsd/gsd-core@latest --help` 확인 후 재시작 |
| agent-browser가 브라우저 못 엶 | CLI 미설치 | `npm install -g agent-browser` → `agent-browser install` |
| 리눅스에서 브라우저 실행 실패 | 시스템 파일 부족 | `agent-browser install --with-deps` |

## 바로 쓰는 체크리스트
- [ ] `node --version` ≥ 22.20, `claude --version` 확인
- [ ] agent-browser 스킬 + `npm install -g agent-browser` + `agent-browser install` + `--version`
- [ ] find-skills / design-taste-frontend(`--skill` 지정) / mcp-builder 설치
- [ ] `npx --yes @opengsd/gsd-core@latest --claude --global` 후 Claude Code 완전 재시작
- [ ] `ls .claude/skills`에 4개 이름, GSD `--help` 버전 출력 확인
- [ ] `/gsd-new-project` 인식 확인
- [ ] 스킬 목록·화면 캡처·스킬 탐색·디자인·MCP 생성을 작은 요청으로 점검
