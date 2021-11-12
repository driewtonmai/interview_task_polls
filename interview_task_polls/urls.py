from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/polls/', include('polls.urls')),
    path('api/v1/admin-panel/', include('admin_panel.urls')),
    path('admin/', admin.site.urls),
]
