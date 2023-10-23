# Generated by Django 4.2 on 2023-10-23 10:21

from django.db import migrations, models
import main.services.storage_backends


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_user_date_of_birth_user_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar_picture",
            field=models.ImageField(
                null=True,
                storage=main.services.storage_backends.public_storage,
                upload_to="",
            ),
        ),
    ]
