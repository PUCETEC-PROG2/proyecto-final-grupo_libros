# Generated by Django 4.2 on 2024-08-16 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='condition',
            field=models.CharField(choices=[('Nuevo', 'Nuevo'), ('Mal estado', 'Mal estado'), ('Usado', 'Usado')], max_length=30),
        ),
    ]
