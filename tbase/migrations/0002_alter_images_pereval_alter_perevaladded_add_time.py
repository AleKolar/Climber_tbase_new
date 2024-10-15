# Generated by Django 5.0.4 on 2024-10-07 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='pereval',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tbase.perevaladded'),
        ),
        migrations.AlterField(
            model_name='perevaladded',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
