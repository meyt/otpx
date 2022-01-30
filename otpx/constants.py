import re

TOTP_SECRET_PATTERN = re.compile(r"^([A-Z]|[2-7]+)+$")
