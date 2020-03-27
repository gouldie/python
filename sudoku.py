import copy
import utils

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

def isRowValid(posY):
  for i in range(9):
    if (board[posY].count(i + 1) > 1):
      return False

  return True

def isColValid(posX):
  arr = []

  for i in range(9):
    arr.append(board[i][posX])

  for j in range(9):
    if arr.count(j + 1) > 1:
      return False

  return True

def isCubeValid(posY, posX):
  yRange = False
  xRange = False
  arr = []

  if posY < 3:
    yRange = [0, 1, 2]
  elif posY < 6:
    yRange = [3, 4, 5]
  else:
    yRange = [6, 7, 8]

  if posX < 3:
    xRange = [0, 1, 2]
  elif posX < 6:
    xRange = [3, 4, 5]
  else:
    xRange = [6, 7, 8]

  for y in yRange:
    for x in xRange:
      arr.append(board[y][x])

  for i in range(9):
    if arr.count(i + 1) > 1:
      return False

  return True

def getNextNode(posY, posX):
  newY = 0
  newX = 0

  if posX < 8:
    newY = posY
    newX = posX + 1
  elif posY < 8:
    newY = posY + 1
    newX = 0
  else:
    return False

  if board[newY][newX] != 0:
    return getNextNode(newY, newX)

  return [newY, newX]
    

def solve(posY, posX):
  for i in range(9):
    board[posY][posX] = i + 1

    if (isRowValid(posY) and isColValid(posX) and isCubeValid(posY, posX)):
      nextNode = getNextNode(posY, posX)

      if (nextNode == False):
        return True

      if (solve(nextNode[0], nextNode[1])):
        return True

    board[posY][posX] = START[posY][posX] or 0


print('Attempting to solve..')

board = copy.deepcopy(START)

result = solve(0, 0)

if (result):
  print('Complete! Board:')
  for i in range(9):
    print(board[i])
else:
  print('Unable to complete.', board)