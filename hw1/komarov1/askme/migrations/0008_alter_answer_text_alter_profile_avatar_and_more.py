# Generated by Django 4.2 on 2023-04-24 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0007_likeanswer_estimation_likequestion_estimation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='static/img/avatar2.png', upload_to='static/img'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
