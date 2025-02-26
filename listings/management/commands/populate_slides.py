# your_app/management/commands/fill_carousel.py

from django.core.management.base import BaseCommand
from pages.models import CarouselSlide


class Command(BaseCommand):
    help = "Fill CarouselSlide data with three slides."

    def handle(self, *args, **options):
        # شريحة 1: القصبة في الجزائر العاصمة
        slide1, created = CarouselSlide.objects.get_or_create(
            title="القصبة في الجزائر العاصمة",
            defaults={
                "subtitle": "اكتشف روعة الهندسة المعمارية والتراث العتيق في قلب العاصمة.",
                "image": "https://images.unsplash.com/photo-1569288063578-99417757ee37?w=1200&auto=format&fit=crop&q=80",  # Placeholder image
                "button_text": "اقرأ المزيد",
                "button_link": "https://en.wikipedia.org/wiki/Casbah_of_Algiers",
                "order": 1,
                "is_active": True,
            },
        )

        # شريحة 2: جسور قسنطينة المعلقة
        slide2, created = CarouselSlide.objects.get_or_create(
            title="جسور قسنطينة المعلقة",
            defaults={
                "subtitle": "تجربة لا تُنسى بين الطبيعة الخلابة والهندسة المعمارية الرائعة.",
                "image": "https://images.unsplash.com/photo-1555001802-c8495545cce2?w=1200&auto=format&fit=crop&q=80",  # Placeholder image
                "button_text": "استكشف المزيد",
                "button_link": "https://en.wikipedia.org/wiki/Constantine,_Algeria",
                "order": 2,
                "is_active": True,
            },
        )

        # شريحة 3: الآثار الرومانية في تيبازة
        slide3, created = CarouselSlide.objects.get_or_create(
            title="الآثار الرومانية في تيبازة",
            defaults={
                "subtitle": "استمتع بجولة عبر التاريخ مع أروع الآثار الرومانية في تيبازة.",
                "image": "https://images.unsplash.com/photo-1542361345-89e58247f2d5?w=1200&auto=format&fit=crop&q=80",  # Placeholder image
                "button_text": "تعرف على المزيد",
                "button_link": "https://en.wikipedia.org/wiki/Tipasa",
                "order": 3,
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Carousel Slides added successfully."))
