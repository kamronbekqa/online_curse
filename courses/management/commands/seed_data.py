from django.core.management.base import BaseCommand
from django.utils.text import slugify
from courses.models import Category, Course, Center
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial categories and courses'

    def handle(self, *args, **kwargs):
        # Create categories
        categories_data = [
            {'name': 'Dasturlash', 'slug': 'dasturlash'},
            {'name': 'Dizayn', 'slug': 'dizayn'},
            {'name': 'Marketing', 'slug': 'marketing'},
            {'name': 'Xorijiy tillar', 'slug': 'xorijiy-tillar'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {cat.name}"))

        # Create centers
        centers_data = [
            {
                'name': 'Proweb',
                'slug': 'proweb',
                'description': 'Proweb - Toshkentdagi eng yirik o\'quv markazlaridan biri. Biz zamonaviy IT kasblarni o\'rgatamiz.',
                'address': 'Toshkent sh., Chilonzor tumani',
                'phone': '+998 71 200 00 00',
                'website': 'https://proweb.uz'
            },
            {
                'name': 'Najot Ta\'lim',
                'slug': 'najot-talim',
                'description': 'Sifatli ta\'lim va zamonaviy muhit. Biz bilan kelajagingizni quring.',
                'address': 'Toshkent sh., Olmazor tumani',
                'phone': '+998 71 123 45 67',
                'website': 'https://najottalim.uz'
            },
        ]
        
        centers = {}
        for center_data in centers_data:
            center, created = Center.objects.get_or_create(
                slug=center_data['slug'],
                defaults={
                    'name': center_data['name'],
                    'description': center_data['description'],
                    'address': center_data['address'],
                    'phone': center_data['phone'],
                    'website': center_data['website']
                }
            )
            centers[center_data['slug']] = center
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created center: {center.name}"))

        # Create courses
        courses_data = [
            {
                'title': 'Python Full Stack',
                'description': 'Python dasturlash tili va Django frameworki orqali mukammal veb-saytlar yaratishni o\'rganing.',
                'price': 12000000,
                'duration_months': 12,
                'category': categories['dasturlash'],
                'center': centers['proweb'],
                'image': 'course_images/python.png',
                'is_popular': True
            },
            {
                'title': 'Frontend Development',
                'description': 'ReactJS va zamonaviy web texnologiyalar yordamida interaktiv interfeyslar yaratish.',
                'price': 9000000,
                'duration_months': 9,
                'category': categories['dasturlash'],
                'center': centers['najot-talim'],
                'image': 'course_images/frontend.png',
                'is_popular': True
            },
            {
                'title': 'Graphic Design',
                'description': 'Adobe Photoshop va Illustrator yordamida professional dizayner bo\'ling.',
                'price': 6000000,
                'duration_months': 6,
                'category': categories['dizayn'],
                'center': centers['proweb'],
                'image': 'course_images/design.png',
                'is_popular': True
            },
            {
                'title': 'SMM & Digital Marketing',
                'description': 'Ijtimoiy tarmoqlar orqali brendni rivojlantirish va sotuvlarni oshirish.',
                'price': 4500000,
                'duration_months': 4,
                'category': categories['marketing'],
                'center': centers['najot-talim'],
                'is_popular': False
            },
            {
                'title': 'IELTS Intensive',
                'description': 'Ingliz tili darajangizni qisqa vaqt ichida IELTS 7+ ga olib chiqing.',
                'price': 3000000,
                'duration_months': 3,
                'category': categories['xorijiy-tillar'],
                'center': centers['najot-talim'],
                'image': 'course_images/ielts.png',
                'is_popular': False
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.update_or_create(
                slug=slugify(course_data['title']),
                defaults={
                    'title': course_data['title'],
                    'description': course_data['description'],
                    'price': course_data['price'],
                    'duration_months': course_data['duration_months'],
                    'category': course_data['category'],
                    'center': course_data['center'],
                    'image': course_data.get('image'),
                    'is_popular': course_data['is_popular']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created course: {course.title}"))

        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS("Created superuser: admin (pass: admin123)"))

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
