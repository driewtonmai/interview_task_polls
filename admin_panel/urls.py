from django.urls import path

from . import views


app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('polls/', views.PollListCreateAPIView.as_view(), name='polls-list-create'),
    path('polls/<int:pk>/', views.PollDetailView.as_view(), name='polls-retrieve'),
]
