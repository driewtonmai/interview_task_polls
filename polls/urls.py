from django.urls import path

from . import views


app_name = 'polls'

urlpatterns = [
    path('', views.ActivePollListView.as_view(), name='polls-active-list'),
    path('<int:pk>/', views.ActivePollDetailView.as_view(), name='polls-detail'),
    path('select-poll/', views.CreateUserSelectPollView.as_view(), name='select-poll'),
    path('create-answer/', views.CreateAnswerView.as_view(), name='write-answer'),
    path('client/<int:pk>/results/', views.ListClientResultsView.as_view(), name='list-client-results'),
    path('client/<int:client_pk>/results/<int:selected_poll_pk>/',
         views.RetrieveClientResultsView.as_view(), name='retrieve-client-results'),
]
