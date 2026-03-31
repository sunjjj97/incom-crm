#!/bin/bash
set -e

echo "=========================================="
echo "Railway 배포 시작"
echo "=========================================="

# DATABASE_URL 확인
if [ -z "$DATABASE_URL" ]; then
    echo "⚠ 경고: DATABASE_URL 환경 변수가 설정되지 않았습니다."
    echo "Railway에서 PostgreSQL 서비스를 추가했는지 확인하세요."
else
    echo "✓ DATABASE_URL 설정됨"
fi

echo "데이터베이스 마이그레이션 실행 중..."
python manage.py migrate --noinput || echo "⚠ 마이그레이션 실패 (계속 진행)"

echo "=========================================="
echo "Gunicorn 서버 시작"
echo "=========================================="
echo "Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn crm_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 4 --timeout 300 --graceful-timeout 300 --keep-alive 5

