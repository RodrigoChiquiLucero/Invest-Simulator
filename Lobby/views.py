from django.shortcuts import render, redirect


def lobby(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        return render(request, 'Lobby/lobby.html')
