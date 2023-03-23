# Generated by Django 4.1.7 on 2023-03-18 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0002_rename_cretaed_at_service_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='service',
            name='customer_type',
            field=models.CharField(choices=[('cash', 'نقدي'), ('warranty', 'ضمان')], default='cash', max_length=15),
        ),
    ]
