from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('/game/')
    else:
        return render(request, 'Home/home.html')
