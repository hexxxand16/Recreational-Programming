import random


# card object 
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


# function for creating deck
def deck():
    deck = []
    suit = ["clubs", "spades", "diamonds", "hearts"]
    rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    for i in suit:
        for j in rank:
            if i == "hearts":
                j += 100
            deck.append(Card(i, j))

    return deck


def count_suit(hand, suit):
    count = 0
    for i in hand:
        if i.suit == suit:
            count += 1
    return count


# set the player's hand
def set_hand(deck, round):
    p1 = deck[0:(9 - round)]
    p2 = deck[(9 - round):(18 - 2 * round)]
    return p1, p2


# Sort hand in ascending order by value (insertion sort)
def hand_sort(hand):
    i = 1
    while i < len(hand):
        j = i
        while j > 0 and hand[j - 1].rank > hand[j].rank:
            hand[j - 1], hand[j] = hand[j], hand[j - 1]
            j -= 1
        i += 1


def card_compare(x, y):
    if y.suit != "hearts" and x.suit != y.suit:
        return True
    if x.rank > y.rank:
        return True
    return False


class game:
    def __init__(self):
        self.Deck = deck()
        self.p1_score = 0
        self.p2_score = 0
        self.p1_first = False

    def five(self, predict=False):
        if predict:
            if self.round < 5:
                return 5
            else:
                return count_suit(self.p1, "hearts")
        else:
            if self.trick_first:
                for i in reversed(self.p1):
                    if i.suit == "hearts":
                        continue
                    return i  # Play highest non heart
                return self.p1[0]  # Play lowest heart (only if all cards are hearts)
            else:  # Going second
                for i in reversed(self.p1):
                    if i.suit == self.p2_play.suit:
                        return i  # Play lowest card that beats opponent

                for i in self.p1:
                    if i.suit == "hearts":
                        return i  # Play heart if no other play

                return self.p1[0]  # Play worst card if no moves

    def basic(self, predict=False):
        if predict:
            return count_suit(self.p2, "hearts")
        else:
            if not self.trick_first:
                for i in reversed(self.p2):
                    if i.suit == "hearts":
                        continue
                    return i  # Play highest non heart
                return self.p2[0]  # Play lowest heart (only if all cards are hearts)
            else:
                for i in reversed(self.p2):
                    if i.suit == self.p1_play.suit:
                        return i  # Play lowest card that beats opponent

                for i in self.p2:
                    if i.suit == "hearts":
                        return i  # Play heart if no other play

                return self.p2[0]  # Play worst card if no moves

    def play(self):
        self.round = 0
        while self.round < 8:
            self.p1_first = not self.p1_first
            p1_trick = 0
            p2_trick = 0
            self.round += 1
            random.shuffle(self.Deck)
            self.p1, self.p2 = set_hand(self.Deck, self.round)
            hand_sort(self.p1)
            hand_sort(self.p2)

            # Gameplay
            self.trick_first = True
            p1_predict = self.five(True)
            p2_predict = self.basic(True)
            while len(self.p1) != 0 or len(self.p2) != 0:
                if self.trick_first:  # p1 first
                    self.p1_play = self.five()
                    self.p2_play = self.basic()
                    if card_compare(self.p1_play, self.p2_play):
                        p1_trick += 1
                    else:
                        p2_trick += 1
                        self.trick_first = False
                else:  # p2 first
                    self.p2_play = self.basic()
                    self.p1_play = self.five()
                    if card_compare(self.p2_play, self.p1_play):
                        p2_trick += 1
                    else:
                        p1_trick += 1
                        self.trick_first = True
                del self.p1[self.p1.index(self.p1_play)]
                del self.p2[self.p2.index(self.p2_play)]

            if p1_predict == p1_trick:
                if p1_predict == 5:
                    self.p1_score += 1000
                    return
                else:
                    self.p1_score += 10
            if p2_predict == p2_trick:
                if p2_predict == 5:
                    self.p2_score += 1000
                    return
                else:
                    self.p2_score += 10
            self.p1_score += p1_trick
            self.p2_score += p2_trick
            

def main():
    Game = game()
    p1 = 0
    p2 = 0
    for i in range(100000):
        Game.play()
        if Game.p1_score > Game.p2_score:
            p1 += 1
        else:
            p2 += 1
        Game.p1_score = 0
        Game.p2_score = 0

    print(p1, p2)


main()