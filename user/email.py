from .utils import encode_uid
from .tokens import email_verification_token


def send_email_verification(user):
    uid = encode_uid(user.id)
    token = email_verification_token.make_token(user)

    print("uid", uid)
    print("token", token)
