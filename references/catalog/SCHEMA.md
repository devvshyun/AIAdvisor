# 카탈로그 항목 형식

`catalog/<area>.yaml`은 도구 하나가 항목 하나인 목록이다. `scripts/check_catalog.py --validate`가 이 형식을 검사한다.

| 키 | 필수 | 뜻 |
|---|---|---|
| `id` | 예 | 소문자·숫자·하이픈. 카탈로그 전체에서 하나뿐 |
| `name` | 예 | 도구 이름 |
| `kind` | 예 | `skill`, `plugin`, `mcp`, `cli`, `built-in`, `github-action`, `service` 중 하나 |
| `area` | 예 | `web-design`, `coding`, `automation` 중 하나 (새 분야는 여기에 더한다) |
| `what` | 예 | 무엇을 하는지, 한국어 한 문장. 직접 쓴 문장 |
| `when` | 예 | 언제 쓰면 좋은지 |
| `not_when` | 예 | 언제 쓰지 말아야 하는지 |
| `install` | 예 | 공식 문서의 설치 명령 그대로. Windows가 다르면 함께 적는다. `built-in`이면 켜는 방법 |
| `verify` | 예 | 설치나 연결이 됐는지 확인하는 명령 또는 방법 |
| `repo` | 아니오 | GitHub 저장소 주소 (없으면 `null`) |
| `docs` | 예 | 공식 문서 주소 |
| `license` | 아니오 | SPDX 이름. 모르면 `null` |
| `stars` | 아니오 | 기준일의 별 수. 모르면 `null` |
| `last_push` | 아니오 | 저장소 마지막 push 날짜 `YYYY-MM-DD` |
| `maintained` | 예 | 보관되지 않았고 180일 안에 push가 있으면 `true` |
| `cost` | 예 | `free`, `paid`, `needs account` 등 |
| `needs` | 아니오 | 필요한 키, 계정, 런타임 버전 |
| `overlaps` | 아니오 | 같은 일을 하는 다른 항목의 `id` 목록 |
| `also` | 아니오 | 이 도구가 함께 쓰이는 다른 분야 목록. 도구는 한 파일에만 두고, 다른 분야에서도 찾을 수 있게 여기에 적는다 |
| `risks` | 예 | 권한, 전역 설치, 유료 API, 외부로 나가는 데이터 등. 없으면 "특이 사항 없음" |
| `always_on_tokens` | 아니오 | 문서에 나온 상시 토큰 비용. 모르면 `null` |
| `hands_on` | 아니오 | 이 저장소 작업에서 직접 써 본 기록. `YYYY-MM-DD: 무엇을 해 봤고 어땠는지` 한 줄. 문서로만 확인했으면 이 키를 두지 않는다 |
| `source_checked` | 예 | 이 항목을 확인한 기준일 `YYYY-MM-DD` |
| `sources` | 예 | 확인에 쓴 주소 목록 |
