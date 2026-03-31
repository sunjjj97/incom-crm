"""
개인별 직원 계정 생성 스크립트
이름 기반으로 아이디를 생성하고 초기 비밀번호는 1234로 설정
"""
import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.contrib.auth.models import User

# 생성할 직원 목록
EMPLOYEE_NAMES = [
    '김민우',
    '김태형',
    '김하연',
    '김희라',
    '나병훈',
    '남영우',
    '서원호',
    '이성민',
    '이승결',
    '이현우',
    '장동희',
    '천명서',
]

DEFAULT_PASSWORD = '1234'  # 초기 비밀번호

def create_username_from_name(name):
    """이름을 기반으로 아이디 생성 (공백 제거)"""
    return name.replace(' ', '').strip()

def create_employee_users():
    """개인별 직원 계정 생성"""
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    print('=' * 50)
    print('개인별 직원 계정 생성 시작')
    print('=' * 50)
    print()
    
    for name in EMPLOYEE_NAMES:
        username = create_username_from_name(name)
        password = DEFAULT_PASSWORD
        
        # 기존 사용자 확인
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # 비밀번호를 1234로 업데이트 (초기화)
            user.set_password(password)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save()
            updated_count += 1
            print(f'✓ 사용자 "{name}" (아이디: {username})의 비밀번호와 권한이 업데이트되었습니다.')
            print(f'  - 비밀번호: {password} (초기 비밀번호)')
            print(f'  - 읽기 전용 (is_staff=False, is_superuser=False)')
            print(f'  - 활성화됨 (is_active=True)')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                is_staff=False,
                is_superuser=False,
                is_active=True
            )
            created_count += 1
            print(f'✓ 새로운 읽기 전용 사용자 "{name}" (아이디: {username})가 생성되었습니다.')
            print(f'  - 아이디: {username}')
            print(f'  - 비밀번호: {password} (초기 비밀번호)')
            print(f'  - 읽기 전용 (수정 불가, 조회만 가능)')
        print()
    
    print('=' * 50)
    print('계정 생성 완료!')
    print('=' * 50)
    print(f'생성된 계정: {created_count}개')
    print(f'업데이트된 계정: {updated_count}개')
    print(f'총 처리된 계정: {created_count + updated_count}개')
    print()
    print('⚠️  중요: 모든 사용자는 초기 비밀번호 1234로 설정되었습니다.')
    print('   사용자들은 로그인 후 본인의 비밀번호를 변경할 수 있습니다.')
    print('   관리자는 Admin 페이지에서 비밀번호를 변경하거나 계정을 관리할 수 있습니다.')

if __name__ == '__main__':
    create_employee_users()

