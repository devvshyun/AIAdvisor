# Claude Code 한도 이후에도 작업을 이어가는 OmniRoute 입문 가이드
- 원문: https://lazyowen.com/guides/omniroute
- 도구·주제: OmniRoute + Claude Code · 비용 절약 / 한도 이후 폴백 + 토큰 압축 (2026-08-06 갱신, npm 공개판 v3.8.48 기준, STEP 8개 · 약 32분)
- 한 줄 요약: Claude Code와 여러 AI 제공자 사이의 로컬 게이트웨이를 세워, Claude 한도가 끝나면 연결해 둔 다른 모델로 요청을 넘기고 긴 도구 출력은 보내기 전에 압축한다.

## 언제 쓰나
- Claude Code 한도가 끝난 뒤에도 연결한 다른 모델로 작업을 이어가고 싶을 때
- 긴 로그·빌드·테스트 출력의 토큰을 줄이고 싶을 때
- 게이트웨이=Claude Code 요청을 먼저 받아 연결된 AI 중 어디로 보낼지 정하는 중간 서버, 로컬=지금 쓰는 내 컴퓨터

## 준비물 / 필요 도구
- OmniRoute: https://omniroute.online/ · https://github.com/diegosouzapw/OmniRoute (MIT)
- Claude Code: npm 패키지 `@anthropic-ai/claude-code` (Node 22+ 필요) · 설치 문서 https://code.claude.com/docs/en/setup
- Node.js 22.x 또는 24.x~26.x (23.x는 지원 범위 아님), npm — https://nodejs.org/en/download
- 공식 문서(v3.8.48): README https://github.com/diegosouzapw/OmniRoute/blob/v3.8.48/README.md · 설치 https://github.com/diegosouzapw/OmniRoute/blob/v3.8.48/docs/guides/SETUP_GUIDE.md · Claude Code 연결 https://github.com/diegosouzapw/OmniRoute/blob/v3.8.48/docs/guides/CLAUDE-CODE-CONFIGURATION.md · CLI https://github.com/diegosouzapw/OmniRoute/blob/v3.8.48/docs/guides/CLI-INTEGRATIONS.md · 무료 tier https://github.com/diegosouzapw/OmniRoute/blob/v3.8.48/docs/reference/FREE_TIERS.md · 압축 https://github.com/diegosouzapw/OmniRoute/blob/v3.8.48/docs/compression/COMPRESSION_GUIDE.md
- 비용: OmniRoute 자체는 무료 오픈소스. 연결한 제공자의 과금은 별개(아래 주의)
- 용어: 제공자(Provider)=요청을 실제 처리하는 AI 서비스 / Endpoint=OmniRoute에 접속하는 주소+인증 키 지점 / OAuth=비밀키 복사 없이 계정 로그인으로 권한 부여 / combo=먼저 쓸 모델과 실패 시 넘길 모델을 순서대로 묶은 설정 / dry-run=변경 없이 결과만 보여 주는 시험 실행

## 단계별 방법
**Quick Start** (OmniRoute를 실행한 터미널은 그대로 열어 둠)
```bash
node --version
npm --version
npm install -g omniroute@latest
omniroute --version
omniroute
```
브라우저에서 http://localhost:20128 → Providers에서 제공자 연결, Endpoints에서 OmniRoute API 키 생성 후 새 터미널에서:
```bash
export OMNIROUTE_API_KEY="<Dashboard → Endpoints에서 복사한 키>"
omniroute launch
```
Claude Code 입력 화면이 열리면 성공.

**설치~검증 위임 프롬프트 뼈대 (Claude Code)**
- 역할: OmniRoute 설치·연결 검증 담당. 맥락: 미설치일 수 있는 프로젝트
- 채울 곳: [프로젝트 상황 한 줄], [OS·셸], [기술 스택], [목표 한 줄]
- 작업: ① `command -v omniroute`, `omniroute --version` 및 Node·npm·Claude Code 버전 점검 ② 없으면 공식 문서 확인 후 `npm install -g omniroute@latest`, 서버를 열고 대시보드에서 제공자 연결·접근 키 생성 안내 ③ 순서대로 검증: `omniroute --version` → `omniroute status` → `omniroute doctor` → `curl http://localhost:20128/v1/models -H "Authorization: Bearer $OMNIROUTE_API_KEY"` → `curl http://localhost:20128/v1/chat/completions`(헤더 `Authorization: Bearer $OMNIROUTE_API_KEY`, `Content-Type: application/json`, 본문 `{"model":"auto","messages":[{"role":"user","content":"연결 확인이라고만 답해줘"}]}`) → 대시보드 요청 로그 확인 ④ OmniRoute가 무엇이고 한도 뒤에 어떻게 넘기는지 쉽게 설명
- 제약: 비밀키 값 출력·저장 금지, 미지원 Node 버전·설치/연결 오류를 건너뛰지 말 것, 기존 파일·테스트 파손 금지
- 출력/검증: 각 검증 결과와 버전·연결 상태. 하나라도 실패하면 완료 보고 금지

**STEP 1. 실행 환경 확인 (3분)**
```bash
node --version
npm --version
npm install -g @anthropic-ai/claude-code@latest     # Claude Code가 없을 때
claude --version
```
- Node 버전이 안 맞으면 nodejs.org에서 지원 버전으로 교체 후 터미널 재시작

**STEP 2. OmniRoute 설치하고 서버 열기 (5분)**
```bash
npm install -g omniroute@latest
omniroute --version
omniroute                 # 서버 실행 화면이 남음. 이 터미널 유지
```
| 용도 | 주소 |
|---|---|
| 대시보드 | http://localhost:20128 |
| OpenAI 호환 API | http://localhost:20128/v1 |
| Claude Code용 Base URL | http://localhost:20128 |
- Claude Code용 주소에는 `/v1`을 붙이지 않음(Claude Code가 `/v1/messages`를 직접 붙임)
- 새 터미널에서 `omniroute status`, `omniroute doctor` → 치명적 오류 없고 대시보드가 열리면 다음 단계

**STEP 3. 제공자와 API 키 연결 (5분)**
1. 대시보드 Providers에서 제공자 연결(API 키/OAuth/인증 없는 무료 경로 등 제공자마다 다름). v3.8.48 빠른 시작 예시는 Kiro AI, OpenCode Free — 무료 조건·자동화 허용 범위는 바뀔 수 있으니 이용약관 확인
2. 자동 전환까지 쓰려면 성격이 다른 경로 2개 이상 권장: 평소 쓰는 구독/품질 우선 모델 → 저비용 API 모델 → 약관 확인한 무료 tier
3. Endpoints에서 API 키 생성 직후 복사(프롬프트·저장소·캡처에 넣지 않기)
```bash
export OMNIROUTE_API_KEY="<Endpoints에서 복사한 키>"
curl http://localhost:20128/v1/models \
  -H "Authorization: Bearer $OMNIROUTE_API_KEY"
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer $OMNIROUTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"연결 확인이라고만 답해줘"}]}'
omniroute providers list
omniroute providers test-all
```
- 모델 목록(`data` 또는 `models`)에 연결한 모델이 보이면 성공, 두 번째 요청은 짧은 답이 오고 대시보드 요청 로그에 남음. 실패 항목은 해당 제공자의 인증·이용 조건부터 재확인

**STEP 4. 숫자를 정확히 이해하기 (3분)**
- v3.8.48 문서: 전체 제공자 250개, 무료 tier 90개+ (250개가 전부 무료라는 뜻 아님)
- 매달 반복되는 무료량 약 15.4억 토큰(README는 약 16억으로 반올림). 한 계정에 한 번에 주는 양이 아니라 40개+ 제공자의 공식 무료 상한을 중복 없이 합산한 추정치
- 첫 달 가입 크레딧은 별개. 무료 tier 종료·조건 변경 시 합계가 내려가므로 설치 버전의 대시보드 수치가 최종값
| 오해 | 정확한 뜻 |
|---|---|
| 250개 모델이 전부 무료 | 제공자 250개 중 무료 tier가 90개+ |
| 내 계정 하나에 월 16억 토큰 지급 | 여러 제공자의 공식 무료 상한 합산 추정치 |
| 무료 경로면 품질이 같다 | 모델마다 품질·속도·읽는 길이·도구 지원이 다름 |
| 자동 전환이면 절대 안 멈춘다 | 모든 경로가 실패하면 요청도 실패 |

**STEP 5. Claude Code를 OmniRoute로 실행 (3분)**
```bash
export OMNIROUTE_API_KEY="<Endpoints에서 복사한 키>"
omniroute launch        # 상태 확인 후 주소·인증 값을 넣어 claude 실행. 별도 설정 파일 없음
```
- 프로필 방식(모델별 연결 설정을 이름으로 저장):
```bash
omniroute setup-claude --dry-run                         # 만들 프로필 미리보기(파일 변경 없음)
omniroute setup-claude --only "<provider 또는 model ID 일부>"
omniroute launch --profile "<생성된 프로필 이름>"          # ~/.claude/profiles/<이름>/settings.json, 인증 값은 프로필에 안 씀
```
- 프로필 없이 직접 지정(Base URL에 `/v1` 금지):
```bash
export ANTHROPIC_BASE_URL="http://localhost:20128"
export ANTHROPIC_AUTH_TOKEN="$OMNIROUTE_API_KEY"
claude
```
- 연결 확인 프롬프트(뼈대): 현재 작업은 연결 확인, 프로젝트 파일 수정 금지, 사용 가능한 도구를 한 줄로 요약하고 "OmniRoute 연결 확인 완료"라고 답하기 → 응답과 대시보드 요청 로그 기록 확인

**STEP 6. 자동 전환 경로 만들기 (5분)**
1. 대시보드 Combos에서 순서대로: 평소 쓰는 구독/품질 우선 → 저비용 API → 이용약관 확인한 무료 모델
2. 전략은 순서대로 소진하려면 `priority` 또는 `fill-first`
3. 저장 후 대시보드에 표시되는 combo 모델 ID를 복사해 Claude Code에서 사용
4. 처음엔 경로 3개만(실패 지점 찾기 쉬움)
```bash
omniroute status
omniroute providers list
omniroute providers test-all
```
- 실제 전환 시험: 첫 경로를 잠시 끄고 짧은 요청을 한 번 보낸 뒤 바로 복원
- 같은 요청을 모든 제공자·계정에 반복 전송하지 말 것(무료량만 줄어듦)

**STEP 7. 토큰 압축 켜기 (5분)** — 대시보드 Context & Cache에서 모드 선택, Preview로 원문/압축 비교
| 모드 | 대상 | 문서상 절감 |
|---|---|---|
| Off | 원문 그대로 | 0% |
| Lite | 공백·중복·안전한 형식 정리 | 약 15% |
| Standard | 긴 자연어 표현 | 약 30% |
| Aggressive | 오래된 대화·긴 도구 결과 요약 | 약 50% |
| Ultra | 관련도 기반 가지치기·코드 블록 압축 | 약 75% |
| RTK | 터미널·테스트·빌드·git 출력 | 60~90% |
| Stacked | RTK 뒤 Caveman 적용 | 줄일 수 있는 구간의 78~95% |
- RTK와 Caveman이 같은 입력을 모두 줄일 수 있을 때 공식 계산 평균 89.2%. 모든 요청·토큰이 같은 비율로 줄지는 않음. 짧은 프롬프트·이미 압축된 코드는 거의 안 줄 수 있음
- 절차: 실제 긴 로그를 Preview에 붙임 → 오류·경고·파일명·숫자 보존 비교 → 기본은 Lite부터 → 긴 테스트/빌드 출력 작업에만 RTK 또는 Stacked → 어긋나면 즉시 Off
- 코드·URL·경로·JSON 보호 규칙이 있어도 결과가 항상 같다고 단정 금지. 배포·보안 점검·데이터 이동 같은 중요 작업은 원문을 먼저 보존

**STEP 8. 안전하게 운영하기 (3분)**
- 서버·설정은 내 컴퓨터에서 돌지만 요청은 선택된 외부 AI 제공자로 전달됨(프롬프트가 내 컴퓨터 안에만 남지 않음)
- `.env`·API 키·고객 정보를 프롬프트에 넣지 않기 / 무료 tier의 개인용·자동화·대리 접속 제한 확인 / 포트 20128을 인터넷에 공개하지 않기 / 원격 이전 시 HTTPS + 권한 범위를 좁힌 접근 키 / 유료 제공자는 대시보드의 비용·사용량 한도부터 설정 / 작업 전후 `git status`와 테스트 확인
```bash
omniroute doctor
omniroute logs --follow      # 자동 수정보다 진단 먼저
```

## 핵심 팁 · 주의사항
- 유료/자동 과금 키를 combo에 넣으면 무료량 초과 시 비용 발생 → 연결 전에 비용·사용량 한도 설정
- Base URL에 `/v1`을 붙이면 Claude Code가 OmniRoute를 거치지 않음
- 자동 전환이어도 연결한 모든 경로가 실패하면 요청도 실패
- 숫자(250개/90개+/약 15.4억 토큰)는 추정치, 최종값은 설치 버전 대시보드

## 문제 해결 (FAQ)
- `npm install -g omniroute`가 Node 버전 오류로 멈춤 → `node --version` 확인, v3.8.48 지원 범위(22.x 또는 24.x~26.x)로 교체 후 재설치
- 20128 포트 충돌:
```bash
omniroute --port 3000
omniroute launch --port 3000     # 대시보드가 http://localhost:3000 으로 바뀜
```
- Claude Code가 OmniRoute를 거치지 않음 → `ANTHROPIC_BASE_URL` 끝의 `/v1` 제거, Claude Code 완전 종료 후 `omniroute launch`
- 401/인증 오류 → 값 출력 없이 키 설정 여부만 확인:
```bash
if [ -n "$OMNIROUTE_API_KEY" ]; then printf 'OMNIROUTE_API_KEY is set\n'; else printf 'OMNIROUTE_API_KEY is missing\n'; fi
```
- `setup-claude`가 프로필을 못 만듦 → 서버를 먼저 실행하고 `omniroute setup-claude --dry-run`과 `/v1/models` curl로 확인
- 자동 전환이 안 됨 → 활성 제공자가 1개뿐이거나 combo에 대체 경로 없음. Providers 연결 상태 확인 후 Combos에 두 번째 경로 추가
- 압축을 켰는데 안 줄어듦 → 짧은 프롬프트·코드 중심·이미 정리된 로그는 줄일 부분이 적음. Preview에 실제 긴 테스트/빌드 출력으로 비교

## 바로 쓰는 체크리스트
- [ ] Node 22.x 또는 24.x~26.x 확인
- [ ] `omniroute doctor` 정상, 서버 터미널 유지
- [ ] Providers 2개 이상 + OmniRoute API 키 생성
- [ ] `/v1/models` 응답 및 `auto` 모델 짧은 요청 확인
- [ ] `omniroute launch`로 Claude Code 실행 (Base URL에 `/v1` 없음)
- [ ] Combo 3경로 구성, 첫 경로를 잠시 꺼서 전환 시험 후 복원
- [ ] 압축은 Preview 확인 후 Lite부터, 이상하면 Off
- [ ] 유료 제공자 한도 설정, 포트 20128 비공개, `.env`·키는 프롬프트에 넣지 않기
