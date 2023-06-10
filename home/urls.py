from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="index"),
    path('stats-data', csrf_exempt(views.stats_data), name="stats-data"),
    path('filter-stats', csrf_exempt(views.filter_stats), name="filter-stats"),
]
