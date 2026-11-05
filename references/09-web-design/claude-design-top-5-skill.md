# 디자인 스킬 5개 (클로드한테 디자인 시키기 전에 깔 것)
- 원문: https://lazyowen.com/guides/claude-design-top-5-skill
- 도구·주제: Claude Code + 스킬 5종 · AI 웹디자인 품질
- 한 줄 요약: Awesome DESIGN.md, Image to Code, Taste, agent-browser, Web Design Guidelines를 순서대로 설치해 디자인 고정→참고 이미지→탈 AI 스타일→자기 검증→배포 전 검사 흐름을 만든다. (2026-08-25 공개, 읽는 데 16분, 7단계 따라 하면 약 28분)

## 언제 쓰나
- 랜딩/포트폴리오 등 웹 화면을 클로드로 만들기 전 환경 세팅. 클로드가 매번 같은 글꼴·보라 그라데이션·카드 안의 카드를 내놓는 이유는 따라 할 기준·참고 화면·자기 확인 수단이 없기 때문.
- Taste는 보이는 게 중요한 화면용 — 대시보드/복잡한 데이터 표에는 쓰지 않음.

## 준비물 / 필요 도구 (이름 + 공식 링크)
- Node.js v22.20.0+ (브라우저 도구는 24+ 권장, https://nodejs.org/ LTS), Claude Code(https://claude.com/claude-code), 터미널(macOS 터미널 / Windows PowerShell)
- Awesome DESIGN.md (현재 74개 사이트 디자인 규칙, MIT): https://github.com/VoltAgent/awesome-design-md · 미리보기 https://getdesign.md/ · 형식 문서 https://stitch.withgoogle.com/docs/design-md/overview/
- Image to Code / Taste(design-taste-frontend, MIT): https://github.com/Leonxlnx/taste-skill · https://www.tasteskill.dev/ · Image to Code 문서 https://github.com/Leonxlnx/taste-skill/blob/main/skills/image-to-code-skill/SKILL.md
- agent-browser: https://agent-browser.dev/ · https://github.com/vercel-labs/agent-browser
- Web Design Guidelines(100+ 규칙, Vercel): https://github.com/vercel-labs/agent-skills (문서 https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md)
- 스킬 검색 https://skills.sh/
- 비용: 전부 무료(Claude 구독 외 추가 결제 없음)

## 단계별 방법
**Quick Start** — 프로젝트 폴더에서 한 줄씩(스킬 4개). 성공 시 `✓ design-taste-frontend (copied)`처럼 줄마다 표시.
```
npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend" --agent claude-code --yes --copy
npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill "image-to-code" --agent claude-code --yes --copy
npx --yes skills@latest add vercel-labs/agent-skills --skill "web-design-guidelines" --agent claude-code --yes --copy
npx --yes skills@latest add vercel-labs/agent-browser --agent claude-code --yes --copy
npm install -g agent-browser
agent-browser install
ls .claude/skills && agent-browser --version
```
(마지막 줄 성공 기준: 스킬 폴더 4개 이름 + 버전 번호)

1. **STEP 1 준비물 확인 (2분)**
   ```
   node --version
   claude --version
   ```
   - `v22.20.0` 이상. 낮거나 `command not found`면 nodejs.org LTS 설치 후 새 터미널. claude가 없으면 설치부터.
2. **STEP 2 Awesome Design — 기준 파일 먼저 (5분)** — 가장 먼저. 기준이 없으면 AI는 학습된 기본값으로 돌아가 나머지 네 개로도 결과가 거의 안 바뀜. DESIGN.md = 색·글꼴·간격·버튼 모양 규칙 메모 파일(AI가 화면 만들 때마다 먼저 읽음).
   ```
   curl -o DESIGN.md https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/linear.app/DESIGN.md
   head -20 DESIGN.md
   ```
   - 성공은 조용히 끝나고 `DESIGN.md` 생성(정상). `head`에서 색상 코드·글꼴 이름이 나오면 OK. 주소의 `linear.app`만 교체:
   | 느낌 | 이름 |
   |---|---|
   | 어둡고 절제된 제품 화면 | `linear.app` |
   | 따뜻한 크림색 편집 화면 | `claude` |
   | 흑백 대비 개발자 화면 | `vercel` |
   | 여백 넓은 프리미엄 | `apple` |
   | 초록 강조 다크 | `supabase` |
   - 요청 뼈대: 프로젝트 루트 `DESIGN.md`를 먼저 읽고 거기 정의된 색·글꼴·간격·버튼 스타일**만** 써서 `<만들 화면 설명>`을 만들 것, DESIGN.md에 없는 색/글꼴은 새로 만들지 말 것.
3. **STEP 3 Image to Code (4분)**: "이미지가 설계도, 코드는 그걸 옮기는 층" — 참고 화면 먼저 생성 → 설계도처럼 분석 → 코드. 설치:
   ```
   npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill "image-to-code" --agent claude-code --yes --copy
   ```
   - 성공: `✓ image-to-code (copied)` + `→ ./.claude/skills/image-to-code`. 사용(공식 권장):
   ```
   follow the skill: generate images, then analyze, then code
   <만들 화면 설명>
   ```
   - 규칙: 섹션이 여러 개면 한 장에 몰지 말고 **섹션마다 이미지 한 장**(글자가 작아지면 분석 불가). 일부가 잘 안 보이면 기존 이미지를 자르지 말고 **그 부분만 새로 생성**(자르면 간격·비율이 망가짐).
4. **STEP 4 Taste (4분)**: 배치·움직임 기준을 기본값에서 밀어냄. 설치:
   ```
   npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend" --agent claude-code --yes --copy
   ```
   - 저장소에 비슷한 스킬이 많아 `--skill` 필수(옵션 없으면 10개 넘게 설치). 다이얼 1~10:
   | 다이얼 | 기본 | 낮추면 | 올리면 |
   |---|---|---|---|
   | `DESIGN_VARIANCE` | 8 | 반듯한 대칭 | 과감한 비대칭 |
   | `MOTION_INTENSITY` | 6 | 거의 안 움직임 | 스크롤·물리 효과 |
   | `VISUAL_DENSITY` | 4 | 여백 넓음 | 정보 빽빽 |
   - 요청 시 숫자로 지정. 예: `DESIGN_VARIANCE`는 5, `MOTION_INTENSITY`는 3으로 낮춰 차분하고 읽기 쉽게. 막아 주는 AI 기본값: 보라 그라데이션, 어두운 배경 위 가운데 정렬 히어로, 똑같은 카드 세 장, 무작위 유리 효과, 끝없는 미세 애니메이션, Inter 글꼴.
5. **STEP 5 agent-browser — 자기 화면 보기 (6분)**: 스킬(안내문) + 명령줄 도구 둘 다 필요.
   ```
   npx --yes skills@latest add vercel-labs/agent-browser --agent claude-code --yes --copy
   npm install -g agent-browser
   agent-browser install
   agent-browser --version
   agent-browser doctor
   agent-browser install --with-deps
   ```
   - `agent-browser install`은 자동화 전용 크롬을 별도로 받음(평소 크롬 로그인·북마크 무영향). `doctor`는 크롬 설치 상태·네트워크 점검(안 될 때 먼저). `--with-deps`는 리눅스에서 시스템 파일이 부족해 실행 실패할 때만.
   - 요청 뼈대: 로컬 개발 서버를 띄운 뒤 agent-browser로 `<확인할 주소>`를 열어 캡처하고, DESIGN.md의 색·글꼴이 실제 적용됐는지 확인, 어긋나면 코드 수정 후 다시 캡처해 비교.
6. **STEP 6 Web Design Guidelines — 배포 전 검사 (4분)**: Vercel 웹 인터페이스 가이드라인 100+ 규칙(접근성, 포커스 상태, 폼, 애니메이션, 타이포, 이미지, 성능, 다크 모드)으로 코드 검사. 눈엔 멀쩡해도 키보드로 못 누르는 버튼, 라벨 없는 입력창, 대비 부족 글자를 잡음.
   ```
   npx --yes skills@latest add vercel-labs/agent-skills --skill "web-design-guidelines" --agent claude-code --yes --copy
   ```
   - 요청 뼈대: `web-design-guidelines` 스킬로 `<검사할 폴더>` 검사 → 지적 항목을 하나씩 수정하되 DESIGN.md의 색·글꼴 기준은 유지 → 전부 고친 뒤 같은 검사를 재실행해 남은 게 없는지 확인.
   - 출력은 파일/줄/문제 한 줄씩(예: `src/Button.tsx:42 - icon button missing aria-label`, `input lacks label`, `animation missing prefers-reduced-motion`), `✓ pass`=고칠 게 없음. 검사할 때마다 최신 규칙을 받아오므로 별도 업데이트 불필요.
7. **STEP 7 한 흐름으로 쓰기 (3분)**: 순서 = DESIGN.md(기준 고정) → Image to Code(참고 화면 생성·분석) → Taste(기본값 탈피) → agent-browser(실제 확인) → Web Design Guidelines(배포 전 검사).
   - 통합 요청 뼈대(Claude Code): `<만들 화면 설명>`을 ① 루트 DESIGN.md 읽고 색·글꼴 기준 파악 ② `image-to-code`로 참고 화면 생성·분석 ③ `design-taste-frontend` 기준으로 구현 ④ `agent-browser`로 실제 화면 캡처 후 어긋난 곳 수정 ⑤ `web-design-guidelines`로 검사 후 지적 수정, 각 단계 끝에 한 줄 보고.

**설치·검증 위임 프롬프트 뼈대(Claude Code)**: 역할=디자인 도구 5개 설치·연결 검증 담당. 슬롯 `<운영체제와 셸>`, `<기술 스택>`, `<목표 한 줄>`. 작업: ① `node --version` 22.20+ 확인, `ls .claude/skills`로 4개 스킬, DESIGN.md 존재 확인(있으면 재설치 말고 보고) ② 없는 것만 위 npx 명령 실행, agent-browser는 `npm install -g agent-browser` + `agent-browser install` ③ `ls .claude/skills`의 4개 폴더와 `agent-browser --version` 확인(DESIGN.md가 없으면 "기준 파일 아직 없음"으로 보고) ④ 다섯 개의 역할·순서를 5줄 이내로 설명. 제약: 덮어쓰기/삭제 금지, 중복 설치 금지, `.env` 읽기·출력 금지, 한 번에 하나씩 설치·확인. 실패 시 완료 보고 금지.

## 핵심 팁 · 주의사항
- 설치 후 Claude Code 완전 재시작해야 인식. `--skill "<이름>"` 필수(저장소 통째 설치 시 10개+ 설치). 처음엔 프로젝트 설치, 전역은 `-g`(`~/.claude/skills`).
- 결과를 가장 크게 바꾸는 건 STEP 2(기준 파일). 5개를 다 깔 필요 없이 하나씩 붙여도 됨.
- DESIGN.md에 담긴 건 로고·문구가 아니라 색값·글꼴 크기·간격 규칙. 그대로 써도 되지만 주색 하나만 내 브랜드 색으로 바꾸면 더 좋은 출발점.
- 순서가 어긋나면 앞 단계의 효과가 사라짐(기준 파일 없이 Taste만 깔면 결과가 거의 안 바뀜).
- 제거: `.claude/skills`의 해당 폴더 삭제, 브라우저 도구는 `npm uninstall -g agent-browser`.

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| `command not found: npx` | Node.js 없음 | nodejs.org LTS 설치 후 터미널 재시작 |
| 설치됐는데 클로드가 모름 | 재시작 전 | Claude Code 완전 종료·재실행 |
| 스킬이 여러 개 깔림 | `--skill` 없이 저장소 통째 설치 | `--skill "design-taste-frontend"`처럼 이름 지정 재설치 |
| 스킬 깔았는데 결과 그대로 | STEP 2 건너뜀 | DESIGN.md를 먼저 받아 프로젝트 루트에 |
| curl 후 파일이 비어 있음 | 사이트 이름 오타 | 주소의 이름을 저장소 폴더명(`linear.app` 등)과 일치 |
| agent-browser가 브라우저 못 엶 | CLI 미설치 | `npm install -g agent-browser` 후 `agent-browser install` |
| 리눅스에서 브라우저 실행 실패 | 시스템 파일 부족 | `agent-browser install --with-deps` |
| 검사 결과가 아무것도 안 나옴 | 고칠 게 없음 | 정상(`✓ pass`) |

## 바로 쓰는 체크리스트
- [ ] `node --version` ≥ 22.20 / `claude --version` 확인
- [ ] 스킬 3종(+agent-browser 스킬) 설치 + `npm install -g agent-browser` + `agent-browser install`, Claude Code 재시작
- [ ] DESIGN.md 다운로드 후 주색 변경
- [ ] Taste 다이얼 값 지정(변경 시 숫자로 명시)
- [ ] `ls .claude/skills` 4개 + `agent-browser --version` + `ls DESIGN.md` 확인
- [ ] 스크린샷 비교 후 Web Design Guidelines 통과(`✓ pass`)
