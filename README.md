# 인컴 CRM 시스템

회사 매출 및 계약업체 관리 시스템

## 주요 기능

- ✅ 팀별/개인별 매출 기록 및 조회
- ✅ 월별/년도별 매출 통계
- ✅ 사업부별 매출 관리
- ✅ 계약업체 관리 (전체/팀별 조회)
- ✅ 대시보드 (월별 매출 그래프 - Chart.js)
- ✅ 엑셀 백업 기능 (계약업체, 팀원 데이터)
- ✅ Admin 인증 시스템
- ✅ 직관적인 UI (Bootstrap 5)

## 설치 방법

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# 또는
source venv/bin/activate  # Mac/Linux
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정 (선택사항)

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

### 5. 관리자 계정 생성

```bash
python manage.py createsuperuser
```

사용자 이름, 이메일, 비밀번호를 입력하세요.

### 6. 서버 실행

```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000` 또는 `http://localhost:8000`으로 접속하세요.

## 사용 방법

### 초기 설정

1. **사업부 등록**: Django Admin (`/admin/`)에서 사업부를 등록합니다.
2. **팀 등록**: Django Admin에서 팀을 등록하고 사업부를 연결합니다.
3. **팀원 등록**: 웹 인터페이스의 "팀원 관리" 메뉴에서 팀원을 등록합니다.

### 매출 등록

1. "매출 관리" 메뉴에서 "매출 등록" 버튼을 클릭합니다.
2. 다음 정보를 입력합니다:
   - 업체명
   - 대표자명
   - 전화번호
   - 계약일
   - 계약만료일
   - 결제금액
   - 담당 팀원 (선택)
   - 담당 팀 (선택)
   - 비고 (선택)

### 데이터 조회

- **대시보드**: 월별 매출 그래프를 확인할 수 있습니다.
- **매출 관리**: 전체 매출을 필터링하여 조회할 수 있습니다.
- **계약업체**: 전체 계약업체 리스트를 확인할 수 있습니다.
- **통계**: 년도별, 월별, 팀별, 개인별, 사업부별 매출 통계를 그래프로 확인할 수 있습니다.

### 엑셀 백업

"엑셀 백업" 메뉴를 클릭하면 모든 데이터가 엑셀 파일로 다운로드됩니다.
- 계약업체 시트: 모든 계약업체 정보
- 팀원 시트: 모든 팀원 정보

## 배포

### Render 배포

1. GitHub에 코드를 푸시합니다.
2. Render에서 새 Web Service를 생성합니다.
3. GitHub 저장소를 연결합니다.
4. 환경 변수를 설정합니다:
   - `SECRET_KEY`: Django 시크릿 키
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app-name.onrender.com
5. Build Command: `pip install -r requirements.txt && python manage.py migrate`
6. Start Command: `gunicorn crm_project.wsgi:application`

### Railway 배포 (권장)

#### 1단계: GitHub에 코드 업로드

1. GitHub 계정에 로그인합니다.
2. 새 저장소를 생성합니다 (예: `incom-crm`).
3. 프로젝트 폴더에서 다음 명령을 실행합니다:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/incom-crm.git
git push -u origin main
```

#### 2단계: Railway에 배포

1. [Railway](https://railway.app/)에 접속하여 계정을 만듭니다 (GitHub 계정으로 로그인 가능).

2. **"New Project"** 버튼을 클릭합니다.

3. **"Deploy from GitHub repo"**를 선택하고 GitHub 저장소를 연결합니다.

4. Railway가 자동으로 프로젝트를 감지하고 배포를 시작합니다.

#### 3단계: PostgreSQL 데이터베이스 추가

1. Railway 대시보드에서 프로젝트를 선택합니다.
2. **"+ New"** 버튼을 클릭합니다.
3. **"Database"** → **"Add PostgreSQL"**를 선택합니다.
4. PostgreSQL이 자동으로 추가되고 `DATABASE_URL` 환경 변수가 설정됩니다.

#### 4단계: 환경 변수 설정

1. 프로젝트 대시보드에서 **"Variables"** 탭을 클릭합니다.
2. 다음 환경 변수를 추가합니다:

```
SECRET_KEY=your-secret-key-here  # Django 시크릿 키 (강력한 랜덤 문자열 생성)
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app  # Railway가 제공하는 도메인
```

**SECRET_KEY 생성 방법:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 5단계: 마이그레이션 실행

1. Railway 대시보드에서 프로젝트를 선택합니다.
2. **"Settings"** 탭에서 **"Generate Domain"**을 클릭하여 도메인을 생성합니다.
3. 배포가 완료되면 Railway가 자동으로 마이그레이션을 실행합니다.
   - 수동으로 실행하려면: **"Deployments"** → **"..."** → **"View Logs"**에서 확인

#### 6단계: 관리자 계정 생성

배포 후 Railway CLI를 사용하거나, 웹 터미널에서 실행:

```bash
railway run python manage.py createsuperuser
```

또는 Railway 대시보드의 **"Connect"** 탭에서 터미널 접속 후:
```bash
python manage.py createsuperuser
```

#### 완료!

- 웹사이트 주소: `https://your-app-name.up.railway.app`
- 관리자 페이지: `https://your-app-name.up.railway.app/admin/`
- 로그인 페이지: `https://your-app-name.up.railway.app/login/`

#### 추가 설정 (선택사항)

- **커스텀 도메인**: Railway 대시보드에서 커스텀 도메인을 추가할 수 있습니다.
- **자동 배포**: GitHub에 푸시하면 자동으로 재배포됩니다.
- **환경 변수**: `Variables` 탭에서 언제든지 환경 변수를 수정할 수 있습니다.

## 🌐 배포하기

직원들이 외부에서 사용할 수 있도록 배포하는 방법은 **[DEPLOYMENT.md](DEPLOYMENT.md)** 파일을 참고하세요.

### 빠른 배포 요약:

1. **GitHub에 코드 업로드**
2. **Railway에서 프로젝트 생성** (GitHub 연동)
3. **PostgreSQL 데이터베이스 추가**
4. **환경 변수 설정** (SECRET_KEY, DEBUG=False 등)
5. **관리자 계정 생성**

자세한 내용은 `DEPLOYMENT.md` 파일을 확인하세요.

---

## 기술 스택

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: SQLite (개발), PostgreSQL (프로덕션 권장)
- **Deployment**: Gunicorn, WhiteNoise

## 라이선스

이 프로젝트는 회사 내부 사용을 위한 것입니다.

