import base64
from django.core.files.base import ContentFile
import os
from django.conf import settings
from celery import shared_task
from django.contrib.auth.models import User
from .models import Car, ImageCar

def save_base64_image(data, filename):
    """
    data: base64 string
    filename: string
    """
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr), name=f"{filename}.{ext}")

    # Şəkili fayl sistemində saxlayır
    file_path = os.path.join(settings.MEDIA_ROOT, 'user/img_cars', data.name)
    with open(file_path, 'wb') as f:
        f.write(data.read())

    return file_path

@shared_task
def create_car_task(user_id, form_data, file_data_list):
    user = User.objects.get(id=user_id)
    car = Car.objects.create(
        user=user,
        brand_id=form_data['brand_id'],
        car_models_id=form_data['car_models_id'],
        new_bord_id=form_data['new_bord_id'],
        mileage=form_data['mileage'],
        mileage_unit_id=form_data['mileage_unit_id'],
        color_id=form_data['color_id'],
        price=form_data['price'],
        price_currency_id=form_data['price_currency_id'],
        owner_number_id=form_data['owner_number_id'],
        fuel_type_id=form_data['fuel_type_id'],
        transmission_id=form_data['transmission_id'],
        year_id=form_data['year_id'],
        engine_capasity=form_data['engine_capasity'],
        engine_power=form_data['engine_power'],
        collected_for_which_market_id=form_data['collected_for_which_market_id'],
        damage_have=form_data['damage_have'],
        painted=form_data['painted'],
        for_accident_or_spare_parts=form_data['for_accident_or_spare_parts'],
        seat_count_id=form_data['seat_count_id'],
        credit_available=form_data['credit_available'],
        barter_available=form_data['barter_available'],
        vin_number=form_data['vin_number'],
        additional_info=form_data['additional_info'],
        light_alloy_whells=form_data['light_alloy_whells'],
        central_locking=form_data['central_locking'],
        leather_seat=form_data['leather_seat'],
        ventilatet_seats=form_data['ventilatet_seats'],
        abs_locking=form_data['abs_locking'],
        parking_radar=form_data['parking_radar'],
        rear_view_camera=form_data['rear_view_camera'],
        xenon_lights=form_data['xenon_lights'],
        sundroof=form_data['sundroof'],
        air_conditioner=form_data['air_conditioner'],
        heated_seats=form_data['heated_seats'],
        side_curtains=form_data['side_curtains'],
        rain_sensor=form_data['rain_sensor'],
        contact_name=form_data['contact_name'],
        city_id=form_data['city_id'],
        email=form_data['email'],
        phone_number=form_data['phone_number'],
        transmission_type_id=form_data['transmission_type_id'],
        car_status_id=form_data['car_status_id'],
        is_approved=form_data['is_approved']
    )

    # Dosyaları fayl sistemində saxlayır
    for idx, file_data in enumerate(file_data_list):
        filename = f"{user.username}_{car.id}_{idx}"
        file_path = save_base64_image(file_data, filename)
        ImageCar.objects.create(car=car, image=file_path)
