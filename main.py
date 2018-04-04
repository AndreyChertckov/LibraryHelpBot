import getopt
import os
import sys
import threading

from Bot.bot import start_bot
from Controller.controller import Controller
from AdminSite.site import Main 


def main():
    file_log = 'controller.log'
    file_db = 'DataBase.db'
    lc = False
    lf = False
    cleanup_database = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h:s:t:c', ['log_file=', 'database=','cleanup_database'])
    except getopt.GetoptError:
        print('main.py -t -c --log_file=<filelog> --database=<filedb>')
        sys.exit(2)
    for opt, arg in opts:
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
        elif opt == '--cleanup_database':
            cleanup_database = True
    c = Controller(file_db, lc, lf, file_log)
    LibraryBot = start_bot(c)
    site = Main(c,LibraryBot.get_bot())
    if cleanup_database:
        site.api.dbmanager.cleanup_database()
        site.api.dbmanager.init_tables()
    thread_site = threading.Thread(target=site.run)
    thread_site.start()
    LibraryBot.run()
    


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
