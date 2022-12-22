from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/")
def index():
  # Get the names and exclusions from the query string
  names = request.args.get("names")
  exclusions = request.args.get("exclusions")

  # If names and exclusions are provided, generate the secret santa assignments
  assignments = []
  if names and exclusions:
    # Parse the names and exclusions from the query string
    names = names.split(",")
    exclusions = [tuple(exclusion.split(",")) for exclusion in exclusions.split(";")]

    # Loop until a valid assignment is found
    while True:
      # Shuffle the list of names
      random.shuffle(names)

      # Assign each person in the list to give to the next person in the list,
      # except for the last person, who will give to the first person
      givers = names[1:] + [names[0]]

      # Check if the current assignment violates any of the exclusions
      valid = True
      for exclusion in exclusions:
        if (names[exclusion[0]], givers[exclusion[0]]) == exclusion or (names[exclusion[1]], givers[exclusion[1]]) == exclusion:
          valid = False
          break

      # If the current assignment is valid, store the list of givers and exit the loop
      if valid:
        assignments = [(names[i], givers[i]) for i in range(len(names))]
        break

  # Render the index template with the names, exclusions, and assignments
  return render_template("index.html", names=names, exclusions=exclusions, assignments=assignments)

if __name__ == "__main__":
  app.run()
