# Generated by Django 5.0.6 on 2024-06-11 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_note_profil_alter_note_subject_and_more'),
        ('profil', '0001_initial'),
        ('subjects', '0002_remove_subject_ue_subject_ue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='profil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profil.profil'),
        ),
        migrations.AlterField(
            model_name='note',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.subject'),
        ),
    ]
