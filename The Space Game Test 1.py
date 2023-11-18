import pygame

pygame.init()




# VARIABLES

WINDOW_WIDTH, WINDOW_HEIGHT = 750, 750
placingTower = False
allTowers = []

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("The Space Game")

screen.fill((255,255,255))

def createTower(x,y):
    allTowers.append((x,y))

def drawTowers():
    for towerLocs in allTowers:
        x,y = towerLocs
        pygame.draw.circle(screen,(0,0,0), (x,y), 15, 0)

    
def drawTowerRange(radius, x, y):
    color = (0,0,0)
    towerHighlightColor = (25,200,25)
    thickness = 2
    pygame.draw.circle(screen, color, (x,y), radius, thickness)
    pygame.draw.circle(screen, towerHighlightColor, (x,y), 15, 0)
    

running = True
while running:
    screen.fill((255,255,255))
    drawTowers()
    if(placingTower == True):
        mouseX, mouseY = pygame.mouse.get_pos()
        drawTowerRange(100, mouseX, mouseY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse_buttons = pygame.mouse.get_pressed()
        if(mouse_buttons[0]):
            if(placingTower == True):
                mouseX, mouseY = pygame.mouse.get_pos()
                createTower(mouseX, mouseY)
            placingTower = not placingTower

    pygame.display.update()

pygame.quit()
