from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from User.form import RegistrationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.user.is_authenticated:
        return redirect('/game/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            render(request, 'registration/signup.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

def view_profile(request):
    return render(request, 'accounts/profile.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/user/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your user data was successfully updated!')
            return redirect('/user/profile')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = UserChangeForm(request.user)
        args = {'from': form}
        return render(request, 'accounts/edit_profile.html', args)