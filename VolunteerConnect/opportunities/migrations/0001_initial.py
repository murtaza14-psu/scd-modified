# Generated by Django 5.1.7 on 2025-03-17 15:20

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=200)),
                ('date', models.DateTimeField()),
                ('required_skills', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('removed', 'Removed')], default='open', max_length=20)),
                ('content_status', models.CharField(choices=[('active', 'Active'), ('flagged', 'Flagged'), ('removed', 'Removed')], default='active', max_length=20)),
                ('moderation_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='authentication.ngoprofile')),
            ],
        ),
    ]
