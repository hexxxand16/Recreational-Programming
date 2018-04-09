import itertools
import csv

values = [6, 5, 4, 3, 2, 1]
hands = ["Triple", "Run+Flush", "Run", "Flush", "Pair", "High"]
hands = list(itertools.combinations_with_replacement(hands, 3))
hands2 = list(itertools.combinations_with_replacement(values, 3))
with open("Nines Hands.csv", "w", newline='') as f:
    temp = []
    for i in range(len(hands)):
        temp2 = []
        temp2.append(str(hands[i][0] + ", " + hands[i][1] + ", " + hands[i][2]))
        temp2.append(str(str(hands2[i][0]) + "," + str(hands2[i][1]) + "," + str(hands2[i][2])))
        temp.append(temp2)
    wr = csv.writer(f, delimiter=",")
    for i in temp:
        wr.writerow(i)

"""
hands = list(itertools.combinations_with_replacement(values, 3))

results = []
for i in range(len(hands)):
    matchup = []
    for j in range(len(hands)):
        score = 0
        for k in range(3):
            if hands[i][k] > hands[j][k]:
                score += 1
            elif hands[i][k] == hands[j][k]:
                score += 0.5
        matchup.append(score)
    results.append(matchup)

with open("Results.csv", "w") as f:
    wr = csv.writer(f, delimiter="\n")
    wr.writerow(results)
"""
