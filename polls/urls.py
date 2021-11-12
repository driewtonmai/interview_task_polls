from django.urls import path

from . import views


app_name = 'polls'

urlpatterns = [
    path('', views.ListActivePollsView.as_view(), name='polls-active-list')
]