from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView
from .views import *
from . import views
from django.contrib.auth import views as auth_views


router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'carmodles', CarModelViewSet)
router.register(r'mileage', MileageViewSet)
router.register(r'money-currencies', MoneyCurrenciesViewSet)
router.register(r'fuel-type-choices', FuelTypeChoicesViewSet)
router.register(r'transmission-choices', TransmissionChoicesViewSet)
router.register(r'body-type-choices', BodyTypeChoicesViewSet)
router.register(r'color-choices', ColorChoicesViewSet)
router.register(r'market-choices', MarketChoicesViewSet)
router.register(r'city-choices', CityChoicesViewSet)
router.register(r'seat-count-choices', SeatCountChoicesViewSet)
router.register(r'owner-count', OwnerCountViewSet)
router.register(r'year-choices', YearChoicesViewSet)
router.register(r'car-status', CarStatusViewSet)
router.register(r'is-approved', IsApprovedViewSet)
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('create_car/', views.create_car, name='create_car'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'), 
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('api', include(router.urls)),
    path('car-model-autocomplete/', CarModelAutocomplete.as_view(), name='car-model-autocomplete'),
    path('', views.home, name='home'),
    path('salon/', views.salons, name='salons'),
    path('favicon.ico/', RedirectView.as_view(url='/static/favicon.ico')),
    path('like/', views.like_page, name='like_page'),
    path('login-register/', views.login_register, name='login_register'),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('car_page/<int:car_id>/', views.car_page, name='car_page'),
    path('approve_car/<int:car_id>/', views.approve_car, name='approve_car'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    path('create_payment/<int:car_id>/', views.create_payment, name='create_payment'),
    path('execute_payment/<int:car_id>/', views.execute_payment, name='execute_payment'),
    path('cancel_payment/', views.cancel_payment, name='cancel_payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

