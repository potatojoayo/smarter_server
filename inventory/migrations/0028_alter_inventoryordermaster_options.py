
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_auto_20221026_1626'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventoryordermaster',
            options={'ordering': ('-date_created',)},
        ),
    ]
