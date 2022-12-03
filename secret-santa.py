import random

# List of names for secret santa
names = ["Jane", "John", "Sue", "Bob", "Molly", "Tom"]

# Shuffle the list of names
random.shuffle(names)

# Assign each person in the list to give to the next person in the list,
# except for the last person, who will give to the first person
givers = names[1:] + [names[0]]

# Print the list of givers and use zip function to group the recipients alongside givers
for giver, recipient in zip(names, givers):
  print(f"{giver} will give to {recipient}")
