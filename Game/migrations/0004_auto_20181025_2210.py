# Generated by Django 2.1.2 on 2018-10-25 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0003_wallet_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='asset_price',
        ),
        migrations.AddField(
            model_name='transaction',
            name='asset_price_buy',
            field=models.FloatField(default=-1),
        ),
        migrations.AddField(
            model_name='transaction',
            name='asset_price_sell',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='quantity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='image',
            field=models.ImageField(default='profile_image/no_image.jpg', upload_to='profile_image'),
        ),
    ]