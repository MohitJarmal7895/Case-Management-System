from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from .forms import UserSignUpForm, AdminSignUpForm

def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('dashboard')
    else:
        form = AdminSignUpForm()
    return render(request, 'registration/admin_signup.html', {'form': form})
