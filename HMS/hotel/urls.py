from django.urls import path
from .views import home, signup_request, login_request, logout_request, bookings_request, book_request, \
    booking_cancel_request, RoomListCreateView

urlpatterns = [
    path('', home, name='home'),
    path('bookings/', bookings_request, name='bookings'),
    path('book/<str:room_pk>/', book_request, name='book'),
    path('booking_cancel/<str:booking_pk>/', booking_cancel_request, name='booking_cancel'),
    path('signup/', signup_request, name='signup'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),

    path('api/rooms', RoomListCreateView.as_view(), name='room-list-create')
]