from django.shortcuts import render, redirect
from Game.interface_control import AssetComunication as ACommunication
from Game.models import Wallet
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required
def loggedin(request):
    return render(request, 'Game/loggedin.html')


@login_required
def game(request):
    return render(request, 'Game/game.html')


@login_required
def assets(request):
    asset_comunication = ACommunication(settings.API_URL)
    asset_list = asset_comunication.get_assets()
    context = {'assets': asset_list}
    return render(request, 'Game/assets.html', context)


@login_required
def wallet(request):
    user = request.user
    wallet_info = Wallet.get_info(user)
    return render(request, 'Game/wallet.html', wallet_info)
