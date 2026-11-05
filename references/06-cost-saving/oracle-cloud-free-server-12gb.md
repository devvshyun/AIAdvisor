# 오라클 클라우드 12기가 서버 평생 무료로 받는 법
- 도구·주제: Oracle Cloud(OCI) Always Free (Ubuntu, ssh, tmux) · 무료 서버 / 비용 절감
- 한 줄 요약: 오라클 클라우드 Always Free의 Arm(Ampere A1) 2 OCPU·메모리 12GB 서버를 가입부터 생성, ssh 접속, tmux로 봇 상시 구동까지 만들고 무료 범위 안에서 유지한다. (2026-11-04 공개, 읽는 데 11분, 따라 하면 약 33분, STEP 5개)

## 언제 쓰나
- 앱이나 봇(텔레그램 봇, OpenClaw 같은 AI 에이전트)을 24시간 돌릴 서버가 필요한데 월 서버비가 부담스러울 때

## 준비물 / 필요 도구
- 오라클 클라우드 프리 티어: https://www.oracle.com/cloud/free/ · 가입 https://signup.cloud.oracle.com/
  - FAQ: https://www.oracle.com/cloud/free/faq/
  - Always Free 자원 목록: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
  - 첫 서버 튜토리얼: https://docs.oracle.com/en-us/iaas/Content/GSG/Reference/overviewworkflow.htm
  - 홈 리전 안내: https://docs.oracle.com/en-us/iaas/Content/Identity/Tasks/managingregions.htm
- 웹 브라우저, 이메일, 전화번호, 본인 명의 신용카드(PIN 입력 체크카드·가상/일회용/선불카드는 불가)
- ssh (맥·리눅스·윈도 기본 내장), 서버 쪽 tmux
- 비용: Always Free 자원은 계정이 있는 동안 무료. 지원 국가는 가입 시 30일간 쓰는 $300 크레딧도 지급. 유료 계정(Pay As You Go)으로 바꾼 뒤에만 무료 한도 초과분에 요금.
- 라이선스: 오픈소스 아님, 오라클 클라우드 서비스 약관
- 용어: 리전 = 오라클 데이터센터 지역(홈 리전 = 가입 때 고르는 기본 지역, 무료 서버는 여기서만 생성), 인스턴스 = 서버 한 대, OCPU = 오라클의 CPU 성능 단위, SSH = 멀리 있는 서버에 안전하게 접속하는 방법, tmux = 접속을 끊어도 터미널 화면을 서버에 남겨 두는 프로그램
- 무료 자원
| 자원 | 무료 한도 |
|---|---|
| Arm 서버(Ampere A1) | OCPU 2개, 메모리 12GB를 서버 1대 또는 2대로 나눠 사용 |
| AMD 서버 | 1/8 OCPU, 메모리 1GB짜리 2대 |
| 디스크(Block Volume) | 전체 200GB, 백업 5개 |
| 데이터베이스 | Autonomous Database 최대 2개 |
| 외부로 나가는 데이터 | 한 달 10TB |

## 단계별 방법
### 프롬프트 뼈대 A. 서버 첫 접속·사양 확인 위임 (STEP 2 후 터미널에서 `claude` 실행, 첫 메시지)
- 목적: 방금 만든 무료 서버(Ampere A1, Ubuntu)에 접속해 상시 구동 준비 확인
- 역할: 서버 첫 접속·확인 담당. 사용자는 초보, 비밀 키(.key)는 다운로드 폴더에 있음
- 슬롯: [서버 공인 IP = 콘솔 인스턴스 화면의 Public IP address], [내 목표 = 서버에서 돌릴 것(예: 텔레그램 봇 24시간)]. OS·셸·키 위치는 직접 확인
- 작업: ① `ssh -V` 확인, 다운로드 폴더에서 .key 파일 탐색 ② 권한이 400이 아닐 때만 `chmod 400` ③ 키와 공인 IP로 ubuntu 계정 접속 후 `uname -m`, `free -h`, `df -h /`, `tmux -V` 실행(서버 지문 질문은 `accept-new`로 처음 한 번만 수락) ④ 서버 사양과 목표를 tmux 안에서 계속 켜 두려면 다음에 할 일을 초보 눈높이로 안내
- 제약: 서버에서 sudo 전 질문, 비밀 키 내용 출력·복사 금지, 오라클 콘솔 설정·요금제 변경 금지, 기존 파일 덮어쓰기 금지
- 출력: 실행 명령, CPU 종류·메모리·디스크 크기, 바뀐 파일 권한, 남은 오류
- 검증: `uname -m`이 `aarch64`, `free -h`의 Mem 줄과 `df -h /` 디스크 크기가 나와야 하며 실패 시 완료 보고 금지

### Quick Start
https://signup.cloud.oracle.com/ 를 열어 국가·이름·이메일을 넣는 가입 양식이 보이면 성공. 가입은 브라우저에서 끝나고 설치할 프로그램은 없다.

### STEP 1. 가입하고 홈 리전 고르기 (10분)
1. 가입 페이지에서 국가, 이름, 이메일 입력
2. 메일로 온 인증 링크로 이메일 확인 후 나머지 양식 작성
3. 주소, 전화번호, 카드 정보로 본인 확인
4. 홈 리전 선택 후 가입 완료 — 가까운 리전. 한국은 서울(South Korea Central). 춘천(South Korea North)은 Arm 무료 서버를 만들 수 있는 가용 영역이 제한될 수 있음
5. 오라클 클라우드 콘솔에 로그인
- 홈 리전은 계정 생성 후 변경 불가
- 이름·주소·카드 정보는 실제 정보로(틀린 정보나 여러 계정은 정지 사유)
- 카드에 잠깐 승인 보류가 걸릴 수 있으나 보통 3~5일 안에 은행이 풀고 실제 청구는 아님

### STEP 2. 무료 서버(Ampere A1) 만들기 (10분)
1. 콘솔 왼쪽 위 메뉴 Compute → Instances → `Create Instance`
2. 이름 입력, Placement는 기본값
3. 이미지(운영체제) 칸에서 `Always Free-eligible` 표시가 붙은 Ubuntu 선택
4. `Change shape` → Virtual Machine → Ampere → `VM.Standard.A1.Flex` → OCPU 2, 메모리 12GB
5. 네트워크에서 `Assign a public IPv4 address`가 켜져 있는지 확인
6. SSH 키 칸에서 `Generate a key pair for me` → `Save Private Key`로 비밀 키 파일 저장
7. 부트 볼륨은 기본 크기로 두고 `Create` (서버 한 대만 쓸 거면 부트 볼륨을 200GB까지 늘려도 무료)
8. 상태가 `Provisioning` → `Running`이 되면 성공. 인스턴스 화면의 Public IP address를 복사하고, 운영체제가 켜질 때까지 몇 분 더 기다렸다 접속.
- 비밀 키 파일은 생성 후 다시 받을 수 없음: 안전하게 보관, 타인에게 전달 금지
- `Out of host capacity` 오류: 무료 서버 자리가 잠깐 부족한 상태 → 다른 가용 영역(Availability domain)을 고르거나 잠시 후 재시도

### STEP 3. 내 컴퓨터에서 서버 접속하기 (5분)
터미널: 맥은 응용 프로그램 → 유틸리티 → 터미널, 윈도는 시작 메뉴에서 PowerShell.
1. ssh 확인(`OpenSSH_10.3p1, LibreSSL 3.3.6` 같은 버전이 나오면 준비 끝)
```bash
ssh -V
```
2. 키 파일 권한을 나만 읽기로 바꾸고 ubuntu 계정으로 접속(꺾쇠는 내 키 파일 이름·공인 IP로 교체)
```bash
chmod 400 ~/Downloads/<키 파일 이름>.key
ssh -i ~/Downloads/<키 파일 이름>.key ubuntu@<공인 IP>
```
처음 접속 시 서버 지문 질문에는 `yes`. 프롬프트가 `ubuntu@`로 시작하면 성공. 권한을 안 바꾸면 ssh가 키 파일이 너무 열려 있다는 경고와 함께 접속을 거절.
3. 윈도: PowerShell에서는 `chmod` 줄이 실패하니 건너뛰고, 키 파일 속성 → 보안 → 고급 → 상속 사용 안 함 → 내 계정만 남기기로 권한을 바꾼 뒤 ssh 줄 실행
4. 접속한 서버에서 사양 확인
```bash
uname -m
free -h
df -h /
tmux -V
```
`aarch64` = Arm 서버(프로그램은 arm64/aarch64용으로 받기), `free -h` Mem 줄 = 메모리, `df -h /` = 디스크, `tmux -V`에 버전이 나오면 STEP 4 설치 생략.

### STEP 4. 봇을 서버에서 계속 켜 두기 (5분)
1. `tmux -V`에 `not found`가 나오면 서버에서 설치 후 `tmux -V`로 재확인
```bash
sudo apt update && sudo apt install -y tmux
```
2. `bot`이라는 tmux 화면 열기(맨 아래 `[bot]` 초록 줄이 보이면 tmux 안)
```bash
tmux new -s bot
```
3. 그 안에서 내 봇 실행 — 봇 설치 명령은 프로그램마다 다르니 공식 안내에서 리눅스(Ubuntu)·Arm(aarch64)용 명령을 찾아 그대로 붙여넣기
4. 봇이 돌면 `Ctrl + B`를 누르고 손을 뗀 뒤 `D`로 분리. 이후 접속을 끊어도 봇은 서버에서 계속 동작.
5. 다시 접속해 상태 확인: `tmux ls`에 `bot: 1 windows`로 시작하는 줄이 보이면 화면이 살아 있음
```bash
tmux ls
tmux attach -t bot
```
6. 서버를 재시작하면 tmux도 꺼지므로 다시 접속해 같은 순서로 켠다. 텔레그램 봇 토큰 같은 비밀 값은 봇 공식 안내가 정한 자리에만 넣고, 화면 캡처·코드 공유 시 같이 나가지 않는지 확인.

### STEP 5. 무료 범위 안에서 계속 쓰기 (3분)
1. 콘솔 왼쪽 위 메뉴 Governance & Administration → Tenancy Management 아래 Limits, Quotas and Usage
2. 서비스별 무료 한도와 사용량 확인(새 서버·디스크 만들기 전에 먼저)
3. 서버·디스크는 홈 리전에서 `Always Free-eligible` 표시가 붙은 것만 생성

## 핵심 팁 · 주의사항
- ❌ 아무 리전이나 골라 나중에 바꾸기 → ✅ 가까운 리전을 처음부터 신중하게(홈 리전 변경 불가)
- ❌ 처음 보이는 기본 사양으로 생성 → ✅ `Always Free-eligible` 표시의 `VM.Standard.A1.Flex`, OCPU 2·메모리 12GB
- ❌ 키 파일 권한을 그대로 두고 접속 → ✅ `chmod 400` 먼저
- ❌ 접속한 터미널에서 봇을 바로 켜고 창 닫기 → ✅ tmux 안에서 켜고 `Ctrl + B`, `D`로 분리
- ❌ 30일 체험 끝날 때 유료 계정(Pay As You Go)으로 바로 전환 → ✅ 그대로 두기(체험이 끝나도 Always Free 자원은 유지, 전환 시 한도 초과분에 요금이 붙으니 요금 구조를 이해하기 전엔 누르지 말 것)
- 홈 리전 밖 디스크는 무료 한도에 포함되지 않음(체험 기간엔 크레딧 차감, 유료 계정이면 요금)
- 쉬는 서버 회수: 7일간 CPU 사용률(바쁜 시간 상위 5% 제외)·네트워크·메모리 사용률이 모두 20% 미만이면 오라클이 회수할 수 있음 → 중요한 파일은 서버 밖에도 백업
- 30일 넘게 쓰지 않은 계정은 정지될 수 있고, 무료 계정은 1인 1개
- 비밀 키 파일은 재다운로드 불가

## 바로 쓰는 체크리스트
- [ ] 가까운 홈 리전 선택하여 가입(신용카드 요건·실제 정보 확인)
- [ ] `VM.Standard.A1.Flex` 2 OCPU/12GB Ubuntu 인스턴스 생성, 비밀 키 저장, 공인 IP 복사
- [ ] `chmod 400` 후 ssh 접속 성공(`ubuntu@` 프롬프트)
- [ ] `uname -m`(aarch64)/`free -h`/`df -h /`로 사양 확인
- [ ] tmux로 봇 실행 후 분리, `tmux ls`로 확인
- [ ] Limits, Quotas and Usage에서 무료 한도 점검
- [ ] 중요 파일 서버 외부 백업
