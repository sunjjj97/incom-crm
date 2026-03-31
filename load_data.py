"""
Railway 배포 후 JSON 파일에서 데이터를 가져오는 스크립트
export_data.py로 내보낸 데이터를 Railway PostgreSQL 데이터베이스에 로드합니다.
"""
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.core.management import call_command

# exported_data 폴더의 모든 JSON 파일 로드
exported_data_dir = 'exported_data'

if not os.path.exists(exported_data_dir):
    print(f"오류: {exported_data_dir} 폴더를 찾을 수 없습니다.")
    print("먼저 export_data.py를 실행하여 데이터를 내보내세요.")
    exit(1)

print("데이터 가져오기 시작...")
print("-" * 50)

# 로드 순서가 중요합니다 (외래키 관계 때문에)
load_order = [
    'auth_user.json',  # 사용자 먼저
    'crm_app_Department.json',  # 사업부
    'crm_app_Team.json',  # 팀 (사업부 필요)
    'crm_app_TeamMember.json',  # 팀원 (팀 필요)
    'crm_app_ContractCompany.json',  # 계약업체 (팀원, 팀 필요)
]

for filename in load_order:
    filepath = os.path.join(exported_data_dir, filename)
    
    if os.path.exists(filepath):
        try:
            print(f"가져오는 중: {filepath}")
            call_command('loaddata', filepath, verbosity=1)
            print(f"✓ 성공: {filepath}")
        except Exception as e:
            print(f"✗ 실패: {filepath} - {str(e)}")
            print("  (이미 존재하는 데이터일 수 있습니다. 건너뜁니다.)")
    else:
        print(f"⚠ 파일 없음: {filepath} (건너뜀)")

print("-" * 50)
print("데이터 가져오기 완료!")

