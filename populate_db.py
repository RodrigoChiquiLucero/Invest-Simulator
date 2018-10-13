import os
import sys


def create_transactions(username):
    # crear assets
    a1 = Asset(name="MARSHALL", type="currency")
    a2 = Asset(name="ADIDAS", type="stock")
    a1.save()
    a2.save()

    # tomar usuario y wallet
    user = User.objects.filter(username=username)[0]
    wallet = Wallet.objects.filter(user=user)[0]

    # crear transacciones
    transaction_1 = Transaction(asset=a1, wallet=wallet, quantity=2, asset_price=23, is_purchase=True)
    transaction_2 = Transaction(asset=a2, wallet=wallet, quantity=5, asset_price=46, is_purchase=True)
    transaction_1.save()
    transaction_2.save()


if __name__ == '__main__':
    print('\n' + ('=' * 80) + '\n')
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'InvestSimulator.settings')
    django.setup()
    from Game.models import *
    from django.contrib.auth.models import User
    from django.db import IntegrityError

    try:
        username = sys.argv[1]
        print(username)
        create_transactions(username)
    except IntegrityError:
        pass
