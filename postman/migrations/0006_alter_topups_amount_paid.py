# Generated by Django 4.1.1 on 2022-10-26 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postman', '0005_alter_servicetypes_unit_amount_ghs_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topups',
            name='amount_paid',
            field=models.FloatField(default=0, null=True),
        ),
    ]
