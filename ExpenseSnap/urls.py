from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('expense/', include('expense.urls')),
    path('income/', include('income.urls'))
]

handler404 = 'home.views.handler404'
