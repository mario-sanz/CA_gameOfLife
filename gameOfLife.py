import pygame, sys
import numpy as np
import matplotlib.pyplot as plt
import time
import math

pygame.init()

# Height and width of the screen
width, height = 600, 600

# Number of cells
nxC = 60
nyC = 60
# Dimensions of each cell
dimCW = (width-1) / nxC
dimCH = (height-1) / nyC

# Background color
bg = 25,25,25

# Creation of the screen
screen = pygame.display.set_mode((height, width), pygame.RESIZABLE)

# Paint the screen with the background color
screen.fill(bg)

# Initialize the board with the shape we want
gameState = np.zeros((nxC, nyC))

# Mobile Automata
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Execution control of the player
pauseExec = False

while 1:

    new_gameState = np.copy(gameState)

    # proceed events
    ev = pygame.event.get()

    for event in ev:
        # Detect if any key is pressed
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        # Detect if the mouse is pressed
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()

            if posX > 0 and posX < width-1 and posY > 0 and posY < height-1:
                new_gameState[math.floor(posX / dimCW),
                              math.floor(posY / dimCH)] = mouseClick[0] and not mouseClick[2]
         

    screen.fill(bg)

    for y in range(0, nyC):
        for x in range(0, nxC):
            # If the execution is not paused
            if not pauseExec:
                # Count the number of neighbours we have (the module is used to have a toroidal model)
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[(x)   % nxC, (y-1) % nyC] + \
                          gameState[(x+1) % nxC, (y-1) % nyC] + \
                          gameState[(x-1) % nxC, (y)   % nyC] + \
                          gameState[(x+1) % nxC, (y)   % nyC] + \
                          gameState[(x-1) % nxC, (y+1) % nyC] + \
                          gameState[(x)   % nxC, (y+1) % nyC] + \
                          gameState[(x+1) % nxC, (y+1) % nyC]
                
                
                # ORIGINAL RULES OF THE "GAME OF LIFE"
                # Any dead cell with three live neighbours becomes a live cell.
                if gameState[x,y] == 0 and n_neigh == 3:
                    new_gameState[x,y] = 1
                # Any live cell with two or three live neighbours lives on to the next generation. Otherwise, it dies.
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_gameState[x,y] = 0
                """
                # COOL RULES I HAVE FOUND
                if gameState[x,y] == 0 and n_neigh == 3:
                    new_gameState[x,y] = 1
                elif gameState[x,y] == 1 and (n_neigh < 1 or n_neigh > 4):
                    new_gameState[x,y] = 0
                """

            # Calculate the position of each cell
            poly = [((x)*dimCW, (y)*dimCH),
                    ((x+1)*dimCW, (y)*dimCH),
                    ((x+1)*dimCW, (y+1)*dimCH),
                    ((x)*dimCW, (y+1)*dimCH)]
    
            # Draw the state computed in the cell
            if gameState[x,y] == 0:
                pygame.draw.polygon(screen, (128,128,128), poly, 1)
            else:
                pygame.draw.polygon(screen, (200,200,200), poly, 0)

    time.sleep(1/30)

    gameState = np.copy(new_gameState)
    pygame.display.flip()
