# listings/management/commands/populate_samples.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from listings.models import *
from accounts.models import *
from payments.models import *
from django.contrib.contenttypes.models import ContentType
import random
import requests


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

    def create_users(self, num_users=5):
        User = get_user_model()
        users = []
        for i in range(num_users):
            username = f"user{i+1}"
            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="password123",
            )
            users.append(user)
        return users

    def create_payment_methods(self):
        payment_methods = [
            "CIB",
            "Satim",
            "Cash Payment",
            "Mobile Payment",
        ]

        for name in payment_methods:
            PaymentMethod.objects.create(
                name=name, is_active=True, is_default=(name == "CIB")
            )

    def create_saved_cards(self, users):
        payment_methods = PaymentMethod.objects.filter(name__in=["CIB", "Satim"])

        for user in users:
            for _ in range(random.randint(1, 2)):
                card_number = str(random.randint(1000000000000000, 9999999999999999))
                SavedCard.objects.create(
                    user=user,
                    card_type=random.choice(payment_methods),
                    card_holder=f"{user.username.title()} User",
                    last_four=card_number[-4:],
                    encrypted_card_number=hashlib.sha256(
                        card_number.encode()
                    ).hexdigest(),
                    expiry_month=str(random.randint(1, 12)).zfill(2),
                    expiry_year=str(random.randint(23, 28)),
                    is_default=False,
                )

    def create_hotel_payment(self, reservation, user):
        saved_card = SavedCard.objects.filter(user=user).first()

        Payment.objects.create(
            user=user,
            amount=reservation.total_price,
            saved_card=saved_card,
            status=random.choice(["pending", "completed"]),
            transaction_id=f"HTRANS{random.randint(10000, 99999)}",
            content_type=ContentType.objects.get_for_model(HotelReservation),
            object_id=reservation.id,
        )

    def create_restaurant_payment(self, reservation, user):
        saved_card = SavedCard.objects.filter(user=user).first()

        Payment.objects.create(
            user=user,
            amount=reservation.total_price,
            saved_card=saved_card,
            status=random.choice(["pending", "completed"]),
            transaction_id=f"RTRANS{random.randint(10000, 99999)}",
            content_type=ContentType.objects.get_for_model(RestaurantReservation),
            object_id=reservation.id,
        )

    def create_car_payment(self, reservation, user):
        saved_card = SavedCard.objects.filter(user=user).first()

        Payment.objects.create(
            user=user,
            amount=reservation.total_price,
            saved_card=saved_card,
            status=random.choice(["pending", "completed"]),
            transaction_id=f"CTRANS{random.randint(10000, 99999)}",
            content_type=ContentType.objects.get_for_model(CarReservation),
            object_id=reservation.id,
        )

    def create_hotel_reservations(self, users):
        hotels = Hotel.objects.all()

        for user in users:
            for _ in range(random.randint(1, 3)):
                hotel = random.choice(hotels)
                check_in = timezone.now().date() + timedelta(days=random.randint(1, 30))
                check_out = check_in + timedelta(days=random.randint(1, 7))

                reservation = HotelReservation.objects.create(
                    user=user,
                    hotel=hotel,
                    check_in=check_in,
                    check_out=check_out,
                    number_of_guests=random.randint(1, 4),
                    total_price=random.randint(200, 1000),
                    status=random.choice(["pending", "confirmed", "completed"]),
                    has_swimming_pool=random.choice([True, False]),
                    has_gym=random.choice([True, False]),
                    has_outdoor_area=random.choice([True, False]),
                )

                # Add rooms to reservation
                available_rooms = Room.objects.filter(hotel=hotel)
                for room in random.sample(
                    list(available_rooms), k=random.randint(1, 2)
                ):
                    ReservationRoom.objects.create(
                        reservation=reservation,
                        room=room,
                    )

                # Create payment for reservation
                self.create_hotel_payment(reservation, user)

    def create_restaurant_reservations(self, users):
        restaurants = Restaurant.objects.all()

        for user in users:
            for _ in range(random.randint(1, 3)):
                restaurant = random.choice(restaurants)
                reservation_date = timezone.now().date() + timedelta(
                    days=random.randint(1, 14)
                )

                reservation = RestaurantReservation.objects.create(
                    user=user,
                    restaurant=restaurant,
                    reservation_date=reservation_date,
                    reservation_time=f"{random.randint(11, 21)}:00",
                    table_type=random.choice(["family", "business", "private"]),
                    total_price=random.randint(50, 200),
                    status=random.choice(["pending", "confirmed", "completed"]),
                )

                # Add menu items to reservation
                menu_items = MenuItem.objects.filter(restaurant=restaurant)
                for item in random.sample(list(menu_items), k=random.randint(1, 4)):
                    ReservationMenuItem.objects.create(
                        reservation=reservation,
                        menu_item=item,
                    )

                # Create payment for reservation
                self.create_restaurant_payment(reservation, user)

    def create_car_reservations(self, users):
        agencies = CarRentalAgency.objects.all()

        for user in users:
            for _ in range(random.randint(1, 3)):
                agency = random.choice(agencies)
                start_date = timezone.now().date() + timedelta(
                    days=random.randint(1, 30)
                )
                end_date = start_date + timedelta(days=random.randint(1, 7))

                reservation = CarReservation.objects.create(
                    user=user,
                    agency=agency,
                    start_date=start_date,
                    end_date=end_date,
                    car_brand="Sample Brand",
                    car_type=random.choice(["economy", "luxury", "suv"]),
                    total_price=random.randint(100, 500),
                    status=random.choice(["pending", "confirmed", "completed"]),
                    with_driver=random.choice([True, False]),
                    insurance_type=random.choice(["basic", "full"]),
                )

                # Add cars to reservation
                available_cars = Car.objects.filter(agency=agency)
                for car in random.sample(list(available_cars), k=random.randint(1, 2)):
                    ReservationCar.objects.create(
                        reservation=reservation,
                        car=car,
                    )

                # Create payment for reservation
                self.create_car_payment(reservation, user)

    def handle(self, *args, **options):
        self.stdout.write("Starting to populate database...")

        # Clear existing data
        Hotel.objects.all().delete()
        Restaurant.objects.all().delete()
        CarRentalAgency.objects.all().delete()
        PaymentMethod.objects.all().delete()
        User = get_user_model()
        User.objects.exclude(is_superuser=True).delete()

        # Create basic data
        self.create_hotels()
        self.stdout.write(self.style.SUCCESS("Hotels created successfully!"))

        self.create_restaurants()
        self.stdout.write(self.style.SUCCESS("Restaurants created successfully!"))

        self.create_car_agencies()
        self.stdout.write(self.style.SUCCESS("Car agencies created successfully!"))

        # Create users and payment-related data
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS("Users created successfully!"))

        self.create_payment_methods()
        self.stdout.write(self.style.SUCCESS("Payment methods created successfully!"))

        self.create_saved_cards(users)
        self.stdout.write(self.style.SUCCESS("Saved cards created successfully!"))

        # Create reservations
        self.create_hotel_reservations(users)
        self.stdout.write(
            self.style.SUCCESS("Hotel reservations created successfully!")
        )

        self.create_restaurant_reservations(users)
        self.stdout.write(
            self.style.SUCCESS("Restaurant reservations created successfully!")
        )

        self.create_car_reservations(users)
        self.stdout.write(self.style.SUCCESS("Car reservations created successfully!"))

        self.stdout.write(
            self.style.SUCCESS("Successfully populated database with all sample data!")
        )
