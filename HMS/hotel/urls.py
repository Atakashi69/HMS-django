from django.urls import path
from hotel import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bookings/', views.bookings_request, name='bookings'),
    path('book/<str:room_pk>/', views.book_request, name='book'),
    path('booking_cancel/<str:booking_pk>/', views.booking_cancel_request, name='booking_cancel'),
    path('signup/', views.signup_request, name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path('api/rooms', views.RoomListView.as_view(), name='room-list-create'),
]