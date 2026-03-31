"""
로컬 데이터베이스의 데이터를 JSON 파일로 내보내는 스크립트
Railway 배포 시 이 데이터를 가져와 사용할 수 있습니다.
"""
import os
import sys
import django

# Windows 인코딩 문제 해결
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 로컬 환경에서는 SQLite 사용 (DATABASE_URL 설정 안 함)
os.environ.pop('DATABASE_URL', None)

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.core.management import call_command

# 모든 앱 데이터 내보내기
print("데이터 내보내기 시작...")
print("-" * 50)

# 각 앱의 데이터를 별도 파일로 내보내기
apps_to_export = [
    'auth.user',  # 사용자 데이터 (admin 계정 포함)
    'crm_app.Department',  # 사업부
    'crm_app.Team',  # 팀
    'crm_app.TeamMember',  # 팀원
    'crm_app.ContractCompany',  # 계약업체
]

output_files = []

for app in apps_to_export:
    filename = f'{app.replace(".", "_")}.json'
    output_path = f'exported_data/{filename}'
    
    # exported_data 폴더가 없으면 생성
    os.makedirs('exported_data', exist_ok=True)
    
    try:
        print(f"내보내는 중: {app} -> {output_path}")
        # UTF-8 인코딩으로 명시적으로 저장
        call_command('dumpdata', app, indent=2, output=output_path, natural_foreign=True, natural_primary=True)
        
        # 파일이 UTF-8로 저장되었는지 확인하고 재인코딩
        try:
            with open(output_path, 'rb') as f:
                content = f.read()
            # UTF-8로 디코딩 시도
            content_str = content.decode('utf-8')
            # UTF-8로 다시 저장 (BOM 없이)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content_str)
        except UnicodeDecodeError:
            # CP949나 다른 인코딩으로 저장된 경우
            try:
                with open(output_path, 'rb') as f:
                    content = f.read()
                # CP949로 디코딩 시도
                content_str = content.decode('cp949')
                # UTF-8로 다시 저장
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content_str)
            except Exception:
                pass  # 이미 UTF-8일 수도 있음
        
        output_files.append(output_path)
        print(f"✓ 성공: {output_path}")
    except Exception as e:
        print(f"✗ 실패: {app} - {str(e)}")

print("-" * 50)
print("모든 데이터 내보내기 완료!")
print(f"\n내보낸 파일:")
for file in output_files:
    print(f"  - {file}")
print("\n이 파일들을 Railway에 업로드한 후 load_data.py 스크립트를 실행하세요.")

