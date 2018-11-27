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
cardwidth = 80
cardlength = 100

class Card:
    def __init__(self,v,x,y,spade=True,faceup=False):
        self.v=v
        self.x=x
        self.y=y
        self.spade = spade
        self.faceup=faceup
        
    #display
    
               
class Deck:
    def __init__(self, spade=True):
        self.deck=[]
        self.suits=['spades','hearts']
        self.ranks=[]
        for i in range(13):
            self.rankes.append(i+1)
        #if spade:
        #    for i in range(8):
                #
        #else:
        #    for i in range(4):
                #
            
            
    def shuffle_cards(self):
        random.shuffle(self.deck)
    
    def load_cards(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.card_images[img] = pygame.image.load(img)
                self.cards.append(Card(img,suit))
                self.cards.append(Card(name_of_image,self.x,self.y,suit))
            
  
class Game:
    def __init__(self, spade = True, win = False):
        self.moves = 0
        self.win = win
        self.spade = spade
        self.deck = Deck(self.spade)
        self.deck.shuffle_cards()
        
        self.piles = []
        for i in range(4):
            pile = []
            for n in range(6):
                pile.append(self.deck.pop())
            piles.append(pile)
        for i in range(6):
            pile = []
            for n in range(5):
                pile.append(self.deck.pop())
            piles.append(pile)    

        self.addons = []
        for i in range(5):
            addon = []
            for n in range(10):
                addon.append(self.deck.pop())
            self.addons.append(addon)
        
        
        
    def display(self,):
        pass
        
    def clicked(self):
        x = mouseX
        y = mouseY
        # identify which pile
        # return home & target
        home = piles[x//#width of cards + space between piles]
        
        
                
        self.win = self.check_exit()
        if not self.win:
            undo = self.check_undo()
            if undo:
                self.un_do(card, home, target)
            
            card = 
            checkValidMoves(card)
           
            #check if the first displayed in home is facedown:
                #faceup
        

                self.moves += 1
    
    def checkValidMoves(self,card,target):
        #select cards
        --> # run a for loop from the top card 
        #check if valid
        for card in 
        sequence=[]
        sequence.append(card.v)
        for i in range(len(sequence)):
            checkvalid = ''.join(sequence[i])
        if checkvalid in '13121110987654321':
            return True
        
        #if empty:
            #accept it
        elif:
            if card.v+1 == target[len(target)-1].v:
                target.append(sequence)

        
    def check_exit(self):
        x = mouseX
        y = mouseY
        if # x of exit button < x < buttonx + width and y
        return True
    
    def check_undo(self):    
        x = mouseX
        y = mouseY
        if # x of exit button < x < buttonx + width and y
        return True
    
    def un_do(self, home, target):
        #draw the sequence back
    
    def check_win():
        #
        
            
class Addon:
    def __init__(self,#):
        
    #50 cards into 5 groups
    #display each group one at a time
    def clicked():
            for card in self.cards:
                #distribute to all piles

    
class Pile(list):
    def __init__(self, cards, x, y, card_size, pile_type="line"):
        # complete!!!
        self.cardwitdh,self.cardlength = card_size
    
    

        
        

    def update(self, piles_to_update):
        for pile in self.piles:
            pile.update()

        if piles_to_update != None:
            for pile in piles_to_update:
                pile.update_positions()
             
        
        
def setup():
    

def draw():
    #if player choose easy:
    g = Game(True,False)
    else:
        g = Game(False,False)
    g.display()
    
def mouseClicked():
    if not g.win():
        g.clicked()
        
        
        
        
        
        
