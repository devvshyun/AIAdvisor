# AI 도구 가이드 레퍼런스

Claude Code와 주변 AI 도구를 다루는 가이드 78편입니다. 2026-11-05 기준입니다. 웹 디자인 가이드 4편은 "생성 스킬은 하나만" 레시피와 충돌해서 2026-11-09에 `_archive/09-web-design/`으로 옮겼습니다. 웹 디자인은 `recipes/web-design.md`와 `catalog/web-design.yaml`을 봅니다.

- 가이드마다 파일을 하나씩 두었고, 모든 파일은 `언제 쓰나 → 준비물 → 단계별 방법 → 팁·주의사항 → 체크리스트` 순서로 되어 있습니다.
- 긴 프롬프트는 전문 대신 구조(역할, 채울 칸, 제약, 출력 형식)만 적었습니다.
- 같은 줄에 붙은 `# 주석`은 명령을 설명하려고 덧붙인 것입니다.
- 범위 숫자(예: 30~50%) 일부는 표기가 깨진 것을 문맥으로 복원했습니다. 비용이나 비율처럼 중요한 수치는 공식 문서에서 확인하세요.
- 도구 버전, 무료 한도, 캠페인 기한은 바뀔 수 있습니다. 실제로 설치하기 전에 공식 저장소와 문서를 다시 확인하세요.

---

## 상황별 빠른 찾기

| 이런 게 필요할 때 | 먼저 볼 가이드 |
|---|---|
| Claude Code 첫 세팅(필수 스킬·MCP·플러그인) | [claudeskill](01-skills-mcp/claudeskill.md) · [claude-skills-top5](01-skills-mcp/claude-skills-top5.md) · [claude-code-skills-5-0813](01-skills-mcp/claude-code-skills-5-0813.md) · [mcps](01-skills-mcp/mcps.md) · [claude-weekend-setup-roadmap](01-skills-mcp/claude-weekend-setup-roadmap.md) |
| 토큰·사용 한도 절약 | [tokensave](06-cost-saving/tokensave.md) · [graphify](06-cost-saving/graphify.md) · [pxpipe-token-save](06-cost-saving/pxpipe-token-save.md) · [markitdown-pdf-token-saver](06-cost-saving/markitdown-pdf-token-saver.md) · [prompt-master](06-cost-saving/prompt-master.md) · [claude-skills-top5-0815](06-cost-saving/claude-skills-top5-0815.md) |
| 한도에 걸린 뒤에도 다른 모델로 작업 잇기 | [9router](06-cost-saving/9router.md) · [9router-free-fallback](06-cost-saving/9router-free-fallback.md) · [omniroute](06-cost-saving/omniroute.md) · [free-llm-api-claude-code-setup](99-etc/free-llm-api-claude-code-setup.md) |
| 세션 관리(되감기·분기·요약) | [claude-code-session-commands-5](05-coding/claude-code-session-commands-5.md) |
| 바이브 코딩용 도구, 에이전트 팀 | [vibecoding3](05-coding/vibecoding3.md) · [ecc-claude-code-agent-team](01-skills-mcp/ecc-claude-code-agent-team.md) · [ruflo](03-automation/ruflo.md) · [agency-agents-7seats](03-automation/agency-agents-7seats.md) · [munder-difflin-ai-office-setup](03-automation/munder-difflin-ai-office-setup.md) |
| 낯선 GitHub 레포 빠르게 파악 | [github-repo-diagram-ingest-cheats](05-coding/github-repo-diagram-ingest-cheats.md) · [graphify](06-cost-saving/graphify.md) |
| AI 티 안 나는 웹 디자인 | 가이드 대신 [웹 디자인 레시피](recipes/web-design.md)와 `catalog/web-design.yaml` |
| 클로드에 기억(세컨드 브레인) 붙이기 | [claude-notebooklm-second-brain](07-study-research/claude-notebooklm-second-brain.md) · [claudeskill](01-skills-mcp/claudeskill.md) (claude-mem·Obsidian) |
| 웹·유튜브·레딧 자료 수집 | [agent-reach](07-study-research/agent-reach.md) · [claude-youtube-skill](07-study-research/claude-youtube-skill.md) · [scrapegraphai](08-business/scrapegraphai.md) |
| 아이디어·이력서를 비판적으로 검토 | [claude-court-jury-skill](01-skills-mcp/claude-court-jury-skill.md) · [claude-idea-council-4-agents](08-business/claude-idea-council-4-agents.md) · [claude-resume-hiring-panel](01-skills-mcp/claude-resume-hiring-panel.md) |
| 글에서 AI 흔적 지우기 | [remove-ai-marks](10-writing/remove-ai-marks.md) · [storyscope-ai-fiction](10-writing/storyscope-ai-fiction.md) |
| 발표 자료(PPT) 만들기 | [claude-presentation-prompts-6](04-prompts/claude-presentation-prompts-6.md) |
| 업무 자동화(메일·n8n·SNS) | [inbox-zero-claude-email-setup](03-automation/inbox-zero-claude-email-setup.md) · [claude-and-n8n](03-automation/claude-and-n8n.md) · [chatgpt-metricool-social-manager](03-automation/chatgpt-metricool-social-manager.md) · [business-jobs-to-agent-files](03-automation/business-jobs-to-agent-files.md) |
| 영상·모션 그래픽 만들기 | [02-video-image](02-video-image/) 폴더 전체 (Higgsfield 계열, 모션 프롬프트, 무료 영상 AI) |
| 무료 인프라·도구 | [oracle-cloud-free-server-12gb](06-cost-saving/oracle-cloud-free-server-12gb.md) · [google-aitool-free-15](06-cost-saving/google-aitool-free-15.md) |
| ChatGPT 프롬프트 모음 | [04-prompts](04-prompts/) 폴더 · [chatgpt-book-mindmap-codes](07-study-research/chatgpt-book-mindmap-codes.md) · [chagpt-4commands-study](07-study-research/chagpt-4commands-study.md) |
| 자동매매 실험 (모의 계좌 전용, 투자 책임은 본인) | [self-improving-ai-trading-loop](03-automation/self-improving-ai-trading-loop.md) · [trading-bot](03-automation/trading-bot.md) · [phil-ai-trader-paper-1000](03-automation/phil-ai-trader-paper-1000.md) 외 |

## 여러 가이드에 반복해서 나오는 도구

설치하기 전에 같은 도구를 다룬 가이드끼리 비교해 보면 겹쳐서 설치하는 일을 막을 수 있습니다.

- **ECC**: ecc-claude-code-agent-team, vibecoding3, claude-skills-top5, claudeskill
- **Graphify / Headroom / Ponytail**: tokensave, graphify, claude-skills-top5-0815, claudeskill
- **OmniRoute / 9Router (모델 폴백)**: omniroute, 9router, 9router-free-fallback, claude-skills-top5-0815
- **claude-mem**: claude-skills-top5-0815, claudeskill
- **taste-skill / impeccable**: designskill, claude-design-top-5-skill, claude-designer-kill, claude-code-skills-5-0813
- **Higgsfield**: 02-video-image 폴더 대부분, fable5-website, higgsfield-api-cashback-app-prompt
- **Playwright MCP**: mcps, claude-designer-kill, vibecoding3

---

# 주제별 전체 목차
## 스킬·MCP (`01-skills-mcp`)

| 가이드 | 한 줄 요약 |
|---|---|
| [클로드·버지로 시네마틱 광고 5개](01-skills-mcp/claude-buzzy-product-video-ads.md) | Buzzy MCP를 Claude Code에 연결해 제품 사진 한 장으로 15초 광고를 만들고, 같은 사진으로 조명·각도가 다른 5개 버전을 뽑아 폴더에 모은다. |
| [클로드 코드로 66가지 스타일의 바이럴 애니메이션 만드는 법](01-skills-mcp/claude-code-animation-skill-66-styles.md) | lemo-opuscar 스킬 하나를 설치하면 클로드가 스토리·나레이션·음악·효과음을 만들고 영상을 코드로 한 프레임씩 렌더링한다(영상 생성 AI·스톡 영상 미사용). 66가지 스타일 중 고르거나 나만의 스타일을 만들 수 있다. |
| [클로드 코드 필수 스킬 5개](01-skills-mcp/claude-code-skills-5-0813.md) | agent-browser, find-skills, design-taste-frontend, mcp-builder, GSD 5개를 npx 한 줄씩 설치하고 `ls`로 확인한 뒤 작은 요청으로 실사용 점검. |
| [아이디어를 클로드 12명 재판에 세우는 스킬](01-skills-mcp/claude-court-jury-skill.md) | `/court` 스킬이 검사, 변호인, 배심원 12명, 판사 역할의 에이전트를 돌려 내 아이디어에 유죄/무죄 표결과 "무죄가 되는 조건"을 알려 준다. |
| [클로드에 뉴테이크 MCP 연결해서 AI 숏드라마 만드는 법](01-skills-mcp/claude-newtake-mcp-ai-short-drama.md) | Newtake 원격 MCP를 Claude에 연결해 캐릭터 시트·배경 → 5단계 장면 설계 → 태그한 에셋으로 15초 9:16 영상을 생성한다. |
| [클로드로 이력서를 탈락시키려는 채용 심사단 만드는 법](01-skills-mcp/claude-resume-hiring-panel.md) | hiring-panel 스킬을 설치하면 자동 검사 1명 + 채용 관리자 1명 + 독립 평가자 5명이 이력서를 서로 다른 관점에서 심사해 탈락 사유 목록과 수정본을 만들어 준다. |
| [Claude Code 스킬 TOP 5, 겹치지 않게 설치하는 가이드](01-skills-mcp/claude-skills-top5.md) | 많이 깔지 말고 역할이 안 겹치게 하나씩 설치하고, `claude plugin details`로 고정(always-on) 토큰 비용까지 확인하라는 가이드. |
| [이틀 만에 90%의 사람보다 클로드를 잘 쓰게 되는 로드맵](01-skills-mcp/claude-weekend-setup-roadmap.md) | 토요일에 About Me·세컨드 브레인·프로젝트, 일요일에 MCP 앱 연결·스킬을 세팅해, 클로드가 나를 아는 상태로 일하게 만드는 2일 로드맵. |
| [Claude Code 필수 설정 4개, 한 번에 붙이는 퀵 가이드](01-skills-mcp/claudeskill.md) | 플러그인 3개와 Obsidian 보관함을 셸 블록 하나로 한 번에 설치·연결하고, 결과 확인과 첫 작업까지 마무리하는 퀵 가이드. |
| [ECC 하나 설치해서 클로드에 엔지니어 전부를 맡기는 법](01-skills-mcp/ecc-claude-code-agent-team.md) | ECC 플러그인 하나(명령 두 줄)를 설치해 planner·security-reviewer 등 에이전트와 `/ecc:plan`, `/ecc:test-coverage`, `/ecc:security-scan` 명령으로 기능 하나를 설계부터 보안 점검까지 한 줄씩 맡긴다. (2026-09-30 갱신, 약 25분, 검증 기준: ECC v2.2.2 / Claude Code 2.1.283) |
| [링크드인 스킬 12개](01-skills-mcp/linkedin-skills-claude-code-setup.md) | 링크드인 스킬 묶음을 설치해 프로필/콘텐츠/댓글 초안을 키 없이 쓰고, Apify 토큰을 연결해 내 포스트 반응자를 동료/윗선/잠재 고객 3그룹으로 나눈다. (4단계) |
| [클로드 코드에 무조건 깔아야 하는 MCP 5개](01-skills-mcp/mcps.md) | 검색·브라우저 조작·크롤링·이미지 생성·내 탭 점검 능력을 `claude mcp add` 한 줄씩으로 붙이고 실제 연결을 확인하는 가이드. |

## 영상·이미지 (`02-video-image`)

| 가이드 | 한 줄 요약 |
|---|---|
| [진짜 터지는 AI 사진 효과 프롬프트 10개](02-video-image/ai-photo-effect-prompts-10.md) | 사진을 올려 편집되는 AI 이미지 도구에 영어 원문 프롬프트를 통째로 붙여 4K, 피부 보정, GTA, 레고 등 10가지 효과를 내는 방법. |
| [클로드에 원본 영상 올리고 10분 뒤 모션 그래픽 완성본 받는 법](02-video-image/claude-higgsfield-katana-video-edit.md) | Claude에 Higgsfield 커넥터를 연결하고 `/katana` 프리셋(Personalized edits / Style transfer / Motion transfer)으로 내 원본 영상을 레퍼런스 편집 스타일(컷 순서·길이·음악 컷)로 다시 만든다. 약 20분, 영상 1개당 편집 약 10분. (2026-10-14 공개) |
| [오퍼스 프롬프트 하나로 15초 모션 영상](02-video-image/claude-opus-motion-design-prompts.md) | Claude Code를 `--model claude-opus-5-5 --effort max`로 열어 영어 프롬프트 하나로 15초 모션 쇼릴 코드를 만들게 하고 ffmpeg로 MP4 렌더한다. (원문 2026-10-05 갱신, 읽는 데 10분, 4단계) |
| [클로드 효과음 도구 3개 (오픈버스 API · 리얼 SFX · 이어샷)](02-video-image/claude-sound-effects-tools.md) | 공개 효과음 검색(Openverse), 영상에 실제 녹음 효과음을 맞는 프레임에 삽입(real-sfx), 맞는 소리가 없을 때 코드로 생성(earshot) 세 도구를 설치해 Claude Code에 연결한다. 모두 무료, 코드는 MIT. |
| [월 1000만원 버는 유튜브 채널, 클로드 오퍼스로 만드는 5단계 (얼굴 없는 유튜브 채널)](02-video-image/faceless-youtube-channel-opus-higgsfield.md) | 리서치 → 대본 재구성(Opus 5.5) → 힉스필드 연결 → 설명 영상 제작 → 쇼츠 변환의 5단계 워크플로. 월 1000만원은 제목상의 문구이며 수익 보장이 아니다. |
| [모션 그래픽 한 편을 10분 만에 만드는 레퍼런스 번역법](02-video-image/google-motion.md) | 따라 하고 싶은 모션 그래픽을 프레임 사진으로 잘라 Claude에게 읽혀 생성 프롬프트로 번역시키고, 그 프롬프트를 Google Flow(Omni Flash)에 넣어 클립으로 받는다. (2026-09-12 공개, STEP 6개) |
| [힉스필드로 AI 인플루언서 만들기](02-video-image/higgsfield-ai-influencer-genjutsu.md) | 힉스필드에서 캐릭터를 만들고 Genjutsu로 참고 영상의 동작을 입혀, 인스타 게시 후 Launchpoint 캠페인에 제출하는 5단계 흐름. (원문 갱신 2026-10-11, 읽는 데 10분, 따라 하면 약 23분) |
| [클로드에서 쓰는 힉스필드 명령어 8개](02-video-image/higgsfield-commands-claude.md) | Higgsfield 커넥터를 Claude에 붙이고 `/tier-list` 등 8개 슬래시 명령어로 직접 찍은 말하는 클립에 그래픽 효과를 넣는다. |
| [힉스필드 콘텐츠 팩토리 숏폼 공장](02-video-image/higgsfield-content-factory-claude.md) | Higgsfield MCP를 Claude에 연결하고 Content Factory에서 스타일을 골라 30초 9:16 애니메이션 설명 영상을 만든 뒤, 제품 소개와 판매 링크 연결까지 잇는다. |
| [마누스 AI로 모션 그래픽 누구나 만드는 법, 1분 세팅](02-video-image/manus-hyperframes-srt-motion.md) | Manus에 HyperFrames 스킬("HTML 비디오 제작")을 한 번 추가해 두면, 자막(.srt)과 프롬프트만으로 문장 시간에 맞춰 장면이 바뀌는 1080×1920 세로 모션 그래픽 MP4를 받는다. (4단계, 약 11분, 2026-10-05 갱신) |
| [미니맥스 H3 (무료 영상+소리 생성 AI)](02-video-image/minimaxh3.md) | 영상과 효과음/대사/배경음을 한 번에 만드는 옴니 모델을 무료 체험판으로 써보고, 프롬프트 스킬과 로컬 실행(Pinokio+Wan2GP)까지 안내한다. (갱신 2026-08-27, 읽는 데 11분, 5단계 약 56분) |
| [AI 냄새 줄이는 영상 만들기: Banana Pro Director 2.0 + Cinema Worldbuilder Pro 2.0](02-video-image/movieskill.md) | 두 스킬은 영상을 직접 만들지 않고 Claude가 이미지·영상 프롬프트를 제작 규칙대로 쓰게 하는 지침. 얼굴 잠금 → 의상 → 6패널 시트 → 장면 플레이트 → 움직임 설계 → Seedance 생성 → 부분 수정 → 편집. |
| [유료 영상 AI 대신 쓰는 무료 스튜디오 입문 가이드 (Open Generative AI)](02-video-image/open-generative-ai.md) | 오픈소스(MIT) 앱 하나로 이미지·영상 모델 200여 개를 한 화면에서 쓰고, muapi-cli와 스킬로 Claude Code/Codex 자동화까지 하는 입문. |
| [어떤 화면 녹화든 모션 디자이너 작품처럼 만드는 레코들리 사용법](02-video-image/recordly-screen-recorder-setup.md) | 무료 오픈소스 데스크톱 앱 Recordly로 녹화를 멈추면 커서 따라가는 자동 확대가 잡히고, 부드러운 커서·배경 프레임·얼굴 버블까지 클릭 몇 번으로 입혀 MP4/GIF로 내보낸다. (검증 기준 v1.4.0, 2026-09-27, 약 17분) |

## 자동화 (`03-automation`)

| 가이드 | 한 줄 요약 |
|---|---|
| [무료 AI 에이전트 일곱 자리](03-automation/agency-agents-7seats.md) | 279개 에이전트 명단에서 필수 7명만 골라 설치하고 총괄(orchestrator)에게만 목표를 주는 방식. (2026-09-13 공개, 읽는 데 13분, 6단계 약 20분) |
| [맥용 자비스 아티커스(Atticus) 설치하고 세팅하는 법](03-automation/atticus-mac-voice-assistant-setup.md) | 단축키를 누른 채 영어로 말하면 앱 실행, 창 이동, 파일 찾기를 해 주는 무료 오픈소스(MIT) 앱을 명령 한 줄로 설치하고 권한을 세팅한다. |
| [돈을 못 벌면 진짜 죽는 AI 에이전트 오토마톤 설치법](03-automation/automaton-self-funding-ai-agent.md) | 크립토 지갑 잔고로 자신의 추론 비용을 내고 잔고 0이 1시간 지속되면 스스로 멈추는 오픈소스(MIT) 터미널 에이전트를 소스에서 빌드해 지갑·지출 한도 설정까지 해보는 실험 가이드. |
| [회사 전체를 파일과 폴더로 옮기는 4단계, 업무 137개 지도](03-automation/business-jobs-to-agent-files.md) | 반복 업무를 부서별 폴더 + 업무당 `.md` 파일 하나로 적어 AI 에이전트가 읽고 실행하게 만드는 방법. SkillTree(skilltreeos.ai) 운영 창업가가 2026-09-03 공개, 본인 회사를 부서 7개·업무 137개로 운영. (2026-09-30 갱신, 약 18분, 검증 기준 Claude Code v2.1.283) |
| [ChatGPT로 SNS 관리](03-automation/chatgpt-metricool-social-manager.md) | ChatGPT에 Metricool 앱을 연결해 SNS 성과 분석, 콘텐츠 아이디어, 게시물 예약을 대화로 처리하는 5단계(프롬프트 10개). (2026-10-05 갱신, 읽는 데 12분, 따라 하면 약 20분) |
| [아무도 모르는 ChatGPT 신기능 4개 세팅하는 법](03-automation/chatgpt-new-features-four.md) | 워드 안의 ChatGPT, 앱을 닫아도 일하는 dots, 함께 쓰는 스페이스, 셀카 스티커팩을 켜는 곳과 요청 문장, 요금제별 가능 여부를 정리했다. |
| [클로드로 첫 n8n 에이전트 만드는 6단계](03-automation/claude-and-n8n.md) | Claude 프로젝트에 지시문과 샘플 워크플로 JSON을 넣어 두고, 만들고 싶은 자동화를 말로 적으면 n8n에 붙여넣을 JSON을 받는 방식으로 첫 자동화를 만든다. |
| [그록 에이전트 7개로 트레이딩 팀 만드는 법](03-automation/grok-bot-trading-team-setup.md) | Grok Bot 앱에서 총괄 봇 CHIEF 1개 + 역할 봇 6개(SCAN/VET/BOOK/SIZE/FILLS/RISK)를 만들고, 밈코인 데스크와 예측시장 데스크 두 그룹으로 실제 돈 없는 모의 매매 팀을 돌린다. (2026-10-20 공개, 약 60분) |
| [그록 50달러 자동매매 에이전트](03-automation/grok-polymarket-trading-agent.md) | Grok Bot이 10분마다 Polymarket 시장을 훑어 가상 $50으로 모의 거래하는 루틴을 만드는 방법. 실거래는 다루지 않음. (2026-10-08 갱신, 읽는 데 15분, 4단계 약 30분, 검증 기준일 2026-10-03) |
| [그록 봇 6개 트레이딩 팀, 클로드 코드로 그대로 만드는 법](03-automation/grok-six-bot-paper-trading-team.md) | Claude Code 프롬프트 한 번으로 grok-trader 프로젝트를 만들고, 발굴·뉴스·여론·차트·리스크·결정 6개 봇 지시문으로 후보를 거르고 가상 잔고로만 매매하는 대시보드까지 돌린다. 실제 주문·지갑 연결 없음. |
| [메일 답장, 이제 클로드한테 맡기는 세팅법](03-automation/inbox-zero-claude-email-setup.md) | Gmail/Outlook 위에서 동작하는 오픈소스 AI 메일 비서 Inbox Zero로 분류·답장 초안·후속 연락 추적을 켜고, API 키+CLI(또는 커넥터)로 Claude가 규칙과 통계를 읽기 전용으로 점검하게 하는 5단계. |
| [AI 오피스를 통째로 고용하는 법: 먼더 디플린](03-automation/munder-difflin-ai-office-setup.md) | 클로드 코드·코덱스 같은 AI 코딩 에이전트 여러 개를 사무실 화면 하나에 모으고, 팀장 에이전트 마이클에게만 말하면 마이클이 일을 나눠 맡기는 무료 앱의 설치·운영법. 챗봇이 아니고 AI 모델도 들어 있지 않다. (2026-10-08 공개, 읽는 데 13분, 따라 하면 약 33분) |
| [클로드 트레이더 Phil](03-automation/phil-ai-trader-paper-1000.md) | Claude Code가 가상 $1,000으로 Polymarket 단기 시장을 모의 거래하고, 결과마다 전략 파일을 고쳐 git 커밋으로 남기는 실험 저장소를 돌리는 4단계. (2026-10-08 갱신, 읽는 데 10분) |
| [Claude Code에 에이전트 팀 붙이는 Ruflo 입문 가이드](03-automation/ruflo.md) | Claude Code 바깥에 에이전트 조율·메모리·작업 라우팅을 얹는 오픈소스 Ruflo를 연습 폴더에서 작은 팀(최대 8 에이전트)부터 단계적으로 써 보는 입문. |
| [돈 잃을 때마다 자기 코드를 다시 짜는 AI 트레이딩 시스템 만드는 법](03-automation/self-improving-ai-trading-loop.md) | 아이디어 → 전략 코드 → 백테스트 → 코드로 건 손실 한도 아래 모의 매매 → 사후 검토 → 실패 장부 누적의 5단계 루프를 Claude Code로 구성한다. 돈을 벌어 주는 기계도 투자 조언도 아니다. |
| [클로드 코드로 만드는 5자산 자동매매 봇](03-automation/trading-bot.md) | Claude Code로 SPY·QQQ·BTC/USD·GLD·USO 5자산 봇을 만들고 백테스트 → 2주 모의투자 → 손실 한도 → 아침저녁 리포트 → 실계좌 순서로 8단계에 걸쳐 검증하며 넘어가는 방법. (2026-08-06 갱신, 약 23분, STEP 8개) |

## 프롬프트 (`04-prompts`)

| 가이드 | 한 줄 요약 |
|---|---|
| [ChatGPT 얼굴 평가 프롬프트 5개](04-prompts/chatgpt-face-rating-prompts.md) | 본인 셀카 한 장으로 같은 대화에서 영어 프롬프트 5개(얼굴 평가, 나이 추정, 분위기, MBTI, 직업)를 순서대로 돌려 흑백 리포트를 받고, 한국어 한 줄을 덧붙여 10점 만점·한국어 출력으로 받는다. 오락용. (2026-10-14 공개, 읽는 데 15분, 5단계 약 12분) |
| [ChatGPT한테 '사진 고쳐줘' 대신 쓰는 프롬프트 10개](04-prompts/chatgpt-modify-photo-prompt.md) | "사진 고쳐줘" 대신 지킬 것/바꿀 것을 한 번에 적은 영어 편집 프롬프트 10종을 대괄호 칸만 채워 붙여넣어 ChatGPT 사진 편집 품질을 올린다. |
| [챗GPT 쓸 때 모르면 손해인 코드 100개](04-prompts/chatgpt-prompt-codes-100.md) | 질문 앞에 ELI5, TLDR 같은 영어 코드 한 단어와 그 뜻 한 줄을 붙여 ChatGPT 답의 길이·난이도·말투를 바꾸는 방법과 코드 100개 목록(아래는 뜻을 요약한 것). |
| [반박하면 57% 맞장구치는 ChatGPT, 바른말 하게 만드는 법](04-prompts/chatgpt-truth-prompt-honest-mode.md) | 솔직 모드 프롬프트를 ChatGPT 사용자 지정 지침에 저장해 맞장구 대신 근거로 답하게 만들고, 틀린 계산으로 반박 테스트해 확인하며, 상황별 후속 프롬프트(계획·글·해석·사실 확인 등)를 꺼내 쓴다. (2026-10-08 공개, 읽는 데 12분, 따라 하면 약 8분) |
| [발표 자료 뽑는 클로드 프롬프트 6개](04-prompts/claude-presentation-prompts-6.md) | 한 대화 안에서 설계도→슬라이드 구조→스토리→디자인→내용→다듬기 6개 프롬프트를 순서대로 보낸 뒤 .pptx 파일을 요청한다. (2026-10-19 공개, 읽는 데 8분, 5단계 약 14분) |
| [클로드를 개인 과외 선생님으로 바꾸는 프롬프트 6개](04-prompts/claude-private-tutor-prompts.md) | 새 대화에 프롬프트 하나를 통째로 붙여넣고 대괄호 `[ ]`만 내 주제로 바꾸면, 클로드가 질문하고 내 답을 기다리며 가르치는 6가지 과외 모드(학습 곡선 가이드, 실수 시뮬레이터, 난해한 글 번역기, 7일 경로 설계, 숨은 구멍 탐지, 파인만 기법)로 바뀐다. |
| [클로드 코드에 무료 프롬프트 라이브러리 연결하는 법](04-prompts/hani-prompt.md) | prompts.chat(2,300개+ 공개 프롬프트)을 플러그인으로 연결해, 요청 문장에 검색 지시를 넣으면 클로드가 필요한 프롬프트를 찾아 적용하게 한다. |
| [PT비 내기 전에 봐야할 ChatGPT 프롬프트 4개](04-prompts/pt-prompts.md) | 개인 트레이너 모드, 신체 변화 계획, 주간 식단, 개인 영양사, 진행 상황 추적기까지 프롬프트 5개(제목은 4개지만 페이지에는 5개 섹션)를 ChatGPT에 붙여넣어 맞춤 운동·영양 계획을 받는다. (2026-09-11 공개, 읽는 데 1분) |

## 코딩 (`05-coding`)

| 가이드 | 한 줄 요약 |
|---|---|
| [클로드 세션 명령어 5개](05-coding/claude-code-session-commands-5.md) | 대화에 남기지 않는 질문, 한 줄 요약, 되감기, 갈림길, 프롬프트 보관 5가지와 git 저장 지점을 함께 쓰는 법. (2026-10-17 공개, 읽는 데 11분, 5단계 약 8분) |
| [GitHub 레포를 한눈에 읽는 치트키 사이트 2곳](05-coding/github-repo-diagram-ingest-cheats.md) | GitHub 주소의 `hub` 세 글자만 바꿔(`github` → `gitdiagram`/`gitingest`) 레포 구조를 그림(GitDiagram)으로 보고, 전체를 AI용 텍스트(GitIngest)로 묶어 ChatGPT/Claude에 붙여 질문한다. |
| [Higgsfield + GPT-6 Astra로 앱 만드는 프롬프트](05-coding/higgsfield-api-cashback-app-prompt.md) | GPT-6 Astra 새 대화에 영어 프롬프트 하나를 붙여, 상품 사진/고객 요청을 Higgsfield API로 이미지·영상으로 바꾸는 자동화 앱을 만들게 한다. |
| [클로드 코드로 바이브 코딩한다면 깔아야 하는 3개](05-coding/vibecoding3.md) | 클로드가 중간에 길을 잃고, 옛 문법으로 코드를 쓰고, 보안 구멍을 모르는 문제를 무료 도구 세 개(ECC=검증된 작업 방식, Context7=최신 문서, Strix=AI 모의 해킹)로 메우고, 계획 → 구현 → 테스트 → 보안 점검 흐름을 만든다. (2026-08-28 공개, 읽는 데 12분, 따라 하면 약 36분, STEP 6개) |

## 비용 절약 (`06-cost-saving`)

| 가이드 | 한 줄 요약 |
|---|---|
| [9Router 백업 모델 설정](06-cost-saving/9router-free-fallback.md) | 로컬 라우터 9Router의 Fallback Combo로, Claude Code 한도 소진 시 무료 모델로 자동 이어가는 9단계 설정. (갱신 2026-08-19, 읽는 데 11분) |
| [Claude Code 한도 뒤에도 계속 코딩하는 9Router 설정](06-cost-saving/9router.md) | 주 모델과 백업 모델을 9Router의 Fallback Combo로 묶어 Claude Code 한도 초과나 라우팅 가능한 오류 때 자동으로 다음 모델로 넘기고, Cursor 등 다른 도구에도 같은 엔드포인트를 쓴다. |
| [클로드 코드를 쓰기 전에 깔아야 하는 플러그인 5개](06-cost-saving/claude-skills-top5-0815.md) | 한도 소진·맥락 망각을 막는 무료 도구 5개(OmniRoute, Headroom, Claude-mem, Claude Code Setup, Task Observer)를 하나씩 설치하고 진짜 붙었는지 확인한다. |
| [구글이 무료로 푼 AI 도구 15개](06-cost-saving/google-aitool-free-15.md) | 구글이 열어 둔 무료(개인 무료 등급 포함) AI 도구 15개를 한 줄 설명과 주소로 정리하고, 내 상황에 맞는 것을 골라 열어 보고 접근 가능 여부까지 걸러 내는 방법. (2026-08-15 공개, 읽는 데 11분, 따라 하면 약 23분, STEP 5개) |
| [Graphify 가이드](06-cost-saving/graphify.md) | 함수·클래스·호출 관계를 그래프로 만들어 Claude Code가 파일을 뒤지기 전에 그래프부터 조회하게 하는 11단계. (갱신 2026-08-06, 읽는 데 14분) |
| [클로드에 PDF 올리면 토큰 2배, 무료 마크잇다운으로 줄이는 법](06-cost-saving/markitdown-pdf-token-saver.md) | PDF/Word/Excel/PowerPoint를 글자만 남긴 마크다운으로 변환해 Claude에 올려 토큰을 줄이고, MCP로 Claude Desktop 대화 안에서 바로 변환하게 연결한다. |
| [Claude Code 한도 이후에도 작업을 이어가는 OmniRoute 입문 가이드](06-cost-saving/omniroute.md) | Claude Code와 여러 AI 제공자 사이의 로컬 게이트웨이를 세워, Claude 한도가 끝나면 연결해 둔 다른 모델로 요청을 넘기고 긴 도구 출력은 보내기 전에 압축한다. |
| [오라클 클라우드 12기가 서버 평생 무료로 받는 법](06-cost-saving/oracle-cloud-free-server-12gb.md) | 오라클 클라우드 Always Free의 Arm(Ampere A1) 2 OCPU·메모리 12GB 서버를 가입부터 생성, ssh 접속, tmux로 봇 상시 구동까지 만들고 무료 범위 안에서 유지한다. (2026-11-04 공개, 읽는 데 11분, 따라 하면 약 33분, STEP 5개) |
| [프롬프트 마스터 (Prompt Master 스킬)](06-cost-saving/prompt-master.md) | 한도를 갉아먹는 건 긴 요청 한 번이 아니라 재요청 — 대충 쓴 한 줄을 결과 모양·범위·종료 조건이 채워진 완성 프롬프트로 바꿔주는 오픈소스(MIT) 스킬을 설치한다. (2026-08-29 공개, 읽는 데 11분, 7단계 약 13분) |
| [같은 Fable, 청구서만 반으로 줄이는 법 (pxpipe-proxy)](06-cost-saving/pxpipe-token-save.md) | 시스템 프롬프트·도구 설명·지난 대화 같은 덩치 큰 맥락을 촘촘한 이미지로 바꿔 보내는 로컬 프록시를 켜고 Claude Code를 연결해 입력 토큰(청구서)을 줄인다. 모델·출력은 그대로. |
| [클로드 코드 토큰 3배로 오래 쓰는 무료 도구 3개](06-cost-saving/tokensave.md) | 토큰이 새는 세 지점(AI가 쓰는 코드량, 찾느라 읽는 파일량, 모델에 실제로 보내는 양)을 각각 막는 무료 도구 3개를 함께 설치하고, `headroom savings`로 실제 절감을 확인한다. |

## 공부·리서치 (`07-study-research`)

| 가이드 | 한 줄 요약 |
|---|---|
| [클로드가 유튜브·레딧·깃허브를 무료로 긁어오게 만드는 도구](07-study-research/agent-reach.md) | 클로드가 기본 상태에선 못 읽는 유튜브 자막·레딧·엑스 등의 통로를 무료 도구 하나로 열어 주고, 어떤 통로가 열렸는지 점검한 뒤 여러 통로를 엮은 조사를 시키는 방법. (2026-09-04 공개, 읽는 데 11분, 따라 하면 약 36분, STEP 8개) |
| [ChatGPT 공부 명령어 4개 (요약 → 퀴즈)](07-study-research/chagpt-4commands-study.md) | Cheat Sheet → Blueprint → Flashcards → Mind Map 4개 명령어를 같은 채팅에서 주제만 바꿔 보내 요약부터 퀴즈까지 이어간다. (2026-08-19 공개, 읽는 데 10분 / 따라 하면 약 40분, 7단계. 제목의 "25분"은 핵심 4단계 기준) |
| [책 한 권을 마인드맵·만화로 바꾸는 챗GPT 명령어 100개](07-study-research/chatgpt-book-mindmap-codes.md) | 대화 안에서 뜻을 정의해 둔 약속어(그림 명령어 4개 + 슬래시 명령어 96개)로, 붙여넣은 책 한 장을 그림·요약·퀴즈·공부 계획으로 바꾼다. |
| [클로드에게 절대 안 잊는 두 번째 뇌 붙이기 (NotebookLM)](07-study-research/claude-notebooklm-second-brain.md) | NotebookLM을 MCP로 연결하고 저장용 스킬을 만들어 대화 요약을 `Claude Memory` 노트북에 쌓고, `CLAUDE.md` 규칙으로 다음 세션에서 먼저 검색하게 하는 5단계. |
| [유튜브 튜토리얼을 클로드가 실행하는 스킬로 바꾸는 세 가지 세팅](07-study-research/claude-youtube-skill.md) | 클로드에게 영상을 보는 눈(watch 스킬)을 달고, 같은 영상을 Gemini가 두 번째 눈으로 따로 읽게 한 뒤, 두 기록을 SPEC.md로 합쳐 skill-creator로 실제 실행되는 스킬로 굽는 순서. (2026-09-10 공개, 읽는 데 16분, 따라 하면 약 54분, STEP 9개) |

## 비즈니스 (`08-business`)

| 가이드 | 한 줄 요약 |
|---|---|
| [무료 클로드 스킬로 다섯 부서 채우기](08-business/84skills.md) | 재무·법무·마케팅·SNS(+디자인) 스킬 팩을 플러그인으로 설치하고, 복사본을 내 사업에 맞게 고쳐 쓰는 순서. (2026-08-10 공개, 읽는 데 14분, 7단계 따라 하면 약 68분) |
| [고객 유치만을 위한 클로드 에이전트(하비/Harvey) 세팅하는 법](08-business/claude-harvey-sales-agent.md) | 오픈소스 Harvey를 설치해 내 제품 홈페이지로 학습시키고, 조건에 맞는 업체를 찾아 사이트에서 본 사실로 콜드메일 초안을 쓰고, 내 승인 후 발송·회신 처리를 이어 가게 한다. 영어 메일 기준이라 해외 업체 영업에 적합. |
| [내 아이디어를 6개월 만들기 전에 뜯어보는 네 자리 (아이디어 검토 에이전트 4개)](08-business/claude-idea-council-4-agents.md) | 지지자·회의론자·투자자·판사 네 역할을 한 번만 만들어 두고 순서대로 돌려 "만든다 / 고치고 만든다 / 접는다" 중 하나의 판결을 받는다. |
| [클로드로 업체 연락처 수천 개를 무료로 모으는 법](08-business/scrapegraphai.md) | 무료 오픈소스 ScrapeGraphAI와 내 컴퓨터에서 도는 무료 로컬 모델(Ollama)로 웹페이지의 공개 업체 연락처만 골라 CSV로 모으고, 매일 아침 자동 실행되게 한다. (2026-08-19 공개, 읽는 데 10분, 따라 하면 약 58분, STEP 7개) |

## 글쓰기 (`10-writing`)

| 가이드 | 한 줄 요약 |
|---|---|
| [클로드가 남기는 표식 지우기](10-writing/remove-ai-marks.md) | 글 속 안 보이는 문자와 이미지/PDF 메타데이터는 도구로 제거·검증할 수 있고, 단어 선택 패턴은 검증 방법이 없다는 한계를 안내한다. (2026-08-21 공개, 읽는 데 12분, 6단계 따라 하면 약 53분) |
| [AI가 쓴 글은 문체가 아니라 이야기 구조에서 걸립니다 (StoryScope)](10-writing/storyscope-ai-fiction.md) | 문체가 아니라 "이야기를 짜는 방식(서사 구조)"으로 AI 소설을 93.2% 가려낸다는 StoryScope 논문을 정리하고, 내 글을 같은 기준으로 진단·수정하는 체크리스트와 프롬프트를 제공한다. |

## 기타 (`99-etc`)

| 가이드 | 한 줄 요약 |
|---|---|
| [ChatGPT·뉴테이크로 인외 캐릭터 챌린지 영상 만들기](99-etc/chatgpt-newtake-object-head-dance-challenge.md) | 얼굴만 사물이고 몸은 사람인 "인외" 캐릭터 이미지를 만든 뒤, 챌린지 영상 속 댄서 두 명만 그 캐릭터로 교체한 15초 무음 영상을 만든다. |
| [클로드 코드 돈 안 내고 쓰는 프리 LLM API 세팅법](99-etc/free-llm-api-claude-code-setup.md) | 계속 무료로 쓸 수 있는 LLM API 공급자 16곳 목록(+키 설정을 돕는 `free-llm-apis` 스킬)을 내려받고, 무료 키를 Manifest 라우터에 연결한 뒤, 테스트 폴더 하나의 `.claude/settings.json`에서만 Claude Code가 무료 모델을 쓰게 하고 되돌리는 4단계. (2026-10-08 갱신, 읽는 데 11분, 따라 하면 약 18분) |

