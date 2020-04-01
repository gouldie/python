""" A Star pathfinding algorithm """
import pygame

class Grid:
  def __init__(self, screen, grid, start = (3, 3), end = (20, 20)):
    self.screen = screen
    self.grid = grid
    self.nodes = []
    self.startX = start[0]
    self.startY = start[1]
    self.endX = end[0]
    self.endY = end[1]
    self.solving = False

    for row in range(len(grid)):
      self.nodes.append([])

    pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 450, 450))

    for x in range(len(self.grid)):
      for y in range(len(self.grid[x])):
        self.nodes[x].append(Node(self.screen, self.grid[x][y], x, y))

    # Set up start and end node
    self.nodes[self.startX][self.startY].value = 5
    self.nodes[self.startX][self.startY].draw()
    self.nodes[self.endX][self.endY].value = 4
    self.nodes[self.endX][self.endY].draw()

  def click(self, pos):
    if (self.solving):
      return

    posX = pos[0]
    posY = pos[1]

    x = int(posX / 15)
    y = int(posY / 15)

    print(x,y)

    if self.nodes[x][y].value == 0:
      self.nodes[x][y].value = 3
    elif self.nodes[x][y].value == 3:
      self.nodes[x][y].value = 0

    self.nodes[x][y].draw()

  def distanceBetweenNodes(self, node1, node2):
    xDif = abs(node1.x - node2.x)
    yDif = abs(node1.y - node2.y)

    return max(xDif, yDif)

  def solve(self):
    print('Solving')
    self.solving = True
    start_node = self.nodes[self.startX][self.startY]
    end_node = self.nodes[self.endX][self.endY]

    open_list = []
    closed_list = []

    open_list.append(start_node)

    # Loop until we find the end
    while len(open_list) > 0:
      # Get the current node
      current_node = open_list[0]

      for node in open_list:
        if node.f < current_node.f:
          current_node = node

      # Draw nodes
      for node in open_list:
        self.nodes[node.x][node.y].value = 2

      current_node.value = 1

      for x in range(len(self.nodes)):
        for y in range(len(self.nodes[x])):
          self.nodes[x][y].draw()

      pygame.display.update()
      pygame.time.delay(50)

      open_list.remove(current_node)
      closed_list.append(current_node)

      # Found the goal
      if end_node.eq(current_node):
        print('Reached goal!')
        path = []
        current = current_node
        while current is not None:
          path.append((current.x, current.y))
          current = current.parent
        path = path[::-1]

        # Redraw solution path
        for x in range(len(self.grid)):
          for y in range(len(self.grid[x])):
            value = self.nodes[x][y].value
            if value == 1 or value == 2:
              self.nodes[x][y].value = 0

        for node in path:
          self.nodes[node[0]][node[1]].value = 1

        for x in range(len(self.grid)):
          for y in range(len(self.grid[x])):
            self.nodes[x][y].draw()

        return path[::-1] # Return reversed path

      # Generate children
      children_coords = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
      children_coords_relative = []

      for coord in children_coords:
        children_coords_relative.append((current_node.x + coord[0], current_node.y + coord[1]))

      children_nodes = []

      for coord in children_coords_relative:
        # If coord is in the board
        if coord[0] >= 0 and coord[1] >= 0 and len(self.nodes) > coord[0] and len(self.nodes[coord[0]]) > coord[1]:
          # If coord is value 0
          if self.nodes[coord[0]][coord[1]].value == 0 or self.nodes[coord[0]][coord[1]].value == 4:
            self.nodes[coord[0]][coord[1]].parent = current_node
            children_nodes.append(self.nodes[coord[0]][coord[1]])

      # Loop through children
      for child in children_nodes:
        onClosedList = False

        # Child is on the closed list
        for closed in closed_list:
          if (closed.eq(child)):
            onClosedList = True

        if onClosedList:
          continue

        child.g = current_node.g + self.distanceBetweenNodes(current_node, child)
        child.h = self.distanceBetweenNodes(child, end_node)
        child.f = child.g + child.h

        # Child already in open list
        for item in open_list:
          if item.eq(child):
            if child.g > item.g:
              continue
        
        # Add child to open list
        open_list.append(child)



class Node:
  def __init__(self, screen, value, x = None, y = None, parent = None):
    self.screen = screen
    self.width = 15
    self.height = 15
    self.x = x
    self.y = y
    self.value = value
    self.parent = parent
    self.g = 0
    self.h = 0
    self.f = 0

    self.draw()

  def eq(self, node):
    if self.x == node.x and self.y == node.y:
      return True

  def draw(self):
    # 0 = empty
    # 1 = attempts
    # 2 = open list
    # 3 = block
    # 4 = goal
    # 5 = start

    if self.value == 0:
      innerColour = (255, 255, 255)
    elif self.value == 1:
      innerColour = (0, 255, 0)
    elif self.value == 2:
      innerColour = (0, 150, 100)
    elif self.value == 3:
      innerColour = (255, 0, 0)
    else:
      innerColour = (0, 255, 0)
    pygame.draw.rect(self.screen, (0, 0, 0), (self.x * self.width, self.y * self.height, self.width, self.height))
    pygame.draw.rect(self.screen, innerColour, ((self.x * self.width) + 1, (self.y * self.height) + 1, self.width - 2, self.height - 2))


def main():
  screen = pygame.display.set_mode((450,450))
  pygame.display.set_caption("A Star")
  values = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  ]

  grid = Grid(screen, values)

  key = None
  run = True

  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        grid.click(pos)
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          if grid.solving:
            continue
          solution = grid.solve()
          print(solution)

    pygame.display.update()

main()
pygame.quit()