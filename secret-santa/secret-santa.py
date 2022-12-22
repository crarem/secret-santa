import random

# List of names for secret santa
names = ["Jane", "John", "Sue", "Bob", "Molly", "Tom"]

# List of exclusions, where each element is a tuple containing the names of
# two parties that cannot give to each other
exclusions = [("Jane", "Bob"), ("John", "Sue"), ("Molly", "Tom")]

# Loop until a valid assignment is found
while True:
  # Shuffle the list of names
  print('Shuffling names...')
  random.shuffle(names)

  # Assign each person in the list to give to the next person in the list,
  # except for the last person, who will give to the first person
  givers = names[1:] + [names[0]]

  # Check if the current assignment violates any of the exclusions
  valid = True
  for exclusion in exclusions:
    if ((names[names.index(exclusion[0])], givers[names.index(exclusion[0])]) == exclusion or (names[names.index(exclusion[1])], givers[names.index(exclusion[1])]) == (exclusion[1],exclusion[0])):
      valid = False
      print('Exclusion found!', exclusion)
      break

  # If the current assignment is valid, print the list of givers and recipients and exit the loop
  if valid:
    for giver, recipient in zip(names, givers):
      print(f"{giver} will give to {recipient}")
    break

