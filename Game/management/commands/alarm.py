from django.core.management.base import BaseCommand, CommandError
import threading
import sys
from Game.models import Alarm
from Game.interface_control import AssetComunication as Acom


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def __init__(self):
        super().__init__()
        self.event = threading.Event()

    def handle(self, *args, **options):
        try:
            self.search_for_alarms()
        except KeyboardInterrupt:
            sys.exit()

    def search_for_alarms(self):
        while True:
            self.stdout.write(
                self.style.SUCCESS('Searching for alarms to trigger'))

            alarms = Alarm.objects.all()
            for a in alarms:
                self.trigger(a)
            self.event.wait(30)

    def trigger(self, alarm):
        self.stdout.write(self.style.SUCCESS(alarm.asset.name))
