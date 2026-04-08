import secrets
import string


def generate_otp_code(l=5):
    char = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(char) for _ in range(l))
