# 무료 클로드 스킬로 다섯 부서 채우기
- 도구·주제: Claude Code 플러그인/스킬 팩 · 업무 자동화 (재무·법무·마케팅·SNS·디자인)
- 한 줄 요약: 재무·법무·마케팅·SNS(+디자인) 스킬 팩을 플러그인으로 설치하고, 복사본을 내 사업에 맞게 고쳐 쓰는 순서. (2026-08-10 공개, 읽는 데 14분, 7단계 따라 하면 약 68분)

## 언제 쓰나
- 마케팅 카피, 숏폼 대본, 계약서 검토, 재무 분석 등을 혼자 붙잡고 있어 클로드 스킬에 맡기고 싶을 때
- 스킬 = 업무 처리 방법을 적은 지침서(폴더 1개에 `SKILL.md` 1개), 플러그인 = 스킬 여러 개를 묶은 배포 단위(부서 1개 = 플러그인 1개), 마켓플레이스 = 플러그인 창고(등록해야 꺼냄). 스킬 자체에는 별도 구독료 없음.

## 준비물 / 필요 도구
- Claude Code: https://claude.com/claude-code (`claude --version`). 설치 방법 문서 https://code.claude.com/docs/en/discover-plugins · 스킬 문서 https://code.claude.com/docs/en/skills · 플러그인 안내 https://claude.com/plugins/
- 재무·법무(앤트로픽 공식): https://github.com/anthropics/knowledge-work-plugins (법무 폴더 https://github.com/anthropics/knowledge-work-plugins/tree/main/legal)
- 마케팅(커뮤니티): https://github.com/coreyhaines31/marketingskills · https://marketing-skills.com/
- SNS(커뮤니티): https://github.com/charlie947/social-media-skills
- 디자인(선택, 커뮤니티): https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (https://www.uupm.cc/) · https://github.com/Leonxlnx/taste-skill (https://tasteskill.dev/)
- Node.js LTS (디자인 팩 `npx`용, https://nodejs.org/)

## 단계별 방법
**Quick Start** — Claude Code 안에서 7줄을 위에서부터 차례로(네 부서 한 번에 설치), 끝나면 Claude Code 완전 종료 후 재시작:
```
/plugin marketplace add anthropics/knowledge-work-plugins
/plugin install finance@knowledge-work-plugins
/plugin install legal@knowledge-work-plugins
/plugin marketplace add coreyhaines31/marketingskills
/plugin install marketing-skills@marketingskills
/plugin marketplace add charlie947/social-media-skills
/plugin install social-media-skills@social-media-skills
```
확인: `/help`에 `finance`, `legal`, `marketing-skills`, `social-media-skills`가 보이면 성공.

1. **STEP 1 준비물 확인 (2분)**: 스킬 팩은 Claude Code 안에서만 설치됨(홈페이지 채팅과 다른 도구).
   ```
   claude --version
   claude
   ```
   - 버전 숫자(예: 2.1.215)가 나오면 준비 완료. 이후 `/` 명령은 모두 `claude` 실행 후 대화창에서 입력.
2. **STEP 2 스킬 개념 (2분)**: 매번 붙여넣는 프롬프트가 아니라 한 번 설치하면 클로드가 그 업무를 알아서 기억. 여기서는 부서 단위 플러그인 설치.
3. **STEP 3 재무·법무 (3분)**: 앤트로픽 공식, 창고 하나에 함께 들어 있어 명령 3줄로 스킬 17개.
   ```
   /plugin marketplace add anthropics/knowledge-work-plugins
   /plugin install finance@knowledge-work-plugins
   /plugin install legal@knowledge-work-plugins
   ```
   - 재무 8개: audit-support, close-management, financial-statements, journal-entry, journal-entry-prep, reconciliation, sox-testing, variance-analysis
   - 법무 9개: brief, compliance-check, legal-response, legal-risk-assessment, meeting-briefing, review-contract, signature-request, triage-nda, vendor-check
   - 자주 쓰는 3개: `financial-statements`(손익계산서·재무상태표 + 증감 설명), `variance-analysis`(목표 미달이 적게 팔아서인지 싸게 팔아서인지 분리), `review-contract`(조항 단위로 훑어 자동 갱신 같은 독소 조항 탐색).
   - 이 팩의 명령은 부서명 접두 필수:
   ```
   /finance:variance-analysis
   ```
   - 클로드가 무엇을 분석할지 되물으면 정상.
4. **STEP 4 마케팅·SNS (3분)**
   ```
   /plugin marketplace add coreyhaines31/marketingskills
   /plugin install marketing-skills@marketingskills
   /plugin marketplace add charlie947/social-media-skills
   /plugin install social-media-skills@social-media-skills
   ```
   - 마케팅 49개, SNS 17개. 마케팅 대표: `ad-creative`(광고 문구·각도 후보 다수), `copywriting`(랜딩·이메일·제목, 가장 먼저 내 말투로 고칠 스킬), `cro`(기존 페이지에서 손님이 새는 지점 진단).
   - SNS 팩은 `voice-builder`를 **가장 먼저** 실행: 질문에 답하면 `about-me.md`, `voice.md` 두 파일 생성, 나머지 16개 스킬이 글을 쓰기 전에 항상 이 파일을 읽음(건너뛰면 16개 모두 남들과 같은 말투). 약 10분. 시작 요청 뼈대: voice-builder 스킬을 실행해 내 말투 파일을 만들어 달라. 클로드가 질문을 하나씩 던지면 정상.
5. **STEP 5 디자인 팩 (선택, 3분)** — 화면/웹페이지를 직접 만들 때만. 터미널에서:
   ```
   npx --yes skills@latest add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --agent claude-code --yes
   npx --yes skills@latest add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend" --agent claude-code --yes
   ```
   - 설치 완료 표시와 저장 경로가 나오면 성공. `command not found: npx`면 Node LTS 설치 후 터미널 재시작.
6. **STEP 6 내 사업에 맞게 고치기 (20분)** — 가장 중요. 앤트로픽 공식 저장소도 이 스킬들을 "일반적인 출발점"이라 부르며 조직 용어·절차를 직접 넣으라고 안내.
   - ❌ 설치된 자리에서 직접 수정: 플러그인은 업데이트 때 자기 폴더를 통째로 새로 써서 고친 내용이 경고 없이 사라짐. ✅ 복사본을 만들어 수정.
   | 위치 | 경로 | 적용 범위 |
   |---|---|---|
   | 내 계정 전체 | `~/.claude/skills/이름/SKILL.md` | 이 컴퓨터 모든 작업 |
   | 특정 프로젝트 | `.claude/skills/이름/SKILL.md` | 그 프로젝트 폴더 안에서만 |
   - 말투·사업 규칙은 계정 전체, 고객사 전용 규칙만 프로젝트 쪽. 이름이 같으면 계정 쪽 우선. 명령어는 파일 안 이름이 아니라 **폴더 이름** 기준(폴더명을 바꾸면 명령어도 바뀜). 고칠 파일은 `SKILL.md` 하나, 맨 위 `---` 두 줄 사이 설정 영역은 건드리지 말고 본문만 수정.
   - 커스터마이즈 프롬프트 뼈대: `copywriting` 스킬을 `~/.claude/skills/copywriting/`로 복사한 뒤 **복사본만** 수정, 원본 플러그인 폴더 수정 절대 금지. 슬롯: `내 사업은 <사업 한 줄>`, `주 고객은 <고객층>`, ① 쓰지 않을 표현(예: 줄표, 과장된 감탄) ② 유지할 어조(예: 따뜻하지만 직설적) ③ 내 상품과 가격 — 말투 규칙 부분을 다시 쓰기, 설정 영역은 그대로, 끝나면 바뀐 항목을 항목별로 보고.
   - 부서별 넣을 내용: 마케팅=내 말투·실제 상품과 가격·고객이 이미 써 본 것과 두려워하는 것 / SNS=voice-builder 결과·쓰는 플랫폼·영상 길이·절대 안 쓰는 오프닝 / 디자인=브랜드 색상 코드·글꼴·여백·모서리 값·반복 요소 / 재무=계정 과목·회계연도 시작 월·보고서 양식 / 법무=사업장 국가·받아들일 조항과 절대 안 되는 조항·위험 기준선.
   - 한 번에 다섯 부서를 고치지 말고 오늘은 `copywriting` 하나.
7. **STEP 7 오늘 실행 순서 (35분)**: ① 앤트로픽 창고 등록 ② 재무·법무 설치(명령 2줄로 17개) ③ 마케팅·SNS 창고 등록·설치 ④ `voice-builder` 최우선 실행 ⑤ `copywriting` 하나만 복사해 내 사업에 맞게 수정.

**설치·검증 위임 프롬프트 뼈대(Claude Code)**: 역할=스킬 팩 4개 설치·연결 검증 담당. 슬롯 `<운영체제와 셸>`, `<내 사업 한 줄>`, `<목표 한 줄>`. 작업: ① `claude --version`, `/plugin` 목록에서 3개 마켓플레이스 등록 여부 확인(있으면 재등록 말고 보고) ② 없으면 위 7줄 순서 실행 ③ 재시작 후 `/help`에 4개 항목, `/finance:variance-analysis` 인식 확인 ④ 네 팩의 역할과 사용법을 5줄 이내로 설명. 제약: 기존 파일·설정 덮어쓰기/삭제 금지, 스킬 원본 직접 수정 금지, `.env` 등 비밀키 읽기·출력 금지, 중복 설치 금지. 검증: `/help` 4개 + 접두 명령 인식, 실패 시 완료 보고 금지.

## 핵심 팁 · 주의사항
- 재무·법무만 앤트로픽이 직접 관리, 마케팅·SNS·디자인은 커뮤니티 제작. 플러그인은 내 컴퓨터에서 내 권한으로 코드를 실행하므로 믿을 수 있는 곳에서만 설치(공식 문서 안내) — 설치 전 저장소 주소를 열어 확인.
- 법무 스킬(`review-contract` 등)은 변호사 대체가 아님: 변호사에게 보내기 전에 계약서를 이해하는 시간을 줄이는 용도.
- 순서의 이유: 재무·법무를 먼저(창고 하나에 둘이 있어 최소 명령으로 최대 스킬, 순서 바꾸면 같은 창고 이중 등록), `voice-builder`를 SNS 스킬보다 먼저(나중에 돌리면 이전 글을 전부 다시 만들어야 함), 마지막 한 개 고치기를 건너뛰면 설치만 하고 끝남.
- 재무 명령은 `/finance:variance-analysis` 형식(`/variance-analysis`는 인식 안 됨).

## 문제 해결
| 증상 | 원인 | 해결 |
|---|---|---|
| `/plugin` 명령 못 알아들음 | Claude Code 구버전 | 최신 버전으로 업데이트 후 재실행 |
| 설치했는데 목록에 안 보임 | 재시작 전 | Claude Code 완전 종료 후 재실행 |
| `/variance-analysis` 인식 안 됨 | 부서 이름 누락 | `/finance:variance-analysis` |
| SNS 글이 남 얘기처럼 나옴 | `voice-builder` 미실행 | 다른 SNS 스킬 전에 먼저 실행 |
| 고쳐 둔 스킬이 사라짐 | 설치 폴더에서 직접 수정 | 계정 폴더로 복사한 뒤 복사본 수정 |
| `command not found: npx` | Node.js 미설치 | nodejs.org LTS 설치 후 터미널 재시작 |

## 바로 쓰는 체크리스트
- [ ] `claude --version` 확인 후 플러그인 4종 설치, 재시작 뒤 `/help`에 보임
- [ ] `voice-builder` 실행해 `about-me.md`, `voice.md` 생성
- [ ] `copywriting`을 `~/.claude/skills/`로 복사 후 본문만 수정
- [ ] 재무/법무 명령을 `/finance:...` 형식으로 시험
- [ ] 설치 전 각 저장소 주소 확인
- [ ] (선택) 디자인 팩 2종 npx 설치
