from django.contrib import admin
from .models import Flight, Booking

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'departure_time', 'arrival_time', 'total_seats', 'available_seats')
    search_fields = ('flight_number', 'origin', 'destination')
    list_filter = ('origin', 'destination', 'departure_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seats_booked', 'booking_time')
    search_fields = ('user__username', 'flight__flight_number')
    list_filter = ('flight__origin', 'flight__destination')
