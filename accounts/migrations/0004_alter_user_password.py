# Generated by Django 4.0 on 2023-09-14 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_cls_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=258),
        ),
    ]
