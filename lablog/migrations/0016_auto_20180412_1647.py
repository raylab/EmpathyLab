# Generated by Django 2.0.4 on 2018-04-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lablog', '0015_auto_20180410_0112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='TENSControl',
        ),
        migrations.AlterField(
            model_name='record',
            name='EEG',
            field=models.FilePathField(match='.*\\.db$', path='/home/yoyo/srv/git/github.com/raylab/EmpathyLab/eeg/'),
        ),
    ]
