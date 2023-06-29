import datetime
from hotel.models import Booking

def check_availability(room, check_in, check_out):
    booking_list = Booking.objects.filter(room=room, check_out__gte=datetime.datetime.now())
    for booking in booking_list:
        if booking.check_in <= check_out and booking.check_out >= check_in:
            return False
    return True