from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Department, Team, TeamMember, ContractCompany


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'created_at']
    list_filter = ['department']
    search_fields = ['name']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'email', 'phone', 'created_at']
    list_filter = ['team']
    search_fields = ['name', 'email']
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'team', 'email', 'phone')
        }),
        ('사용자 계정 (선택사항)', {
            'fields': ('user',),
            'description': '팀원에게 로그인 권한이 필요한 경우에만 사용자 계정을 연결하세요. 일반적으로는 비워두면 됩니다.',
            'classes': ('collapse',),  # 기본적으로 접혀있음
        }),
    )


@admin.register(ContractCompany)
class ContractCompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'representative', 'contract_date', 'contract_expiry', 'payment_amount', 'team_member', 'team']
    list_filter = ['contract_date', 'team', 'team_member']
    search_fields = ['company_name', 'representative', 'phone']
    date_hierarchy = 'contract_date'


# User 관리 커스터마이징
# 기본 User 등록을 해제하고 커스텀 UserAdmin으로 다시 등록
admin.site.unregister(User)

class UserAdmin(BaseUserAdmin):
    """사용자 관리 - 비밀번호 변경, 삭제, 추가 기능 포함"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'password_change_link']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']
    list_per_page = 25
    
    # 사용자 추가 권한 활성화
    add_form_template = 'admin/auth/user/add_form.html'
    
    def password_change_link(self, obj):
        """비밀번호 변경 링크"""
        if obj.pk:
            url = reverse('admin:auth_user_password_change', args=[obj.pk])
            return format_html('<a href="{}" class="button">비밀번호 변경</a>', url)
        return '-'
    password_change_link.short_description = '비밀번호 변경'
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('개인 정보', {'fields': ('first_name', 'last_name', 'email')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('중요한 날짜', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
            'description': mark_safe(
                '<div style="background-color: #e7f3ff; padding: 15px; border-left: 4px solid #2196F3; margin-bottom: 20px; border-radius: 4px;">'
                '<h3 style="margin-top: 0; color: #1976D2;">📝 사용자 계정 생성 안내</h3>'
                '<ul style="margin-bottom: 0; padding-left: 20px;">'
                '<li><strong>아이디:</strong> 사용자의 이름으로 입력하세요 (예: 김민우, 이성민 등)</li>'
                '<li><strong>비밀번호:</strong> 초기 비밀번호는 <strong style="color: #d32f2f;">1234</strong>로 설정하는 것을 권장합니다.</li>'
                '<li><strong>비밀번호 확인:</strong> 위와 동일하게 <strong style="color: #d32f2f;">1234</strong>를 입력하세요.</li>'
                '<li><strong>권한 설정:</strong> 일반 직원 계정은 <strong>is_staff</strong>와 <strong>is_superuser</strong>를 <span style="color: #d32f2f;">체크 해제</span>하세요. (읽기 전용 권한)</li>'
                '<li><strong>비밀번호 변경:</strong> 사용자는 로그인 후 사이드바의 "비밀번호 변경" 메뉴에서 본인의 비밀번호를 변경할 수 있습니다.</li>'
                '</ul>'
                '</div>'
            ),
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """사용자 추가/수정 폼 커스터마이징"""
        form = super().get_form(request, obj, **kwargs)
        # 새 사용자 생성 시 (obj가 None인 경우)
        if obj is None:
            # 비밀번호 필드에 도움말 추가
            if 'password1' in form.base_fields:
                form.base_fields['password1'].help_text = '초기 비밀번호는 1234를 권장합니다.'
            if 'password2' in form.base_fields:
                form.base_fields['password2'].help_text = '비밀번호 확인을 위해 동일한 비밀번호를 입력하세요.'
        return form

# User 모델을 Admin에 등록 (한글 이름으로 표시)
admin.site.register(User, UserAdmin)

# Admin 사이트 제목 및 헤더 설정
admin.site.site_header = '인컴 CRM 관리자'
admin.site.site_title = '인컴 CRM'
admin.site.index_title = '관리자 페이지'

