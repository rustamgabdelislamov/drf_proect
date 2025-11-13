from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from vehicle.models import Car, Moto, Millage
from vehicle.services import convert_currencies
from vehicle.validators import TitleValidator


class MillageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Millage
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    last_milage = serializers.IntegerField(source='milage.all.first.milage', read_only=True)
    # • millage — обратная связь (RelatedManager) для модели Millage (обычно так называется автоматически при ForeignKey).
    # • all — менеджер/метод all() будет вызван
    # • first — у возвращённого QuerySet вызовется first().
    # • milage — берётся атрибут milage у найденного экземпляра.
    milage = MillageSerializer(many=True, required=False)
    usd_price = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = '__all__'

    def get_usd_price(self, instance):
        return convert_currencies(instance.amount)

    def create(self, validated_data):
        # Извлекаем данные пробега из validated_data
        milage = validated_data.pop("milage", [])

        car_item = Car.objects.create(**validated_data)
        # Для каждого элемента пробега создаем отдельную запись
        for m in milage:
            Millage.objects.create(**m, car=car_item)  # Связываем с созданной машиной

        return car_item


class MotoSerializer(serializers.ModelSerializer):
    last_milage = serializers.SerializerMethodField()
    class Meta:
        model = Moto
        fields = '__all__'

    def get_last_milage(self, instance):
        if instance.milage.all().first():
            return instance.milage.all().first().milage
        return 0


class MotoMillageSerializer(serializers.ModelSerializer):
    moto = MotoSerializer()

    class Meta:
        model = Millage
        fields = ('milage', 'year', 'moto')


class MotoCreateSerializer(serializers.ModelSerializer):
    milage = MillageSerializer(many=True)

    class Meta:
        model = Moto
        fields = '__all__'
        validators = [TitleValidator(field='title'), UniqueTogetherValidator(fields=['title', 'description'], queryset=Moto.objects.all())]

    def create(self, validated_data):
        milage = validated_data.pop('milage')

        moto_item = Moto.objects.create(**validated_data)

        for m in milage:
            Millage.objects.create(**m, moto=moto_item)

        return moto_item

