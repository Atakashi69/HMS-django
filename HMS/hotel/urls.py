from django.urls import path, include
from hotel import views

urlpatterns = [
    path('api/register/', views.RegistrationView.as_view(), name='user-registration'),
    path('api/login/', views.LoginView.as_view(), name='user-login'),
    path('api/rooms/', views.RoomListView.as_view(), name='room-list'),
    path('api/rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('api/bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('api/bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
]