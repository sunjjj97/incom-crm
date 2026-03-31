"""
Railway에서 데이터가 제대로 로드되었는지 확인하는 스크립트
"""
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from crm_app.models import Department, Team, TeamMember, ContractCompany

User = get_user_model()

print("=" * 50)
print("Railway 데이터베이스 확인")
print("=" * 50)

# 사용자 확인
user_count = User.objects.count()
print(f"\n[사용자]")
print(f"  총 사용자 수: {user_count}")
if user_count > 0:
    users = User.objects.all()[:5]
    for user in users:
        print(f"  - {user.username} (staff: {user.is_staff}, superuser: {user.is_superuser})")

# 사업부 확인
dept_count = Department.objects.count()
print(f"\n[사업부]")
print(f"  총 사업부 수: {dept_count}")
if dept_count > 0:
    depts = Department.objects.all()[:5]
    for dept in depts:
        print(f"  - {dept.name}")

# 팀 확인
team_count = Team.objects.count()
print(f"\n[팀]")
print(f"  총 팀 수: {team_count}")
if team_count > 0:
    teams = Team.objects.all()[:5]
    for team in teams:
        print(f"  - {team.name} (사업부: {team.department.name if team.department else '없음'})")

# 팀원 확인
member_count = TeamMember.objects.count()
print(f"\n[팀원]")
print(f"  총 팀원 수: {member_count}")
if member_count > 0:
    members = TeamMember.objects.all()[:5]
    for member in members:
        print(f"  - {member.name} (팀: {member.team.name if member.team else '없음'})")

# 계약업체/매출 확인
company_count = ContractCompany.objects.count()
print(f"\n[계약업체/매출]")
print(f"  총 계약업체 수: {company_count}")
if company_count > 0:
    companies = ContractCompany.objects.all()[:5]
    for company in companies:
        print(f"  - {company.company_name} (금액: {company.payment_amount:,}원)")

print("\n" + "=" * 50)
print("확인 완료!")
print("=" * 50)

