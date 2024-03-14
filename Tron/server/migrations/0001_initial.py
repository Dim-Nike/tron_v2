# Generated by Django 5.0.3 on 2024-03-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('login', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('IDF', models.CharField(max_length=500)),
                ('tariff', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]