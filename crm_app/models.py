from django.db import models
from django.contrib.auth.models import User


class LoginLog(models.Model):
    """로그인 로그 모델"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='사용자')
    username = models.CharField(max_length=150, verbose_name='아이디')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP 주소')
    user_agent = models.TextField(blank=True, null=True, verbose_name='사용자 에이전트')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='로그인 시간')
    success = models.BooleanField(default=True, verbose_name='로그인 성공')
    failure_reason = models.CharField(max_length=200, blank=True, null=True, verbose_name='실패 사유')
    
    class Meta:
        verbose_name = '로그인 로그'
        verbose_name_plural = '로그인 로그'
        ordering = ['-login_time']
    
    def __str__(self):
        status = '성공' if self.success else '실패'
        return f'{self.username} - {self.login_time.strftime("%Y-%m-%d %H:%M:%S")} ({status})'


class Department(models.Model):
    """사업부 모델"""
    name = models.CharField(max_length=100, verbose_name='사업부명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        verbose_name = '사업부'
        verbose_name_plural = '사업부'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Team(models.Model):
    """팀 모델"""
    name = models.CharField(max_length=100, verbose_name='팀명')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='사업부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        verbose_name = '팀'
        verbose_name_plural = '팀'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TeamMember(models.Model):
    """팀원 모델"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='사용자 계정')
    name = models.CharField(max_length=100, verbose_name='이름')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='팀')
    email = models.EmailField(blank=True, null=True, verbose_name='이메일')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='전화번호')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        verbose_name = '팀원'
        verbose_name_plural = '팀원'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ContractCompany(models.Model):
    """계약업체 모델"""
    CONTRACT_TYPE_CHOICES = [
        ('new', '신규 계약'),
        ('renewal', '재계약'),
        ('additional', '추가 계약'),
    ]
    
    company_name = models.CharField(max_length=200, verbose_name='업체명')
    representative = models.CharField(max_length=100, blank=True, null=True, verbose_name='대표자명')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='전화번호')
    contract_date = models.DateField(verbose_name='계약일')
    contract_expiry = models.DateField(verbose_name='계약만료일')
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='결제금액')
    team_member = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='담당 팀원')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='담당 팀')
    notes = models.TextField(blank=True, null=True, verbose_name='비고')
    
    # 계약 유형 및 관계 필드
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPE_CHOICES,
        default='new',
        verbose_name='계약 유형'
    )
    previous_contract = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_contracts',
        verbose_name='이전 계약'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        verbose_name = '계약업체'
        verbose_name_plural = '계약업체'
        ordering = ['-created_at']  # 등록 순서대로 정렬
    
    def __str__(self):
        return self.company_name
    
    def get_contract_type_display_class(self):
        """계약 유형에 따른 CSS 클래스 반환"""
        try:
            contract_type = getattr(self, 'contract_type', 'new')
            type_classes = {
                'new': 'primary',
                'renewal': 'success',
                'additional': 'info',
            }
            return type_classes.get(contract_type, 'secondary')
        except (AttributeError, Exception):
            return 'secondary'

