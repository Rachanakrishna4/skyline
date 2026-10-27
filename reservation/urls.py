from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all-flights/', views.all_flights, name='all_flights'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('bookings/', views.my_bookings, name='my_bookings'),

    # User Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Cancellation
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('cancel-seats/<int:booking_id>/', views.cancel_seats, name='cancel_seats'),
]
