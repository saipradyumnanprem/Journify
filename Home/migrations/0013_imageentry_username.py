# Generated by Django 4.2.7 on 2024-05-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Home", "0012_alter_imageentry_journal_counter"),
    ]

    operations = [
        migrations.AddField(
            model_name="imageentry",
            name="username",
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
