# 힉스필드로 AI 인플루언서 만들기
- 원문: https://lazyowen.com/guides/higgsfield-ai-influencer-genjutsu
- 도구·주제: Higgsfield · ChatGPT 플러그인 · AI 인플루언서 / 모션 전이 영상(Genjutsu)
- 한 줄 요약: 힉스필드에서 캐릭터를 만들고 Genjutsu로 참고 영상의 동작을 입혀, 인스타 게시 후 Launchpoint 캠페인에 제출하는 5단계 흐름. (원문 갱신 2026-10-11, 읽는 데 10분, 따라 하면 약 23분)

## 언제 쓰나
- 얼굴 없이(가상 캐릭터로) 숏폼 영상 계정을 운영하고 싶을 때
- 유행하는 춤/동작을 내 캐릭터에게 그대로 입히고 싶을 때
- 캐릭터 한 명을 만들어 두고 실제 영상의 움직임을 입혀 올리는 방식. 원문은 12일 만에 팔로워 23만을 넘긴 AI 캐릭터 계정을 소개.

## 준비물 / 필요 도구
- Higgsfield: https://higgsfield.ai/ (웹 서비스, 오픈소스 아님. 가입 시 무료 생성 최대 5회)
- ChatGPT 플러그인 설치: https://higgsfield.ai/mcp (플러그인 디렉터리를 쓸 수 있는 ChatGPT 계정 필요)
- AI Influencer Studio: https://higgsfield.ai/ai-influencer-studio
- Genjutsu: 원본 영상의 움직임·카메라·타이밍은 두고 인물/물건만 바꿔 주는 힉스필드 영상 도구(웹, 설치 없음)
- Launchpoint 캠페인 "AI Videos ONLY": https://launchpoint.sh/deals
- 요금표: https://higgsfield.ai/pricing
- 참고 글: https://higgsfield.ai/blog/new-ai-influencer , https://higgsfield.ai/blog/higgsfield-genjutsu , https://higgsfield.ai/blog/generate-ai-videos-chatgpt-2026
- 비용: $1 = 20크레딧, 캐릭터 1회 1.12크레딧(약 6센트), 유료 플랜 월 $15부터.
  | 15초 영상 | 크레딧 |
  |---|---|
  | 480p | 40 |
  | 720p | 104 |
  | 1080p | 144 |
- Launchpoint 보상: 인정 조회 1,000회당 $1, 영상당 최대 $2,000, 캠페인 총예산 $1M (소진 시 종료). 예: 50만 회=$500, 200만 회=상한 $2,000. 조회수 보장 없음.

## 단계별 방법
1. **STEP 1 ChatGPT에 힉스필드 연결 (3분)** — 사이트만 쓸 계획이면 건너뛰어도 됨.
   - ChatGPT에서 Plugins Directory 열기 → Higgsfield 검색 → Add → 힉스필드 계정으로 로그인·권한 허용(계정 없으면 먼저 가입) → 새 대화에서 `@Higgsfield` 입력 또는 도구 목록에서 선택. (한국어 UI: 왼쪽 메뉴 '플러그인' = Plugins Directory, 상세 화면 '플러그인 설치' = Add)
   - 디렉터리에서 못 찾으면 https://higgsfield.ai/mcp 의 설치 버튼 이용.
   - 연결 끊김/권한 오류: Settings → Plugins → Higgsfield 에서 재연결. 그래도 안 보이면 STEP 2부터 사이트에서 진행.
   - ChatGPT에서 생성하면 크레딧이 바로 소모될 수 있으니 생성 전 비용 표시를 요청하고, 무료 생성은 사이트에서 먼저 사용.
2. **STEP 2 캐릭터 만들기 (5분)** — 계정의 전부이므로 길에서 마주치면 기억날 얼굴 하나가 목표(너무 평범하면 묻히고 과하면 거부감).
   - AI Influencer Studio에서 Character type 선택: Average(평범) / Bold(눈에 띄지만 친근) / Extreme(코미디·밈용 과장).
   - 설정 19개. 인상을 크게 바꾸는 5개: Hairstyle, Facial hair, Style, Features, Distinctive features.
   - 내 얼굴 기반이면 Upload your photo(내 사진 또는 허락받은 사진만) → Generate(1.12크레딧) → 얼굴 클로즈업 + 전신 2장. 느낌만 아쉬우면 Recreate. 아이디어 없으면 Randomize로 19칸을 채운 뒤 일부만 수정.
   - ChatGPT 프롬프트 뼈대: `@Higgsfield Create an AI Influencer character ...` + Character type, 성별/나이/키/체형, Hairstyle, Hair color, Style, Features, Distinctive feature, Accessories를 열거하고 "영상 만들기 전에 포트레이트와 전신 컷부터 보여 달라"로 끝냄. 외모 칸만 내 캐릭터로 교체.
   - ❌ "예쁜 20대 여자 인플루언서 만들어 줘"(흔한 AI 얼굴) → ✅ Bold로 두고 머리 모양·피부 특징·액세서리 중 눈에 띄는 특징 2~3개 지정.
   - 실존 인물이나 기존 AI 캐릭터를 따라 만들지 말 것.
3. **STEP 3 따라 할 영상 고르기 (5분)**
   - 요즘 뜨는 동작: Explore의 Trending Genjutsu 피드에서 선택(따로 올릴 영상 불필요). 직접 촬영: 길이 4~30초.
   - 촬영 요령: 삼각대로 고정, 고른 조명(창문을 마주 보고), 전신이 프레임 안에, 보통 속도.
   - ❌ 빠르게 도는 춤, 손이 얼굴 앞을 지나가는 동작, 손으로 들고 찍기(얼굴·손이 가장 많이 깨짐) → ✅ 삼각대 + 정면 + 보통 속도의 10~15초 전신 영상.
4. **STEP 4 Genjutsu 적용 (5분)**
   - 캐릭터 열기 → `Turn to motion with Genjutsu` → Motion 탭의 `Motion transfer` → 영상 업로드 또는 STEP 3 동작 선택 → **480p로 먼저 테스트**(얼굴·손·움직임) → 괜찮으면 같은 설정으로 1080p. 비용은 Generate 버튼에 먼저 표시.
   - ChatGPT 프롬프트 뼈대: `@Higgsfield /genjutsu` + 내 캐릭터와 올린 영상 사용, Motion transfer로 움직임·카메라·타이밍 유지하고 캐릭터 고유 의상으로 수행, 480p 테스트 먼저, 1080p 실행 전 비용 표시. (원본 영상을 같은 대화에 올릴 것)
   - Motion 탭의 Objects swap: 옷/상품/장소 중 하나만 바꾸고 나머지 유지(나중에 상품 들리기용).
   - ❌ 처음부터 1080p(얼굴 어긋나면 가장 비싼 생성 낭비) → ✅ 480p를 원본과 나란히 틀어 확인 후 1080p.
5. **STEP 5 업로드·제출 (5분)**
   - 인스타그램에 올릴 때 `Add AI label` 켜기 → https://launchpoint.sh/deals 에서 "AI Videos ONLY" 캠페인 열기 → 규칙 먼저 읽기(인정되는 조회 정의) → 런치포인트 계정 생성 → 인스타 게시물 링크를 제출 칸에 붙여넣기.

**ChatGPT 위임 프롬프트 뼈대(캐릭터 생성~480p 테스트)**: 역할=`@Higgsfield`로 캐릭터를 만들고 Genjutsu 테스트까지 이끄는 제작 담당, 맥락=초보자·플러그인 미연결 가능. 슬롯 `내 캐릭터 = <한 번 보면 기억나는 외모 한 줄>`(나머지 설정은 스스로 결정). 작업: ① Higgsfield 도구 사용 가능 여부 확인 ② 불가하면 Plugins Directory에서 Add·로그인하는 순서를 한 줄씩 안내하고 멈춤 ③ 외모를 AI Influencer 설정(Character type, Hairstyle, Facial hair, Style, Features, Distinctive features)으로 변환해 보여 주고 승인 후 생성 ④ 영상을 올리면 Motion transfer로 480p 테스트 후 다음 할 일 안내. 제약: 크레딧 드는 생성은 매번 비용 먼저 표시·승인 대기, 실존 인물·기존 AI 캐릭터 모방 금지, 1080p는 480p 승인 후에만. 출력: 선택 설정, 사용 크레딧, 생성된 이미지·영상, 남은 문제. 검증: 클로즈업+전신 2장 존재, 480p에서 얼굴이 끝까지 동일인으로 보임. 실패는 완료로 보고하지 말고 실패 단계·원인·조치 제시.

## 핵심 팁 · 주의사항
- 실존 인물처럼 속이지 말고 AI 캐릭터임을 밝힐 것. 남의 캐릭터를 베끼지 말 것.
- 조회수·수익은 누구에게도 보장되지 않음. 캠페인 예산이 소진되면 종료되므로 제출 전 페이지가 열려 있는지 확인.
- 유료 생성 전 비용 확인 필수. 무료 생성 5회를 다 쓰거나 ChatGPT에서 생성하면 크레딧이 소모됨.

## 문제 해결
- 조회 미집계: 캠페인 규칙의 인정 조건 재확인 + 제출 링크가 실제 게시물과 같은지 확인.
- 얼굴이 중간에 바뀜: 정면·밝은 곳에서 찍은 더 짧은 원본으로 재생성.
- 손/몸이 뭉개짐: 원본 동작을 더 느리게, 전신이 화면에 들어오게 촬영.
- 결과가 흐림: 480p 테스트본을 보고 있을 가능성 → 같은 설정으로 1080p 생성.
- 크레딧 요구: 무료 생성 소진 또는 ChatGPT에서 생성 중 → 비용 확인 후 진행 여부 결정.

## 바로 쓰는 체크리스트
- [ ] 힉스필드 계정 + (선택) ChatGPT 플러그인 연결, `@Higgsfield` 호출 확인
- [ ] 캐릭터 유형·핵심 5개 설정 정하고 Generate (클로즈업+전신 확인)
- [ ] 참고 동작 선택 (Trending Genjutsu 또는 4~30초 직접 촬영)
- [ ] Genjutsu 480p 테스트 → 얼굴/손/동작 확인
- [ ] 1080p 재생성 전 크레딧 확인 (15초 144크레딧)
- [ ] 인스타 업로드 시 Add AI label 켜기
- [ ] Launchpoint 캠페인 규칙·잔여 예산 확인 후 링크 제출
