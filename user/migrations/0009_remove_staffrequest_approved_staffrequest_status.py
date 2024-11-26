# Generated by Django 4.1.5 on 2024-11-25 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_staffvacation_vacationtime_staffrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffrequest',
            name='approved',
        ),
        migrations.AddField(
            model_name='staffrequest',
            name='status',
            field=models.CharField(choices=[('Bekliyor', 'Bekliyor'), ('Onaylandı', 'Onaylandı'), ('Reddedildi', 'Reddedildi')], default='Bekliyor', max_length=10),
        ),
    ]