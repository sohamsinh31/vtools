# Generated by Django 4.0.5 on 2022-07-17 07:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=122),
            preserve_default=False,
        ),
    ]
