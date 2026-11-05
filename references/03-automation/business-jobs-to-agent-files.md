# 회사 전체를 파일과 폴더로 옮기는 4단계, 업무 137개 지도
- 원문: https://lazyowen.com/guides/business-jobs-to-agent-files
- 도구·주제: Claude Code(또는 claude.ai) · 마크다운 파일 · 업무 지도화 / 에이전트용 업무 문서
- 한 줄 요약: 반복 업무를 부서별 폴더 + 업무당 `.md` 파일 하나로 적어 AI 에이전트가 읽고 실행하게 만드는 방법. SkillTree(skilltreeos.ai) 운영 창업가가 2026-09-03 공개, 본인 회사를 부서 7개·업무 137개로 운영. (2026-09-30 갱신, 약 18분, 검증 기준 Claude Code v2.1.283)

## 언제 쓰나
- 견적서·입금 확인·문의 응대 순서가 내 머릿속에만 있어 모든 일이 나를 거쳐야 끝날 때
- 반복 업무를 에이전트에게 위임할 수 있는지 점수로 가려내 문서화하고 싶을 때

## 준비물 / 필요 도구
- 방법 자체는 앱이 아닌 평범한 폴더와 텍스트 파일(도구를 바꿔도 파일은 그대로 이식). 라이선스 명시 없음
- 웹 채팅(인터뷰·초안): https://claude.ai/new — 폴더가 자동 생성되지 않아 초안을 텍스트 파일로 직접 저장
- Claude Code(폴더·파일 자동 생성): 환경 macOS 13.0+ / Windows 10 1809+ / Ubuntu 20.04+, 메모리 4GB+, Claude 구독 또는 Anthropic Console 계정 필요
  - 개요: https://code.claude.com/docs/en/overview
  - 설치(윈도우 PowerShell 명령 포함): https://code.claude.com/docs/en/setup
  - 저장소: https://github.com/anthropics/claude-code
  - 요금: https://claude.com/pricing
- 원 출처 사이트: https://skilltreeos.ai/
- 구글 시트 또는 엑셀(업무 점검 워크시트용)
- 용어: 리드 = 아직 고객은 아니지만 연락해 볼 잠재 고객, CRM = 고객 이름·연락 기록·거래 단계를 모아 두는 프로그램, `.md` = 제목·목록 표시만 조금 더한 평범한 텍스트 파일

## 단계별 방법
### 프롬프트 뼈대 A. 웹 채팅용 (claude.ai 새 대화에 붙여넣기, Quick Start)
- 목적: 사업 반복 업무를 에이전트 실행용 파일로 옮기는 전 과정을 인터뷰형으로 진행
- 지시 4가지: ① 7개 부서(세일즈, 딜 관리, 마케팅, 운영, 정보 조사, 고객, 백오피스)별로 인터뷰해 반복 업무를 전부 목록화, 구체적으로 말하도록 몰아붙일 것("영업 처리하기"는 업무가 아니고 "리드의 웹사이트를 보고 첫 연락 메일 쓰기"가 업무) ② 업무마다 4질문(반복되나요 / 규칙이 있나요 / 디지털로 들어와 디지털로 나가나요 / 틀려도 괜찮나요)에 0~2점, 8점 만점 순위표 ③ 6점 이상 업무마다 부서 폴더 하나, 업무 하나당 `.md` 하나, 섹션은 목적·시작 조건·입력·단계·결과물·완료 기준·예외, 불확실한 부분은 추측 말고 "확인 필요" 표시 ④ 먼저 돌릴 부서 하나와 이유 제시
- 규칙: 한 번에 질문 하나씩, 지금 시작
- 성공 시: 답을 쏟지 않고 첫 부서에 대한 질문 하나로 인터뷰 시작

### 프롬프트 뼈대 B. Claude Code용 (my-business 폴더에서 `claude` 실행 후 첫 메시지)
- 역할: 사업의 반복 업무를 부서별 폴더·업무 파일로 옮기는 인터뷰·정리 담당. 사용자는 개발 초보
- 슬롯: [내 목표 = 내 사업 한 줄과 제일 귀찮은 일] (예: 1인 디자인 스튜디오 — 견적서·입금 확인). OS·셸·폴더 위치는 직접 확인
- 작업: ① `pwd`, `ls`로 현재 폴더·OS 확인 ② `ls business`로 부서 폴더 7개 확인, 없을 때만 `mkdir -p business/sales business/deals business/marketing business/operations business/intelligence business/customer business/back-office` ③ 7개 부서 순서로 한 번에 질문 하나씩 인터뷰, 4질문 점수표(8점 만점 순위) 제시, 6점 이상만 업무 하나당 `.md`(7칸: 목적·시작 조건·입력·단계·결과물·완료 기준·예외, 불확실하면 "확인 필요"), 끝나면 `find business -name "*.md" | wc -l`로 개수 표시 ④ 가장 먼저 돌릴 부서와 이유를 3줄 이내로
- 제약: 폴더·파일 생성 전 계획을 보여 주고 허락, 기존 파일 덮어쓰기 금지(새 이름), sudo·전역 설치·설정 파일 수정 금지, 연락처·비밀번호·API 키 기록 금지
- 출력: 실행 명령, 만든 폴더·파일 목록, 점수 순위표, "확인 필요" 칸, 첫 부서
- 검증: `ls business`에 7개(back-office, customer, deals, intelligence, marketing, operations, sales), `find ... | wc -l` 숫자가 만든 파일 수와 일치

### STEP 1. 부서별로 반복 업무 전부 적기 (STEP 2와 합쳐 오후 반나절)
프로젝트·목표가 아닌 매일/매주 되풀이되는 업무만 적는다. 이번 주에 누가 그 일을 하는 장면이 안 그려지면 더 잘게 쪼갠다.
| 부서 | 떠올리는 질문 | 업무 예시 |
|---|---|---|
| 세일즈 | 잠재 고객이 나를 어떻게 알게 되나요? | 잠재 고객 찾기, 첫 연락, 후속 연락, 통화 예약 |
| 딜 관리 | '관심 있어요'와 '입금' 사이에 무슨 일이? | 제안서, 가격, 반론 대응, 계약서 챙기기 |
| 마케팅 | 관심을 얻는 일은? | 콘텐츠 아이디어, 스크립트, 캡션, 발행, 댓글 답장 |
| 운영 | 판매 뒤 실제 일은 어떻게 끝나나요? | 온보딩, 프로젝트 세팅, 진행 상황 공유, 품질 점검 |
| 정보 조사 | 이기려면 무엇을 알아야 하나요? | 잠재 고객 조사, 경쟁사 추적, 통화 준비, 회의 요약 |
| 고객 | 이미 돈 낸 사람을 어떻게 지키나요? | 안부 연락, 문의 응대, 갱신 준비, 후기 받기 |
| 백오피스 | 아무도 안 보는 일은? | 청구서, 입금 독촉, 장부 정리, 보고, 메일함 정리 |

업무 점검 워크시트: 아래 헤더와 예시를 탭 구분으로 구글 시트/엑셀 A1에 붙여넣으면 8칸으로 나뉜다. 점수 칸은 STEP 2에서 채운다.
- 헤더: 부서 / 업무 / 반복 / 규칙 / 디지털 / 틀려도 됨 / 합계 / 판정
- 예시 행: 세일즈 – 리드 웹사이트 보고 첫 연락 메일 쓰기 / 백오피스 – 입금 안 된 청구서 독촉 메일 보내기 / 고객 – 들어온 문의를 종류별로 나누기

보통 업무가 80~150개 나오며 아직 거르지 않는다(거르는 건 STEP 2).

### STEP 2. 업무마다 점수 매기기
질문 4개에 아니다 0점, 가끔 1점, 그렇다 2점(합계 8점 만점).
- 반복되나요? 매일·매주 일은 금방 본전, 분기 1회는 대기
- 규칙이 있나요? 똑똑한 신입에게 10분 안에 설명 가능한가. "그때그때 감으로"면 낮게
- 디지털로 들어와 디지털로 나가나요? 메일·문서·스프레드시트·CRM 기록이면 2점, 악수·현장 방문이 끼면 낮음
- 틀려도 괜찮나요? 90%만 맞아도 되는 일인가. 초안·조사는 높고 최종 가격 결정은 0점
| 합계 | 판정 | 하는 일 |
|---|---|---|
| 6~8점 | 먼저 파일로 | 반복 잦고 규칙 분명, 부담 적음. 업무 20~40개가 여기 해당 |
| 3~5점 | 확인 후 넘기기 | 에이전트가 초안을 쓰고 나가기 전에 내가 승인 |
| 0~2점 | 내가 계속 | 관계·감각·큰 결정. 적어 두면 나만 할 일이 보임 |
원문 회사에서 6점 이상: 답장 분류, 성사·실패 분석, 구매 신호 포착, 업무 매뉴얼 작성, 회의 요약, 청구서 독촉. 사람이 쥔 업무: 큰 거래의 전략, 브랜드 목소리, 최종 발행 승인.

### STEP 3. 6점 이상만 파일로 옮기기 (파일 하나에 15~30분)
1. 원문 회사의 폴더 모양(업무 수)
```
business/
sales/           업무 22개 (세일즈)
deals/           업무 24개 (딜 관리)
marketing/       업무 23개 (마케팅)
operations/      업무 19개 (운영)
intelligence/    업무 17개 (정보 조사)
customer/        업무 14개 (고객)
back-office/     업무 18개 (백오피스)
```
2. Claude Code 설치(맥·리눅스; 윈도우는 공식 설치 안내의 PowerShell 명령). 이후 명령 블록은 맥·리눅스 터미널 기준. 설치 후 새 터미널 창.
```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
```
버전 뒤에 `(Claude Code)`가 붙으면 성공.
3. 업무 파일 전용 폴더에서 Claude Code 실행
```bash
mkdir -p ~/my-business && cd ~/my-business
claude
```
윈도우: PowerShell에서 `mkdir ~\my-business` → `cd ~\my-business` → `claude`. 처음 켜면 로그인 후 입력창. 입력창에 프롬프트 뼈대 B를 붙여넣으면 인터뷰~파일 작성까지 이어진다(윈도우도 OS에 맞는 명령으로 실행).
4. 웹 채팅만 쓸 때: 클로드가 쓴 초안을 직접 저장. 맥은 텍스트 편집기에서 새 문서 → 포맷 메뉴 '일반 텍스트 만들기' 후 붙여넣기, 윈도우는 메모장. 이름은 `collections.md`처럼 `.md`로 끝내고 끝에 `.txt`가 붙었으면 제거.
5. 프롬프트 없이 폴더만 만들려면 Claude Code 창이 아닌 터미널에서(Claude Code 창이면 `/exit` 또는 새 창, 새 창은 먼저 `cd ~/my-business`)
```bash
cd ~/my-business
mkdir -p business/sales business/deals business/marketing business/operations business/intelligence business/customer business/back-office
ls business
```
`ls business`에 폴더 7개 이름이 보이면 성공.
6. 업무 파일 7칸 템플릿(업무마다 파일 하나). 예시는 원문의 `trigger-detection.md`(구매 신호 포착)
```
# trigger-detection.md

### 목적
관심 고객사의 구매 신호를 잡습니다: 투자 유치, 새 임원 채용,
채용 공고, 제품 출시.

### 시작 조건
매일 아침 7시에 관심 고객사 목록을 대상으로 실행합니다.

### 입력
CRM의 관심 고객사 목록, 뉴스·채용 사이트 검색,
이미 기록한 최근 30일 신호.

### 단계
1. 지난 실행 이후 새로 나온 신호를 고객사마다 검색합니다
2. 이미 기록한 신호는 버립니다
3. 거래와 관련 깊은 순서로 줄 세웁니다
4. 신호마다 "왜 지금인지" 두 줄 메모를 씁니다

### 결과물
일일 브리핑에 들어갈 순위표: 고객사, 신호, 출처 링크, 다음 행동 제안.

### 완료 기준
새 신호가 전부 출처와 함께 기록되고 중복은 0개입니다.

### 예외
유료 벽에 막힌 출처는 조용히 건너뛰지 말고 표시합니다.
애매한 것은 추측하지 말고 "확인 필요"라고 적습니다.
```
신입이 이 파일만 보고 따라 할 수 있으면 에이전트도 할 수 있다. 첫 주에 파일 10개면 충분.
7. 파일 수 확인(`~/my-business`에서; 폴더만 만든 직후엔 0)
```bash
find business -name "*.md" | wc -l
```

### STEP 4. 한 부서만 먼저 돌리기 (2주)
전부 한 번에 옮기려다 파일 12개쯤에서 지쳐 포기하는 것이 흔한 실패.
1. 6~8점이 가장 많은 부서 선택(대개 세일즈나 백오피스), 파일 5~10개
2. 파일 하나를 에이전트에게 주고 그 일을 시킴 → 헤매는 곳이 파일이 흐릿한 곳
3. 결과가 틀리면 프롬프트가 아니라 파일을 고침
4. 계속 맞으면 2주 돌린 뒤 다음 폴더로
실행 프롬프트(경로는 내 파일로 교체). 성공하면 파일을 읽었다고 알리고 단계 순서대로 진행, 규칙이 빠진 곳에서 멈춰 질문. 빠진 규칙은 파일에 적는다.
```
business/back-office/collections.md 파일을 읽고 그 파일의 단계대로 오늘 할 일을 해 주세요. 파일에 없는 규칙이 필요하면 멈추고 무엇이 빠졌는지 알려 주세요.
```

## 업무 137개 지도 (원문 회사의 파일명, 참고용)
내 사업에 없는 업무는 지우고 워크시트 채우는 참고로만 쓴다.

- sales 22: icp-definition(이상적 고객상) · market-mapping(시장 지도) · trigger-detection(구매 신호 포착) · lookalike-modeling(닮은 회사 찾기) · database-mining(DB에서 잠재 고객 캐기) · web-and-maps-scraping(웹·지도 업체 목록) · social-mining(SNS 잠재 고객) · list-building(연락 목록) · contact-enrichment(담당자 연락처 채우기) · email-verification(이메일 검증) · account-enrichment(회사 정보 채우기) · fit-scoring(적합도 점수) · personalization-research(맞춤 메시지 조사) · cold-email-drafting(첫 연락 메일) · linkedin-messaging(링크드인 메시지) · proof-matching(맞는 사례 고르기) · cold-call-scripting(첫 통화 스크립트) · video-prospecting(영상 영업 메시지) · campaign-orchestration(캠페인 순서 설계) · campaign-launch(발송 시작) · deliverability(메일 도달률) · send-optimization(발송 시간·빈도)
- deals 24: reply-classification(답장 분류) · objection-response(반론 답변) · hot-lead-routing(뜨거운 리드 전달) · meeting-booking(미팅 잡기) · referral-capture(소개 받아 두기) · speed-to-lead(즉시 응대) · lead-qualification(리드 자격 판정) · comment-cta-fulfillment(댓글 요청 자료 발송) · inbox-triage(받은편지함 분류) · pre-call-briefing(통화 전 브리핑) · call-capture(통화 기록) · post-call-debrief(통화 후 정리) · follow-up-drafting(후속 메일) · objection-library(반론 모음집) · demo-prototyping(데모 시안) · proposal-generation(제안서) · deal-room-assembly(거래 자료방) · agreement-drafting(계약서 초안) · pricing-support(가격 책정 보조) · crm-hygiene(CRM 정리) · pipeline-reporting(진행 거래 보고) · forecasting(매출 예측) · reactivation(끊긴 리드 되살리기) · win-loss-analysis(성사·실패 분석)
- marketing 23: performance-mining(성과 분석) · trend-monitoring · competitor-analysis · audience-analysis · hook-writing · script-writing · caption-writing · carousel-production · video-production · image-generation · thumbnail-and-cover-design · ad-creative · landing-page-copy · deck-production(발표 자료) · cross-platform-adaptation · clip-extraction(긴 영상에서 클립) · lead-magnet-builds · publishing · newsletter-and-broadcast · seo-and-geo · og-and-share-surface(공유 미리보기) · deal-scripting · approval-docs
- operations 19: kickoff-pack · access-collection(접근 권한 받기) · project-scaffolding · document-extraction · integration-builds · data-migration · portal-provisioning(고객 포털) · qa-and-verification · agent-evaluation · monitoring-and-alerting · cost-and-usage-tracking · incident-response · status-updates · meeting-follow-ups · portal-sync · transcript-processing(녹취록 정리) · context-maintenance · sop-generation(업무 매뉴얼) · handoff-docs
- intelligence 17: company-deep-dive · tech-stack-detection · funding-and-financials-lookup · buying-committee-mapping · person-research · network-mapping · warm-path-finding(소개 경로) · competitor-teardown · vertical-analysis · pricing-research · tam-market-sizing · account-monitoring · news-and-mention-tracking · alert-routing · research-reports · data-visualization · adversarial-verification(반대편 검증)
- customer 14: ticket-triage · faq-and-self-serve · escalations · macro-authoring(답변 템플릿) · onboarding-journeys · health-scoring · churn-prediction · renewals-and-expansion · advocacy-and-referrals · qbr-prep(분기 리뷰) · engagement-and-replies · moderation(커뮤니티 관리) · member-spotlights · event-coordination
- back-office 18: invoice-generation · payment-tracking · collections(미수금 독촉) · revenue-reporting · goal-pacing · cash-flow-forecasting · budget-tracking · crm-sync · expense-categorization · document-filing-and-retrieval · contract-lifecycle · entity-compliance · calendar-management · email-triage · candidate-sourcing · screening-and-scheduling · onboarding-and-training · hr-and-policy-assistant

## 핵심 팁 · 주의사항
- ❌ "영업 처리하기"처럼 부서 이름과 다를 바 없는 영역을 업무로 적기 → ✅ "리드의 웹사이트와 링크드인을 보고 첫 연락 메일 쓰기"처럼 입력·출력이 보이는 한 동작
- ❌ 결과가 틀릴 때마다 채팅창에 "이건 이렇게 고쳐줘" → ✅ 빠진 규칙·예시·예외를 업무 파일에 한 줄 적고 재실행(채팅은 다음 실행에 안 남음)
- 파일은 설명서일 뿐: 에이전트가 실제 메일 발송·CRM 수정을 하려면 도구 연결 설정이 따로 필요(이 자료는 다루지 않음)
- 137개는 한 회사의 지도: 내 사업은 부서·업무 수가 다름
- 0~2점 업무(큰 거래 전략, 브랜드 목소리, 최종 발행 승인)는 사람이, 3~5점도 나가기 전 사람이 승인
- Claude Code는 유료 계정 필요, 웹 채팅만 쓰면 파일을 직접 붙여넣어 저장
- 파일을 쓴 사람이 틀리면 에이전트도 틀림: "확인 필요" 칸은 채우기 전까지 위임 금지

## 문제 해결
- 업무가 20개도 안 나옴: 부서 질문을 다시 보고 "이번 주에 실제로 한 일"을 달력·메일함에서 거꾸로 찾고, 큰 덩어리는 2~3개로 쪼갠다
- 점수가 전부 4~5점: 규칙 칸이 낮은 경우가 많으니 신입에게 설명하듯 순서를 적어 규칙을 만들면 점수가 오른다
- 에이전트가 파일을 무시하고 자기 방식대로: 파일 경로를 정확히 주고 "파일의 단계대로"라 적고, 벗어난 지점을 파일의 예외 칸에 기록

## 바로 쓰는 체크리스트
- [ ] Claude Code 설치(`claude --version`) 또는 claude.ai 준비, `~/my-business` 생성
- [ ] 부서 7개 폴더 생성(`ls business`로 확인)
- [ ] 반복 업무 목록(입력/출력이 보이는 단위) 워크시트 작성
- [ ] 업무별 4질문 점수화(0~8), 6점 이상 선별
- [ ] 6점 이상을 7칸 `.md`로 작성(불확실=확인 필요), 파일 수 확인
- [ ] 한 부서 5~10개 파일로 2주 시험, 오류는 프롬프트가 아니라 파일 수정
