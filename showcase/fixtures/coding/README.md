# 코딩 비포 재료

일부러 문제를 심어 둔 작은 Python 패키지다. 실행하지 말고 도구에 읽히기만 한다.

| 파일 | 심어 둔 것 | 쓰는 쇼케이스 |
|---|---|---|
| `ledger/money.py` | `parse_amount`가 세 파일에서 쓰인다 | `lsp-plugins` (참조 찾기) |
| `ledger/report.py` | 포맷이 흐트러진 코드 | `claude-code-hooks` (편집 뒤 포매터) |
| `ledger/backup.py` | `pickle.loads`, `shell=True` 문자열 명령, `eval` | `security-guidance` |

비밀 키 예시는 저장소에 넣지 않는다(GitHub push protection과 gitleaks가 막는다). 필요하면 RUNBOOK의 방법으로 실행할 때 만들고 지운다.
