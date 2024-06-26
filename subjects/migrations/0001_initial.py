# Generated by Django 4.1 on 2024-06-04 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("profil", "0001_initial"),
        ("group", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UE",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("semester", models.CharField(max_length=2)),
                ("coef", models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("coef", models.CharField(max_length=3)),
                ("prof", models.ManyToManyField(to="profil.profil")),
                ("student_group", models.ManyToManyField(to="group.group")),
                ("ue", models.ManyToManyField(to="subjects.ue")),
            ],
        ),
    ]
