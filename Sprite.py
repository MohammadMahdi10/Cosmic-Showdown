#Importing the key libraries for the game
import pygame
import os
from Settings import * #This imports from the 'Settings.py' file - Holds the constants

class Player: #This is the template which holds the entire player functionality of the game
  def __init__(self, x, y, playerSizes, playerScale, playerShift, playerDamage): #Constructior which takes in the constants within the 'Settings.py' of: PLAYERSIZES (constant list), PLAYERSCALE (constant value), PLAYERSHIFT (constant list)
    #The player damage is an integer value which determines amount of damage the enemy takes

    #Player properties:
    self.x = x #This sets the starting x value of the player
    self.y = y #This sets the starting y value of the player

    self.previousXPosition = x #This holds the previous x value of the player rectangle. Used within the 'Movement' method
    self.previousYPosition = y #This holds the previous y value of the player rectangle. Used within the 'Movement' method

    self.changeInX = 0 #This sets this value to the change within the player x value
    self.changeInY = 0 #This sets this value to the change within the player y value

    self.yVelocity = 0 #This sets the jump speed of the player

    self.currentEffect = "Nothing..." #This is used to display what potion is currently in effect. For example colliding with a speed potion will change this variable to "Speed"

    self.playerHealth = 100 #This is the starting health value of the player

    self.coins = 0 #The amount of coins the player has
    self.exp = 0 #The amount of exp the player has
    self.playerLevel = 1 #The player current level

    #Natural regeneration:
    self.regenerationTimeInterval = 60 * 1000 #How long till the natural regneration for the player starts (1 minute)
    self.regenerationLastTime = pygame.time.get_ticks() #This gets the last time the player regenerated to ensure precise calculations of when the player needs to regenerate again

    #Speed boost:
    self.speedBoostEffect = False #Default false ensures player velocity stays low. If set to true, player velocity doubles for a set periof
    self.speedBoostDuration = 10000 #How long the speed boost should last for (10 seconds)
    self.currentSpeedTime = 0 #Currently set to 0 but will hold the speed timer within the 'Movements' method

    self.playerSheet = pygame.image.load(os.path.join(('Player/NEW_PLAYER.png'))).convert_alpha() #This is the player sprite sheet
    self.playerAnimationIndex = [10, 4, 4, 5, 9, 3, 2, 2, 6] #These are the index values for the player animations

    self.sizeX = playerSizes[0] #This is the x horizontal size of the square that is to be used to create a square
    self.sizeY = playerSizes[1] #This is the y vertical size of the square that is to be used to create a square
    self.playerScale = playerScale #This will enlargement the player image squares
    self.playerShiftX = playerShift[0] #This will offset the player by a set amount in the x direction to ensure the player images is inline with the player rectangle
    self.playerShiftY = playerShift[1] #This will offset the player by a set amount in the y direction to ensure the player images is inline with the player rectangle

    self.animationsList = self.SpriteAnimations() #This holds the entire 2D array of the list of player animations
    self.currentAction = 0 #This sets to one of the list within the 2D array to play that entire animation
    #self.currentAction = 0: Idle animation
    #self.currentAction = 1: Attack 1 animation
    #self.currentAction = 2: Attack 2 animation
    #self.currentAction = 3: Attack 3 animation
    #self.currentAction = 4: Death animation
    #self.currentAction = 5: Taken damage animation
    #self.currentAction = 6: Fall animation
    #self.currentAction = 7: Jump animation
    #self.currentAction = 8: Run animation

    self.currentFrame = 0 #This will go through each square within the 'self.animationsList' list mapped by the 'self.currentAction' attribute to show the animation on screen
    self.currentImage = self.animationsList[self.currentAction][self.currentFrame] #Maps the 'self.currentAction' to a list and 'self.currentFrame' to the items within the list to show the current image on screen

    self.flipH = False #Default facing is right so when this is set to true, flips player to the left

    self.playerAnimations = True #Ensures player animations play but when they are defeated, this will stop all animations when set to false
    self.running = False #Used to play the player running animation
    self.jumping = True #Used to play the player jump animation and to ensure that the player can press the jump button
    self.attackAnimation = False #Used to play the player attack animation
    self.playerDeath = False #Used to play the player death animation
    self.playerTakenDamage = False #Used to play the player taken damage animation

    self.disableMovement = False #Used to stop the player inputs. Ensures player cannot click any buttons when they are defeated

    self.attack = False #False ensures player is not attacking but true ensures player is attacking. Can then be used to manipulate other parts of code

    self.attackDamage = playerDamage #Amount of damage the player will do

    #Cooldowns for the animations
    self.attackCooldown = 0 #This ensures player attacks once for every few seconds
    self.damageCooldown = 0
    self.deathCooldown = 0
    self.attackCooldownAnimation = 0

    #Interface functions
    self.win = False #Used to check if the player has won to load up player win interface
    self.lose = False #Used to check if the player has lost to load up player lose interface
    self.draw = False #Used to check if the player has draw to load up player draw interface
    self.pause = False #Used to check if the player has clicked the 'Esc' button to load up the pause screen interface

    self.playerWin = False #Used as a checker to allow the win timer to function correctly
    self.playerLoss = False #Used as a checker to allow the lose timer to function correctly
    self.playerDraw = False #Used as a checker to allow the draw timer to function correctly

    self.returnMain = False #Ensures that the player can click the 'Next Level' at level 1 or 2 but not go back to the main menu screen. When set to true, allows the player to click 'Return To Main Menu' in level 3 win screen

    self.onPlatform = False #Ensures the code knowns when the player has collided with the platform rectangle which can suitably update the y velocity of the player new ground level

    #Other
    self.updateTime = pygame.time.get_ticks() #Current game time for animation
    self.playerRectangle = pygame.Rect((self.x, self.y, PLAYERWIDTH, PLAYERHEIGHT)) #This creates a rectangle with the player x, y, width and height

  def Controls(self, window, Enemy, speed):
    #Code beneath is for when the player has collided with the speed potion
    keysPressed = pygame.key.get_pressed() #This gets the player inputs
    if keysPressed[pygame.K_d]: #Checks if the 'D' button has been pressed
      self.flipH = False #Running right so flip not needed therefore set to false
      self.changeInX = (PLAYERVELOCITYX*speed) #Doubles player velocity to the right
      self.running = True #Ensures running animation plays
  
    elif keysPressed[pygame.K_a]: #Checks if the 'A' button has been pressed
      self.flipH = True #Running left so flip needed therefore set to true
      self.changeInX = -(PLAYERVELOCITYX*speed) #Doubles player velocity to the left
      self.running = True #Ensures running animation plays
    else:
      self.changeInX = 0 #This ensures that if the player is not pressing the 'A' or 'D' key, that the change in x becomes 0 to ensure the player stays still
  
    if keysPressed[pygame.K_w] and self.jumping == True: #Checks if the 'W' button has been pressed and if the player is allowed to jump again 
      self.Jumping() #Runs the 'Jumping' method
  
    if keysPressed[pygame.K_l]: #Checks if the 'L' button has been pressed
      self.attackAnimation = True #Ensures the attack animation plays when 'L' clicked
      if self.attackCooldown == 0: #Checks whether the attack cooldown is 0 to ensure the player can attack. If not 0, player cannot attack and the enemy won't lose health
        self.attack = True #If cooldown 0, set attack to true to ensure player is attacking
  
        #This creates an attack rectangle that sticks out from the player rectangle which is the attack of the player. This is a proportion of the original rectangle
        self.attackBox = pygame.Rect(self.playerRectangle.centerx - (self.playerRectangle.width * self.flipH),self.playerRectangle.y, self.playerRectangle.width, self.playerRectangle.height)
        if self.attackBox.colliderect(Enemy.enemyRectangle): #Checks if the 'attackBox' has collided with the body of the enemy
          Enemy.enemyTakenDamage = True #Ensure enemy taken damage animation plays
          Enemy.enemyHealth -= self.attackDamage #Ensure that the enemy loses health which is determined by the player attack
          self.attackCooldown = 50 #Sets the attack cooldown for if the player has collide its attack with the enemy
          self.PlayerLevelChecker(5, Enemy) #Gives the player 5 experience points if collision successful
  
        #pygame.draw.rect(window, RED, self.attackBox) #Draws the attack rectangle on the screen even if the player does not collide. Provides realism
  
        if Enemy.enemyHealth <= 0: #Checks whether the enemy health is below or equal to 0
          Enemy.enemyHealth = 0 #Sets it to 0 to ensure enemy does not have negative health
          self.playerWin = True #This allows the timers within 'Main.py' to be able to be subtracted from each other and checked if it is greater or equal to 3 seconds
          self.winTimer = pygame.time.get_ticks() #Gets the time at which the enemy has been defeated
          self.PlayerLevelChecker(100, Enemy) #As enemy has been defeated, give player 100 exp
  
        if self.playerHealth == 0 and Enemy.enemyHealth == 0: #Checks if the player and enemy health has become 0
          self.playerHealth = 0
          Enemy.enemyHealth = 0
          self.draw = True #Ensures the player draw screen pops up
          self.playerDraw = True #This allows the timers within 'Main.py' to be able to be subtracted from each other and checked if it is greater or equal to 3 seconds
          self.drawTimer = pygame.time.get_ticks() #Gets the time at which the player and enemy have both been defeated
  
    if keysPressed[pygame.K_ESCAPE]: #Checks if the 'Esc' button has been pressed
      self.pause = True #Ensures the pause screen interface shows
  
  def Movements(self, window, Enemy, coinList, healthPotionList, speedPotionList, platformList): #This method is used to control the player movements, collisions and inputs
    #Parameters ensures player can interact with these items
    self.running = False #Set to false player running animation does not play
    if self.disableMovement == False: #Checks whether the player is able to move around or attack
      if self.speedBoostEffect == True: #Th checks that if the player speed potion has been collided with and that this attribute has been changed to true, tishis should double player speed
        self.Controls(window, Enemy, 2)
      else:
        self.Controls(window, Enemy, 1)

    self.previousXPosition = self.playerRectangle.x #Remembers the player previous x position - Ensures player does not go beyond x border
    self.previousYPosition = self.playerRectangle.y #Remembers the player previous y position - Ensures player does not go beyond y border

    self.GravityEffect() #Sets the player to the ground which ensures player does not go beyond the ground border. Makes player fall here

    if (self.playerRectangle.bottom + self.changeInY) > (HEIGHT - 70): #Checks if the bottom of the player rectangle, including the jump, has gone beyond the border of the ground
      #"- 70" is so that the ground becomes 650 and not 720 as this will be beyond the ground border

      self.yVelocity = 0 #Set back to 0 to ensure player can jump again as this value controls the jump velocity. Ensures player does not keep going upwards
      self.changeInY = (HEIGHT - 70 - self.playerRectangle.bottom) #This limits the ground border for the player to just about land above the ground border as exceeding this will make the player fall continuously
      self.jumping = True #Player can now jump once again

    self.playerRectangle.x += self.changeInX #Sets the increase of the player x by the change in x value
    self.playerRectangle.y += self.changeInY #Sets the increase of the player y by the change in x value

    if (self.playerRectangle.left < 0) or (self.playerRectangle.right > WIDTH): #Checks if the player has exceeded the width of the screen in the right side and left side
      self.playerRectangle.x = self.previousXPosition #Returns player back to the previous x position of the player x rectangle to ensure player does not exceed border

    if self.attackCooldown > 0: #Checks if the attack cooldown is greater than 0
      self.attackCooldown -= 1 #Subtracts 1 until it is smaller than 0 to allow player to attack again

    if self.attackCooldownAnimation > 0: #Checks if the attack cooldown animation is greater than 0
        self.attackCooldownAnimation -= 1 #Subtracts 1 until it is smaller than 0
        if self.attackCooldownAnimation == 0: #If it is set to 0 at one point during the subraction
          self.attackAnimation = False #Then let the attribute turn false to allow player attack animation to stop running

    if self.damageCooldown > 0: #Checks if the player damage cooldown animation is greater than 0
      self.damageCooldown -= 1 #Subtracts 1 until it is smaller than 0
      if self.damageCooldown == 0: #If it is set to 0 at one point during the subraction
        self.playerTakenDamage = False #Then let the attribute turn false to allow player damage animation to stop running

    if self.deathCooldown > 0: #Checks if the player death cooldown animation is greater than 0
      self.deathCooldown -= 1 #Subtracts 1 until it is smaller than 0
      if self.deathCooldown == 0: #If it is set to 0 at one point during the subraction
        self.playerAnimations = False #Then let the attribute turn false to allow player death animation to stop running
        self.currentAction = 4 #This sets to the 5th list within the 2D array which is the death list
        self.currentFrame = 8 #Chooses the last frame within the list to halt to a pause
        self.currentImage = self.animationsList[self.currentAction][self.currentFrame] #Sets this image to the current image to display on screen

    if self.playerHealth == 0: #Checks if the player health has become 0
        Enemy.playerTrack = False #Make the enemy stop moving
        self.playerTakenDamage = False #Make the player stop taking damage
        self.playerDeath = True #Play the death animation
        self.disableMovement = True #Ensure that the player cannot click any buttons to move character on screen
        Enemy.attack = False #Ensure that the enemy cannot attack the player anymore
        Enemy.enemyAnimations = False #Make the enemy animations stop occuring
        Enemy.attacking = False #Make the enemy attack animations stop
        self.lose = True

    for coins in coinList: #Iterates through each item within the coin list
      if self.playerRectangle.colliderect(coins.coinRectangle): #Checks if the player rectangle has collided with the coins rectangle
        self.coins += 10 #Gives the player 10 coins for when it collided with the coin
        coinList.remove(coins) #Removes that collided coin from the list which removes it visually

    for health in healthPotionList: #Iterates through each item within the health potion list
      if self.playerRectangle.colliderect(health.healthRectangle): #Checks if the player rectangle has collided with the health potion rectangle
        if self.playerHealth < 100: #Checks if the player health is smaller than 100 to check if it can increase the health of the player
          self.playerHealth += 30 #Gives the player 30 hp for when it collided with the health potion
          healthPotionList.remove(health) #Removes that collided health potion from the list which removes it visually
        if self.playerHealth >= 100: #Checks if the player health is equal to or bigger than 100
          self.playerHealth = 100 #Sets back to 100 to allow the player health not exceed 100 (their maxiumum health)

    for speed in speedPotionList: #Iterates through each item within the speed potion list
      if self.playerRectangle.colliderect(speed.speedRectangle): #Checks if the player rectangle has collided with the speed potion rectangle
        speedPotionList.remove(speed) #Removes that collided speed potion from the list which removes it visually
        self.speedBoostEffect = True #Sets the speed state to true to allow the player velocity to double
        self.currentEffect = "Speed" #Updates the text on the screen to allow the player to know what potion is in effect
        self.currentSpeedTime = pygame.time.get_ticks() #Gets the current speed time to allow the speed to run for 10 seconds

    for platform in platformList: #Iterates through each item within the platform list
      if self.playerRectangle.colliderect(platform.platformRectangle): #Checks if the player rectangle has collided with the platform rectangle
        self.onPlatform = True #Sets the attribue to true to update the player new ground level
        self.playerRectangle.y = platform.platformRectangle.top - self.playerRectangle.height #When the player collides with the platform, sets the player y coordinate to the top of the platform
        self.yVelocity = 0 #This will make as if the player is on the main game ground again (same behaviour as when on the platform ground)
        self.jumping = False #Ensures the player cannot jump during the duration of the jump

        if (self.playerRectangle.bottom + self.changeInY) > (platform.platformRectangle.top): #Checks if the player has went below the floor of the platform
          self.yVelocity = 0 #Resets the y velocity back to 0 to ensure same behaviour as when on the ground
          self.changeInY = (platform.platformRectangle.top - self.playerRectangle.bottom) #Ensures the player lands on the floor of the platform
          self.jumping = True #Allows the player to jump again
      else:
        self.onPlatform = False #If it is not true, none of the above occurs

    self.UpdateAnimations() #Ensures after every movement, animatons can be updated

  def Win(self): #Method for checking if the player has won by returning the 'self.win' value for if it has been set to true to load up the win screen interface
    return self.win

  def Lose(self): #Method for checking if the player has lost by returning the 'self.lose' value for if it has been set to true to load up the lose screen interface
    return self.lose

  def Draw(self): #Method for checking if the player has draw by returning the 'self.draw' value for if it has been set to true to load up the draw screen interface
    return self.draw

  def Pause(self): #Method for checking if the player has paused the game by returning the 'self.pause' value for if it has been set to true to load up pause screen interface
    return self.pause

  def SpeedPotionBuyTime(self):
    self.currentSpeedTime = pygame.time.get_ticks() #Gets the current speed time for when the player has bought a speed potion (ensures time of speed lasts for 10 seconds)

  def SpeedPotionTimer(self):
     if self.speedBoostEffect == True: #Checks whether the attribute is set to true to allow further proceedings to take place
        self.currentGameTime = pygame.time.get_ticks() #Gets the current game time
        if self.currentGameTime - self.currentSpeedTime >= self.speedBoostDuration: #Subtratcs the current time from the speed time which gets the duration of the length of the speed potion
           #If it is greater than the duration of 10 seconds, reset the player velocity and text back to normal

            #Player attribute returned back to normal
           self.speedBoostEffect = False
           self.currentEffect = "Nothing..."

  def NaturalRegeneration(self):
    self.currentRegenTime = pygame.time.get_ticks() #Gets the current speed time to allow the natural regeneration wait time to be 60 seconds
    if self.currentRegenTime - self.regenerationLastTime >= self.regenerationTimeInterval: #Subtracts the regeneration time by the regeneration last time attribute to get the actual time of wait
      #If it is greater than 60 seconds, then action below occurs

      self.playerHealth += 10 #Increases the player hp by 10 
      self.regenerationLastTime = self.currentRegenTime #Ensures that the timer resets
      if self.playerHealth >= 100: #Checks if the player health is above 100 or equal to
        self.playerHealth = 100 #This ensures that if the natural regeneration does give the player 10 hp, this increase is not shown

  def Jumping(self):
    self.yVelocity = PLAYERVELOCITYY #Sets the y velocity to become the constant y velocity within the 'Settings.py' file for when 'W' is clicked to make player increase
    self.jumping = False #Makes the player not allowed to jump for the duration of being in the air

    if self.onPlatform == True: #Checks if the player has collided with the platform
          self.yVelocity = -50  #Sets a new y velocity to ensure the player jumps higher on the platform floor
          self.jumping = True #Allows the player to jump once again after the jump

  def GravityEffect(self): 
    if self.onPlatform == True: #Checks if the player has collided with the platform
      self.yVelocity += 0 #Sets the gravity to the floor of the platform
      self.changeInY += self.yVelocity #Ensures the player y coordinate is set to the floor of the ground
    else:
      self.yVelocity += GRAVITY #After the jump, this method sets the y velocity to increase by the gravity constant which makes the player return back to the ground
      self.changeInY += self.yVelocity #Makes the player y velocity increase by the gravity which makes the player move to the ground fast. This is then set to the y value of the player rectangle

  def PlayerLevelChecker(self, expIncrease, Enemy):
    self.exp += expIncrease #Make the player exp increase by the parameter

    while self.exp >= 50: #Check if the player exp is above the 50 exp threshold
        self.playerLevel += 1 #If the player exp is above 50, then let the player level increase by 1
        self.attackDamage += 6 #If the player exp is above 50, then let the player attack damage increase by 6

        if self.playerHealth == 0 and Enemy.enemyHealth == 0:
          self.playerHealth += 0 #If the player exp is above 50, then let the player health increase by 5
        else:
          self.playerHealth += 5

        self.exp -= 50 #If the player exp is above 50, then let the player exp reset back to 0

        if self.playerHealth >= 100: #As the player health increases, must check if it is equal to 100 or more
          self.playerHealth = 100 #If it is, don't increase the player health to be over 100

  def SpriteAnimations(self): #This method handles making the squares onto the spritesheet which is then appended into a 2D array
    self.animationsList = [] #Creates an empty list - this will store the huge list of animations
    y = 0 #Initialises the y iteration to 0
    for animations in self.playerAnimationIndex: #Iterating through each value within the list of indexes
      self.playerList = [] #Creates an empty player list
      for x in range(animations): #Iterates for that index number of times e.g. if self.playerAnimationIndex = [2], iterates twice in the range
        self.playerXSize = x * self.sizeX #Calculates the x position and size of the square on the spritesheet
        self.playerYSize = y * self.sizeY #Calculates the y position and size of the square on the spritesheet
        self.playerImage = self.playerSheet.subsurface(self.playerXSize, self.playerYSize, self.sizeX, self.sizeY) #Extract a square from the player spritesheet
        self.playerScaleUp = pygame.transform.scale(self.playerImage, (self.sizeX * self.playerScale, self.sizeY * self.playerScale)) #This makes the squares bigger to ensure the player looks bigger on screen
        self.playerList.append(self.playerScaleUp) #Adds this scaled square to the second list
      y += 1 #Increase the y value to move to the next index within the list
      self.animationsList.append(self.playerList) #After one index finishes, this is then appended to the larger array to form the 2D array
    return self.animationsList #Return list of all the animations (squares)

  def UpdateAnimations(self): #This method ensures that the correct animation plays
    if self.jumping == False: #Checks if the player is jumping
      if self.currentAction != 7: #Checks if the current action is not the animation it already is
        self.currentAction = 7 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    elif self.playerDeath == True: #Checks if the player has been defeated
      if self.currentAction != 4: #Checks if the current action is not the animation it already is
        self.currentAction = 4 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    elif self.playerTakenDamage == True: #Checks if the player is taking damage
      if self.currentAction != 5: #Checks if the current action is not the animation it already is
        self.currentAction = 5 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    elif self.attackAnimation == True: #Checks if the player is attacking
      if self.currentAction != 1: #Checks if the current action is not the animation it already is
        self.currentAction = 1 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    elif self.running == True: #Checks if the player is running
      if self.currentAction != 8: #Checks if the current action is not the animation it already is
        self.currentAction = 8 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    else: #If the player is not doing any of the animations above, then play idle animation
      if self.currentAction != 0: #Checks if the current action is not the animation it already is
        self.currentAction = 0 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    if self.playerAnimations == True: #Checks if the player animations is set to true. If it is set to false, no animations will play
      self.cooldown = 100 #Sets a cooldown for the animations to allow each frame to play for that length
      self.currentImage = self.animationsList[self.currentAction][self.currentFrame] #After the several if statement above, these will then set the animations to be that list and that index. This will then display that frame onto the screen
      if pygame.time.get_ticks() - self.updateTime > self.cooldown: #Checks if 100 milliseconds is done
        self.currentFrame += 1 #Increases the current action by one - this will make the player see an animation but really it is just the frames scrolling from 0 to the max value very quickly
        self.updateTime = pygame.time.get_ticks() #Ensures the timer resets to allow the frame to increase by 1 again to show the next frame within the animation
      if self.currentFrame >= len(self.animationsList[self.currentAction]): #Checks if the frames has exceeded the length of that index
        self.currentFrame = 0 #Sets frame back to zero to ensure that the frame can recycle
        self.UpdateCooldowns() #This method updates all the cooldowns for when the length of the current action has been exceeded

  def UpdateCooldowns(self):
    if self.currentAction == 1: #Checks if the animation is the attack animation
      self.attackCooldownAnimation = 5 #Ensures that the animation cooldown lasts for a few seconds before stopping
      self.attack = False #Ensures the player attack stops

    if self.currentAction == 5: #Checks if the animation is the player taken damage animation
      self.damageCooldown = 4 #Sets the cooldown which ensures the animation plays then stops
      self.playerTakenDamage = False #Ensures that the player does not take damage anymore

    if self.currentAction == 4: #Checks if the animation is the player death animation
      self.deathCooldown = 3 #Sets the cooldown which ensures the animation plays then stops

  def DrawPlayer(self, window): #This method ensures that the player rectangle and image is drawn onto the screen
    self.newImage = pygame.transform.flip(self.currentImage, self.flipH, False) #This ensures that the player is flipped for when 'self.flipH' sets to true
    #pygame.draw.rect(window, GREEN, self.playerRectangle) #This draws the player rectangle on the screen
    window.blit(self.newImage, (self.playerRectangle.x - (self.playerShiftX * self.playerScale),self.playerRectangle.y - (self.playerShiftY * self.playerScale))) #This draws the player image onto the screen. This offsets the player in the x and y direction depending on the enlargement of the player x and y

class Enemy: #This is the template which holds the entire enemy functionality of the game
  def __init__(self, x, y, enemySizes, enemyScale, enemyShift, imagePath, velocity, attackDamage): #Constructior which takes in the constants within the 'Settings.py' of: ENEMYSIZES (constant list), ENEMYSCALE (constant value), ENEMYSHIFT (constant list)
    #The enemy attack damage is an integer value which determines amount of damage the player takes

    #Enemy properties:
    self.x = x #This sets the starting x value of the enemy
    self.y = y #This sets the starting y value of the enemy

    self.enemyHealth = 100 #This is the starting health value of the player

    self.enemyVelocity = velocity #This determines how fast the enemy will be moving

    self.imagePath = imagePath #This sets the enemy path to an attribute which then can be used as an image for a sprite sheet

    self.playerTrack = True #Ensures that the enemy always tracks the player movement
    self.flipH = False #Default facing is right so when this is set to true, flips player to the left

    self.attackDamage = attackDamage #This is the attribute that will ensure the player loses hp by this amount
    self.attacking = True #Ensures the enemy cannot atack the player for when this value is set to false

    self.enemyAnimations = True #Ensures enemy animations play but when they are defeated, this will stop all animations when set to false
    self.enemyMovement = False #Used to play the enemy running animation
    self.enemyDeath = False #Used to play the player death animation
    self.enemyTakenDamage = False #Used to play the player taken damage animation

    self.attackTrigger = False #This creates the enemy attack box for when this value sets to true

    self.enemySheet = pygame.image.load(os.path.join((self.imagePath))).convert_alpha() #This is the enemy sprite sheet
    self.enemyAnimationIndex = [7, 7, 12, 12, 16, 4, 8] #These are the index values for the enemy animations

    self.sizeX = enemySizes[0] #This is the x horizontal size of the square that is to be used to create a square
    self.sizeY = enemySizes[1] #This is the y vertical size of the square that is to be used to create a square
    self.enemyScale = enemyScale #This will enlargement the enemy image squares
    self.enemyShiftX = enemyShift[0] #This will offset the enemy by a set amount in the x direction to ensure the enemy images is inline with the enemy rectangle
    self.enemyShiftY = enemyShift[1] #This will offset the enemy by a set amount in the y direction to ensure the enemy images is inline with the enemy rectangle

    self.animationsList = self.SpriteAnimations() #This holds the entire 2D array of the list of player animations
    self.currentAction = 0 #This sets to one of the list within the 2D array to play that entire animation
    #self.currentAction = 0: Idle animation
    #self.currentAction = 1: Run animation
    #self.currentAction = 2: Attack 1 animation
    #self.currentAction = 3: Attack 2 animation
    #self.currentAction = 4: Attack 3 animation
    #self.currentAction = 5: Taken damage animation
    #self.currentAction = 6: Death animation

    self.currentFrame = 0 #This will go through each square within the 'self.animationsList' list mapped by the 'self.currentAction' attribute to show the animation on screen
    self.currentImage = self.animationsList[self.currentAction][self.currentFrame] #Maps the 'self.currentAction' to a list and 'self.currentFrame' to the items within the list to show the current image on screen

    #Cooldowns for the animations
    self.attackCooldown = 0 #Ensures the enemy attack once per every few seconds
    self.damageCooldown = 0 
    self.movementCooldown = 0 #Ensures the enemy stops moving temporarily when cooldown above 0
    self.deathCooldown = 0

    self.updateTime = pygame.time.get_ticks() #Current game time for animation

    self.enemyRectangle = pygame.Rect((x, y, ENEMYWIDTH, ENEMYHEIGHT)) #This creates a rectangle with the enemy x, y, width and height

  def Movements(self, window, Player): #This method is used to control the enemy movements, collisions
    #Parameters ensures enemy can interact with these items

    if self.playerTrack == True: #Value set to true which ensures that the below code will run - this for the enemy tracking the player
      if Player.playerRectangle.centerx > self.enemyRectangle.centerx: #Checks if the player is on the right side of the enemy
        self.enemyRectangle.x += self.enemyVelocity #Increases the enemy x position by the enemy x velocity to ensure the enemy moves towards the player to the right
        self.flipH = False #Enemy facing right therefore flip not needed
        self.enemyMovement = True #Ensures the enemy movement animation plays
        self.EnemyAttack(window, Player) #This ensures that the enemy will be able to attack the player when it comes close to the player

      else: #If the player is on the left side of the enemy
        self.enemyRectangle.x -= self.enemyVelocity #Decreases the enemy x position by the enemy x velocity to ensure the enemy moves towards the player to the left
        self.flipH = True #Enemy facing left therefore flip is needed
        self.enemyMovement = True #Ensures the enemy movement animation plays
        self.EnemyAttack(window, Player) #This ensures that the enemy will be able to attack the player when it comes close to the player

    if self.attackCooldown > 0: #Checks if the attack cooldown is greater than 0
      self.attackCooldown -= 1 #Subtracts 1 until it is smaller than 0 to allow player to attack again
      if self.attackCooldown == 0: #If it is set to 0 at one point during the subraction
        self.playerTrack = True #Allow the enemy to be able to follow the player again - after enemy has attacked, cooldown ensures enemy stops moving for a brief second before following the player again

    if self.movementCooldown > 0: #Checks if the movement cooldown is greater than 0
        self.movementCooldown -= 1 #Subtracts 1 until it is smaller than 0 to allow player to move again
        if self.movementCooldown == 0: #If it is set to 0 at one point during the subraction
            self.playerTrack = True #Allow the enemy to be able to follow the player again - after enemy has attacked, cooldown ensures enemy stops moving for a brief second before following the player again

    if self.damageCooldown > 0: #Checks if the enemy damage cooldown animation is greater than 0
        self.damageCooldown -= 1 #Subtracts 1 until it is smaller than 0
        if self.damageCooldown == 0: #If it is set to 0 at one point during the subraction
            self.enemyTakenDamage = False #Then let the attribute turn false to allow enemy damage animation to stop running

    if self.deathCooldown > 0: #Checks if the player death cooldown animation is greater than 0
      self.deathCooldown -= 1 #Subtracts 1 until it is smaller than 0
      if self.deathCooldown == 0: #If it is set to 0 at one point during the subraction
        self.enemyAnimations = False #Then let the attribute turn false to allow enemy death animation to stop running
        self.currentAction = 6 #This sets to the 7th list within the 2D array which is the death list
        self.currentFrame = 6 #Chooses the last frame within the list to halt to a pause
        self.currentImage = self.animationsList[self.currentAction][self.currentFrame] #Sets this image to the current image to display on screen

    if self.enemyHealth == 0: #Checks if the player health has become 0
      self.playerTrack = False #Make the enemy stop tracking the player
      self.attack = False #Ensures the enemy does not attack
      self.enemyDeath = True #Play the death animation
      Player.disableMovement = True #Ensure that the player cannot do any key inputs to move the player
      Player.win = True #Ensures the player win screen pops up
      Player.returnMain = True #This allows the 'Return To Main Menu' button to be active within the level 3 win screen

    self.UpdateAnimations() #Ensures after every movement, animatons can be updated

  def EnemyAttack(self, window, Player):
    if self.attacking == True: #Allows the enemy to attack as when this sets to false, enemy cannot attack
        if self.attackCooldown == 0: #Checks whether the attack cooldown is 0 to ensure the enemy can attack. If not 0, enemy cannot attack and the player won't lose health

            #This creates an attack rectangle that sticks out from the enemy rectangle which is the attack of the enemy. This is a proportion of the original rectangle
            self.attackBox = pygame.Rect(self.enemyRectangle.centerx - (self.enemyRectangle.width * self.flipH), self.enemyRectangle.y,self.enemyRectangle.width, self.enemyRectangle.height)
            if self.attackBox.colliderect(Player.playerRectangle): #Checks if the 'attackBox' has collided with the body of the player
                self.attackTrigger = True #Allows the attack box rectangle to be shown on the screen
                self.playerTrack = False #Makes the player not track the player for a brief moment
                self.attack = True #Indicates that the enemy is attacking the player
                Player.playerHealth -= self.attackDamage #Makes the player hp reduced by the attack damage of the enemy
                Player.playerTakenDamage = True #Plays the player damage animation
                self.attackCooldown = 100 #Sets the attack cooldown for if the enemy has collide its attack with the player
            else:
                self.attackTrigger = False #If the enemy attack box has not collided, this attack box will not appear

            #if self.attackTrigger == True: #If the attribute is set to true
                # pygame.draw.rect(window, YELLOW, self.attackBox) #This will draw the enemy attack box onto the screen

        if Player.playerHealth <= 0: #Checks whether the player health is below or equal to 0
            Player.playerHealth = 0 #Sets it to 0 to ensure enemy does not have negative health
            Player.playerLoss = True #This allows the timers within 'Main.py' to be able to be subtracted from each other and checked if it is greater or equal to 3 seconds
            self.loseTimer = pygame.time.get_ticks() #Gets the time at which the player has been defeated

  def SpriteAnimations(self): #This method handles making the squares onto the spritesheet which is then appended into a 2D array
    self.animationsList = [] #Creates an empty list - this will store the huge list of animations
    y = 0 #Initialises the y iteration to 0
    for animations in self.enemyAnimationIndex: #Iterating through each value within the list of indexes
      self.enemyList = [] #Creates an empty enemy list
      for x in range(animations): #Iterates for that index number of times e.g. if self.enemyAnimationIndex = [2], iterates twice in the range
        self.enemyXSize = x * self.sizeX #Calculates the x position and size of the square on the spritesheet
        self.enemyYSize = y * self.sizeY #Calculates the y position and size of the square on the spritesheet
        self.enemyImage = self.enemySheet.subsurface(self.enemyXSize,self.enemyYSize,self.sizeX, self.sizeY) #Extract a square from the enemy spritesheet
        self.enemyScaleUp = pygame.transform.scale(self.enemyImage,(self.sizeX * self.enemyScale, self.sizeY * self.enemyScale)) #This makes the squares bigger to ensure the enemy looks bigger on screen
        self.enemyList.append(self.enemyScaleUp) #Adds this scaled square to the second list
      y += 1 #Increase the y value to move to the next index within the lis
      self.animationsList.append(self.enemyList) #After one index finishes, this is then appended to the larger array to form the 2D array
    return self.animationsList #Return list of all the animations (squares)

  def UpdateAnimations(self): #This method ensures that the correct animation plays
    if self.enemyDeath == True: #Checks if the enemy has been defeated
      if self.currentAction != 6: #Checks if the current action is not the animation it already is
        self.currentAction = 6 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    elif self.enemyTakenDamage == True: #Checks if the enemy is taking damage
      if self.currentAction != 5: #Checks if the current action is not the animation it already is
        self.currentAction = 5 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    elif self.attackTrigger == True: #Checks if the enemy is attacking
      if self.currentAction != 2: #Checks if the current action is not the animation it already is
        self.currentAction = 2 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    elif self.enemyMovement == True: #Checks if the enemy is running
      if self.currentAction != 1: #Checks if the current action is not the animation it already is
        self.currentAction = 1 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    else: #If the enemy is not doing any of the animations above, then play idle animation
      if self.currentAction != 0: #Checks if the current action is not the animation it already is
        self.currentAction = 0 #Sets the current action to be that animation
        self.currentFrame = 0 #Plays from the start of the animation
        self.updateTime = pygame.time.get_ticks() #Gets the duration of the animation

    if self.enemyAnimations == True: #Checks if the enemy animations is set to true. If it is set to false, no animations will play
      self.cooldown = 100 #Sets a cooldown for the animations to allow each frame to play for that length
      self.currentImage = self.animationsList[self.currentAction][self.currentFrame] #After the several if statement above, these will then set the animations to be that list and that index. This will then display that frame onto the screen
      if pygame.time.get_ticks() - self.updateTime > self.cooldown: #Checks if 100 milliseconds is done
        self.currentFrame += 1 #Increases the current action by one - this will make the player see an animation but really it is just the frames scrolling from 0 to the max value very quickly
        self.updateTime = pygame.time.get_ticks() #Ensures the timer resets to allow the frame to increase by 1 again to show the next frame within the animation
      if self.currentFrame >= len(self.animationsList[self.currentAction]): #Checks if the frames has exceeded the length of that index
        self.currentFrame = 0 #Sets frame back to zero to ensure that the frame can recycle
        self.UpdateCooldowns() #This method updates all the cooldowns for when the length of the current action has been exceed

  def UpdateCooldowns(self):
    if self.currentAction == 1: #Checks if the animation is the moving animation
      self.movementCooldown = 10 #Ensures that the animation cooldown lasts for a few seconds before stopping

    if self.currentAction == 5: #Checks if the animation is the enemy taken damage animation
      self.damageCooldown = 6 #Sets the cooldown which ensures the animation plays then stops

    if self.currentAction == 6: #Checks if the animation is the enemy death animation
      self.deathCooldown = 7 #Sets the cooldown which ensures the animation plays then stops

  def DrawEnemy(self, window): #This method ensures that the enemy rectangle and image is drawn onto the screen
    self.newImage = pygame.transform.flip(self.currentImage, self.flipH, False) #This ensures that the enemy is flipped for when 'self.flipH' sets to true
    #pygame.draw.rect(window, BLUE, self.enemyRectangle) #This draws the enemy rectangle on the screen
    window.blit(self.newImage, (self.enemyRectangle.x - (self.enemyShiftX * self.enemyScale),self.enemyRectangle.y - (self.enemyShiftY * self.enemyScale))) #This draws the enemy image onto the screen. This offsets the enemy in the x and y direction depending on the enlargement of the enemy x and y

class Coin: #This is the template which holds the entire coin functionality of the game
    def __init__(self, x, y, coinShift): #Constructior which takes in the constants within the 'Settings.py' of: COINSHIFT (constant list)

        #Coin properties:
        self.x = x #This sets the starting x value of the coin
        self.y = y #This sets the starting y value of the coin

        self.coinShiftX = coinShift[0] #This will offset the coin by a set amount in the x direction to ensure the coin image is inline with the coin rectangle
        self.coinShiftY = coinShift[1] #This will offset the coin by a set amount in the y direction to ensure the coin images is inline with the coin rectangle

        self.coinImage = pygame.image.load(os.path.join('Other','SingleCoin2.png')).convert_alpha() #This is the coin image
        self.coinRectangle = pygame.Rect((self.x, self.y, COINWIDTH, COINHEIGHT)) #This creates a rectangle with the coin x, y, width and height

    def DrawCoin(self, window): #This method ensures that the coin rectangle and image is drawn onto the screen
      # pygame.draw.rect(window, YELLOW, self.coinRectangle) #This draws the coin rectangle on the screen
      window.blit(self.coinImage, (self.coinRectangle.x - (self.coinShiftX),self.coinRectangle.y - (self.coinShiftY))) #This draws the coin image onto the screen. This offsets the coin in the x and y direction

class Potion: #This is the super class which holds the entire potion functionality of the game
    def __init__(self, x, y, potionShift, imagePath): #Constructior which takes in the constants within the 'Settings.py' of: POTIONSHIFT (constant list)

        #Potion properties:
        self.x = x #This sets the starting x value of the potion
        self.y = y #This sets the starting y value of the potion

        self.imagePath = imagePath #This sets the potion path to an attribute which then can be used as an image to create multiple potions

        self.potionShiftX = potionShift[0] #This will offset the potion by a set amount in the x direction to ensure the potion image is inline with the potion rectangle
        self.potionShiftY = potionShift[1] #This will offset the potion by a set amount in the y direction to ensure the potion images is inline with the potion rectangle

        self.potionImage = pygame.image.load(self.imagePath).convert_alpha() #This will set the potion image
        self.potionRectangle = pygame.Rect((x, y, POTIONWIDTH, POTIONHEIGHT)) #This creates a rectangle with the potion x, y, width and height

    def DrawPotion(self, window): #This method ensures that the potion rectangle and image is drawn onto the screen
        # pygame.draw.rect(window, DARKBLUE, self.potionRectangle) #This draws the potion rectangle on the screen
        window.blit(self.potionImage, (self.potionRectangle.x - (self.potionShiftX), self.potionRectangle.y - (self.potionShiftY))) #This draws the potion image onto the screen. This offsets the potion in the x and y direction

class InstantHealth(Potion): #This is the sub class which inherits from the Potion class
   def __init__(self, x, y):

    #Health potion properties:
    self.x = x #This sets the starting x value of the potion
    self.y = y #This sets the starting y value of the potion

    self.imagePath = os.path.join('Other','Health2.png') #This sets the path of the image to be the health potion image

    self.healthRectangle = pygame.Rect((x, y, POTIONWIDTH, POTIONHEIGHT)) #This creates a rectangle with the health potion x, y, width and height

    super().__init__(x, y, POTIONSHIFT, self.imagePath) #This inherits all of the x, y, potion shifts and image path from the Potion class

   def DrawPotion(self, window): #This method ensures that the instant potion rectangle and image is drawn onto the screen
     # pygame.draw.rect(window, RED, self.potionRectangle) #This draws the instant health potion rectangle on the screen
     window.blit(self.potionImage, (self.healthRectangle.x - (self.potionShiftX), self.healthRectangle.y - (self.potionShiftY))) #This draws the instant health potion image onto the screen. This offsets the instant health potion in the x and y direction 

class Speed(Potion): #This is the sub class which inherits from the Potion class
   def __init__(self, x, y):

    #Speed Potion properties:
    self.x = x #This sets the starting x value of the potion
    self.y = y #This sets the starting y value of the potion

    self.imagePath = os.path.join('Other','Speed2.png') #This sets the path of the image to be the speed potion image

    self.speedRectangle = pygame.Rect((x, y, POTIONWIDTH, POTIONHEIGHT)) #This creates a rectangle with the speed potion x, y, width and height

    super().__init__(x, y, POTIONSHIFT, self.imagePath) #This inherits all of the x, y, potion shifts and image path from the Potion class

    self.potionShiftY = 70 #This overwrites the shift y value of the potion class

   def DrawPotion(self, window): #This method ensures that the speed potion rectangle and image is drawn onto the screen
     # pygame.draw.rect(window, BLUE, self.potionRectangle) #This draws the speed potion rectangle on the screen
     window.blit(self.potionImage, (self.speedRectangle.x - (self.potionShiftX), self.speedRectangle.y - (self.potionShiftY))) #This draws the speed potion image onto the screen. This offsets the speed potion in the x and y direction

class Platform:
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

    self.platformRectangle = pygame.Rect((x, y, self.width, self.height))

  def DrawPlatform(self, window):
    pygame.draw.rect(window, LIGHTORANGE, self.platformRectangle)