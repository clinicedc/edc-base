import random

safe_allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'


def get_safe_random_string(self, length=12, safe=None, allowed_chars=None):
    safe = True if safe is None else safe
    allowed_chars = (allowed_chars or
                     'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ012346789!@#%^&*()?<>.,[]{}')
    if safe:
        allowed_chars = 'ABCDEFGHKMNPRTUVWXYZ2346789'
    return ''.join([random.choice(allowed_chars) for _ in range(length)])
