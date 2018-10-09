from django.shortcuts import render, redirect


def game(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        return render(request, 'Game/game.html')
