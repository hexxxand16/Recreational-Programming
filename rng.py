import random
import csv

enemy = [2, 2, 2]
"""
For list of length two with both numbers x being the same, the number of 
combinations is sum from i = 1 to x, (i+x)C(i)
"""
result = []
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
random.seed()
count = 0
while count < 10000:
    hp = list(enemy)
    x = ""
    while all(i > 0 for i in hp):
        rng = random.randint(0, len(enemy) - 1)    
        hp[rng] -= 1
        x.append(alph[rng])

    if x not in result:
        count = 0
        result.append(x)
    else:
        count += 1

print(len(result))




def binomial(n, k):
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

