# Generated by Django 5.1.6 on 2025-02-12 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_carrentalagency_slug_hotel_slug_restaurant_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrentalagency',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5, max_digits=2, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5, max_digits=2, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5, max_digits=2, verbose_name='Rating'),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Item Name')),
                ('category', models.CharField(choices=[('main', 'Main Dish'), ('appetizer', 'Appetizer'), ('dessert', 'Dessert'), ('beverage', 'Beverage'), ('salad', 'Salad')], max_length=20, verbose_name='Category')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('is_available', models.BooleanField(default=True, verbose_name='Available')),
                ('is_vegetarian', models.BooleanField(default=False, verbose_name='Vegetarian')),
                ('is_vegan', models.BooleanField(default=False, verbose_name='Vegan')),
                ('is_gluten_free', models.BooleanField(default=False, verbose_name='Gluten Free')),
                ('spiciness_level', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0, verbose_name='Spiciness Level')),
                ('preparation_time', models.IntegerField(default=15, verbose_name='Preparation Time (minutes)')),
                ('calories', models.IntegerField(blank=True, null=True, verbose_name='Calories')),
                ('image', models.ImageField(blank=True, null=True, upload_to='menu_items/', verbose_name='Image')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='listings.restaurant')),
            ],
            options={
                'verbose_name': 'Menu Item',
                'verbose_name_plural': 'Menu Items',
            },
        ),
        migrations.CreateModel(
            name='MenuItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='menu_items/gallery/', verbose_name='Image')),
                ('caption', models.CharField(blank=True, max_length=255, verbose_name='Caption')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='listings.menuitem')),
            ],
            options={
                'verbose_name': 'Menu Item Image',
                'verbose_name_plural': 'Menu Item Images',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('suite', 'Suite'), ('family', 'Family'), ('deluxe', 'Deluxe')], max_length=20, verbose_name='Room Type')),
                ('room_number', models.CharField(max_length=10, verbose_name='Room Number')),
                ('floor', models.IntegerField(verbose_name='Floor')),
                ('capacity', models.IntegerField(verbose_name='Capacity')),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price per Night')),
                ('size_sqm', models.IntegerField(verbose_name='Size (m²)')),
                ('is_available', models.BooleanField(default=True, verbose_name='Available')),
                ('has_air_conditioning', models.BooleanField(default=False, verbose_name='Air Conditioning')),
                ('has_heating', models.BooleanField(default=False, verbose_name='Heating')),
                ('has_minibar', models.BooleanField(default=False, verbose_name='Minibar')),
                ('has_tv', models.BooleanField(default=False, verbose_name='TV')),
                ('has_safe', models.BooleanField(default=False, verbose_name='Safe')),
                ('has_private_bathroom', models.BooleanField(default=True, verbose_name='Private Bathroom')),
                ('has_sea_view', models.BooleanField(default=False, verbose_name='Sea View')),
                ('has_balcony', models.BooleanField(default=False, verbose_name='Balcony')),
                ('image', models.ImageField(blank=True, null=True, upload_to='rooms/', verbose_name='Image')),
                ('description', models.TextField(verbose_name='Description')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='listings.hotel')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
                'unique_together': {('hotel', 'room_number')},
            },
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='rooms/gallery/', verbose_name='Image')),
                ('caption', models.CharField(blank=True, max_length=255, verbose_name='Caption')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='listings.room')),
            ],
            options={
                'verbose_name': 'Room Image',
                'verbose_name_plural': 'Room Images',
            },
        ),
    ]
