# move freely
# time steps
# drag and drop (wrong position go back)
# sound effect
# add creepy voices asking 'wanna continue? 100 moves already'

# undo
# exit and start a new game
# winning screen

# how cards are displayed first

import os
import random
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
    def __init__(self, spade = True, win = False):
        self.moves = 0
        self.win = win
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
            if not pile[-1].faceup:
                pile[-1].flip()
            for card in pile:
                card.display()
    
        for addon in self.addons:
            addon.display()
        
        #test if the mouse is over the card& highlight the card
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
    
            
    #def clicked(self):

    #def mousePressed(self):
    #def mouseDragged(self):
    #def mouseReleased(self):
    
    
        # identify which pile
        # return home & target
    #    home = piles[x//#width of cards + space between piles]
        
        
                
    #    self.win = self.check_exit()
    #    if not self.win:
    #        undo = self.check_undo()
    #        if undo:
    #            self.un_do(card, home, target)
            

    #        checkValidMoves(card)
           
            #check if the first displayed in home is facedown:
                #faceup
        

    #            self.moves += 1
    
    #def checkValidMoves(self,card,target):
        #select cards
    #    --> # run a for loop from the top card 
        #check if valid
    #    for card in 
    #    sequence=[]
    #    sequence.append(card.v)
    #    for i in range(len(sequence)):
    #        checkvalid = ''.join(sequence[i])
    #    if checkvalid in '13121110987654321':
    #        return True
        
        #if empty:
            #accept it
    #    elif:
    #        if card.v+1 == target[len(target)-1].v:
    #            target.append(sequence)

        
    #def check_exit(self):
    #    x = mouseX
    #    y = mouseY
    #    if # x of exit button < x < buttonx + width and y
    #    return True
    
    #def check_undo(self):    
    #    x = mouseX
    #    y = mouseY
    #    if # x of exit button < x < buttonx + width and y
    #    return True
    
    #def un_do(self, home, target):
        #draw the sequence back
    
    #def check_win():
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
             
g = Game(True,False)    
        
def setup():
    size(940, 800)
    background(0, 255, 0)

def draw():
    background(0, 100, 0)
    
    #else:
    #    g = Game(False,False)
    g.display()
    
    
#def mouseClicked():
#    if not g.win():
   # g.clicked()
        
        
        
        
        
        
