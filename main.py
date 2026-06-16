#Importing the key libraries for the game
import pygame
import os
import random
from Settings import * #This imports from the 'Settings.py' file - Holds the constants
from Sprite import * #This imports from the 'Sprite.py. file - Holds the player, enemy, coins and potions class

class Button: #Button class creates multiple buttons within the game. This will be used to ensure the buttons can be interacted and shown on the screen
    def __init__(self, x, y, width, height): #__init__ takes in the x, y, width and height of the button. This is the button visual property

      #These are the property of the button which determines its shape
      self.x = x #This sets the starting x value of the button
      self.y = y #This sets the starting y value of the button
      self.width = width #This sets the starting width of the button
      self.height = height #This sets the starting height of the button

      self.buttonRectangle = pygame.Rect((self.x, self.y, self.width, self.height)) #Creates a rectangle taking in the attrubutes as paramaters
      self.buttonClicked = False #This checks whether the button has been clicked or not. This is to ensure that the button can only be clicked once and not repetitevly

    #This method updates the original property of the button rectangle to a new one without having to instantiate another button
    def UpdateAttribute(self, x, y, width, height):
      self.x = x #This updates the x value of the button
      self.y = y #This updates the y value of the button
      self.width = width #This updates the width of the button
      self.height = height #This updates the height of the button
      self.buttonRectangle = pygame.Rect((x, y, width, height)) #Updates the rectangle using the new updated x, y, width and height

    def CheckState(self, mousePosition, mouseClick): #This method checks whether a button has been clicked
      #The if statement below checks the mouse position relative to the width of the button and height of the button. When clicked, this then allows the button to do an action
      if ((mousePosition[0] >= self.x and mousePosition[0] <= (self.x+self.width)) and (mousePosition[1] >= self.y and mousePosition[1] <= (self.y+self.height))) and (self.buttonClicked == False):
        if mouseClick[0]: #If left click on the mouse is true
          self.buttonClicked = True #Sets the attribute to true which allows it to be clicked once
          return self #Function which allows buttons to be independant. 'Return' allows the button to do something different from another button using this method
      if mouseClick[0] == 0: #If the button is not clicked, this should not do anything
        self.buttonClicked = False #Does not do anything
      return None #Nothing occurs

    def CheckMousePosition(self, mousePosition):
      if ((mousePosition[0] >= self.x and mousePosition[0] <= (self.x+self.width)) and (mousePosition[1] >= self.y and mousePosition[1] <= (self.y+self.height))):
        return self
      else:
        return None
  
    def DrawButton(self, window):
      #pygame.draw.rect(window, GREEN, self.buttonRectangle) #This creates the button onto the screen
      pass

class Game: #This is the template which holds the entire game. This is where the player, enemy and items will be created. This will hold the all the functionalities of the game
  def __init__(self):
    pygame.init() #Initialises the pygame module
    pygame.font.init() #Initialises the pygame fonts

    self.window = pygame.display.set_mode((WIDTH, HEIGHT)) #Sets the width and height of the screen

    self.clock = pygame.time.Clock() #This initialises a clock which tells the cpu how much frames the game should run per second

    pygame.display.set_caption("Cosmic Showdown") #Title of the window

    self.level = 1 #What level the player is currently on. Changes display of level when this changes

    #All the fonts for the game and their respective sizes
    self.mainTitleFont = pygame.font.Font('Fonts/GameTitleFont.ttf', 150) #This is a newly imported font. This shows the title of the game on the main menu screen

    #These fonts are for the respective draw methods onto the main game
    self.healthFont = pygame.font.SysFont('comicsans', 30)
    self.expFont = pygame.font.SysFont('comicsans', 25)
    self.coinsFont = pygame.font.SysFont('comicsans', 30)
    self.objectivesFont = pygame.font.SysFont('comicsans', 20)
    self.potionEffectFont = pygame.font.SysFont('comicsans', 20)

    #Fonts for the settings screen interface
    self.titleFont = pygame.font.SysFont('comicsans', 50)
    self.controlFont = pygame.font.SysFont('comicsans', 40)
    self.instructionsFont = pygame.font.SysFont('comicsans', 18)
    self.mainTextFont = pygame.font.SysFont('comicsans', 40)
    self.audioTextFont = pygame.font.SysFont('comicsans', 30)

    #Fonts for the pause screen interface
    self.pauseTitleTextFont = pygame.font.SysFont('comicsans', 60)
    self.pauseTextFont = pygame.font.SysFont('comicsans', 30)
    self.showTextFont = pygame.font.SysFont('comicsans', 18)

    self.shopTitleTextFont = pygame.font.SysFont('comicsans', 60)
    self.shopTextFont = pygame.font.SysFont('comicsans', 30)

    #Fonts for the win screen interface
    self.winTitleTextFont = pygame.font.SysFont('comicsans', 60)
    self.winTextFont = pygame.font.SysFont('comicsans', 30)

    #Fonts for the lose screen interface
    self.loseTitleTextFont = pygame.font.SysFont('comicsans', 60)
    self.loseTextFont = pygame.font.SysFont('comicsans', 30)

    #Fonts for the draw screen interface
    self.drawTitleTextFont = pygame.font.SysFont('comicsans', 60)
    self.drawTextFont = pygame.font.SysFont('comicsans', 30)

    #Fonts for the shop screen interface
    self.shopTitleTextFont = pygame.font.SysFont('comicsans', 60)
    self.shopTextFont = pygame.font.SysFont('comicsans', 29)

    #Images within the game
    self.mainScreenBackground = pygame.transform.scale(pygame.image.load(os.path.join('Backgrounds','Parallax Background.jpg')),(WIDTH, HEIGHT)).convert_alpha() #Displays the first image onto the screen (for the parallax background)
    self.mainScreenOverlayingBackground = pygame.transform.scale(pygame.image.load(os.path.join('Backgrounds','Parallax Background.jpg')),(WIDTH, HEIGHT)).convert_alpha() #Displays the next multiple images onto the screen (for the parallax background)

    self.background = pygame.transform.scale(pygame.image.load(os.path.join('Backgrounds','Space.png')), (WIDTH, HEIGHT)).convert_alpha() #Background image for the main game

    self.coinStillImage = pygame.transform.scale(pygame.image.load(os.path.join('Other','SingleCoin.png')), (60, 60)).convert_alpha() #This is used within the 'DrawCoinCounter' method to show the coin image
    self.healthStillImage = pygame.transform.scale(pygame.image.load(os.path.join('Other','Health2.png')), (160, 300)).convert_alpha()
    self.speedStillImage = pygame.transform.scale(pygame.image.load(os.path.join('Other','Speed2.png')), (160, 300)).convert_alpha()

    self.whiteArrow = pygame.image.load(os.path.join('Other','WhiteArrow2.png')).convert_alpha()

    #Respective enemies within the game at their level
    self.enemy1 = 'Enemy/Necromancer_creativekind-Sheet.png' #Level 1 enemy
    self.enemy2 = 'Enemy/Enemy2.png' #Level 2 enemy
    self.boss = 'Enemy/Boss.png' #Level 3 enemy

    self.enemyFace1 = pygame.transform.scale(pygame.image.load(os.path.join('Enemy','EnemyFace1.png')), (80, 80)).convert_alpha() #Level 1 enemy face
    self.enemyFace2 = pygame.transform.scale(pygame.image.load(os.path.join('Enemy','EnemyFace2.png')), (100, 100)).convert_alpha() #Level 2 enemy face
    self.bossFace = pygame.transform.scale(pygame.image.load(os.path.join('Enemy','BossFace.png')), (120, 120)).convert_alpha() #Level 3 enemy face

    #Button images
    self.greenButton = pygame.transform.scale(pygame.image.load(os.path.join('Other','StartButton.png')), (335, 119)).convert_alpha()
    self.orangeButton = pygame.transform.scale(pygame.image.load(os.path.join('Other','SettingsButton.png')), (335, 119)).convert_alpha()
    self.redButton = pygame.transform.scale(pygame.image.load(os.path.join('Other','QuitButton.png')), (335, 119)).convert_alpha()
    self.blueButton = pygame.transform.scale(pygame.image.load(os.path.join('Other','ShopButton.png')), (335, 119)).convert_alpha()

    self.backgroundPosition = 0 #This is set to the first position of the background image to be the first frame the player see's
    self.overlayingPosition = WIDTH #This is set to the position of beyond the width of the screen. Player cannot see this image but this ensures repeition of image for a parallax background illusion
    self.speedRate = 0.8 #Speed in which how quickly the parallax background scrolls to the left (how fast the background and overlay position is subtracted)

    self.currentGameState = 1 #Controls the interfaces for the game and tells which interface is displayed
    #self.currentGameState = 1: Main menu interface
    #self.currentGameState = 2: Level selector interface
    #self.currentGameState = 3: Settings interface
    #self.currentGameState = 4: Level 1/Level 2/Level 3 interface

    #List for all of the items with in the game
    self.coinList = [] #Holds the coin objects - to be shown on screen and used within the 'Sprite.py' file for collisions
    self.healthPotionList = [] #Holds the health potion objects - to be shown on screen and used within the 'Sprite.py' file for collisions
    self.speedPotionList = [] #Holds the speed potion objects - to be shown on screen and used within the 'Sprite.py' file for collisions

    self.settings = True #This ensures that the settings button is not clicked for when the player clicks the 'Return To Main Menu' within the win/lose/draw screen as the mouse click will register twice. Sets to false to ensure this does not occur
    self.quit = True #This ensures that the quit button is not clicked for when the player clicks the 'Return To Main Menu' within the pause screen as the mouse click will register twice. Sets to false to ensure this does not occur

    self.level2 = False #This ensures that the level 2 button is not clicked for when the player clicks the 'Start Game' within the main menu screen as the mouse click will register twice. Sets to true after 'Start Game' clicked

    self.bossLock = True #Ensures that the boss level cannot be played for when this value is true. When this value is set to false, boss level unlocked

    self.interfaceDuration = 1600 #Duration of how long the animations of the player death or enemy death or both should be viewed before respective interface pops up

    #Shop interface attributes to be manipulated
    self.shop = False #Turns the shop screen interface on and off

    #When the player buys the potion, sets to true which ensures these potions can be activated. This also updates the visuals on the screen. For exmaple, turning the background from red or blue to grey
    self.instantHealthPotionBuy = False
    self.speedPotionBuy = False

    self.previousCoinCount = 0 #Holds the amount of coins the player currently had in the previous level
    self.previousExpCount = 0 #Holds the amount of experience the player currently had in the previous level
    self.previousPlayerLevelCount = 0 #Holds the player level the player currently had in the previous level

  def DrawTransparentSurface(self, x, y, width, height, alphaValue):
    self.transparentSurface = pygame.Surface((width, height), pygame.SRCALPHA)
    self.transparentSurface.fill((0, 0, 0, alphaValue))
    self.window.blit(self.transparentSurface, (x, y))

  def TextCreator(self, text, font, colour, x, y):
    self.textAttribute = font.render(text, 1, colour)
    self.window.blit(self.textAttribute, (x, y))

  def DrawWindow(self): #This is used to display the various interfaces within the game
    if self.currentGameState == 1: #Checks if the current game state is equal to 1
      self.MainMenu(self.mousePosition) #If it is, run the main menu method

    if self.currentGameState == 2: #Checks if the current game state is equal to 2
      self.LevelSelector(self.mousePosition) #If it is, run the level selector method

    if self.currentGameState == 3: #Checks if the current game state is equal to 3
      self.Settings(self.mousePosition) #If it is, run the settings method

    if self.currentGameState == 4: #Checks if the current game state is equal to 4
      self.LevelLogic(self.mousePosition) #If it is, run the level logic method - this will display the features, like the health bar, onto the screen for when the player is on level 1, 2 or 3

  def DrawHealthBar(self, playerHealth, enemyHealth):
    self.playerHealthProportion = playerHealth / 100 

    self.backgroundColourList = [DARKGREEN, DARKYELLOW, EVENDARKRED] #List of the dark background colours to change when player hp is a certain threshold
    self.frontColourList = [LIMEGREEN, ORANGE, DARKRED] #List of the light foreground colours to change when the player hp is a certain threshold
    
    if playerHealth >= 75: #When the player hp is bigger than or equal to 75
      #Both foreground and background colours change to a green tone
      self.backgroundColour = self.backgroundColourList[0]
      self.frontColour = self.frontColourList[0]
    if playerHealth >= 25 and playerHealth <= 74: #When the player hp is between 25 or 74 (inclusive)
      #Both foreground and background colours change to an orange tome
      self.backgroundColour = self.backgroundColourList[1]
      self.frontColour = self.frontColourList[1]
    if playerHealth >= 0 and playerHealth <= 24: #When the player hp is between 0 and 24 (inclusive)
      #Both foreground and background colours change to a red tone
      self.backgroundColour = self.backgroundColourList[2]
      self.frontColour = self.frontColourList[2]

    #Creates three rectangles: One for the black outline. One for the foreground changing rectangle that the player can see change. One for the background still colour
    pygame.draw.rect(self.window, BLACK, (17, 17, 406, 36)) #Black outline rectangle
    pygame.draw.rect(self.window, self.backgroundColour, (20, 20, 400, 30)) #Background rectangle
    pygame.draw.rect(self.window, self.frontColour, (20, 20, (400 * self.playerHealthProportion), 30)) #Changing foreground rectangle

    self.TextCreator(str(playerHealth)+"%", self.healthFont, WHITE, 170, 14)
    
    self.enemyHealthProportion = enemyHealth / 100 #This finds the ratio in which the enemy current health is out of the enemy max health (100) and then uses this to change rectangle size

    #Creates three rectangles: One for the black outline. One for the foreground changing rectangle that the player can see change. One for the background still colour
    pygame.draw.rect(self.window, BLACK, (857, 17, 406, 36)) #Black outline rectangle
    pygame.draw.rect(self.window, DARKRED, (860, 20, 400, 30)) #Background rectangle
    pygame.draw.rect(self.window, RED, (860, 20, (400 * self.enemyHealthProportion), 30)) #Changing foreground rectangle

    self.TextCreator(str(enemyHealth)+"%", self.healthFont, WHITE, 1030, 14)
  
  def DrawExpLevels(self, playerExp, playerLevel): #This method is like the 'DrawHealthBar' method in which it draws the player exp bar with a black outline, changing foreground and background
    #Creates three rectangles: One for the black outline. One for the foreground changing rectangle that the player can see change. One for the background still colour
    pygame.draw.rect(self.window, BLACK, (2 - 3, 683 - 3, 1180, 40)) #Black outline rectangle
    pygame.draw.rect(self.window, DARKBLUE, (2, 683, 1174, 34)) #Background rectangle
    pygame.draw.rect(self.window, LIGHTBLUE, (2, 683, 20 * playerExp, 34)) #Changing foreground rectangle
    self.TextCreator("Exp: "+str(playerExp)+"/"+str(50), self.expFont, WHITE, 540, 683)

    pygame.draw.rect(self.window, BLACK, (1183 - 3, 683 - 3, 100, 40)) #Black outline rectangle
    pygame.draw.rect(self.window, LIGHTBLUE, (1183, 683, 94, 34)) #Background rectangle
    self.TextCreator(str(playerLevel), self.expFont, WHITE, 1225, 683)

  def DrawCoinCounter(self, x, y, playerCoins):
    self.DrawTransparentSurface(17, 53, 203, 130, 128)
    self.TextCreator(str(playerCoins), self.coinsFont, WHITE, x, y)
    self.window.blit(self.coinStillImage, (17, 53)) #Places an image of a coin onto the screen

  def DrawObjectives(self):
    self.DrawTransparentSurface(857, 53, 280, 80, 128)

    self.levelMessage = {1: ("Collect All Coins", "Kill The Enemy")}
    newList = []
    for keys in self.levelMessage:
      message = (keys, self.levelMessage[keys])
      newList.append(message)
    
   # if self.level == 1: #This shows the level 1 objectives
  #    self.messageOne = "Collect All Coins"
   #   self.messageTwo = "Kill The Enemy"

 #   if self.level == 2: #This shows the level 2 objectives  
  #    self.messageOne = "Kill Enemy At Green Health"
   #   self.messageTwo = "Kill The Enemy"

   # if self.level == 3: #This shows the level 3 objectives
   #   self.messageOne = "Don't Use Potions"
  #    self.messageTwo = "Kill The Boss"

    #These then create the texts for the respective texts above
 #   self.TextCreator("Objectives:", self.objectivesFont, WHITE, 867, 50)
  #  self.TextCreator(self.messageOne, self.objectivesFont, WHITE, 867, 75)
  #  self.TextCreator(self.messageTwo, self.objectivesFont, WHITE, 867, 100)

  def DrawCurrentEffectPotion(self, potionInEffect):
    self.TextCreator("Potions Activated:", self.potionEffectFont, WHITE, 28, 110)
    self.TextCreator(potionInEffect, self.potionEffectFont, WHITE, 28, 140)
  
  def MainMenu(self, mousePosition): #This holds the buttons for the main menu screen and how the buttons will change when hovered
    for buttons in self.mainMenuInterfaceList: #This iterates through the buttons within the list
      buttons.DrawButton(self.window) #For each button, it draws it on the screen at the desired x and y coordinates

    self.window.blit(self.greenButton, (462, 181)) #This is the start button image
    self.window.blit(self.orangeButton, (462, 381)) #This is the settings button image
    self.window.blit(self.redButton, (462, 581)) #This is the quit button image
    
    self.TextCreator("Cosmic Showdown", self.mainTitleFont, WHITE, 290, 60)

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes

    self.setColour = [WHITE, WHITE, WHITE]
    
    if self.startButton.CheckMousePosition(mousePosition):
      self.setColour[0] = BLACK #'Start Game' button text changed to white

    if self.settingsButton.CheckMousePosition(mousePosition):
      self.setColour[1] = BLACK #'Settings' button text changed to white
      self.settings = True #This ensures that the 'Settings' interface loads up when hovered

    if self.quitButton.CheckMousePosition(mousePosition):
      self.setColour[2] = BLACK #'Quit' button text changed to white
      self.quit = True #This ensures the player can quit the game when hovered
    
    self.TextCreator("Start Game", self.mainTextFont, self.setColour[0], 520, 208)
    self.TextCreator("Settings", self.mainTextFont, self.setColour[1], 550, 408)
    self.TextCreator("Quit", self.mainTextFont, self.setColour[2], 580, 608)

  def ParallaxBackground(self):
    #The background position is the starting image and the overlay is the image that comes second. Once the background image leaves, the overlay images takes over. Once the overlay image leaves, the background takes over
    if self.backgroundPosition <= -WIDTH: #Checks if the background position of the image has completly left the screen on the left side
      self.backgroundPosition = WIDTH #Warps the image back around to the right side of the screen
    if self.overlayingPosition <= -WIDTH: #Checks if the overlay position of the image has completly left the screen on the left side
      self.overlayingPosition = WIDTH #Warps the image back around to the right side of the screen

    #This is the scroll rate of the images moving from right to left (how fast the scroll is)
    self.backgroundPosition -= self.speedRate
    self.overlayingPosition -= self.speedRate

    #The images are then mapped onto the screen continuosly which gives a parallax background effect (as it is in the main game loop)
    self.window.blit(self.mainScreenBackground, (self.backgroundPosition, 0)) #Background position updates constantly meaning image constantly moves
    self.window.blit(self.mainScreenOverlayingBackground, (self.overlayingPosition, 0)) #Overlaying position updates constantly meaning image constantly moves

  def LevelSelector(self, mousePosition): #This holds the buttons for the level selector screen and how the buttons will change when hovered
    for buttons in self.levelSelectorInterfaceList: #This iterates through the buttons within the list
      buttons.DrawButton(self.window) #For each button, it draws it on the screen at the desired x and y coordinates

    pygame.draw.rect(self.window, SPACEBLUE, (370, 60, 540, 80)) #This creates a background rectangle where the title of the interface is placed on top of
    self.TextCreator("Select Level", self.controlFont, WHITE, 524, 68)

    #These are rectangles that is on the screen. These rectangles are not clickable but are on the screen for design purposes. They give a sense of difficulty of the level
    pygame.draw.rect(self.window, GREEN, (70, 200, 300, 300))
    pygame.draw.rect(self.window, DARKORANGE, (490, 200, 300, 300))
    pygame.draw.rect(self.window, GREY, (910, 200, 300, 300))

    self.setColour = [BLACK, BLACK, BLACK] #List of colours which is mapped to a corresponding button
    #self.setColour[0]: Mapped colour to the 'Level 1' button
    #self.setColour[1]: Mapped colour to the 'Level 2' button
    #self.setColour[2]: Mapped colour to the 'Level 3' button

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes
    if self.level1Button.CheckMousePosition(mousePosition):
      self.setColour[0] = WHITE #'Level 1' button text changed to white

    if self.level2Button.CheckMousePosition(mousePosition):
      self.setColour[1] = WHITE #'Level 2' button text changed to white
      self.level2 = True #This is set to true within this interface as it is now allowed to be clicked. Prevents multiple clicks on the button

    if self.level3Button.CheckMousePosition(mousePosition) and (self.bossLock == False):
      self.setColour[2] = WHITE #'Level 3' button text changed to white

    if self.bossLock == True: #Checks if the boss level is locked. If false, the code below does not appear
      self.TextCreator("Level Locked", self.mainTextFont, WHITE, 943, 440)

    if self.bossLock == False: #Checks if the boss level is unlocked
      pygame.draw.rect(self.window, DARKRED2, (910, 200, 300, 300)) #This changes the colour of the rectangle from grey to dark red to tell the player it is unlocked

    self.TextCreator("Level 1", self.mainTextFont, self.setColour[0], 155, 208)
    self.TextCreator("Level 2", self.mainTextFont, WHITE, 570, 208)
    self.TextCreator("Level 3", self.mainTextFont, WHITE, 990, 208)
  
    #The images are then placed onto the screen
    self.window.blit(self.enemyFace1, (178, 300))
    self.window.blit(self.enemyFace2, (590, 300))
    self.window.blit(self.bossFace, (1005, 300))

    if self.keysPressed[pygame.K_ESCAPE]: #Takes the input of the player for when the click the 'Esc' button on the interface. Checks if 'Esc' is pressed
      self.currentGameState = 1 #If pressed, returns the game back to the main menu interface
      self.level2 = False #Ensures that level 2 cannot be clicked for when 'Start Game' is clicked or will instantly load level 2

  def Settings(self, mousePosition): #This method displays the controls, instructions and audio adjustment for the game
    #This is used to ensure there is a transparent black overlay onto the screen which allows images or text on the transparent rectangle to be seperated from the background
    self.DrawTransparentSurface(0, 0, 1280, 720, 128)

    #This is creating the three big titles for the settings interface
    self.controlTitle = self.titleFont.render("Controls", 1, WHITE)
    self.instructionTitle = self.titleFont.render("Instructions", 1, WHITE)
    self.audioTitle = self.titleFont.render("Audio", 1, WHITE)

    #Under the controls section, this will show the various key binds
    self.aText = self.controlFont.render("A", 1, WHITE)
    self.dText = self.controlFont.render("D", 1, WHITE)
    self.wText = self.controlFont.render("W", 1, WHITE)
    self.lText = self.controlFont.render("L", 1, WHITE)
    self.escText = self.controlFont.render("Esc", 1, WHITE)

    #Next to the keys (shown above), this will describe what those buttons do
    self.moveA = self.controlFont.render("Move Left", 1, WHITE)
    self.moveD = self.controlFont.render("Move Right", 1, WHITE)
    self.moveW = self.controlFont.render("Jump", 1, WHITE)
    self.moveL = self.controlFont.render("Attack", 1, WHITE)
    self.returnEsc = self.controlFont.render("Pause/Back", 1, WHITE)

    #Under the instructions section, this will show all the instructions of the game
    pygame.draw.rect(self.window, LIGHTORANGE, (440, 120, 400, 350))

    self.instructionTextList = ["1. Select Your Preferred Level"]
    
    self.instructionText1 = self.instructionsFont.render("1. Select Your Preferred Level", 1, WHITE)
    self.instructionText2 = self.instructionsFont.render("2. Try And Complete The In-Game Objectives", 1, WHITE)
    self.instructionText3 = self.instructionsFont.render("3. Complete Levels 1 or 2 To Unlock Boss Level", 1, WHITE)
    self.instructionText4 = self.instructionsFont.render("4. Collect Coins To Buy Potions In The Shop", 1, WHITE)
    self.instructionText5 = self.instructionsFont.render("5. Speed Potion: Velocity Increases", 1, WHITE)
    self.instructionText6 = self.instructionsFont.render("6. Instant Health: Gain 30 HP", 1, WHITE)
    self.instructionText7 = self.instructionsFont.render("7. Natural Regeneration After 1 Minute", 1, WHITE)
    self.instructionText8 = self.instructionsFont.render("8. Gain Exp By Attacking And Defeating Enemy", 1, WHITE)
    self.instructionText9 = self.instructionsFont.render("9. Once Player Levels Up, Attack Increases By 6", 1, WHITE)
    self.instructionText10 = self.instructionsFont.render("10. Once Player Levels Up, HP Increases By 5", 1, WHITE)
    self.instructionText11 = self.instructionsFont.render("11. Potions Bought From Shop Activate Instantly", 1, WHITE)
    self.instructionText11P2 = self.instructionsFont.render("For When Resume Button Clicked", 1, WHITE)

    self.window.blit(self.instructionText1, (440, 120))
    self.window.blit(self.instructionText2, (440, 150))
    self.window.blit(self.instructionText3, (440, 180))
    self.window.blit(self.instructionText4, (440, 210))
    self.window.blit(self.instructionText5, (440, 240))
    self.window.blit(self.instructionText6, (440, 270))
    self.window.blit(self.instructionText7, (440, 300))
    self.window.blit(self.instructionText8, (440, 330))
    self.window.blit(self.instructionText9, (440, 360))
    self.window.blit(self.instructionText10, (440, 390))
    self.window.blit(self.instructionText11, (440, 420))
    self.window.blit(self.instructionText11P2, (467, 440))

    
    self.audioText1 = self.audioTextFont.render("Background Music Volume", 1, WHITE)

    #These rectangles are the title rectangles (three long rectangles formed at the top of the settings interface)
    pygame.draw.rect(self.window, LIGHTORANGE, (10, 20, 400, 60))
    pygame.draw.rect(self.window, LIGHTORANGE, (440, 20, 400, 60))
    pygame.draw.rect(self.window, LIGHTORANGE, (870, 20, 400, 60))

    #The title texts of the settings interface is then placed onto the screeen
    self.window.blit(self.controlTitle, (105, 15))
    self.window.blit(self.instructionTitle, (495, 15))
    self.window.blit(self.audioTitle, (1000, 15))

    #These rectangles are the key binds rectangles (small squares under the controls title)
    pygame.draw.rect(self.window, LIGHTORANGE, (10, 120, 100, 80))
    pygame.draw.rect(self.window, LIGHTORANGE, (10, 230, 100, 80))
    pygame.draw.rect(self.window, LIGHTORANGE, (10, 340, 100, 80))
    pygame.draw.rect(self.window, LIGHTORANGE, (10, 450, 100, 80))
    pygame.draw.rect(self.window, LIGHTORANGE, (10, 560, 100, 80))

    #These are the texts of the key binds that is being placed onto the screen
    self.window.blit(self.aText, (42, 130))
    self.window.blit(self.dText, (42, 240))
    self.window.blit(self.wText, (37, 350))
    self.window.blit(self.lText, (46, 460))
    self.window.blit(self.escText, (28, 570))

    #These rectangles are the key binds description (fairly long rectangles formed under controls title)
    self.coordinates = [120, 230, 340, 450, 560]
    for new, i in enumerate(self.coordinates):
      pygame.draw.rect(self.window, LIGHTORANGE, (150, i, 260, 80))

    #These are the texts of the key binds description that is being placed onto the screen
    self.movements = [130, 240, 350, 460, 570]
    self.buttons = [self.moveA, self.moveD, self.moveW, self.moveL, self.returnEsc]
    for pos, i in enumerate(self.buttons):
      self.window.blit(i, (183, self.movements[pos]))

    #This is the rectangle which will hold the instruction texts (large rectangle under the instructions title)


    #These are the texts of the instructions of the game that is being placed onto the screen


    pygame.draw.rect(self.window, LIGHTORANGE, (888, 170, 355, 80))

    pygame.draw.rect(self.window, BLACK, (895 - 3, 180 - 3, (66), 66))
    pygame.draw.rect(self.window, GREY, (895, 180 , 60, 60))

    pygame.draw.rect(self.window, BLACK, (965 - 3, 180 - 3, (66), 66))
    pygame.draw.rect(self.window, GREY, (965, 180 , 60, 60))

    pygame.draw.rect(self.window, BLACK, (1035 - 3, 180 - 3, (66), 66))
    pygame.draw.rect(self.window, GREY, (1035, 180 , 60, 60))

    pygame.draw.rect(self.window, BLACK, (1105 - 3, 180 - 3, (66), 66))
    pygame.draw.rect(self.window, GREY, (1105, 180 , 60, 60)) 

    pygame.draw.rect(self.window, BLACK, (1175 - 3, 180 - 3, (66), 66))
    pygame.draw.rect(self.window, GREY, (1175, 180 , 60, 60))

    volume = [895, 965, 1035, 1105, 1175]

    for position, x in enumerate(volume):
        if ((mousePosition[0] >= x and mousePosition[0] <= x + 60) and
            (mousePosition[1] >= 180 and mousePosition[1] <= 180 + 60)):
            pygame.draw.rect(self.window, LIMEGREEN, (x, 180, 60, 60))

    self.window.blit(self.audioText1, (886, 100))

    if self.keysPressed[pygame.K_ESCAPE]: #Takes the input of the player for when the click the 'Esc' button on the interface. Checks if 'Esc' is pressed
      self.currentGameState = 1 #If pressed, returns the game back to the main menu interface

  def LevelLogic(self, mousePosition): #This handles the main game logic - draws the player, enemy, items and features onto the screen. Updated via the main game loop. Handles the win/lose/draw/shop interface
      self.window.blit(self.background, (0, 0))

      #Draws the player and enemy movements within the game and updates all the time
      self.playerObject.Movements(self.window, self.enemyObject, self.coinList, self.healthPotionList, self.speedPotionList, self.platformList)
      self.enemyObject.Movements(self.window, self.playerObject)

      #Draws the player and enemy within the game
      self.playerObject.DrawPlayer(self.window)
      self.enemyObject.DrawEnemy(self.window)

      #This ensures that all items within the respective lists are drawn onto the screen
      for coins in self.coinList:
        coins.DrawCoin(self.window)

      for health in self.healthPotionList:
        health.DrawPotion(self.window)

      for speed in self.speedPotionList:
        speed.DrawPotion(self.window)

      for platform in self.platformList:
        platform.DrawPlatform(self.window)

      #This draws all of the methods onto the screen to allow the player to see the visuals onto the screen
      self.DrawHealthBar(self.playerObject.playerHealth, self.enemyObject.enemyHealth)
      self.DrawExpLevels(self.playerObject.exp, self.playerObject.playerLevel)
      self.DrawCoinCounter(83, 65, self.playerObject.coins)
      self.DrawCurrentEffectPotion(self.playerObject.currentEffect)
      self.DrawObjectives()

      self.playerObject.SpeedPotionTimer() #Speed potion timer
      self.playerObject.NaturalRegeneration() #Natural regeneration timer

      if self.playerObject.Pause(): #Checks the return value of the player pause function for if it is set to true
        self.PauseMenu(mousePosition) #If it is, this will load up the pause screen interface

      if self.playerObject.Win(): #Checks the return value of the player win function for if it is set to true
        if self.playerObject.draw != True: #Checks if the draw attribute within the player class is not set to true
          if self.playerObject.playerWin == True: #If not, checks if the 'self.playerWin' attribute for if it has been set to true for when the enemy has been defeated
            self.currentGameTime = pygame.time.get_ticks() #If it is, this attribute gets the current game time
            if self.currentGameTime - self.playerObject.winTimer >= self.interfaceDuration: #It then is subtracted by the win timer, which runs when the enemy health is set to 0, and checks if it is bigger than 3 seconds
              if self.level == 1 or self.level == 2: #If it is, it checks what level the player is currently on, if they are on level 1 or 2, to load the respective win screen
                self.bossLock = False #Unlocks the boss level
                self.WinMenu(mousePosition) #Runs the first win menu screen
              if self.level == 3: #Checks if the player is on level 3
                self.WinMenu2(mousePosition) #Runs the second win menu screen

      if self.playerObject.Lose(): #Checks the return value of the player lose function for if it is set to true
        if self.playerObject.draw != True: #Checks if the draw attribute within the player class is not set to true
          if self.playerObject.playerLoss == True: #If not, checks if the 'self.playerLoss' attribute for if it has been set to true for when the player has been defeated
            self.currentGameTime = pygame.time.get_ticks() #If it is, this attribute gets the current game time
            if self.currentGameTime - self.enemyObject.loseTimer >= self.interfaceDuration: #It then is subtracted by the win timer, which runs when the player health is set to 0, and checks if it is bigger than 3 seconds
              self.LoseMenu(mousePosition) #Runs the lose menu screen

      if self.playerObject.Draw(): #Checks the return value of the player draw function for if it is set to true
        if self.playerObject.playerDraw == True: #Checks if the 'self.playerDraw' attribute for if it has been set to true for when the player and enemy has been defeated
          self.currentGameTime = pygame.time.get_ticks() #If it is, this attribute gets the current game time
          if self.currentGameTime - self.playerObject.drawTimer >= self.interfaceDuration: #It then is subtracted by the win timer, which runs when the player and enemy 0health is set to 0, and checks if it is bigger than 3 seconds
            self.DrawMenu(mousePosition) #Runs the draw menu screen

      if self.shop == True: #Checks if the 'self.shop' attribute has set to true
        self.Shop(mousePosition, self.playerObject.coins) #if it has, this will open up the shop screen interface

  def PauseMenu(self, mousePosition): #This holds the buttons for the pause menu screen and how the buttons will change when hovered
    #This is used to ensure there is a transparent black overlay onto the screen which allows images or text on the transparent rectangle to be seperated from the background
    self.transparentSurface = pygame.Surface((1280, 720), pygame.SRCALPHA) #Alpha method allows a transparent black box to be created onto the surface of the screen
    self.transparentSurface.fill((0, 0, 0, 200)) #Transparency using 4th index (alpha value)
    self.window.blit(self.transparentSurface, (0, 0)) #Placed the black transparent rectangle onto the screen

    pygame.draw.rect(self.window, GREY, (160, 270, 230, 70))
    self.hintTextShow1 = self.showTextFont.render("You Can Buy More Potions", 1, WHITE)
    self.hintTextShow2 = self.showTextFont.render("Using The In-Game Shop!", 1, WHITE)
    self.window.blit(self.hintTextShow1, (170, 280))
    self.window.blit(self.hintTextShow2, (170, 305))

    self.window.blit(self.whiteArrow, (280, 245))

    for buttons in self.pauseInterfaceList: #This iterates through the buttons within the list
      buttons.DrawButton(self.window) #For each button, it draws it on the screen at the desired x and y coordinates

    self.pauseTitle = self.pauseTitleTextFont.render("Game Paused", 1, WHITE) #The text for the title of the interface
    self.window.blit(self.pauseTitle, (445, 80)) #Places the text of the pause title onto the screen

    self.setColour = [BLACK, BLACK, BLACK] #List of colours which is mapped to a corresponding button
    #self.setColour[0]: Mapped colour to the 'Resume' button
    #self.setColour[1]: Mapped colour to the 'Shop' button
    #self.setColour[2]: Mapped colour to the 'Return To Main Menu' button

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes
    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 200 and mousePosition[1] <= (200+80))):
      self.setColour[0] = WHITE #'Resume' button text changed to white

    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 400 and mousePosition[1] <= (400+80))):
      self.setColour[1] = WHITE #'Shop' button text changed to white

    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 600 and mousePosition[1] <= (600+80))):
      self.setColour[2] = WHITE #'Return To Main Menu' button text changed to white
      self.quit = False #This ensures that when the 'Return To Main Menu' button is clicked, the 'Quit' button is not also clicked. Ensures the game does not register two different buttons on different interfaces
      self.level2 = False #This ensures that when on the main menu interface, clicking 'Start Game' does not also play level 2 as this attribute is set to false

    #In all the texts below, you can see that the list values are being the colours therefore if list value changes, colour also changes
    self.resumeText = self.pauseTextFont.render("Resume", 1, self.setColour[0]) #This is the resume text which changes from black to white vice versa depending on mouse hover
    self.shopText = self.pauseTextFont.render("Shop", 1, self.setColour[1]) #This is the shop text which changes from black to white vice versa depending on mouse hover
    self.returnText = self.pauseTextFont.render("Return To Main Menu", 1, self.setColour[2]) #This is the return to main menu text which changes from black to white vice versa depending on mouse hover

    #These are what makes the pause menu seem like the game has completly frozen when 'Esc' pressed
    self.playerObject.disableMovement = True #Player movement is now disabled
    self.playerObject.playerAnimations = False #Player animations is now at stand still
    self.enemyObject.playerTrack = False #Enemy movement is now disabled
    self.enemyObject.enemyAnimations = False #Enemy animations is now at stand still

    self.window.blit(self.greenButton, (462, 181)) #This is the resume button image
    self.window.blit(self.blueButton, (462, 381)) #This is the shop button image
    self.window.blit(self.redButton, (462, 581)) #This is the return to main menu button images

    #The texts are then placed onto the screen
    self.window.blit(self.resumeText, (572, 215))
    self.window.blit(self.shopText, (592, 415))
    self.window.blit(self.returnText, (480, 615))

    if self.resumeButton.CheckState(self.mousePosition, self.mouseClick): #This checks if the resume button has been clicked using the 'CheckState' method
      self.playerObject.pause = False #Ensures that the pause screen interface is removed

      #When the resume button is clicked, these take effect if the values are set to true
      if self.instantHealthPotionBuy == True: #Checks if the health potion has been bought
        self.playerObject.playerHealth += 30 #If it has, increase player hp by 30
        if self.playerObject.playerHealth >= 100: #Checks if the player hp is 100 or over
          self.playerObject.playerHealth = 100 #Ensures the player hp does not exceed 100 hp limit

      if self.speedPotionBuy == True: #Checks if the speed potion has been bought
        self.playerObject.speedBoostEffect = True #Ensures the player an get their velocity doubled
        self.playerObject.SpeedPotionBuyTime() #Resets the 'self.currentSpeedTime' attribue to the time of bought. Ensures speed potion lasts for 10 seconds

      #These are then returned back to their normal state
      self.playerObject.disableMovement = False #Player movement is now enabled
      self.playerObject.playerAnimations = True #Player animations is now enabled
      self.enemyObject.playerTrack = True #Enemy movement is now enabled
      self.enemyObject.enemyAnimations = True #Enemy animations is now enabled

    if self.shopButton.CheckState(self.mousePosition, self.mouseClick): #This checks if the shop button has been clicked using the 'CheckState' method
      self.shop = True #Enables the shop screen interface to be shown


    if self.returnButton1.CheckState(self.mousePosition, self.mouseClick): #This checks if the return to main menu button has been clicked using the 'CheckState' method
      self.previousCoinCount += self.playerObject.coins #Holds the previous amount of coins within the level
      self.previousExpCount += self.playerObject.exp  #Holds the previous amount of experience within the level
      self.previousPlayerLevelCount += self.playerObject.playerLevel #Holds the previous player level within the level
      self.instantHealthPotionBuy = False #Ensures that the health potion resets
      self.speedPotionBuy = False #Ensures that the health potion resets
      self.currentGameState = 1 #This then changes the interface back to the main menu interface
      self.RemoveItems() #This ensures that the current coins and potions are removed from the list which ensures items can be randomised when levels are loaded up again

  def Shop(self, mousePosition, playerCoins):
    #Background of the shop screen interface
    pygame.draw.rect(self.window, SPACEBLUE, (0, 0, 1280, 720))

    #Shop title rectangle
    pygame.draw.rect(self.window, BLACK, (465 - 3, 20 - 3, 356, 86)) #Border of the shop title rectangle
    pygame.draw.rect(self.window, NAVYBLUE, (465, 20, 350, 80)) #Background colour of the shop title rectangle

    #Coin counter rectangle
    pygame.draw.rect(self.window, BLACK, (20 - 3, 20 - 3, 111, 86)) #Border of the coin counter rectangle
    pygame.draw.rect(self.window, WHITE, (20, 20, 105, 80)) #Background colour of the coin counter rectangle

    #Shop title text
    self.shopTitle = self.shopTitleTextFont.render("Shop", 1, WHITE)
    self.window.blit(self.shopTitle, (570, 10))

    for buttons in self.shopInterfaceList: #This iterates through the buttons within the list
      buttons.DrawButton(self.window) #For each button, it draws it on the screen at the desired x and y coordinates

    #Instant health potion rectangle
    pygame.draw.rect(self.window, BLACK, (160 - 3, 200 - 3, 306, 306)) #Border of the instant health potion rectangle
    if self.instantHealthPotionBuy == False: #Checks if the potion has been bought
      pygame.draw.rect(self.window, DARKRED2, (160, 200, 300, 300)) #If it has not, ensure the background colour of the rectangle is red
    else:
      pygame.draw.rect(self.window, GREY, (160, 200, 300, 300)) #If it has, ensure the background colour of the rectangle is grey

    #Speed potion rectangle
    pygame.draw.rect(self.window, BLACK, (800 - 3, 200 - 3, 306, 306)) #Border of the speed potion rectangle
    if self.speedPotionBuy == False: #Checks if the potion has been bought
      pygame.draw.rect(self.window, LIGHTBLUE, (800, 200, 300, 300)) #If it has not, ensure the background colour of the rectangle is blue
    else:
      pygame.draw.rect(self.window, GREY, (800, 200, 300, 300)) #If it has, ensure the background colour of the rectangle is grey

    self.setColour = [BLACK, BLACK] #List of colours which is mapped to a corresponding button
    #self.setColour[0]: Mapped colour to the 'Instant Health Potion' button
    #self.setColour[1]: Mapped colour to the 'Shop' button
    #self.setColour[2]: Mapped colour to the 'Speed Potion' button

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes
    if ((mousePosition[0] >= 160 and mousePosition[0] <= (160+300)) and (mousePosition[1] >= 200 and mousePosition[1] <= (200+300))):
      self.setColour[0] = WHITE #'Instant Health Potion' button text changed to white
      self.healthPotion = True

    if ((mousePosition[0] >= 800 and mousePosition[0] <= (800+300)) and (mousePosition[1] >= 200 and mousePosition[1] <= (200+300))):
      self.setColour[1] = WHITE #'Speed Potion' button text changed to white

    #Title of the instant health potion rectangle
    self.instantHealthText = self.shopTextFont.render("Instant Health Potion", 1, self.setColour[0])
    self.window.blit(self.instantHealthText, (161, 200))

    #Title of the speed potion rectangle
    self.speedText = self.shopTextFont.render("Speed Potion", 1, self.setColour[1])
    self.window.blit(self.speedText, (860, 200))

    #Placing the respective potion images on the screen
    self.window.blit(self.healthStillImage, (225, 200))
    self.window.blit(self.speedStillImage, (875, 200))

    #Shows the price and amount of coins needed to buy the potion. Shows a coin image instead of a text to reduce space usage
    self.instantHealthPriceText = self.shopTextFont.render("14", 1, BLACK)
    self.window.blit(self.instantHealthPriceText, (315, 456))
    self.window.blit(self.coinStillImage, (260, 445))

    #Shows the price and amount of coins needed to buy the potion. Shows a coin image instead of a text to reduce space usage
    self.speedPriceText = self.shopTextFont.render("8", 1, BLACK)
    self.window.blit(self.speedPriceText, (965, 456))
    self.window.blit(self.coinStillImage, (910, 445))

    #Located top left of screen. Shows how much coins the player currently has collected
    self.playerCoinsText = self.shopTextFont.render(str(playerCoins), 1, BLACK)
    self.window.blit(self.playerCoinsText, (85, 40))
    self.window.blit(self.coinStillImage, (20, 30))

    #Prices of the potions
    self.instantHealthPrice = 14
    self.speedHealthPrice = 8

    if self.instantHealthPotionButton.CheckState(self.mousePosition, self.mouseClick) and (self.instantHealthPotionBuy == False): #Checks if the potion button has been clicked and if the potions has not been bought
      if self.playerObject.coins >= self.instantHealthPrice: #Checks if the amount of coins the player has is greater than the instant health potion price
        self.playerObject.coins -= self.instantHealthPrice #Reduces the player coins by that amount if true
        self.instantHealthPotionBuy = True #Player has boguht the item therefore cannot buy anymore

    if self.speedPotionButton.CheckState(self.mousePosition, self.mouseClick) and (self.speedPotionBuy == False): #Checks if the potion button has been clicked and if the potions has not been bought
      if self.playerObject.coins >= self.speedHealthPrice: #Checks if the amount of coins the player has is greater than the speed potion price
        self.playerObject.coins -= self.speedHealthPrice #Reduces the player coins by that amount if true
        self.speedPotionBuy = True #Player has boguht the item therefore cannot buy anymore

    if self.keysPressed[pygame.K_ESCAPE]: #Checks if the 'Esc' button has been clicked
      self.shop = False #Closes the shop and returns the player back to the shop screen interface

  def WinMenu(self, mousePosition): #This holds the buttons for the win screen and how the buttons will change when hovered
    self.transparentSurface = pygame.Surface((1280, 720), pygame.SRCALPHA) #Alpha method allows a transparent black box to be created onto the surface of the screen
    self.transparentSurface.fill((0, 0, 0, 200)) #Transparency using 4th index (alpha value)
    self.window.blit(self.transparentSurface, (0, 0)) #Placed the black transparent rectangle onto the screen

    for buttons in self.winInterfaceList: #This iterates through the buttons within the list
      buttons.DrawButton(self.window) #For each button, it draws it on the screen at the desired x and y coordinates

    self.winTitle = self.winTitleTextFont.render("You Win!", 1, WHITE) #The text for the title of the interface
    self.window.blit(self.winTitle, (505, 80)) #Places the text of the win title onto the screen

    self.setColour = [BLACK, BLACK] #List of colours which is mapped to a corresponding button
    #self.setColour[0]: Mapped colour to the 'Next Level' button
    #self.setColour[1]: Mapped colour to the 'Return To Main Menu' button

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes
    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 200 and mousePosition[1] <= (200+80))):
      self.setColour[0] = WHITE #'Next Level' button text changed to white

    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 400 and mousePosition[1] <= (400+80))):
      self.setColour[1] = WHITE #'Return To Main Menu' button text changed to white

    self.window.blit(self.blueButton, (462, 181)) #This is the next level button image
    self.window.blit(self.redButton, (462, 381)) #This is the return to main menu button image

    #In all the texts below, you can see that the list values are being the colours therefore if list value changes, colour also changes
    self.nextLevelText = self.winTextFont.render("Next Level", 1, self.setColour[0]) #This is the next level text which changes from black to white vice versa depending on mouse hover
    self.returnText = self.winTextFont.render("Return To Main Menu", 1, self.setColour[1]) #This is the return to main menu text which changes from black to white vice versa depending on mouse hover

    #The texts are then placed onto the screen
    self.window.blit(self.nextLevelText, (552, 215))
    self.window.blit(self.returnText, (480, 415))

    if self.nextLevelButton.CheckState(self.mousePosition, self.mouseClick): #This checks if the next level button has been clicked using the 'CheckState' method
      self.previousCoinCount += self.playerObject.coins #Holds the previous amount of coins within the level
      self.previousExpCount += self.playerObject.exp  #Holds the previous amount of experience within the level
      self.previousPlayerLevelCount += self.playerObject.playerLevel #Holds the previous player level within the level
      self.instantHealthPotionBuy = False #Ensures that the health potion resets
      self.speedPotionBuy = False #Ensures that the health potion resets
      self.RemoveItems() #Clears the coins and potions from their respective lists
      self.RandomiseItems() #Generate new coins and potions for the next level to ensure randomised coins and potions for each level

      self.level += 1 #Increases level counter by one to ensure main game features changes
      if self.level == 2: #Checks if the level is level 2
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 8) #Spawns the player within level 2 and its statistics

        self.playerObject.coins = self.previousCoinCount #Sets the new coin count to the amount of coins the player had in the previous level
        self.previousCoinCount = 0 #Ensures that the previous sets to zero to ensure that when in a new level, it can remember the previous coins again

        self.playerObject.exp = self.previousExpCount #Sets the new experience to the amount of experience the player had in the previous level
        self.previousExpCount = 0 #Ensures that the previous sets to zero to ensure that when in a new level, it can remember the previous experience again

        self.playerObject.playerLevel = self.previousPlayerLevelCount #Sets the new player level to the previous player level in the previous level
        self.previousPlayerLevelCount = 0 #Ensures that the previous sets to zero to ensure that when in a new level, it can remember the previous player level again

        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.enemy2, 4, 12) #Spawns the level 2 enemy

        #Spawning only two platforms within level 2
        self.platform2 = Platform(60, 150, 350, 30)
        self.platform3 = Platform(860, 150, 350, 30)
        self.platformList = [self.platform2, self.platform3]

      if self.level == 3: #Checks if the level is level 3
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 5) #Spawns the player within level 3 and its statistics

        self.playerObject.coins = self.previousCoinCount #Sets the new coin count to the amount of coins the player had in the previous level
        self.previousCoinCount = 0 #Ensures that the previous sets to zero to ensure that when in a new level, it can remember the previous coins again

        self.playerObject.exp = self.previousExpCount #Sets the new experience to the amount of experience the player had in the previous level
        self.previousExpCount = 0 #Ensures that the previous sets to zero to ensure that when in a new level, it can remember the previous experience again

        self.playerObject.playerLevel = self.previousPlayerLevelCount #Sets the new player level to the previous player level in the previous level
        self.previousPlayerLevelCount = 0 #Ensures that the previous sets to zero to ensure that when in a new level, it can remember the previous player level again

        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.boss, 5, 17) #Spawns the level 3 enemy

        #Spawning only one platform within level 1
        self.platform1 = Platform(460, 350, 350, 30)
        self.platformList = [self.platform1]

    if self.returnButton2.CheckState(self.mousePosition, self.mouseClick): #This checks if the return to main menu button has been clicked using the 'CheckState' method
      self.instantHealthPotionBuy = False #Ensures that the health potion resets
      self.speedPotionBuy = False #Ensures that the health potion resets
      self.currentGameState = 1 #This then changes the interface back to the main menu interface
      self.settings = False #This ensures that when this button is clicked, the settings button is not also clicked
      self.level2 = False #This ensures that when the 'Start Game' button is clicked, level 2 does not load up as well
      self.RemoveItems() #This ensures that the current coins and potions are removed from the list which ensures items can be randomised when levels are loaded up again

  def WinMenu2(self, mousePosition): #This holds the buttons for the win screen and how the buttons will change when hovered
    self.transparentSurface = pygame.Surface((1280, 720), pygame.SRCALPHA) #Alpha method allows a transparent black box to be created onto the surface of the screen
    self.transparentSurface.fill((0, 0, 0, 200)) #Transparency using 4th index (alpha value)
    self.window.blit(self.transparentSurface, (0, 0)) #Placed the black transparent rectangle onto the screen

    self.returnButton2.UpdateAttribute(480, 200, 300, 80) #This method of the button updates the return button from the middle position to the top position
    self.returnButton2.DrawButton(self.window) #This then draws this newly updated button onto the screen

    self.winTitle = self.winTitleTextFont.render("You Win!", 1, WHITE) #The text for the title of the interface
    self.window.blit(self.winTitle, (505, 80)) #Places the text of the win title onto the screen

    self.setColour = [BLACK] #List of colours which is mapped to a corresponding button
    #self.setColour[0]: Mapped colour to the 'Return To Main Menu' button

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes
    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 200 and mousePosition[1] <= (200+80))):
      self.setColour[0] = WHITE #'Return To Main Menu' button text changed to white

    self.window.blit(self.redButton, (462, 181)) #This is the return to main menu button image

    self.returnText = self.winTextFont.render("Return To Main Menu", 1, self.setColour[0]) #This is the return to main menu text which changes from black to white vice versa depending on mouse hover

    #The text is then placed onto the screen
    self.window.blit(self.returnText, (480, 215))

    if self.returnButton2.CheckState(self.mousePosition, self.mouseClick) and (self.playerObject.returnMain == True): #This checks if the return to main menu button has been clicked using the 'CheckState' method
      #'self.returnMain' within the player object must be set to true in order for this return button to work. This button is to ensure when the 'Next Level' button is clicked within level 1 or 2, that it does not make the interface go back to main menu
      #This is because the 'Return To Main Menu' button is in the same position as 'Next Level' so this means the mouse left click could click all three buttons
      self.instantHealthPotionBuy = False #Ensures that the health potion resets
      self.speedPotionBuy = False #Ensures that the health potion resets
      self.returnButton2.UpdateAttribute(480, 400, 300, 80) #After it is clicked, return the button back to original position
      self.playerObject.returnMain = False #Sets back to false so when 'Next Level' button is clicked, will not produce the main menu error
      self.currentGameState = 1 #This then changes the interface back to the main menu interface
      self.settings = False #This ensures that when this button is clicked, the settings button is not also clicked
      self.level2 = False #This ensures that when the 'Start Game' button is clicked, level 2 does not load up as well
      self.level = 1 #Sets the interface back to level 1, but can change depending on the level clicks which will set the level to a new level. For example clicking level 2 button will set 'self.level' to 2
      self.RemoveItems() #This ensures that the current coins and potions are removed from the list which ensures items can be randomised when levels are loaded up again

  def LoseMenu(self, mousePosition): #This holds the buttons for the win screen and how the buttons will change when hovered
    self.transparentSurface = pygame.Surface((1280, 720), pygame.SRCALPHA) #Alpha method allows a transparent black box to be created onto the surface of the screen
    self.transparentSurface.fill((0, 0, 0, 200)) #Transparency using 4th index (alpha value)
    self.window.blit(self.transparentSurface, (0, 0)) #Placed the black transparent rectangle onto the screen

    for buttons in self.loseInterfaceList: #This iterates through the buttons within the list
      buttons.DrawButton(self.window) #For each button, it draws it on the screen at the desired x and y coordinates

    self.loseTitle = self.loseTitleTextFont.render("You Lose!", 1, WHITE) #The text for the title of the interface
    self.window.blit(self.loseTitle, (505, 80)) #Places the text of the lose title onto the screen

    self.setColour = [BLACK, BLACK] #List of colours which is mapped to a corresponding button
    #self.setColour[0]: Mapped colour to the 'Try Again' button
    #self.setColour[1]: Mapped colour to the 'Return To Main Menu' button

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes
    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 200 and mousePosition[1] <= (200+80))):
      self.setColour[0] = WHITE #'Try Again' button text changed to white

    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 400 and mousePosition[1] <= (400+80))):
      self.setColour[1] = WHITE #'Return To Main Menu' button text changed to white

    self.window.blit(self.greenButton, (462, 181)) #This is the try again button image
    self.window.blit(self.redButton, (462, 381)) #This is the return to main menu button image

    #In all the texts below, you can see that the list values are being the colours therefore if list value changes, colour also changes
    self.tryAgainText = self.loseTextFont.render("Try Again", 1, self.setColour[0]) #This is the try again text which changes from black to white vice versa depending on mouse hover
    self.returnText = self.loseTextFont.render("Return To Main Menu", 1, self.setColour[1]) #This is the return to main menu text which changes from black to white vice versa depending on mouse hover

    #The texts are then placed onto the screen
    self.window.blit(self.tryAgainText, (558, 215))
    self.window.blit(self.returnText, (480, 415))

    if self.tryAgainButton1.CheckState(self.mousePosition, self.mouseClick): #This checks if the try again button has been clicked using the 'CheckState' method
      self.RemoveItems() #Clears the coins and potions from their respective lists
      self.RandomiseItems() #Generate new coins and potions for the next level to ensure randomised coins and potions for each level

      if self.level == 1: #Checks if the current level is 1
        #Loads the corresponding player and enemy again for that level
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 10)
        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.enemy1, 3, 5)

      if self.level == 2: #Checks if the current level is 2
        #Loads the corresponding player and enemy again for that level
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 8)
        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.enemy2, 4, 12)

      if self.level == 3: #Checks if the current level is 3
        #Loads the corresponding player and enemy again for that level
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 5)
        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.boss, 5, 17)

    if self.returnButton3.CheckState(self.mousePosition, self.mouseClick): #This checks if the return to main menu button has been clicked using the 'CheckState' method
      self.instantHealthPotionBuy = False #Ensures that the health potion resets
      self.speedPotionBuy = False #Ensures that the health potion resets
      self.currentGameState = 1 #This then changes the interface back to the main menu interface
      self.settings = False #This ensures that when this button is clicked, the settings button is not also clicked
      self.level2 = False #This ensures that when the 'Start Game' button is clicked, level 2 does not load up as well
      self.RemoveItems() #This ensures that the current coins and potions are removed from the list which ensures items can be randomised when levels are loaded up again

  def DrawMenu(self, mousePosition): #This holds the buttons for the win screen and how the buttons will change when hovered
    self.transparentSurface = pygame.Surface((1280, 720), pygame.SRCALPHA) #Alpha method allows a transparent black box to be created onto the surface of the screen
    self.transparentSurface.fill((0, 0, 0, 200)) #Transparency using 4th index (alpha value)
    self.window.blit(self.transparentSurface, (0, 0)) #Placed the black transparent rectangle onto the screen

    for buttons in self.drawInterfaceList: #This iterates through the buttons within the list
      buttons.DrawButton(self.window) #For each button, it draws it on the screen at the desired x and y coordinates

    self.drawTitle = self.drawTitleTextFont.render("Draw!", 1, WHITE) #The text for the title of the interface
    self.window.blit(self.drawTitle, (540, 80)) #Places the text of the draw title onto the screen

    self.setColour = [BLACK, BLACK] #List of colours which is mapped to a corresponding button
    #self.setColour[0]: Mapped colour to the 'Try Again' button
    #self.setColour[1]: Mapped colour to the 'Return To Main Menu' button

    #The if statements below check if the mouse positions are between the coordinates of x and y and between the width and height of the buttons. If they are, the colour of the text changes
    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 200 and mousePosition[1] <= (200+80))):
      self.setColour[0] = WHITE #'Try Again' button text changed to white

    if ((mousePosition[0] >= 480 and mousePosition[0] <= (480+300)) and (mousePosition[1] >= 400 and mousePosition[1] <= (400+80))):
      self.setColour[1] = WHITE #'Return To Main Menu' button text changed to white

    self.window.blit(self.greenButton, (462, 181)) #This is the try again button image
    self.window.blit(self.redButton, (462, 381)) #This is the return to main menu button image

    #In all the texts below, you can see that the list values are being the colours therefore if list value changes, colour also changes
    self.tryAgainText = self.loseTextFont.render("Try Again", 1, self.setColour[0]) #This is the try again text which changes from black to white vice versa depending on mouse hover
    self.returnText = self.loseTextFont.render("Return To Main Menu", 1, self.setColour[1]) #This is the return to main menu text which changes from black to white vice versa depending on mouse hover

    #The texts are then placed onto the screen
    self.window.blit(self.tryAgainText, (558, 215))
    self.window.blit(self.returnText, (480, 415))

    if self.tryAgainButton2.CheckState(self.mousePosition, self.mouseClick): #This checks if the try again button has been clicked using the 'CheckState' method
      self.RemoveItems() #Clears the coins and potions from their respective lists
      self.RandomiseItems() #Generate new coins and potions for the next level to ensure randomised coins and potions for each level

      if self.level == 1: #Checks if the current level is 1
        #Loads the corresponding player and enemy again for that level
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 10)
        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.enemy1, 3, 5)

      if self.level == 2: #Checks if the current level is 2
        #Loads the corresponding player and enemy again for that level
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 8)
        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.enemy2, 4, 12)

      if self.level == 3: #Checks if the current level is 3
        #Loads the corresponding player and enemy again for that level
        self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 5)
        self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.boss, 5, 17)

    if self.returnButton4.CheckState(self.mousePosition, self.mouseClick): #This checks if the return to main menu button has been clicked using the 'CheckState' method
      self.instantHealthPotionBuy = False #Ensures that the health potion resets
      self.speedPotionBuy = False #Ensures that the health potion resets
      self.currentGameState = 1 #This then changes the interface back to the main menu interface
      self.settings = False #This ensures that when this button is clicked, the settings button is not also clicked
      self.level2 = False #This ensures that when the 'Start Game' button is clicked, level 2 does not load up as well
      self.RemoveItems() #This ensures that the current coins and potions are removed from the list which ensures items can be randomised when levels are loaded up again

  def RandomiseItems(self): #This method is used to randomise the items within the game
    b = [self.coinList,self.healthPotionList,self.speedPotionList]
    for i in range(7):
      self.randomXSpawns = random.randint(0, 1220)
      self.randomYSpawns = random.randint(165, 500)
      if i % 3 == 0:
        b[0].append(Coin(self.randomXSpawns, self.randomYSpawns, COINSHIFT))
      if i % 3 == 1:
        b[1].append(InstantHealth(self.randomXSpawns, self.randomYSpawns))
      if i % 3 == 2:
        b[2].append(Speed(self.randomXSpawns, self.randomYSpawns))
    

  def RemoveItems(self): #This method ensures that all items within the list is cleared
    #Clears all the currently existing items inside the list
    self.coinList.clear()
    self.healthPotionList.clear()
    self.speedPotionList.clear()

  def NewGame(self): #This holds the main game loop and tells which interface should run. Also instantiates multiple buttons for various interfaces
    #Main menu interface buttons
    self.startButton = Button(480, 200, 300, 80)
    self.settingsButton = Button(480, 400, 300, 80)
    self.quitButton = Button(480, 600, 300, 80)
    self.mainMenuInterfaceList = [self.startButton, self.settingsButton, self.quitButton] #Appended to a list for easier drawing of the buttons

    #Level selector interface buttons
    self.level1Button = Button(70, 200, 300, 300)
    self.level2Button = Button(490, 200, 300, 300)
    self.level3Button = Button(910, 200, 300, 300)
    self.levelSelectorInterfaceList = [self.level1Button, self.level2Button, self.level3Button] #Appended to a list for easier drawing of the buttons

    #Pause screen interface buttons
    self.resumeButton = Button(480, 200, 300, 80)
    self.shopButton = Button(480, 400, 300, 80)
    self.returnButton1 = Button(480, 600, 300, 80)
    self.pauseInterfaceList = [self.resumeButton, self.shopButton, self.returnButton1] #Appended to a list for easier drawing of the buttons

    #Win screen interface buttons
    self.nextLevelButton = Button(480, 200, 300, 80)
    self.returnButton2 = Button(480, 400, 300, 80)
    self.winInterfaceList = [self.nextLevelButton, self.returnButton2] #Appended to a list for easier drawing of the buttons

    #Lose screen interface buttons
    self.tryAgainButton1 = Button(480, 200, 300, 80)
    self.returnButton3 = Button(480, 400, 300, 80)
    self.loseInterfaceList = [self.tryAgainButton1, self.returnButton3] #Appended to a list for easier drawing of the buttons

    #Draw screen interface buttons
    self.tryAgainButton2 = Button(480, 200, 300, 80)
    self.returnButton4 = Button(480, 400, 300, 80)
    self.drawInterfaceList = [self.tryAgainButton2, self.returnButton4] #Appended to a list for easier drawing of the buttons

    self.instantHealthPotionButton = Button(160, 200, 300, 300)
    self.speedPotionButton = Button(800, 200, 300, 300)
    self.shopInterfaceList = [self.instantHealthPotionButton, self.speedPotionButton]

    self.run = True
    while self.run == True: #Main game loop - keeps running until 'self.run' becomes false
      self.clock.tick(FPS) #This sets the amount of time the loop should run per second. In this case, loops runs 60 frames per second
      for event in pygame.event.get():
        if event.type == pygame.QUIT: #When the player clicks the 'X' button on top right on the game window, game window closes
          self.run = False #Game window closes as attribute becomes false

      #These get the various inputs from the player
      self.keysPressed = pygame.key.get_pressed() #Gets the key inputs
      self.mousePosition = pygame.mouse.get_pos() #Gets the mouse positions
      self.mouseClick = pygame.mouse.get_pressed() #Gets the mouse click input

      if self.currentGameState >= 1: #If the current game state is above 1, this will ensure that the parallax background of the game loops constantly producing the continuous scrolling effect
        self.ParallaxBackground() #Calling the parallax background method

      if self.currentGameState == 1: #Checks if the current game state is the main menu interface
        if self.startButton.CheckState(self.mousePosition, self.mouseClick): #This checks if the start game button has been clicked using the 'CheckState' method
          self.currentGameState = 2 #This then loads the level selector interface

        if self.settingsButton.CheckState(self.mousePosition, self.mouseClick) and (self.settings == True): #This checks if the settings button has been clicked using the 'CheckState' method
          #'self.settings' must also be set to true because as buttons are overlapping within different interfaces, clicking 'Return To Main Menu' within the win/lose/draw screen turns on the settings interface
          #This does not return to the main menu interface. 'self.settings' set to true but false for when these buttons are clicked
          self.currentGameState = 3 #This then loads the settings interface

        if self.quitButton.CheckState(self.mousePosition, self.mouseClick) and (self.quit == True): #This checks if the quit button has been clicked using the 'CheckState' method
          #'self.quit' must also be set to true because as buttons are overlapping within different interfaces, clicking 'Return To Main Menu' within the pause screen quits the entire game
          #This does not return to the main menu interface. 'self.quit' set to true but false for when this buttons are clicked
          self.run = False

      if self.currentGameState == 2: #Checks if the current game state is the level selector interface interface
        if self.level1Button.CheckState(self.mousePosition, self.mouseClick): #This checks if the level 1 button has been clicked using the 'CheckState' method
          self.level = 1 #Sets the game level to 1
          self.currentGameState = 4 #Ensures the game interface runs

          #Loads the respective player and enemy for that level
          self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 10)

          self.playerObject.coins = self.previousCoinCount #Sets the current coin count to the previous coin count
          self.previousCoinCount = 0 #Resets the previous coin count so it can be remembered in the next level

          self.playerObject.exp = self.previousExpCount #Sets the current experience to the previous experience
          self.previousExpCount = 0 #Resets the previous experience so it can be remembered in the next level

          self.playerObject.playerLevel = self.previousPlayerLevelCount #Sets the current player level to the previous plaayer level
          self.previousPlayerLevelCount = 0 #Resets the previous player level so it can be remembered in the next level

          self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.enemy1, 3, 5)

          #Amount of platforms within the level
          self.platform1 = Platform(460, 350, 350, 30)
          self.platform2 = Platform(60, 150, 350, 30)
          self.platform3 = Platform(860, 150, 350, 30)
          self.platformList = [self.platform1, self.platform2, self.platform3]

          self.RandomiseItems() #This ensures that the items within the level is randomised for when the level 1 button is clicked

        if self.level2Button.CheckState(self.mousePosition, self.mouseClick) and (self.level2 == True): #This checks if the level 2 button has been clicked using the 'CheckState' method
          #Must also check if 'self.level2' is true when the 'Start Game' button is clicked because as the buttons are overlapping, this instantly loaded level 2
          #Default value is set to to false so this error does not occur. Then set to true when mouse hovers over the button

          self.level = 2 #Sets the game level to 2
          self.currentGameState = 4 #Ensures the game interface runs

          #Loads the respective player and enemy for that level
          self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 8)

          self.playerObject.coins = self.previousCoinCount #Sets the current coin count to the previous coin count
          self.previousCoinCount = 0 #Resets the previous coin count so it can be remembered in the next level

          self.playerObject.exp = self.previousExpCount #Sets the current experience to the previous experience
          self.previousExpCount = 0 #Resets the previous experience so it can be remembered in the next level

          self.playerObject.playerLevel = self.previousPlayerLevelCount #Sets the current player level to the previous plaayer level
          self.previousPlayerLevelCount = 0 #Resets the previous player level so it can be remembered in the next level

          self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.enemy2, 4, 12)

          #Amount of platforms within the level
          self.platform2 = Platform(60, 150, 350, 30)
          self.platform3 = Platform(860, 150, 350, 30)
          self.platformList = [self.platform2, self.platform3]

          self.RandomiseItems() #This ensures that the items within the level is randomised for when the level 2 button is clicked

        if self.level3Button.CheckState(self.mousePosition, self.mouseClick) and (self.bossLock == False): #This checks if the level 3 button has been clicked using the 'CheckState' method
          #Must also check if 'self.bossLock' is false because if the player completes level 1 or 2, this level will unlock allowing the player to be able to click the level 3 button

          self.level = 3 #Sets the game level to 3
          self.currentGameState = 4 #Ensures the game interface runs

          #Loads the respective player and enemy for that level
          self.playerObject = Player(200, 410, PLAYERSIZES, PLAYERSCALE, PLAYERSHIFT, 5)

          self.playerObject.coins = self.previousCoinCount #Sets the current coin count to the previous coin count
          self.previousCoinCount = 0 #Resets the previous coin count so it can be remembered in the next level

          self.playerObject.exp = self.previousExpCount #Sets the current experience to the previous experience
          self.previousExpCount = 0 #Resets the previous experience so it can be remembered in the next level

          self.playerObject.playerLevel = self.previousPlayerLevelCount #Sets the current player level to the previous plaayer level
          self.previousPlayerLevelCount = 0 #Resets the previous player level so it can be remembered in the next level

          self.enemyObject = Enemy(800, 450, ENEMYSIZES, ENEMYSCALE, ENEMYSHIFT, self.boss, 5, 17)

          #Amount of platforms within the level
          self.platform1 = Platform(460, 350, 350, 30)
          self.platformList = [self.platform1]

          self.RandomiseItems() #This ensures that the items within the level is randomised for when the level 3 button is clicked

      self.DrawWindow() #This method will run to ensure the interfaces that is to be run is ran via button clicks
      pygame.display.update() #Updates the display constantly

createGame = Game() #Creates an object for the 'Game' class
createGame.NewGame() #Calls the 'NewGame' method to allow game to run