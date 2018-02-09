from Bot.main import start_bot
from Controller.controller import Controller
c = Controller()
#start_bot(c)
c.add_book("Book1","Book1","Carlsen",1,1000,0)
can_get_1 = c.check_out_book(190863023,1)
can_get_2 = c.check_out_book(204458156,1)
print("Can get 1 :" + str(can_get_1))
print("Can get 2 :" + str(can_get_2))