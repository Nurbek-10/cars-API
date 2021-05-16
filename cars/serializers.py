from rest_framework import serializers

from cars.models import Model_auth, Brand, Car, ExtraTableForPrice, Comment


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('title', )


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraTableForPrice
        fields = ('model_auths', 'price', )


class Model_authSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_auth
        fields = ('title', )


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        model_auths = validated_data.pop('model_auth', [])
        car = Car.objects.create(**validated_data)
        car.format.add(*model_auths)
        return car

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['brand'] = Model_authSerializer(instance.brand, context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes_count'] = instance.likes.count()
        representation['price'] = PriceSerializer(instance.cars_price.all(), many=True).data
        return representation


class CarListSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='car-detail', lookup_field='slug')

    class Meta:
        model = Car
        fields = ['title', 'author', 'brand', 'image', 'details']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Укажите рейтинг от 1 до 5')
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment