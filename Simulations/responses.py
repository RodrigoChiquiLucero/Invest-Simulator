from django.http import JsonResponse, HttpResponse


def get_available_assets(request):
    response_data = {
        "availableAssets": [
            {
                "name": "DOLAR",
                "type": "currency"
            },
            {
                "name": "ADIDAS",
                "type": "stock"
            },
            {
                "name": "LXA",
                "type": "stock",
            },
            {
                "name": "MARSHALL",
                "type": "currency",
            }
        ]
    }
    return JsonResponse(response_data)


quotes = {
    "DOLAR":
        {
            "sell": 23,
            "buy": 54
        },
    "ADIDAS":
        {
            "sell": 65,
            "buy": 90
        },
    "LXA":
        {
            "sell": 43,
            "buy": 230
        },
    "MARSHALL":
        {
            "sell": 232,
            "buy": 4669
        }
}


def get_asset_marketprice(request, name):
    try:
        res = quotes[name]
        return JsonResponse(res)
    except KeyError:
        return HttpResponse(status=404, reason='No asset found for name')

# TODO: get_asset_history
