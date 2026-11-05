# Claude Code 필수 설정 4개, 한 번에 붙이는 퀵 가이드
- 원문: https://lazyowen.com/guides/claudeskill
- 도구·주제: ECC · Ponytail · Claude-Mem (Claude Code 플러그인) + Obsidian · 스킬/플러그인 + 메모리 보관함 (2026-08-06 갱신, STEP 6개, 약 9분)
- 한 줄 요약: 플러그인 3개와 Obsidian 보관함을 셸 블록 하나로 한 번에 설치·연결하고, 결과 확인과 첫 작업까지 마무리하는 퀵 가이드.

## 언제 쓰나
- 개발 흐름 확장(ECC), 과잉 구현 억제(Ponytail), 세션 기억(Claude-Mem), 노트 보관(Obsidian)을 한꺼번에 세팅하고 싶을 때
- 터미널 조작이 가능한 AI 에이전트(Claude, Claude Code, Codex 등)에게 설치·설정·검증을 한 흐름으로 맡기고 싶을 때

## 준비물 / 필요 도구
- Claude Code 2.1 이상 (ECC 요구) — https://claude.com/claude-code
- Node.js 20.12 이상 + npm/npx (Claude-Mem 요구) — https://nodejs.org/
- macOS/Linux 터미널 (Quick Start 셸 블록 기준)
- ECC: https://github.com/affaan-m/ecc · https://ecc.tools
- Ponytail: https://github.com/DietrichGebert/ponytail · 벤치마크 https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md
- Claude-Mem: https://github.com/thedotmack/claude-mem · 설치 문서 https://docs.claude-mem.ai/installation
- Obsidian: https://obsidian.md/download · 보관함 https://help.obsidian.md/vault
- 플러그인 문서: https://code.claude.com/docs/en/discover-plugins
- 가격 정보는 페이지에 없음. 용어: 플러그인 "사용자 범위" = 로그인한 계정의 모든 Claude Code 프로젝트에서 같은 플러그인을 쓰는 설치 방식

## 단계별 방법
**AI에게 맡기기 프롬프트 뼈대** (터미널 조작 가능한 에이전트에 전달)
- 목적/역할: 플러그인 3개 설치 + Obsidian 보관함 연결을 맡는 시스템 설정 전문가
- 채울 곳: [보관함 폴더 경로, 예: ~/Documents/ClaudeVault], [운영체제: macOS 또는 Linux]
- 작업 순서: (1) `node --version`, `npx --version`, `claude --version`으로 Node 20.12+/Claude Code 2.1+ 확인, 미달이면 아무것도 설치하지 말고 공식 업데이트 링크만 안내 (2) 아래 6개 plugin 명령을 사용자 범위로 순서대로 실행 (3) `npx --yes claude-mem@latest repair` (4) 보관함 경로 생성, `CLAUDE.md`·`00-시작.md`는 없을 때만 생성 (5) Obsidian 설치 여부 확인, 미설치면 임의 패키지 관리자로 깔지 말고 공식 링크 + `Open folder as vault` 방법 안내 (6) `claude plugin list --json`과 `npx --yes claude-mem@latest doctor` 실제 실행으로 검증
- 제약: 기존 파일·설정 파괴 금지, ECC가 수동 설치돼 있으면 중복 설치 말고 보고, `npm install -g` 금지, .env·자격 증명·키·비밀번호 파일 읽기/출력 금지, Codex 등 다른 에이전트여도 플러그인은 Claude Code에 설치되는 것임을 명시, 기존 `CLAUDE.md`/`00-시작.md`는 존재 여부만 확인하고 덮어쓰지 않기
- 출력: 설치된 플러그인 목록, 보관함 위치, 검증 결과, Obsidian에서 직접 할 마지막 한 단계. 검증 증거로 list 결과와 doctor 실행 화면 제시

**Quick Start 셸 블록** (macOS/Linux, 재실행해도 이미 등록된 항목은 그대로 둠)
```bash
set -Eeuo pipefail
command -v claude >/dev/null || { echo "Claude Code가 필요합니다: https://claude.com/claude-code"; exit 1; }
command -v node >/dev/null || { echo "Node.js 20.12 이상이 필요합니다: https://nodejs.org/"; exit 1; }
command -v npx >/dev/null || { echo "npm/npx가 필요합니다: https://nodejs.org/"; exit 1; }
node -e 'const v=process.versions.node.split(".").map(Number); if(v[0]<20 || (v[0]===20 && v[1]<12)){console.error(`Node.js 20.12 이상이 필요합니다. 현재 ${process.versions.node}`);process.exit(1)}'
node -e 'const m=process.argv[1].match(/(\d+)\.(\d+)\.(\d+)/); if(!m || +m[1]<2 || (+m[1]===2 && +m[2]<1)){console.error(`Claude Code 2.1 이상이 필요합니다. 현재 ${process.argv[1]}`);process.exit(1)}' "$(claude --version)"
claude plugin marketplace add affaan-m/ECC --scope user
claude plugin install ecc@ecc --scope user
claude plugin marketplace add DietrichGebert/ponytail --scope user
claude plugin install ponytail@ponytail --scope user
claude plugin marketplace add thedotmack/claude-mem --scope user
claude plugin install claude-mem@thedotmack --scope user
npx --yes claude-mem@latest repair
VAULT="${CLAUDE_VAULT:-$HOME/Documents/ClaudeVault}"
mkdir -p "$VAULT"
if [ ! -e "$VAULT/CLAUDE.md" ]; then
  printf '%s\n' \
    '# Obsidian 보관함 작업 규칙' \
    '- 새 기록은 Markdown으로 작성합니다.' \
    '- 관련 기록은 [[노트 이름]]으로 연결합니다.' \
    '- 답하기 전에 관련 노트를 먼저 찾습니다.' \
    '- 요청받지 않으면 .obsidian 설정과 첨부파일은 수정하지 않습니다.' \
    > "$VAULT/CLAUDE.md"
fi
if [ ! -e "$VAULT/00-시작.md" ]; then
  printf '%s\n' '# 시작' '' '- 지금 하는 프로젝트:' '- 다음에 할 일:' > "$VAULT/00-시작.md"
fi
claude plugin list --json | node -e 'const fs=require("fs");const a=JSON.parse(fs.readFileSync(0,"utf8"));const need=["ecc@ecc","ponytail@ponytail","claude-mem@thedotmack"];const have=new Set(a.filter(x=>x.enabled).map(x=>x.id));const miss=need.filter(x=>!have.has(x));if(miss.length){console.error(`설치 확인 실패: ${miss.join(", ")}`);process.exit(1)}console.log("플러그인 3개 설치 확인 완료")'
printf 'Obsidian 보관함: %s\nClaude Code를 완전히 종료했다가 다시 열어주세요.\n' "$VAULT"
```
(페이지 복사본은 줄바꿈이 사라져 있어 위는 읽기 쉽게 줄을 나눈 형태)

설치 후 Obsidian에서 `Open folder as vault` → `~/Documents/ClaudeVault` 선택, 그다음 터미널에서:
```bash
cd "${CLAUDE_VAULT:-$HOME/Documents/ClaudeVault}"
claude
```

**STEP 1. 실행 환경 확인 (1분)**: 세 플러그인 모두 Node.js 훅을 사용
```bash
node --version
npx --version
claude --version
```
세 명령이 버전을 출력하면 준비 완료. 낮으면 공식 페이지에서 업데이트.

**STEP 2. 네 도구 역할 확인 (1분)**
| 도구 | 붙는 위치 | 하는 일 |
|---|---|---|
| ECC | Claude Code 플러그인 | 스킬·에이전트·명령·훅으로 개발 흐름 확장 |
| Obsidian | 별도 데스크톱 앱 + 로컬 폴더 | Markdown 기록 보관, `[[노트]]` 링크로 연결 |
| Ponytail | Claude Code 플러그인 | 기존 코드·표준 기능부터 쓰게 해 과잉 구현 감소 |
| Claude-Mem | Claude Code 플러그인 + 로컬 워커 | 세션 관찰·요약을 로컬 DB에 남기고 다음 세션에 관련 맥락 로드 |

- Ponytail은 사용량을 무조건 50% 줄이는 도구가 아님. 공식 벤치마크(기능 작업 12개, Haiku 4.5, 작업당 4회): 코드 줄 -54%, 토큰 -22%, 비용 -20%, 시간 -27%. 작업·모델에 따라 다르고 이미 간결한 코드는 감소폭 거의 없음
- Obsidian은 파일을 자동 연결하지 않음. `[[노트 이름]]` 링크를 만들거나 Claude Code에 연결을 요청해야 관계가 생김

**STEP 3. 설치 경로 하나만 사용 (1분)**
- ECC는 플러그인 설치와 수동 전체 설치 중 하나만. Quick Start는 플러그인 경로이므로 이후 `install.sh --profile full`이나 `npx ecc-install --profile full`을 겹쳐 실행하면 스킬·훅 중복
- Claude-Mem을 `npm install -g claude-mem`으로 설치하지 말 것(SDK만 설치되고 Claude Code 훅·워커 미연결). 플러그인 설치 후 `npx claude-mem repair`로 런타임 정렬 (원문 본문은 `npx claude-mem repair`로 쓰지만 Quick Start·FAQ는 `npx --yes claude-mem@latest repair` 사용 → 후자 권장)

**STEP 4. Obsidian 보관함 연결 (2분)**
1. https://obsidian.md/download 에서 앱 설치(Claude Code 플러그인이 아닌 별도 앱)
2. Obsidian 실행 → `Open folder as vault` → `~/Documents/ClaudeVault` 선택
3. 왼쪽 파일 목록에 `CLAUDE.md`, `00-시작.md` 확인
- 다른 경로를 쓰려면 Quick Start 실행 전에:
```bash
export CLAUDE_VAULT="$HOME/<내 보관함 폴더>"
```
- 연결 확인: 해당 폴더에서 `claude` 실행 후 "관련 노트를 먼저 찾아줘"라고 하여 Markdown 파일을 읽으면 연결된 것

**STEP 5. 설치 결과 확인 (2분)**
```bash
claude plugin list --json
claude plugin details ecc@ecc
claude plugin details ponytail@ponytail
claude plugin details claude-mem@thedotmack
npx --yes claude-mem@latest doctor
```
- 정상이면 `ecc@ecc`, `ponytail@ponytail`, `claude-mem@thedotmack` 세 식별자가 모두 보임
- doctor가 런타임 누락을 표시하면 `npx --yes claude-mem@latest repair`

**STEP 6. 첫 작업 실행 (2분)**
- 설치 후 실행 중인 Claude Code를 완전히 종료하고 새 세션을 열어야 훅·스킬이 모두 로드됨
```bash
cd "${CLAUDE_VAULT:-$HOME/Documents/ClaudeVault}"
claude
```
- 첫 요청은 작게(프롬프트 뼈대): 보관함에서 관련 노트를 먼저 찾고 현재 연결 상태만 확인, 파일 수정 금지, 마지막에 ECC·Ponytail·Claude-Mem이 설치 목록에서 확인되는지만 보고

## 핵심 팁 · 주의사항
- ❌ ECC 플러그인 설치 후 수동 전체 설치(`--profile full`) 겹치기 → ✅ 경로 하나만
- ❌ `npm install -g claude-mem` → ✅ 플러그인 설치 + `repair`
- Claude-Mem은 도구 사용을 관찰함: 비밀번호·API 키·고객 정보는 프롬프트·노트에 넣지 말고, `.env`·자격 증명 파일 읽기 금지 제약을 첫 프롬프트에 유지
- Obsidian 보관함은 로컬 폴더, 링크는 직접 만들거나 요청해야 연결됨
- 현재 에이전트가 Codex 등이어도 플러그인은 Claude Code에 설치되는 것

## 문제 해결
- 설치했는데 현재 세션에 안 보임: 설치 전부터 열린 세션은 모름 → Claude Code 완전 종료 후 재실행. 세션 유지가 필요하면 `/reload-plugins`
- `Marketplace not found`: 마켓플레이스 등록 확인 후 해당 add 재실행
```bash
claude plugin marketplace list --json
claude plugin marketplace add affaan-m/ECC --scope user
```
  (Ponytail은 `DietrichGebert/ponytail`, Claude-Mem은 `thedotmack/claude-mem`을 같은 방식으로)
- 명령/훅이 두 번 실행: ECC 플러그인 위에 수동 전체 설치가 겹친 경우가 큼 → 덮어쓰지 말고 ECC README의 "Reset / Uninstall ECC" (https://github.com/affaan-m/ecc#reset--uninstall-ecc) 순서로 정리 후 플러그인 하나만 재설치
- Claude-Mem 워커 미시작:
```bash
npx --yes claude-mem@latest doctor
npx --yes claude-mem@latest repair
```
- Obsidian에서 파일이 안 보임: 다른 폴더를 연 경우가 대부분 → 실제 경로를 확인하고 같은 폴더를 다시 `Open folder as vault`
```bash
printf '%s\n' "${CLAUDE_VAULT:-$HOME/Documents/ClaudeVault}"
```

## 바로 쓰는 체크리스트
- [ ] Claude Code ≥ 2.1, Node ≥ 20.12, npx 확인
- [ ] Quick Start 셸 블록 실행(또는 에이전트에 위임)
- [ ] 플러그인 3개 활성 (`claude plugin list --json`)
- [ ] `npx --yes claude-mem@latest doctor` 통과
- [ ] Obsidian에서 보관함 열기, `CLAUDE.md`·`00-시작.md` 보임
- [ ] Claude Code 완전 종료 후 보관함 폴더에서 `claude` 재실행
- [ ] 설치 경로 중복(플러그인+수동) 없음
