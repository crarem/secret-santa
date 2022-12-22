from flask import Flask, request, render_template
import random

app = Flask(__name__)

def generate_assignments(names, exclusions):
  # Loop until a valid assignment is found
  i=0
  while True:

    # Validate the input
    if len(names) < 2:
      raise ValueError('There must be at least 2 participants')
    if len(set(names)) != len(names):
      raise ValueError('Participant names must be unique')
    if any(len(e) != 2 for e in exclusions) and exclusions[0][0]!='':
      raise ValueError('Exclusions must be two names in format "name1,name2"')
    if any(e[0].strip() not in names or e[1].strip() not in names for e in exclusions) and exclusions[0][0]!='':
      raise ValueError('Excluded participants must be in the list of participants')

    # Shuffle the list of names
    print('Shuffling names...')
    random.shuffle(names)

    # Assign each person in the list to give to the next person in the list,
    # except for the last person, who will give to the first person
    receivers = names[1:] + [names[0]]

    
    valid = True
    # Check if the current assignment violates any of the exclusions (only if exclusions present)
    if exclusions[0][0]!='':
      for exclusion in exclusions:
        i = i+1
        e0 = exclusion[0].strip()
        e1 = exclusion[1].strip()
        if (e0 in names) and (e1 in names):
          if ((names[names.index(e0)], receivers[names.index(e0)]) == (e0,e1) or (names[names.index(e1)], receivers[names.index(e1)]) == (e1,e0)):
            valid = False
            print('Exclusion found!', exclusion)
            print(i)
            if i >= 50:
              raise ValueError('Impossible exclusion parameters')
            break

    # If the current assignment is valid, generate the list of assignments and exit the loop
    if valid:
      assignments = []
      for giver, recipient in zip(names, receivers):
        assignments.append(f"{giver} will give to {recipient}")
      break

  return assignments

@app.route('/secret-santa/')
def index():
  return render_template('index.html')

@app.route('/secret-santa/output', methods=['POST'])
def secret_santa():
  if request.method == 'POST':
    # Get the input from the form
    participants_input = request.form['participants']
    exclusions_input = request.form['exclusions']

    # Convert the input strings to lists of names and exclusions
    names = participants_input.strip().split('\r\n')
 
    exclusions = []
    exclusions = [tuple(t.split(',')) for t in exclusions_input.strip().split('\n')]

    #print('Names:',names)
    #print('Exclusions:',exclusions)

    # Generate the secret santa assignments
    try:
      assignments = generate_assignments(names, exclusions)
      print('Success...')
    except ValueError as e:
      # Render the template with the error message
      print('Error hit!')
      return render_template('index.html', error=str(e), participants=participants_input, exclusions=exclusions_input)

    # Render the template with the assignments and form data
    return render_template('index.html', assignments=assignments, participants=participants_input, exclusions=exclusions_input)
  else:
    # Render the template with empty form data
    return render_template('index.html', participants='', exclusions='')

if __name__ == '__main__':
  app.run()


