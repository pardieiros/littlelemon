from django.forms import ModelForm, TextInput, DateInput, Select, NumberInput
from .models import Booking


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
        widgets = {
            'first_name': TextInput(attrs={'id': 'first_name'}),
            'reservation_date': DateInput(attrs={'id': 'reservation_date', 'type': 'date'}),
            'reservation_time': Select(attrs={'id': 'reservation_slot'}),
            'party_size': NumberInput(attrs={'id': 'party_size', 'min': 1}),
        }