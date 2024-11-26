# Generated by Django 4.1.5 on 2024-11-26 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0012_alter_staffrequest_requestedvacationtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffrequest',
            name='staff_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='staff_id', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffrequest',
            name='requestedVacationTime',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='staffrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]