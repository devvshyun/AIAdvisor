# ChatGPT한테 '사진 고쳐줘' 대신 쓰는 프롬프트 10개
- 원문: https://lazyowen.com/guides/chatgpt-modify-photo-prompt
- 도구·주제: ChatGPT(Images, 사진 편집) · 사진 편집 프롬프트 (프롬프트, 영상·이미지, 12분 읽기, STEP 4개, 약 10분 실습, 2026-09-27 갱신. 검증 기준: ChatGPT Images 2.5, 공식 도움말 확인)
- 한 줄 요약: "사진 고쳐줘" 대신 지킬 것/바꿀 것을 한 번에 적은 영어 편집 프롬프트 10종을 대괄호 칸만 채워 붙여넣어 ChatGPT 사진 편집 품질을 올린다.

## 언제 쓰나
- 사진 보정, 객체 제거, 배경/옷/시간대 변경, 화질 개선, 확장, 눈 수정, 주름 펴기, 색보정을 ChatGPT로 할 때
- "좀 고쳐줘"만 치면 얼굴선까지 손대 딴사람처럼 나오는 문제를 줄이고 싶을 때

## 준비물 / 필요 도구
- ChatGPT (https://chatgpt.com, 웹/iOS/안드로이드). 설치 없음. 계정 하나면 됨.
- 공식 도움말: https://help.openai.com/en/articles/9055440-editing-your-images-with-dall-e · 요금제 https://openai.com/chatgpt/pricing/ · 이용약관 https://openai.com/policies/row-terms-of-use/
- 비용: 무료 요금제도 가능하나 이미지 생성이 제한적·느림. 안내 기준 Go는 한도 증가, Pro는 이미지 생성 무제한(최신 요금은 공식 페이지 확인).
- 결과물은 이용약관상 사용자 소유, 대신 올리는 사진의 권리는 본인에게 있어야 함.

## 단계별 방법
### STEP 1. 붙여넣는 규칙 (1분)
1. 대화창에 고칠 사진을 첨부.
2. 프롬프트 블록을 빈 줄까지 통째로 복사해 같은 메시지에 붙여넣기 (조건이 두 문단에 걸쳐 있어 한 문단만 넣으면 절반이 빠짐: 지킬 것 문단 + 고칠 것 문단).
3. 한 메시지에 편집 하나만 (예: 5번은 배경을 지키라 하고 3번은 배경을 바꾸라 해서 충돌).
4. 결과가 아쉬우면 같은 대화에서 틀어진 곳만 짚어 재요청.
5. 대괄호 칸(2·3·5·6·7번)은 대괄호 기호까지 지우고 영어로 채움.
- ❌ "이 사진 좀 자연스럽게 고쳐줘" (지킬 것이 없어 얼굴까지 편집 대상) ✅ 1번 원문을 통째로 붙여넣기
- ❌ `[OBJECT/PERSON]` 자리에 `the person` ✅ `the man in the red jacket on the left` (위치+옷 색으로 한 명만 지정)

### 보조 프롬프트: 고른 원문을 그대로 적용시키는 래퍼 (프롬프트 뼈대)
- 역할: 첨부 사진을 아래 영어 편집 프롬프트 그대로 고치는 편집 담당. 슬롯: [쓸 프롬프트 = 아래에서 고른 영어 원문 전체].
- 작업: 사진을 직접 보고 확인 → 대괄호 칸이 남아 있으면 편집 전에 무엇으로 채울지 한 번만 질문 → 내 답 외에는 프롬프트를 한 글자도 바꾸지 말고 적용 → 결과 아래에 바뀐 것/그대로 둔 것 안내.
- 제약: preserving/keeping/Preserve 뒤에 나열된 항목은 변경 금지, 언급 안 된 부분도 유지, 없는 편집 추가 금지, 프롬프트가 고치라 한 곳 외 얼굴 손대지 않기.
- 출력/검증: 편집본 1장 + 바뀐 것 3줄 이하 + 그대로 둔 것 3줄 이하. 원본과 비교해 바꾸라 한 것만 바뀌었는지, 지키라 한 것이 유지됐는지 점검, 실패 시 완료 보고 금지.

### STEP 2. 1~3번: 보정·지우기·배경 (3분)
영어 원문은 영어로 그대로 사용(번역해 쓰지 말 것). 뼈대:
1. 전문가 보정 (대괄호 없음): 얼굴은 그대로 두고 빛·선명도만 개선. "Professionally retouch this image while preserving…" 형태. 지킬 것=인물 정체성, 이목구비, 피부 결, 신체 비율, 헤어스타일, 옷, 전체 모습. 개선할 것=조명, 선명도, 색 균형, 노출, 또렷함. 결과는 자연스럽고 사실적으로. 시작 문구: `Professionally retouch this image while preserving the person’s identity, facial features, skin texture, body proportions, hairstyle, clothing, and overall appearance.`
2. 뭐든 지우기: `Remove [OBJECT/PERSON] from this image and realistically reconstruct the area behind it.` 뒤에 배경·조명·그림자·질감·반사·깊이·원근·주변 디테일을 맞춰 자연스럽게 섞으라는 요구. 예: `[OBJECT/PERSON]` → `the man in the red jacket on the left`.
3. 배경 바꾸기: `Replace the current background with [NEW BACKGROUND] while keeping the main subject unchanged.` 인물 얼굴·몸·옷·헤어·포즈·비율·디테일 유지, 조명·그림자·색·원근을 새 환경에 맞춤. 예: `a bright white studio wall with soft light`.
- 확인: 1·3번은 얼굴·머리 모양 유지, 2번은 지운 자리 주변 그림자·질감이 끊기지 않았는지.

### STEP 3. 4~7번: 화질·옷·넓히기·시간대 (3분)
4. 화질 올리기 (대괄호 없음): 원래 구도·내용 유지하며 더 선명·깔끔·전문적으로. 디테일, 조명, 노출, 색 정확도, 대비, 선명도 개선, 인공적으로 보이지 않게.
5. 옷 바꾸기: `Replace the current outfit with [OUTFIT DESCRIPTION] while keeping the person’s identity completely unchanged.` 얼굴·헤어·체형·포즈·손·피부톤·비율·표정·배경 유지, 새 옷은 몸에 자연스럽게. 예: `a navy wool coat over a white shirt`.
6. 사진 넓히기: `Expand this image beyond its current borders to [ASPECT RATIO/SIZE] while keeping everything inside the original image unchanged.` 배경·바닥·벽·하늘·풍경·사물·조명·질감·패턴을 자연스럽게 이어 줌. 예: `16:9`.
7. 시간대 바꾸기: `Change this scene from [CURRENT TIME OF DAY] to [SUNRISE / GOLDEN HOUR / SUNSET / NIGHT].` 하늘·빛 방향·색온도·반사·그림자·창문·주변 환경을 새 시간대에 맞게 조정. 예: `midday` → `golden hour` (넷 중 하나만 남기고 슬래시와 나머지 삭제). 골든아워=해 뜬 직후/지기 직전의 낮고 따뜻한 빛.
- 확인: 4번은 구도 유지, 5번은 얼굴·손·배경 유지, 6번은 원본 테두리 안쪽 불변, 7번은 하늘색·그림자 방향이 새 시간대에 맞는지.

### STEP 4. 8~10번: 눈·주름·색보정 (3분)
8. 감은 눈 뜨게 (대괄호 없음): 감기거나 반쯤 감긴 눈을 얼굴과 어울리게 자연스럽게. 표정·시선 방향·조명·눈 모양·정체성 유지, 티 나지 않게 사실적으로. 단체 사진에서 한 명만 눈 감았을 때.
9. 옷 주름 펴기 (대괄호 없음): 거슬리는 주름·구김·뭉침·고르지 않은 천을 펴되 소재·핏·박음선·질감·자연스러운 접힘은 유지, 디지털로 그린 느낌 금지.
10. 프로처럼 색보정 (대괄호 없음): 피부톤 자연스럽게, 인물 그대로, 영화 같은 전문 색보정. 밝은/어두운 부분 균형, 대비·채도 다듬기, 사진 전체 한 톤으로 마무리.
- 확인: 8번은 눈 모양·시선, 단체 사진이면 다른 사람 얼굴 불변, 9번은 질감·박음선 유지, 10번은 피부톤 자연스러움.
- 용어: 색보정(컬러 그레이딩)=사진 전체 색감·밝기를 한 분위기로 맞추는 작업.

## 핵심 팁 · 주의사항
- ⚠️ 사람 사진은 결과 편차가 있음. 지킬 것을 다 적어도 얼굴선이 미세하게 달라질 수 있어 증명사진처럼 정확도가 필요한 용도에는 부적합.
- ⚠️ 무료 요금제는 제한적·느림, 여러 장 연속 편집 시 한도에 걸림.
- ⚠️ 영역 선택 도구로 칠해도 공식 도움말 설명대로 편집이 선택 영역 밖으로 번질 수 있음.
- ⚠️ 권리 없는 사진 업로드 금지, 다른 사람 얼굴을 바꾸는 편집은 문제될 수 있음.
- 여러 편집을 한꺼번에 시키지 말고 한 메시지에 하나.
- 대상은 위치+옷 색으로 특정.

## 바로 쓰는 체크리스트
- [ ] 사진 첨부
- [ ] 편집 하나만 골라 프롬프트(빈 줄 포함 전체) 복사
- [ ] 대괄호를 영어 설명으로 채움 (위치+옷 색으로 대상 특정)
- [ ] 한 메시지 = 한 편집
- [ ] 원본과 나란히 비교 (얼굴/배경/그림자)
- [ ] 아쉬운 부분만 같은 대화에서 재요청
