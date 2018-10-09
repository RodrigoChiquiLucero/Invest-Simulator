from django.contrib.auth import login, authenticate
from User.form import RegistrationForm
from django.shortcuts import render, redirect


def signup(request):
    if request.user.is_authenticated:
        return redirect('/lobby/')
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