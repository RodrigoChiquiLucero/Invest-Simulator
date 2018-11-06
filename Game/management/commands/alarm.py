from django.core.management.base import BaseCommand, CommandError
import threading
import sys
from Game.models import Alarm
from django.core.mail import send_mail
from Game.interface_control import AssetComunication
from django.conf import settings
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Periodic check for triggered alarms'

    def __init__(self):
        super().__init__()
        self.event = threading.Event()
        self.SEPARATOR = '--------------------- ALARM ---------------------\n'
        self.message = ''
        self.acom = AssetComunication(settings.API_URL)

    def print_success(self):
        self.stdout.write(
            self.style.SUCCESS(
                self.SEPARATOR + self.message + '\n' + self.SEPARATOR))
        self.message = ''

    def handle(self, *args, **options):
        try:
            self.search_for_alarms()
        except KeyboardInterrupt:
            sys.exit()

    def search_for_alarms(self):
        while True:
            self.message += 'Searching for triggered alarms \n'

            alarms = Alarm.objects.all()
            for a in alarms:
                if not a.triggered:
                    self.trigger(a)
            self.event.wait(10)
            self.print_success()

    def trigger(self, alarm):
        if not alarm.triggered:
            if alarm.trigger():
                self.message += ('Alarm triggered for: ' + alarm.asset.name +
                                 '  with threshold: ' + str(alarm.threshold) +
                                 '  and type: ' + alarm.type + '\n')

                asset = self.acom.get_asset_quote(alarm.asset)
                price = asset.__getattribute__(alarm.price)
                user = User.objects.get(wallet=alarm.wallet)
                email = user.email
                self.message += 'sending to mail: ' + email + '\n'

                alarm.triggered = True
                alarm.save()

                send_mail(
                    'Your alarm for asset ' +
                    alarm.asset.name + ' has been triggered',

                    'The asset ' + asset.name +
                    ' has reached the expected value of $' + str(
                        alarm.threshold) +
                    '\n\n' + asset.name +
                    '\nCurrent price: $' + str(price),
                    'invest.simulator.alarms@gmail.com',
                    [email],
                    fail_silently=False,
                )
        # TODO: congelar la alarma para que no se envie cada 5 min
