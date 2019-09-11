# Generated by Django 2.2.4 on 2019-09-04 07:35

import accounts.validators
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applicants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sei_number', models.CharField(error_messages={'unique': 'A certification with that SEI process number already exists.'}, help_text='Required.', max_length=20, unique=True, validators=[accounts.validators.NumericValidator()], verbose_name='SEI process number')),
                ('sei_protocol', models.CharField(help_text='Required.', max_length=20, verbose_name='SEI process protocol')),
                ('domain', models.CharField(help_text='Required.', max_length=100, verbose_name='domain')),
                ('sei_nature', models.CharField(choices=[('PB', 'public'), ('PV', 'private')], default='PV', max_length=2, verbose_name='SEI process nature')),
                ('request_date', models.DateTimeField(verbose_name='request date')),
                ('refusal_date', models.DateTimeField(verbose_name='refusal date')),
                ('code', models.CharField(help_text='Required.', max_length=20, validators=[accounts.validators.NumericValidator()], verbose_name='code')),
                ('grant_date', models.DateTimeField(verbose_name='grant date')),
                ('renewal_date', models.DateTimeField(verbose_name='renewal date')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this certification should be treated as active. Unselect this instead of deleting certifications.', verbose_name='active')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicants.Applicant')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(error_messages={'unique': 'A page with that URL already exists.'}, help_text='Required.', max_length=200, unique=True, verbose_name='URL')),
                ('is_homepage', models.BooleanField(default=False, verbose_name='homepage')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this page should be treated as active. Unselect this instead of deleting pages.', verbose_name='active')),
                ('certification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certifications.Certification')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_found', models.BooleanField(default=True, verbose_name='page found')),
                ('grade', models.IntegerField(verbose_name='evaluation grade')),
                ('creation_date_time', models.DateTimeField(default=datetime.datetime(2019, 9, 4, 4, 35, 28, 434687), verbose_name='creation date/time')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certifications.Page')),
            ],
        ),
    ]