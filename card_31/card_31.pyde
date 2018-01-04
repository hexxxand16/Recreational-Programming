from Card import *
from game import *

deck = []
Game = game(deck)

def setup():
    size(1200,900)
    suit = ["Club", "Spade", "Heart", "Diamond"]
    rank = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
    value = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    for i in suit:
        for j in range(13):
            deck.append(Card(i, rank[j], value[j]))
    
Game = game(deck)
def draw():
    background(200)
    if Game.playing:
        Game.insta_win()
        Game.display_cards()
        Game.display_deck()
        Game.display_discard()
        Game.display_knock()
        Game.display_draw()
        Game.display_log()
        Game.display_record()
        if Game.knocking:
            Game.knock()
    else:
        Game.title_screen()

def mouseReleased():
    if not Game.game_over:
        Game.move()
    elif Game.difficulty != 0:
        Game.log = []
        Game.new_game(Game.difficulty)
    else:
        Game.select_difficulty()
    