# Generated by Django 2.0 on 2021-05-11 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0005_auto_20210511_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='order_id',
            field=models.CharField(default='', max_length=50),
        ),
    ]