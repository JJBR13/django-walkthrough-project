# Generated by Django 3.2.17 on 2023-03-14 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderlineitem',
            old_name='quantitiy',
            new_name='quantity',
        ),
    ]
