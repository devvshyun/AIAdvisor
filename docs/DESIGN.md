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
| 스크롤 모먼트 | `pinned-chapters` (#how): 두 화면 동안 고정, 세 단계가 차례로 열림 | `scripts/moments.mjs pick --kind scroll --fits section` |

## 화면 구성
한 섹션이 정확히 한 화면이나 두 화면을 차지합니다.

1. 히어로 (1): 알림 한 줄, 제목, 설명, 버튼 두 개, 제품 창
2. 상황별 추천 결과 (1): 왼쪽 상황 목록, 오른쪽 결과 화면이 한 창 안에 있는 app-frame
3. 동작 순서 (2): pinned-chapters
4. 두 가지 모드 (1, 모바일 2)
5. 가이드 82편 (1, 모바일 2): 행 목록
6. 설치 (1): 환경별 탭과 터미널 창
7. 자주 묻는 질문 (1): 답이 모두 열려 있음
8. 마무리와 꼬리말 (1)

## 키트 규칙에서 벗어난 곳
- 한글 때문에 `--font-*` 변수에 Pretendard를 대체 서체로 붙였습니다. 키트는 `:root`를 출력된 그대로 두라고 합니다.
- 스크롤 모먼트는 키트 기본 추첨이 `word-rotate`(히어로 단어 회전)였습니다. 그런데 히어로에 이미 제품 창의 대화 연출이 있어서, 사용자 요청(스크롤 연출)에 맞게 `--kind scroll`로 다시 뽑았습니다.
- 키트의 일관성 검사(`consistency.mjs`)와 레이아웃 검사(`check.mjs`)는 이 환경에서 헤드리스 Chrome이 뜨지 않아 돌리지 못했습니다. 같은 검사 코드(`layout-check.js`)를 브라우저 안에서 직접 실행했습니다.

## 확인 결과
- `layout-check.js`: 1440×900, 1024×768, 820×1180, 768×1024, 375×812 모두 발견 0건
- 가로 스크롤 없음, 탭 전환 동작, 모먼트 로드 확인
- 확인하지 못한 것: 키트의 `consistency.mjs`(카피·명암비·링크 검사), `perf.mjs`(무게), 움직임 줄이기 설정을 실제로 켠 화면
