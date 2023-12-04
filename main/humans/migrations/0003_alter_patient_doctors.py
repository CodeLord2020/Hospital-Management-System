# Generated by Django 4.2.3 on 2023-12-04 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humans', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='doctors',
            field=models.ManyToManyField(blank=True, related_name='patients_attending', to='humans.doctor'),
        ),
    ]
