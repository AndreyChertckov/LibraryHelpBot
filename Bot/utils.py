import random


def key_gen():
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    key = ""
    for i in range(32):
        key += symbols[random.randint(0, len(symbols)-1)]
    open("Bot/key.txt", 'w').write(key)
    return key


def get_key(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=key_gen())

key_gen()