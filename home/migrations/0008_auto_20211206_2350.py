# Generated by Django 3.2.7 on 2021-12-07 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='email',
        ),
        migrations.RemoveField(
            model_name='client',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='client',
            name='password',
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='home.client', verbose_name='cliente'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='schedule', to='home.service', verbose_name='serviço'),
        ),
    ]