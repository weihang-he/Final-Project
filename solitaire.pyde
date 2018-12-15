add_library('minim')

import os
import random
import time

path = os.getcwd() + '/'
player = Minim(this)

cardwidth = 70
cardlength = 100

class Card:
    def __init__(self, num, r, spade=True, faceup=False, moving=False):
        self.p = []      # the pile history of the card
        self.num = num   # the order of it in current pile
        self.r = r       # the rank
        self.spade = spade
        self.faceup = faceup
        self.fuh = []    # keep track of face up history
        self.moving = moving    #if it is moving with the mouse
        self.img = loadImage(path + 'images/back.jpg')
        
    def display(self):
        if not self.moving:
            image(self.img, 30+(self.p[len(self.p)-1]-1)*(cardwidth+20), 160+self.num*20, cardwidth, cardlength)
        else:
            image(self.img, mouseX-cardwidth/2, mouseY-10+self.num*20, cardwidth, cardlength)
    
    def flip(self):
        # traditional flipping cards
        if not self.faceup:
            self.img = loadImage(path + 'images/' + str(int(self.spade)) + str(self.r) + '.png')
            self.faceup = True
    
    def cover(self):
        # in case of undo, sometimes a card needs to be unflipped
        if self.faceup:
            self.img = loadImage(path + 'images/back.jpg')
            self.faceup = False  
               
class Deck(list):
    def __init__(self, spade=True):
        self.spade = spade     # whether of not the deck is all spade cards
        self.ranks = []
        
        for i in range(13):
            self.ranks.append(i+1)
        
        if self.spade:    # all spade cards
            for i in range(8):
                for r in self.ranks:
                    self.append(Card(0, r, True, False))
        else:      # half spade cards, half heart cards
            for i in range(4):
                for r in self.ranks:
                    self.append(Card(0, r, True, False))
            for i in range(4):
                for r in self.ranks:
                    self.append(Card(0, r, False, False))
                    
    def shuffle_cards(self):
        random.shuffle(self)
    
class Game:
    def __init__(self, spade = True, win = False, gameon = False):
        self.moves = 0
        self.win = win
        self.gameon = gameon      # whether or not it is in the menu
        self.spade = spade        # whether the game is easy or hard
        self.deck = Deck(self.spade)
        self.deck.shuffle_cards()
        self.mouselist = []
        self.done = []
        self.undotimes = 0
        self.hinttimes = 0
        self.doneimg1 = loadImage(path + 'images/11.png')
        self.doneimg2 = loadImage(path + 'images/01.png')
        self.bgimg = loadImage(path + 'images/bg.jpeg')
        
        # append each pile
        self.piles = []
        for i in range(1,5):
            pile = Pile(i)
            for n in range(6):
                card = self.deck.pop()
                card.p.append(i)
                card.fuh.append(int(card.faceup))
                card.num = n
                pile.append(card)
            pile[5].flip()
            pile[5].fuh[0] = 1
            self.piles.append(pile)
        for i in range(5,11):
            pile = Pile(i)
            for n in range(5):
                card = self.deck.pop()
                card.p.append(i)
                card.fuh.append(int(card.faceup))
                card.num = n
                pile.append(card)
            pile[4].flip()
            pile[4].fuh[0] = 1
            self.piles.append(pile)    
        
        # append each addon
        self.addons = []
        for i in range(5):
            addon = Addon(i)
            for n in range(10):
                addon.append(self.deck.pop())
            self.addons.append(addon)
    
    def gamestart(self):    # the menu
        fill(255)
        textSize(60)
        text('SOLITAIRE', 330, 250)
        noFill()
        stroke(200)
        strokeWeight(2)
        rect(300, 350, 150, 50)
        rect(300, 480, 150, 50)
        textSize(40)
        text('EASY', 325, 390)
        text('HARD', 320, 520) 
        textSize(30)
        text('Record: ', 470, 390)
        text('Record: ', 470, 520)
        # read highest record
        file1 = open(path + 'scoreboard/1.csv', 'r')
        file2 = open(path + 'scoreboard/2.csv', 'r')
        record1 = file1.read().split(',')
        record2 = file2.read().split(',')
        r1 = 1000
        for n in range (1, len(record1)):
            if int(record1[n]) < r1:
                r1 = int(record1[n])
        r2 = 1000
        for n in range (1, len(record2)):
            if int(record2[n]) < r2:
                r2 = int(record2[n])
        file1.close()
        file2.close()
        text(r1, 600, 390)
        text(r2, 600, 520)
                    
    def display(self):
        #highlight
        strokeWeight(2)
        stroke(200)
        rect(30, 30, cardwidth, 30)
        textSize(26)
        text('Menu', 31, 56)
        rect(30, 100, cardwidth, 30)
        text('Undo', 31, 126)
        textSize(35)
        text(self.moves, 660, 93)
        rect(630, 60, 100, 40)
        textSize(35)
        text('Hint', 510, 93)
        rect(500, 60, 100, 40)
        
        # if a pile has no cards, display a rectangle in the card position
        for i in range(10):
            if self.piles[i] == []:
                stroke(200)
                noFill()
                strokeWeight(2)
                rect(30+i*(cardwidth+20), 160, cardwidth, cardlength)
        
        # if no done, display a rectangle in the position
        if self.done == []:
            rect(120, 30, cardwidth, cardlength)
        else:
            cnt = 0
            for i in self.done:
                image(i, 120+cnt*20, 30, cardwidth, cardlength)
                cnt += 1
        
        # if no more addons, display a rectangle
        if self.addons == []:
            rect(840, 30, cardwidth, cardlength)
      
        # display all the cards in the piles  
        for pile in self.piles:
            if len(pile) != 0:
                for card in pile:
                    card.display()
                    
        # constantly updating what's following the mouse
        if self.mouselist != []:
            for c in self.mouselist:
                c.display()
        
        # display addons
        for addon in self.addons:
            addon.display()
        
        # highlight cards
        i = (mouseX-30)//90
        if i >= 9:
            i = 9
        elif i == -1:
            i = 0
        if 160 <= mouseY <= 160 + (len(self.piles[i])-1)*20 + 100:
            if self.piles[i] == []:
                stroke(0, 0, 100)
                strokeWeight(3)
                rect(30+i*(cardwidth+20), 160, cardwidth, cardlength)
            else:
                n = min((mouseY-160)//20, len(self.piles[i])-1)
                stroke(0, 0, 100)
                strokeWeight(3)
                rect(30+i*(cardwidth+20), 160+n*20, cardwidth, 20*(len(self.piles[i])-n)+80)
        
        # highlight menu button
        if 30 < mouseX < 100 and 30 < mouseY < 60:
            noFill()
            strokeWeight(3)
            stroke(0, 0, 100)
            rect(30, 30, cardwidth, 30)
        
        # highlight undo button        
        if 30 < mouseX < 100 and 100 < mouseY < 130:
            noFill()
            stroke(0, 0, 100)
            strokeWeight(3)
            rect(30, 100, 70, 30)
        
        # highlight addons
        if 30 < mouseY < 130 and 910-(len(self.addons)-1)*20-cardwidth < mouseX < 910-(len(self.addons)-1)*20:
            if self.addons != []:
                noFill()
                stroke(0, 0, 100)
                strokeWeight(3)
                rect(910-(len(self.addons)-1)*20-cardwidth, 30, 70, 100)
        
        # highlight hint button
        if 500 < mouseX < 600 and 60 < mouseY < 100:
            noFill()
            strokeWeight(3)
            stroke(0, 0, 100)
            rect(500, 60, 100, 40)
            
    def clicked(self):
        self.checkexit()
        self.checkundo()
        self.checkaddon()
        self.checkhint()
        
    def checkexit(self):
        if 30 < mouseX < 100 and 30 < mouseY < 60:
            menu.rewind()
            menu.play()
            self.gameon = False
            self.gamestart()
    
    def checkundo(self):    
        if 30 < mouseX < 100 and 100 < mouseY < 130:
            self.undotimes += 1
            if self.undotimes != 0 and self.moves != 70 and self.moves != 100 and self.undotimes%5 == 0:
                undo5.rewind()
                undo5.play()
            
            for pi in self.piles:
                for c in pi:
                    if len(c.p) == 1:
                        # if the game just starts or an addon is just distributed, no undo
                        return
            self.moves += 1
            self.checkmoves()    # whether or not play sound
            # see which cards changed piles in the last move
            for pi in self.piles:
                updatelist = []
                for c in pi:
                    if c.p[len(c.p)-1] != c.p[len(c.p)-2]:
                        updatelist.append(c)
                if updatelist != []:
                    for c in updatelist:
                        target = c.p[len(c.p)-1]
                        home = c.p[len(c.p)-2]
                        self.piles[target-1].remove(c)
                        self.piles[home-1].append(c)
                    break
           
            # every card goes back one in pile history   
            for pi in self.piles:
                cnt = 0
                for c in pi:
                    c.p.pop()
                    c.num = cnt
                    cnt += 1
                    c.fuh.pop()
                    if c.fuh[len(c.fuh)-1] == 0:
                        c.cover()
    
    def checkaddon(self):
        if self.addons != []:
            if 30 < mouseY < 130 and 910-(len(self.addons)-1)*20-cardwidth < mouseX < 910-(len(self.addons)-1)*20:
                addon = self.addons[len(self.addons)-1]
                i = 0
                # distribute one card to every pile
                for c in addon:
                    self.piles[i].append(c)
                    c.p.append(i+1)
                    c.num = len(self.piles[i])-1
                    c.fuh.append(1)
                    c.flip()
                    i += 1
                self.addons.remove(addon)
                
    def checkhint(self):
        if 500 < mouseX < 600 and 60 < mouseY < 100:
            self.hinttimes += 1
            if self.hinttimes != 0 and self.hinttimes%5 == 0:
                    hint5.rewind()
                    hint5.play()
            #the first priority is to check the empty piles
            hintlist =[] #for empyty pile
            for i in range(10):    
                if self.piles[i] == []:
                    hintlist.append(i)
            if hintlist != []:
                h = random.choice(hintlist)
                frameRate(3)
                stroke(200,0,0)
                noFill()
                strokeWeight(3)
                rect(30+h*(cardwidth+20), 160, cardwidth, cardlength)
            elif hintlist == []:
                # find the card to attach to 
                for j in range(10):
                    fpsequence = [] # for the faceup list for every pile
                    for c in self.piles[j]:
                       if c.faceup == True:
                           fpsequence.append(c)
                    checkline = ''
                    checkspade = 0
                    hintsequence = [] # for cards in order and with same suit, from bottom up
                    hintsequence.append(fpsequence[len(fpsequence)-1])
                    for c in fpsequence[len(fpsequence)-2::-1]:
                        if c.spade == fpsequence[len(fpsequence)-1].spade and c.r == hintsequence[len(hintsequence)-1].r+1:
                            hintsequence.append(c)
                        else:
                            break
                            # return hintsequence[-1].r+1
                    # check other piles last
                    for i in range(10):
                        b = False    # if we can find a hint, True we double break, False we check addons
                        if self.piles[i][len(self.piles[i])-1].spade == hintsequence[len(hintsequence)-1].spade and self.piles[i][len(self.piles[i])-1].r == hintsequence[len(hintsequence)-1].r+1:
                            frameRate(3)
                            stroke(200,0,0)
                            noFill()
                            strokeWeight(3)
                            rect(30+j*(cardwidth+20), 160+20*(len(self.piles[j])-len(hintsequence)), cardwidth, 20*(len(hintsequence)-1)+100)
                            stroke(50,0,0)
                            rect(30+i*(cardwidth+20), 160+20*(len(self.piles[i])-1), cardwidth, cardlength)
                            b = True
                            break
                    if b:
                        break
                # check addons
                if not b and self.addons != []:
                    frameRate(3)
                    stroke(200,0,0)
                    noFill()
                    strokeWeight(3)
                    rect(910-(len(self.addons)-1)*20-cardwidth, 30, cardwidth, cardlength) 
                elif not b and self.addons == []:
                    # no more possible moves, just quit
                    self.hinttimes = 0
                    nohint.rewind()
                    nohint.play() 
    
    def pressed(self):
        # id which pile mouse's at
        pile = (mouseX-30)//90
        if pile == 10:
            pile = 9
        elif pile == -1:
            pile = 0
        home = self.piles[pile]
        if len(home) != 0 and mouseY >= 160 and mouseY <= 160 + (len(home)-1)*20 + 100:
            cardn = (mouseY-160)//20
            if cardn > len(home)-1:
                cardn = len(home)-1
            sequence = home[cardn:]
            if home[cardn].faceup:
                # check if the sequence is in order
                if self.checkMovable(sequence):
                    # can be moved, move with mouse
                    self.mouselist = []
                    cnt = 0
                    for c in sequence:
                        c.moving = True
                        self.mouselist.append(c)
                        c.num = cnt
                        home.remove(c)
                        cnt += 1
        
    def released(self):
        if self.mouselist != []:
            # id target pile
            pile = (mouseX-30)//90
            if pile == 10:
                pile = 9
            elif pile == -1:
                pile = 0
            target = self.piles[pile]
            home = self.piles[self.mouselist[0].p[len(self.mouselist[0].p)-1]-1]
            if mouseY >= 160 + (len(target)-1)*20 and mouseY <= 160 + (len(target)-1)*20 + 100:
                if self.checkAcceptable(pile, target):
                    # can accept
                    self.moves += 1
                    self.checkmoves()
                    # flip the last card from the home pile
                    if home != [] and not home[len(home)-1].faceup:
                        home[len(home)-1].flip()
                    # append cards to target
                    for c in self.mouselist:
                        target.append(c)
                    # relabel cards
                    for n in range(len(target)):
                        target[n].num = n
                        target[n].moving = False
                    for pi in range(1, 11):
                        for c in self.piles[pi-1]:
                            c.p.append(pi)
                            c.fuh.append(int(c.faceup))
                    # check possible win
                    possiblewin = []
                    for c in target:
                        if c.faceup:
                            possiblewin.append(c)
                    if len(possiblewin) >= 13: 
                        pw =  possiblewin[-1:-14:-1]    
                        self.win = self.checkwin(target, pw)
                else:    # not acceptable, move back to home
                    for c in self.mouselist:
                        home.append(c)
                        c.moving = False
                        c.num = len(home)-1
            else:     # release outside the pile zone, move back to home
                 for c in self.mouselist:
                    home.append(c)
                    c.moving = False
                    c.num = len(home)-1   
            self.mouselist = []
    
    def checkMovable(self, sequence):
        checkline = '.'
        checkspade = 0
        for c in sequence:
            checkline += (str(c.r))
            checkline += '.'
            checkspade += int(c.spade)
        if checkline in '.13.12.11.10.9.8.7.6.5.4.3.2.1.':
            if checkspade == 0 or checkspade == len(sequence): 
                return True
            else:
                return False
        else:
            return False

    def checkAcceptable(self, p, target):
        if target == []:
            return True        
        else:
            if target[len(target)-1].faceup and target[len(target)-1].r - 1 == self.mouselist[0].r:
                return True
            else:
                return False        
    
    def checkmoves(self):
        if self.moves == 70:
            move70.rewind()
            move70.play()
        elif self.moves == 100:
            move100.rewind()
            move100.play()
                            
    def checkwin(self, target, pw):
        checkline = ''
        checkspade = 0
        for c in pw:
            checkline += (str(c.r))
            checkline += '.'
            checkspade += int(c.spade)
        if checkline == '1.2.3.4.5.6.7.8.9.10.11.12.13.':
            if checkspade == 0 or checkspade == 13:     # either all spade or all heart
                for c in pw:
                    target.remove(c)
                if target != [] and not target[len(target)-1].faceup:
                    target[len(target)-1].flip()
                if checkspade == 0:    # all spade
                    self.done.append(self.doneimg2)
                else:     # all heart
                    self.done.append(self.doneimg1)
                for pi in range(10):
                    for c in self.piles[pi]:
                        c.fuh.append(int(c.faceup))
                        c.p = [pi+1]
                if len(self.done) == 1:
                    win1.rewind()
                    win1.play()
                elif len(self.done) == 4:
                    win4.rewind()
                    win4.play()
                elif len(self.done) == 7:
                    win7.rewind()
                    win7.play()
                elif len(self.done) == 8:
                    winning.rewind()
                    winning.play()
                    # write record
                    if self.spade:
                        file = open(path + 'scoreboard/1.csv', 'a')
                    else:
                        file = open(path + 'scoreboard/2.csv', 'a')
                    file.write(',' + str(self.moves))
                    file.close()
                    return True
            else:
                return False
        else:
            return False
                
class Addon(list):    # distribute one new card to each pile when clicked
    def __init__(self, order):
        self.order = order
        self.backimg = loadImage(path + 'images/back.jpg')
    
    def display(self):
        image(self.backimg, 910-50-(self.order+1)*20, 30, cardwidth, cardlength)
    
class Pile(list):
    def __init__(self, order):
        self.order = order
            
g = Game()
easywelcome = player.loadFile(path + 'sounds/easywelcome.mp3')
hardwelcome = player.loadFile(path + 'sounds/hardwelcome.mp3')
move70 = player.loadFile(path + 'sounds/move70.mp3')
move100 = player.loadFile(path + 'sounds/move100.mp3')
hint5 = player.loadFile(path + 'sounds/hint5.mp3')
nohint = player.loadFile(path + 'sounds/nohint.mp3')
menu = player.loadFile(path + 'sounds/menu.mp3')
undo5 = player.loadFile(path + 'sounds/undo5.mp3')
winning = player.loadFile(path + 'sounds/winning.mp3')
win1 = player.loadFile(path + 'sounds/win1.mp3')
win4 = player.loadFile(path + 'sounds/win4.mp3')
win7 = player.loadFile(path + 'sounds/win7.mp3')
        
def setup():
    size(940, 800)
    background(100)

def draw():
    frameRate(15)
    image(g.bgimg, 0, 0)
    
    if g.win:
        textSize(50)
        text('CONGRATULATIONS!', 250, 300)
    elif not g.gameon:
        g.gamestart()        
    else:
        g.display()
    
def mouseClicked():
    if not g.gameon:   # menu
        if 300 < mouseX < 450 and 350 < mouseY < 400:      # easy
            g.__init__(spade = True, win = False, gameon = False)
            g.gameon = True
            easywelcome.rewind()
            easywelcome.play()
            g.display()
        elif 300 < mouseX < 450 and 480 < mouseY < 530:    # hard
            g.__init__(spade = False, win = False, gameon = False)
            g.gameon = True
            hardwelcome.rewind()
            hardwelcome.play()
            g.display()        
    elif g.gameon and not g.win:
        g.clicked()
    elif g.win:
        time.sleep(7)
        g.win = False
        g.gameon = False
        g.gamestart()
        
def mousePressed():
    if g.gameon and not g.win:
        g.pressed()

def mouseReleased():
    if g.gameon and not g.win:
        g.released()
