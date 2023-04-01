# Generated by Django 4.1.7 on 2023-03-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'مدير الموقع'), ('install_supervisor', ' مدير التركيبات'), ('repair_supervisor', '  مدير الصيانة'), ('company', 'شركة'), ('quarter_supervisor', 'مشرف كوارتر '), ('sales', 'بائع'), ('accountant', 'محاسب'), ('technician', 'فني'), ('excution', 'تنفيذ كوارتر '), ('quarter_sales', 'مبيعات كوارتر '), ('egypt_office', 'مكتب مصر  ')], default='sales', max_length=25),
        ),
    ]