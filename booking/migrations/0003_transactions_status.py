# Generated by Django 2.1.1 on 2018-10-15 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20181015_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]