from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    !!! WRITTEN MANUALLY !!! To avoid circular dependency between customers and accounts migration scripts.
    Add the owner on the CustomerSpace model.
    """
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='CustomerSpace',
            name='owner',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
