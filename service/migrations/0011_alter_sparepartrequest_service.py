# Generated by Django 4.1.7 on 2023-03-21 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_alter_service_options_sparepartrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparepartrequest',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sp_request', to='service.service'),
        ),
    ]
