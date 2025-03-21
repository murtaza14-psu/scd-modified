# Generated by Django 5.1.7 on 2025-03-20 11:46

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
        ('authentication', '0001_initial'),
        ('opportunities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('checked_in', 'Checked In'), ('completed', 'Completed'), ('no_show', 'No Show')], default='checked_in', max_length=20)),
                ('check_in_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('check_out_time', models.DateTimeField(blank=True, null=True)),
                ('hours_contributed', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='opportunities.opportunity')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='authentication.volunteerprofile')),
            ],
        ),
    ]
