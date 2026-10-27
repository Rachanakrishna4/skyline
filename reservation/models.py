from django.db import models
from django.contrib.auth.models import User

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)

    def save(self, *args, **kwargs):
        # Only set available_seats on creation (not on every update)
        if not self.pk or self.available_seats is None:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=1)  # ✅ Add this field
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    booking_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.flight:
            self.total_price = self.seats_booked * self.flight.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number}"
