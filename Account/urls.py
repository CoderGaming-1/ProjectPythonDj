from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.get_login_view, name='login'),
    path('postLogin/', views.login_view, name='login'),
    path('register/', views.get_register_view, name='register'),
    path('postRegister/', views.register_view, name='register'),
    path('admin/', views.admin, name='admin'),
    path('patient/', views.patient, name='patient'),
    path('doctor/<int:idUser>', views.doctor, name='doctor'),
    path('forgetpass/', views.forget_password, name='forgetpass'),
]