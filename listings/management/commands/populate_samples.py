# listings/management/commands/populate_samples.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from listings.models import (
    Hotel,
    Room,
    Restaurant,
    MenuItem,
    CarRentalAgency,
    Car,
    HotelImage,
    RoomImage,
    RestaurantImage,
    MenuItemImage,
    CarAgencyImage,
)
import random
from django.utils.text import slugify
import requests
from io import BytesIO
from django.core.files import File


class Command(BaseCommand):
    help = "Populate database with sample data"

    def get_random_image(self, category):
        # Using Lorem Picsum with specific categories from Unsplash
        image_categories = {
            "hotel": ["hotel", "resort", "building"],
            "room": ["room", "bedroom", "interior"],
            "restaurant": ["restaurant", "cafe", "dining"],
            "food": ["food", "dish", "meal"],
            "car": ["car", "vehicle", "automobile"],
        }

        width = 800
        height = 600

        # Random choice from category-specific keywords
        keyword = random.choice(image_categories[category])
        url = f"https://source.unsplash.com/random/{width}x{height}/?{keyword}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return ContentFile(
                    response.content, name=f"{category}_{random.randint(1, 1000)}.jpg"
                )
        except:
            # Fallback to Lorem Picsum if Unsplash fails
            picsum_url = f"https://picsum.photos/{width}/{height}"
            try:
                response = requests.get(picsum_url)
                if response.status_code == 200:
                    return ContentFile(
                        response.content,
                        name=f"{category}_{random.randint(1, 1000)}.jpg",
                    )
            except:
                return None
        return None

    def generate_lorem(self, words=30):
        lorem = """Lorem ipsum dolor sit amet consectetur adipiscing elit sed do 
        eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim 
        veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo 
        consequat Duis aute irure dolor in reprehenderit in voluptate velit esse 
        cillum dolore eu fugiat nulla pariatur""".split()
        return " ".join(random.sample(lorem, words))

    def create_hotels(self):
        hotel_names = [
            "Sunset Paradise",
            "Royal Plaza",
            "Ocean View",
            "Mountain Resort",
            "City Comfort",
            "Grand Hotel",
            "Palm Beach Resort",
            "Diamond Lodge",
            "Silver Springs",
            "Golden Gate Inn",
        ]

        for name in hotel_names:
            hotel = Hotel.objects.create(
                name=name,
                address=f"{random.randint(1, 999)} {random.choice(['Main', 'Beach', 'Mountain', 'Park'])} Street",
                description=self.generate_lorem(),
                rating=round(random.uniform(3.5, 5.0), 1),
                price_per_night=random.randint(100, 500),
                has_wifi=random.choice([True, False]),
                has_parking=random.choice([True, False]),
                has_swimming_pool=random.choice([True, False]),
                has_gym=random.choice([True, False]),
                has_restaurant=random.choice([True, False]),
                main_image="default_picture.png",
            )

            # Create additional hotel images
            for _ in range(3):
                HotelImage.objects.create(
                    hotel=hotel,
                    image="default_picture.png",
                    caption=f"{name} View {_+1}",
                )

            # Create 5 rooms for each hotel
            room_types = ["single", "double", "suite", "family", "deluxe"]
            for i in range(5):
                room = Room.objects.create(
                    hotel=hotel,
                    room_type=room_types[i],
                    room_number=f"{random.randint(1, 9)}0{i}",
                    floor=random.randint(1, 5),
                    capacity=random.randint(1, 6),
                    price_per_night=random.randint(80, 400),
                    size_sqm=random.randint(20, 100),
                    description=self.generate_lorem(20),
                    has_air_conditioning=random.choice([True, False]),
                    has_minibar=random.choice([True, False]),
                    has_tv=True,
                    image="default_picture.png",
                )

                # Create room images
                for _ in range(2):
                    RoomImage.objects.create(
                        room=room,
                        image="default_picture.png",
                        caption=f"Room {room.room_number} View {_+1}",
                    )

    def create_restaurants(self):
        restaurant_names = [
            "Taste of Italy",
            "Asian Fusion",
            "Mexican Fiesta",
            "French Bistro",
            "Seafood Harbor",
            "Steakhouse",
            "Vegan Delight",
            "Sushi Master",
            "Mediterranean Kitchen",
            "Indian Spices",
        ]

        categories = ["main", "appetizer", "dessert", "beverage", "salad"]

        for name in restaurant_names:
            restaurant = Restaurant.objects.create(
                name=name,
                address=f"{random.randint(1, 999)} {random.choice(['Food', 'Restaurant', 'Cuisine'])} Street",
                description=self.generate_lorem(),
                rating=round(random.uniform(3.5, 5.0), 1),
                price_range=random.randint(20, 100),
                has_family_tables=random.choice([True, False]),
                has_business_tables=random.choice([True, False]),
                has_private_tables=random.choice([True, False]),
                main_image="default_picture.png",
            )

            # Create restaurant images
            for _ in range(3):
                RestaurantImage.objects.create(
                    restaurant=restaurant,
                    image="default_picture.png",
                    caption=f"{name} Interior {_+1}",
                )

            # Create 5 menu items for each restaurant
            for i in range(5):
                menu_item = MenuItem.objects.create(
                    restaurant=restaurant,
                    name=f"{name} Special {i+1}",
                    category=categories[i],
                    description=self.generate_lorem(15),
                    price=random.randint(10, 50),
                    is_vegetarian=random.choice([True, False]),
                    spiciness_level=random.randint(0, 5),
                    preparation_time=random.randint(10, 45),
                    calories=random.randint(200, 1000),
                    image="default_picture.png",
                )

                # Create menu item images
                for _ in range(2):
                    MenuItemImage.objects.create(
                        menu_item=menu_item,
                        image="default_picture.png",
                        caption=f"{menu_item.name} View {_+1}",
                    )

    def create_car_agencies(self):
        agency_names = [
            "Speed Rentals",
            "Luxury Cars",
            "Budget Rides",
            "Premium Auto",
            "City Wheels",
            "Airport Cars",
            "Easy Drive",
            "Fast Track",
            "Road Masters",
            "Elite Motors",
        ]

        car_brands = [
            ("Toyota", ["Corolla", "Camry", "RAV4"]),
            ("Honda", ["Civic", "Accord", "CR-V"]),
            ("Ford", ["Focus", "Fusion", "Escape"]),
            ("BMW", ["3 Series", "5 Series", "X3"]),
            ("Mercedes", ["C-Class", "E-Class", "GLC"]),
        ]

        for name in agency_names:
            agency = CarRentalAgency.objects.create(
                name=name,
                address=f"{random.randint(1, 999)} {random.choice(['Auto', 'Car', 'Vehicle'])} Street",
                description=self.generate_lorem(),
                rating=round(random.uniform(3.5, 5.0), 1),
                has_24hr_service=random.choice([True, False]),
                has_driver_service=random.choice([True, False]),
                has_airport_pickup=random.choice([True, False]),
                main_image="default_picture.png",
            )

            # Create agency images
            for _ in range(3):
                CarAgencyImage.objects.create(
                    agency=agency,
                    image="default_picture.png",
                    caption=f"{name} Office {_+1}",
                )

            # Create 5 cars for each agency
            for i in range(5):
                brand, models = random.choice(car_brands)
                Car.objects.create(
                    agency=agency,
                    brand=brand,
                    model=random.choice(models),
                    year=random.randint(2018, 2024),
                    transmission=random.choice(["auto", "manual"]),
                    price_per_day=random.randint(50, 200),
                    is_available=random.choice([True, False]),
                    image="default_picture.png",
                )

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate database...")

        # Clear existing data
        Hotel.objects.all().delete()
        Restaurant.objects.all().delete()
        CarRentalAgency.objects.all().delete()

        # Create new data
        self.create_hotels()
        self.stdout.write(self.style.SUCCESS("Hotels created successfully!"))

        self.create_restaurants()
        self.stdout.write(self.style.SUCCESS("Restaurants created successfully!"))

        self.create_car_agencies()
        self.stdout.write(self.style.SUCCESS("Car agencies created successfully!"))

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated database with sample data and images!"
            )
        )
