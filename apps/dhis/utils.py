import random
from .models import DHIS2User


CHARACTERS = "abcdefghijkmnpqrtuvwxyz2345689"
LENGTH = 6


def generate_passcode():
    password = ""
    for i in range(LENGTH):
        password += random.choice(CHARACTERS)
    return password


def unique_passcode():
    passcode = generate_passcode()
    user = DHIS2User.objects.get_or_none(passcode=passcode)
    n = 593775  # combination - 𝐶(30,6) 30 unique characters and passcode length is 6
    i = 0
    while i <= n and user is not None:
        i += 1
        passcode = generate_passcode()
        user = DHIS2User.objects.get_or_none(passcode=passcode)
    if i > n:
        return "No unique passcode"
    return passcode
