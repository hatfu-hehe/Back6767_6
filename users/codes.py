import random
from django.core.cache import cache


def save_code(user_id):
    code = str(random.randint(100000, 999999))
    key = "confirm_code_" + str(user_id)
    cache.set(key, code, 300) 
    return code


def check_code(user_id, code):
    key = "confirm_code_" + str(user_id)
    saved_code = cache.get(key)
    if saved_code == code:
        cache.delete(key)  
        return True
    return False