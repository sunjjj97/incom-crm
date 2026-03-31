"""
Railway에서 데이터를 다시 로드하는 스크립트 (기존 데이터 삭제 후 재로드)
"""
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.core.management import call_command

# exported_data 폴더의 모든 JSON 파일 로드
exported_data_dir = 'exported_data'

print("=" * 50)
print("Railway 데이터 재로드 시작")
print("=" * 50)

# exported_data 폴더 확인
if not os.path.exists(exported_data_dir):
    print(f"❌ 오류: {exported_data_dir} 폴더를 찾을 수 없습니다.")
    print("먼저 GitHub에서 파일이 제대로 푸시되었는지 확인하세요.")
    exit(1)

# exported_data 폴더 내용 확인
print(f"\n{exported_data_dir} 폴더 내용:")
files = os.listdir(exported_data_dir)
for file in files:
    filepath = os.path.join(exported_data_dir, file)
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✓ {file} ({size:,} bytes)")

print("\n" + "=" * 50)
print("기존 데이터 삭제 중...")
print("=" * 50)

# 기존 데이터 삭제 (주의: 모든 데이터가 삭제됩니다)
try:
    call_command('flush', '--noinput', verbosity=0)
    print("✓ 기존 데이터 삭제 완료")
except Exception as e:
    print(f"⚠ 기존 데이터 삭제 중 오류: {e}")
    print("(계속 진행합니다...)")

print("\n" + "=" * 50)
print("데이터 가져오기 시작...")
print("=" * 50)

# 로드 순서가 중요합니다 (외래키 관계 때문에)
load_order = [
    'auth_user.json',  # 사용자 먼저
    'crm_app_Department.json',  # 사업부
    'crm_app_Team.json',  # 팀 (사업부 필요)
    'crm_app_TeamMember.json',  # 팀원 (팀 필요)
    'crm_app_ContractCompany.json',  # 계약업체 (팀원, 팀 필요)
]

success_count = 0
fail_count = 0

for filename in load_order:
    filepath = os.path.join(exported_data_dir, filename)
    
    if os.path.exists(filepath):
        try:
            print(f"\n📥 가져오는 중: {filename}")
            call_command('loaddata', filepath, verbosity=2)
            print(f"✓ 성공: {filename}")
            success_count += 1
        except Exception as e:
            print(f"✗ 실패: {filename}")
            print(f"  오류: {str(e)}")
            fail_count += 1
    else:
        print(f"⚠ 파일 없음: {filename}")
        fail_count += 1

print("\n" + "=" * 50)
print("데이터 가져오기 완료!")
print("=" * 50)
print(f"성공: {success_count}개")
print(f"실패: {fail_count}개")

if success_count == len(load_order):
    print("\n✅ 모든 데이터가 성공적으로 로드되었습니다!")
else:
    print("\n⚠ 일부 데이터 로드에 실패했습니다. 오류 메시지를 확인하세요.")

