# 색인 (스킬용)

스킬이 먼저 읽는 작은 색인입니다. 자동화·코딩·웹 디자인은 레시피와 카탈로그부터 보고, 그 밖의 주제는 가이드 상황별 표로 후보를 고른 뒤 필요한 파일만 엽니다. 가이드별 한 줄 요약이 필요하면 `README.md`의 주제별 목차를 봅니다. 이 파일은 `python scripts/build_demo.py`가 만듭니다.

## 레시피

- `recipes/automation.md`: 레시피: 저장소 자동화 두 가지
- `recipes/coding.md`: 레시피: 기능 하나를 계획부터 병합까지
- `recipes/web-design.md`: 레시피: AI 티 안 나는 랜딩·소개 페이지

## 도구 카탈로그

id 뒤 괄호는 종류, `+`는 함께 쓰이는 다른 분야(`also`), "써 봄"은 이 저장소 작업에서 직접 써 본 도구(`hands_on`)입니다. 자세한 내용은 해당 yaml에서 id로 찾습니다.

- `catalog/automation.yaml` 12개: `claude-code-action` (github-action), `claude-code-hooks` (built-in, +coding), `claude-cloud-scheduled-tasks` (built-in), `claude-local-scheduling` (built-in), `github-pages-deploy` (github-action, 써 봄), `lychee-action` (github-action), `n8n-mcp` (service), `zapier-mcp` (mcp), `make-mcp` (mcp), `inbox-zero` (service), `github-mcp` (mcp, +coding), `ntfy` (service)
- `catalog/coding.yaml` 19개: `superpowers` (plugin, 써 봄), `context7` (mcp), `ecc` (plugin), `graphify` (skill), `serena` (mcp), `builtin-code-review` (built-in, 써 봄), `builtin-security-review` (built-in, 써 봄), `security-guidance` (plugin), `claude-security` (plugin), `feature-dev` (plugin), `pr-review-toolkit` (plugin), `commit-commands` (plugin), `lsp-plugins` (plugin), `semgrep-guardian` (plugin), `claude-code-security-review-action` (github-action, 관리 중단), `gitleaks` (cli, +automation, 써 봄), `claude-mem` (plugin), `caveman` (plugin), `understand-anything` (plugin)
- `catalog/web-design.yaml` 15개: `impeccable` (skill, 써 봄), `taste-skill` (skill, 써 봄), `emil-design-eng` (skill, 써 봄), `web-design-guidelines` (skill), `frontend-design` (plugin), `awesome-design-md` (service), `shadcn-mcp` (mcp), `agent-browser` (cli), `playwright-mcp` (mcp, +coding, automation), `playwright-cli` (cli, +automation), `chrome-devtools-mcp` (mcp), `figma-mcp` (mcp), `lighthouse-cli` (cli), `axe-cli` (cli), `superdesign` (plugin)

## 상황별 빠른 찾기

| 이런 게 필요할 때 | 먼저 볼 가이드 |
|---|---|
| Claude Code 첫 세팅(필수 스킬·MCP·플러그인) | [claudeskill](01-skills-mcp/claudeskill.md) · [claude-skills-top5](01-skills-mcp/claude-skills-top5.md) · [claude-code-skills-5-0813](01-skills-mcp/claude-code-skills-5-0813.md) · [mcps](01-skills-mcp/mcps.md) · [claude-weekend-setup-roadmap](01-skills-mcp/claude-weekend-setup-roadmap.md) |
| 토큰·사용 한도 절약 | [tokensave](06-cost-saving/tokensave.md) · [graphify](06-cost-saving/graphify.md) · [pxpipe-token-save](06-cost-saving/pxpipe-token-save.md) · [markitdown-pdf-token-saver](06-cost-saving/markitdown-pdf-token-saver.md) · [prompt-master](06-cost-saving/prompt-master.md) · [claude-skills-top5-0815](06-cost-saving/claude-skills-top5-0815.md) |
| 한도에 걸린 뒤에도 다른 모델로 작업 잇기 | [9router](06-cost-saving/9router.md) · [9router-free-fallback](06-cost-saving/9router-free-fallback.md) · [omniroute](06-cost-saving/omniroute.md) · [free-llm-api-claude-code-setup](99-etc/free-llm-api-claude-code-setup.md) |
| 세션 관리(되감기·분기·요약) | [claude-code-session-commands-5](05-coding/claude-code-session-commands-5.md) |
| 바이브 코딩용 도구, 에이전트 팀 | [vibecoding3](05-coding/vibecoding3.md) · [ecc-claude-code-agent-team](01-skills-mcp/ecc-claude-code-agent-team.md) · [ruflo](03-automation/ruflo.md) · [agency-agents-7seats](03-automation/agency-agents-7seats.md) · [munder-difflin-ai-office-setup](03-automation/munder-difflin-ai-office-setup.md) |
| 낯선 GitHub 레포 빠르게 파악 | [github-repo-diagram-ingest-cheats](05-coding/github-repo-diagram-ingest-cheats.md) · [graphify](06-cost-saving/graphify.md) |
| AI 티 안 나는 웹 디자인 | [designskill](09-web-design/designskill.md) · [claude-design-top-5-skill](09-web-design/claude-design-top-5-skill.md) · [claude-designer-kill](09-web-design/claude-designer-kill.md) · [fable5-website](09-web-design/fable5-website.md) |
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

## 가이드 전체 파일 목록

- **스킬·MCP** `01-skills-mcp/`: claude-buzzy-product-video-ads, claude-code-animation-skill-66-styles, claude-code-skills-5-0813, claude-court-jury-skill, claude-newtake-mcp-ai-short-drama, claude-resume-hiring-panel, claude-skills-top5, claude-weekend-setup-roadmap, claudeskill, ecc-claude-code-agent-team, linkedin-skills-claude-code-setup, mcps
- **영상·이미지** `02-video-image/`: ai-photo-effect-prompts-10, claude-higgsfield-katana-video-edit, claude-opus-motion-design-prompts, claude-sound-effects-tools, faceless-youtube-channel-opus-higgsfield, google-motion, higgsfield-ai-influencer-genjutsu, higgsfield-commands-claude, higgsfield-content-factory-claude, manus-hyperframes-srt-motion, minimaxh3, movieskill, open-generative-ai, recordly-screen-recorder-setup
- **자동화** `03-automation/`: agency-agents-7seats, atticus-mac-voice-assistant-setup, automaton-self-funding-ai-agent, business-jobs-to-agent-files, chatgpt-metricool-social-manager, chatgpt-new-features-four, claude-and-n8n, grok-bot-trading-team-setup, grok-polymarket-trading-agent, grok-six-bot-paper-trading-team, inbox-zero-claude-email-setup, munder-difflin-ai-office-setup, phil-ai-trader-paper-1000, ruflo, self-improving-ai-trading-loop, trading-bot
- **프롬프트** `04-prompts/`: chatgpt-face-rating-prompts, chatgpt-modify-photo-prompt, chatgpt-prompt-codes-100, chatgpt-truth-prompt-honest-mode, claude-presentation-prompts-6, claude-private-tutor-prompts, hani-prompt, pt-prompts
- **코딩** `05-coding/`: claude-code-session-commands-5, github-repo-diagram-ingest-cheats, higgsfield-api-cashback-app-prompt, vibecoding3
- **비용 절약** `06-cost-saving/`: 9router-free-fallback, 9router, claude-skills-top5-0815, google-aitool-free-15, graphify, markitdown-pdf-token-saver, omniroute, oracle-cloud-free-server-12gb, prompt-master, pxpipe-token-save, tokensave
- **공부·리서치** `07-study-research/`: agent-reach, chagpt-4commands-study, chatgpt-book-mindmap-codes, claude-notebooklm-second-brain, claude-youtube-skill
- **비즈니스** `08-business/`: 84skills, claude-harvey-sales-agent, claude-idea-council-4-agents, scrapegraphai
- **웹 디자인** `09-web-design/`: claude-design-top-5-skill, claude-designer-kill, designskill, fable5-website
- **글쓰기** `10-writing/`: remove-ai-marks, storyscope-ai-fiction
- **기타** `99-etc/`: chatgpt-newtake-object-head-dance-challenge, free-llm-api-claude-code-setup
