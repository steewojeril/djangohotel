"""hotelproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotelapi import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register("api/v3/sapphire/dishes",views.DishesViewsetView,basename="dishes")
router.register("api/v4/sapphire/dishes",views.DishesModelViewsetView,basename="modeldishes")
router.register("api/v5/accounts/register",views.UserRegistrationView,basename="registration")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/sapphire/dishes/',views.DishesView.as_view()),
    path('api/v1/sapphire/dishes/<int:id>/',views.DishDetailsView.as_view()),
    path('api/v2/sapphire/dishes/',views.DishesModelView.as_view()),
    path('api/v2/sapphire/dishes/<int:id>/',views.DisheDetailsModelView.as_view()),
    path("accounts/token/",obtain_auth_token)
]+router.urls
