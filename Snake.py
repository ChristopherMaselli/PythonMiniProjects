import tkinter as tk
from tkinter import messagebox
import math
import random
import pygame


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        # Put eyes on the block snake: "[O-O]"
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Allows you to quit on pressing quit arrow
                pygame.quit()

            # Makes a dictionary for keys pressed so that multiple keys being pressed can be accounted for in the loop
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    # Adding a new turn to the dictionary so the snakes body can also turn where we previously turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    # Adding a new turn to the dictionary so the snakes body can also turn where we previously turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    # Adding a new turn to the dictionary so the snakes body can also turn where we previously turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    # Adding a new turn to the dictionary so the snakes body can also turn where we previously turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # Go through all of the cube objects in the body
        for i, c in enumerate(self.body):
            p = c.pos[:]  # for each object, grab the position of it "p"
            if p in self.turns:  # See if that position is in our turn list
                # Cube then sees that where we will turn is the turn at the index of p
                turn = self.turns[p]
                # Turn it in the X and Y coordinate it is supposed to move
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:  # If we are on the last cube...
                    self.turns.pop(p)  # We will remove that turn

            else:  # Code written for when you hit the edge, i.e. if you are going left, and position is 0 or less, the position of the cube now goes to the other side of the screen
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):  # Reset the snake in the game for another round
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx = tail.dirnx
        dy = tail.dirny

        # Figure out what direction the tail is going in so the tail can be added to the opposite side of the direction on the snake. i.e. if tial-cube is going right, attach it to the left of the tail-cube.

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        # Then make the cube go in the direction that the previous end of the tail was
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # Get a list of the filtered list of any positions to see if any positions are the same position as the snake, makes sure snack doesnt randomly pop up on top of the snake
        # A fancy way of looping through all of the snake square positions and checking if the positions are the same as where we are about to place the snack. then choosing a different point
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()  # Makes a new messagebox
    # Makes sure this new messagebox window is on top of anything/all other windows, like a popup
    root.attributes("-topmost", True)
    root.withdraw()  # Makes the window invisible
    messagebox.showinfo(subject, content)  # Shows the info
    # Code below destroys the message box when you click the "X" button
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    # Color, and then position (middle would be 10,10)
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)  # slows down the program, higher = slower
        # Make sure game doesnt run at more than 10 frames per second higher = faster
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        # Loop through every cube in our list of the snake's body, then if one of the cubes positions are the same, the game is over and you lose.
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redrawWindow(win)


main()
