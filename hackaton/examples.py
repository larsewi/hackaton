import prompter


def select(prompt, choices):
    selected = prompter.select(prompt, choices)
    print("You selected '%s'!" % selected)
