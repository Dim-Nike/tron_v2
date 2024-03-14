# Generated by Django 5.0.3 on 2024-03-14 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flesh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IDF', models.CharField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mess_ln', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='IDF',
        ),
        migrations.RemoveField(
            model_name='user',
            name='tariff',
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(default='', max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AddField(
            model_name='user',
            name='flesh',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='server.flesh'),
        ),
        migrations.AddField(
            model_name='flesh',
            name='tariff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.tariff'),
        ),
    ]