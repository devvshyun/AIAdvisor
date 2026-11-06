# 쇼케이스 고정 프롬프트

비포와 애프터에 **글자 하나 바꾸지 않고** 같은 프롬프트를 넣는다. 도구를 부르는 말(예: `/caveman`)이 필요한 경우만 애프터 앞에 붙이고, 그 차이를 결과에 적는다.

## code-tour (graphify, lsp-plugins)

작업 폴더: 이 저장소 루트(`project-upgrade-advisor`). 파일 90여 개라 "탐색량" 차이가 드러난다.

```
scripts/build_demo.py가 references/INDEX.md를 만드는 흐름을 설명해줘. 카탈로그 yaml과 레시피 md를 어디서 어떻게 읽는지, INDEX.md의 각 섹션이 어느 함수에서 나오는지 함수 이름과 함께 알려줘. 파일은 고치지 마.
```

## short-answer (caveman)

작업 폴더: 이 저장소 루트.

```
references/catalog/SCHEMA.md를 읽고, 카탈로그 항목을 새로 추가할 때 꼭 채워야 하는 키와 자주 틀리는 점을 정리해줘. 파일은 고치지 마.
```

## fresh-docs (context7)

작업 폴더: 빈 임시 폴더. 실행 전에 라이브러리를 고른다(RUNBOOK의 context7 절 참고). `<LIB>`와 `<VERSION>`만 바꾼다.

```
<LIB> <VERSION>에서 <TASK>를 하는 최소 예제 코드를 써줘. 이 버전에서 바뀐 API가 있으면 그걸 기준으로 써. 파일 하나로, 설명은 세 줄 이내.
```

## web-fix (frontend-design, web-design-guidelines)

작업 폴더: `showcase/fixtures/web/`을 복사한 임시 폴더.

```
index.html이 AI가 만든 티가 난다. 같은 내용(제품 소개, 기능 세 가지, 가입 버튼)을 유지하면서 디자인을 고쳐 index.html에 덮어써줘. 외부 이미지는 쓰지 마.
```

web-design-guidelines는 고치지 않고 검토만 시킨다.

```
index.html의 UI를 검토해서 문제를 file:line 형식으로 목록으로 줘. 파일은 고치지 마.
```

## page-check (playwright-cli)

작업 폴더: `showcase/fixtures/web/`을 복사한 임시 폴더.

```
index.html을 브라우저에서 열었을 때 375px 폭에서 깨지는 곳이 있는지 확인하고 결과를 알려줘. 파일은 고치지 마.
```

## tidy-edit (claude-code-hooks)

작업 폴더: `showcase/fixtures/coding/`을 복사한 임시 폴더.

```
ledger/report.py의 monthly 함수에 빈 줄과 공백만 있는 줄을 건너뛴다는 docstring을 한 줄 추가해줘. 다른 줄은 손대지 마.
```

## risky-edit (security-guidance)

작업 폴더: `showcase/fixtures/coding/`을 복사한 임시 폴더.

```
ledger/backup.py에 restore_from_file(path) 함수를 추가해줘. 파일을 바이너리로 읽어서 restore에 넘기면 돼.
```
