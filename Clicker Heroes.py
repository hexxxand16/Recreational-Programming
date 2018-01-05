import math
from decimal import Decimal


def mob_hp(zone, boss=False):
    hp = Decimal(10)
    if zone <= 140:
        hp *= Decimal(zone - 1 + 1.55**(zone - 1))
    elif zone <= 500:
        hp *= Decimal(139 + 1.55**139 * 1.145**(zone - 140))
    elif zone <= 200000:
        hp *= Decimal(139 + 1.55**139 * 1.145**360)
        for i in range(501, zone, 1):
            hp *= Decimal(1.145 + 0.001 * math.floor((i - 1) / 500))

    if boss:
        hp *= 10

    return hp


print(mob_hp(12000, True))