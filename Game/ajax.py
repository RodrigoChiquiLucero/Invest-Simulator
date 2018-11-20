from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from Game.interface_control import AssetComunication as ACommunication
from Game.models import Asset, Wallet, Notification


# AJAX JSON RESPONSES
@login_required
def ajax_quote(request, name):
    """
    returns the quote for an asset given the name
    :rtype: JsonResponse or HttpResponse
    """
    asset_comunication = ACommunication(settings.API_URL)
    asset = asset_comunication.get_asset_quote(Asset(name=name))
    if asset.buy != -1 and asset.sell != -1:
        return JsonResponse(asset.to_dict())
    else:
        return HttpResponse(status=403, reason="No asset quote")


@login_required
def ajax_buy(request):
    """
    given an asset name and type,
    buys the wallet for the user that makes the request.
    Error handling specified in Wallet.buy_asset
    :rtype: JsonResponse or HttpResponse
    """
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
    """
    given an asset name and type,
    sells the wallet for the user that makes the request.
    Error handling specified in Wallet.sell_asset
    :rtype: JsonResponse or HttpResponse
    """
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


def notify(request):
    """
    Searchs notifications for a given user
    :rtype: JsonResponse
    """
    wallet = Wallet.objects.get(user=request.user)
    return JsonResponse(Notification.notifity(wallet))
