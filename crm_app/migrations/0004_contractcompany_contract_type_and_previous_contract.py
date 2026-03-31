# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0003_loginlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractcompany',
            name='contract_type',
            field=models.CharField(
                choices=[('new', '신규 계약'), ('renewal', '재계약'), ('additional', '추가 계약')],
                default='new',
                max_length=20,
                verbose_name='계약 유형'
            ),
        ),
        migrations.AddField(
            model_name='contractcompany',
            name='previous_contract',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='related_contracts',
                to='crm_app.contractcompany',
                verbose_name='이전 계약'
            ),
        ),
        migrations.AlterModelOptions(
            name='contractcompany',
            options={'ordering': ['-created_at'], 'verbose_name': '계약업체', 'verbose_name_plural': '계약업체'},
        ),
    ]

