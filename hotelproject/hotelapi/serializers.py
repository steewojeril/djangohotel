from rest_framework import serializers
from hotelapi.models import Dishes,Reviews
from django.contrib.auth.models import User

# using normal serializer

class DishesSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField()
    category=serializers.CharField()
    price=serializers.IntegerField()

    def validate(self,data):
        cost=data.get("price")
        if cost<0:
            raise serializers.ValidationError("invalid price")
        return data

# using modelserilaizer

class DishesModelSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    average_review=serializers.CharField(read_only=True)
    total_reviews=serializers.CharField(read_only=True)
    class Meta:
        model=Dishes
        fields=["id",
            "name",
            "category",
            "price",
            "average_review",
            "total_reviews"
        ]
    def validate(self,data):
        price=data.get("price")
        if price<0:
            raise serializers.ValidationError("invalid price")
        return data

class UserModelSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=[
            "username",
            "first_name",
            "last_name",
            "email",
            "password"
        ]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    customer=UserModelSerializer(read_only=True)
    class Meta:
        model=Reviews
        fields=["review","rating","customer"]

    def create(self, validated_data):
        user=self.context.get("user")
        dish=self.context.get("dish")
        return Reviews.objects.create(customer=user,dish=dish,**validated_data)


