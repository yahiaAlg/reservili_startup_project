# Generated by Django 5.1.6 on 2025-02-24 11:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_savedcard_card_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Main heading for the slide', max_length=200, verbose_name='Title')),
                ('subtitle', models.TextField(blank=True, help_text='Descriptive text below the title', max_length=500, verbose_name='Subtitle')),
                ('image', models.ImageField(help_text='Recommended size: 1920x1080px', upload_to='carousel/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])], verbose_name='Slide Image')),
                ('button_text', models.CharField(blank=True, help_text='Optional call-to-action button text', max_length=50, verbose_name='Button Text')),
                ('button_link', models.URLField(blank=True, help_text='URL for the call-to-action button', verbose_name='Button Link')),
                ('order', models.PositiveIntegerField(default=0, help_text='Order in which slides are displayed', verbose_name='Display Order')),
                ('is_active', models.BooleanField(default=True, help_text='Show/hide this slide', verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Carousel Slide',
                'verbose_name_plural': 'Carousel Slides',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
