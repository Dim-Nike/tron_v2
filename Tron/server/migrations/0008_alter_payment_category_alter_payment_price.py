# Generated by Django 4.1.3 on 2024-03-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_keyidentification_payment_user_identification_dialog_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='category',
            field=models.CharField(choices=[('purchase', 'Покупка'), ('update', 'Обновление'), ('purchase_bonuses', 'Оплата бонусами')], max_length=30, verbose_name='Категория операции'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Стоимость'),
        ),
    ]