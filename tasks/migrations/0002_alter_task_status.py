
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('SUBMITTED', 'Submitted for Review'), ('COMPLETED', 'Completed')], default='PENDING', max_length=20),
        ),
    ]
