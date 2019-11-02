from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("about", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(
            name="technology",
            options={"ordering": ["name"], "verbose_name_plural": "technologies"},
        )
    ]
