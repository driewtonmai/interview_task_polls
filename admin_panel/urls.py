from django.urls import path

from . import views


app_name = 'admin_panel'

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('polls/', views.PollListCreateAPIView.as_view(), name='admin-polls-list-create'),
    path('polls/<int:pk>/', views.PollDetailView.as_view(), name='admin-polls-retrieve'),
    path('polls/<int:polls_pk>/questions/', views.QuestionListCreateAPIView.as_view(),
         name='admin-questions-list-create'),
    path('polls/<int:polls_pk>/questions/<int:questions_pk>/',
         views.QuestionDetailAPIView.as_view(), name='admin-questions-retrieve'),
]
