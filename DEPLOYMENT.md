# 배포 가이드 - 인컴 CRM

직원들이 외부에서 사용할 수 있도록 배포하는 방법입니다.

## 🚀 빠른 배포 (Railway 권장)

### 1단계: GitHub에 코드 업로드

1. **Git 저장소 초기화** (아직 안 했다면)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **GitHub에 새 저장소 생성**
   - GitHub.com에 로그인
   - "New repository" 클릭
   - 저장소 이름 입력 (예: `incom-crm`)
   - Public 또는 Private 선택
   - "Create repository" 클릭

3. **로컬 저장소를 GitHub에 연결**
   ```bash
   git remote add origin https://github.com/사용자명/저장소명.git
   git branch -M main
   git push -u origin main
   ```

### 2단계: Railway 계정 생성 및 프로젝트 생성

1. **Railway 회원가입**
   - https://railway.app 접속
   - GitHub 계정으로 로그인 (추천)

2. **새 프로젝트 생성**
   - Railway 대시보드에서 "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 방금 만든 저장소 선택
   - "Deploy Now" 클릭

### 3단계: PostgreSQL 데이터베이스 추가

1. **Railway 프로젝트 대시보드에서**
   - "+ New" 버튼 클릭
   - "Database" → "Add PostgreSQL" 선택
   - PostgreSQL이 자동으로 추가되고 `DATABASE_URL` 환경 변수가 설정됩니다

### 4단계: 환경 변수 설정

1. **Railway 프로젝트 대시보드에서**
   - "Variables" 탭 클릭
   - 다음 환경 변수 추가:

   ```
   SECRET_KEY=여기에-강력한-랜덤-문자열-생성
   DEBUG=False
   ALLOWED_HOSTS=*.up.railway.app
   ```

2. **SECRET_KEY 생성 방법:**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   또는 온라인 도구 사용: https://djecrety.ir/

### 5단계: 정적 파일 수집 설정

1. **settings.py 확인**
   - 이미 `whitenoise`가 설치되어 있고 설정되어 있는지 확인
   - `STATIC_ROOT`가 설정되어 있는지 확인

2. **Railway에서 빌드 명령 추가** (필요시)
   - 프로젝트 설정에서 "Build Command" 추가:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

### 6단계: 배포 완료 후 작업

1. **마이그레이션 실행**
   - Railway 대시보드에서 "Deployments" 탭 클릭
   - 최신 배포의 "View Logs" 확인
   - 마이그레이션이 자동으로 실행되는지 확인
   - 수동 실행이 필요하면:
     - "Connect" 탭에서 터미널 접속
     - 다음 명령 실행:
     ```bash
     python manage.py migrate
     ```

2. **관리자 계정 생성**
   - Railway 터미널에서:
   ```bash
   python manage.py createsuperuser
   ```
   - 사용자명과 비밀번호 입력

### 7단계: 도메인 확인

1. **Railway 도메인 확인**
   - Railway 대시보드에서 "Settings" → "Networking" 탭
   - 생성된 도메인 확인 (예: `your-app-name.up.railway.app`)

2. **접속 테스트**
   - 브라우저에서 생성된 도메인으로 접속
   - 로그인 페이지 확인
   - 관리자 계정으로 로그인 테스트

### 8단계: 커스텀 도메인 설정 (선택사항)

1. **도메인 구매** (예: Namecheap, GoDaddy)
2. **Railway에서 커스텀 도메인 추가**
   - Settings → Networking → Custom Domain
   - 도메인 입력 및 DNS 설정

---

## 📋 배포 후 체크리스트

- [ ] 모든 환경 변수 설정 완료
- [ ] PostgreSQL 데이터베이스 연결 확인
- [ ] 마이그레이션 실행 완료
- [ ] 관리자 계정 생성 완료
- [ ] 웹사이트 접속 및 로그인 테스트
- [ ] 매출 등록/수정 테스트
- [ ] 통계 페이지 확인
- [ ] 정적 파일 (CSS, JS) 정상 작동 확인

---

## 🔒 보안 설정

### 프로덕션 환경 권장사항:

1. **DEBUG=False** (반드시!)
   ```
   DEBUG=False
   ```

2. **강력한 SECRET_KEY** 사용
   - 절대 공개하지 않기
   - GitHub에 업로드하지 않기 (`.gitignore`에 `.env` 포함됨)

3. **HTTPS 사용**
   - Railway는 자동으로 HTTPS 제공

4. **ALLOWED_HOSTS 설정**
   ```
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   ```

---

## 🌐 다른 배포 옵션

### Render
- GitHub 연동 가능
- PostgreSQL 지원
- 무료 플랜 제공
- https://render.com

### AWS (Elastic Beanstalk)
- 더 복잡하지만 더 많은 제어 가능
- EC2 + RDS 조합

### Heroku
- 유료 플랜만 제공 (무료 플랜 종료)

---

## ❓ 문제 해결

### 마이그레이션 에러
- Railway 터미널에서 수동으로 실행
- `python manage.py migrate`

### 정적 파일이 안 보임
- `python manage.py collectstatic --noinput` 실행
- WhiteNoise 설정 확인

### 데이터베이스 연결 에러
- `DATABASE_URL` 환경 변수 확인
- PostgreSQL 서비스가 실행 중인지 확인

### 로그 확인
- Railway 대시보드 → Deployments → View Logs
- 오류 메시지 확인

---

## 📞 지원

문제가 발생하면 Railway 로그를 확인하거나 개발자에게 문의하세요.

