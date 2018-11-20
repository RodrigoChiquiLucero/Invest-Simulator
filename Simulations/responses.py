from django.http import JsonResponse, HttpResponse
from Game.interface_control import str_to_date
import datetime


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
            },
        ]
    }
    return JsonResponse(response_data)


quotes = {
    "DOLAR":
        {
            "sell": 500,
            "buy": 400
        },
    "ADIDAS":
        {
            "sell": 900,
            "buy": 90
        },
    "LXA":
        {
            "sell": 40000,
            "buy": 22323
        },
    "MARSHALL":
        {
            "sell": 2,
            "buy": 1000
        }
}


def get_asset_marketprice(request, name):
    try:
        res = quotes[name]
        return JsonResponse(res)
    except KeyError:
        return HttpResponse(status=404, reason='No asset found for name')


history = {
    "DOLAR":
        {
            "prices": [
                {"day": "2018-09-08", "buy": "2.01", "sell": "3.02"},
                {"day": "2018-09-09", "buy": "3.01", "sell": "3.01"},
                {"day": "2018-09-10", "buy": "2.05", "sell": "4.00"},
                {"day": "2018-09-11", "buy": "2.35", "sell": "4.30"},
                {"day": "2018-09-12", "buy": "2.45", "sell": "3.30"},
                {"day": "2018-09-13", "buy": "2.55", "sell": "5.30"},
                {"day": "2018-09-14", "buy": "3.55", "sell": "5.32"},
                {"day": "2018-09-15", "buy": "4.55", "sell": "2.32"},
            ]
        },
    "ADIDAS":
        {
            "prices": [
                {"day": "2018-09-08", "buy": "2.01", "sell": "3.02"},
                {"day": "2018-09-09", "buy": "3.01", "sell": "3.01"},
                {"day": "2018-09-10", "buy": "2.05", "sell": "4.00"},
                {"day": "2018-09-11", "buy": "2.35", "sell": "4.30"},
                {"day": "2018-09-12", "buy": "2.45", "sell": "3.30"},
                {"day": "2018-09-13", "buy": "2.55", "sell": "5.30"},
                {"day": "2018-09-14", "buy": "3.55", "sell": "5.32"},
                {"day": "2018-09-15", "buy": "4.55", "sell": "2.32"},
            ]
        },
    "LXA":
        {
            "prices": [
                {"day": "2018-09-08", "buy": "2.01", "sell": "3.02"},
                {"day": "2018-09-09", "buy": "3.01", "sell": "3.01"},
                {"day": "2018-09-10", "buy": "2.05", "sell": "4.00"},
                {"day": "2018-09-11", "buy": "2.35", "sell": "4.30"},
                {"day": "2018-09-12", "buy": "2.45", "sell": "3.30"},
                {"day": "2018-09-13", "buy": "2.55", "sell": "5.30"},
                {"day": "2018-09-14", "buy": "3.55", "sell": "5.32"},
                {"day": "2018-09-15", "buy": "4.55", "sell": "2.32"},
            ]
        },
    "MARSHALL":
        {
            "prices": [
                {"day": "2018-09-08", "buy": "2.01", "sell": "3.02"},
                {"day": "2018-09-09", "buy": "3.01", "sell": "3.01"},
                {"day": "2018-09-10", "buy": "2.05", "sell": "4.00"},
                {"day": "2018-09-11", "buy": "2.35", "sell": "4.30"},
                {"day": "2018-09-12", "buy": "2.45", "sell": "3.30"},
                {"day": "2018-09-13", "buy": "2.55", "sell": "5.30"},
                {"day": "2018-09-14", "buy": "3.55", "sell": "5.32"},
                {"day": "2018-09-15", "buy": "4.55", "sell": "2.32"},
            ]
        },
}


def get_asset_history(request, name, start_date, end_date):
    try:
        start_date = str_to_date(start_date)
        end_date = str_to_date(end_date)
        dates = [start_date + datetime.timedelta(days=x) for x in
                 range(0, (end_date - start_date).days)]

        prices = history[name]["prices"]
        prices = [p for p in prices if str_to_date(p["day"]) in dates]

        return JsonResponse({"prices": prices})
    except KeyError:
        return HttpResponse(status=404, reason='No asset found for name')
