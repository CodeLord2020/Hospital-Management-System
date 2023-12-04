# Generated by Django 4.2.3 on 2023-11-24 18:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0, 'Age must be greater than or equal to zero'), django.core.validators.MaxValueValidator(150, 'Age is unrealistic')])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('emergency_contact_name', models.CharField(max_length=100)),
                ('emergency_contact_phone', models.CharField(max_length=15)),
                ('blood_type', models.CharField(blank=True, max_length=5, null=True)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('pre_existing_conditions', models.TextField(blank=True, null=True)),
                ('doctors', models.ManyToManyField(blank=True, related_name='patients_attending', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]