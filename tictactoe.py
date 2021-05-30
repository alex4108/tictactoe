import pygame, sys, random, easygui, ast
import easygui as eg
from pygame.locals import Color

# Fix fonts in move() and moveAI()
# Font Settings Menu

class tictactoeGui:
    global currentFont, fontSize
    currentFont = "Times New Roman"
    fontSize = 80
    def __init__ (self):
        self.screen = 0
        self.board = 0
        self.AIs = 0
        self.PLAYERs = 0
        self.wins = 0
        self.wins2 = 0
        self.playerAmount = 0
        self.player1Color = (0, 0, 0)
        self.player2Color = (0, 0, 0)
        self.currentMusic = 0
        self.musicStatus = -1 # -1 = Unloaded, 0 = Stopped, 1 = Paused, 2 = Playing
        
        pygame.init()
        
        self.f = pygame.font.SysFont(currentFont, fontSize)
        self.screen = pygame.display.set_mode((300,300))
        pygame.display.set_caption("Tic Tac Toe")
        self.screen.fill([255,255,255])

        #draw lines
        pygame.draw.line(self.screen,(0,0,0),(100,300),(100,0))
        pygame.draw.line(self.screen,(0,0,0),(200,300),(200,0))
        pygame.draw.line(self.screen,(0,0,0),(300,100),(0,100))
        pygame.draw.line(self.screen,(0,0,0),(300,200),(0,200))

        #set up game data
        self.board = [[0,0,0],
                 [0,0,0],
                 [0,0,0]]

        #get wining combos
        self.wins = []
        #rows and collums
        for x in range(0,3):
            self.wins.append([[x,0],[x,1],[x,2]])
        for y in range(0,3):
            self.wins.append([[0,y],[1,y],[2,y]])
        #diagonals
        self.wins.append([[0,0],[1,1],[2,2]])
        self.wins.append([[0,2],[1,1],[2,0]])
        #make all combos
        self.wins2 = []
        for mix in self.wins:
            self.wins2.append([mix[0],mix[2],mix[1]])
            self.wins2.append(mix)
            self.wins2.append([mix[1],mix[0],mix[2]])
            self.wins2.append([mix[1],mix[2],mix[0]])
            self.wins2.append([mix[2],mix[1],mix[0]])
            self.wins2.append([mix[2],mix[0],mix[1]])
        self.wins = self.wins2

        self.AIs = []
        self.PLAYERs = []
        #self.currentMusic = "C:\Users\Public\Music\Sample Music\Kalimba.mp3"
        #self.musicMenu(True)
        
    def playAgain(self):
        pygame.display.flip()
        choice = eg.buttonbox(msg='Play Again?', title='Tic Tac Toe', choices=("Yes", "No"))
        if choice == "Yes":
            self = tictactoeGui()
            self.menu()
        else:
            sys.exit()

    def checkwin(self):
        for P1 in self.PLAYERs:
            for P2 in self.PLAYERs:
                for P3 in self.PLAYERs:
                    if [P1,P2,P3] in self.wins:
                        pygame.time.delay(1000)
                        eg.msgbox(msg="PLAYER ONE WINS!", title='Tic Tac Toe', ok_button="Continue")
                        self.playAgain()
        for AI1 in self.AIs:
            for AI2 in self.AIs:
                for AI3 in self.AIs:
                    if [AI1,AI2,AI3] in self.wins:
                        pygame.time.delay(1000)
                        if self.playerAmount == 1:
                            eg.msgbox(msg="CPU WINS!", title='Tic Tac Toe', ok_button="Continue")
                        elif self.playerAmount == 2:
                            eg.msgbox(msg="PLAYER TWO WINS!", title='Tic Tac Toe', ok_button="Continue")
                        self.playAgain()
        #check if it is a tie
        full = 1
        for tester1 in self.board:
            for tester2 in tester1:
                if tester2 == 0:
                    full = 0
        if full == 1:
            pygame.time.delay(1000)
            eg.msgbox(msg="TIE!", title='Tic Tac Toe', ok_button="Continue")
            self.playAgain()
                            
    
    #define moves
    def move(self, side, pos):
        global currentFont, fontSize
        #pos[0] is col, pos[1] is row
        if pos[1] == 0:
            yPosition = 5
        elif pos[1] == 1:
            yPosition = 105
        elif pos[1] == 2:
            yPosition = 205

        if pos[0] == 0:
            xPosition = 20
        elif pos[0] == 1:
            xPosition = 120
        elif pos[0] == 2:
            xPosition = 220

    
            
        self.board[pos[1]][pos[0]] = side
                      # width   #height
        
        position = (xPosition,yPosition,100,100)
               
        if side == 2:
            testcolor = self.player2Color
            self.screen.blit(self.f.render("O", 1, testcolor), position)
            self.AIs.append(pos)
        elif side == 1:
            testcolor = self.player1Color
            self.screen.blit(self.f.render("X", 1, testcolor), position)
            self.PLAYERs.append(pos)

    def moveAI(self):
        mover = [1,1]
        while self.board[mover[1]][mover[0]] != 0:
            mover = [random.randint(0,2),random.randint(0,2)]
            try:
                self.board[mover[1]][mover[0]]
            except:
                mover = [1,1]
        advantage = 0
        for ysquare in self.board:
            for xsquare in ysquare:
                curadvantage = 0
                for AI1 in self.AIs:
                    for ysquare2 in self.board:
                        for xsquare2 in ysquare2:
                            if AI1!=[ysquare2.index(xsquare2),self.board.index(ysquare2)] and AI1!=[ysquare.index(xsquare),self.board.index(ysquare)]:
                                if ysquare[ysquare.index(xsquare)] == 0 and ysquare2[ysquare2.index(xsquare2)] == 0:
                                    combo = [AI1,[ysquare2.index(xsquare2),self.board.index(ysquare2)],[ysquare.index(xsquare),self.board.index(ysquare)]]
                                    if combo in self.wins:
                                        curadvantage += 1
                                        if curadvantage > advantage:
                                            mover = [ysquare.index(xsquare),self.board.index(ysquare)]
                                            advantage = curadvantage
        for ysquare in self.board:
            for xsquare in ysquare:
                if ysquare[ysquare.index(xsquare)] == 0:
                    for AI1 in self.PLAYERs:
                        for AI2 in self.PLAYERs:
                            if AI1!=AI2:
                                combo = [AI1,AI2,[ysquare.index(xsquare),self.board.index(ysquare)]]
                                if combo in self.wins:
                                    mover = [ysquare.index(xsquare),self.board.index(ysquare)]
        for ysquare in self.board:
            for xsquare in ysquare:
                if ysquare[ysquare.index(xsquare)] == 0:
                    for AI1 in self.AIs:
                        for AI2 in self.AIs:
                            if AI1!=AI2:
                                combo = [AI1,AI2,[ysquare.index(xsquare),self.board.index(ysquare)]]
                                if combo in self.wins:
                                    mover = [ysquare.index(xsquare),self.board.index(ysquare)]
        self.move(2,mover)
    def fontMenu(self):
        global currentFont, fontSize
        fontMenuChoice = eg.buttonbox(msg="Font Menu\nCurrent Font: " + currentFont, title="Tic Tac Toe", choices=("New Font", "Main Menu"))
        if fontMenuChoice == "New Font":
            fontList = pygame.font.get_fonts()
            fontSelected = eg.choicebox(msg="Please choose a font", title="Tic Tac Toe", choices=fontList)
            currentFont = fontSelected
            self.f = pygame.font.SysFont(currentFont, fontSize)
            self.menu()
        else:
            self.menu()
            
        self.menu()
        
    def musicMenu(self, startup = False):
        musicName = str(self.currentMusic)
        songStatus = ["Stopped", "Paused", "Playing"]
        if startup:
            musicMenuSel = "Load New Song"
            
        if self.musicStatus == -1:
            musicName = "<No Song Loaded>"

        if not startup:
            musicMenuSel = eg.buttonbox(msg="Current Song: " + str(musicName) + "\nSong Status: " + songStatus[self.musicStatus], choices=("Load New Song", "Play", "Pause", "Stop", "Main Menu"))

        if musicMenuSel == "Load New Song":
            if not startup:
                self.currentMusic = eg.fileopenbox(filetypes=["*.mp3"])
            pygame.mixer.music.load(self.currentMusic)
            pygame.mixer.music.play(-1, 0.0)
            self.musicStatus = 2
        elif musicMenuSel == "Play" and self.musicStatus == 0: # Music is stopped
            pygame.mixer.music.play(-1, 0.0)
            self.musicStatus = 2
        elif musicMenuSel == "Play" and self.musicStatus == 1: # Music is paused
            pygame.mixer.music.unpause()
            self.musicStatus = 2
        elif musicMenuSel == "Play" and self.musicStatus == -1: # Unloaded
            eg.msgbox("Please load a song first!")
            self.musicMenu()
            
        elif musicMenuSel == "Pause":
            pygame.mixer.music.pause()
            self.musicStatus = 1

        elif musicMenuSel == "Stop":
            pygame.mixer.music.stop()
            self.musicStatus = 0
        else:
            self.menu()
            
        self.menu()

    def menu(self):  
        mainMenuSelection = easygui.buttonbox("Please select an option below", title="Tic Tac Toe", choices=("New Game", "Settings", "About", "Exit"))
        if mainMenuSelection == "New Game":
            # How many players?
                if eg.boolbox("How many players?", "New Game", ["1 Player", "2 Players"]):
                    self.playerAmount = 1
                else:
                    self.playerAmount = 2
                self.chooseColors()
                self.startGame()
        elif mainMenuSelection == "About":
            eg.textbox(msg='About', text='Game created by Alex Schittko\nAP CS Spring 2014', codebox=0)# By Alex Schittko
            self.menu()
        elif mainMenuSelection == "Settings":
            # Font
            settingsMenu = eg.buttonbox("Options", title="Tic Tac Toe", choices=("Music", "Font", "Exit"))
            if settingsMenu == "Music":
                self.musicMenu()
            elif settingsMenu == "Font":
                self.fontMenu()
            elif settingsMenu == "Exit":
                self.menu()
                
            self.menu()
        else:
            sys.exit()
            
    def getRGB(self, colorName):
        # Add orange!
        if colorName == "Red":
            return (255, 0, 0)
        elif colorName == "Orange":
            return (255, 140, 0)
        elif colorName == "Maroon":
            return (128, 0, 0)
        elif colorName == "Blue":
            return (0, 0, 255)
        elif colorName == "Lime Green":
            return (0, 255, 0)
        elif colorName == "Dark Green":
            return (0, 128, 0)
        elif colorName == "Aqua":
            return (0, 255, 255)
        elif colorName == "Gray":
            return (128, 128, 128)
        elif colorName == "Yellow":
            return (255, 255, 0)
        elif colorName == "Pink":
            return (255, 105, 180)
        elif colorName == "Purple":
            return (255, 0, 255)
        elif colorName == "Black":
            return (0, 0, 0)
        
    def chooseColors(self):
        colors = ("Red", "Orange", "Maroon", "Blue", "Lime Green", "Dark Green", "Aqua", "Gray", "Yellow", "Pink", "Purple", "Black")
    
        player1Temp = eg.choicebox(msg="Player 1 - Pick a color!", title="Tic Tac Toe", choices=colors)
            
        if self.playerAmount == 1:
            player2Temp = eg.choicebox(msg="CPU - Pick a color!", title="Tic Tac Toe", choices=colors)
        elif self.playerAmount == 2:
            player2Temp = eg.choicebox(msg="Player 2 - Pick a color!", title="Tic Tac Toe", choices=colors)
        
        ## Set to color, convert strings to ints
        self.player1Color = self.getRGB(player1Temp)
        self.player2Color = self.getRGB(player2Temp)

    def startGame(self):
        pygame.display.flip()
        pygame.time.delay(500)
        askPlayers = True
        currentPlayer = 1
        while askPlayers:
            if self.playerAmount == 1 or self.playerAmount == 2:
                askPlayers = False
                if self.playerAmount == 1:
                    if not eg.boolbox(msg="Would you like to go first?", title="Tic Tac Toe", choices=("Yes", "No")):
                        self.moveAI()
                   
                elif self.playerAmount == 2:
                    if eg.boolbox(msg="Which player is going first?", title="Tic Tac Toe", choices=("Player 1", "Player 2")):
                        currentPlayer = 1
                    else:
                        currentPlayer = 2
                while True:
                    mousepos = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.board[int(mousepos[1]/100)][int(mousepos[0]/100)] == 0:
                                if currentPlayer == 1 and self.playerAmount == 1:
                                    self.move(currentPlayer,[int(mousepos[0]/100),int(mousepos[1]/100)])
                                    pygame.display.flip()
                                    self.checkwin()
                                    self.moveAI()
                                    pygame.display.flip()
                                    self.checkwin()
                                elif currentPlayer == 1 and self.playerAmount == 2:
                                    self.move(currentPlayer,[int(mousepos[0]/100),int(mousepos[1]/100)])
                                    pygame.display.flip()
                                    self.checkwin()
                                    currentPlayer = 2
                                elif currentPlayer == 2 and self.playerAmount == 2:
                                    self.move(currentPlayer,[int(mousepos[0]/100),int(mousepos[1]/100)])
                                    pygame.display.flip()
                                    self.checkwin()
                                    currentPlayer = 1
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    pygame.display.flip()

game = tictactoeGui()
game.menu()
