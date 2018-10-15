from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from User.form import RegistrationForm, EditProfileForm
from django.shortcuts import render, redirect
from Game.models import Wallet
from django.contrib.auth.models import User


def signup(request):
    if request.user.is_authenticated:
        return redirect('/game/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # asign a wallet
            new_user = User.objects.get(username=username)
            wallet = Wallet(user=new_user)
            wallet.save()
            # authenticate
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'registration/signedup.html')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})


def view_profile(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        return render(request, 'accounts/profile.html')


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('/user/profile/password')
            else:
                messages.warning(request, 'Please correct the error above.')
                form = PasswordChangeForm(request.user)
                args = {'form': form}
                return render(request, 'accounts/change_password.html', args)

        else:
            form = PasswordChangeForm(request.user)
            args = {'form': form}
            return render(request, 'accounts/change_password.html', args)


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        old_user = request.user
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid(request.user):
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('/user/profile')
            else:
                args = {'email': old_user.email,
                        'first': old_user.first_name,
                        'last': old_user.last_name,
                        'image': old_user.image,
                        'form': form}
                return render(request, 'accounts/edit_profile.html', args)
        else:
            form = EditProfileForm(instance=request.user)
            args = {'email': old_user.email,
                    'first': old_user.first_name,
                    'last': old_user.last_name,
                    'form': form}
            return render(request, 'accounts/edit_profile.html', args)

def change_avatar(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid(request.user):
                form.clean_avatar()
                form.save()
                messages.success(request, 'Your profile avatar was successfully updated')
                return redirect('/user/profile')
            else:
                args = {'form': form}
                return render(request, 'accounts/edit_avatar.html', args)
        else:
            form = EditProfileForm(request.POST, instance=request.user)
            args = {'form': form}
            return render(request, 'accounts/edit_avatar.html', args)