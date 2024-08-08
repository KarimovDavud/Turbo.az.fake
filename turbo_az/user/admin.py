from .models import Profile
from django.contrib import admin
from .forms import CarForm, CarFilterForm
from .models import (
    Car, Mileage, MoneyCurrencies, FuelTypeChoices, TransmissionChoices,
    BodyTypeChoices, ColorChoices, MarketChoices, CityChoices,
    SeatCountChoices, OwnerCount, Brand, CarModel, TransmissionType, ImageCar,YearChoices, CarStatus, IsApproved, IsVip
)

class CarAdmin(admin.ModelAdmin):
    form = CarForm
    list_display = ('brand', 'car_models', 'price', 'year', 'mileage', 'is_approved', 'is_vip')
    search_fields = ('name', 'brand__name', 'car_models__name', 'year', 'price')
    list_filter = ('brand', 'car_models', 'fuel_type', 'transmission', 'is_approved', 'is_vip')
    # is_approved sahəsini admin interfeysdə redaktə etmək üçün fields əlavə edin
    fields = ('user', 'brand', 'car_models', 'new_bord', 'mileage', 'mileage_unit', 'color', 'price', 'price_currency',
              'owner_number', 'fuel_type', 'transmission', 'year', 'engine_capasity', 'engine_power',
              'collected_for_which_market', 'damage_have', 'painted', 'for_accident_or_spare_parts', 'seat_count',
              'credit_available', 'barter_available', 'vin_number', 'additional_info', 'light_alloy_whells',
              'central_locking', 'leather_seat', 'ventilatet_seats', 'abs_locking', 'parking_radar',
              'rear_view_camera', 'xenon_lights', 'sundroof', 'air_conditioner', 'heated_seats', 'side_curtains',
              'rain_sensor', 'front_view_image', 'rear_view_image', 'interior_view_image', 'contact_name', 'city',
              'email', 'phone_number', 'transmission_type', 'car_status', 'is_approved', 'is_vip')

admin.site.register(CarStatus)
admin.site.register(YearChoices)
admin.site.register(Car, CarAdmin)
admin.site.register(Mileage)
admin.site.register(MoneyCurrencies)
admin.site.register(FuelTypeChoices)
admin.site.register(TransmissionChoices)
admin.site.register(BodyTypeChoices)
admin.site.register(ColorChoices)
admin.site.register(MarketChoices)
admin.site.register(CityChoices)
admin.site.register(SeatCountChoices)
admin.site.register(OwnerCount)
admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(TransmissionType)
admin.site.register(ImageCar)
admin.site.register(IsApproved)
admin.site.register(IsVip)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'birth_date', 'gender')