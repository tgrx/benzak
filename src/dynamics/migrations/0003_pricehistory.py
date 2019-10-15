# Generated by Django 2.2.6 on 2019-10-15 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynamics', '0002_auto_20191015_0012'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=4, max_digits=24)),
                ('at', models.DateField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dynamics.Currency')),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dynamics.Fuel')),
            ],
        ),
    ]
