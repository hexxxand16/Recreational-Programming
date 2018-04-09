import random
import itertools
import csv


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


def nines(deck):
    with open("best_hands.csv", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        best_hands = []
        hand_names = []
        for i in csvreader:
            best_hands.append([int(i[0]), int(i[1]), int(i[2])])
            hand_names.append(str(i[3]))

    random.shuffle(deck)
    # hand = [deck[39], deck[33], deck[6], deck[28], deck[4], deck[32], deck[7], deck[29], deck[12]]
    hand = deck[0:9]
    sets = list(itertools.combinations(hand, 3))
    plays = []
    for i in range(64):
        play = []
        for j in range(len(sets)):
            play = []
            play.append(sets[i])
            if comp(play[0], sets[j]):
                continue

            play.append(sets[j])
            for k in range(len(sets)):
                if not comp(play[0], sets[k]) and not comp(play[1], sets[k]):
                    play.append(sets[k])
                    break

            plays.append(play)

    play_values = []
    for i in plays:
        values = []
        for j in i:
            values.append(checks(j))
        play_values.append(values)

    index = []
    for i in play_values:
        index.append(best_hands.index(sorted(i, reverse=True)))

    best_hand = sorted(range(len(index)), key=lambda i: index[i])[:1]

    for i in best_hand:
        print("Best Hand is: " + str(hand_names[index[i]]) + " (" + str(index[i] + 1) + ")")
        for j in plays[i]:
            print()
            print_hand(j)


def check_triple(set):
    if set[0].rank == set[1].rank == set[2].rank:
        return True

    return False


def check_run_flush(set):
    if set[0].suit == set[1].suit == set[2].suit:
        hand = sorted(set)
        if (hand[0].rank + 1) % 13 == hand[1].rank and (hand[0].rank + 2) % 13 == hand[2].rank:
            return True

    return False


def check_run(set):
    hand = sorted(set)
    if (hand[0].rank + 1) % 13 == hand[1].rank and (hand[0].rank + 2) % 13 == hand[2].rank:
        return True

    return False


def check_flush(set):
    if set[0].suit == set[1].suit == set[2].suit:
        return True

    return False


def check_pair(set):
    for i in range(len(set)):
        for j in range(i + 1, len(set)):
            if set[i].rank == set[j].rank:
                return True

    return False


def comp(list1, list2):
    for val in list1:
        if val in list2:
            return True
    return False


def checks(set):
    if check_triple(set):
        return 6
    elif check_run_flush(set):
        return 5
    elif check_run(set):
        return 4
    elif check_flush(set):
        return 3
    elif check_pair(set):
        return 2
    else:
        return 1


def print_hand(hand):
    for i in hand:
        print(str(i.rank) + " of " + str(i.suit))


Deck = deck()
nines(Deck)
