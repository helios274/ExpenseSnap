from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ProfileView, DeleteAccountView

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('profile', ProfileView.as_view(), name="profile"),
    path('delete-account', DeleteAccountView.as_view(), name="delete-account"),
]
