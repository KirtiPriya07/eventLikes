# Generated by Django 5.0.4 on 2024-04-14 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_event_timestamp_eventlike_event_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="parent",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="events.event",
            ),
        ),
    ]