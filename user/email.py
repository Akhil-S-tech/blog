from .utils import encode_uid
from .tokens import email_verification_token


def send_email_verification(user):
    uid = encode_uid(user.id)
    token = email_verification_token.make_token(user)

    file_name = "token.txt"
    file = open(file_name, "w")
    file.write(f"UID = {uid}\n")
    file.write(f"TOKEN = {token}\n")
    file.close()


def email_verification_success(user):
    print(f"Email verificaion succes", user.email)
