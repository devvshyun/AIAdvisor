# DESIGN.md: AIAdvisor 데모 페이지

제품 맥락은 저장소 루트의 `PRODUCT.md`에 있습니다. 이 페이지는 스킬 속 웹 디자인 가이드가 권하는 도구 중 **taste-skill(design-taste-frontend)** 키트로 지었습니다. 색, 서체, 히어로, 내비게이션, 꼬리말, 버튼, 스크롤 연출은 사람이 고르지 않고 키트의 스크립트로 뽑았습니다. 레이아웃 시스템, 모션 레이어, 히어로 레이아웃은 키트 파일(`docs/assets/`)을 그대로 씁니다.

`docs/assets/`의 키트 파일은 [taste-skill](https://github.com/Leonxlnx/taste-skill)(MIT 라이선스, © 2026 Leonxlnx)에서 가져왔고, 라이선스 전문은 `docs/assets/LICENSE-taste-skill.txt`에 있습니다.

## 뽑은 결과 (deal)
| 항목 | 결과 | 뽑은 명령 |
|---|---|---|
| 페이지 종류 | software (개발자 도구) | |
| 히어로 | `centred`: 가운데 제목, 그 아래 제품 창 | `assets/layout/deal.mjs --type software --has ui` |
| 팔레트 | `green-black-bone`: 바탕 `#161c1a`, 글자 `#e3e2da`, 포인트 `#9fc7b8` | `scripts/start.mjs deal --page software` |
| 서체 | Mona Sans + Geist Mono (한글은 Pretendard가 받침) | 같은 명령 |
| 모서리 | `sharp` (개발자 도구 기준) | `start.mjs css --radius sharp` |
| 내비게이션 | `nav-mega` | sections.md 2장의 뽑기 |
| 꼬리말 · 마무리 | `footer-statement` · `close-type` | 같은 뽑기 |
| 리듬 · 버튼 · 마크 | `space` · `arrow` · `ring` | 같은 뽑기 |
| 히어로 효과 | `prism-dispersion` (WebGL, 제품 창 뒤 바탕) | `scripts/effects.mjs pick --slots hero --palette dark` |
| 밝은 바탕 | `sage` (녹흑 팔레트에 맞춤) | `<html data-ground>` |
| 스크롤 모먼트 | 처음엔 `pinned-chapters`를 뽑았으나, 스크롤이 길다는 피드백으로 빼고 클릭 탭으로 바꿈 | `scripts/moments.mjs pick --kind scroll --fits section` |

## 화면 구성
한 섹션이 정확히 한 화면이나 두 화면을 차지합니다.

1. 히어로 (1): 알림 한 줄, 제목, 설명, 버튼 두 개, 제품 창
2. 상황별 추천 결과 (1): 왼쪽 상황 목록, 오른쪽 결과 화면이 한 창 안에 있는 app-frame
3. 동작 순서 (1, 모바일 2): 단계를 누르면 오른쪽 창이 바뀌는 탭
4. 두 가지 모드 (1, 모바일 2)
5. 카탈로그와 레시피 (1, 모바일 2): 분야를 누르면 왼쪽에 레시피 단계, 오른쪽에 그 분야 도구(종류, 한 줄 설명)가 나오는 탐색기. 관리가 멈춘 도구는 취소선. `scripts/build_demo.py`가 `references/catalog/*.yaml`과 `references/recipes/*.md`로 만듭니다
6. 가이드 78편 (1, 모바일 2): 주제를 누르면 가이드 제목과 한 줄 요약이 펼쳐지는 탐색기, 가이드를 누르면 GitHub 전문
7. 설치 (1): 환경별 탭과 터미널 창
8. 자주 묻는 질문 (1, 모바일 2): 답이 모두 열려 있음
9. 방명록 (1): 왼쪽 안내, 오른쪽 giscus 창(고정 높이, 안에서 스크롤). 테마는 `docs/giscus-theme.css`, 설정은 `docs/SETUP-DISCUSSIONS.md`
10. 마무리와 꼬리말 (1)

## 키트 규칙에서 벗어난 곳
- 한글 때문에 `--font-*` 변수에 Pretendard를 대체 서체로 붙였습니다. 키트는 `:root`를 출력된 그대로 두라고 합니다.
- 스크롤 모먼트는 뽑아서 넣었다가(`pinned-chapters`) 스크롤이 길다는 피드백으로 뺐습니다. 지금 페이지에는 모먼트가 없고, 움직임은 히어로 창의 대화 연출과 키트 모션 레이어(호버·누름·탭 전환)뿐입니다.
- 히어로: 제목을 2줄("Claude Code 도구 추천 스킬")로, 설명을 1줄로 줄였습니다. 화면 높이 860px 이하에서는 제목을 줄이고 창 속 도구 실행 줄을 숨겨, 대화의 버튼이 창 아래 흐림 구간(아래 18%) 위에서 끝나게 했습니다. 레시피가 실수로 꼽는 "대화가 흐림 속에 들어가는 상태"를 피하려는 조정입니다.
- 키트의 일관성 검사(`consistency.mjs`)와 레이아웃 검사(`check.mjs`)는 이 환경에서 헤드리스 Chrome이 뜨지 않아 돌리지 못했습니다. 같은 검사 코드(`layout-check.js`)를 브라우저 안에서 직접 실행했습니다.

## 확인 결과
- 방명록 추가 후(2026-11-06) `layout-check.js`: 1440×900, 1024×768, 820×1180, 768×1024, 375×812 모두 발견 0건. 키트의 `.panel`은 배경 그라데이션이 붙어서 쓰지 않고 `figure`로 감쌌습니다. 휴대폰에서 자주 묻는 질문이 다음 섹션을 덮어서 두 화면(`--hm: 2`)으로 늘렸습니다.
- 카탈로그 섹션 추가 후(2026-11-06) `layout-check.js`: 1440×900, 1024×768, 820×1180, 768×1024, 375×812 모두 발견 0건. 창 안의 목록은 `ul`/`ol` 대신 `role="list"` div로 만들었습니다. 페이지 수준 목록으로 잡히면 단 선에 맞추라는 지적이 나오기 때문입니다. `data-ui`는 키트 스크립트가 안의 이름을 바꿔 쓰므로 쓰지 않았습니다.
- 히어로 버튼과 흐림: 설명 문구를 바꾼 뒤 1440×900, 1366×768에서 대화 버튼이 흐림 구간 위에 있는 것을 화면으로 확인
- `layout-check.js`: 1440×900, 1024×768, 820×1180, 768×1024, 375×812 모두 발견 0건
- 히어로 버튼과 흐림 시작점: 900px 높이 72px 위, 800px 24px 위, 768px 1px 위
- 가로 스크롤 없음, 탭 전환 동작, 모먼트 로드 확인
- 확인하지 못한 것: 키트의 `consistency.mjs`(카피·명암비·링크 검사), `perf.mjs`(무게), 움직임 줄이기 설정을 실제로 켠 화면

## 컨셉 A·B (2026-11-09)

기본 페이지는 그대로 두고, 같은 내용을 레퍼런스 하나씩만 따라 다시 지은 페이지 두 개를 함께 둔다. 세 페이지 왼쪽 아래의 "컨셉" 버튼으로 오가며, 보던 섹션(demo, how, kit, faq, guestbook)을 이어서 연다(`docs/concept-switch.js`).

| 컨셉 | 위치 | 레퍼런스 | 방향 |
|---|---|---|---|
| 기본 | `docs/index.html` | taste-skill 키트 | 녹흑 팔레트, 한 섹션 한 화면 |
| A | `docs/concept-a/` | linear.app | 거의 검정 바탕, 조인 산세리프 제목, 제품 화면을 크게 |
| B | `docs/concept-b/` | bun.sh | 흰 바탕, 문서형 정보 밀도, 가로 막대와 검은 코드 블록 |

- A·B는 레퍼런스의 구조와 리듬만 가져왔고 로고·문구·브랜드 색 조합은 쓰지 않았다. 무엇을 가져오고 뺐는지는 각 폴더의 `NOTES.md`.
- A·B의 상황별 예시, 카탈로그, 레시피, 가이드 목록은 `docs/data/*.json`을 읽어 그린다. 이 JSON은 `scripts/build_demo.py`가 `references/`와 기본 페이지의 예시에서 만들기 때문에, 내용이 바뀌어도 세 페이지가 같은 데이터를 보여 준다.
- 섹션은 6개(히어로, 상황별 결과, 동작 방식, 추천 근거, 질문·방명록, 마무리)로 기본 페이지의 10개보다 적다.
