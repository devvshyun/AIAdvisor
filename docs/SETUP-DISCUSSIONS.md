# 방명록 설정 (GitHub Discussions + giscus)

데모 페이지에 방명록을 붙인 절차입니다. 2026-11-06에 이 순서대로 설정했고, 실제 쓴 값을 함께 적었습니다. 방문자가 남긴 글은 이 저장소의 Discussions에 쌓이고 알림은 GitHub로 옵니다. 서버나 DB, 비밀 키는 필요 없습니다.

| 단계 | 누가 | 걸리는 시간 |
|---|---|---|
| 1. Discussions 켜기 | 저장소 주인 | 1분 |
| 2. 방명록 카테고리 만들기 | 저장소 주인 | 2분 |
| 3. giscus 앱 설치 | 저장소 주인 | 2분 |
| 4. 설정값 받기 | 저장소 주인 | 3분 |
| 5. 다른 사이트에서 못 쓰게 막기 | Claude | 1분 |
| 6. 페이지에 붙이기 | Claude | 30분 |
| 7. 시험 글로 확인 | 같이 | 5분 |

1~4단계는 저장소 설정과 앱 설치라 주인 계정으로 직접 해야 합니다.

## 동작 방식

giscus는 페이지에 GitHub Discussions 글 하나를 댓글 창으로 띄웁니다. 첫 글이 달릴 때 giscus 봇이 Discussions에 글을 하나 만듭니다. 그 뒤 댓글은 모두 그 글 아래에 달립니다. 방문자는 GitHub로 로그인해 giscus 앱에 권한을 주거나 Discussions에 가서 직접 씁니다.

조건은 세 가지입니다(giscus.app 설정 화면 기준).

- 저장소가 공개 상태다. 비공개면 방문자가 글을 볼 수 없다.
- giscus 앱이 저장소에 설치돼 있다. 없으면 글과 반응을 남길 수 없다.
- 저장소에 Discussions가 켜져 있다.

## 1. Discussions 켜기

1. 저장소 **Settings → General**로 갑니다.
2. **Features**에서 **Discussions**에 체크합니다.

확인: 저장소 위쪽 탭에 **Discussions**가 생깁니다.

## 2. 방명록 카테고리 만들기

1. **Discussions** 탭 → 왼쪽 카테고리 옆 연필 아이콘 → **New category**를 누릅니다.
2. 이름을 정하고 형식(Discussion Format)은 **Announcement**로 고릅니다. 이 저장소는 `GuestPage`로 만들었습니다.

Announcement 형식을 쓰는 이유: 새 글은 주인과 giscus 봇만 만들 수 있고 방문자는 댓글만 답니다. 방명록 글이 여러 개로 갈라지지 않습니다. giscus 설정 화면도 이 형식을 권합니다.

확인: 카테고리 목록에 새 카테고리가 보입니다.

## 3. giscus 앱 설치

1. https://github.com/apps/giscus 에서 **Install**을 누릅니다.
2. **Only select repositories**를 고르고 `devvshyun/AIAdvisor` 하나만 선택합니다.

모든 저장소에 권한을 줄 필요는 없습니다.

확인: https://giscus.app/ko 의 저장소 칸에 `devvshyun/AIAdvisor`를 넣으면 "통과했습니다! 이 저장소는 모든 조건을 만족합니다."가 뜹니다.

## 4. 설정값 받기

https://giscus.app/ko 에서 아래처럼 고릅니다.

| 항목 | 고를 값 | 이유 |
|---|---|---|
| 언어 | 한국어 | |
| 저장소 | `devvshyun/AIAdvisor` | |
| 페이지 ↔ Discussions 연결 | **Discussion 제목이 특정 단어를 포함**, 단어는 카테고리 이름과 같게 (`GuestPage`) | 페이지 주소가 바뀌어도 같은 글을 계속 씁니다 |
| 엄격한 제목 일치 사용 | 켬 | 비슷한 제목 글과 섞이지 않게 |
| 카테고리 | 2단계에서 만든 카테고리, "이 카테고리에서만 Discussion 찾기" 켬 | |
| 기능 | "댓글 위에 댓글 상자 배치", "댓글 느리게 불러오기" 켬 | 스크롤하지 않고 바로 쓰고, 첫 화면 로딩을 가볍게 |
| 테마 | 아무거나 | 6단계에서 페이지 색에 맞춘 테마로 바꿉니다 |

화면 아래에 생긴 `<script>` 코드를 통째로 복사해서 Claude에게 넘깁니다. 안에 든 `data-repo-id`와 `data-category-id`는 페이지에 공개되는 값이라 비밀이 아닙니다.

## 5. 다른 사이트에서 못 쓰게 막기 (Claude)

저장소 맨 위에 `giscus.json`을 둡니다. 여기 적은 주소에서만 방명록이 열립니다.

```json
{
  "origins": ["https://devvshyun.github.io", "http://localhost:8767"]
}
```

`localhost:8767`은 로컬 미리보기용입니다. 필요 없으면 빼도 됩니다.

## 6. 페이지에 붙이기 (Claude)

- 데모 페이지에 `#guestbook` 섹션을 한 화면 크기로 추가하고 4단계의 `<script>`를 넣습니다.
- 페이지 색(녹흑 팔레트)에 맞춘 테마 CSS를 `docs/giscus-theme.css`로 만들고 `data-theme`에 그 주소를 넣습니다. GitHub Pages는 CSS를 `Access-Control-Allow-Origin: *`로 내보내서 giscus가 불러올 수 있습니다.
- 내비게이션과 꼬리말에 방명록 링크를 더합니다.
- 1440, 1024, 820, 768, 375px에서 레이아웃 검사를 다시 돌립니다.

### 이 저장소에 적용한 값

| 항목 | 값 |
|---|---|
| 카테고리 | `GuestPage` (`DIC_kwDOVjk56s4DKfyK`) |
| 연결 | 특정 단어 `GuestPage`, 엄격한 제목 일치 |
| 테마 | `https://devvshyun.github.io/AIAdvisor/giscus-theme.css` (giscus 공식 dark 테마의 색만 페이지 팔레트로 바꿈) |
| 허용 주소 | `giscus.json`: `https://devvshyun.github.io`, `http://localhost:8767` |
| 위치 | 데모 페이지 `#guestbook` 섹션, 자주 묻는 질문 다음 |

## 7. 시험 글로 확인

1. 배포된 페이지의 방명록에 시험 글을 하나 남깁니다.
2. Discussions의 `GuestPage` 카테고리에 `GuestPage` 제목의 글이 생기고 그 아래에 시험 글이 달렸는지 봅니다.
3. GitHub 알림이 오는지 봅니다. 안 오면 아래 "알림 받기"를 설정합니다.
4. 시험 글은 지웁니다.

## 운영

**알림 받기**: 저장소 위쪽 **Watch → Custom → Discussions**에 체크하면 새 글마다 알림이 옵니다. 메일로도 받으려면 GitHub **Settings → Notifications**에서 이메일을 켭니다.

**글 관리**: Discussions에서 댓글마다 **…** 메뉴로 숨기거나 지울 수 있습니다. 글이 너무 많이 달리면 그 글을 **Lock**해서 새 댓글을 막습니다. 같은 사람이 계속 스팸을 남기면 저장소 설정의 **Moderation options**에서 그 사용자를 차단합니다.

## 미리 알아 둘 것

- 방명록에 쓰려면 GitHub 계정이 필요합니다. 계정 없는 방문자의 의견까지 받으려면 이메일로 오는 폼 서비스를 따로 붙여야 합니다.
- 남긴 글은 모두 공개됩니다.
- giscus와 GitHub Discussions API는 아직 바뀌는 중이라 일부 기능이 달라질 수 있다고 giscus가 직접 안내합니다. 동작이 이상하면 giscus.app 설정 화면부터 다시 확인합니다.
- 테마 CSS를 외부 주소에서 불러오면 그 파일을 만든 쪽을 믿어야 합니다. 그래서 이 저장소 안에 둡니다.

확인한 날짜: 2026-11-06 (giscus README, ADVANCED-USAGE.md, giscus.app 설정 화면 문구)
