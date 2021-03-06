// Select canvas by HTML tag
var canvas = document.querySelector("canvas");
canvas.width = 1800;
canvas.height = 1200;
canvas.style.width = "900px";
canvas.style.height = "600px";

var ctx = canvas.getContext('2d')
ctx.scale(2, 2);
ctx.imageSmoothingEnabled = false;

card_width = 500;
card_height = 726;

// Variable for storing mouse coordinates
var mouse = {
    x: undefined,
    y: undefined
};

// Variable for storing mouse click coordinates
var mousedown = {
    x: undefined,
    y: undefined
};

window.addEventListener("mousedown", function(m) {
    mousedown.x = m.x;
    mousedown.y = m.y;
});

window.addEventListener("mousemove", function(m) {
    mouse.x = m.x;
    mouse.y = m.y;
});

window.addEventListener("mouseup", function() {
    mousedown.x = undefined;
    mousedown.y = undefined;
    for (var i = 0; i < p1_plays.length; i++) {
        p1_plays[i].xcorner = p1_plays[i].x + card_width/8;
        p1_plays[i].ycorner = p1_plays[i].y + card_height/8;
        if (p1_plays[i].xTarget > p1_plays[i].xcorner ||
            p1_plays[i].xTarget + card_width/8 < p1_plays[i].x ||
            p1_plays[i].yTarget > p1_plays[i].ycorner ||
            p1_plays[i].yTarget + card_height/8 < p1_plays[i].y && p1_plays[i].dragging == false) {
                p1_plays[i].x = p1_plays[i].xOld;
                p1_plays[i].y = p1_plays[i].yOld;
            } else {
                p1_plays[i].x = p1_plays[i].xTarget;
                p1_plays[i].y = p1_plays[i].yTarget;
                pile.push(p1_plays[i]);
                p1.splice(p1.indexOf(p1_plays[i]), 1);
                p1_plays.splice(i, 1);
                p1Move = false;
                return;
            }
    }
});

// Shuffle Algorithm
function shuffle(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
    return a;
}

// Suit sorting
function compareSuit(a, b) {
    if (a.suit < b.suit)
      return -1;
    if (a.suit > b.suit)
      return 1;
    return 0;
}

// Rank sorting
function compareRank(a, b) {
    if (a.rank < b.rank)
      return -1;
    if (a.rank > b.rank)
      return 1;
    return 0;
}

// Rank sorting (desending)
function compareRankD(a, b) {
    if (a.rank > b.rank)
      return -1;
    if (a.rank < b.rank)
      return 1;
    return 0;
}

function searchRankSuit(hand, rank, suit) {
    for (var i = 0; i < hand.length; i++) {
        if (hand[i].rank == rank && hand[i].suit == suit)
            return true;
    }
    return false;
}

// Card object
function Card(suit, rank, src) {
    this.suit = suit;
    this.rank = rank;
    this.sprite = src;
    // x, y positions
    this.x;
    this.y;
    // Corner positions
    this.xcorner;
    this.ycorner;
    this.dragging = false;
    // Original x, y corners when dragging
    this.dragx = undefined;
    this.dragy = undefined;
    // x, y position for final position of card
    this.xTarget;
    this.yTarget;
    // x, y position before dragging
    this.xOld;
    this.yOld;
    this.distance = -1;

    this.draw = function() {
        this.xcorner = this.x + card_width/8;
        this.ycorner = this.y + card_height/8;
        var img = new Image();
        img.src = this.sprite;
        ctx.drawImage(img, this.x, this.y, img.width/8, img.height/8);
    }
}

// Create deck
function generateDeck() {
    var deck = [];
    for (var i = 0; i < 4; i++) {
        for (var j = 1; j <= 13; j++) {
            var suit;
            switch(i) {
                case 0:
                    suit = "club";
                    break;
                case 1:
                    suit = "diamond";
                    break;
                case 2:
                    suit = "heart";
                    break;
                case 3:
                    suit = "spade";
                    break;
            }
            var card = new Card(suit, j, "Cards/" + (13 * i + j) + ".png");
            if (card.rank == 7) {
                card.xTarget = 310 + i * 70;
                card.yTarget = 250;
            } else if (card.rank < 7) {
                card.xTarget = 310 + i * 70;
                card.yTarget = 20 + 20 * j;
            } else {
                card.xTarget = 310 + i * 70;
                card.yTarget = 360 + 20 * (j - 8);
            }
            deck.push(card);
        }
    }
    return deck
}

// Set position of cards for CPU
function setCPU(hand) {
    var suits = ["club", "diamond", "heart", "spade"];
    suits.reverse();
    var lower = [];
    var upper = [];
    for (var i = 0; i < hand.length; i++) {
        if (hand[i].rank <= 7) {
            lower.push(hand[i]);
        } else {
            upper.push(hand[i]);
        }
    }
    lower.sort(compareRank);
    lower.sort(compareSuit);
    upper.sort(compareRankD);
    upper.sort(compareSuit);
    var drawn;
    for (var i = 0; i < 4; i++) {
        drawn = 0;
        for (var j = 0; j < lower.length; j++) {
            if (lower[j].suit == suits[i]) {
                lower[j].x = 835 - i * 70
                lower[j].y = 80 + 20 * drawn
                drawn++;
            }
        }
    }
    upper.reverse()
    for (var i = 0; i < 4; i++) {
        drawn = 0;
        for (var j = upper.length - 1; j >= 0; j--) {
            if (upper[j].suit == suits[i]) {
                upper[j].x = 835 - i * 70
                upper[j].y = 360 + 20 * drawn
                drawn++;
            }
        }
    }
    var arr = [lower, upper];
    return arr;
}

// Set X, Y positions of cards for player
function setPlayer(hand) {
    var suits = ["club", "diamond", "heart", "spade"];
    var lower = [];
    var upper = [];
    // Partition hand
    for (var i = 0; i < hand.length; i++) {
        if (hand[i].rank <= 7) {
            lower.push(hand[i]);
        } else {
            upper.push(hand[i]);
        }
    }
    // Sort by rank and suit
    lower.sort(compareRank);
    lower.sort(compareSuit);
    upper.sort(compareRankD);
    upper.sort(compareSuit);
    var drawn;
    // Set positions
    for (var i = 0; i < 4; i++) {
        drawn = 0;
        for (var j = 0; j < lower.length; j++) {
            if (lower[j].suit == suits[i]) {
                lower[j].x = i * 70
                lower[j].y = 80 + 20 * drawn
                lower[j].xOld = i * 70
                lower[j].yOld = 80 + 20 * drawn
                drawn++;
            }
        }
    }
    upper.reverse()
    for (var i = 0; i < 4; i++) {
        drawn = 0;
        for (var j = upper.length - 1; j >= 0; j--) {
            if (upper[j].suit == suits[i]) {
                upper[j].x = i * 70
                upper[j].y = 360 + 20 * drawn
                upper[j].xOld = i * 70
                upper[j].yOld = 360 + 20 * drawn
                drawn++;
            }
        }
    }
    var arr = [lower, upper];
    return arr;
}

function drawCPU(hand) {
    for (var i = 0; i < hand[0].length; i++) {
        hand[0][i].draw();
    }
    for (var i = hand[1].length - 1; i >= 0; i--) {
        hand[1][i].draw();
    }
}

function drawPlayer(hand, plays) {
    for (var i = 0; i < hand[0].length; i++) {
        hand[0][i].draw();
    }
    for (var i = hand[1].length - 1; i >= 0; i--) {
        hand[1][i].draw();
    }
    for (var i = 0; i < plays.length; i++) {
        plays[i].draw();
    }
}

function drawGrid() {
    for (var i = 0; i < 4; i++) {
        ctx.beginPath();
        ctx.strokeStyle = "black";
        ctx.lineWidth = "1";
        // Upper cards
        ctx.rect(310 + i * 70, 140, card_width/8, card_height/8);
        // Center cards
        ctx.rect(310 + i * 70, 250, card_width/8, card_height/8);
        // Lower cards
        ctx.rect(310 + i * 70, 360, card_width/8, card_height/8);
        ctx.stroke();
        ctx.closePath();
    }
}

function dragCard(mousedown, mouse) {
    // Check if mouse is held down
    if (mousedown.x == undefined) {
        for (var i = 0; i < p1_plays.length; i++) {
            p1_plays[i].dragging = false;
        }
        return;
    }
    // Move card if mouse is down and over a card
    for (var i = 0; i < p1_plays.length; i++) {
        if (p1_plays[i].dragging == true) {
            p1_plays[i].x = p1_plays[i].dragx - card_width/8 + (mouse.x - mousedown.x);
            p1_plays[i].y = p1_plays[i].dragy - card_height/8 + (mouse.y - mousedown.y);
            return;
        }
    }
    // Check if over card on mouse click
    for (var i = 0; i < p1_plays.length; i++) {
        if (mousedown.x > p1_plays[i].x && mousedown.x < p1_plays[i].xcorner && mousedown.y > p1_plays[i].y && mousedown.y < p1_plays[i].ycorner) {
            p1_plays[i].dragging = true;
            p1_plays[i].xOld = p1_plays[i].x;
            p1_plays[i].yOld = p1_plays[i].y;
            p1_plays[i].dragx = p1_plays[i].xcorner;
            p1_plays[i].dragy = p1_plays[i].ycorner;
            return;
        }
    }
}

function playableCards(hand, pile) {
    var playable = []
    for (var i = 0; i < hand.length; i++) {
        if (hand[i].rank == 7) {
            playable.push(hand[i]);
            continue;
        }   
        for (var j = 0; j < pile.length; j++) {
            if (hand[i].suit == pile[j].suit) {
                if (hand[i].rank > 7 && pile[j].rank == hand[i].rank - 1) {
                    playable.push(hand[i]);
                } else if (hand[i].rank < 7 && pile[j].rank == hand[i].rank + 1) {
                    playable.push(hand[i]);
                }
            }
        }
    }
    return playable
}

// Calculate card distance
function calculateDistance(hand) {
    suits = ["diamond", "heart", "spade", "club"];
    for (var i = 0; i < suits.length; i++) {
        lower = [];
        upper = [];
        for (var j = 0; j < hand.length; j++) {
            if (hand[j].suit == suits[i]) {
                if (hand[j].rank == 7) {
                    lower.push(hand[j]);
                    upper.push(hand[j]);
                }
                else if (hand[j].rank < 7) {
                    lower.push(hand[j]);
                } else {
                    upper.push(hand[j]);
                }
            }
        }
        lower.sort(compareRankD);
        upper.sort(compareRank);
        for (var j = 0; j < lower.length - 1; j++) {
            lower[j].distance = lower[j].rank - lower[j + 1].rank;
        }
        if (lower.length != 0) {
            lower[lower.length - 1].distance = lower[lower.length - 1].rank + 1;
        }
        for (var j = 0; j < upper.length - 1; j++) {
            if (upper[j].rank == 7) {
                upper[j].distance += Math.abs(upper[j].rank - upper[j + 1].rank);
            }
            upper[j].distance = Math.abs(upper[j].rank - upper[j + 1].rank);
        }
        if (upper.length != 0) {
            upper[upper.length - 1].distance = 13 - upper[upper.length - 1].rank + 2;
        }
    }
}

// Finds the best move based on distance
function findBestMove(p1, hand, pile) {
    var p1_plays = playableCards(p1, pile);
    var playable = playableCards(hand, pile);
    for (var i = 0; i < playable.length; i++) {
        if (playable[i].distance == 2) {
            return playable[i];
        }
    }
    for (var i = 0; i < playable.length; i++) {
        if (playable[i].distance == 1 && p1_plays.length != 0) {
            return playable[i];
        }
    }
    var distances = []
    for (var i = 0; i < playable.length; i++) {
        if (playable[i].distance > 2) {
            distances.push(playable[i].distance);
        }
    }
    for (var i = 0; i < playable.length; i++) {
        if (playable[i].distance == Math.min.apply(null, distances)) {
            return playable[i];
        }
    }
    console.log("There's a bug");
    return playable[0];
}

function evaluate(p1, cpu, pile) {
    var bestMove = findBestMove(p1, cpu, pile);
    pile.push(bestMove);
    cpu.splice(cpu.indexOf(bestMove), 1);
    // Change position
    bestMove.x = bestMove.xTarget;
    bestMove.y = bestMove.yTarget;
}

function blueBorder(plays) {
    for (var i = 0; i < plays.length; i++) {
        ctx.beginPath();
        ctx.strokeStyle = "blue";
        ctx.lineWidth = "2";
        ctx.rect(plays[i].x, plays[i].y, card_width/8, card_height/8);
        ctx.stroke()
        ctx.closePath();
    }
}

var deck = generateDeck();
shuffle(deck);
// Boolean to check if player moves
var p1Move;
var p1 = deck.slice(0, 26);
var p2 = deck.slice(26, 52);
calculateDistance(p2);
p1.sort(compareRank);
p2.sort(compareRank);
var pile = [];
var p1_draw = setPlayer(p1);
var p2_draw = setCPU(p2);
// Search and play 7 of diamonds
for (var i = 0; i < p1.length; i++) {
    if (p1[i].suit == "diamond" && p1[i].rank == 7) {
        pile.push(p1[i]);
        p1[i].x = p1[i].xTarget;
        p1[i].y = p1[i].yTarget;
        p1.splice(i, 1);
        p1Move = false;
        break;
    }
}
if (pile.length != 1) {
    for (var i = 0; i < p2.length; i++) {
        if (p2[i].suit == "diamond" && p2[i].rank == 7) {
            pile.push(p2[i]);
            p2[i].x = p2[i].xTarget;
            p2[i].y = p2[i].yTarget;
            p2.splice(i, 1);
            p1Move = true;
            break;
        }
    }
}
var p1_plays = playableCards(p1, pile);
if (p1_plays === undefined || p1_plays.length == 0) {
    p1Move = false
}

var toggle = true;
function update() {
    // Set to 30fps
    requestAnimationFrame(update);
    if (toggle) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "green";
        ctx.fillRect(0, 0, innerWidth, innerHeight);
        drawGrid();
        while (p1Move == false) {
            p2_plays = playableCards(p2, pile);
            if (p2_plays === undefined || p2_plays.length == 0) {
                p1_plays = playableCards(p1, pile);
                p1Move = true;
                break;
            }
            evaluate(p1, p2, pile);
            p1_plays = playableCards(p1, pile);
            if (p1_plays === undefined || p1_plays.length == 0) {
                if (pile.length == 52) {
                    p1Move = true;
                }
            } else {
                p1Move = true
            }  
        }
        ctx.fillStyle = "black";
        pile.sort(compareRank)
        dragCard(mousedown, mouse);
        drawCPU(p2_draw);
        drawPlayer(p1_draw, p1_plays);
        for (var i = 0; i < pile.length; i++) {
            pile[i].draw();
        }
        blueBorder(p1_plays);
    }
}

update();