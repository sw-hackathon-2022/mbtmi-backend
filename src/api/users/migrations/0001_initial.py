# Generated by Django 4.0.5 on 2022-06-22 19:29

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('mbti', models.CharField(choices=[('XXXX', 'XXXX'), ('ISTJ', 'ISTJ'), ('ISTP', 'ISTP'), ('ISFJ', 'ISFJ'), ('INTJ', 'INTJ'), ('ESTJ', 'ESTJ'), ('ISFP', 'ISFP'), ('INFJ', 'INFJ'), ('ESFJ', 'ESFJ'), ('ESFP', 'ESFP'), ('INFP', 'INFP'), ('INTP', 'INTP'), ('ESTP', 'ESTP'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'), ('ENFP', 'ENFP'), ('ENFJ', 'ENFJ')], default='XXXX', max_length=4)),
                ('email', models.EmailField(blank=True, max_length=30, null=True)),
                ('username', models.BigIntegerField(unique=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('about', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]