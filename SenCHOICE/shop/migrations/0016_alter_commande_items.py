# Generated by Django 4.0.3 on 2022-11-22 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_rename_valider_cart_es_valider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='items',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
