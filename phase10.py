import random
from itertools import chain, combinations


def powerset(iterable, length):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(0, length))


# Solves longest consecutive subsequence problem O(n)
def findLongestConseqSubseq(arr):
    s = set()
    ans = 0
    n = len(arr)

    # Hash all the array elements
    for ele in arr:
        s.add(ele)

    # check each possible sequence from the start
    # then update optimal length
    for i in range(n):

        # if current element is the starting
        # element of a sequence
        if (arr[i] - 1) not in s:

            # Then check for next elements in the
            # sequence
            j = arr[i]
            while(j in s):
                j += 1

            # update  optimal length if this length
            # is more
            ans = max(ans, j - arr[i])
    return ans


class Card:
    def __init__(self, type, rank=0, colour="black"):
        self.type = type
        self.rank = rank
        self.colour = colour

    def __str__(self):
        return "{} of {}".format(self.type, self.suit)


def generateDeck():
    deck = []
    colours = ["red", "green", "blue", "yellow"]
    for n in range(0, 2):
        for i in range(1, 13):
            for j in colours:
                deck.append(Card("colour", i, j))
        for j in colours:
            deck.append(Card("wild", 0, j))

    return deck


def checkSets(hand, sets):
    maxRank = [0] * 12
    # Count wilds and count sets
    numOfWilds = 0
    for i in hand:
        if i.type != "wild":
            maxRank[i.rank - 1] += 1
        else:
            numOfWilds += 1

    # Wild card allocation
    maxRank.sort(reverse=True)
    if numOfWilds != 0:
        for i in range(0, len(sets)):
            if maxRank[i] < sets[i]:
                wildstoAdd = sets[i] - maxRank[i]
                if wildstoAdd <= numOfWilds:
                    maxRank[i] += wildstoAdd
                    numOfWilds -= wildstoAdd
                else:
                    break

    for i in range(0, len(sets)):
        if maxRank[i] < sets[i]:
            return False

    return True


# Generic algorithim O(n)
def checkRuns(hand, length):
    handarray = []
    numOfWilds = 0
    for i in hand:
        if i.type != "wild":
            handarray.append(i.rank)
        else:
            numOfWilds += 1

    # Array of integers corresponding to each card
    handarray = list(set(handarray))
    # Find numbers not in hand
    notInHand = set(range(1, 13)) - set(handarray)
    # Generate combinations of wilds
    wilds = combinations(notInHand, r=numOfWilds)
    for i in wilds:
        longestRun = findLongestConseqSubseq(handarray + list(i))
        if longestRun >= length:
            return True

    return False


# Brute force algorithm (Best case O(1))
def checkRuns2(hand, length):
    # Generate all hands of run length
    subHands = combinations(hand, length)
    for i in subHands:
        handarray = []
        maxRank = [0] * 12
        numOfWilds = 0
        for j in i:
            if j.type != "wild":
                handarray.append(j.rank)
                maxRank[j.rank - 1] += 1
            else:
                numOfWilds += 1
        # Check if run is possible
        if max(maxRank) != 1:
            continue
        handarray.sort()
        wildsRequired = 0
        for j in range(len(handarray) - 1):
            wildsRequired += handarray[j + 1] - handarray[j] - 1
        if wildsRequired <= numOfWilds:
            return True

    return False


def checkRunSets(hand, length, sets):
    handarray = []
    maxRank = [0] * 12
    # Count wilds and count sets
    numOfWilds = 0
    for i in hand:
        if i.type != "wild":
            handarray.append(i.rank)
            maxRank[i.rank - 1] += 1
        else:
            numOfWilds += 1

    # Array of integers corresponding to each card
    handarray = list(set(handarray))
    handarray.sort()
    # Find numbers not in hand
    notInHand = set(range(1, 13)) - set(handarray)
    # Generate combinations of wilds
    for x in range(1, numOfWilds + 1):
        for y in chain(((),), combinations(notInHand, r=x)):
            newHand = handarray + list(y)
            longestRun = findLongestConseqSubseq(newHand)
            # For valid run
            if longestRun >= length:
                # Find location of run
                for j in range(1, 14 - length):
                    if set(range(j, j + length)).issubset(set(newHand)):
                        index = j
                        newMaxRank = list(maxRank)
                        # Wilds to be used for sets
                        setNumOfWilds = numOfWilds - len(y)
                        # Remove cards used for run
                        for k in range(index - 1, length + index - 2):
                            if k - 1 not in y:
                                newMaxRank[k] -= 1

                        # Find sets
                        newMaxRank.sort(reverse=True)
                        if setNumOfWilds != 0:
                            for i in range(0, len(sets)):
                                if newMaxRank[i] < sets[i]:
                                    wildstoAdd = sets[i] - newMaxRank[i]
                                    if wildstoAdd <= setNumOfWilds:
                                        newMaxRank[i] += wildstoAdd
                                        setNumOfWilds -= wildstoAdd
                                    else:
                                        break

                        succeed = 0
                        for i in range(0, len(sets)):
                            if newMaxRank[i] < sets[i]:
                                break
                            else:
                                succeed += 1

                        if succeed == len(sets):
                            return True

    return False


def checkColourRuns(hand, length):
    if not checkColourSets(hand, length) or not checkRuns(hand, length):
        return False

    # Generate all hands of run length
    subHands = combinations(hand, length)
    for i in subHands:
        if checkColourSets(i, length):
            if checkRuns2(i, length):
                return True

    return False


def checkColourSets(hand, n):
    colourCount = {
        "blue": 0,
        "red": 0,
        "green": 0,
        "yellow": 0
    }
    numOfWilds = 0
    for i in hand:
        if i.type != "wild":
            colourCount[i.colour] += 1
        else:
            numOfWilds += 1

    mostColour = max(colourCount.values())
    if mostColour + numOfWilds >= n:
        return True


# Check for colour run of x and y sets of z
def checkColourRunsAndSets(hand, length, sets):
    if not checkSets(hand, sets):
        return False

    # Generate all hands of run length
    subHands = combinations(hand, length)
    for i in subHands:
        if checkColourRuns(i, length):
            handDifference = list(set(hand) - set(i))
            if checkSets(handDifference, sets):
                return True

    return False


# Check for colour run of x and colour sets
def checkColourRunsAndColourSets(hand, length, n):
    # Generate all hands of run length
    subHands = combinations(hand, length)
    for i in subHands:
        if checkColourRuns(i, length):
            handDifference = list(set(hand) - set(i))
            if checkColourSets(handDifference, n):
                return True

    return False


# Check Vintage Gas Station Phase 10
def checkVGSP10(hand, length, n, m):
    # Generate all hands of run length
    subHands = combinations(hand, length)
    for i in subHands:
        if checkColourRuns(i, length):
            handDifference = list(set(hand) - set(i))
            subsubHands = combinations(handDifference, n)
            for j in subsubHands:
                if checkColourSets(j, n):
                    handDifference2 = list(set(handDifference) - set(j))
                    if checkSets(handDifference2, [2]):
                        return True

    return False


# Check of x of one colour + 1 set of y
def checkColourAndSets(hand, length, n):
    if not checkSets(hand, [n]):
        return False

    # Generate all hands of run length
    subHands = combinations(hand, length)
    for i in subHands:
        if checkColourSets(i, length):
            handDifference = list(set(hand) - set(i))
            if checkSets(handDifference, [n]):
                return True

    return False


# Check colours of two sets
def checkMultiColourSets(hand, sets):
    if not checkColourSets(hand, sets[0]):
        return False

    # Generate all hands of run length
    subHands = combinations(hand, sets[0])
    for i in subHands:
        if checkColourSets(i, sets[0]):
            handDifference = list(set(hand) - set(i))
            if checkColourSets(handDifference, sets[1]):
                return True

    return False


def checkOddEven(hand, n):
    odd = 0
    even = 0
    for i in hand:
        if i.rank == 0:
            odd += 1
            even += 1
        elif i.rank % 2 == 0:
            even += 1
        elif i.rank % 2 == 1:
            odd += 1

    if odd >= n or even >= n:
        return True

    return False


# Check colour sets and odd and even
def checkColourOddEven(hand, n):
    if not checkColourSets(hand, n):
        return False

    subHands = combinations(hand, n)
    for i in subHands:
        if checkColourSets(i, n) and checkOddEven(i, n):
            return True

    return False


def check2Runs(hand, length):
    if not checkRuns(hand, length):
        return False

    subHands = combinations(hand, length)
    for i in subHands:
        if checkRuns2(i, length):
            handDifference = list(set(hand) - set(i))
            if checkRuns(handDifference, length):
                return True

    return False


def game():
    count = 0
    deck = generateDeck()
    for i in range(10000):
        random.shuffle(deck)
        p1 = deck[0:11]
        if checkVGSP10(p1, 3, 3, 2):
            count += 1

    print(str("1/") + str(10000 / count))
    print(str(count / 100) + str("%"))
    print(count)


game()
