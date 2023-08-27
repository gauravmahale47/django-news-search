from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_management.urls', namespace='auth_management')),
    path('news/', include('news_search.urls', namespace='news_search')),
]
