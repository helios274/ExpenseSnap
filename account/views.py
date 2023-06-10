from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
import json

class RegistrationView(View):
    def get(self, request):
        return render(request, "account/register.html")

    def post(self, request):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if (len(username) < 6 or len(username) > 15):
            messages.error(request, "Username length is not within the limits")
            return render(request, 'account/register.html')
        if not (username.isalnum() and not username.isalpha() and not username.isdigit()):
            messages.error(request, "Username is not alphanumerical")
            return render(request, 'account/register.html')
        if (len(password) < 6) or (len(password) > 25):
            messages.error(request, "Password must be 6 to 25 characters long")
            return render(request, 'account/register.html')
        if (not (password.isalnum() and not password.isalpha() and not password.isdigit())):
            messages.error(request, "Password is not alphanumerical")
            return render(request, 'account/register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'account/register.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('/')

class LoginView(View):
    def get(self, request):
        return render(request, "account/login.html")
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'Welcome back, ' + username)
                return redirect('/')
        else:
            messages.error(request, 'Invalid credentials, try again')
            return redirect('login')
        
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('/')
    
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "account/login-error.html")
        return render(request, "account/profile.html")
    
    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, "account/login-error.html")   
        username  = request.POST["username"]
        first_name  = request.POST["first_name"]
        last_name  = request.POST["last_name"]
        if (len(username) < 6 or len(username) > 15):
            messages.error(request, "Username should be 6 to 15 characters long")
            return render(request, 'account/profile.html')
        if not (username.isalnum() and not username.isalpha() and not username.isdigit()):
            messages.error(request, "Username is not alphanumerical")
            return render(request, 'account/profile.html')
        user = User.objects.get(id=request.user.id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, "Profile has been updated successfully")
        return redirect("profile")
    

class DeleteAccountView(View):
    def post(self, request):
        password = request.POST['password']
        user = User.objects.get(id=request.user.id)
        if user.check_password(password):
            user.delete()
            messages.success(request, "Account has been deleted successfully")
            return redirect('/')
        else:
            messages.error(request, "Wrong password entered")
            return redirect("profile")