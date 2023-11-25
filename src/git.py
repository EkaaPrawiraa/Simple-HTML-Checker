import os

start_input = ""
found = 0
accepted_config = []
productions = {}
states = []
symbols = []
stack_symbols = []
start_symbol = ""
start_stack = ""
acceptable_states = []
accept_with = ""


def generate(state, input, stack, config):
    global productions
    global found

    total = 0

    if found:
        return 0

    if is_found(state, input, stack):
        found = 1
        accepted_config.extend(config)
        return 1

    moves = get_moves(state, input, stack, config)
    if len(moves) == 0:
        return 0

    for i in moves:
        total += generate(i[0], i[1], i[2], config + [(i[0], i[1], i[2])])

    return total


def get_moves(state, input, stack, config):
    global productions

    moves = []

    for i in productions:
        if i != state:
            continue

        for j in productions[i]:
            current = j
            new = []

            new.append(current[3])

            if len(current[0]) > 0:
                if len(input) > 0 and input[0] == current[0]:
                    new.append(input[1:])
                else:
                    continue
            else:
                new.append(input)

            if len(current[1]) > 0:
                if len(stack) > 0 and stack[0] == current[1]:
                    new.append(current[2] + stack[1:])
                else:
                    continue
            else:
                new.append(current[2])

            moves.append(new)

    return moves


def is_found(state, input, stack):
    global accept_with
    global acceptable_states

    if len(input) > 0:
        return 0

    if accept_with == "E":
        if len(stack) < 1:
            return 1

        return 0
    else:
        for i in acceptable_states:
            if i == state:
                return 1

        return 0


def print_config(config):
    for i in config:
        print(i)


def parse_file(filename):
    global productions
    global start_symbol
    global start_stack
    global acceptable_states
    global accept_with

    try:
        lines = [line.rstrip() for line in open(filename)]
    except FileNotFoundError:
        return 0

    start_symbol = lines[3]
    start_stack = lines[4]
    acceptable_states.extend(lines[5].split())
    accept_with = lines[6]

    for i in range(7, len(lines)):
        production = lines[i].split()
        configuration = [(production[1], production[2], production[4], production[3])]

        if production[0] not in productions.keys():
            productions[production[0]] = []

        configuration = [tuple(s if s != "e" else "" for s in tup) for tup in configuration]

        productions[production[0]].extend(configuration)

    print(productions)
    print(start_symbol)
    print(start_stack)
    print(acceptable_states)
    print(accept_with)

    return 1


def done():
    if found:
        print("Hurray! Input word \"" + start_input + "\" is part of grammar.")
    else:
        print("Sorry! Input word \"" + start_input + "\" is not part of grammar.")


filename = input("Please enter your automata file:\n")
while not parse_file(filename):
    print("File not found!")
    filename = input("Please enter your automata file again:\n")
print("Automata built.")

start_input = input("Please enter your word:\n")
print("Checking word \"" + start_input + "\" ...")

while start_input != "end":
    if not generate(start_symbol, start_input, start_stack, [(start_symbol, start_input, start_stack)]):
        done()
    else:
        print_config(accepted_config)
        done()

    start_input = input("Enter your next word (or end):\n")
    print("Checking word \"" + start_input + "\" ...")
