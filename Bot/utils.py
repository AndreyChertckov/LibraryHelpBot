import random


def key_gen():
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    key = ""
    for i in range(30):
        key += symbols[random.randint(0, len(symbols))]
    open("key.txt", 'w').write(key)
    return key