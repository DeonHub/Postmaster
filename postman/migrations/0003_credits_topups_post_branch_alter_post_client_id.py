# Generated by Django 4.1.1 on 2022-10-18 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postman', '0002_post_client_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100, null=True)),
                ('service_type', models.CharField(max_length=100, null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('available_units', models.IntegerField(default=0, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopUps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100, null=True)),
                ('service_type', models.CharField(max_length=100, null=True)),
                ('branch', models.CharField(max_length=100, null=True)),
                ('amount_paid', models.IntegerField(default=0, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='branch',
            field=models.CharField(default='Main Branch', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='client_id',
            field=models.CharField(default='1', max_length=100, null=True),
        ),
    ]