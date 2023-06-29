from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput
from django.utils import timezone, dateformat

from hotel.models import Booking


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']

    check_in = forms.DateField(label='Дата заезда',
                               required=True,
                               widget=DateInput(
                                   attrs={'type': 'date', 'min': f'{dateformat.format(timezone.now(), "Y-m-d")}',
                                          'value': f'{dateformat.format(timezone.now(), "Y-m-d")}'}))
    check_out = forms.DateField(label='Дата выезда',
                                required=True,
                                widget=DateInput(attrs={'type': 'date'}))

    def clean_check_in(self):
        check_in = self.cleaned_data['check_in']
        if check_in and check_in < timezone.now().date():
            raise forms.ValidationError('Дата заезда не может быть раньше текущей даты')
        return check_in

    def clean_check_out(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data['check_out']
        if check_in and check_out and check_out < check_in:
            raise forms.ValidationError('Дата выезда не может быть раньше даты заезда')
        return check_out


class RoomFilterForm(forms.Form):
    min_price = forms.DecimalField(label='Минимальная цена',
                                   required=False,
                                   widget=forms.NumberInput(attrs={'type': 'range', 'step': '100', 'min': '1000', 'max': '10000', 'value': '1000'}))
    max_price = forms.DecimalField(label='Максимальная цена',
                                   required=False,
                                   widget=forms.NumberInput(attrs={'type': 'range', 'step': '100', 'min': '1000', 'max': '10000', 'value': '10000'}))
    capacity = forms.IntegerField(label='Количество мест',
                                  required=False)
    check_in = forms.DateField(label='Дата заезда',
                                   required=False,
                                   widget=DateInput(attrs={'type': 'date', 'min': f'{dateformat.format(timezone.now(), "Y-m-d")}', 'value': f'{dateformat.format(timezone.now(), "Y-m-d")}'}))
    check_out = forms.DateField(label='Дата выезда',
                                   required=False,
                                   widget=DateInput(attrs={'type': 'date'}))

    def clean_check_in(self):
        check_in = self.cleaned_data['check_in']
        if check_in and check_in < timezone.now().date():
            raise forms.ValidationError('Дата заезда не может быть раньше текущей даты')
        return check_in

    def clean_check_out(self):
        check_in = self.cleaned_data.get('check_in')
        check_out = self.cleaned_data['check_out']
        if check_in and check_out and check_out < check_in:
            raise forms.ValidationError('Дата выезда не может быть раньше даты заезда')
        return check_out
