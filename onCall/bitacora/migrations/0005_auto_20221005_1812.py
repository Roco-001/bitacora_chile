# Generated by Django 3.0 on 2022-10-05 23:12

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bitacora', '0004_auto_20221005_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incideciahijo',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Descripción'),
        ),
    ]