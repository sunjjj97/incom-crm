FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 PostgreSQL 클라이언트 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# start.sh 스크립트를 실행 가능하게 설정
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 정적 파일 수집
RUN python manage.py collectstatic --noinput || true

# 포트 환경 변수 (Railway에서 자동으로 설정됨)
ENV PORT=8000

# 스크립트 실행 (마이그레이션 자동 실행 포함)
CMD ["/app/start.sh"]

