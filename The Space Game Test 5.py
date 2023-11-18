import pygame
import math
import copy
import random
from pygame.locals import *

class Tower:
    position = None
    hp = None
    size = None
    cost = None
    color = None
    buildTime = None
    buildState = None
    connectionRange = 75
    connections = []
    maxConnections = None
    connectionAtCapacity = False
    energyConsumption = None
    energySatisfaction = 0
    operational = False
    level = 1

    def _checkCollision(self):

        allTowers = allOpenTowers + allClosedTowers + allOpenNodes + allClosedNodes + allOpenAsteroids + allClosedAsteroids

        for tower in allTowers:
            if((self.size + tower.size) >= calcDistance(self.position, tower.position)):
                return True
        return False

    def checkPress(self):

        if((self.size + tower.size) <= calcDistance(self.position, tower.position)):
            currentHUD = "TOWER"
            selectedTower = self

    def checkCapacity(self):

        oldCapacity = self.connectionAtCapacity

        self.connectionAtCapacity = len(self.connections) == self.maxConnections

        if(oldCapacity == False and self.connectionAtCapacity == True): # now at capacity, swap arrays
            allOpenTowers.remove(self)
            allClosedTowers.append(self)
        elif(oldCapacity == True and self.connectionAtCapacity == False): # now not at capacity, swap arrays
            allClosedTowers.remove(self)
            allOpenTowers.append(self)

    def findNearestOpenTowers(self):

        nodes = []

        for node in allOpenNodes:

            tempDistance = calcDistance(self.position, node.position)
            
            if(tempDistance <= self.connectionRange):
                nodes.append((tempDistance,node))

        sortedNodes = sorted(nodes, key=lambda x: x[0])

        result = []

        for node in sortedNodes[:self.maxConnections]:

            result.append(node[1])

        return result
        
    def place(self):

        newCopy = copy.copy(self)
        newCopy.connections = newCopy.findNearestOpenTowers()

        for tower in newCopy.connections:
            tower.connections.append(newCopy)
            tower.checkCapacity()
        
        if(len(newCopy.connections) == newCopy.maxConnections):
            allClosedTowers.append(newCopy)
        else:
            allOpenTowers.append(newCopy)

    def drawTower(self):
        pygame.draw.circle(SCREEN, self.color, tupleSubtraction(self.position, camera), self.size, 0)

    def drawConnections(self):
        for connection in self.connections:
            pygame.draw.line(SCREEN, RELAY_BLUE, tupleSubtraction(self.position, camera), tupleSubtraction(connection.position,camera),2)

    def drawGhost(self):
        global collision
        pygame.draw.circle(SCREEN, ENERGY_CONNECTION_GREEN, tupleSubtraction(self.position, camera), self.connectionRange, 1) ## ENERGY CONNECTION RANGE
        if(self._checkCollision() == True):
            collision = True
            pygame.draw.circle(SCREEN, ERROR_RED, tupleSubtraction(self.position, camera), self.size, 0)
        else:
            collision = False
            pygame.draw.circle(SCREEN, HIGHLIGHT_GREEN, tupleSubtraction(self.position, camera), self.size, 0)

class EnergyNode(Tower):

    def __init__(self, position):
        self.position = position
        self.hp = 35
        self.size = 4
        self.cost = 25
        self.color = NODE_BLUE
        self.buildTime = 5
        self.buildState = 0
        self.maxConnections = 6
        self.energyConsumption = 0
        self.energySatisfaction = 0

    def findNearestOpenTowers(self):

        closestTowers = []

        towersToCheck = allOpenTowers + allOpenNodes

        for tower in towersToCheck:
            
            tempDistance = calcDistance(self.position, tower.position)
            
            if(tempDistance <= self.connectionRange):
                closestTowers.append((tempDistance,tower))

        sortedClosestTowers = sorted(closestTowers, key=lambda x: x[0])

        result = []

        for tower in closestTowers[:self.maxConnections]:

            result.append(tower[1])

        return result

    def place(self):

        newCopy = copy.copy(self)
        newCopy.connections = newCopy.findNearestOpenTowers()

        for tower in newCopy.connections:
            tower.connections.append(newCopy)
            tower.checkCapacity()
            
        if(len(newCopy.connections) == newCopy.maxConnections):
            allClosedNodes.append(newCopy)
        else:
            allOpenNodes.append(newCopy)

    def checkCapacity(self):

        oldCapacity = self.connectionAtCapacity

        self.connectionAtCapacity = len(self.connections) == self.maxConnections

        if(oldCapacity == False and self.connectionAtCapacity == True): # now at capacity, swap arrays
            allOpenNodes.remove(self)
            allClosedNodes.append(self)
        elif(oldCapacity == True and self.connectionAtCapacity == False): # now not at capacity, swap arrays
            allOpenNodes.remove(self)
            allClosedNodes.append(self)

        if(self.connectionAtCapacity == True):
            self.color = NODE_RED
        else:
            self.color = NODE_BLUE


class WeaponTower(Tower):

    damage = None
    weaponRange = None
    target = None
    maxConnections = 1

    def drawGhost(self):
        super().drawGhost()
        pygame.draw.circle(SCREEN, BLACK, tupleSubtraction(self.position, camera), self.weaponRange, 1)

class LogisticTower(Tower):

    maxConnections = 1

##

class BasicLaserTower(WeaponTower):

    def __init__(self, position):
        self.position = position
        self.hp = 150
        self.size = 10
        self.cost = 100
        self.color = BLACK
        self.buildTime = 15
        self.buildState = 0
        self.energyConsumption = 1

        self.damage = 5
        self.weaponRange = 75
        self.target = None

class MissileTower(WeaponTower):

    def __init__(self, position):
        self.position = position
        self.weaponRange = 250
        self.hp = 150
        self.size = 9
        self.cost = 250
        self.color = GRAY
        self.buildTime = 15
        self.buildState = 0
        self.energyConsumption = 3

        self.cooldown = 0
        self.maxCooldown = 50
        self.missileAmount = 1

class MineralMiner(LogisticTower):

    def __init__(self, position):
        
        self.position = position
        self.hp = 45
        self.size = 5
        self.cost = 40
        self.color = MINERAL_MINER_GREEN
        self.buildTime = 7
        self.buildState = 0
        self.energyConsumption = 3
        
        self.asteroidRange = 35
        self.targetAsteroid = None
        self.asteroidQueue = []
        self.MineralProductionRate = 0

    def drawGhost(self):
        super().drawGhost()
        pygame.draw.circle(SCREEN, BLACK, tupleSubtraction(self.position, camera), self.asteroidRange, 1)
        nearbyAsteroids = self.checkNearbyAsteroids()
        for asteroid in nearbyAsteroids:
            pygame.draw.line(SCREEN, HIGHLIGHT_GREEN, tupleSubtraction(self.position, camera), tupleSubtraction(asteroid.position, camera), 2)
        
    def checkNearbyAsteroids(self):

        nearbyAsteroids = []

        for asteroid in allOpenAsteroids:
            if(calcDistance(self.position, asteroid.position) <= self.asteroidRange + asteroid.size):
                nearbyAsteroids.append(asteroid)

        return nearbyAsteroids
        

class SolarStation(LogisticTower):

        def __init__(self, position):
        
            self.position = position
            self.hp = 200
            self.size = 12
            self.cost = 200
            self.color = BLACK
            self.buildTime = 15
            self.buildState = 0
            self.energyConsumption = 0
            self.maxConnections = 25
            
##
## Asteroid Classes
##

class Asteroid:

    def __init__(self, position):
        self.seed = random.randint(10, 30)
        self.totalMinerals = self.seed * 5 * (self.seed/2)
        self.remainingMinerals = self.totalMinerals
        self.empty = False
        self.size = self.seed
        self.position = position

    def drawAsteroid(self):
        tempGreen = ASTEROID_FULL_GREEN
        pygame.draw.circle(SCREEN, ASTEROID_EMPTY_BROWN, tupleSubtraction(self.position, camera), self.size, 0)
        pygame.draw.circle(SCREEN, ASTEROID_FULL_GREEN, tupleSubtraction(self.position, camera), self.size, 0)
        pygame.draw.circle(SCREEN, ASTEROID_EMPTY_BROWN, tupleSubtraction(self.position, camera), self.size, 2)

    

##

class TowerButton:

    def __init__(self, position, tower, text):
        self.size = 20
        self.font = pygame.font.Font(None, self.size)
        self.textRender = self.font.render(text, True, BLACK)
        self.position = position
        self.tower = tower
        self.rectangle = pygame.Rect(100+self.position*85, WINDOW_HEIGHT-95, 80, 100)
        self.color = HIGHLIGHT_GREEN
        self.outline = DARK_HIGHLIGHT_GREEN
        self.available = False

    def drawButton(self):

        SCREEN.blit(self.textRender, pygame.draw.rect(SCREEN, self.color, self.rectangle))
        pygame.draw.rect(SCREEN, self.outline, self.rectangle,2)
        

    def checkPrice(self):

        if(minerals >= self.tower.cost):
            self.color = HIGHLIGHT_GREEN
            self.outline = DARK_HIGHLIGHT_GREEN
            self.available = True
        else:
            self.color = GRAY
            self.outline = BLACK
            self.available = False

    def checkPress(self, position):
        if(self.rectangle.collidepoint(position) and self.available == True):
           return True
        return False

## Functions

def calcDistance(position1, position2):
    distance = math.sqrt((position2[0] - position1[0])**2 + (position2[1] - position1[1])**2)
    return distance

def handleGhost(position):
    adjustedPosition = tupleAddition(mouseCoords, camera)
    
    towerObjectBeingPlaced.position = adjustedPosition
    towerConnections = towerObjectBeingPlaced.findNearestOpenTowers()
    for connection in towerConnections:
        pygame.draw.line(SCREEN, GHOST_BLUE, tupleSubtraction(towerObjectBeingPlaced.position, camera), tupleSubtraction(connection.position, camera), 2)
    towerObjectBeingPlaced.drawGhost()
        
def tupleSubtraction(tuple1, tuple2):
    return (tuple1[0] - tuple2[0], tuple1[1] - tuple2[1])

def tupleAddition(tuple1, tuple2):
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])


## Generation

def generateAsteroidField():
    global allOpenAsteroids

    generation = random.randint(30,50)

    for i in range(generation):
        randomX = random.randint(-500,1000)
        randomY = random.randint(-500,1000)
        newAsteroid = Asteroid((randomX, randomY))
        allOpenAsteroids.append(newAsteroid)

## draw functions

def drawButtons():
    for button in allButtons:
        button.checkPrice()
        button.drawButton()

def drawTowers():
    towers = allOpenTowers + allClosedTowers + allOpenNodes + allClosedNodes
    for tower in towers:
        tower.drawConnections()
    for tower in towers:
        tower.drawTower()

def drawAsteroids():
    asteroids = allOpenAsteroids + allClosedAsteroids
    for asteroid in asteroids:
        asteroid.drawAsteroid()
        
def checkTowerButtonPress(position):
    global towerBeingPlaced
    global towerObjectBeingPlaced
    for button in allButtons:
        if(button.checkPress(position) == True):
            towerBeingPlaced = True
            towerObjectBeingPlaced = button.tower
            break
            
            


pygame.init()

# CONSTANTS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
GRAY = (100,100,100)
NODE_BLUE = (56, 189, 239)
NODE_RED = (235,50,50)
GHOST_BLUE = (63, 82, 214)
RELAY_BLUE = (17, 160, 215)
HIGHLIGHT_GREEN = (50,200,50)
DARK_HIGHLIGHT_GREEN = (0,75,0)
ERROR_RED = (200,50,50)
ENERGY_CONNECTION_GREEN = (18,80,18)
MINERAL_MINER_GREEN = (0,106,9)

ASTEROID_EMPTY_BROWN = (102,72,4)
ASTEROID_FULL_GREEN = (31,131,5)

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Space Game")

BLASER_BUTTON = TowerButton(1,BasicLaserTower(None),"BLaser")
MISSILE_LAUNCHER_BUTTON = TowerButton(2,MissileTower(None),"MLauncher")
ENERGY_NODE_BUTTON = TowerButton(3,EnergyNode(None),"ENode")
MINERAL_MINER_BUTTON = TowerButton(4,MineralMiner(None),"MMiner")
SOLAR_STATION_BUTTON = TowerButton(5,SolarStation(None),"SStation")

allButtons = [BLASER_BUTTON, MISSILE_LAUNCHER_BUTTON, ENERGY_NODE_BUTTON, MINERAL_MINER_BUTTON, SOLAR_STATION_BUTTON]

# VARIABLES

running = True
minerals = 5000

camera = (0,0)
oldMouse = (0,0)
dragVelocity = [0,0]
dragging = False

allOpenTowers = []
allClosedTowers = []
allOpenNodes = []
allClosedNodes = []

allOpenAsteroids = []
allClosedAsteroids = []

currentHUD = "MAIN"
selectedTower = None
towerBeingPlaced = False
towerObjectBeingPlaced = None
collision = False

SCREEN.fill(WHITE)

generateAsteroidField()
allOpenTowers.append(SolarStation((WINDOW_WIDTH/2,WINDOW_HEIGHT/2)))

while running:
    
    mouseCoords = pygame.mouse.get_pos()

    SCREEN.fill(WHITE)

    drawAsteroids()

    if(dragging == True):
        drag_offset = (mouseCoords[0] - oldMouse[0], mouseCoords[1] - oldMouse[1])
        dragVelocity[0] += drag_offset[0]
        dragVelocity[1] += drag_offset[1]
        camera = (int(dragVelocity[0]/2), int(dragVelocity[1]/2))
        oldMouse = mouseCoords
        
    drawTowers()
        
    if(towerBeingPlaced == True):
        handleGhost(mouseCoords)
        
    drawButtons()
    
    for event in pygame.event.get():
        
        if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if(towerBeingPlaced == False):
                checkTowerButtonPress(mouseCoords)
                if(towerBeingPlaced == False):
                    dragging = True
                    oldMouse = mouseCoords
            else:
                if(collision == False):
                    towerObjectBeingPlaced.place()
                    if(pygame.key.get_pressed()[pygame.K_LSHIFT] != True):
                        towerBeingPlaced = False
                        towerObjectBeingPlaced = None

        elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
            if(towerBeingPlaced == True):
                towerBeingPlaced = False
                towerObjectBeingPlaced = None
                
        elif (event.type == pygame.QUIT):
            running = False

        elif(event.type == pygame.MOUSEBUTTONUP and event.button == 1):
            if(dragging == True):
                dragging = False
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_x):
                camera = (0,0)
                dragVelocity = [0,0]
    
    pygame.display.flip()

pygame.quit()
