from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Flight, Booking
from .forms import UserRegistrationForm

def home(request):
    # Only show the first 6 flights on the homepage
    flights = Flight.objects.all()[:6]
    return render(request, 'home.html', {'flights': flights})

def all_flights(request):
    # Show all available flights
    flights = Flight.objects.all()
    return render(request, 'all_flights.html', {'flights': flights})

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, 'flight_detail.html', {'flight': flight})

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)

    if request.method == 'POST':
        seats_requested = int(request.POST.get('seats', 1))
        if seats_requested <= 0:
            messages.error(request, "Invalid number of seats requested.")
            return redirect('flight_detail', flight_id=flight_id)
        if seats_requested > flight.available_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('flight_detail', flight_id=flight_id)

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            seats_booked=seats_requested
        )
        # Reduce seats available
        flight.available_seats -= seats_requested
        flight.save()

        return render(request, 'confirm_booking.html', {'booking': booking})

    return render(request, 'book_flight.html', {'flight': flight})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_time')
    return render(request, 'my_bookings.html', {'bookings': bookings})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'confirm_booking.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    # Restore seats to the flight
    flight = booking.flight
    flight.available_seats += booking.seats_booked
    flight.save()
    
    booking.delete()
    messages.success(request, f"Booking for {flight.flight_number} has been fully cancelled.")
    return redirect('my_bookings')

@login_required
def cancel_seats(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    
    if request.method == 'POST':
        seats_to_remove = int(request.POST.get('seats_to_remove', 0))
        
        if seats_to_remove <= 0:
            messages.error(request, "Please enter a valid number of seats to cancel.")
        elif seats_to_remove >= booking.seats_booked:
            # If they cancel all seats, just use the full cancellation logic
            return cancel_booking(request, booking_id)
        else:
            # Reduce seats in booking
            booking.seats_booked -= seats_to_remove
            # Recalculate total price (Booking.save handles this automatically if I set it up right, 
            # but let's be explicit if needed. My model.save already handles total_price = seats * price)
            booking.save()
            
            # Restore seats to flight
            flight = booking.flight
            flight.available_seats += seats_to_remove
            flight.save()
            
            messages.success(request, f"Successfully cancelled {seats_to_remove} seat(s).")
            
    return redirect('my_bookings')

