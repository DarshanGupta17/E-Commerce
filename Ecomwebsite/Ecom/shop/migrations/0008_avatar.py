# Generated by Django 4.2.3 on 2023-07-25 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_product_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imag1', models.ImageField(upload_to='media/avatar_imgs')),
                ('imag2', models.ImageField(upload_to='media/avatar_imgs')),
                ('imag3', models.ImageField(upload_to='media/avatar_imgs')),
                ('imag4', models.ImageField(upload_to='media/avatar_imgs')),
                ('imag5', models.ImageField(upload_to='media/avatar_imgs')),
                ('imag6', models.ImageField(upload_to='media/avatar_imgs')),
                ('imag7', models.ImageField(upload_to='media/avatar_imgs')),
                ('imag8', models.ImageField(upload_to='media/avatar_imgs')),
            ],
        ),
    ]
