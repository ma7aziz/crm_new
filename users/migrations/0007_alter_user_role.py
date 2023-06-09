# Generated by Django 4.1.7 on 2023-04-04 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_quarter_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'مدير الموقع'), ('install_supervisor', ' مدير التركيبات'), ('repair_supervisor', '  مدير الصيانة'), ('company', 'شركة'), ('technician', 'فني'), ('sales', 'بائع'), ('quarter_supervisor', 'مشرف كوارتر '), ('accountant', 'محاسب'), ('quarter_sales', 'مندوب كوارتر'), ('egypt_office', 'مكتب مصر  ')], default='sales', max_length=25),
        ),
    ]
