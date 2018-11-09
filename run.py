# Python3

# ESSENTIALS
from subprocess import Popen, PIPE

# COMMANDS
MANAGE = ['python', 'manage.py']
RUNSERVER = MANAGE + ['runserver']
SEARCH_ALARMS = MANAGE + ['search-alarms']
SEARCH_LOANS = MANAGE + ['search-loans']


def run_both():
    runserver = Popen(RUNSERVER, stdin=None)
    search_alarms = Popen(SEARCH_ALARMS, stdin=None)
    search_loans = Popen(SEARCH_LOANS, stdin=None)

    runserver.wait()
    search_alarms.wait()
    search_loans.wait()


if __name__ == '__main__':
    try:
        run_both()
    except KeyboardInterrupt:
        print("You killed all programs")
