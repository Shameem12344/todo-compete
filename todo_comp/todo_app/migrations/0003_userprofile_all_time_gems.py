# Generated by Django 5.0.7 on 2024-07-19 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo_app", "0002_shopitem_userprofile_daily_task_limit_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="all_time_gems",
            field=models.IntegerField(default=0),
        ),
    ]
