from django import forms
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
            'email', 'phone_number', 'transmission_type', 'car_status'
        ]
        widgets = {
            'front_view_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'rear_view_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'interior_view_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class CarFilterForm(forms.Form):
    # Marka seçimləri üçün query seti
    brand_choices = Brand.objects.values_list('name', flat=True).distinct()
    brand_choices = [(brand, brand) for brand in brand_choices]

    # Model seçimləri üçün query seti
    model_choices = CarModel.objects.values_list('name', flat=True).distinct()
    model_choices = [(model, model) for model in model_choices]



    brand = forms.ChoiceField(choices=[('', 'Tüm Markalar')] + brand_choices, required=False)
    model = forms.ChoiceField(choices=[('', 'Tüm Modeller')] + model_choices, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    min_engine_capacity = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    max_engine_capacity = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    min_power = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    max_power = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    min_mileage = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_mileage = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    MILEAGE_UNIT = forms.ChoiceField(choices=[('', 'Mileage seçin')] + [(mileage.id, mileage.name) for mileage in Mileage.objects.all()], required=False)
    min_year = forms.ModelChoiceField(queryset=YearChoices.objects.all(), required=False)
    max_year = forms.ModelChoiceField(queryset=YearChoices.objects.all(), required=False)
    CITY = forms.ChoiceField(choices=[('', 'Şəhər seçin')] + [(city.id, city.name) for city in CityChoices.objects.all()], required=False)
    OWNER_COUNT = forms.ChoiceField(choices=[('', 'Sahib sayı seçin')] + [(owner.id, owner.name) for owner in OwnerCount.objects.all()], required=False)
    SEAT_COUNT = forms.ChoiceField(choices=[('', 'Yerlər sayı seçin')] + [(seat.id, seat.name) for seat in SeatCountChoices.objects.all()], required=False)
    MARKET = forms.ChoiceField(choices=[('', 'Bazar seçin')] + [(market.id, market.name) for market in MarketChoices.objects.all()], required=False)
    CAR_STATUS = forms.ChoiceField(choices=[('', 'Status seçin')] + [(status.id, status.name) for status in CarStatus.objects.all()], required=False)
