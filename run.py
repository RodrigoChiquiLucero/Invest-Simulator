# Python3

# ESSENTIALS
from subprocess import Popen
import traceback


class Run:
    # COMMANDS
    MANAGE = ['python', 'manage.py']
    RUNSERVER = MANAGE + ['runserver']
    CRONTAB = MANAGE + ['crontab']
    CRONTAB_RUN = CRONTAB + ['add']
    CRONTAB_RM = CRONTAB + ['remove']

    def __init__(self):
        self.runserver = Popen(self.RUNSERVER, stdin=None)
        self.crontab_run = Popen(self.CRONTAB_RUN, stdin=None)

    def run(self):
        self.runserver.wait()
        self.crontab_run.wait()

    def kill(self):
        self.runserver.kill()
        crontab_rm = Popen(self.CRONTAB_RM, stdin=None)
        crontab_rm.wait()
        print("You killed all jobs")


if __name__ == '__main__':
    run = Run()
    try:
        run.run()
    except KeyboardInterrupt:
        run.kill()
    except:
        traceback.print_exc()
        run.kill()
