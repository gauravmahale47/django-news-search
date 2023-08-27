from django.urls import path
from . import views

app_name = 'auth_management'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('admin-page/', views.AdminCollectionView.as_view(), name='admin'),
    path('admin-page/<int:pk>/', views.AdminSingleView.as_view(), name='admin-detail'),
]
