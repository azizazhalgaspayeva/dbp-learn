# Generated by Django 4.2 on 2023-04-17 11:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("developer", "Developer"),
                    ("manager", "Manager"),
                    ("admin", "Admin"),
                ],
                default="developer",
                max_length=255,
            ),
        ),
    ]
