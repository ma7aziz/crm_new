# Generated by Django 4.1.7 on 2023-03-19 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='notes',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
