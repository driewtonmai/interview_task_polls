from django.urls import path

from . import views


app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin-login'),
]
