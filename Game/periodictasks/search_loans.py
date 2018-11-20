from datetime import datetime as dt
from datetime import timedelta, datetime
from Game.models import Loan, Notification


class LoanSearch:
    """
    Searchs and operates on taken Loans,
    this project has a cron job scheduled to run everyday at 00:00,
    to run this cron job execute:
        python manage.py crontab add
    on your command line.
    This class also creates logs that will be stored in
        /tmp/invest_simulator.logs
    """
    help = 'Periodic check for loans'
    logfile = '/tmp/invest_simulator.logs'

    def __init__(self):
        super().__init__()
        self.BEGIN = \
            '--------------------- LOAN SEARCH ---------------------\n\n' + \
            '-----------    ' + str(datetime.today()) + '   -----------\n'
        self.END = \
            '------------------- END LOAN SEARCH -------------------\n'
        self.message = ''

    def log_success(self):
        """
        Writes message to the logfile
        :rtype: None
        """
        with open(self.logfile, 'a+') as f:
            f.write(self.BEGIN + self.message + '\n' + self.END)
            self.message = ''

    def do(self):
        """
        Search for all the taken Loans that expires today or tomorrow,
        for today -> charge
        for tomorrow -> notify
        :rtype: None
        """
        self.message += 'Searching for unpayed loans \n'
        today = dt.now()
        tomorrow = today + timedelta(days=1)

        expired = Loan.objects.filter(due_date=today)
        almost = Loan.objects.filter(due_date=tomorrow)

        self.charge(expired)
        self.notify(almost)

        self.log_success()

    def charge(self, expired):
        """
        Takes a list of taken Loans and tries to charge all of them.
        If any of the borrowers doesn't have the enough money to pay,
        it will be eliminated from the game.
        :rtype: None
        """
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
        """
        Takes a list of taken Loans that expire tomorrow and saves a
        notification for each of them
        :rtype: None
        """
        self.message += \
            '------------------  ALMOST EXPIRED  ------------------\n'
        for lo in almost:
            self.message += 'NOTIFIED :: ' + lo.borrower.user.username
            self.message += '\n'
            notif = Notification(wallet=lo.borrower,
                                 message_short="You have a pending"
                                               " loan which dues tomorrow",
                                 message_large="You have borrowed " +
                                               str(lo.loaned) + " from " +
                                 lo.offer.lender.user.username + ", if you " +
                                 "don't pay by this time tomorrow you will " +
                                 "be banned")
            notif.save()


def search_loans():
    loan_search = LoanSearch()
    loan_search.do()
