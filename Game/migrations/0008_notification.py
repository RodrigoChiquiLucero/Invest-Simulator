# Generated by Django 2.1.2 on 2018-11-11 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0007_auto_20181109_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_short', models.TextField(default='')),
                ('message_large', models.TextField(default='')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Wallet')),
            ],
        ),
    ]