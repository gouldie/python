""" Runs the GUI """
import pygame
import copy
import time

pygame.init()
pygame.font.init()

START = [
  [0, 0, 0, 0, 0, 0, 2, 0, 0],
  [0, 8, 0, 0, 0, 7, 0, 9, 0],
  [6, 0, 2, 0, 0, 0, 5, 0, 0],
  [0, 7, 0, 0, 6, 0, 0, 0, 0],
  [0, 0, 0, 9, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 2, 0, 0, 4, 0],
  [0, 0, 5, 0, 0, 0, 6, 0, 3],
  [0, 9, 0, 4, 0, 0, 0, 7, 0],
  [0, 0, 6, 0, 0, 0, 0, 0, 0]
]

class Grid:
  def __init__(self, screen, width, height):
    self.board = copy.deepcopy(START)
    self.screen = screen
    self.width = width
    self.height = height
    self.cubes = [
      [],[],[],[],[],[],[],[],[]
    ]
    self.selected = []
    self.count = 0

    for i in range(9):
      for j in range(9):
        self.cubes[i].append(Cube(width/9, height/9, i, j, self.board[j][i]))

  def draw(self):
    print('drawing')
    squareWidth = (self.width / 9)

    pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 500, 500))

    for i in range(9):
      for j in range(9):
        self.cubes[i][j].draw(self.screen, self.board[j][i])

    for i in range(10):
      if i % 3 == 0 and i != 0:
        thickness = 3
      else:
        thickness = 1

      pygame.draw.line(self.screen, (0, 0, 0), (0, int(i * squareWidth)), (self.height, int(i * squareWidth)), thickness)
      pygame.draw.line(self.screen, (0, 0, 0), (int(i * squareWidth), 0), (int(i * squareWidth), self.width), thickness)

  def click(self, pos):
    posX = pos[0]
    posY = pos[1]

    squareWidth = (self.width / 9)

    x = int(posX/squareWidth)
    y = int(posY/squareWidth)

    if len(self.selected) == 0:
      self.selected = [x, y]
      self.cubes[x][y].selected = True
    elif self.selected[0] == x and self.selected[1] == y:
      self.selected = []
      self.cubes[x][y].selected = False
    else:
      self.cubes[self.selected[0]][self.selected[1]].selected = False
      self.cubes[x][y].selected = True
      self.selected = [x, y]

  def enter(self, num):
    if self.selected[0] and self.selected[1]:
      # self.cubes[self.selected[0]][self.selected[1]].value = num
      self.board[self.selected[0]][self.selected[1]] = num


  def getNextNode(self, posX, posY):
    newX = 0
    newY = 0

    if posY < 8:
      newX = posX
      newY = posY + 1
    elif posX < 8:
      newX = posX + 1
      newY = 0
    else:
      return False

    if self.board[newX][newY] != 0:
      return self.getNextNode(newX, newY)

    return [newX, newY]

  def solve(self, posX, posY):
    for i in range(9):
      self.board[posX][posY] = i + 1
      
      # self.draw(x, y)
      # pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 500, 500))
      self.cubes[posY][posX].draw(self.screen, i + 1)

      if (self.isRowValid(posX) and self.isColValid(posY) and self.isCubeValid(posX, posY)):
        nextNode = self.getNextNode(posX, posY)

        if (nextNode == False):
          return True

        pygame.display.update()
        pygame.time.delay(50)

        if (self.solve(nextNode[0], nextNode[1])):
          return True

      self.board[posX][posY] = START[posX][posY] or 0

  def isRowValid(self, posX):
    for i in range(9):
      if (self.board[posX].count(i + 1) > 1):
        return False

    return True

  def isColValid(self, posY):
    arr = []

    for i in range(9):
      arr.append(self.board[i][posY])

    for j in range(9):
      if arr.count(j + 1) > 1:
        return False

    return True

  def isCubeValid(self, posX, posY):
    yRange = False
    xRange = False
    arr = []

    if posX < 3:
      xRange = [0, 1, 2]
    elif posX < 6:
      xRange = [3, 4, 5]
    else:
      xRange = [6, 7, 8]

    if posY < 3:
      yRange = [0, 1, 2]
    elif posY < 6:
      yRange = [3, 4, 5]
    else:
      yRange = [6, 7, 8]

    for x in xRange:
      for y in yRange:
        arr.append(self.board[x][y])

    for i in range(9):
      if arr.count(i + 1) > 1:
        return False

    return True


class Cube:
  def __init__(self, width, height, row, col, value):
    self.selected = False
    # self.value = value
    self.width = width
    self.height = height
    self.row = row
    self.col = col

  def draw(self, screen, value):
    fnt = pygame.font.SysFont("comicsans", 40)

    if (self.selected):
      pygame.draw.rect(screen, (200, 200, 200), (int(self.row * self.width) + 1, int(self.col * self.height) + 1, int(self.width), int(self.height)))
    
    text = str(value) 
    textSurface = fnt.render(text, 1, (128,128,128), (255,255,255))
    screen.blit(textSurface, (int(self.row * self.width) + int(self.width/2.7), int(self.col * self.height) + int(self.height/3.1)))

def draw_window(board):
  board.draw()

def main():
  screen = pygame.display.set_mode((500,500))
  pygame.display.set_caption("Sudoku")
  grid = Grid(screen, 500, 500)

  key = None
  run = True

  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        x = grid.click(pos)
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          grid.enter(0)
        if event.key == pygame.K_1:
          grid.enter(1)
        if event.key == pygame.K_2:
          grid.enter(2)
        if event.key == pygame.K_3:
          grid.enter(3)
        if event.key == pygame.K_4:
          grid.enter(4)
        if event.key == pygame.K_5:
          grid.enter(5)
        if event.key == pygame.K_6:
          grid.enter(6)
        if event.key == pygame.K_7:
          grid.enter(7)
        if event.key == pygame.K_8:
          grid.enter(8)
        if event.key == pygame.K_9:
          grid.enter(9)
        if event.key == pygame.K_SPACE:
          grid.solve(0, 0)

    draw_window(grid)
    pygame.display.update()

print('Running..')
main()
pygame.quit()
