from random import choice, shuffle
from itertools import product
import csv


def checkdbl(lst):
    return lst[0] == lst[1] or lst[0] == lst[2] or lst[1] == lst[2]


def game():
    position = 0
    tiles = [0] * 52
    jail = False
    dbl = 0
    turnInJail = 0
    chest = [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 4, 0, 0, 0]
    # Community Chest: 1 = Pos 1, 2 = Jail, 3 = Pos 0, 4 = Chance
    chance = [0, 0, 0, 0, 1, 2, 0, 0, 3, 4, 0, 0, 0, 5, 6, 7]
    # Chance: 1 = Pos 30, 2 = Pos 16, 3 = Pos 0, 4 = -3 pos, 5 = Jail, 6 = Pos 51, 7 = Pos 6
    d1 = [1, 2, 3, 4, 5, 6]
    d2 = [1, 2, 3, 4, 5, 6]
    d3 = [1, 2, 3, "bus", "mono", "mono"]
    dice = list(product(d1, d2, d3))
    shuffle(chest)
    shuffle(chance)

    for n in range(10000000):
        roll = choice(dice)
        if checkdbl(roll):
            dbl += 1
        else:
            dbl = 0
        if dbl == 3:
            position = 13
            jail = True
            dbl = 0
            continue
        for i in roll:
            if jail:
                if turnInJail == 3:
                    jail = False
                    turnInJail = 0
                elif dbl == 0:
                    turnInJail += 1
                    break
                else:
                    jail = False
            if i == "bus":
                position += 0
            elif i == "mono":
                if position == 39:
                    position = 13
                    jail = True
                    dbl = 0
                else:
                    tiles[position] += 1
                    while position in [0, 2, 5, 9, 13, 14, 22, 26, 28, 32, 43, 46, 47, 50]:
                        position = (position + 1) % 52
            else:
                position = (position + i) % 52
        
        if position == 39:
            position = 13
            jail = True
            dbl = 0
        elif position in [2, 22, 43]:
            if chest[0] == 1:
                position = 1
            elif chest[0] == 2:
                position = 13
                jail = True
                dbl = 0
            elif chest[0] == 3:
                position = 0
            elif chest[0] == 4:
                if chance[0] == 1:
                    position = 30
                elif chance[0] == 2:
                    position = 16
                elif chance[0] == 3:
                    position = 0
                elif chance[0] == 4:
                    position -= 3
                elif chance[0] == 5:
                    position = 13
                    jail = True
                    dbl = 0
                elif chance[0] == 6:
                    position = 51
                elif chance[0] == 7:
                    position = 6
                chance.append(chance.pop(0))
            chest.append(chest.pop(0))
        elif position in [9, 28, 46]:
            if chance[0] == 1:
                position = 30
            elif chance[0] == 2:
                position = 16
            elif chance[0] == 3:
                position = 0
            elif chance[0] == 4:
                position -= 3
            elif chance[0] == 5:
                position = 13
                jail = True
                dbl = 0
            elif chance[0] == 6:
                position = 51
            elif chance[0] == 7:
                position = 6
            chance.append(chance.pop(0))

        tiles[position] += 1
    print(tiles)
    print(list(x/sum(tiles) for x in tiles))
    # with open("monopoly.csv", "w", newline='') as f:
    #    wr = csv.writer(f, delimiter=",")
    #    for i in list(x/sum(tiles) for x in tiles):
    #        wr.writerow([i])


game()