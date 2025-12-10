import hashlib
from typing import Optional


def mask_id(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    v = str(value)
    if len(v) <= 4:
        return "*" * len(v)
    return "*" * (len(v) - 4) + v[-4:]


def mask_email(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        user, domain = value.split("@", 1)
    except Exception:
        return "***"
    if len(user) <= 2:
        user_mask = "*" * len(user)
    else:
        user_mask = user[0] + "*" * (len(user) - 2) + user[-1]
    return f"{user_mask}@{domain}"


def mask_phone(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    v = str(value)
    if len(v) <= 3:
        return "*" * len(v)
    return "*" * (len(v) - 3) + v[-3:]


def hash_value(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()
