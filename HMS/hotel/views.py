from rest_framework import generics, viewsets
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, RoomFilterForm, BookingForm
from .models import Room, Booking
from .booking_functions.availability import check_availability
from .serializers import RoomSerializer


def home(request):
    template_name = 'home.html'
    form = RoomFilterForm(request.GET or None)
    rooms = Room.objects.all()

    if form.is_valid():
        min_price = form.cleaned_data['min_price']
        max_price = form.cleaned_data['max_price']
        capacity = form.cleaned_data['capacity']
        check_in = form.cleaned_data['check_in']
        check_out = form.cleaned_data['check_out']

        if min_price:
            rooms = rooms.filter(price__gte=min_price)
        if max_price:
            rooms = rooms.filter(price__lte=max_price)
        if capacity:
            rooms = rooms.filter(capacity=capacity)
        if check_in and check_out:
            for room in rooms:
                if not check_availability(room, check_in, check_out):
                    rooms = rooms.exclude(pk=room.pk)

    return render(request, template_name, {'filter_form':form, 'rooms':rooms})

def bookings_request(request):
    template_name = 'bookings.html'
    if not request.user.is_authenticated:
        messages.error(request, 'Вы не авторизованы')
        return redirect('login')

    bookings = Booking.objects.filter(user=request.user)
    return render(request, template_name, {'bookings':bookings})

def book_request(request, room_pk):
    template_name = 'book.html'
    if not request.user.is_authenticated:
        messages.error(request, 'Вы не авторизованы')
        return redirect('login')

    room = get_object_or_404(Room, pk=room_pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.check_in = form.cleaned_data['check_in']
            booking.check_out = form.cleaned_data['check_out']

            if not check_availability(room, form.cleaned_data['check_in'], form.cleaned_data['check_out']):
                messages.error(request, 'Комната уже забронирована на данный промежуток времени!')
                return render(request, template_name, {'booking_form':form})

            booking.save()
            messages.success(request, 'Вы успешно забронировали комнату!')
            return redirect('bookings')
        else:
            messages.error(request, 'Одно из полей заполнено неверно!')
    else:
        form = BookingForm()
    return render(request, template_name, {'booking_form':form, 'room': room})


def booking_cancel_request(request, booking_pk):
    booking = get_object_or_404(Booking, id=booking_pk)
    booking.delete()
    messages.success(request, 'Бронь успешно отменена')
    return redirect('bookings')


def signup_request(request):
    template_name = 'signup.html'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
        else:
            messages.error(request, 'Одно из полей заполнено неверно!')
    else:
        form = SignUpForm()
    return render(request, template_name, {'signup_form':form})

def login_request(request):
    template_name = 'login.html'
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже вошли')
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Добро пожаловать, {username}')
                return redirect('home')
            else:
                messages.error(request, 'Неверный никнейм или пароль!')
        else:
            messages.error(request, 'Неверный никнейм или пароль!')
    else:
        form = AuthenticationForm()
    return render(request, template_name, {'login_form':form})

def logout_request(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли!')
    return redirect('home')

class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        number = self.request.query_params.get('number', None)
        capacity = self.request.query_params.get('capacity', None)
        if number is not None:
            queryset = queryset.filter(number=number)
        if capacity is not None:
            queryset = queryset.filter(capacity=capacity)
        return queryset
