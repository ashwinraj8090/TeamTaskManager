
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_activitylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
