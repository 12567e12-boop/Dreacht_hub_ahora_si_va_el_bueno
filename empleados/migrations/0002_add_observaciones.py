# Generated manually to add observaciones field to Requisicion

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empleados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
