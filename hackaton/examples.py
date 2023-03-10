import prompter

def select(question, choices):
    selected = prompter.select(question, choices)
    print("You selected %s" % selected)
