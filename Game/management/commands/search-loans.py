from django.core.management.base import BaseCommand, CommandError
import threading
import sys
from django.core.mail import send_mail
from datetime import datetime as dt
from datetime import timedelta
from Game.models import Loan, Notification


class Command(BaseCommand):
    help = 'Periodic check for loans'

    def __init__(self):
        super().__init__()
        self.event = threading.Event()
        self.SEPARATOR = '--------------------- LOANS ---------------------\n'
        self.message = ''

    def print_success(self):
        self.stdout.write(
            self.style.SUCCESS(
                self.SEPARATOR + self.message + '\n' + self.SEPARATOR))
        self.message = ''

    def handle(self, *args, **options):
        try:
            self.search_for_loans()
        except KeyboardInterrupt:
            sys.exit()

    def search_for_loans(self):
        while True:
            self.message += 'Searching for unpayed loans \n'
            today = dt.now()
            tomorrow = today + timedelta(days=1)

            expired = Loan.objects.filter(due_date=today)
            almost = Loan.objects.filter(due_date=tomorrow)

            self.charge(expired)
            self.notify(almost)

            self.print_success()
            self.event.wait(24 * 60 * 60)

    def charge(self, expired):
        for lo in expired:
            self.message += 'Expired: ' + lo.borrower.user.username
            # try to charge, or eliminate user
            if not lo.charge_borrower():
                lo.borrower.delete_for_loan()

    def notify(self, almost):
        self.message += 'Almost expired: '
        for lo in almost:
            self.message += 'Almost: ' + lo.borrower.user.username
            notif = Notification(wallet=lo.borrower,
                                 message_short=
                                 "You have a pending loan which dues tomorrow",
                                 message_large=
                                 "You have borrowed " + str(lo.loaned) +
                                 " from " +
                                 lo.offer.lender.user.username + ", if you " +
                                 "don't pay by this time tomorrow you will " +
                                 "be banned")
            notif.save()
