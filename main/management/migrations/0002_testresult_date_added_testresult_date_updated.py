# Generated by Django 4.2.3 on 2023-11-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='testresult',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]