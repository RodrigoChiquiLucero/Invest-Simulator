from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from User.form import RegistrationForm, EditProfileForm, AvatarForm
from django.shortcuts import render, redirect
from Game.models import Wallet


def signup(request):
    if request.user.is_authenticated:
        return redirect('/game/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
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
        wallet = Wallet.objects.get(user=request.user)
        context = {'image_url': wallet.image.url}
        return render(request, 'accounts/profile.html', context)


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                return render(request, 'accounts/change_succesfull.html')
            else:
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
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your profile was successfully updated!')
                return render(request, 'accounts/change_succesfull.html')
            else:
                args = {'email': old_user.email,
                        'first': old_user.first_name,
                        'last': old_user.last_name,
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
        wallet = Wallet.objects.get(user=request.user)
        context = {'avatar_url': wallet.image.url}
        if request.method == 'POST':
            form = AvatarForm(request.POST, request.FILES)
            form.set_user(request.user)
            if form.is_valid():
                form.save()
                return redirect('/user/profile')
            context['form'] = form
            return render(request, 'accounts/change_avatar.html', context)
        else:
            return render(request, 'accounts/change_avatar.html', context)
