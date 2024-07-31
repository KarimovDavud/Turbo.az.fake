from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from dal import autocomplete
from .forms import CarForm
from .serializers import BrandSerializer, CarModelSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Car, Brand, CarModel, FuelTypeChoices, TransmissionChoices,
    BodyTypeChoices, ColorChoices, MarketChoices, CityChoices,
    SeatCountChoices, OwnerCount, YearChoices, Mileage, MoneyCurrencies,
    TransmissionType, ImageCar, Profile, CarStatus
)

from .forms import CarFilterForm

def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
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
    return render(request, 'user/user_profile.html', {'profile': profile})


def car_page(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'user/car_page.html', {'car': car})


def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
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
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        
        if not username:
            messages.error(request, 'İstifadəçi adı daxil edilməlidir.')
            return render(request, 'user/register_user.html')
        
        if not email:
            messages.error(request, 'Email daxil edilməlidir.')
            return render(request, 'user/register_user.html')
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Bu istifadəçi adı artıq mövcuddur.')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                profile, created = Profile.objects.get_or_create(user=user)
                if created:
                    profile.save()
                login(request, user)
                
                # Email göndərmə məntiqi
                subject = 'Qeydiyyatınız tamamlandı'
                recipient_list = [user.email]  # istifadəçinin email adresi
                customer_message = render_to_string('user/register_email.html', {'username': username})

                try:
                    send_mail(
                        subject,
                        '',
                        'rzazadfrid@gmail.com',
                        recipient_list,
                        fail_silently=False,
                        html_message=customer_message,
                    )
                    messages.success(request, 'Qeydiyyat uğurla tamamlandı və e-poçt göndərildi.')
                except Exception as e:
                    messages.error(request, f'E-poçt göndərməkdə problem var: {e}')
                
                return redirect('home')
        else:
            messages.error(request, 'Şifrələr uyğun deyil.')
    
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
            car = form.save(commit=False)
            car.user = request.user
            car.is_approved = False  # Yeni əlavə olunan sahə
            car.save()
            
            # Adminə email göndərmək
            subject = 'Yeni elan yaradıldı'
            recipient_list = ['admin@example.com']
            customer_message = render_to_string('user/admin_notify_email.html', {'car': car})
            
            send_mail(
                subject,
                '',
                'from@example.com',  # Göndərənin emaili
                recipient_list,
                fail_silently=False,
                html_message=customer_message,
            )
            
            messages.success(request, 'Elanınız göndərildi və admin tərəfindən təsdiqlənməsini gözləyir.')
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
    cars = Car.objects.filter(is_approved=True)  # Yalnızca onaylanmış ilanları getir

    if form.is_valid():
        filters = {}
        
        # Filtrləri tətbiq etmək
        if form.cleaned_data.get('brand'):
            filters['brand'] = form.cleaned_data['brand']
        if form.cleaned_data.get('model'):
            filters['car_models'] = form.cleaned_data['model']
        if form.cleaned_data.get('min_price'):
            filters['price__gte'] = form.cleaned_data['min_price']
        if form.cleaned_data.get('max_price'):
            filters['price__lte'] = form.cleaned_data['max_price']
        if form.cleaned_data.get('min_engine_capacity'):
            filters['engine_capacity__gte'] = form.cleaned_data['min_engine_capacity']
        if form.cleaned_data.get('max_engine_capacity'):
            filters['engine_capacity__lte'] = form.cleaned_data['max_engine_capacity']
        if form.cleaned_data.get('min_power'):
            filters['engine_power__gte'] = form.cleaned_data['min_power']
        if form.cleaned_data.get('max_power'):
            filters['engine_power__lte'] = form.cleaned_data['max_power']
        if form.cleaned_data.get('min_mileage'):
            filters['mileage__gte'] = form.cleaned_data['min_mileage']
        if form.cleaned_data.get('max_mileage'):
            filters['mileage__lte'] = form.cleaned_data['max_mileage']
        if form.cleaned_data.get('min_year'):
            filters['year__gte'] = form.cleaned_data['min_year']
        if form.cleaned_data.get('max_year'):
            filters['year__lte'] = form.cleaned_data['max_year']
        if form.cleaned_data.get('CITY'):
            filters['city'] = form.cleaned_data['CITY']
        if form.cleaned_data.get('OWNER_COUNT'):
            filters['owner_number'] = form.cleaned_data['OWNER_COUNT']
        if form.cleaned_data.get('SEAT_COUNT'):
            filters['seat_count'] = form.cleaned_data['SEAT_COUNT']
        if form.cleaned_data.get('MARKET'):
            filters['collected_for_which_market'] = form.cleaned_data['MARKET']
        if form.cleaned_data.get('CAR_STATUS'):
            filters['car_status'] = form.cleaned_data['CAR_STATUS']
        if form.cleaned_data.get('BODY_TYPE'):
            filters['body_type'] = form.cleaned_data['BODY_TYPE']
        if form.cleaned_data.get('MILEAGE_UNIT'):
            filters['mileage_unit'] = form.cleaned_data['MILEAGE_UNIT']

        cars = cars.filter(**filters)

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
        'car_status': CarStatus.objects.all()
    }
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


class CarModelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CarModel.objects.none()

        qs = CarModel.objects.all()

        brand_id = self.forwarded.get('brand', None)
        if brand_id:
            qs = qs.filter(brand_id=brand_id)

        return qs


def like_page(request):
    return render(request, 'user/like.html')

