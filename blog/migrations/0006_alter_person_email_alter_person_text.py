# Generated by Django 4.0.9 on 2023-02-14 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_person_gender_alter_person_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(default='123@qq.com', max_length=254, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='person',
            name='text',
            field=models.TextField(default='', help_text='随便写点', verbose_name='内容'),
        ),
    ]
