# Generated by Django 5.0.7 on 2024-07-26 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Circuitrecommender', '0003_rename_dietaryrestrictions_tourism_dietaryrestrictions'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourism',
            name='Country',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
