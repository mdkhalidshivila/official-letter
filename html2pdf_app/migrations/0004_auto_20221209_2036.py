# Generated by Django 3.2 on 2022-12-09 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('html2pdf_app', '0003_auto_20221209_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='barcode',
        ),
        migrations.RemoveField(
            model_name='reexp',
            name='barcode',
        ),
    ]
