from django.core.management.base import BaseCommand, CommandError
import threading
import sys
from Game.models import Alarm
from Game.interface_control import AssetComunication as Acom


class Command(BaseCommand):
    help = 'Periodic check for triggered alarms'

    def __init__(self):
        super().__init__()
        self.event = threading.Event()
        self.SEPARATOR = '--------------------- ALARM ---------------------\n'
        self.message = ''

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
                self.trigger(a)
            self.event.wait(10)
            self.print_success()

    def trigger(self, alarm):
        if alarm.trigger():
            self.message += ('Alarm triggered for: ' + alarm.asset.name +
                            '  with threshold: ' + str(alarm.threshold) +
                            '  and type: ' + alarm.type + '\n')

