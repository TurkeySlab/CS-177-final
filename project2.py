'''
# Project 2
# Max Williams
# project2.py for CS 177
# This program simulates a pull shot game
'''


from graphics import*
from math     import*
from random   import randint
from time     import sleep, time

class Button:
    # This class creates button objects to be used on the GUI panel
    def __init__(self, center, width, height, label, colour):
        # constrcutor
        # center        : The center point of the button
        # width         : The width of the button
        # height        : The height of the button
        # label         : Text ( if any ) to be written on the button
        # colour        : Sets the buttons active colour
        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        
        p1 = Point( self.xmin, self.ymin )
        p2 = Point( self.xmax, self.ymax )
        
        self.rect = Rectangle(p1, p2)
        self.label = Text(center, label)
        self.colour = colour

        self.activate()
         
    def activate(self):
        # sets the colour of the button to active
        self.rect.setFill(self.colour)
    def deactivate(self, col):
        # sets the colour to the desired deactive colout
        self.rect.setFill(col)
    def clicked(self, p):
        # Does checks for if the button has been clicked
        click = False
        try:
            click = ( self.xmin <+ p.getX() <= self.xmax and
                      self.ymin <+ p.getY() <= self.ymax     )
            return click
        except: 
            return click
# ===== ===== ===== ===== ===== ===== ===== ===== ===== #
def highScores():
    # initializes variables
    w = GraphWin("High Scores!", 200, 400)
    w.setBackground("navy")
    rBox = Rectangle(Point(10,10), Point(190, 360))
    rBox.setOutline("white")
    rBox.setWidth("5")
    bClose = Button(Point(100,380), 150, 30, "Close!", "white")
    # draws objects
    bClose.rect.draw(w)
    bClose.label.draw(w)
    rBox.draw(w)
    
    # used for displaying scores
    lables = ['1.','2.','3.','4.','5.','6.','7.','8.','9.','10.']
    scores = getScores()
    
    # removes header from scores list
    del scores[0]
    del scores[0]
    
    yVal = 70
    i = 0
    while i < 10:
        # prints the position labels
        place = Text(Point(30, yVal), i)
        place.setTextColor('white')
        place.draw(w)
        try:
            # prints the score and assoiated name for the top ten
            name = Text(Point(100, yVal), "{0:^15}".format(scores[i][0]) )
            score = Text(Point(170, yVal),"{0:>5}".format(scores[i][1]) )
            
            score.setTextColor('white')
            score.draw(w)
            
        except Exception as e:
            # catchs out of bounds exception and prints place text in empty positions
            print(e)
            name = Text(Point(85, yVal), "< Empty >")
            
        name.setTextColor('white')
        name.draw(w)
        # increase line values
        yVal += 30
        i    += 1
        
        
    clicked = False
    while not clicked:
        # holds code inside "High Scores" window until closed
        cp = w.getMouse()
        if(bClose.clicked(cp)):
            clicked = True
            w.close()        
def getScores():
    # gets the previous high scores
    r = open("top_scores.txt", "r")
    # data is stored as
    # head ( 2 lines ) 
    # name \t  score \n
    scores = []
    for line in r.readlines():
        # reads into list 'scores' with each element being a list of ['name', 'score']
        scores.append(line.strip().split('\t'))
    r.close()
    # returns the scores list to be used
    return scores
def setScores(name, score):
    # sets the high scores 
    added = False
    try:
        # checks if the highscores file exists
        scores = getScores()
        del scores[0]
        del scores[0]
        
        
        i = 0
        while( i < len(scores) ):
            # compares scores
            if(float(score) >= float(scores[i][1])):
                added = True
                scores.insert(i, [name, score])
                break;
            i += 1  
            
    except Exception as e:
        print(e)
        # if it does not program assumes the user is a cheater and adds 
        # last score to the top_scores and creates the file later
        scores = [[name, score]]
    
    if(len(scores) < 10 and not added):
        # if the value does not change the high scores listing but the score board is not full
        # the name is then added to teh end
        scores.append([name, score])
    
    # creates writer and writes header
    w = open("top_scores.txt", 'w')
    i = 0
    w.write("Top 10 Scores\n")
    w.write("=============\n")
    
    while( i < len(scores) ):
        # writes the high score values into "top_scores.txt" to be used later
        w.write(scores[i][0])
        w.write('\t')
        w.write(str(scores[i][1]))
        w.write('\n')
        i += 1
    w.close()
    
def creation():
    # this method defines a series of shapes and button objects
    # these objects are added to a list to be later drawn                                                                                                                    (because thats realistic)
    values = []
    w = GraphWin("Pull! The shot put game", 400, 600)
    gP = Rectangle(Point(25,40), Point(375, 170))
    t1 = Text(Point(200, 25), "Game Panel")

#Highscores
    # high scores section and header    
    rHigh = Rectangle(Point(25, 430), Point(375, 580))
    tHigh = Text(Point(200, 405), 'High Scores')
    pHigh = 'null'
    
    bHighU = Button(Point(360, 460), 20, 30, '↑', 'light grey')
    bHighU.activate()
    bHighD = Button(Point(360, 550), 20, 30, '↓', 'light grey')
    bHighD.activate()
#User panel    
    # new game button and colours it
    bNew = Button(Point(85, 75), 110, 50, "New Game", "light green")
    bNew.deactivate('light grey')
    # quit button and colours it
    bQuit = Button(Point(315, 75), 110, 50, "Quit", "tomato")
    bQuit.activate()
    # player name entry box and display text header
    tPlayer = Text(Point(90, 120), " Player")
    ePlayer = Entry(Point(95, 145), 12)
    # round disply and header text
    tRound = Text(Point(200, 120), "Round")
    rRound = Rectangle(Point(180, 130), Point(220, 160))
    tNum   = Text(Point(200, 145), '0')
    # score display and header text
    tScore = Text(Point(330, 120), "Score")
    rScore = Rectangle(Point(310, 130), Point(350, 160))
    tPoint = Text(Point(330, 145), '0')
    
#Target Panel

    tP = Rectangle(Point(25, 220), Point(375, 380))
    tT = Text(Point(200, 195), "Target Panel")
    tAngle = Text(Point(90, 250), "Angle")
    rAngle = Rectangle(Point(60,260), Point(120, 300))
    tAVal  = Entry(Point(90,280), 5)
    tAVal.setText("45")
    bAU = Button(Point(135, 270), 20, 20, '+', 'light grey')
    bAD = Button(Point(135, 290), 20, 20, '-', 'light grey')
    
    tPower = Text(Point(200, 250), "Power")
    rPower = Rectangle(Point(170, 260), Point(230, 300))
    tPVal  = Entry(Point(200, 280), 5)
    tPVal.setText("10")
    bPU = Button(Point(245, 270), 20, 20, '+', 'light grey')
    bPD = Button(Point(245, 290), 20, 20, '-', 'light grey')

    tGravy = Text(Point(310, 250), "Gravity")
    rGravy = Rectangle(Point(280, 260), Point(340, 300))
    tGVal  = Entry(Point(310,280), 5)
    tGVal.setText("10")
    bGU = Button(Point(355, 270), 20, 20, '+', 'light grey')
    bGD = Button(Point(355, 290), 20, 20, '-', 'light grey')
    
    bPull1 = Button(Point(420, 350), 200, 50, "PULL DOUBLE!", "yellow")
    bPull1.deactivate('pink')
    bPull2 = Button(Point(120, 350), 200, 50, "PULL SINGLE!", "yellow")
    bPull2.deactivate('pink')

    highList = []
    y = 450
    for i in range(10):
        highList.append( Text(Point(35, y), i))
        y += 50
# appending to the later return in a more organized style
    #  0 - 4
    values.append(gP)
    values.append(t1)
    values.append(bNew)
    values.append(rHigh)
    values.append(bQuit)
    #  5 - 9
    values.append(tPlayer)
    values.append(ePlayer)
    values.append(tRound)
    values.append(rRound)
    values.append(tNum)
    # 10 - 14
    values.append(tScore)
    values.append(rScore)
    values.append(tPoint)
    values.append(tP)
    values.append(tT)
    # 15 - 19
    values.append(tAngle)
    values.append(rAngle)
    values.append(tAVal)
    values.append(bAU)
    values.append(bAD)
    # 20 - 24 
    values.append(tPower)
    values.append(rPower)
    values.append(tPVal)
    values.append(bPU)
    values.append(bPD)
    # 25 - 29
    values.append(tGravy)
    values.append(rGravy)
    values.append(tGVal)
    values.append(bGU)
    values.append(bGD)
    # 30 - 34
    values.append(bPull1)
    values.append(tHigh)
    values.append(highList)
    values.append(bHighU)
    values.append(bHighD)
    # 35
    values.append(w) 
    values.append(bPull2)  
    
    return ( w, values )

def drawer(w, values):
    # draws the values that were created in 'creation( )'
    # values[32].draw(w)
    for i in values[32]:
        i.draw(w)
        
    bg = Rectangle(Point(-1, -1), Point(401, 430))
    bg.setFill('white')
    bg.setOutline('white')
    bg.draw(w)
    
    for vis in values:
        if(type(vis) == Button):
            # done because the button class has special attributes for drawing
            # as it is not a graphics object but a self made class with special attributes
            vis.rect.draw(w)
            vis.label.draw(w)
        else:
            # all other values
            try:
                vis.draw(w)
            except:
                print(vis)

    # TODO
    '''
    Modify drawer to layer the highscores panel to be the first drawn then skipped
    '''
    return values
def diskClicked(disk, p):
    # method for the game to make conditionals easier to read
    click = False
    try:
        if ((disk.getP1().getX() < p.getX() and disk.getP2().getX() > p.getX()) and
            (disk.getP1().getY() < p.getY() and disk.getP2().getY() > p.getY())     ):
            click = True
            # if the object was clicked then it returns true
        return click
    except: 
        # if not then it returns False
        return click
def newGameWindow():
    # creates the actual game to be played
    w = GraphWin("The Game!", 600, 600)
    # Negative done to hide the borders
    # Creates the sky and ground2:34 PM 11/28/2017
    sky = Rectangle(Point(-1, -1),   Point(600, 450))
    sky.setFill('#00a2e8')
    drt = Rectangle(Point(-1, 450), Point(600, 600))
    drt.setFill('#00a202')
    drt.setOutline('#00a202')
   
    # Draws the stuff ( like the method says )
    Image(Point(300,225),'background.png').draw(w)
    drt.draw(w)
    
    return w
def newGame(w, pwr, ang, grvy, points, rnd):
    # creates the disk and holds all game related things
    dskL = Circle(Point(590, int(randint(350, 450))), 8)
    dskR = Circle(Point(10, int(randint(350, 450))), 8)
    rabL = Circle(Point(590, 450), 8)
    rabR = Circle(Point(10 , 450), 8)
    dskL.setFill('dark grey')
    dskR.setFill('dark grey')
    rabL.setFill('dark grey')
    rabR.setFill('dark grey')
    
    rand = randint(1, 10)
    
    if rand >= 5:
        dskL.draw(w)
        dskR.draw(w)
    else:
        rabL.draw(w)
        rabR.draw(w)
    
    # special conditionals for when the disks are done 
    L, R = 0, 0
    # movement values
    dx = pwr * cos(radians(ang))
    if(dx < 0):
        dx *= -1
    
    dy = -(pwr * sin(radians(ang)))
        
    points = points / 100 / rnd
    while( True ):
        # loop runs until the disk are both "shot" or have reached the end
        sleep(.05)
        
        # re defines variables for conditionals 
        cp = w.checkMouse()
        rP = dskR.getCenter()
        lP = dskL.getCenter()
        rr = rabR.getCenter()
        lr = rabL.getCenter()
        
        if( diskClicked(dskR, cp) ):
            # if the right moving disk is clicked
# addes hit marker 
            l = Text(Point(cp.getX(), cp.getY() - 30),"hit")
            l.draw(w)
            points += .5
            dskR.undraw()
            rabR.undraw()
            R = 1
        if( diskClicked(dskL, cp) ):
            # if the left moving disk is clicked
# addes hit marker 
            r = Text(Point(cp.getX(), cp.getY() - 30),"hit")
            r.draw(w)
            points += .5
            dskL.undraw()
            rabL.undraw()
            L = 1
            
        if( rP.getX() >= 600 or rP.getY() >= 450 ):
            # conditional to check if right moving disk is in play
            R = 1
        if( lP.getX() <= 0 or lP.getY() >= 450 ):
            # conditional to check if left moving disk is in play
            L = 1
        if( rr.getX() >= 600 or rr.getY() >= 450 ):
            # conditional to check if right moving disk is in play
            Q = 1
        if( lr.getX() <= 0 or lr.getY() >= 450 ):
            # conditional to check if left moving disk is in play
            T = 1
            
        if( L == 1 and R == 1 and Q == 1 and T == 1):
            # conditional to break the loop if the balls are done
            print("end")
            dskL.undraw()
            dskR.undraw()
            rabR.undraw()
            rabL.undraw()
            break

        print(dx,dy, sep = '\t\t')
        
        # moves the disks after all conditions are done
        if( R == 0):
            # moves when not out of bounds
            dskR.move(dx, dy)
        if( L == 0):
            # moves when not out of bounds
            dskL.move(-dx, dy)
        if( Q == 0):
            # moves when not out of bounds
            rabR.move(dx, 0)
        if( T == 0):
            # moves when not out of bounds
            rabL.move(-dx, 0)
            
            
        # unable to get perfect trajectory equation
        dy += 1/ grvy
        # dx = pwr * cos(radians(ang))
        # dy = pwr * sin(radians(ang)) - 1/grvy
        # print(dx, dy, sep ="\t|\t")

        
    
    return round((points/rnd * 100), 2)
def operation(values, ngW):
    pullClickable = [False, False, False, False]  # Angle, Power, Gravity, Name
    newClickable  = [False, True]                 # Name, !running game
    highIndex     = -1                             # used to keep the highscores view window between min and max values

    # creates variables form list of all graphics objects
    bNew = values[2]
    bHigh = values[3]
    bQuit = values[4]
    ePlayer = values[6]
    tRound = values[9]
    tPoint = values[12]
    tAVal = values[17]
    bAU = values[18]
    bAD = values[19]
    tPVal = values[22]
    bPU = values[23]
    bPD = values[24]
    tGVal = values[27]
    bGU = values[28]
    bGD = values[29]
    bPull1 = values[30]   
    highList = values[32] 
    bHighU = values[33]
    bHighD = values[34]
    w = values[35]

    while( ePlayer.getText() == '' ):
        # re-check until text is filled
        bNew.deactivate('light grey')
        bPull1.deactivate('pink')
        bPull2.deactivate('pink')
        cp = w.checkMouse()
        if(bQuit.clicked(cp) ):
            bQuit.deactivate('light grey')
            w.close()
        if(bHighU.clicked(cp)):
            # moves highscore up
            bHighU.deactivate('white')
            
            if(highIndex > -1):
                for i in highList:
                    i.move(0, 50)
                highIndex -= 1
            
            sleep(.05)
            bHighU.activate()
        if(bHighD.clicked(cp)):
            # moves highscore down
            bHighD.deactivate('white')
            
            if(highIndex < 6):
                for i in highList:
                    i.move(0, -50)
                highIndex += 1
          
            sleep(.05)
            bHighD.activate()
            
    bNew.activate()
    bPull1.activate()
    bPull2.activate()
    
    # Name is filled at this point new game and pull are active buttons
    match = 0
    while True:
        
        if( ePlayer.getText() == ''):
            # if name is removed
            while( ePlayer.getText() == '' ):
                # re-check until text is filled
                bNew.deactivate('light grey')
                bPull1.deactivate('pink')
                bPull2.deactivate('pink')
            bNew.activate()
            bPull1.activate()
            bPull2.activate()
            
        # active clicks!
        cp = ngW.checkMouse()
    
    # Game buttons
    
    # High Scores
        if(bHighU.clicked(cp)):
            # moves highscore up
            bHighU.deactivate('white')
           
            if(highIndex > -1):
                for i in highList:
                    i.move(0, 50)
                highIndex -= 1
           
            sleep(.05)
            bHighU.activate()
            
        if(bHighD.clicked(cp)):
            # moves highscore down
            bHighD.deactivate('white')
            
            if(highIndex < 6):
                for i in highList:
                    i.move(0, -50)
                highIndex += 1
            
            sleep(.05)
            bHighD.activate()
            
    # Quit
        if(bQuit.clicked(cp)):
            # sets scores before closing
            bQuit.deactivate('light grey')
            sleep(.5)
            setScores(ePlayer.getText(), tPoint.getText())
            w.close()
        if( ePlayer.getText() == '' ):
            newClickable[0] = False
        else:
            newClickable[0] = True
        
        if( newClickable[0] and newClickable[1] ):
            bNew.activate()
            if(bNew.clicked(cp)):
                tGVal.setText('10')
                tPVal.setText("10")
                tAVal.setText("45")
                tPoint.setText("0")
                ePlayer.setText("")
                while( ePlayer.getText() == '' ):
                    # re-check until text is filled
                    bNew.deactivate('light grey')
                    bPull1.deactivate('pink')
                    bPull2.deactivate('pink')
                bNew.activate()
                bPull1.activate()
                bPull2.activate()
        
    # Angle, Power, Gravity buttons
        # Angles
        if(bAU.clicked(cp)):
            bAU.deactivate('red')
            if( int(tAVal.getText()) >= 60 ):
                tAVal.setText('60')
            elif( int(tAVal.getText()) <= 30 ):
                tAVal.setText('30')
            else:
                tAVal.setText(int(tAVal.getText()) + 1)
        if(bAD.clicked(cp)):
            bAD.deactivate('red')
            if( int(tAVal.getText()) <= 30 ):
                tAVal.setText('30')
            elif( int(tAVal.getText()) >= 60 ):
                tAVal.setText('60')
            else:
                tAVal.setText(int(tAVal.getText()) - 1)
    # Power       
        if(bPU.clicked(cp)):
            bPU.deactivate('red')
            if( int(tPVal.getText()) >= 50 ):
                tPVal.setText('50')
            elif( int(tPVal.getText()) <= 5):
                tPVal.setText('5')
            else:
                tPVal.setText(int(tPVal.getText()) + 1)
        if(bPD.clicked(cp)):
            bPD.deactivate('red')
            if( int(tPVal.getText()) <= 5):
                tPVal.setText('5')
            elif( int(tPVal.getText()) >= 50 ):
                tPVal.setText('50')
            else:
                tPVal.setText(int(tPVal.getText()) - 1)
    # Gravity     
        if(bGU.clicked(cp)):
            bGU.deactivate('red')
            if( int(tGVal.getText()) >= 25):
                tGVal.setText('25')
            elif( int(tGVal.getText()) <= 3 ):
                tGVal.setText('3')
            else:
                tGVal.setText(int(tGVal.getText()) + 1)
        if(bGD.clicked(cp)):
            bGD.deactivate('red')
            if( int(tGVal.getText()) <= 3 ):
                tGVal.setText('3')
            elif( int(tGVal.getText()) >= 25):
                tGVal.setText('25')
            else:
                tGVal.setText(int(tGVal.getText()) - 1)
    # Pull          
        # Angle
        if( int(tAVal.getText()) <= 60 and int(tAVal.getText()) >= 30 ):
            pullClickable[0] = True
        else:
            pullClickable[0] = False
        # Power
        if( int(tPVal.getText()) <= 50 and int(tPVal.getText()) >= 5  ):
            pullClickable[1] = True
        else:
            pullClickable[1] = False
        # Gravity
        if( int(tGVal.getText()) <= 25 and int(tGVal.getText()) >= 3  ):
            pullClickable[2] = True
        else:
            pullClickable[2] = False
        # Name
        if( ePlayer.getText() == '' ):
            pullClickable[3] = False
        else:
            pullClickable[3] = True
       
        # switch operation   
        if( pullClickable[0] and pullClickable[1] and pullClickable[2] and pullClickable[3] ):
            # button colour is changed
            bPull1.activate()
            bPull2.activate()
            if( bPull1.clicked(cp) ):
                # if user wants to play
                bPull1.deactivate("light grey")
                sleep(.2)
                bPull1.activate()
                
                # sets new to be unclickable
                newClickable[1] = True
                bNew.deactivate('light grey')
                
                match += 1
         
                cp = w.checkMouse()
                if(bQuit.clicked(cp)):
                    # sets scores before closing
                    bQuit.deactivate('light grey')
                    sleep(.5)
                    setScores(ePlayer.getText(), tPoint.getText())
                    w.close()

                tRound.setText(str(match))
                tPoint.setText( newGame( ngW, int(tPVal.getText()), int(tAVal.getText()), 
                                             int(tGVal.getText()), int(tPoint.getText()), int(tRound.getText()) )     )
                # re activates button
                newClickable[1] = False
                bNew.activate()
            bPull1.activate()
            bPull2.activate()
        else:
            bPull1.deactivate('pink')
            bPull2.deactivate('pink')
            
        # holds code for colour change of some buttons to appear
        sleep(.2)
        
        # resets buttons to be correct state
        bAU.activate()
        bAD.activate()
        
        bPU.activate()
        bPD.activate()
        
        bGU.activate()
        bGD.activate()
        
        
        
    return w
   
def main():
    # handles the order of the games
    w, values = creation()
    ngW       = newGameWindow()
    values    = drawer(w, values)
    
    operation(values, ngW)
    
main()



















