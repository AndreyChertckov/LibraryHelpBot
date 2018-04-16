import hashlib
import random
import base64


def generate_sault():
    sault = bytes([random.randint(0, 16) for i in range(16)])
    return base64.b64encode(sault)


def create_session(login, passwd, dbmanager):
    hasher = hashlib.md5()
    hasher.update(
        (login + str(passwd) + str(generate_sault())).encode('utf-8'))
    user_id = dbmanager.get_user_id(login, passwd)[0]
    dbmanager.create_session(hasher.hexdigest(), user_id)
    return hasher.hexdigest()


def check_session(session_id, dbmanager):
    return dbmanager.get_user_id_by_session(session_id) != None


def md5_hash(bytes_):
    hasher = hashlib.md5()
    hasher.update(bytes_)
    return hasher.hexdigest()


def check_privilege(session_id,privilege_val, dbmanager):
    user_id = dbmanager.get_user_id_by_session(session_id)[0]
    print(privilege_val,dbmanager.get_privilege_by_user_id(user_id)[0])
    return privilege_val <= dbmanager.get_privilege_by_user_id(user_id)[0]