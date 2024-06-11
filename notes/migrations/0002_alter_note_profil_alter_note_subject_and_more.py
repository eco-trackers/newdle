# Generated by Django 5.0.6 on 2024-06-10 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='profil',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='note',
            name='subject',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='note',
            name='valeur',
            field=models.DecimalField(decimal_places=3, max_digits=1000),
        ),
    ]
