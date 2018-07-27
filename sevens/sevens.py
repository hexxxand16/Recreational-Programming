from random import shuffle, randrange
import csv


# card object
class Card:
    def __init__(self, suit, rank, play=0):
        self.suit = suit
        self.rank = rank
        self.play = play

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Game:
    def __init__(self):
        deck = createDeck()
        shuffle(deck)
        pile = []
        p1 = deck[0:26]
        p2 = deck[26:52]

        self.hand = [0] * 52
        for i in p1:
            if i.suit is "clubs":
                self.hand[i.rank - 1] = 1
            elif i.suit is "spades":
                self.hand[i.rank + 12] = 1
            elif i.suit is "diamonds":
                self.hand[i.rank + 25] = 1
            else:
                self.hand[i.rank + 38] = 1

        p1_plays = playableCards(p1, pile)
        p2_plays = playableCards(p2, pile)
        for i in p1_plays:
            if i.suit == "spades":
                pile.append(i)
                p1.remove(i)
                if p2_plays:
                    num = randrange(0, len(p2_plays))
                    pile.append(p2_plays[num])
                    p2.remove(p2_plays[num])
                    del p2_plays[num]

        for i in p2_plays:
            if i.suit == "spades" and i.rank == 7:
                pile.append(i)
                p2.remove(i)

        while len(p1) > 0 and len(p2) > 0:
            p1_plays = playableCards(p1, pile)
            p2_plays = playableCards(p2, pile)
            if p1_plays:
                num = randrange(0, len(p1_plays))
                pile.append(p1_plays[num])
                p1.remove(p1_plays[num])
                del p1_plays[num]
            if p2_plays:
                num = randrange(0, len(p2_plays))
                pile.append(p2_plays[num])
                p2.remove(p2_plays[num])
                del p2_plays[num]

        if len(p1) == 0:
            self.hand.append(1)
        else:
            self.hand.append(0)


def createDeck():
    deck = []
    suit = ["clubs", "spades", "diamonds", "hearts"]
    rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    for i in suit:
        for j in rank:
            if j == 7:
                deck.append(Card(i, j))
            elif j > 7:
                deck.append(Card(i, j, j - 1))
            elif j < 7:
                deck.append(Card(i, j, j + 1))

    return deck


def playableCards(hand, played):
    playable = []
    for i in hand:
        if i.rank == 7:
            playable.append(i)
            continue
        for j in played:
            if i.suit == j.suit and i.play == j.rank:
                playable.append(i)

    return playable


with open("sevens.csv", "w", newline='') as f:
    for i in range(100000):
        game = Game()
        a = game.hand
        writer = csv.writer(f)
        writer.writerows([a])