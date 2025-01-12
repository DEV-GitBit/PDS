# Generated by Django 5.0.7 on 2024-12-31 10:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_model',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=20)),
                ('admin_email', models.EmailField(max_length=50, unique=True, validators=[django.core.validators.EmailValidator(message='Enter a valid email address.')])),
                ('admin_password', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'admin_table',
            },
        ),
        migrations.CreateModel(
            name='FPS_model',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fps_id', models.AutoField(primary_key=True, serialize=False)),
                ('fps_name', models.CharField(max_length=20)),
                ('fps_email', models.EmailField(max_length=50, unique=True, validators=[django.core.validators.EmailValidator(message='Enter a valid email address.')])),
                ('fps_password', models.CharField(max_length=128)),
                ('fps_phone', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator('^\\d{10,13}$', message='Enter a valid phone number.')])),
                ('owner_image', models.ImageField(upload_to='fps_owners/')),
            ],
            options={
                'db_table': 'fps_table',
            },
        ),
        migrations.CreateModel(
            name='Ration_card',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('r_id', models.AutoField(primary_key=True, serialize=False)),
                ('beneficiary_card_no', models.CharField(default=str, max_length=15, unique=True)),
                ('ration_card_beneficiary_name', models.CharField(max_length=20)),
                ('b_ration_address', models.CharField(default=str, max_length=100)),
                ('b_ration_aadhaar', models.CharField(default=str, max_length=10)),
                ('b_ration_state', models.CharField(default=str, max_length=20)),
                ('b_ration_pincode', models.CharField(default=str, max_length=6)),
                ('b_ration_family_size', models.IntegerField(default=1)),
                ('b_ration_family', models.JSONField(default=list)),
            ],
            options={
                'db_table': 'ration_card_table',
            },
        ),
        migrations.CreateModel(
            name='Beneficiaries',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('beneficiary_id', models.AutoField(primary_key=True, serialize=False)),
                ('beneficiary_card_no', models.CharField(default=str, max_length=15, unique=True)),
                ('beneficiary_name', models.CharField(max_length=20)),
                ('beneficiary_email', models.EmailField(max_length=50, validators=[django.core.validators.EmailValidator(message='Enter a valid email address.')])),
                ('beneficiary_phone', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^\\d{10,13}$', message='Enter a valid phone number.')])),
                ('beneficiary_address', models.CharField(max_length=100)),
                ('beneficiary_aadhaar', models.CharField(max_length=10)),
                ('beneficiary_state', models.CharField(max_length=20)),
                ('beneficiary_pincode', models.CharField(max_length=6)),
                ('beneficiary_family_size', models.IntegerField()),
                ('beneficiary_family', models.JSONField()),
                ('beneficiary_card', models.CharField(choices=[('select', 'Select'), ('yellow', 'Yellow'), ('white', 'White'), ('saffron', 'Saffron'), ('green', 'Green')], default='select', max_length=20)),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaries', to='USERapp.ration_card')),
            ],
            options={
                'db_table': 'beneficiaries_table',
            },
        ),
    ]