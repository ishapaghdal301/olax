# Generated by Django 4.1.7 on 2023-03-04 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_customer_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='password',
            new_name='password1',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(default=12, max_length=20),
            preserve_default=False,
        ),
    ]
