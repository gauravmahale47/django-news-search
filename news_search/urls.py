from django.urls import path
from . import views

app_name = 'news_search'

urlpatterns = [
    path('search/', views.SearchNewsView.as_view(), name='search'),
    path('result/', views.ResultView.as_view(), name='result'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('history/<str:keyword>/', views.HistoryDetailView.as_view(), name='history-detail'),
    path('sort-by-published-date/', views.SortByDateView.as_view(), name='sort-by-date'),
]
