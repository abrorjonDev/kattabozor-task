# Generated by Django 4.2.4 on 2023-08-31 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='_id',
            field=models.IntegerField(db_index=True, default=1, verbose_name='Kattabozor server ID'),
            preserve_default=False,
        ),
    ]