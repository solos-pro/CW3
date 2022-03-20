import base64
import hashlib
import hmac

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, PWD_HASH_ALGO, SECRET
from flask import current_app


def get_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name=PWD_HASH_ALGO,
        password=password.encode("utf-8"),
        salt=PWD_HASH_SALT,
        iterations=PWD_HASH_ITERATIONS
    )


def get_password_hash(password: str) -> str:
    return base64.b64encode(get_password_digest(password)).decode('utf-8', "ignore")

def compare_passwords(password_hash, other_password):
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        get_password_digest(other_password)
    )


'''
# ------------------------- test ------------------------- #
passW = 'f8fsa65'
hash_passw_digest = get_password_digest(passW)          # create a HASH from a password in a string
print(hash_passw_digest)

hash_passw_digest_str = get_password_hash(passW)        # create a HASH from a password in a bites (for bd)
print(hash_passw_digest_str)

print(base64.b64decode(hash_passw_digest_str))

print(compare_passwords(hash_passw_digest_str, passW))

exit()
'''