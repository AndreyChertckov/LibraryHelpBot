import random
import re


# Generate and return random key
def key_gen():
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    key = ""
    for i in range(32):
        key += symbols[random.randint(0, len(symbols) - 1)]
    open("Bot/key.txt", 'w').write(key)
    return key


# Send the key
# params:
#  bot -- This object represents a Bot's commands
#  update -- This object represents an incoming  update

def get_key(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=key_gen())


def randint(min=0, max=2**40 - 1):
    return random.randint(min, max)


def data_checker(user):
    name = user['name']
    address = user["address"]
    phone = user['phone']
    status = user["status"]
    if (not re.findall(r'\d', name)) and len(name.split(" ")) < 2:
        return [True, 'You have to enter your full real name']
    elif False:
        return [True, 'Your address must be real and located in the Innopolis']
    elif re.findall('\+[^1234567890]', phone) or not re.findall(r'\+\d{11,11}', phone):
        return [True, 'You phone number must be correct']
    elif status != 'Student' and status != 'Faculty':
        return [True, 'You must be faculty or student']
    else:
        return [False]


def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False
