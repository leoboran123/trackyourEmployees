# Generated by Django 4.1.5 on 2024-11-23 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0004_alter_stafftrack_logout_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='staffLate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('todays_date', models.DateTimeField(blank=True)),
                ('late_diff', models.DateTimeField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]