from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import ( CarStatus, Car, Brand, CarModel, FuelTypeChoices, TransmissionChoices,
    BodyTypeChoices, ColorChoices, MarketChoices, CityChoices,
    SeatCountChoices, OwnerCount, YearChoices, Mileage, MoneyCurrencies,
    TransmissionType, ImageCar, Profile
)

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'car_models', 'new_bord', 'mileage', 'mileage_unit',
            'color', 'price', 'price_currency', 'owner_number', 'fuel_type',
            'transmission', 'year', 'engine_capasity', 'engine_power',
            'collected_for_which_market', 'damage_have', 'painted',
            'for_accident_or_spare_parts', 'seat_count', 'credit_available',
            'barter_available', 'vin_number', 'additional_info',
            'light_alloy_whells', 'central_locking', 'leather_seat',
            'ventilatet_seats', 'abs_locking', 'parking_radar',
            'rear_view_camera', 'xenon_lights', 'sundroof', 'air_conditioner',
            'heated_seats', 'side_curtains', 'rain_sensor', 'front_view_image',
            'rear_view_image', 'interior_view_image', 'contact_name', 'city',
            'phone_number', 'transmission_type', 'car_status'
        ]
        widgets = {
            'front_view_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'rear_view_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'interior_view_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class CarFilterForm(forms.Form):
    brand = forms.ChoiceField(choices=[('', '-------')], required=False)
    model = forms.ChoiceField(choices=[('', '-------')], required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_engine_capasity = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    max_engine_capasity = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    min_power = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    max_power = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    min_mileage = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_mileage = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    MILEAGE_UNIT = forms.ChoiceField(choices=[('', '-------')], required=False)
    min_year = forms.ModelChoiceField(queryset=YearChoices.objects.all(), required=False)
    max_year = forms.ModelChoiceField(queryset=YearChoices.objects.all(), required=False)
    CITY = forms.ChoiceField(choices=[('', '-------')], required=False)
    OWNER_COUNT = forms.ChoiceField(choices=[('', '-------')], required=False)
    SEAT_COUNT = forms.ChoiceField(choices=[('', '-------')], required=False)
    MARKET = forms.ChoiceField(choices=[('', '-------')], required=False)
    CAR_STATUS = forms.ChoiceField(choices=[('', '-------')], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].choices += [(brand.id, brand.name) for brand in Brand.objects.all()]
        self.fields['model'].choices += [(model.id, model.name) for model in CarModel.objects.all()]
        self.fields['MILEAGE_UNIT'].choices += [(mileage.id, mileage.name) for mileage in Mileage.objects.all()]
        self.fields['CITY'].choices += [(city.id, city.name) for city in CityChoices.objects.all()]
        self.fields['OWNER_COUNT'].choices += [(owner.id, owner.name) for owner in OwnerCount.objects.all()]
        self.fields['SEAT_COUNT'].choices += [(seat.id, seat.name) for seat in SeatCountChoices.objects.all()]
        self.fields['MARKET'].choices += [(market.id, market.name) for market in MarketChoices.objects.all()]
        self.fields['CAR_STATUS'].choices += [(status.id, status.name) for status in CarStatus.objects.all()]

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)
    birth_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                profile = Profile.objects.get(user=user)
                self.fields['phone'].initial = profile.phone
                self.fields['gender'].initial = profile.gender
                self.fields['birth_date'].initial = profile.birth_date
            except Profile.DoesNotExist:
                pass


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    phone = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=[('male', 'Kişi'), ('female', 'Qadın'), ('other', 'Digər')])
    birth_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Şifrələr uyğun gəlmir.')

        return cleaned_data