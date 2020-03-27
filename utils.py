def getIndexPositions(listOfElements, element):
  ''' Returns the indexes of all occurrences of give element in
  the list- listOfElements '''
  indexPosList = []
  indexPos = 0
  while True:
    try:
      # Search for item in list from indexPos to the end of list
      indexPos = listOfElements.index(element, indexPos)
      # Add the index position in list
      indexPosList.append(indexPos)
      indexPos += 1
    except ValueError:
      break

  return indexPosList

def array_to_string(arr):
  string = ''
  for val in arr:
    if (bool(val)):
      string += val
    else:
      string += '_'

    string += ' '

  return string