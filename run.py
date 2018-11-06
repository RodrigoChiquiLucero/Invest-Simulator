#Python3

#ESSENTIALS
from subprocess import Popen, PIPE

#COMMANDS
MANAGE = ['python', 'manage.py']
RUNSERVER = MANAGE + ['runserver']
SCRIPT = MANAGE + ['alarm']


def run_both():
        runserver = Popen(RUNSERVER, stdin=None)
        script = Popen(SCRIPT, stdin=None)

        runserver.wait()
        script.wait()


if __name__ == '__main__':
    try:
        run_both()
    except KeyboardInterrupt:
        print("You killed both programs")
