from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'menuitems', views.MenuItemViewSet, basename='menuitem')
router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'), 


    #APIs
    path('restaurant/booking/', include(router.urls)),
]

