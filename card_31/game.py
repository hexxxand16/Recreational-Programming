import random
import itertools
from functions import *


class game:
    def __init__(self, deck):
        self.player = []
        self.cpu = []
        self.deck = deck
        self.playing = False
        self.game_over = True
        self.difficulty = 0
        self.win = 0
        self.lose = 0
        self.log = []
        self.knock_values = [19, 23, 25, 27, 28, 29]
        
    def title_screen(self):
        rectMode(CORNER)
        textAlign(CENTER)
        textSize(18)
        fill(255)
        rect(350, 200, 200, 200)
        rect(650, 200, 200, 200)
        rect(350, 500, 200, 200)
        fill(0)
        text("Random Mode \n Makes random moves", 450, 300)
        text("Smart Mode \n Makes optimal moves", 750, 300)
        text("Smart Mode+ \n Adaptive knocking \n (untested)", 450, 600)

    def new_game(self, difficulty):
        random.shuffle(self.deck)
        self.player = self.deck[0:3]
        self.cpu = self.deck[3:6]
        self.discard = self.deck[6]
        self.drawing = False
        self.knocking = False
        self.reveal = False
        self.cpu_knocking = False
        self.cur_card = 7
        self.playing = True
        self.game_over = False
        self.cpu_count = 0
        self.difficulty = difficulty
        self.first_turn = True
    
    def select_difficulty(self):
        if mouseX <= 550 and mouseX >= 350 and mouseY <= 400 and mouseY >= 200:
            self.new_game(1)
        elif mouseX <= 850 and mouseX >= 650 and mouseY <= 400 and mouseY >= 200:
            self.new_game(2)
        elif mouseX <= 550 and mouseX >= 350 and mouseY <= 700 and mouseY >= 500:
            self.new_game(3)

    def display_cards(self):
        for i in range(len(self.player)):
            self.player[i].display(440 + 110 * i, 640)
        for i in range(len(self.cpu)):
            self.cpu[i].display(440 + 110 * i, 100, self.reveal)

    def display_deck(self):
        fill(255)
        rectMode(CENTER)
        for i in range(len(self.deck) - self.cur_card):
            rect(width / 5, 350 + 5 * i, 100, 160)

    def display_log(self):
        textAlign(LEFT)
        if len(self.log) > 10:
            del self.log[0]
        fill(0)
        textSize(14)
        for i in range(len(self.log)):
            text(self.log[i], 5 * width / 7, 150 + 15 * i)

    def display_discard(self):
        fill(255)
        self.discard.display(width / 2 - 50, height / 2 - 80)

    def display_draw(self):
        self.deck[self.cur_card].display(7 * width / 9, 640, self.drawing)
        fill(0)
        if not self.drawing:
            textSize(16)
            textAlign(RIGHT)
            text("Click to draw", 1035, 720)

    def display_knock(self):
        if not self.drawing and not self.cpu_knocking and not self.first_turn:
            fill(255)
            rect(7 * width / 9, height / 2 - 80, 100, 160)
            textAlign(CENTER)
            textSize(24)
            fill(0)
            text("KNOCK", 7 * width / 9 + 50, height / 2)

    def display_record(self):
        text("Wins: " + str(self.win), 100, height/2)
        text("Losses: " + str(self.lose) , 100, height/2 + 15)
        if self.lose == 0:
            win_ratio = 100
        else:
            win_ratio = self.win/float(self.win + self.lose) * 100
        text("Win %: " + '%.1f' % win_ratio, 100, height/2 + 30)
        
    def insta_win(self):
        if value(self.player) == 31 or value(self.cpu) == 31:
            self.knocking = True

    def knock(self):
        textAlign(CENTER)
        player_score = value(self.player)
        cpu_score = value(self.cpu)
        text(player_score, width / 2, 850)
        text(cpu_score, width / 2, 50)
        self.reveal = True
        if not self.game_over:
            if player_score > cpu_score:
                self.log.append("You win")
                self.win += 1
            elif player_score == cpu_score:
                if self.cpu_knocking:
                    self.log.append("You win")
                    self.win += 1
                else:
                    self.log.append("You lose")
                    self.lose += 1
            else:
                self.log.append("You lose")
                self.lose += 1
        self.game_over = True
        textSize(24)
        text("Click to continue", width/2, 325)
    
    def random_cpu(self):
        if self.cpu_count == 3 and not self.knocking:
            self.cpu_knocking = True
            self.log.append("CPU knocks")
        elif random.randint(0, 1) == 0:
            self.log.append("CPU swaps " + str(self.cpu[0].rank) + " of " + str(self.cpu[0].suit) + "s for " + str(self.discard.rank) + " of " + str(self.discard.suit) + "s")
            self.cpu[0], self.discard = self.discard, self.cpu[0]
        else:
            self.cpu.append(self.deck[self.cur_card])
            self.log.append("CPU draws and discards " + str(self.cpu[0].rank) + " of " + str(self.cpu[0].suit) + "s")
            self.discard = self.cpu[0]
            del self.cpu[0]
            self.cur_card += 1
        
    def smart_cpu(self, discard=True):
        if value(self.cpu) >= 25 and self.cpu_count != 0 and not self.knocking:
            self.cpu_knocking = True
            self.log.append("CPU knocks")
        else:
            hand_value = value(self.cpu)
            values = []
            sums = []
            if discard:
                self.cpu.append(self.discard)
            else:
                self.cpu.append(self.deck[self.cur_card])
            hands = list(itertools.combinations(self.cpu, 3))
            for i in hands:
                sum = 0
                values.append(value(i))
                for j in i:
                    sum += j.value
                sums.append(sum)
            
            max_val = max(values)
            indices = [index for index, val in enumerate(values) if val == max_val]
            max_sum = 0
            for i in indices:
                if sums[i] > max_sum:
                    max_sum = sums[i]
            
            indices2 = [i for i, val in enumerate(sums) if val == max_sum]
            index = list(set(indices).intersection(set(indices2)))
            
            for i in self.cpu:
                if i not in hands[index[0]]:
                    if i == self.discard and discard:
                        self.cpu = list(hands[index[0]])
                        self.smart_cpu(False)
                        self.cur_card += 1
                    elif i != self.discard and discard:
                        self.log.append("CPU swaps " + str(i.rank) + " of " + str(i.suit) + "s for " + str(self.discard.rank) + " of " + str(self.discard.suit) + "s")
                        self.discard = i
                        self.cpu = list(hands[index[0]])
                    else:
                        self.log.append("CPU draws and discards " + str(i.rank) + " of " + str(i.suit) + "s")
                        self.discard = i
                        self.cpu = list(hands[index[0]])
                    break

    def smart_cpu2(self, discard=True):
        if self.cpu_count < len(self.knock_values):
            if value(self.cpu) >= self.knock_values[self.cpu_count] and self.knocking and self.cpu_count != 0 and not self.knocking:
                self.cpu_knocking = True
                self.log.append("CPU knocks")
                return
        elif value(self.cpu) >= 29 and self.knocking and self.cpu_count != 0 and not self.knocking:
            self.cpu_knocking = True
            self.log.append("CPU knocks")
            return
        
        hand_value = value(self.cpu)
        values = []
        sums = []
        if discard:
            self.cpu.append(self.discard)
        else:
            self.cpu.append(self.deck[self.cur_card])
        hands = list(itertools.combinations(self.cpu, 3))
        for i in hands:
            sum = 0
            values.append(value(i))
            for j in i:
                sum += j.value
            sums.append(sum)
        
        max_val = max(values)
        indices = [index for index, val in enumerate(values) if val == max_val]
        max_sum = 0
        for i in indices:
            if sums[i] > max_sum:
                max_sum = sums[i]
        
        indices2 = [i for i, val in enumerate(sums) if val == max_sum]
        index = list(set(indices).intersection(set(indices2)))
        
        for i in self.cpu:
            if i not in hands[index[0]]:
                if i == self.discard and discard:
                    self.cpu = list(hands[index[0]])
                    self.smart_cpu(False)
                    self.cur_card += 1
                elif i != self.discard and discard:
                    self.log.append("CPU swaps " + str(i.rank) + " of " + str(i.suit) + "s for " + str(self.discard.rank) + " of " + str(self.discard.suit) + "s")
                    self.discard = i
                    self.cpu = list(hands[index[0]])
                else:
                    self.log.append("CPU draws and discards " + str(i.rank) + " of " + str(i.suit) + "s")
                    self.discard = i
                    self.cpu = list(hands[index[0]])
                break
    
    def computer(self):
        if self.difficulty == 1:
            self.random_cpu()
        elif self.difficulty == 2:
            self.smart_cpu()
        elif self.difficulty == 3:
            self.smart_cpu2()
        self.first_turn = False
        self.cpu_count += 1

    def move(self):
        if mouseX <= 760 and mouseX >= 440 and mouseY <= 800 and mouseY >= 640:  # clicking your 3 cards
            if not self.drawing:
                i = floor((mouseX - 440) / 110)
                self.player[i], self.discard = self.discard, self.player[i]
            else:
                i = floor((mouseX - 440) / 110)
                self.player.append(self.deck[self.cur_card])
                self.discard = self.player[i]
                del self.player[i]
                self.cur_card += 1
                self.drawing = False
            if self.cpu_knocking:
                self.knocking = True
            else:
                self.computer()

        if mouseX <= (7 * width / 9 + 110) and mouseX >= 7 * width / 9 and mouseY <= 800 and mouseY >= 640: # clicking draw button
            if not self.drawing:
                self.drawing = True
            else:
                self.discard = self.deck[self.cur_card]
                self.cur_card += 1
                self.drawing = False
                if self.cpu_knocking:
                    self.knocking = True
                else:
                    self.computer()

        if mouseX <= (7 * width / 9 + 110) and mouseX >= 7 * width / 9 and mouseY <= height / 2 + 80 and mouseY >= height / 2 - 80 and not self.drawing and not self.cpu_knocking and not self.first_turn:  # clicking knock
            self.log.append("You knock")
            self.knocking = True
            self.computer()