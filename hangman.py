import utils

MAX_ATTEMPTS = 10
ANSWER = ['P', 'Y', 'T', 'H', 'O', 'N']

attempts = 0
attempt = ''
word = [False, False, False, False, False, False]
previous_guesses = []

print('Selecting a word..')
print('')

while ((attempts < MAX_ATTEMPTS) & (word != ANSWER)):
  print('Word:', utils.array_to_string(word))
  print(MAX_ATTEMPTS - attempts, 'attempts remaining')
  print('Previous guesses:', utils.array_to_string(previous_guesses))

  attempt = input('Choose the next letter: ').upper()

  if (len(attempt) != 1):
    print('Please enter one character only')
    print('')
    continue

  if (attempt.isalpha() == False):
    print('Please only enter letters')
    print('')
    continue

  if (previous_guesses.count(attempt) > 0):
    print(attempt, 'has been guessed before')
    print('')
    continue

  attempts += 1
  previous_guesses.append(attempt)
  
  match = utils.getIndexPositions(ANSWER, attempt)

  for val in match:
    word[val] = attempt

  print('')

print('Word:', utils.array_to_string(ANSWER))

if (ANSWER == word):
  print('You win!')
elif (attempts >= MAX_ATTEMPTS):
  print('You lose!')

