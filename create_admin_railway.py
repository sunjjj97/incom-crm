"""
Railway에서 관리자 계정을 자동으로 생성하는 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
password = '250801'
email = ''

# 기존 admin 사용자가 있으면 삭제
if User.objects.filter(username=username).exists():
    User.objects.filter(username=username).delete()
    print(f"기존 '{username}' 사용자를 삭제했습니다.")

# 새 관리자 계정 생성
user = User.objects.create_superuser(
    username=username,
    email=email,
    password=password
)

print(f"✓ 관리자 계정이 성공적으로 생성되었습니다!")
print(f"  사용자명: {username}")
print(f"  비밀번호: {password}")

