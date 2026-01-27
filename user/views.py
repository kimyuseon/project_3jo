from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import UserProfile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


def SignUp_view(request): #회원가입 기능
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'user/signup.html', {'form':form})


def login_view(request): #로그인 기능
    if request.method == 'POST':
        u_id = request.POST.get('username')
        u_pw = request.POST.get('password')
        user = authenticate(request, username=u_id, password=u_pw)
        if user is not None:
            auth_login(request, user)
            return redirect('index') 
        else:
            return render(request, 'community/login.html', {'error': '로그인 실패'})
    else:
        return render(request, 'community/login.html')
    

def logout_view(request): #로그아웃 기능
    auth_logout(request)
    return redirect('index') 

def main_index(request):
    return render(request, 'index.html')