from django.shortcuts import render, redirect
import Game.interface_control as interface_control


def game(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        assets = interface_control.get_assets()
        context = {'assets': assets}

        return render(request, 'Game/game.html', context)
