class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value
        
    def display(self, xpos, ypos, detailed=True):
        rectMode(CORNER)
        fill(255)
        rect(xpos, ypos, 100, 160)
        if detailed:
            if self.suit == "Club" or self.suit == "Spade":
                fill(0)
            else:
                fill(255, 0, 0)
            textSize(16)
            textAlign(LEFT)
            text(self.suit, xpos + 3, ypos + 15)
            fill(0)
            textAlign(RIGHT)
            text(self.rank, xpos + 97, ypos + 155)
        
    def __add__(self, other):
        if self.suit == other.suit:
            return Card(self.suit, 0, self.value + other.value)
        elif self.value > other.value:
            return Card(self.suit, 0, self.value)
        else:
            return Card(other.suit, 0, other.value)
            