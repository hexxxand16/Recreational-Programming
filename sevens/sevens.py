from random import shuffle, seed


# card object
class Card:
    def __init__(self, suit, rank, play=0):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        return "{} of {}".format(self.rank, self.suit)


def createDeck():
    deck = []
    suit = ["clubs", "spades", "diamonds", "hearts"]
    rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    for i in suit:
        for j in rank:
            if j == 7:
                deck.append(Card(i, j))
            elif j > 7:
                deck.append(Card(i, j))
            elif j < 7:
                deck.append(Card(i, j))

    return deck


def playableCards(hand, played):
    playable = []
    for i in hand:
        if i.rank == 7:
            playable.append(i)
            continue
        for j in played:
            if i.suit == j.suit:
                if i.rank > 7 and j.rank == i.rank - 1:
                    playable.append(i)
                elif i.rank < 7 and j.rank == i.rank + 1:
                    playable.append(i)

    return playable


def play(p1, p2, pile, first, depth):
    p1_plays = playableCards(p1, pile)
    p2_plays = playableCards(p2, pile)
    # Heuristic
    if depth == 0:
        return len(p1_plays) - len(p2_plays)
    if not p1:
        return 10000
    elif not p2:
        return -10000

    if first:
        score = -10000
        if not p1_plays:
            return play(p1, p2, pile, False, depth - 1)
        for i in p1_plays:
            new_pile = pile.copy()
            new_p1 = p1.copy()
            new_pile.append(i)
            new_p1.remove(i)
            score = play(new_p1, p2, new_pile, False, depth - 1)
    else:
        score = 10000
        if not p2_plays:
            return play(p1, p2, pile, True, depth - 1)
        for i in p2_plays:
            new_pile = pile.copy()
            new_p2 = p2.copy()
            new_pile.append(i)
            new_p2.remove(i)
            score = play(p1, new_p2, new_pile, True, depth - 1)

    return score


def evaluate(p1, p2, pile, first, depth):
    if first:
        p1_plays = playableCards(p1, pile)
        print("P1: " + str(p1_plays))
        score = -20000
        best_move = 0
        for i in p1_plays:
            new_pile = pile.copy()
            new_p1 = p1.copy()
            new_pile.append(i)
            new_p1.remove(i)
            cur_score = max(score, play(new_p1, p2, new_pile, False, depth))
            if cur_score > score:
                score = cur_score
                best_move = i
            print(str(i) + ": " + str(cur_score))

        print(str(best_move) + ": index " + str(p1.index(best_move)))
    else:
        p2_plays = playableCards(p2, pile)
        print("P2: " + str(p2_plays))
        score = 20000
        best_move = 0
        for i in p2_plays:
            new_pile = pile.copy()
            new_p2 = p2.copy()
            new_pile.append(i)
            new_p2.remove(i)
            cur_score = min(score, play(p1, new_p2, new_pile, True, depth))
            if cur_score < score:
                score = cur_score
                best_move = i
            print(str(i) + ": " + str(cur_score))

        print(str(best_move) + ": index " + str(p2.index(best_move)))
    return best_move


def playCard(p1, p2, card, pile):
    if card in p1:
        pile.append(card)
        p1.remove(card)
    elif card in p2:
        pile.append(card)
        p2.remove(card)


def main():
    # Seed 30: P1 gets 4 7s
    # Seed 42: Fair game
    seed(42)
    deck = createDeck()
    shuffle(deck)
    p1 = deck[0:26]
    p2 = deck[26:52]
    pile = []
    
    playCard(p1, p2, p2[7], pile)
    first = True
    while p1 or p2:
        if first:
            if not playableCards(p1, pile):
                first = False
                continue
            move = evaluate(p1, p2, pile, True, 8)
            playCard(p1, p2, move, pile)
            first = False
        else:
            if not playableCards(p2, pile):
                first = True
                continue
            move = evaluate(p1, p2, pile, False, 8)
            playCard(p1, p2, move, pile)
            first = True


main()