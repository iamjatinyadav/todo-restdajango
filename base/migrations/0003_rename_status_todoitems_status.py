# Generated by Django 4.1.3 on 2022-12-20 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_todoitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todoitems',
            old_name='Status',
            new_name='status',
        ),
    ]
