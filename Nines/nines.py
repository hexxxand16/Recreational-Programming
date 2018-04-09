import random
import itertools


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __lt__(self, other):  # overloading <
        return self.rank < other.rank


def deck():
    deck = []
    suit = ["clubs", "spades", "diamonds", "hearts"]
    rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    for i in suit:
        for j in rank:
            deck.append(Card(i, j))

    return deck


def nines(deck, num):
    random.shuffle(Deck)
    hand = Deck[0:9]
    sets = list(itertools.combinations(hand, 3))
    if num == 0:
        return check_triple(sets)
    elif num == 1:
        return check_run_flush(sets)
    elif num == 2:
        return check_run(sets)
    elif num == 3:
        return check_flush(sets)
    elif num == 4:
        return check_pair(sets)


def check_triple(sets):
    for i in sets:
        if i[0].rank == i[1].rank == i[2].rank:
            return True

    return False


def check_run_flush(sets):
    for i in sets:
        if i[0].suit == i[1].suit == i[2].suit:
            hand = sorted(i)
            if (hand[0].rank + 1) % 13 == hand[1].rank and (hand[0].rank + 2) % 13 == hand[2].rank:
                return True

    return False


def check_run(sets):
    for i in sets:
        hand = sorted(i)
        if (hand[0].rank + 1) % 13 == hand[1].rank and (hand[0].rank + 2) % 13 == hand[2].rank:
            return True

    return False


def check_flush(sets):
    for i in sets:
        if i[0].suit == i[1].suit and i[0].suit == i[2].suit:
            return True

    return False


def check_pair(sets):
    for i in sets:
        for j in range(len(i)):
            for k in range(j + 1, len(i)):
                if i[j].rank == i[k].rank:
                    return True

    return False


Deck = deck()
for i in range(5):
    rate = 0
    for j in range(100000):
        rate += nines(Deck, i)
    print(rate / float(100000))