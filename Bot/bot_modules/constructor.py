from Bot.bot_modules.registration_module import Reg_module
from Bot.bot_modules.user_module import User_module
from Bot.bot_modules.material_module import Material_module

classes = [Reg_module, User_module, Material_module]


def construct(cl):
    for mod in classes:
        attrs = [i for i in dir(mod) if i[0] != '_']
        for attr in attrs:
            setattr(cl, attr, getattr(mod, attr))
