#add_library('minim')
# sound effect
# add creepy voices asking 'wanna continue? 100 moves already'

# exit and start a new game
# winning screen

import os
import random
import time
path = os.getcwd() + '/'
#player = Minim(this)
cardwidth = 70
cardlength = 100

class Card:
    def __init__(self, num, r, spade=True, faceup=False, moving=False):
        self.p = []      # the pile history of the card
        self.num = num   # the order of it in this pile
        self.r = r       # the rank
        self.spade = spade
        self.faceup = faceup
        self.fuh = []    # keep track of face up history
        self.moving = moving
        self.img = loadImage(path + 'images/back.jpg')
        
    def display(self):
        if not self.moving:
            image(self.img, 30+(self.p[len(self.p)-1]-1)*(cardwidth+20), 160+self.num*20, cardwidth, cardlength)
        else:
            image(self.img, mouseX-cardwidth/2, mouseY-10+self.num*20, cardwidth, cardlength)
    
    def flip(self):
        if not self.faceup:
            self.img = loadImage(path + 'images/' + str(int(self.spade)) + str(self.r) + '.png')
            self.faceup = True
    
    def cover(self):
        if self.faceup:
            self.img = loadImage(path + 'images/back.jpg')
            self.faceup = False  
               
class Deck(list):
    def __init__(self, spade=True):
        self.spade = spade
        self.ranks = []
        
        for i in range(13):
            self.ranks.append(i+1)
        
        if self.spade:
            for i in range(8):
                for r in self.ranks:
                    self.append(Card(0, r, True, False))
        else:
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
        self.gameon = gameon
        self.spade = spade
        self.deck = Deck(self.spade)
        self.deck.shuffle_cards()
        self.mouselist = []
        self.done = []
        self.doneimg1 = loadImage(path + 'images/11.png')
        self.doneimg2 = loadImage(path + 'images/01.png')
        self.bgimg = loadImage(path + 'images/bg.jpeg')
        #self.easywelcome = player.loadFile(path + 'sounds/easywelcome.mp3')
        
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
        rect(300, 350, 150, 50)
        rect(300, 480, 150, 50)
        textSize(40)
        text('EASY', 325, 390)
        text('HARD', 320, 520) 
        textSize(30)
        text('Record: ', 470, 390)
        text('Record: ', 470, 520)
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
        
        #if self.spade:
        #    self.easywelcome.rewind()
        #    self.easywelcome.play()
        
        for i in range(10):
            if self.piles[i] == []:
                stroke(200)
                noFill()
                strokeWeight(2)
                rect(30+i*(cardwidth+20), 160, cardwidth, cardlength)
        
        if self.done == []:
            rect(120, 30, cardwidth, cardlength)
        else:
            cnt = 0
            for i in self.done:
                image(i, 120+cnt*20, 30, cardwidth, cardlength)
                cnt += 1

        if self.addons == []:
            rect(840, 30, cardwidth, cardlength)
                
        for pile in self.piles:
            if len(pile) != 0:
                for card in pile:
                    card.display()
        
        if self.mouselist != []:
            for c in self.mouselist:
                c.display()
    
        for addon in self.addons:
            addon.display()
        
        i = (mouseX-30)//90
        if i == 10:
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
        
        if 30 < mouseX < 100 and 30 < mouseY < 60:
            noFill()
            strokeWeight(3)
            stroke(0, 0, 100)
            rect(30, 30, cardwidth, 30)
                
        if 30 < mouseX < 100 and 100 < mouseY < 130:
            noFill()
            stroke(0, 0, 100)
            strokeWeight(3)
            rect(30, 100, 70, 30)
        
        if 30 < mouseY < 130 and 910-(len(self.addons)-1)*20-cardwidth < mouseX < 910-(len(self.addons)-1)*20:
            if self.addons != []:
                noFill()
                stroke(0, 0, 100)
                strokeWeight(3)
                rect(910-(len(self.addons)-1)*20-cardwidth, 30, 70, 100)
        
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
            self.gameon = False
            self.gamestart()
    
    def checkundo(self):    
        if 30 < mouseX < 100 and 100 < mouseY < 130:
            for pi in self.piles:
                for c in pi:
                    if len(c.p) == 1:
                        # voice
                        return
            self.moves += 1
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
            #the first priority is to check the empty
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
            # find the card bigger 
            # randomly generate
            elif hintlist == []:
                for j in range(10):
                    fpsequence = [] # for the faceup list for every pile
                    for c in self.piles[j]:
                       if c.faceup == True:
                           fpsequence.append(c)
                    checkline = ''
                    checkspade = 0
                    hintsequence = [] #for unempty pile
                    hintsequence.append(fpsequence[len(fpsequence)-1])
                    for c in fpsequence[len(fpsequence)-2::-1]:
                        if c.spade == fpsequence[len(fpsequence)-1].spade and c.r == hintsequence[len(hintsequence)-1].r+1:
                            hintsequence.append(c)
                        else:
                            break
                            # return hintsequence[-1].r+1
                    #check other piles last
                    for i in range(10):
                        b = False
                        if self.piles[i][len(self.piles[i])-1].spade == hintsequence[len(hintsequence)-1].spade and self.piles[i][len(self.piles[i])-1].r == hintsequence[len(hintsequence)-1].r+1:
                            frameRate(3)
                            stroke(200,0,0)
                            noFill()
                            strokeWeight(3)
                            #hintsequence
                            rect(30+j*(cardwidth+20), 160+20*(len(self.piles[j])-len(hintsequence)), cardwidth, 20*(len(hintsequence)-1)+100)
                            stroke(50,0,0)
                            rect(30+i*(cardwidth+20), 160+20*(len(self.piles[i])-1), cardwidth, cardlength)
                            b = True
                            break
                    if b:
                        break
                #addon 
                if not b and self.addons != []:
                    frameRate(3)
                    stroke(200,0,0)
                    noFill()
                    strokeWeight(3)
                    rect(910-(len(self.addons)-1)*20-cardwidth, 30, cardwidth, cardlength) 
    
    def pressed(self):
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
                if self.checkMovable(sequence):
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
            pile = (mouseX-30)//90
            if pile == 10:
                pile = 9
            elif pile == -1:
                pile = 0
            target = self.piles[pile]
            home = self.piles[self.mouselist[0].p[len(self.mouselist[0].p)-1]-1]
            if mouseY >= 160 + (len(target)-1)*20 and mouseY <= 160 + (len(target)-1)*20 + 100:
                if self.checkAcceptable(pile, target):
                    self.moves += 1
                    if home != [] and not home[len(home)-1].faceup:
                        home[len(home)-1].flip()
                    for c in self.mouselist:
                        target.append(c)
                    for n in range(len(target)):
                        target[n].num = n
                        target[n].moving = False
                    for pi in range(1, 11):
                        for c in self.piles[pi-1]:
                            c.p.append(pi)
                            c.fuh.append(int(c.faceup))
                    possiblewin = []
                    for c in target:
                        if c.faceup:
                            possiblewin.append(c)
                    if len(possiblewin) >= 13: 
                        pw =  possiblewin[-1:-14:-1]    
                        self.win = self.checkwin(target, pw)
                else:
                    for c in self.mouselist:
                        home.append(c)
                        c.moving = False
                        c.num = len(home)-1
            else:
                 for c in self.mouselist:
                    home.append(c)
                    c.moving = False
                    c.num = len(home)-1   
            self.mouselist = []
    
    def checkMovable(self, sequence):
        checkline = ''
        checkspade = 0
        for c in sequence:
            checkline += (str(c.r))
            checkline += '.'
            checkspade += int(c.spade)
        if checkline in '13.12.11.10.9.8.7.6.5.4.3.2.1.':
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
                
    def checkwin(self, target, pw):
        checkline = ''
        checkspade = 0
        for c in pw:
            checkline += (str(c.r))
            checkline += '.'
            checkspade += int(c.spade)
        if checkline == '1.2.3.4.5.6.7.8.9.10.11.12.13.':
            if checkspade == 0 or checkspade == 13: 
                for c in pw:
                    target.remove(c)
                if target != [] and not target[len(target)-1].faceup:
                    target[len(target)-1].flip()
                if checkspade == 0:
                    self.done.append(self.doneimg2)
                else:
                    self.done.append(self.doneimg1)
                for pi in range(10):
                    for c in self.piles[pi]:
                        c.fuh.append(int(c.faceup))
                        c.p = [pi+1]
                if len(self.done) == 8:
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
            
g = Game()
        
def setup():
    size(940, 800)
    background(0, 255, 0)

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
    if not g.gameon:
        if 300 < mouseX < 450 and 350 < mouseY < 400:
            g.__init__(spade = True, win = False, gameon = False)
            g.gameon = True
            g.display()
        elif 300 < mouseX < 450 and 480 < mouseY < 530:
            g.__init__(spade = False, win = False, gameon = False)
            g.gameon = True
            g.display()        
    elif g.gameon and not g.win:
        g.clicked()
    elif g.win:
        time.sleep(5)
        g.win = False
        g.gameon = False
        g.gamestart()
        
def mousePressed():
    if g.gameon and not g.win:
        g.pressed()

def mouseReleased():
    if g.gameon and not g.win:
        g.released()
