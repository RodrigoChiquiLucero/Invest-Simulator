from django.shortcuts import render, redirect
import Game.interface_control as interface_control
from Game.models import Wallet


def game(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        return render(request, 'Game/game.html')


def assets(request):
    if not request.user.is_authenticated:
        return redirect('/user/login')
    else:
        asset_list = interface_control.get_assets()
        context = {'assets': asset_list}
        return render(request, 'Game/assets.html', context)


def wallet(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/user/login')
    else:
        wallet_info = Wallet.get_info(user)
        return render(request, 'Game/wallet.html', wallet_info)
