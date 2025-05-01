from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, time, timedelta
from django.urls import reverse

from restaurant.models import Booking, Menu, Category, MenuItem

class BookingModelTests(TestCase):
    def test_string_representation(self):
        booking = Booking(
            first_name='Alice',
            reservation_date=timezone.now().date(),
            reservation_time=time(18, 0),
            party_size=2
        )
        self.assertEqual(str(booking), f"Alice on {booking.reservation_date} at {booking.reservation_time}")

    def test_validate_not_past_raises_for_past_date(self):
        past_date = timezone.now().date() - timedelta(days=1)
        booking = Booking(
            first_name='Bob',
            reservation_date=past_date,
            reservation_time=time(12, 0),
            party_size=1
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_clean_raises_for_past_time_today(self):
        today = timezone.now().date()
        past_time = (timezone.now() - timedelta(hours=1)).time()
        booking = Booking(
            first_name='Carol',
            reservation_date=today,
            reservation_time=past_time,
            party_size=3
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_get_absolute_url(self):
        booking = Booking.objects.create(
            first_name='Dave',
            reservation_date=timezone.now().date() + timedelta(days=1),
            reservation_time=time(20, 0),
            party_size=4
        )
        url = booking.get_absolute_url()
        expected = reverse('booking-detail', kwargs={'pk': booking.pk})
        self.assertEqual(url, expected)

class MenuModelTests(TestCase):
    def test_string_representation(self):
        menu = Menu(name='Brunch Specials')
        self.assertEqual(str(menu), 'Brunch Specials')

class CategoryModelTests(TestCase):
    def test_string_representation(self):
        category = Category(title='Desserts', slug='desserts')
        self.assertEqual(str(category), 'Desserts')

class MenuItemModelTests(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name='Dinner Menu')
        self.category = Category.objects.create(title='Entrees', slug='entrees')

    def test_string_representation(self):
        item = MenuItem(
            title='Steak',
            price=25.00,
            menu=self.menu,
            category=self.category
        )
        self.assertEqual(str(item), 'Steak')

    def test_clean_raises_for_nonpositive_price(self):
        item = MenuItem(
            title='Free Sample',
            price=0,
            menu=self.menu,
            category=self.category
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_get_absolute_url(self):
        item = MenuItem.objects.create(
            title='Pasta',
            price=12.50,
            menu=self.menu,
            category=self.category
        )
        url = item.get_absolute_url()
        expected = reverse('menuitem-detail', kwargs={'pk': item.pk})
        self.assertEqual(url, expected)
