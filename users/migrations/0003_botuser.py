# Generated by Django 5.1.1 on 2024-10-06 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(unique=True)),
                ('phone_number', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Bot User',
                'verbose_name_plural': 'Bot Users',
                'db_table': 'bot_user',
            },
        ),
    ]
