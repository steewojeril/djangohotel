from django.shortcuts import render

from hotelapi.models import Dishes
from rest_framework.views import APIView
from rest_framework.response import Response
from hotelapi.serializers import DishesSerializer,DishesModelSerializer,UserModelSerializer,ReviewSerializer
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
from rest_framework.decorators import action



# using normal serializer

# url : localhost:8000/api/v1/sapphire/dishes/
# get : to retrieve all dishes
# post : to create a dish
class DishesView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        serializer=DishesSerializer(qs,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=DishesSerializer(data=request.data)
        if serializer.is_valid(): #(validation cheyyunnahtaanu) means error illenkil. [model il kotdutha attribute pole thanneyano , user pass cheythittullath enn check cheyyan. suppose price negative value koduthal error varum
            Dishes.objects.create(**serializer.validated_data)  #validated data
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
# url : localhost:8000/api/v1/sapphire/dishes/{id}
# get : to retrieve specific dish
# post : to update sp dish
# delete : to delete dish
class DishDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            qs = Dishes.objects.get(id=id)
            serializer = DishesSerializer(qs)
            return Response(data=serializer.data)
        except:
            return Response({"msg":"object does not exist"},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            object = Dishes.objects.get(id=id)
            serializer = DishesSerializer(data=request.data)
            if serializer.is_valid():
                object.name = serializer.validated_data.get("name")  # ingane ottakk otakk mathre object update cheyyan pattu. so ottakk ottakk kodukkanam. but post il orumich koduthal mathi. angane oruumich kodukkan aanu **
                object.category = serializer.validated_data.get("category")
                object.price = serializer.validated_data.get("price")
                object.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        except:
            return Response({"msg":"object does not exist"},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            object = Dishes.objects.get(id=id)
            object.delete()
            return Response({"msg": "deleted"})
        except:
            return Response({"msg":"object does not exist"},status=status.HTTP_404_NOT_FOUND)

# using model serializer

# url : localhost:8000/api/v2/sapphire/dishes/
# get : to retrieve all dishes
# post : to create a dish
class DishesModelView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        serializer=DishesModelSerializer(qs,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=DishesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

# url : localhost:8000/api/v2/sapphire/dishes/{id}
# get : to retrieve specific dish
# post : to update sp dish
# delete : to delete dish

class DisheDetailsModelView(APIView):
    def get(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            qs = Dishes.objects.get(id=id)
            serializer = DishesModelSerializer(qs)
            return Response(data=serializer.data)
        except:
            return Response({"object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def put(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            instance = Dishes.objects.get(id=id)
            serializer = DishesModelSerializer(data=request.data, instance=instance)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        except:
            return Response({"object does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,*args,**kwargs):
        try:
            id = kwargs.get("id")
            qs = Dishes.objects.get(id=id)
            qs.delete()
            return Response({"msg": "deleted"})
        except:
            return Response({"object does not exist"},status=status.HTTP_404_NOT_FOUND)

class DishesViewsetView(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        serializer=DishesModelSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def create(self,request,*args,**kwargs):
        serializer=DishesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Dishes.objects.get(id=id)
        serializer=DishesModelSerializer(object)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Dishes.objects.get(id=id)
        serializer=DishesModelSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.data,status=status.HTTP_404_NOT_FOUND)
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        object = Dishes.objects.get(id=id)
        object.delete()
        return Response({"msg":"deleted"},status=status.HTTP_204_NO_CONTENT)

class DishesModelViewsetView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = DishesModelSerializer
    queryset = Dishes.objects.all()

    # url: api/v4/sapphire/dishes/{pid}/add_review/
    # mtd :post
    # data:review,rating
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        dish=Dishes.objects.get(id=id)
        user=request.user
        serializer=ReviewSerializer(data=request.data,context={"user":user,"dish":dish})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # url: api/v4/sapphire/dishes/{pid}/get_review/
    # mtd :get
    @action(methods=["get"],detail=True)
    def get_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        dish=Dishes.objects.get(id=id)
        reviews=dish.reviews_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data)


class UserRegistrationView(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserModelSerializer



