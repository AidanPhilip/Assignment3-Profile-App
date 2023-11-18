import pygame
import math
import copy

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

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Space Game")

STANDARD_CONNECTION_RANGE = 75

# VARIABLES

running = True
minerals = 100

# CLASSES

def calcDistance(position1, position2):
    distance = math.sqrt((position2[0] - position1[0])**2 + (position2[1] - position1[1])**2)
    return distance

class Tower:

    def __init__(self, name, typ, position, size, hp, rang, maxConnections):
        self.towerName = name
        self.towerType = typ
        self.towerPosition = position
        self.towerSize = size
        self.towerHp = hp
        self.towerRange = rang
        self.towerMaxConnections = maxConnections
        self.towerConnectionRange = STANDARD_CONNECTION_RANGE
        self.towerNodeConnections = []

    def _checkCollision(self):

        towersToCheck = allOpenTowers + allClosedTowers
        nodesToCheck = allOpenNodes + allClosedNodes

        for tower in towersToCheck:

            if (calcDistance(tower.towerPosition, self.towerPosition) <= tower.towerSize + self.towerSize):
                return True

        for node in nodesToCheck:

            if (calcDistance(node.nodePosition, self.towerPosition) <= node.nodeSize + self.towerSize):
                return True

        return False

    def checkPress(self):
        
    def drawTower(self):
        pygame.draw.circle(SCREEN, BLACK, self.towerPosition, self.towerSize, 0)

    def drawRange(self):

        if(self._checkCollision()): #colliding with object
            pygame.draw.circle(SCREEN, ERROR_RED, self.towerPosition, self.towerSize, 0)
        else:
            pygame.draw.circle(SCREEN, HIGHLIGHT_GREEN, self.towerPosition, self.towerSize, 0)
        pygame.draw.circle(SCREEN, BLACK, self.towerPosition, self.towerRange, 1)



class Node:

    def __init__(self, position):

        self.nodePosition = position
        self.nodeSize = 4
        self.nodeRange = 100
        self.nodeHp = 50
        self.nodeConnections = []
        self.nodeMaxConnections = 6
        self.nodeColor = NODE_BLUE
        self.nodeAtCapacity = False

    def findNearestOpenNodes(self):

        sortedNodes = []
        returnNodes = []

        for node in allOpenNodes:

            tempDistance = calcDistance(node.nodePosition, self.nodePosition)
            if(tempDistance <= self.nodeRange):
                sortedNodes.append((tempDistance,node))

        sortedNodes = sorted(sortedNodes, key=lambda x: x[0])

        lessThanSix = 0
        for distance, node in sortedNodes:
            lessThanSix += 1
            returnNodes.append(node)
            if(lessThanSix >= 6):
                break
            
        return returnNodes

    def checkCapacity(self):
        if(self.nodeAtCapacity == False and len(self.nodeConnections) == self.nodeMaxConnections):
            self.nodeAtCapacity == True
            self.nodeColor = NODE_RED
            allClosedNodes.append(self)
            allOpenNodes.remove(self)
        elif(self.nodeAtCapacity == True and len(self.nodeConnections) < self.nodeMaxConnections):
            self.nodeAtCapacity == False
            self.nodeColor = NODE_BLUE
            allOpenNodes.append(self)
            allClosedNodes.remove(self)

    def _checkCollision(self):

        towersToCheck = allOpenTowers + allClosedTowers
        nodesToCheck = allOpenNodes + allClosedNodes

        for tower in towersToCheck:

            if (calcDistance(tower.towerPosition, self.nodePosition) <= tower.towerSize + self.nodeSize):
                return True

        for node in nodesToCheck:

            if (calcDistance(node.nodePosition, self.nodePosition) <= node.nodeSize + self.nodeSize):
                return True
            
        return False

    def checkPress(self, mousePos):
        if (calcDistance(tower.towerPosition, self.nodePosition) <= tower.towerSize + self.nodeSize):
            
    
    def drawNode(self):
        pygame.draw.circle(SCREEN, self.nodeColor, self.nodePosition, self.nodeSize, 0)

    def drawConnections(self):
        for node in self.nodeConnections:
            pygame.draw.line(SCREEN, RELAY_BLUE, self.nodePosition, node.nodePosition, 2)

    def drawRange(self):

        if(self._checkCollision()): #colliding with object
            pygame.draw.circle(SCREEN, ERROR_RED, self.nodePosition, self.nodeSize, 0)
        else:
            pygame.draw.circle(SCREEN, HIGHLIGHT_GREEN, self.nodePosition, self.nodeSize, 0)
        pygame.draw.circle(SCREEN, BLACK, self.nodePosition, self.nodeRange, 1)

        
class TowerButton:

    def __init__(self, position, size, towerName, cost):
        self.position = position
        self.size = size
        self.towerName = towerName
        self.rectangle = pygame.Rect(100+self.position*85, WINDOW_HEIGHT-95, 80, 100)
        self.color = HIGHLIGHT_GREEN
        self.outline = DARK_HIGHLIGHT_GREEN
        self.cost = cost
        self.available = False

        self.checkPrice()

    def checkPrice(self):

        if(minerals >= self.cost):
            self.color = HIGHLIGHT_GREEN
            self.outline = DARK_HIGHLIGHT_GREEN
            self.available = True
        else:
            self.color = GRAY
            self.outline = BLACK
            self.available = False

    def drawButton(self):
        pygame.draw.rect(SCREEN, self.color, self.rectangle)
        pygame.draw.rect(SCREEN, self.outline, self.rectangle,2)

    def checkPress(self, position):
        if(self.rectangle.collidepoint(position) and self.available == True):
           return True
        return False

# FUNCTIONS

def drawButtons():
    for button in allTowerButtons:
        button.drawButton()

def drawTowers():
    for tower in allOpenTowers:
        tower.drawTower()
    for tower in allClosedTowers:
        tower.drawTower()

def drawNodes():
    for node in allOpenNodes:
        node.drawConnections()
    for node in allClosedNodes:
        node.drawConnections()
    for node in allOpenNodes:
        node.drawNode()
    for node in allClosedNodes:
        node.drawNode()
    

# BUTTONS

BLASERBUTTON = TowerButton(0, 25, "BLASER", 50)
NODEBUTTON = TowerButton(1,25,"NODE", 10)

#                   name, typ, position, size, hp, rang, maxConnections
ghostBLASER = Tower("BLASER", "LASER", (25,25), 10, 75, 150, 1)
ghostNODE = Node((25,25)) # DEBUG DELETE LATER


placementTowerLookupTable = [ghostBLASER, ghostNODE]
allTowerButtons = [BLASERBUTTON, NODEBUTTON]
allOpenTowers = []
allClosedTowers = []
allOpenNodes = []
allClosedNodes = []

#placement variabless

currentSelection = "HUD"
specificTower = None


while running:

    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    SCREEN.fill(WHITE)
    
    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1): # If mouse 1 is pressed

            if(placingTower == False):
                for button in allTowerButtons:
                    if(button.checkPress( (mouse_x, mouse_y)) == True):
                        specificTower = button.position
                
                        placingTower = True
            else: ## Tower not being placed
                tempTower = placementTowerLookupTable[specificTower]
                if(isinstance(tempTower, Tower)):
                    newTower = Tower(tempTower.towerName, tempTower.towerType, (mouse_x, mouse_y), tempTower.towerSize, tempTower.towerHp, tempTower.towerRange, tempTower.towerMaxConnections)
                    allOpenTowers.append(newTower)
                    placingTower = False
                else:
                    newNode = Node((mouse_x, mouse_y))
                    newConnections = newNode.findNearestOpenNodes()
                    for node in newConnections:
                        node.nodeConnections.append(newNode)
                        node.checkCapacity()
                    newNode.nodeConnections = newConnections #### TODO ASAP: MAKE NODES TELL OTHER NODES THAT THEY ARE NOW CONNECTED TO EACHOTHER, THEN CHECK WHETHER THEY ARE FULL OR NOT!!!!!!!!
                    allOpenNodes.append(newNode)
                    placingTower = False

        elif(event.type == pygame.MOUSEBUTTONDOWN and event.button == 3): # If mouse 2 is pressed

            if(placingTower == True):
                placingTower = False
                
                
        elif (event.type == pygame.QUIT):
            running = False

    if(placingTower == True):
        tempTower = placementTowerLookupTable[specificTower]
        if(isinstance(tempTower, Tower)): #is tower
            tempTower.towerPosition = (mouse_x, mouse_y)
            tempTower.drawRange()
        else: #is Energy Node
            tempTower.nodePosition = (mouse_x, mouse_y)
            nearestNodes = tempTower.findNearestOpenNodes()
            for node in nearestNodes: #draw ghostConnection
                pygame.draw.line(SCREEN, GHOST_BLUE, (mouse_x, mouse_y), node.nodePosition, 2)
            tempTower.drawRange()

    drawTowers()
    drawNodes()
    drawButtons()
                
    pygame.display.update()

pygame.quit()
