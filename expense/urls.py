from django.urls import path
from . import views 
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.expense, name="expense"),
    path('add-expense', views.add_expense, name="add-expense"),
    path('update-expense/<int:id>', views.update_expense, name="update-expense"),
    path('delete-expense/<int:id>', views.delete_expense, name="delete-expense"),
    path('filter-expense', csrf_exempt(views.filter_expense), name="filter-expense"),
    path('search-expense', csrf_exempt(views.search_expense), name="search-expense"),
]
