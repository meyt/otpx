from otpx.constants import TOTP_SECRET_PATTERN


def validate_totp_secret(v):
    return TOTP_SECRET_PATTERN.match(v)
