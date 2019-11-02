var canvas = document.querySelector("canvas");

canvas.width = 1200;
canvas.height = 1200;
canvas.style.width = "600px";
canvas.style.height = "600px";
var c = canvas.getContext("2d");
c.scale(2, 2);
c.imageSmoothingEnabled = false;

// Generates random numbers between a and b (inclusive)
function rng(a, b) {
    return Math.random() * (b - a) + a;
}

// Generates random integers between a and b (inclusive)
function randInt(a, b) {
    return Math.floor(rng(a, b + 1))
}

var mouse = {
    x: undefined,
    y: undefined
};

var dblclick = {
    x: undefined,
    y: undefined
};

var weaponOdds = {
    common: 2000,
    uncommon: 400,
    rare: 100,
    epic: 40,
    legenadry: 10,
    mythical: 1
};

window.addEventListener("mousemove", function(m) {
    mouse.x = m.x;
    mouse.y = m.y;
});

window.addEventListener("dblclick", function(m) {
    dblclick.x = m.x;
    dblclick.y = m.y;
});

function Player() {
    this.level = 1;
    this.exp = 0;
    this.toLevel = 8;

    this.play = function() {
        this.drawExpBar();
        this.levelUp();
    }

    this.drawExpBar = function() {
        c.strokeStyle = "white";
        c.beginPath();
        c.rect(6, 20, 100, 10);
        c.stroke();
        if (this.exp <= this.toLevel) {
            c.beginPath();
            c.fillStyle = "dodgerblue";
            c.rect(6.5, 20.5, Math.floor(this.exp / this.toLevel * 99) , 9);
            c.fill();
        }
        c.font = "10px arial";
        c.fillStyle = "white";
        c.fillText("Lv " + this.level, 6, 15);
    }

    this.levelUp = function() {
        if (this.exp >= this.toLevel) {
            this.level++;
            this.exp -= this.toLevel;
            this.toLevel = 3 * this.level ** 2 + 3 * this.level + 1;
            console.log(this.toLevel);
        }
    }
}

var set_1A = ["Wooden", "Iron", "Paper", "Trash", "Candy", "Copper", "Blunt", "Cheese", "Rusted", "Broken", 
    "Inferior", "Unlucky", "Cursed", "Bronze"];
var set_1B = ["Superior",  "Steel", "Silver", "Gold", "Platinum", "Sharp", "Lucky", "Powerful", "Fiery",  
    "Frozen", "Beserker", "Magic", "Obsidian"];
var set_1C = ["Titanium", "Diamond", "Ultimate", "Holy", "Evil", "Unobtainium", "Ancient"];

function getRarityColour(rarity) {
    switch(rarity) {
        case "common":
            return "white";
        case "uncommon":
            return "green";
        case "rare":
            return "blue";
        case "epic":
            return "rebeccapurple";
        case "legendary":
            return "orangered";
        case "mythical":
            return "violet";
        default:
            console.log("You made a typo you idiot.");
            break;
    }
}

function Weapon(name, dmg, rarity) {
    this.name = name;
    this.rarity = rarity;
    this.minDmg = Math.max(Math.floor(dmg * rng(60, 100) / 100), 1);
    this.maxDmg = Math.max(Math.floor(dmg * rng(100, 140) / 100), this.minDmg);
    this.sprite = [0, 0];

    this.generateSprite = function(rarity) {
        if (rarity === "common" || rarity == "uncommon" || rarity == "rare") {
            this.sprite[0] = randInt(0, 3);
        } else {
            this.sprite[0] = randInt(4, 7);
        }
    }

    this.draw = function(xpos, ypos) {
        image = new Image();
        image.src = "Sprites/Preview.png";

        c.strokeStyle = getRarityColour(this.rarity)
        c.beginPath();        
        c.drawImage(image, 96 * this.sprite[0], 96 * this.sprite[1], 96, 96, xpos, ypos, 32, 32);
        c.rect(xpos, ypos, 32, 32);
        c.stroke();
    }

    this.generateSprite(this.rarity);
}

function Enemy(xpos, ypos, hp, def) {
    this.x = xpos;
    this.y = ypos;
    this.maxHp = hp;
    this.hp = hp;
    this.def = def;
    this.sprite = randInt(0, 200);

    this.draw = function() {
        image = new Image();
        image.src = "Sprites/Enemy/enemy" + this.sprite + ".png";

        c.drawImage(image, 450, 32, 64, 64);

        // Draw HP bar
        c.strokeStyle = "white";
        c.beginPath();
        c.rect(432, 100, 100, 10);
        c.stroke();
        if (this.hp > 0) {
            c.beginPath();
            c.fillStyle = "red";        
            c.rect(432.5, 100.5, Math.floor(this.hp / this.maxHp * 99) , 9);
            c.fill();
        }
        c.font = "10px arial";
        c.fillStyle = "white";
        c.fillText("HP: " + this.hp + "/" + this.maxHp, 432.5, 108.5);
    }
}

function attack(weapon, enemy) {
    enemy.hp -= Math.max(Math.floor(rng(weapon.minDmg, weapon.maxDmg) - enemy.def / 2), 1);
    console.log(enemy.hp, Math.floor(theEnemy.hp / theEnemy.maxHp * 100))
}

function generateRarity() {
    var p = randInt(0, 2550)
    if (p <= 1999) {
        return "common";
    } else if (p <= 2399) {
        return "uncommon";
    } else if (p <= 2499) {
        return "rare";
    } else if (p <= 2539) {
        return "epic";
    } else if (p <= 2549) {
        return "legendary";
    } else {
        return "mythical";
    }
}

function probabilities() {
    c.fillStyle = "white";
    var sum = 0;
    for (let i in weaponOdds) {
        sum += weaponOdds[i];
    }
    c.font = "10px arial";
    let n = 0;
    for (let i in weaponOdds) {
        c.fillText("1/" + Number(sum / weaponOdds[i]).toFixed(1), 100, 50 + 10 * n);
        n++;
    }
}

function generateName(rarity) {
    if (rarity === "common" || rarity === "uncommon") {
        return set_1A[randInt(0, set_1A.length - 1)] + " Sword";
    } else if (rarity === "rare"|| rarity == "epic") {
        return set_1B[randInt(0, set_1B.length - 1)] + " Sword";
    } else {
        return set_1C[randInt(0, set_1C.length - 1)] + " Sword";
    }
}

function generateATK(rarity, level) {
    var atk = randInt(1 + 2 * level, 3 + 2 * level);
    if (rarity === "uncommon") {
        atk *= 1.2;
    } else if (rarity === "rare") {
        atk *= 1.5;
    } else if (rarity === "epic") {
        atk *= 2;
    } else if (rarity === "legendary") {
        atk *= 2.5;
    } else if (rarity === "mythical") {
        atk *= 3;
    }
    return Math.floor(atk);
}

function createWeapon() {   
    var rarity = generateRarity();
    var name = generateName(rarity);
    var atk = generateATK(rarity, player.level);
    var weapon = new Weapon(name, atk, rarity);
    inventory.push(weapon)
}

function spawnEnemy() {
    hp = randInt(50, 100);
    def = randInt(0, 10);
    var enemy = new Enemy(theEnemy.x, theEnemy.y, hp, def);
    return enemy;
}

function dispWindow(mouse) {
    var item;
    if (mouse.x >= 40 && mouse.y >= 40 && mouse.x <= 76 && mouse.y <= 76) { // Check if mouse over equipped
        item = leftHand;
    } else if (mouse.x <= 36 * 16) { // Check if over inventory
        var x = Math.floor(mouse.x / 36);        
        var y = Math.floor((mouse.y - 200) / 36);
        var item = inventory[x + 16 * y]
    }
    if (item != undefined) {
        c.beginPath();
        c.fillStyle = "black"
        c.strokeStyle = "white"
        var r = { // Parameters for rect
            x: 140, 
            y: -120,
            width: mouse.x,
            length: mouse.y
        };
        if (mouse.x + r.x > 600) {
            r.x = -140;
            r.width += r.x;
        } else {
            r.x = 140;
        }
        if (mouse.y + r.y < 0) {
            r.y = 120;
            r.length += 120;
        } else {
            r.y = -120;
        }
        c.rect(mouse.x, mouse.y, r.x, r.y);
        c.fill();
        c.stroke();
        c.fillStyle = "white";
        c.font = "10px arial";
        c.fillText(item.name, r.width + 0.5, r.length - 110);
        c.fillText("Damage: " + item.minDmg + " - " + item.maxDmg, r.width + 0.5, r.length - 100);
        c.fillStyle = getRarityColour(item.rarity);
        c.fillText("Rarity: " + item.rarity, r.width + 0.5, r.length - 90)
    }
}

function swapWeapon(dblclick) {
    if (dblclick.x == undefined) {
        return;
    }
    var x = Math.floor(dblclick.x / 36);    
    var y = Math.floor((dblclick.y - 200) / 36);
    var item = inventory[x + 16 * y];
    if (item != undefined) {
        temp = leftHand;
        leftHand = item;
        inventory[x + 16 * y] = temp;
    }
    dblclick.x = undefined;
    dblclick.y = undefined;
}


player = new Player();
var inventory = [];
leftHand = new Weapon("Wooden Sword", 2, "common");
theEnemy = new Enemy(160, 160, 40, 0);

var spawnWeapon = setInterval(createWeapon, 250);
var dealDamage = setInterval(function() {attack(leftHand, theEnemy)}, 1000);
function update() {
    requestAnimationFrame(update);
    c.fillStyle = "black";
    c.fillRect(0, 0, innerWidth, innerHeight);
    player.play();
    leftHand.draw(40, 40);
    theEnemy.draw();
    for (let i = 0; i < inventory.length; i++) {
        inventory[i].draw(36 * (i % 16), 200 + 36 * Math.floor(i / 16));
    }

    if (inventory.length > 176) {
        inventory = [];
    }
    if (theEnemy.hp <= 0) {
        theEnemy = spawnEnemy();
        player.exp += 10;
    }
    probabilities();
    swapWeapon(dblclick);    
    dispWindow(mouse);
}

update();