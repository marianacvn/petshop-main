# Generated by Django 3.2.7 on 2021-12-08 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_client_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(verbose_name='preco'),
        ),
    ]
