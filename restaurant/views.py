# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking, MenuItem, Booking
from .serializers import MenuItemSerializer, UserSerializer, BookingItemSerializer
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets, permissions
from django.contrib.auth.models import User




#APIs

class BookingViewSet(viewsets.ModelViewSet):
   queryset = Booking.objects.all()
   serializer_class = BookingItemSerializer
   permission_classes = [permissions.IsAuthenticated] 


class MenuItemViewSet(viewsets.ModelViewSet):
   queryset = MenuItem.objects.all()
   serializer_class = MenuItemSerializer
   permission_classes = [permissions.IsAuthenticated] 

class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = [permissions.IsAuthenticated] 



class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


# Templates.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    # Handle POST to create a booking
    if request.method == "POST":
        data = json.load(request)
        exists = Booking.objects.filter(
            reservation_date=data['reservation_date']
        ).filter(
            reservation_slot=data['reservation_slot']
        ).exists()
        if not exists:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse(
                "{'error':1}",
                content_type='application/json'
            )
    # Handle GET to list bookings for a date
    date = request.GET.get('date', datetime.today().date())
    bookings_qs = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings_qs)
    return HttpResponse(
        booking_json,
        content_type='application/json'
    )