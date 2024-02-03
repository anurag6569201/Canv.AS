# Generated by Django 5.0 on 2024-02-03 15:46

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_rename_tags_product_tagsss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='This is a product', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='I am a good vendor', null=True),
        ),
    ]
