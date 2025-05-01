from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from datetime import time


def validate_not_past(value):
    if value < timezone.now().date():
        raise ValidationError("Reservation date cannot be in the past.")


class Booking(models.Model):
    """
    Model representing a restaurant booking.
    """
    first_name = models.CharField(max_length=200,help_text="Customer's first name",)
    reservation_date = models.DateField(validators=[validate_not_past],help_text="Date of the reservation (cannot be in the past)",)
    reservation_time = models.TimeField(default=time(12, 0),help_text="Time slot of the reservation",)
    party_size = models.PositiveSmallIntegerField(default=1,help_text="Number of guests",)

    class Meta:
        ordering = ['reservation_date', 'reservation_time']
        verbose_name_plural = 'Bookings'
        unique_together = ('reservation_date', 'reservation_time', 'first_name')

    def __str__(self):
        return f"{self.first_name} on {self.reservation_date} at {self.reservation_time}"

    def clean(self):
        super().clean()
        if self.reservation_date == timezone.now().date() and self.reservation_time < timezone.now().time():
            raise ValidationError({
                'reservation_time': 'Reservation time cannot be in the past.'
            })

    def get_absolute_url(self):
        return reverse('booking-detail', kwargs={'pk': self.pk})


class Menu(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,help_text="Optional description of the menu",)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.name
   
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE,related_name='items',)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='menu_items',)
    description = models.TextField(blank=True,help_text="Optional detailed description of the item",)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Menu items'
        unique_together = ('title', 'menu')

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.price <= 0:
            raise ValidationError({
                'price': 'Price must be a positive value.'
            })

    def get_absolute_url(self):
        return reverse('menuitem-detail', kwargs={'pk': self.pk})
