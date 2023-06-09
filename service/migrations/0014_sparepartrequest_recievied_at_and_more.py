# Generated by Django 4.1.7 on 2023-03-28 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0013_service_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparepartrequest',
            name='recievied_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sparepartrequest',
            name='recievied_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sp_recieved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[('new', 'جديد'), ('under_process', 'قيد التنفيذ'), ('hold', 'معلق'), ('done', 'تم'), ('closed', 'انتهي')], default='new', max_length=15),
        ),
    ]
