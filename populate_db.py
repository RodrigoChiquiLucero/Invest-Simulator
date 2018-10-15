import os
import sys


def create_ownerships(username):
    # crear assets
    a1 = Asset(name="MARSHALL", type="currency")
    a2 = Asset(name="ADIDAS", type="stock")
    a1.save()
    a2.save()

    # tomar usuario y wallet
    user = User.objects.get(username=username)
    wallet = Wallet.objects.get(user=user)

    # crear transacciones
    ownership_1 = Ownership(asset=a1, wallet=wallet, quantity=2)
    ownership_2 = Ownership(asset=a2, wallet=wallet, quantity=5)
    ownership_1.save()
    ownership_2.save()


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
        create_ownerships(username)
    except IntegrityError:
        pass
