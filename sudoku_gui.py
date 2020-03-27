""" Runs the GUI """
import pygame
import copy

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

    for i in range(9):
      for j in range(9):
        self.cubes[i].append(Cube(width/9, height/9, i, j, self.board[i][j]))

  def draw(self):
    squareWidth = (self.width / 9)

    pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 500, 500))

    for i in range(9):
      for j in range(9):
        self.cubes[i][j].draw(self.screen)

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

class Cube:
  def __init__(self, width, height, row, col, value):
    self.selected = False
    self.value = value
    self.width = width
    self.height = height
    self.row = row
    self.col = col

  def draw(self, screen):
    fnt = pygame.font.SysFont("comicsans", 40)

    if (self.selected):
      pygame.draw.rect(screen, (200, 200, 200), (int(self.row * self.width) + 1, int(self.col * self.height) + 1, int(self.width), int(self.height)))
    
    text = str(self.value)
    textSurface = fnt.render(text, 1, (128,128,128))
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

    draw_window(grid)
    pygame.display.update()

print('Running..')
main()
pygame.quit()
