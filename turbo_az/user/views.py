import base64

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Car
from user.tasks import send_registration_email  
from django.conf import settings
from django.utils.html import strip_tags
from .serializers import CarSerializer
from rest_framework import generics
from .forms import CarFilterForm
from .tasks import create_car_task
from django.core.files.storage import default_storage
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .forms import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Car, Brand, CarModel, FuelTypeChoices, TransmissionChoices,
    BodyTypeChoices, ColorChoices, MarketChoices, CityChoices,
    SeatCountChoices, OwnerCount, YearChoices, Mileage, MoneyCurrencies,
    TransmissionType, ImageCar, Profile, CarStatus
)


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if car.user != request.user:
        messages.error(request, 'Siz bu elanı silməyə icazəniz yoxdur.')
        return redirect('home')
    
    if request.method == 'POST':
        car.delete()
        return redirect('home')
    
    return render(request, 'user/delete_car.html', {'car': car})


@login_required
def user_cars(request):
    user = request.user
    cars = Car.objects.filter(user=user)
    return render(request, 'user/user_cars.html', {'cars': cars})

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    approved_cars = Car.objects.filter(user=request.user, is_approved=True)
    pending_cars = Car.objects.filter(user=request.user, is_approved=False)
    context = {
        'profile': profile,
        'approved_cars': approved_cars,
        'pending_cars': pending_cars
    }
    return render(request, 'user/user_profile.html', context)

@login_required
def delete_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        user = profile.user
        profile.delete()
        user.delete()  # İstifadəçini də silmək üçün
        messages.success(request, 'Profil və istifadəçi uğurla silindi.')
        return redirect('home')  # Silindikdən sonra ana səhifəyə yönləndiririk
    return render(request, 'user/delete_profile.html', {'profile': profile})



def car_page(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.increment_view_count()
    return render(request, 'user/car_page.html', {'car': car})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = form.cleaned_data['phone']
            profile.gender = form.cleaned_data['gender']
            profile.birth_date = form.cleaned_data['birth_date']
            profile.save()
            messages.success(request, 'Profiliniz uğurla yeniləndi.')
            return redirect('home')  # Əsas səhifəyə yönləndirir
    else:
        form = ProfileForm(instance=request.user, user=request.user)
    
    return render(request, 'user/edit_profile.html', {'form': form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if car.user != request.user:
        messages.error(request, 'Siz bu elanı redaktə etməyə icazəniz yoxdur.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm(instance=car)
    
    return render(request, 'user/edit_car.html', {'form': form, 'car': car})

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not username:
            messages.error(request, 'İstifadəçi adı daxil edilməlidir.')
            return render(request, 'user/register_user.html')
        
        if not email:
            messages.error(request, 'E-mail daxil edilməlidir.')
            return render(request, 'user/register_user.html')
        
        if password != confirm_password:
            messages.error(request, 'Şifrələr uyğun deyil.')
            return render(request, 'user/register_user.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu istifadəçi adı artıq mövcuddur.')
            return render(request, 'user/register_user.html')

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        try:
            profile = Profile.objects.get(user=user)
            profile.phone = phone
            profile.gender = gender
            profile.birth_date = birth_date
            profile.save()
        except ObjectDoesNotExist:
            profile = Profile.objects.create(user=user, phone=phone, gender=gender, birth_date=birth_date)
        
        login(request, user)
        
        # Use Celery to send the registration email
        send_registration_email.delay(username, email)

        messages.success(request, 'Qeydiyyat uğurla tamamlandı və e-poçt göndərildi.')
        return redirect('home')
    
    return render(request, 'user/register_user.html')

    
def login_user(request):
    if request.method == 'POST':
        print(request.POST)  
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Yanlış istifadəçi adı və ya şifrə.')
    
    return render(request, 'user/login_user.html')



@login_required
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            # Form məlumatlarını model instansiyasına çevir
            car_instance = form.save(commit=False)
            car_instance.user = request.user
            car_instance.save()

            # Model instansiyasını serializer ilə JSON formatına çevir
            serializer = CarSerializer(car_instance)
            serialized_data = serializer.data

            # Faylları base64 formatına çevir
            file_data_list = []
            for file in request.FILES.values():
                file_data = base64.b64encode(file.read()).decode('utf-8')
                file_data_list.append(f"data:{file.content_type};base64,{file_data}")

            # Asinxron iş yarat
            create_car_task.delay(request.user.id, serialized_data, file_data_list)

            # Email göndərmə
            subject = 'Yeni Elanınız Yaradıldı'
            html_message = render_to_string('user/user_notify_email.html', {'car': serialized_data})
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email, settings.ADMIN_EMAIL]

            email = EmailMessage(subject, html_message, from_email, recipient_list)
            email.send()
            messages.success(request, 'İlanınız göndərildi və admin tərəfindən təsdiqlənməsini gözləyir.')
            return redirect('home')
    else:
        form = CarForm()

    context = {
        'form': form,
        'brands': Brand.objects.all(),
        'models_car': CarModel.objects.all(),
        'fuel_type': FuelTypeChoices.objects.all(),
        'transmission': TransmissionChoices.objects.all(),
        'body_type': BodyTypeChoices.objects.all(),
        'color': ColorChoices.objects.all(),
        'market': MarketChoices.objects.all(),
        'city': CityChoices.objects.all(),
        'seat_count': SeatCountChoices.objects.all(),
        'owner_count': OwnerCount.objects.all(),
        'year': YearChoices.objects.all(),
        'milage_car': Mileage.objects.all(),
        'mony_currenc': MoneyCurrencies.objects.all(),
        'transmission_type': TransmissionType.objects.all(),
        'image_car': ImageCar.objects.all(),
        'car_status': CarStatus.objects.all()
    }
    return render(request, 'user/create_car.html', context)

@login_required
def approve_car(request, car_id):
    if request.user.is_superuser:
        try:
            car = Car.objects.get(id=car_id)
            car.is_approved = True
            car.save()
            messages.success(request, 'Elan təsdiqləndi.')
        except Car.DoesNotExist:
            messages.error(request, 'Elan tapılmadı.')
    else:
        messages.error(request, 'İcazəniz yoxdur.')
    
    return redirect('admin_car_list')

def home(request):
    form = CarFilterForm(request.GET or None)
    vip_cars = Car.objects.filter(is_vip=True).order_by('-is_vip')  

    cars = Car.objects.filter(is_approved=True).order_by('-is_vip') 
    if form.is_valid():
        filters = {}
        
        cleaned_data = form.cleaned_data

        if cleaned_data.get('brand'):
            filters['brand'] = cleaned_data['brand']
        if cleaned_data.get('model'):
            filters['car_models'] = cleaned_data['model']
        if cleaned_data.get('min_price'):
            filters['price__gte'] = cleaned_data['min_price']
        if cleaned_data.get('max_price'):
            filters['price__lte'] = cleaned_data['max_price']
        if cleaned_data.get('min_engine_capasity'):
            filters['engine_capasity__gte'] = cleaned_data['min_engine_capasity']
        if cleaned_data.get('max_engine_capasity'):
            filters['engine_capasity__lte'] = cleaned_data['max_engine_capasity']
        if cleaned_data.get('min_power'):
            filters['engine_power__gte'] = cleaned_data['min_power']
        if cleaned_data.get('max_power'):
            filters['engine_power__lte'] = cleaned_data['max_power']
        if cleaned_data.get('min_mileage'):
            filters['mileage__gte'] = cleaned_data['min_mileage']
        if cleaned_data.get('max_mileage'):
            filters['mileage__lte'] = cleaned_data['max_mileage']
        if cleaned_data.get('min_year'):
            filters['year__gte'] = cleaned_data['max_year']
        if cleaned_data.get('max_year'):
            filters['year__lte'] = cleaned_data['min_year']
        if cleaned_data.get('CITY'):
            filters['city'] = cleaned_data['CITY']
        if cleaned_data.get('OWNER_COUNT'):
            filters['owner_number'] = cleaned_data['OWNER_COUNT']
        if cleaned_data.get('SEAT_COUNT'):
            filters['seat_count'] = cleaned_data['SEAT_COUNT']
        if cleaned_data.get('MARKET'):
            filters['collected_for_which_market'] = cleaned_data['MARKET']
        if cleaned_data.get('CAR_STATUS'):
            filters['car_status'] = cleaned_data['CAR_STATUS']
        if cleaned_data.get('BODY_TYPE'):
            filters['body_type'] = cleaned_data['BODY_TYPE']
        if cleaned_data.get('MILEAGE_UNIT'):
            filters['mileage_unit'] = cleaned_data['MILEAGE_UNIT']
        
        cars = cars.filter(**filters)
        cars = cars.order_by('-is_vip', 'id')

    context = {
        'form': form,
        'cars': cars,
        'brands_car': Brand.objects.all(),
        'models_car': CarModel.objects.all(),
        'fuel_type': FuelTypeChoices.objects.all(),
        'transmission': TransmissionChoices.objects.all(),
        'body_type': BodyTypeChoices.objects.all(),
        'color': ColorChoices.objects.all(),
        'market': MarketChoices.objects.all(),
        'city': CityChoices.objects.all(),
        'seat_count': SeatCountChoices.objects.all(),
        'owner_count': OwnerCount.objects.all(),
        'year': YearChoices.objects.all(),
        'mileage_unit': Mileage.objects.all(),
        'mony_currenc': MoneyCurrencies.objects.all(),
        'transmission_type': TransmissionType.objects.all(),
        'image_car': ImageCar.objects.all(),
        'car_status': CarStatus.objects.all(),
        'is_vip': IsVip.objects.all(),
    }

    if request.user.is_authenticated:
        user_cars = Car.objects.filter(user=request.user)
        profile = Profile.objects.get(user=request.user)
        context.update({
            'user_cars': user_cars,
            'profile': profile,
        })
    return render(request, 'user/home.html', context)


def login_register(request):
    return render(request, 'user/login_register.html')


def salons(request):
    return render(request, 'salons/salons.html')


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @action(detail=True, methods=['get'])
    def models(self, request, pk=None):
        brand = self.get_object()
        car_models = CarModel.objects.filter(brand=brand)
        serializer = CarModelSerializer(car_models, many=True)
        return Response(serializer.data)


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class MileageViewSet(viewsets.ModelViewSet):
    queryset = Mileage.objects.all()
    serializer_class = MileageSerializer

class MoneyCurrenciesViewSet(viewsets.ModelViewSet):
    queryset = MoneyCurrencies.objects.all()
    serializer_class = MoneyCurrenciesSerializer

class FuelTypeChoicesViewSet(viewsets.ModelViewSet):
    queryset = FuelTypeChoices.objects.all()
    serializer_class = FuelTypeChoicesSerializer

class TransmissionChoicesViewSet(viewsets.ModelViewSet):
    queryset = TransmissionChoices.objects.all()
    serializer_class = TransmissionChoicesSerializer

class BodyTypeChoicesViewSet(viewsets.ModelViewSet):
    queryset = BodyTypeChoices.objects.all()
    serializer_class = BodyTypeChoicesSerializer

class ColorChoicesViewSet(viewsets.ModelViewSet):
    queryset = ColorChoices.objects.all()
    serializer_class = ColorChoicesSerializer

class MarketChoicesViewSet(viewsets.ModelViewSet):
    queryset = MarketChoices.objects.all()
    serializer_class = MarketChoicesSerializer

class CityChoicesViewSet(viewsets.ModelViewSet):
    queryset = CityChoices.objects.all()
    serializer_class = CityChoicesSerializer

class SeatCountChoicesViewSet(viewsets.ModelViewSet):
    queryset = SeatCountChoices.objects.all()
    serializer_class = SeatCountChoicesSerializer

class OwnerCountViewSet(viewsets.ModelViewSet):
    queryset = OwnerCount.objects.all()
    serializer_class = OwnerCountSerializer

class YearChoicesViewSet(viewsets.ModelViewSet):
    queryset = YearChoices.objects.all()
    serializer_class = YearChoicesSerializer

class CarStatusViewSet(viewsets.ModelViewSet):
    queryset = CarStatus.objects.all()
    serializer_class = CarStatusSerializer

class IsApprovedViewSet(viewsets.ModelViewSet):
    queryset = IsApproved.objects.all()
    serializer_class = IsApprovedSerializer

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarListView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer





def like_page(request):
    return render(request, 'user/like.html')



