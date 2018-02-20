from Bot.main import start_bot
from Controller.controller import Controller
import sys, getopt

def main():
    file_log = 'controller.log'
    file_db = 'Database.db'
    lc = False
    lf = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],'h',['log_console','log_file=','database='])
    except getopt.GetoptError:
        print('main.py --log_console --log_file=<filelog> --database=<filedb>')
        sys.exit(2)
    print(opts)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py --log_console --log_file=<filelog> --database=<filedb>')
            sys.exit()
        elif opt == "--log_console":
            lc = True
        elif opt == "--log_file":
            if arg == '':
                print('main.py --log_console --log_file=<filelog> --database=<filedb>')
                sys.exit()
            lf = True
            file_log = arg
        elif opt == '--database':
            file_db = arg
    c = Controller(file_db,lc,lf,file_log)
    start_bot(c)


if __name__ == '__main__':
    main()