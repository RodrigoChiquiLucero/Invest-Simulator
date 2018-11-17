from django.core.mail import send_mail
from django.contrib.auth.models import User
import datetime as dt


class AlarmSearch:
    help = 'Check for triggered alarms'
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, acom):
        self.message = ''
        self.acom = acom

    def print_success(self):
        print(self.message)
        self.message = ''

    def search_for_alarms(self, asset):
        from Game.models import Alarm

        alarms = Alarm.objects.filter(asset__name=asset.name)
        for a in alarms:
            self.trigger(a, asset)
        self.print_success()

    def trigger(self, alarm, asset):
        if not alarm.triggered:
            if alarm.trigger(asset):
                self.message += ('Alarm triggered for: ' + alarm.asset.name +
                                 '  with threshold: ' + str(alarm.threshold) +
                                 '  and type: ' + alarm.type + '\n')

                price = asset.__getattribute__(alarm.price)
                user = User.objects.get(wallet=alarm.wallet)
                email = user.email
                self.message += 'sending to mail: ' + email + '\n'

                alarm.triggered = True
                alarm.save()

                subject = 'Your alarm for asset ' + \
                          alarm.asset.name + ' has been triggered'

                mail_content = 'The asset ' + asset.name + \
                               ' has reached the expected value of $' + \
                               str(alarm.threshold) + ' for ' + \
                               str(alarm.type) + '\n\n' + asset.name + \
                               '\nCurrent price: $' + str(price) + \
                               '\nOld price: $' + str(alarm.old_price) + \
                               '\nDate: ' + dt.datetime.today().strftime(
                                                        self.DATE_FORMAT)

                send_mail(
                    subject,
                    mail_content,
                    'Invest Simulator Alarms',
                    [email],
                    fail_silently=False,
                )
                print("Mail sent successfully")
        else:
            alarm.reactivate(asset)
