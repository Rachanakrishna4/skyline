import os
import django
from datetime import timedelta
from django.utils import timezone
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_mgmt.settings')
django.setup()

from reservation.models import Flight

locations = [
    "New Delhi (DEL)", "Mumbai (BOM)", "Bengaluru (BLR)", 
    "Chennai (MAA)", "Kolkata (CCU)", "Hyderabad (HYD)", 
    "Ahmedabad (AMD)", "Pune (PNQ)", "Jaipur (JAI)", 
    "Lucknow (LKO)", "Kochi (COK)", "Goa (GOX)", 
    "Guwahati (GAU)", "Patna (PAT)", "Bhubaneswar (BBI)"
]

airlines = ["6E", "AI", "SG", "UK", "I5", "QP"]

print("Clearing existing flights...")
Flight.objects.all().delete()

print("Seeding new flights...")
now = timezone.now()

for _ in range(30):
    origin = random.choice(locations)
    dest = random.choice(locations)
    while origin == dest:
        dest = random.choice(locations)
    
    airline = random.choice(airlines)
    number = f"{airline}{random.randint(100, 999)}"
    
    # Random departure between 1 day and 30 days from now
    dep_time = now + timedelta(days=random.randint(1, 30), hours=random.randint(0, 23), minutes=random.choice([0, 15, 30, 45]))
    # Random flight duration between 2 and 15 hours
    duration = timedelta(hours=random.randint(2, 15), minutes=random.choice([0, 30]))
    arr_time = dep_time + duration
    
    seats = random.randint(50, 300)
    price = round(random.uniform(2500.0, 15000.0), -2)
    
    Flight.objects.create(
        flight_number=number,
        origin=origin,
        destination=dest,
        departure_time=dep_time,
        arrival_time=arr_time,
        total_seats=seats,
        available_seats=seats,
        price=price
    )

print(f"Successfully seeded {Flight.objects.count()} flights.")
