from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('create/', views.create, name = "create"),
    path('register/', views.register, name = "register"),
    path('<int:tid>/edit/', views.update, name = "update"),
    path('<int:tid>/delete/', views.delete, name = "delete"),
]