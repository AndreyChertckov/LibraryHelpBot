import random


def key_gen():
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    key = ""
    for i in range(32):
        key += symbols[random.randint(0, len(symbols)-1)]
    open("Bot/key.txt", 'w').write(key)
    return key

key_gen()