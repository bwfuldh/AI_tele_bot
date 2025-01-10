# AI 텔레그램 분석 봇 🤖

이 프로젝트는 사용자의 아이디어를 분석하고 전문적인 피드백을 제공하는 텔레그램 봇입니다.

## 🚀 시작하기 전에

### 1. Python 설치하기
1. [Python 공식 사이트](https://www.python.org/downloads/)에서 Python 3.11 다운로드
2. 설치 파일 실행 (반드시 "Add Python to PATH" 옵션 체크!)
3. 설치 완료 후 터미널에서 확인:
   ```bash
   python --version  # Python 3.11.x 가 출력되어야 합니다
   ```

### 2. Git 설치하기
1. [Git 공식 사이트](https://git-scm.com/downloads)에서 Git 다운로드
2. 설치 파일 실행 (기본 옵션으로 설치)
3. 설치 완료 후 터미널에서 확인:
   ```bash
   git --version  # git version x.xx.x 가 출력되어야 합니다
   ```

### 3. 프로젝트 가져오기
1. 터미널을 열고 원하는 폴더로 이동:
   ```bash
   # Windows
   cd C:\Users\사용자이름\Desktop

   # macOS/Linux
   cd ~/Desktop
   ```

2. 프로젝트 복제:
   ```bash
   git clone [프로젝트 URL]
   cd AI_tele_bot
   ```

### 4. 가상환경 설정하기
1. 가상환경 생성:
   ```bash
   # Windows
   python -m venv venv

   # macOS/Linux
   python3 -m venv venv
   ```

2. 가상환경 활성화:
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

### 5. 환경 변수 설정하기
1. `.env.example` 파일을 복사하여 `.env` 파일 생성
   ```bash
   # Windows
   copy .env.example .env

   # macOS/Linux
   cp .env.example .env
   ```

2. 텔레그램 봇 토큰 얻기:
   - 텔레그램에서 [@BotFather](https://t.me/botfather) 검색
   - `/newbot` 명령어로 새 봇 생성
   - 봇 이름과 사용자명 입력
   - 받은 토큰을 `TELEGRAM_TOKEN`에 입력

3. Claude API 키 얻기:
   - [Anthropic Console](https://console.anthropic.com/) 가입
   - API Keys 섹션에서 새 키 생성
   - 생성된 키를 `ANTHROPIC_API_KEY`에 입력

4. 데이터베이스 URL:
   - 로컬 테스트 시: 비워두기 가능
   - Railway 배포 시: 자동으로 설정됨

### 6. 실행하기
```bash
python main.py
```

## ⚠️ 라이센스 주의사항

이 프로젝트는 비공개 소프트웨어이며, 저작권자의 명시적인 허가 없이는 어떠한 형태의 사용, 복제, 수정, 배포도 금지됩니다.
자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🌟 주요 기능

1. **대화형 정보 수집**
   - 아이디어 설명 (자유 입력)
   - 8개 핵심 항목 (버튼 선택)
   - 사용자 친화적 UI

2. **AI 기반 분석**
   - Claude AI를 활용한 심층 분석
   - 체계적인 결과 정리
   - 실용적인 제안 제공

3. **데이터 저장**
   - PostgreSQL 데이터베이스 활용
   - 분석 결과 자동 저장
   - 향후 데이터 활용 가능

## 🛠 기술 스택

- Python 3.11 (필수)
- python-telegram-bot (텔레그램 봇 프레임워크)
- Anthropic Claude AI (AI 분석 엔진)
- PostgreSQL (데이터 저장)
- Docker (배포용)

## 📁 프로젝트 구조

```
AI_tele_bot/
├── bot/
│   ├── conversations.py  # 대화 흐름 관리
│   ├── handlers.py      # 이벤트 핸들러
│   └── messages.py      # 메시지 템플릿
├── services/
│   └── langchain_service.py  # AI 분석 서비스
├── config.py           # 설정 파일
├── database.py        # DB 연결 관리
├── main.py           # 진입점
├── Dockerfile        # 도커 설정
└── railway.toml     # 배포 설정
```

## ⚙️ 환경 변수

```env
TELEGRAM_TOKEN=your_telegram_bot_token
ANTHROPIC_API_KEY=your_claude_api_key
DATABASE_URL=your_postgresql_url
```

## 🚀 배포 방법 (Railway 사용)

1. [Railway](https://railway.app/) 계정 생성

2. 새 프로젝트 생성:
   - Railway 대시보드에서 "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 프로젝트 저장소 선택

3. PostgreSQL 추가:
   - "New" 버튼 클릭
   - "Database" → "PostgreSQL" 선택
   - 자동으로 DATABASE_URL 환경변수 생성됨

4. 환경 변수 설정:
   - "Variables" 탭 클릭
   - TELEGRAM_TOKEN 추가
   - ANTHROPIC_API_KEY 추가

5. 자동 배포 시작:
   - GitHub 저장소에 변경사항을 push하면 자동으로 배포됨
   - "Deployments" 탭에서 배포 상태 확인 가능

## 💡 사용 예시

1. 봇 시작하기:
   - 텔레그램에서 봇 검색
   - `/start` 명령어 입력

2. 아이디어 입력:
   - 자유롭게 아이디어 설명
   - 구체적일수록 좋은 분석 가능

3. 항목 선택:
   - 제시되는 8개 버튼 중 선택
   - 각 항목별 가장 적절한 옵션 선택

4. 분석 결과:
   - AI가 분석한 결과 확인
   - 실행 계획 및 제안사항 검토

## ❗ 자주 발생하는 문제

1. 가상환경 활성화 오류
   - 해결: 터미널을 관리자 권한으로 실행

2. 패키지 설치 오류
   - 해결: pip를 최신 버전으로 업그레이드
   ```bash
   python -m pip install --upgrade pip
   ```

3. 데이터베이스 연결 오류
   - 해결: DATABASE_URL 환경변수 확인

4. 봇 응답 없음
   - 해결: TELEGRAM_TOKEN 확인
   - 해결: main.py 실행 중인지 확인

## 📚 학습 자료

1. Python 기초
   - [Python 공식 튜토리얼](https://docs.python.org/ko/3/tutorial/)
   - [점프 투 파이썬](https://wikidocs.net/book/1)

2. 텔레그램 봇
   - [python-telegram-bot 문서](https://docs.python-telegram-bot.org/)
   - [텔레그램 봇 API](https://core.telegram.org/bots/api)

3. 데이터베이스
   - [PostgreSQL 튜토리얼](https://www.postgresqltutorial.com/)

## 🔒 보안

- 모든 대화는 암호화된 텔레그램 채널을 통해 진행
- 분석 데이터는 안전한 PostgreSQL 데이터베이스에 저장
- API 키는 환경 변수로 관리

## ⚠️ 제한 사항

- 상업적 사용 금지
- 무단 복제/수정 금지
- 재배포 금지
- 소스 코드 공개 금지

## 👥 문의

관리자: @starlenz_inc

---
© 2024 All Rights Reserved.
