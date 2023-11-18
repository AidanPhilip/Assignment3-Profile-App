import pygame
import math

pygame.init()

# CONSTANTS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 200)
GRAY = (100,100,100)
NODE_BLUE = (56, 189, 239)
GHOST_BLUE = (63, 82, 214)
RELAY_BLUE = (17, 160, 215)
HIGHLIGHT_GREEN = (50,200,50)
DARK_HIGHLIGHT_GREEN = (0,75,0)
ERROR_RED = (200,50,50)

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Space Game")

# VARIABLES I COULDN'T PUT BELOW THE CLASSES

# CLASSES

def calcDistance(x1, x2, y1, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance



class Tower:
    def __init__(self, towerName, towerPosition, towerSize, towerHp, towerType, towerRange):
        self.towerName = towerName
        self.towerPosition = towerPosition
        self.towerSize = towerSize
        self.towerHp = towerHp
        self.towerType = towerType
        self.towerRange = towerRange
        self.towerConRange = 75
        self.nodeConnection = None

    def _collisionTowerChecking(self, position, TowersArray):
        collision = False
        for tower in TowersArray:
            tempX,tempY = tower.towerPosition
            tempDistance = calcDistance(position[0], tempX, position[1], tempY)
            if(tempDistance <= self.towerSize*2):
                collision = True
                break
        return collision

    def placeRange(self, position):
        collision = self._collisionTowerChecking(position, allClosedTowers)
        if(collision == False): collision = self._collisionTowerChecking(position, allOpenTowers)
            
        elif(collision == False):
            for node in allOpenNodes:
                tempX,tempY = node.nodePosition
                tempDistance = calcDistance(position[0], tempX, position[1], tempY)
                if(tempDistance <= self.towerSize + node.nodeSize):
                    collision = True
                    break
    
        global towerCollision
        towerCollision = collision
        pygame.draw.circle(SCREEN, BLACK,               position, self.towerRange, 1) # range circle
        if(collision == True):
            pygame.draw.circle(SCREEN, ERROR_RED,       position, self.towerSize, 0) # tower circle
        else:   
            pygame.draw.circle(SCREEN, HIGHLIGHT_GREEN, position, self.towerSize, 0) # tower circle

    def drawTower(self):
        pygame.draw.circle(SCREEN, BLACK, self.towerPosition, self.towerSize, 0)



class EnergyNode:
    def __init__(self, nodePosition):
        self.nodePosition = nodePosition
        self.nodeHp = 50
        self.nodeRange = 150
        self.nodeSize = 4
        self.nodeMaxConnections = 6
        self.nodeConnections = []
        self.towerConnections = []
        self.color = RELAY_BLUE

    def _collisionTowerChecking(self, position, towerArray):
        collision = False
        for tower in towerArray:
            tempX, tempY = tower.towerPosition
            tempDistance = calcDistance(position[0], tempX, position[1], tempY)
            if(tempDistance <= tower.towerSize + self.nodeSize):
                collision = True
                break
        return collision
    
    def placeRange(self, position):
        collision = self._collisionTowerChecking(position, allClosedTowers)
        if(collision == False): collision = self._collisionTowerChecking(position, allOpenTowers)
        elif(collision == False):
            for node in allOpenNodes:
                tempX,tempY = node.nodePosition
                tempDistance = calcDistance(position[0], tempX, position[1], tempY)
                if(tempDistance <= self.nodeSize*2):
                    collision = True
                    break
                
        global towerCollision
        towerCollision = collision
        pygame.draw.circle(SCREEN, BLACK,           position, self.nodeRange, 1) # range circle
        if(collision == True):
            pygame.draw.circle(SCREEN, ERROR_RED, position, self.nodeSize, 0) # node circle
        else:
            pygame.draw.circle(SCREEN, HIGHLIGHT_GREEN, position, self.nodeSize, 0) # node circle

    def drawNode(self):
        pygame.draw.circle(SCREEN, RELAY_BLUE, self.nodePosition, self.nodeSize, 0)
        
    def drawConnection(self):
        for connection in self.nodeConnections:
            pygame.draw.line(SCREEN, NODE_BLUE, self.nodePosition, connection.nodePosition, 2)
        for connection in self.towerConnections:
            pygame.draw.line(SCREEN, NODE_BLUE, self.nodePosition, connection.towerPosition, 2)
        


        

class TowerButton:
    def __init__(self, position, size, towerName):
        self.towerPosition = position
        self.size = size
        self.towerType = towerName
        self.rectangle = pygame.Rect(100+self.towerPosition*85, WINDOW_HEIGHT-95, 80, 100)
        self.color = HIGHLIGHT_GREEN
        self.outline = DARK_HIGHLIGHT_GREEN

    def drawButton(self):
        pygame.draw.rect(SCREEN, self.color, self.rectangle)
        pygame.draw.rect(SCREEN, self.outline, self.rectangle,2)

    def checkButton(self, position):
        if(self.rectangle.collidepoint(position)):
           return True
        return False

def findNearestTowers(towerType, currentPosition):
    nearestTowers = []
    if(towerType == "NODE"):
        for tower,node in zip(allOpenTowers,allOpenNodes):
            towerDistance = calcDistance(tower.towerPosition[0], currentPosition[0], tower.towerPosition[1], currentPosition[1])
            nodeDistance = calcDistance(node.nodePosition[0], currentPosition[0], node.nodePosition[0], currentPosition[1])

            if(towerDistance <= ghostTHEL.towerRange):
                nearestTowers.append(tower)
            if(nodeDistance <= ghostNode.nodeRange):
                nearestTowers.append(node)
    return nearestTowers


def drawTowers():
    for tower in allClosedTowers:
        tower.drawTower()
    for tower in allOpenTowers:
        tower.drawTower()

def drawNodes():
    for node in allOpenNodes:
        if(not len(node.nodeConnections) == 0 or not len(node.towerConnections) == 0):
            node.drawConnection()
    for node in allOpenNodes:
        node.drawNode()
        
def drawTowerButtons():
    for button in allTowerButtons:
        button.drawButton()

# VARIABLES

running = True
placingTower = False
towerCollision = False
towerBeingPlaced = ""
closestConnection = []

ghostTHEL = Tower("THEL", None, 10, 100, "THEL", 150)
ghostNode = EnergyNode(None)

THELButton = TowerButton(1, 25, "THEL")
nodeButton = TowerButton(2, 25, "NODE")

allTowerButtons = [THELButton, nodeButton]
allClosedTowers = []
allOpenTowers = []
allOpenNodes = []
allClosedNodes = []

print(isinstance(THELButton, TowerButton))

while running:
    
    SCREEN.fill(WHITE)

    if(len(closestConnection) != 0):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for connection in closestConnection:
            tempDistance = calcDistance(connection.nodePosition[0], mouse_x, connection.nodePosition[1], mouse_y)
            if(tempDistance >= ghostNode.nodeRange):
                closestConnection.remove(connection)
            else:
                pygame.draw.line(SCREEN, GHOST_BLUE, connection.nodePosition, (mouse_x, mouse_y), 2)
    
    drawNodes()
    drawTowers()

    if(placingTower == True): #GHOST DRAWING
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for node in allOpenNodes:
                
            tempDistance = calcDistance(node.nodePosition[0], mouse_x, node.nodePosition[1], mouse_y)

            if(tempDistance <= ghostNode.nodeRange):
                closestConnection.append(node)
                    
        if(towerBeingPlaced == "THEL"):
            ghostTHEL.placeRange((mouse_x, mouse_y))
        elif(towerBeingPlaced == "NODE"):
            ghostNode.placeRange((mouse_x, mouse_y))
            
    for event in pygame.event.get():

        if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            
            if(placingTower == True and towerCollision == False): # TOWER PLACEMENT
                mouse_x, mouse_y = pygame.mouse.get_pos()
                placingTower = False
                closestConnection = []
                if(towerBeingPlaced == "THEL"):
                    newTHEL = Tower("THEL", (mouse_x, mouse_y), 10, 100, "THEL", 50)
                    successfulConnection = False

                    for node in allOpenNodes:

                        tempDistance = calcDistance(node.nodePosition[0], mouse_x, node.nodePosition[1], mouse_y)

                        if(tempDistance <= ghostNode.nodeRange):
                            newTHEL.nodeConnection = node
                            node.towerConnections.append(newTHEL)
                            successfulConnection = True
                            break

                    if(successfulConnection == True): # if connected, consider it a "closed" tower
                        allClosedTowers.append(newTHEL)
                    else: # if not connected, consider it an "open" tower
                        allOpenTowers.append(newTHEL)
                if(towerBeingPlaced == "NODE"):
                    newNode = EnergyNode((mouse_x,mouse_y))

                    #connect all nodes within the area to the nodes

                    for node in allOpenNodes:

                        tempDistance = calcDistance(node.nodePosition[0], mouse_x, node.nodePosition[1], mouse_y)

                        if(tempDistance <= ghostNode.nodeRange):
                            newNode.nodeConnections.append(node)
                            node.nodeConnections.append(newNode)

                    i = 0
                    while i < len(allOpenTowers):

                        tower = allOpenTowers[i]
                        tempDistance = calcDistance(tower.towerPosition[0], mouse_x, tower.towerPosition[1], mouse_y)
                        
                        if(tempDistance <= ghostNode.nodeRange):
                            newNode.towerConnections.append(tower)
                            tower.nodeConnection = newNode
                            allClosedTowers.append(tower)
                            allOpenTowers.remove(tower)
                        else:
                            i += 1
                    
                    allOpenNodes.append(newNode)
                    
                
            elif(placingTower == False): 
                mouse_x, mouse_y = pygame.mouse.get_pos()
                pressedButton = ""
                for button in allTowerButtons:
                    if(button.checkButton((mouse_x, mouse_y)) == True):
                        placingTower = True
                        towerBeingPlaced = button.towerType
                        break

        elif(placingTower == True and event.type == pygame.MOUSEBUTTONDOWN and event.button == 3):
            placingTower = False
            

        elif (event.type == pygame.QUIT):
            running = False
            closestConnection = []
    
    drawTowerButtons()
        
    pygame.display.update()

pygame.quit()
