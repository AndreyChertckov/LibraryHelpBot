import getopt
import os
import sys

from Bot.bot import start_bot
from Controller.controller import Controller
from AdminSite.api import API


def main():
    file_log = 'controller.log'
    file_db = 'DataBase.db'
    lc = False
    lf = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h:s:t:c', ['log_file=', 'database='])
    except getopt.GetoptError:
        print('main.py -t -c --log_file=<filelog> --database=<filedb>')
        sys.exit(2)
    for opt, arg in opts:
        print(opt)
        if opt == '-h':
            print('main.py -t -c --log_file=<filelog> --database=<filedb>')
            sys.exit()
        elif opt == '-t':
            os.system('python -m pytest -vv Controller/test.py')
            sys.exit()
        elif opt == "-c":
            lc = True
        elif opt == "--log_file":
            if arg == '':
                print('main.py -c --log_file=<filelog> --database=<filedb>')
                sys.exit()
            lf = True
            file_log = arg
        elif opt == '--database':
            file_db = arg
    c = Controller(file_db, lc, lf, file_log)
    api = API(c)
    api.run()
    start_bot(c)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
