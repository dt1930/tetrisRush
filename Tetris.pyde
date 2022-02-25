import os
import random
path = os.getcwd()
NUM_ROWS=20          #constant variable for number of rows
NUM_COLS=10          #constant variable for number of cols
CELL_HEIGHT=20       #constant variable for the height of cell
CELL_WIDTH=20        #constant variable for the width of cell
board_width=CELL_WIDTH*NUM_COLS     #width of window
board_height=CELL_HEIGHT*NUM_ROWS   #height of window

class block:
    
    def __init__(self,row,col,R=255,G=255,B=255):
        self.r=row     #attribute for determining block's row
        self.c=col     #attribute for determining block's column
        self.R=R       #attribute for filling red color level
        self.G=G       #attribute for filling green color level
        self.B=B       #attribute for filling blue color level
        self.colorValue=self.R+self.G+self.B    #attribute for sum of color levels
        
    def show(self):
        fill(self.R,self.G,self.B)
        rect(self.c * CELL_WIDTH, self.r * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)   #drawing a rectangle to represent block
   
    def display(self):
        self.r=self.r+1   #block moved by 1 row
        self.show() 
        
class Game(list):           #game class inherits from list
    def __init__(self):
        self.speed=0       #attribute for changing the speed of falling blocks
        self.counter=0     #attribute for counting number of blocks
        self.scrValue=0    #attribute for recording score
        self.randomBlock() #calling randomBlock() to instantiate first block when the game starts
    
                                            
    def randomBlock(self):          #method to generate random block
        c=0
        value=random.randint(0,NUM_COLS-1)
        for item in self:
            if item.c==value:
                c=c+1
        while c==NUM_ROWS:          #while loop to generate block in a different column if the column is already filled
            c=0
            value=random.randint(0,NUM_COLS-1)
            for item in self:
                if item.c==value:
                    c=c+1
        colorsList=[[255,51,52],[12,150,228],[30,183,66],[246,187,0],[76,0,153],[255,255,255],[0,0,0]]
        b=random.randint(0,6)
        self.append(block(0,value,colorsList[b][0],colorsList[b][1],colorsList[b][2]))
        

            
    def startGame(self):
        for i in range(self.counter):      #displaying the blocks that settled on bottom or top of other blocks
            self[i].show()
        if self[self.counter].r!=NUM_ROWS-1 and self.belowCheck(self[self.counter].r,self[self.counter].c):
            self[self.counter].display()
            self.winCheck()
        elif len(self)==NUM_ROWS*NUM_COLS:    
            self[len(self)-1].show()
            self.gameOver()
        else:
            self[self.counter].show()
            self.counter=self.counter+1     
            self.speed=self.speed+0.2      #increasing the speed of falling blocks 
            self.randomBlock()
            
            
    
    def belowCheck(self,rw,cl):      #method to check the row below is empty or not
        for item in self:
            a=item.r
            b=item.c
            if rw+1==a and cl==b :
                return False
        return True
    
    
    def gameOver(self):             #method called after all the cells are filled
        background(210)
        textSize(15)
        fill(0,0,0)
        text("Game Over. Score:"+str(self.scrValue),board_width/6,board_height/2)

    
    def winCheck(self):                 #method to check if four cells are of same color
        checkingList=[]
        itemList=[]
        filteredList=[]
        a=self[self.counter].c
        b=self[self.counter].r
        if b<=NUM_ROWS-4:
            for item in self:
                if self[self.counter].colorValue==item.colorValue and a==item.c:
                    checkingList.append(item.r)
                    itemList.append(item)
                    
            for c in checkingList:
                if c+1 in checkingList and c+2 in checkingList and c+3 in checkingList:
                    win=True
                    for j in itemList:
                        if j.r==c:
                            filteredList.append(j)
                        if j.r==c+1:
                            filteredList.append(j)
                        if j.r==c+2:
                            filteredList.append(j)
                        if j.r==c+3:
                            filteredList.append(j)
                else:
                    win=False
            if win==True:                           #resetting values if four cells are of same color
                self.scrValue=self.scrValue+1
                self.counter=self.counter-4
                self.speed=0
                for i in filteredList:              #removing the four matched cells
                    self.remove(i)
                
    def display(self):
        for r in range(NUM_ROWS):
            line(0,r*CELL_HEIGHT,board_width,r*CELL_HEIGHT )
        for c in range(NUM_COLS):
            line(c*CELL_WIDTH,0,c*CELL_HEIGHT,board_height)
        textSize(15)
        fill(0,0,0)
        text("Score: "+str(self.scrValue),board_width-3.5*CELL_WIDTH,0.8*CELL_HEIGHT)  #displaying score on top right corner of the window
        self.startGame()        #calling the method to start the game
            
    
    def left(self,rw,cl):           #method called after pressing left arrow
        for item in self:
            a=item.r
            b=item.c
            if cl-1==b and rw==a:
                return False
        return True
    
    def right(self,rw,cl):         #method called after pressing right arrow
        for item in self:
            a=item.r
            b=item.c
            if cl+1==b and rw==a:
                return False
        return True
    
    def reset(self):              #method to reset the game to its initial values
        i=0
        self.speed=0
        self.counter=0
        self.scrValue=0
        while len(self)!=0:
            self.pop(i)
        self.randomBlock()
        
        
game=Game()   #instantiating Game class

def setup():
    size(board_width,board_height)
    background(210)
    stroke(180)
    
def draw():
    #slow down the game by not displaying every frame
    if frameCount%(max(1, int(8 - game.speed)))==0 or frameCount==1:
        background(210)
        #this calls the display method of the game class
        game.display()
    
def keyPressed():
    if keyCode==LEFT:
        #checking the conditions on clicking left arrow
        if game.left(game[game.counter].r,game[game.counter].c)==True and game[game.counter].c>0:
            game[game.counter].c=game[game.counter].c-1
            game.winCheck()
    
    if keyCode==RIGHT:
        #checking the conditions on clicking right arrow
        if game.right(game[game.counter].r,game[game.counter].c)==True and game[game.counter].c<NUM_COLS-1:
            game[game.counter].c=game[game.counter].c+1
            game.winCheck()
    
def mousePressed():
    #mouse click resets the game after all cells are filled
    if len(game)==NUM_ROWS*NUM_COLS:
        game.reset()
    

        
    

    
