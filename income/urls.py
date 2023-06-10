from django.urls import path
from . import views 
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.income, name="income"),
    path('add-income', views.add_income, name="add-income"),
    path('update-income/<int:id>', views.update_income, name="update-income"),
    path('delete-income/<int:id>', views.delete_income, name="delete-income"),
    path('filter-income', csrf_exempt(views.filter_income), name="filter-income"),
    path('search-income', csrf_exempt(views.search_income), name="search-income"),
]