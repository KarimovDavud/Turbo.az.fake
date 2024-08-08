from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    subject_template_name = 'user/password_reset_subject.txt'
    email_template_name = 'user/password_reset_email.html'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Kişi'), ('female', 'Qadın'), ('other', 'Digər')], null=True, blank=True)

    def __str__(self):
        return self.user.username


class Mileage(models.Model):
    name = models.CharField(max_length=6)
    def __str__(self):
        return f"{self.name}"

class MoneyCurrencies(models.Model):
    name = models.CharField(max_length=8)
    def __str__(self):
        return f"{self.name}"

class FuelTypeChoices(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.name}"

class TransmissionChoices(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.name}"

class BodyTypeChoices(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.name}"

class ColorChoices(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.name}"

class MarketChoices(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.name}"

class CityChoices(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.name}"

class SeatCountChoices(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.name}"

class OwnerCount(models.Model):
    name = models.CharField(max_length=36)
    def __str__(self):
        return f"{self.name}"

class YearChoices(models.Model):
    name = models.IntegerField()
    def __str__(self):
        return f"{self.name}"

class Brand(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.name}"

class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class TransmissionType(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.name}"

class CarStatus(models.Model):
    name = models.CharField(max_length=30, verbose_name='Status')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuslar'


class IsApproved(models.Model):
    name = models.CharField(max_length=30, verbose_name='Tesdiq')

    def __str__(self):
        return self.name

class IsVip(models.Model):
    name = models.CharField(max_length=30, verbose_name='Vip')

    def __str__(self):
        return self.name

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Marka')
    car_models = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Model')
    mileage = models.PositiveIntegerField(verbose_name='Yuruyus')
    mileage_unit = models.ForeignKey(Mileage, on_delete=models.CASCADE, default='km')
    new_bord = models.ForeignKey(BodyTypeChoices, on_delete=models.CASCADE, verbose_name='Ban novu')
    color = models.ForeignKey(ColorChoices, on_delete=models.CASCADE, verbose_name='Reng')
    price = models.PositiveIntegerField(verbose_name='Qiymət')
    price_currency = models.ForeignKey(MoneyCurrencies, on_delete=models.CASCADE, default='AZN', verbose_name='Valyuta')
    owner_number = models.ForeignKey(OwnerCount, on_delete=models.CASCADE, verbose_name='Necenci sahibisiniz?')
    fuel_type = models.ForeignKey(FuelTypeChoices, on_delete=models.CASCADE, verbose_name='Yanacaq novu')
    transmission = models.ForeignKey(TransmissionChoices, on_delete=models.CASCADE, verbose_name='Surretler qutusu')
    year = models.ForeignKey(YearChoices, on_delete=models.CASCADE, verbose_name='il')
    engine_capasity = models.PositiveIntegerField(verbose_name='Mühərrikin həcmi, sm³')
    engine_power = models.PositiveIntegerField(verbose_name='Mühərrikin gücü, a.g.')
    collected_for_which_market = models.ForeignKey(MarketChoices, on_delete=models.CASCADE, verbose_name='Hansi bazar ucun yigilib', default='Bakı')
    damage_have = models.BooleanField(default=False, verbose_name='Vurugu var')
    painted = models.BooleanField(default=False, verbose_name='Renglenib')
    for_accident_or_spare_parts = models.BooleanField(default=False, verbose_name='Qezali ve ya ehtiyyat hisseler ucun')
    seat_count = models.ForeignKey(SeatCountChoices, on_delete=models.CASCADE, verbose_name='Yerlerin sayi')
    credit_available = models.BooleanField(default=False, verbose_name='Kreditle')
    barter_available = models.BooleanField(default=False, verbose_name='Barter mumkundur')
    vin_number = models.CharField(max_length=17, verbose_name='VIN_kod')
    additional_info = models.TextField(max_length=320, verbose_name='Elave melumat')
    light_alloy_whells = models.BooleanField(default=False, verbose_name='Yüngül lehimli disklər')
    central_locking = models.BooleanField(default=False, verbose_name='Mərkəzi qapanma')
    leather_seat = models.BooleanField(default=False, verbose_name='Dəri salon')
    ventilatet_seats = models.BooleanField(default=False, verbose_name='Oturacaqların ventilyasiyası')
    abs_locking = models.BooleanField(default=False, verbose_name='ABS')
    parking_radar = models.BooleanField(default=False, verbose_name='Park radarı')
    rear_view_camera = models.BooleanField(default=False, verbose_name='Arxa görüntü kamerası')
    xenon_lights = models.BooleanField(default=False, verbose_name='Ksenon lampalar')
    sundroof = models.BooleanField(default=False, verbose_name='Lyuk')
    air_conditioner = models.BooleanField(default=False, verbose_name='Kondisioner')
    heated_seats = models.BooleanField(default=False, verbose_name='Oturacaqların isidilməsi')
    side_curtains = models.BooleanField(default=False, verbose_name='Yan pərdələr')
    rain_sensor = models.BooleanField(default=False, verbose_name='Yağış sensoru')
    front_view_image = models.ImageField(upload_to='user/img_cars', verbose_name='Ön görünüşü', blank=True, null=True)
    rear_view_image = models.ImageField(upload_to='user/img_cars', verbose_name='Arxa görünüşü', blank=True, null=True)
    interior_view_image = models.ImageField(upload_to='user/img_cars', verbose_name='Ön paneli', blank=True, null=True)
    contact_name = models.CharField(max_length=100, verbose_name='Adınız', default=None)
    city = models.ForeignKey(CityChoices, on_delete=models.CASCADE, verbose_name='Şəhər', default='Bakı')
    email = models.EmailField(verbose_name='E-mail', blank=True)
    phone_number = models.CharField(max_length=20, verbose_name='Telefon nömrəsi')
    transmission_type = models.ForeignKey(TransmissionType, on_delete=models.CASCADE, null=True, verbose_name='Ötürücü')
    car_status = models.ForeignKey(CarStatus, on_delete=models.CASCADE, null=True, verbose_name='Status')
    is_approved = models.BooleanField(default=False, verbose_name='Təsdiq')
    is_vip = models.BooleanField(default=False, verbose_name='Vip')

    def __str__(self):
        return f"{self.brand} {self.car_models} - {self.price}"

class ImageCar(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Avtomobil')
    image = models.ImageField(upload_to='user/img_cars', verbose_name='Şəkil')  # Eksik alan eklendi

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'Avtomobil Şəkili'
        verbose_name_plural = 'Avtomobil Şəkilləri'

