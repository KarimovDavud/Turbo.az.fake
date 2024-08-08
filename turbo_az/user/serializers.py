from rest_framework import serializers
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'brand', 'name']

class MileageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mileage
        fields = ['id', 'name']

class MoneyCurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyCurrencies
        fields = ['id', 'name']

class FuelTypeChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelTypeChoices
        fields = ['id', 'name']

class TransmissionChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionChoices
        fields = ['id', 'name']

class BodyTypeChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyTypeChoices
        fields = ['id', 'name']

class ColorChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorChoices
        fields = ['id', 'name'] 

class MarketChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketChoices
        fields = ['id', 'name'] 

class CityChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityChoices
        fields = ['id', 'name']

class SeatCountChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatCountChoices
        fields = ['id', 'name']

class OwnerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerCount
        fields = ['id', 'name']

class YearChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearChoices
        fields = ['id', 'name']

class TransmissionChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionChoices
        fields = ['id', 'name']

class CarStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarStatus
        fields = ['id', 'name']

class IsApprovedSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsApproved
        fields = ['id', 'name']

class IsVipSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsVip
        fields = ['id', 'name']

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'