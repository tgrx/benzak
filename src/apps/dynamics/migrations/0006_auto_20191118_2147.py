# Generated by Django 2.2.7 on 2019-11-18 21:47

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [("dynamics", "0005_auto_20191117_1620")]

    operations = [
        migrations.RemoveConstraint(model_name="pricehistory", name="singular_price"),
        migrations.AddConstraint(
            model_name="pricehistory",
            constraint=models.UniqueConstraint(
                fields=("at", "fuel", "currency"), name="singular_price"
            ),
        ),
    ]
