# Generated by Django 5.0.2 on 2025-03-29 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_remove_category_image_url_remove_product_is_new_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='order_files/'),
        ),
    ]
