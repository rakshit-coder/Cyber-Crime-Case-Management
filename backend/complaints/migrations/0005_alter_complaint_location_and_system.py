# Generated migration for optimizing incident_location and affected_system fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0004_alter_complaint_affected_system_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='incident_location',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='affected_system',
            field=models.CharField(blank=True, max_length=30, null=True, help_text='e.g., Email, Bank Account, Social Media'),
        ),
    ]
