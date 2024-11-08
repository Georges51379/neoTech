# Generated by Django 5.1.2 on 2024-11-06 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_alter_transaction_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(max_length=10),
        ),
    ]
