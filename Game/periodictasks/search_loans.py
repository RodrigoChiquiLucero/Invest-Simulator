from datetime import datetime as dt
from datetime import timedelta, datetime
from Game.models import Loan, Notification


class LoanSearch:
    help = 'Periodic check for loans'

    def __init__(self):
        super().__init__()
        self.BEGIN = \
            '--------------------- LOAN SEARCH ---------------------\n\n' + \
            '-----------    ' + str(datetime.today()) + '   -----------\n'
        self.END = \
            '------------------- END LOAN SEARCH -------------------\n'
        self.message = ''

    def print_success(self):
        with open('/tmp/invest_simulator.logs', 'a+') as f:
            f.write(self.BEGIN + self.message + '\n' + self.END)
            self.message = ''

    def do(self):
        self.message += 'Searching for unpayed loans \n'
        today = dt.now()
        tomorrow = today + timedelta(days=1)

        expired = Loan.objects.filter(due_date=today)
        almost = Loan.objects.filter(due_date=tomorrow)

        self.charge(expired)
        self.notify(almost)

        self.print_success()

    def charge(self, expired):
        self.message += \
            '-------------------    EXPIRED    -------------------\n'
        for lo in expired:
            self.message += '------------------\n'
            # try to charge, or eliminate user
            if not lo.charge_borrower():
                self.message += 'USER DELETED :: ' + lo.borrower.user.username
                self.message += '\n'
                lo.borrower.delete_for_loan()
            else:
                self.message += 'USER CHARGED :: ' + lo.borrower.user.username
                self.message += '\n'

    def notify(self, almost):
        self.message += \
            '------------------  ALMOST EXPIRED  ------------------\n'
        for lo in almost:
            self.message += 'NOTIFIED :: ' + lo.borrower.user.username
            self.message += '\n'
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


def search_loans():
    loan_search = LoanSearch()
    loan_search.do()
