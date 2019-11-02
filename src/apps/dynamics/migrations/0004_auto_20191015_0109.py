from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("dynamics", "0003_pricehistory")]

    operations = [
        migrations.AlterModelOptions(
            name="pricehistory",
            options={
                "ordering": ["-at", "fuel", "currency"],
                "verbose_name_plural": "Price History",
            },
        )
    ]
