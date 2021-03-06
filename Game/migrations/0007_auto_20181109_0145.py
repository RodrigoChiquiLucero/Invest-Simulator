# Generated by Django 2.1.2 on 2018-11-09 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0006_auto_20181108_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Asset'),
        ),
        migrations.AlterField(
            model_name='alarm',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Wallet'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Wallet'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.LoanOffer'),
        ),
        migrations.AlterField(
            model_name='loanoffer',
            name='lender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Wallet'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.Asset'),
        ),
    ]
