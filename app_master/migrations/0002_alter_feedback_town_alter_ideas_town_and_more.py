# Generated by Django 4.1.10 on 2024-06-06 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_master", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="town",
            field=models.CharField(
                choices=[
                    ("Southbury", "Southbury"),
                    ("Middlebury", "Middlebury"),
                    ("Woodbury", "Woodbury"),
                ],
                default="Southbury",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="ideas",
            name="town",
            field=models.CharField(
                choices=[
                    ("Southbury", "Southbury"),
                    ("Middlebury", "Middlebury"),
                    ("Woodbury", "Woodbury"),
                ],
                default="Southbury",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="ideasummary",
            name="town",
            field=models.CharField(
                choices=[
                    ("Southbury", "Southbury"),
                    ("Middlebury", "Middlebury"),
                    ("Woodbury", "Woodbury"),
                ],
                default="Southbury",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="isummary",
            name="town",
            field=models.CharField(
                choices=[
                    ("Southbury", "Southbury"),
                    ("Middlebury", "Middlebury"),
                    ("Woodbury", "Woodbury"),
                ],
                default="Southbury",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="profaneideas",
            name="town",
            field=models.CharField(
                choices=[
                    ("Southbury", "Southbury"),
                    ("Middlebury", "Middlebury"),
                    ("Woodbury", "Woodbury"),
                ],
                default="Southbury",
                max_length=30,
            ),
        ),
    ]
