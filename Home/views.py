from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect('/lobby/')
    else:
        return render(request, 'Home/home.html')
