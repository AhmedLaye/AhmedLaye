# Generated by Django 4.0.3 on 2022-11-22 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_commande_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='total',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
