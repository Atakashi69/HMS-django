from django.contrib.auth import authenticate
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Room, Booking
from .permissions import AdminOrReadOnly, OwnerOrAdmin
from .serializers import RoomSerializer, BookingSerializer
from .filters import RoomFilter, BookingFilter


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data =request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RoomFilter

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AdminOrReadOnly]


class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [OwnerOrAdmin]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookingFilter

    # Автоматически ставит айди текущего пользователя при создании записи
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [OwnerOrAdmin]
