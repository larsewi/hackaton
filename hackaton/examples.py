import prompter


def select(prompt, choices):
    selected = prompter.select(prompt, choices)
    if selected is not None:
        print("You selected: %s 🚀" % selected)
    else:
        print("Why you no answer? 🤷")
