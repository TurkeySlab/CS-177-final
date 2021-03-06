'''
# Project 2
# Max Williams
# project2.py for CS 177
# This program simulates a pull shot game
'''
'''
  #############################################################################
 ##########################    Our Custom Additions    #########################
#################################################################################
                                                                               ###
1) Hit-boxes                                                                   ###
    These boxes appear when the user clicks a disk to show user confirmation   ###
    that their click was reqistered and that they were given their points      ###
                                                                               ###
2) Clouds                                                                      ###
    Translucent '.png' clouds that hinder the players view of the pigeon disks ###
    Adds extra random challenge to the game making it more difficult to get a  ###
    score of 100                                                               ###
                                                                               ###
3) 'New name > New game' functionality                                         ###
    Kept the 'New Game' button, but added in functionality so when a new name  ### 
    is entered in the player name text box, the previous player's values are   ###
    reset                                                                      ###
                                                                               ###
4) 'Buttons' class                                                             ###
    Instead of using 'Rectangle' objects from 'graphics.py' we created a class ###
    that handles all operations for buttons making cleaner conditionals, more  ###
    readable code, and better functionality                                    ### 
                                                                               ### 
5) This pretty box!                                                            ###
    Reading and finding things can be hard. This way you wont miss a thing!    ###
                                                                               ###
#################################################################################
 ###############################################################################
  #############################################################################
'''


from graphics import*
from math     import*
from random   import randint
from time     import sleep

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
def getScores():
    # gets the current high scores as stored in "top_scores.txt"
    r = open('top_scores.txt','r')
    any_list = []

    for i in r.readlines():
        any_list.append(i.strip().split('\t'))
    r.close()
    d = {}
    try:
        for i in any_list:
            d[i[0]] = [ float(i[1]), int(i[2]) ]
    except:
        return d
    return d
def setScores(name, score, rounds):
    # sets the high scores with the current score board scores
    
    # print('\npoints passed:', score)
    
    score = score / 100 * ( rounds )
    
    # print('rounds passed:', rounds)
    # print('points raw   :', score)
    
    scores_dict = getScores()
    
    # checks if player name is duplicate
    if name not in scores_dict:

        # if not, corresponding score is assigned to name in dict
        score = round( ((score/rounds) * 100), 2)
        scores_dict[name] = [score, rounds]

    else:
        # when current player has played games before need to update score
        current_player = scores_dict[name]

        try:
            # calculates score
            score = round( ((score/rounds) * 100), 2)
        except:
            # in event that there have been 0 rounds played score is set to 0
            score = 0
            
        # updates current player's score
        scores_dict[name] = [ score, rounds]

    # used to sorts the current scores 
    sorted_scores = {}
    
    for key,value in sorted(scores_dict.items(), key = lambda e: e[1][0], reverse = True):
        sorted_scores[key] = value
                
    w = open('top_scores.txt','w')

    # print('Items  saved :', scores_dict[name])
    
    # writes the saved scores to the file
    for i in sorted_scores:
        w.write(str(i))
        w.write('\t')
        for j in sorted_scores[i]:
            w.write(str(j))
            w.write('\t')
        w.write('\n')
    w.close()
    
    try:
        return current_player
    except:
        return
def upDateHigh():
    # resets and formats the high score scroll box to update with the current player 
    
    # holds the list of text objects for scrolling
    highList = []
    # holds current access of high scores
    highDict = getScores()
    place = 1
    y = 450
    for i in highDict:
        if( place > 10 ):
            # only adds the first 10 places
            break
        
        text = Text(Point(180, y), "{0:<3}{1:<16}{2:>5}{3:>5}".format( place, i, highDict[i][0], highDict[i][1] ) )
        text.setFace('courier')
        
        highList.append( text )
        place += 1
        y += 50
    while( place < 11 ):
        # populates missing high scores
        text = Text(Point(180, y), "{0:<3}{1:<16}{2:>5}{3:>5}".format( place, 'None', '0.0', '0' ) )
        text.setFace('courier')
        
        highList.append( text )
        place += 1
        y += 50
    return highList
def creation():
    # this method defines a series of shapes and button objects
    # these objects are added to a list to be later drawn                                                                                                                    (because thats realistic)
    values = []
    w = GraphWin("Pull! The shot put game", 400, 600)
    w.setBackground('white')
    gP = Rectangle(Point(25,40), Point(375, 170))
    t1 = Text(Point(200, 25), "Game Panel")

#Highscores
    # high scores section and header    
    rHigh = Rectangle(Point(25, 430), Point(375, 580))
    tHigh = Text(Point(200, 405), 'High Scores')
    
    bHighU = Button(Point(360, 460), 20, 30, 'â†‘', 'light grey')
    bHighU.activate()
    bHighD = Button(Point(360, 550), 20, 30, 'â†“', 'light grey')
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
    rScore = Rectangle(Point(300, 130), Point(360, 160))
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
    
    bPull1 = Button(Point(290, 350), 150, 50, "PULL DOUBLE!", "yellow")
    bPull1.deactivate('pink')
    bPull2 = Button(Point(110, 350), 150, 50, "PULL SINGLE!", "yellow")
    bPull2.deactivate('pink')

    highList = []
    highDict = getScores()
    place = 1
    y = 450
    for i in highDict:
        if( place > 10 ):
            # only adds the first 10 places
            break
        text = Text(Point(180, y), "{0:<3}{1:<16}{2:>5}{3:>5}".format( place, i, highDict[i][0], highDict[i][1] ) )
        text.setFace('courier')
        
        highList.append( text )
        place += 1
        y += 50
    while( place < 11 ):
        # populates missing highscores
        text = Text(Point(180, y), "{0:<3}{1:<16}{2:>5}{3:>5}".format( place, 'None', '0.0', '0' ) )
        text.setFace('courier')
        
        highList.append( text )
        place += 1
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
    # 35 - 36
    values.append(w) 
    values.append(bPull2)  
    
    return ( w, values )

def undrawer(values):
    '''
    ### WE ADDED THIS IN ###
    
    Takes in all old attributes from control window and un-draws them
    This is done to allow for the high scores to properly scroll 'Underneath' the rest of the objects 
        and be properly updated at the end of each round
    '''
    for i in values[32]:
        # un-draws all high score Text objects
        i.undraw()
        
    for i in values:
        try:
            # un-draws all graphics.py objects
            i.undraw()
        except:
            try:
                # un-draws Buttons class object's attributes of graphics.py
                i.label.undraw()
                i.rect.undraw()
            except:
                # can't undraw a window
                pass
def drawer(w, values):
    # draws the values that were created in 'creation( )'
    # values[32].draw(w)
    for i in values[32]:
        # draws high scores first to have them be "bellow" other attributes for scrolling
        i.draw(w)
    # upper border for high scores   
    bg = Rectangle(Point(-1, -1), Point(401, 430))
    bg.setFill('white')
    bg.setOutline('white')
    bg.draw(w)
    
    for vis in values:
        if(type(vis) == Button):
            '''
            Handles Button class object's attributes 
            '''
            vis.rect.draw(w)
            vis.label.draw(w)
        else:
            # all other values
            try:
                vis.draw(w)
            except:
                pass
    # lower border for high scores
    lbg = Rectangle(Point(-1, 581), Point(601, 601))
    lbg.setFill('white')
    lbg.setOutline('white')
    lbg.draw(w)
    
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
    # Creates the sky and ground
    sky = Rectangle(Point(-1, -1),   Point(600, 450))
    sky.setFill('#00a2e8')
    drt = Rectangle(Point(-1, 450), Point(600, 600))
    drt.setFill('#00a202')
    drt.setOutline('#00a202')
   
    # loads sky image
    Image(Point(300,225),'background.png').draw(w)
    drt.draw(w)
    
    return w
def newGame(w, pwr, ang, grvy, points, rounds, pullT):
    # sets points to a raw disks clicked value
    # print('\tpoints passed:', points)
    
    points = points / 100 * ( rounds - 1 )
    
    # print('\trounds passed:', rounds)
    # print('\tpoints raw   :', points)
    # creates the disks
    dskL = Circle(Point(590, int(randint(350, 450))), 10)
    dskR = Circle(Point(10,  int(randint(350, 450))), 10)
    rabL = Circle(Point(590, int(randint(450, 600))), 10)
    rabR = Circle(Point(10 , int(randint(450, 600))), 10)
    
    dskL.setFill('dark grey')
    dskR.setFill('dark grey')
    rabL.setFill('dark grey')
    rabR.setFill('dark grey')
    
    # Creats the clouds 
    clouds = [Image(Point(randint(-150, -100), randint(0, 375)), "cloud.png"), Image(Point(randint(-100, -50), randint(0, 375)), "cloud.png"),
              Image(Point(randint(-50, 0), randint(0, 375)), "cloud.png"),     Image(Point(randint(0, 50), randint(0, 375)), "cloud.png"),
              Image(Point(randint(50, 100), randint(0, 375)), "cloud.png"),    Image(Point(randint(100, 150), randint(0, 375)), "cloud.png"),
              Image(Point(randint(150, 200), randint(0, 375)), "cloud.png"),   Image(Point(randint(200, 250), randint(0, 375)), "cloud.png")]
    
    # conditionals for when the disks are done 
    pL, pR, rL, rR = 0, 0, 0, 0
    
    
    # determines what is drawn for this game
    if( pullT == 1 ):
        # when there is one disk
        if( randint(1, 10) >= 5 ):
            # disk will be on the left side
            if( randint(1, 10) >= 5 ):
                # disk is a rabbit
                rabL.draw(w)
                rR = 1
            else:
                # disk is a pigeon
                dskL.draw(w)
                pR = 1
        else:
            # disk will be on the right side
            if( randint(1, 10) >= 5 ):
                # disk is a rabbit
                rabR.draw(w)
                rL = 1
            else:
                # disk is a pigeon
                dskR.draw(w)
                pL = 1
    if( pullT == 2 ):
        # when there are 2 disks 
        if( randint(1, 10) >= 5 ):
            # disks are rabbits
            rabL.draw(w)
            rabR.draw(w)
        else:
            # disks are pigeons
            dskL.draw(w)
            dskR.draw(w)  
    
    cloudliness = randint(0, 8)
     
    while( cloudliness < len(clouds) ):
        # picks random cloud of the 4 and draws it
        try:
            clouds[ randint(0, 7) ].draw(w)
        except:
            # when the random cloud has already been drawn
            pass
        
        cloudliness += 1
    
    # movement value calculations
    dx = pwr * cos(radians(ang))
    if(dx < 0):
        dx *= -1
    
    dy = -(pwr * sin(radians(ang)))
        
    while( True ):
        # loop runs until the disk are both "shot" or have reached the end
        sleep(.05)
        
        # re defines variables for conditionals 
        cp = w.checkMouse()
        rPCent = dskR.getCenter()
        lPCent = dskL.getCenter()
        rRCent = rabR.getCenter()
        lRCent = rabL.getCenter()
        
        if( diskClicked(dskR, cp) ):
            # if the right pigeon disk is clicked
            hm1 = Image(Point(cp.getX(), cp.getY()),"hitMarker.png")
            hm1.draw(w)
            points += .5
            dskR.undraw()
            pR = 1
        if( diskClicked(dskL, cp) ):
            # if the left pigeon disk is clicked
            hm2 = Image(Point(cp.getX(), cp.getY()),"hitMarker.png")
            hm2.draw(w)
            points += .5
            dskL.undraw()
            pL = 1
        if( diskClicked(rabR, cp) ):
            # if the right rabbit disk is clicked
            hm3 = Image(Point(cp.getX(), cp.getY()),"hitMarker.png")
            hm3.draw(w)
            points += .5
            rabR.undraw()
            rR = 1
        if( diskClicked(rabL, cp) ):
            # if the left rabbit disk is clicked
            hm4 = Image(Point(cp.getX(), cp.getY()),"hitMarker.png")
            hm4.draw(w)
            points += .5
            rabL.undraw()
            rL = 1
        
        if( rPCent.getX() >= 600 or rPCent.getY() > 450 ):
            # conditional to check if right moving disk is in play
            pR = 1
        if( lPCent.getX() <= 0 or lPCent.getY() > 450 ):
            # conditional to check if left moving disk is in play
            pL = 1
        if( rRCent.getX() >= 600 ):
            # conditional to check if right moving disk is in play
            rR = 1
        if( lRCent.getX() <= 0   ):
            # conditional to check if left moving disk is in play
            rL = 1
         
        if( pL == 1 and pR == 1 or rR == 1 and rL == 1):
            # conditional to break the loop if the balls are done
            sleep(.5)
            # tests and removes hit boxes that were used
            try:
                hm1.undraw()
            except:
                pass
            try:
                hm2.undraw()
            except:
                pass
            try:
                hm3.undraw()
            except:
                pass
            try:
                hm4.undraw()
            except:
                pass
            
            for i in clouds:
                i.undraw()
            
            dskL.undraw()
            dskR.undraw()
            rabR.undraw()
            rabL.undraw()
            break

        # moves the disks after all conditions are done
        if( pR == 0):
            # moves when not out of bounds
            dskR.move(dx, dy)
        if( pL == 0):
            # moves when not out of bounds
            dskL.move(-dx, dy)
        if( rR == 0):
            # moves when not out of bounds
            rabR.move(dx, 0)
        if( rL == 0):
            # moves when not out of bounds
            rabL.move(-dx, 0)
        for i in clouds:
            i.move(5, 0)    
           
        dy += 1/ grvy
    # returns points to the displayed value rounded 2 places
    
    # print('\trounds points:', rounds, points)
    
    points = round(points/rounds * 100, 2)
    
    # print('\tPoints return:', points)
    
    return points

def operation(values, ngW):
    pullClickable = [False, False, False, False]  # Angle, Power, Gravity, Name
    newClickable  = [False, True]                 # Name, !running game
    highIndex     = -1                            # used to keep the highscores view window between min and max values
    player_dict = getScores()
    player = None
    # creates variables form list of all graphics objects
    bNew = values[2]
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
    bPull2 = values[36]
    
    while( ePlayer.getText() == '' ):
        # re-check until text is filled
        bNew.deactivate('light grey')
        bPull1.deactivate('pink')
        bPull2.deactivate('pink')
        cp = w.checkMouse()
        
        if(bQuit.clicked(cp) ):
            bQuit.deactivate('light grey')
            w.close()
            break
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
        else: 
            # checks if the current player exists in previous games
            if( ePlayer.getText() in player_dict ):
                if( player == None ):
                    player = player_dict[ePlayer.getText()]
                    tPoint.setText(player[0])
                    tRound.setText(player[1])
                    # print('player = ', player, '\n')
            else:
                try:
                    if( int(tRound.getText()) == player[1] ):
                        # resets the rounds and scores when a new name is entered
                        # acts as a new game function
                        
                        # print("player reset successful")
                        
                        tPoint.setText(0)
                        tRound.setText(0)
                except:
                    # caught if the first name entered is not a previous player
                    # because nothing has changed due to previous entries, nothing is reset 
                    pass
                if( int(tRound.getText()) >= 1 ):
                    player = [tPoint.getText(), tRound.getText()]
                
            if( len(ePlayer.getText()) >= 15 ):
                '''
                Group added code 
                Limited player name to 15 characters to allow for good text formatting in the highscores scrolling window
                '''
                name = ePlayer.getText()
                name = name[0:16]
                ePlayer.setText(name)    
        # active clicks!
        cp = w.checkMouse()
    
    # Game buttons
    
    # High Scores
        if( bHighU.clicked(cp) ):
            # moves highscore up
            bHighU.deactivate('white')
           
            if(highIndex > -1):
                for i in highList:
                    i.move(0, 50)
                highIndex -= 1
           
            sleep(.05)
            bHighU.activate()
            
        if( bHighD.clicked(cp) ):
            # moves highscore down
            bHighD.deactivate('white')
            
            if(highIndex < 6):
                for i in highList:
                    i.move(0, -50)
                highIndex += 1
            
            sleep(.05)
            bHighD.activate()
            
    # Quit
        if( bQuit.clicked(cp) ):
            # sets scores before closing
            bQuit.deactivate('light grey')
            sleep(.5)
            setScores(ePlayer.getText(), int(tPoint.getText()), int(tRound.getText()))
            w.close()
            break
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
        if( bAU.clicked(cp) ):
            bAU.deactivate('red')
            if( int(tAVal.getText()) >= 60 ):
                tAVal.setText('60')
            elif( int(tAVal.getText()) <= 30 ):
                tAVal.setText('30')
            else:
                tAVal.setText(int(tAVal.getText()) + 1)
        if( bAD.clicked(cp) ):
            bAD.deactivate('red')
            if( int(tAVal.getText()) <= 30 ):
                tAVal.setText('30')
            elif( int(tAVal.getText()) >= 60 ):
                tAVal.setText('60')
            else:
                tAVal.setText(int(tAVal.getText()) - 1)
    # Power       
        if( bPU.clicked(cp) ):
            bPU.deactivate('red')
            if( int(tPVal.getText()) >= 50 ):
                tPVal.setText('50')
            elif( int(tPVal.getText()) <= 5):
                tPVal.setText('5')
            else:
                tPVal.setText(int(tPVal.getText()) + 1)
        if( bPD.clicked(cp) ):
            bPD.deactivate('red')
            if( int(tPVal.getText()) <= 5):
                tPVal.setText('5')
            elif( int(tPVal.getText()) >= 50 ):
                tPVal.setText('50')
            else:
                tPVal.setText(int(tPVal.getText()) - 1)
    # Gravity     
        if( bGU.clicked(cp) ):
            bGU.deactivate('red')
            if( int(tGVal.getText()) >= 25):
                tGVal.setText('25')
            elif( int(tGVal.getText()) <= 3 ):
                tGVal.setText('3')
            else:
                tGVal.setText(int(tGVal.getText()) + 1)
        if( bGD.clicked(cp) ):
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
                '''
                When there are  2  disks
                '''
                # if user wants to play
                bPull1.deactivate("light grey")
                sleep(.2)
                bPull1.activate()
                
                # sets new to be unclickable
                newClickable[1] = True
                bNew.deactivate('light grey')
                
                match += 1
         
                cp = w.checkMouse()
                
                if( bQuit.clicked(cp) ):
                    # sets scores before closing
                    bQuit.deactivate('light grey')
                    sleep(.5)
                    setScores(ePlayer.getText(), int(tPoint.getText()), int(tRound.getText()))
                    w.close()
                    break

                if player == None:
                    # if current player does not exist
                    tRound.setText(str(match))
                    current_score = newGame( ngW, int(tPVal.getText()), int(tAVal.getText()), 
                                             int(tGVal.getText()), int(tPoint.getText()), 
                                             int(tRound.getText()), 2) 
                    
                    tPoint.setText( current_score )
                    
                    setScores(ePlayer.getText(), int(tPoint.getText()), int(tRound.getText()))
                    
                    undrawer(values)
                    highList = upDateHigh() 
                    values[32] = highList      
                    drawer(w, values)
                else:
                    # if player exists
                    tRound.setText(str(match))
                    current_score = newGame( ngW, int(tPVal.getText()), int(tAVal.getText()), 
                                             int(tGVal.getText()), int(tPoint.getText()), 
                                             int(tRound.getText()), 2) 
                    
                    tPoint.setText( current_score )
                    
                    player = setScores(ePlayer.getText(), int(tPoint.getText()), int(tRound.getText()))
                    
                    undrawer(values)
                    highList = upDateHigh() 
                    values[32] = highList      
                    drawer(w, values)
                    
                newClickable[1] = False
                bNew.activate()
                
            if( bPull2.clicked(cp) ):
                '''
                When there are  1  disks
                '''
                # if user wants to play
                bPull2.deactivate("light grey")
                sleep(.2)
                bPull2.activate()
                
                # sets new to be unclickable
                newClickable[1] = True
                bNew.deactivate('light grey')
                
                match += 1
         
                cp = w.checkMouse()
                
                if( bQuit.clicked(cp) ):
                    # sets scores before closing
                    bQuit.deactivate('light grey')
                    sleep(.5)
                    setScores(ePlayer.getText(), int(tPoint.getText()), int(tRound.getText()))
                    w.close()
                    break

                if player == None:
                    # if current player does not exist
                    tRound.setText(str(match))
                    current_score = newGame( ngW, int(tPVal.getText()), int(tAVal.getText()), 
                                             int(tGVal.getText()), int(tPoint.getText()), 
                                             int(tRound.getText()), 1) 
                    tPoint.setText( current_score )
                    
                    setScores(ePlayer.getText(), int(tPoint.getText()), int(tRound.getText()))
                    
                    undrawer(values)
                    highList = upDateHigh() 
                    values[32] = highList      
                    drawer(w, values)
                else:
                    # if player exists
                    tRound.setText(str(match))
                    current_score = newGame( ngW, int(tPVal.getText()), int(tAVal.getText()), 
                                             int(tGVal.getText()), int(tPoint.getText()), 
                                             int(tRound.getText()), 1) 
                    tPoint.setText( current_score )
                    
                    player = setScores(ePlayer.getText(), int(tPoint.getText()), int(tRound.getText()))
                   
                    undrawer(values)
                    highList = upDateHigh() 
                    values[32] = highList      
                    drawer(w, values)
                    
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



















