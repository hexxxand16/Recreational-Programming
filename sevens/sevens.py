from random import shuffle, seed


# card object
class Card:
    def __init__(self, suit, rank, play=0):
        self.suit = suit
        self.rank = rank
        self.connect = -1
        self.shield = -1

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __repr__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


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


def connected(hand):
    # -1: not evaluated
    # 0: not connected
    # 1: singlely connected
    # 3: tail
    for i in range(len(hand) - 1):
        # Check tail end
        if hand[i].rank == 1 or hand[i].rank == 13:
            hand[i].connect = 3
        elif hand[i + 1].rank == hand[i].rank + 1:
            hand[i].connect = 1
            hand[i + 1].connect = 1
        elif hand[i].connect != 1:
            hand[i].connect = 0
    # Last card
    if hand[-1].connect == -1:
        if hand[-1].rank == 1 or hand[-1].rank == 13:
            hand[-1].connect = 3
        elif hand[-1].connect != 1:
            hand[-1].connect = 0


def shield(hand):
    clubs = [x for x in hand if x.suit == "clubs"]
    spades = [x for x in hand if x.suit == "spades"]
    diamonds = [x for x in hand if x.suit == "diamonds"]
    hearts = [x for x in hand if x.suit == "hearts"]
    if clubs[0].rank != 1:
        clubs[0].shield = 1
    if clubs[-1].rank != 13:
        clubs[-1].shield = 1
    if spades[0].rank != 1:
        spades[0].shield = 1
    if spades[-1].rank != 13:
        spades[-1].shield = 1
    if diamonds[0].rank != 1:
        diamonds[0].shield = 1
    if diamonds[-1].rank != 13:
        diamonds[-1].shield = 1
    if hearts[0].rank != 1:
        hearts[0].shield = 1
    if hearts[-1].rank != 13:
        hearts[-1].shield = 1


# Minimax heuristic which values connected cards
def control(p1, p2, pile, first, depth):
    # Heuristic
    p1_plays = playableCards(p1, pile)
    p2_plays = playableCards(p2, pile)
    if depth == 0:
        eval = 0
        for i in p1:
            if i.connect == 1:
                eval += 3
            elif i.connect == 3:
                eval -= 10
        for i in p2:
            if i.connect == 1:
                eval -= 3
            elif i.connect == 3:
                eval += 10
        return eval
    if not p1:
        return 10000
    elif not p2:
        return -10000

    if first:
        score = -10000
        if not p1_plays:
            return control(p1, p2, pile, False, depth - 1)
        for i in p1_plays:
            new_pile = pile.copy()
            new_p1 = p1.copy()
            new_pile.append(i)
            new_p1.remove(i)
            score = max(score, control(new_p1, p2, new_pile, False, depth - 1))
    else:
        score = 10000
        if not p2_plays:
            return control(p1, p2, pile, True, depth - 1)
        for i in p2_plays:
            new_pile = pile.copy()
            new_p2 = p2.copy()
            new_pile.append(i)
            new_p2.remove(i)
            score = min(score, control(p1, new_p2, new_pile, True, depth - 1))

    return score


# Minimax alpha-beta heuristic which values connected cards
def controlab(p1, p2, pile, first, depth, alpha, beta):
    # Heuristic
    p1_plays = playableCards(p1, pile)
    p2_plays = playableCards(p2, pile)
    if depth == 0:
        eval = 0
        for i in p1:
            if i.connect == 1:
                eval += 3
            elif i.connect == 3:
                eval -= 10
        for i in p2:
            if i.connect == 1:
                eval -= 3
            elif i.connect == 3:
                eval += 10
        return eval
    if not p1:
        return 10000
    elif not p2:
        return -10000

    if first:
        score = -10000
        if not p1_plays:
            return controlab(p1, p2, pile, False, depth - 1, alpha, beta)
        for i in p1_plays:
            new_pile = pile.copy()
            new_p1 = p1.copy()
            new_pile.append(i)
            new_p1.remove(i)
            score = max(score, controlab(new_p1, p2, new_pile, False, depth - 1, alpha, beta))
            alpha = max(alpha, score)
            if alpha >= beta:
                break
    else:
        score = 10000
        if not p2_plays:
            return controlab(p1, p2, pile, True, depth - 1, alpha, beta)
        for i in p2_plays:
            new_pile = pile.copy()
            new_p2 = p2.copy()
            new_pile.append(i)
            new_p2.remove(i)
            score = min(score, controlab(p1, new_p2, new_pile, True, depth - 1, alpha, beta))
            beta = min(beta, score)
            if alpha >= beta:
                break

    return score


def controlabSup(p1, p2, pile, first, depth, alpha, beta):
    # Heuristic
    p1_plays = playableCards(p1, pile)
    p2_plays = playableCards(p2, pile)
    if depth == 0:
        eval = 0
        for i in p1:
            if i.connect == 1:
                eval += 2
            if i.connect == 3:
                eval -= 15
            if i.shield == 1:
                eval += 5
        for i in p2:
            if i.connect == 1:
                eval -= 2
            if i.connect == 3:
                eval += 15
            if i.shield == 1:
                eval -= 5
        return eval
    if not p1:
        return 10000
    elif not p2:
        return -10000

    if first:
        score = -10000
        if not p1_plays:
            return controlabSup(p1, p2, pile, False, depth - 1, alpha, beta)
        for i in p1_plays:
            new_pile = pile.copy()
            new_p1 = p1.copy()
            new_pile.append(i)
            new_p1.remove(i)
            score = max(score, controlabSup(new_p1, p2, new_pile, False, depth - 1, alpha, beta))
            alpha = max(alpha, score)
            if alpha >= beta:
                break
    else:
        score = 10000
        if not p2_plays:
            return controlabSup(p1, p2, pile, True, depth - 1, alpha, beta)
        for i in p2_plays:
            new_pile = pile.copy()
            new_p2 = p2.copy()
            new_pile.append(i)
            new_p2.remove(i)
            score = min(score, controlabSup(p1, new_p2, new_pile, True, depth - 1, alpha, beta))
            beta = min(beta, score)
            if alpha >= beta:
                break

    return score


# Minimax heuristic which values number of possible plays
def plays(p1, p2, pile, first, depth):
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
            return plays(p1, p2, pile, False, depth - 1)
        for i in p1_plays:
            new_pile = pile.copy()
            new_p1 = p1.copy()
            new_pile.append(i)
            new_p1.remove(i)
            score = plays(new_p1, p2, new_pile, False, depth - 1)
    else:
        score = 10000
        if not p2_plays:
            return plays(p1, p2, pile, True, depth - 1)
        for i in p2_plays:
            new_pile = pile.copy()
            new_p2 = p2.copy()
            new_pile.append(i)
            new_p2.remove(i)
            score = plays(p1, new_p2, new_pile, True, depth - 1)

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
            cur_score = max(score, controlabSup(new_p1, p2, new_pile, False, 11, -10000, 10000))
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
            cur_score = min(score, controlabSup(p1, new_p2, new_pile, True, 11, -10000, 10000))
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


'''
def player():
    print("Play a card")
        p1_plays = playableCards(p1, pile)
        if not playableCards(p1, pile):
            continue
        print(p1_plays)
        i = int(input())
        while i not in list(range(len(p1_plays))):
            print("Try again")
            i = int(input())
        playCard(p1, p2, p1_plays[i], pile)
'''


def main():
    # Seed 1: P1 gets 6 tails
    # Seed 30: P1 gets 4 7s
    # Seed 42: P1 gets 5 tails, P2 gets 3 7s (P2 forced win?)
    seed(42)
    deck = createDeck()
    shuffle(deck)
    p1 = deck[0:26]
    p2 = deck[26:52]
    pile = []
    p1.sort(key=lambda x: (x.suit, x.rank))
    p2.sort(key=lambda x: (x.suit, x.rank))
    seven = Card("diamonds", 7)
    first = True
    for i in p1:
        if i == seven:
            seven = i
            first = False
            break
    playCard(p1, p2, seven, pile)
    connected(p1)
    connected(p2)
    shield(p1)
    shield(p2)

    while p1 or p2:
        if first:
            if not playableCards(p1, pile):
                first = False
                continue
            move = evaluate(p1, p2, pile, True, 11)
            playCard(p1, p2, move, pile)
            first = False
        else:
            if not playableCards(p2, pile):
                first = True
                continue
            move = evaluate(p1, p2, pile, False, 11)
            playCard(p1, p2, move, pile)
            first = True


main()
