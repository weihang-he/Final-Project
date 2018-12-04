# move freely
# time steps
# drag and drop (wrong position go back)
# sound effect
# add creepy voices asking 'wanna continue? 100 moves already'

# undo
# exit and start a new game
# winning screen

import os
import random
import time
path = os.getcwd() + '/'
cardwidth = 70
cardlength = 100

class Card:
    def __init__(self, p, num, r, spade=True, faceup=False):
        self.p = p       # which pile this card belongs to
        self.num = num   # the order of it in this pile
        self.r = r       # the rank
        self.spade = spade
        self.faceup = faceup
        self.img = loadImage(path + 'images/back.jpg')
        
    def display(self):
        image(self.img, 30+(self.p-1)*(cardwidth+20), 160+self.num*20, cardwidth, cardlength)
    
    def flip(self):
        if not self.faceup:
            self.img = loadImage(path + 'images/' + str(int(self.spade)) + str(self.r) + '.png')
            self.faceup = True
               
class Deck(list):
    def __init__(self, spade=True):
        self.spade = spade
        self.ranks = []
        
        for i in range(13):
            self.ranks.append(i+1)
        
        if self.spade:
            for i in range(8):
                for r in self.ranks:
                    self.append(Card(0, 0, r, True, False))
        else:
            for i in range(4):
                for r in self.ranks:
                    self.append(Card(0, 0, r, True, False))
            for i in range(4):
                for r in self.ranks:
                    self.append(Card(0, 0, r, False, False))
                    
    def shuffle_cards(self):
        random.shuffle(self)
    
class Game:
    def __init__(self, spade = True, win = False, gameon = False):
        self.moves = 0
        self.win = win
        self.gameon = gameon
        self.spade = spade
        self.deck = Deck(self.spade)
        self.deck.shuffle_cards()
        
        self.piles = []
        for i in range(1,5):
            pile = Pile(i)
            for n in range(6):
                card = self.deck.pop()
                card.p = i
                card.num = n
                pile.append(card)
            self.piles.append(pile)
        for i in range(5,11):
            pile = Pile(i)
            for n in range(5):
                card = self.deck.pop()
                card.p = i
                card.num = n
                pile.append(card)
            self.piles.append(pile)    

        self.addons = []
        for i in range(5):
            addon = Addon(i)
            for n in range(10):
                addon.append(self.deck.pop())
            self.addons.append(addon)
    
    def gamestart(self):
        fill(255)
        textSize(60)
        text('SOLITAIRE', 330, 250)
        noFill()
        stroke(200)
        strokeWeight(2)
        rect(400, 350, 150, 50)
        rect(400, 480, 150, 50)
        textSize(40)
        text('EASY', 425, 390)
        text('HARD', 420, 520)    
                
    def display(self):
        strokeWeight(2)
        stroke(200)
        rect(30, 30, cardwidth, 30)
        textSize(26)
        text('Menu', 31, 56)
        rect(30, 100, cardwidth, 30)
        text('Undo', 31, 126)
        
        for i in range(10):
            stroke(200)
            noFill()
            strokeWeight(2)
            rect(30+i*(cardwidth+20), 160, cardwidth, cardlength)
        rect(120, 30, cardwidth, cardlength)
        rect(840, 30, cardwidth, cardlength)
                
        for pile in self.piles:
            if len(pile) != 0:
                if not pile[len(pile)-1].faceup:
                    pile[len(pile)-1].flip()
                for card in pile:
                    card.display()
    
        for addon in self.addons:
            addon.display()
        
        #pile index
        if mouseX >= 30 and mouseX <= 910:
            i = (mouseX-30)//90
        #number in pile
        if mouseY >= 160 and mouseY <= 160 + (len(self.piles[i])-1)*20 + 100:
            n = (mouseY-160)//20
            if n > len(self.piles[i])-1:
                n = len(self.piles[i])-1
            stroke(0, 0, 100)
            strokeWeight(3)
            rect(30+i*(cardwidth+20), 160+n*20, cardwidth, 20*(len(self.piles[i])-n)+80)
            
    def clicked(self):
        self.checkexit()
        self.checkundo()
        
    def checkexit(self):
        if 30 < mouseX < 100 and 30 < mouseY < 60:
            noFill()
            stroke(0, 0, 100)
            strokeWeight(3)
            rect(30, 30, 70, 30)
            self.gameon = False
            self.gamestart()
    
    def checkundo(self):    
        if 30 < mouseX < 100 and 100 < mouseY < 130:
            noFill()
            stroke(0, 0, 100)
            strokeWeight(3)
            rect(30, 100, 70, 30)
    #    return True
    
    def dragged(self):
        homep = (mouseX-30)//90
        if mouseY >= 160 and mouseY <= 160 + (len(self.piles[homep])-1)*20 + 100:
            cardn = (mouseY-160)//20
            if cardn > len(self.piles[homep])-1:
                cardn = len(self.piles[homep])-1
            self.checkMovable(homep, cardn)
    # chekc after the drag function completes
    
        # identify which pile
        # return home & target
    #    home = piles[x//#width of cards + space between piles]
                
    #    self.win = self.check_exit()
    #    if not self.win:
    #        undo = self.check_undo()
    #        if undo:
    #            self.un_do(card, home, target)
            

    #        checkValid(card)
           
            #check if the first displayed in home is facedown:
                #faceup
        

    #            self.moves += 1
    
    def checkMovable(self, homep, cardn):
        home = self.piles[homep]
        sequence = home[cardn:]
        for c in sequence:
            checkline = ''.join(str(int(c.spade)) + str(c.r))
        if checkline in '113112111110191817161514131211' or checkline in '013012011010090807060504030201':
            #cards move with mouse
            for c in sequence:
                home.remove(c)
            return True
        else:
            return False

    #def checkAcceptable(self, targetp):
    #    if targetp == []:
    #        return True
     #   elif 
    #
        #if empty:
            #accept it
    #    elif:
    #        if card.v+1 == target[len(target)-1].v:
    #            target.append(sequence)

    
    #def undo(self, home, target):
        #draw the sequence back
    
    #def checkwin():
        #
        
            
class Addon(list):
    def __init__(self, order):
        self.order = order
        self.backimg = loadImage(path + 'images/back.jpg')
    
    def display(self):
        image(self.backimg, 910-50-(self.order+1)*20, 30, cardwidth, cardlength)
        
    #display each group one at a time
    def clicked(self, order):
        for i in range(10):
            g.piles[i+1].append(self[i])
        
    
class Pile(list):
    def __init__(self, order):
        self.order = order

    #def update(self, piles_to_update):
    #    for pile in self.piles:
    #        pile.update()

    #    if piles_to_update != None:
    #        for pile in piles_to_update:
    #            pile.update_positions()
                 
g = Game()
        
def setup():
    size(940, 800)
    background(0, 255, 0)

def draw():
    frameRate(15)
    background(0, 100, 0)
    
    #else:
    #    g = Game(False,False)
    if not g.gameon:
        g.gamestart()
    else:
        g.display()
    
    
def mouseClicked():
    if not g.gameon:
        if 400 < mouseX < 550 and 350 < mouseY < 400:
            g.__init__(spade = True, win = False, gameon = False)
            g.gameon = True
            g.display()
        elif 400 < mouseX < 550 and 480 < mouseY < 530:
            g.__init__(spade = False, win = False, gameon = False)
            g.gameon = True
            g.display()
    elif g.gameon and not g.win:
        g.clicked()
    elif g.win:
        time.sleep(5)
        g.gameon = False
        g.gamestart()
        
def mouseDragged():
    if g.gameon and not g.win:
        g.dragged()
        
        
        
        
