from django.shortcuts import render, redirect
from Game.interface_control import AssetComunication as ACommunication
from Game.models import Wallet
from django.contrib.auth.decorators import login_required
from django.conf import settings
from Game.models import Transaction, Asset
from django.http import JsonResponse, HttpResponse


@login_required
def loggedin(request):
    return render(request, 'Game/loggedin.html')


@login_required
def game(request):
    return render(request, 'Game/game.html')


@login_required
def assets(request):
    asset_comunication = ACommunication(settings.API_URL)
    asset_list = [a.to_dict() for a in asset_comunication.get_assets()]
    context = {'assets': asset_list}

    # user info
    wallet = Wallet.get_info(request.user)
    context['value_wallet'] = wallet['value_wallet']
    context['liquid'] = wallet['liquid']

    if request.is_ajax():
        return JsonResponse(context)
    else:
        return render(request, 'Game/assets.html', context)


@login_required
def wallet(request):
    user = request.user
    wallet_info = Wallet.get_info(user)
    return render(request, 'Game/wallet.html', wallet_info)


@login_required
def transactions(request):
    user = request.user
    user_wallet = Wallet.objects.get(user=user)
    user_transactions = Transaction.get_info(user_wallet)
    return render(request, 'Game/transactions.html', user_transactions)


@login_required
def history(request, name):
    if request.method == 'POST':

        start = request.POST['start']
        end = request.POST['end']

        asset_comunication = ACommunication(settings.API_URL)
        prices = asset_comunication.get_asset_history(name, start, end)
        prices['name'] = name
        return render(request, 'Game/history.html', prices)
    else:
        return render(request, 'Game/select_dates.html')


@login_required
def ranking(request):
    users = []
    wallets = Wallet.objects.all()
    for w in wallets:
        users.append({'username': w.user.username,
                      'wallet': w.get_info(w.user)['value_wallet'],
                      'ranking': 1})
    users.sort(key=lambda k: k['wallet'], reverse=True)
    index = 0
    for u in users:
        index += 1
        u['ranking'] = index
    return render(request, 'Game/ranking.html', {'users': users})


@login_required
def set_alarm(request):
    if request.method == 'POST':
        if float(request.POST['threshold']) < 0:
            return HttpResponse(status=400, reason="Incorrect threshold value")
        elif not request.POST.getlist('asset'):
            return HttpResponse(status=400,
                                reason="You need to select at least one asset")
        else:
            return HttpResponse(status=200, reason="Your alarm has been set!")
    else:
        asset_comunication = ACommunication(settings.API_URL)
        asset_list = [a.to_dict() for a in asset_comunication.get_assets()]
        context = {'assets': asset_list}
        return render(request, 'Game/set_alarm.html', context)


# AJAX JSON RESPONSES
@login_required
def ajax_quote(request, name):
    asset_comunication = ACommunication(settings.API_URL)
    asset = asset_comunication.get_asset_quote(Asset(name=name))
    if asset.buy != -1 and asset.sell != -1:
        return JsonResponse(asset.to_dict())
    else:
        return HttpResponse(status=403, reason="No asset quote")


@login_required
def ajax_buy(request):
    if request.method == 'POST':
        name = request.POST['name']
        type = request.POST['type']
        quantity = float(request.POST['quantity'])
        asset = Asset(name=name, type=type)
        asset.quantity = quantity

        user = request.user
        wallet = Wallet.objects.get(user=user)

        return JsonResponse(wallet.buy_asset(asset))
    else:
        return HttpResponse(status=400, reason="No GET method")


@login_required
def ajax_sell(request):
    if request.method == 'POST':
        name = request.POST['name']
        type = request.POST['type']
        quantity = float(request.POST['quantity'])
        asset = Asset(name=name, type=type)
        asset.quantity = quantity

        user = request.user
        wallet = Wallet.objects.get(user=user)

        return JsonResponse(wallet.sell_asset(asset))
    else:
        return HttpResponse(status=400, reason="No GET method")
