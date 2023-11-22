class PDA:
    def __init__(self, definition_file):
        self.states = set()
        self.input_symbols = set()
        self.stack_symbols = set()
        self.start_state = None
        self.start_stack_symbol = None
        self.accepting_states = set()
        self.acceptance_condition = None
        self.transitions = []

        self.load_definition(definition_file)

    def load_definition(self, definition_file):
        with open(definition_file, 'r') as file:
            for line in file:
                line = line.strip().split()
                if line[0] == 'Q':
                    self.states = set(line[1:])
                elif line[0] == 'a':
                    self.input_symbols = set(line[1:])
                elif line[0] == 'Z':
                    self.stack_symbols = set(line[1:])
                elif line[0] == 'Q':
                    self.start_state = line[1]
                elif line[0] == 'Z':
                    self.start_stack_symbol = line[1]
                elif line[0] == 'F':
                    self.accepting_states = set(line[1:])
                elif line[0] == 'F':
                    self.acceptance_condition = line[1]
                else:
                    self.transitions.append(tuple(line))

    def process_input(self, input_string):
        stack = [self.start_stack_symbol]
        current_state = self.start_state

        for symbol in input_string:
            for transition in self.transitions:
                if (
                    transition[0] == current_state
                    and transition[1] == symbol
                    and transition[2] == stack[-1]
                ):
                    stack.pop()
                    stack += list(transition[3])
                    current_state = transition[4]
                    break

        if (
            current_state in self.accepting_states
            and (self.acceptance_condition == 'E' and not stack)
            or (self.acceptance_condition == 'F' and current_state in self.accepting_states)
        ):
            return True
        else:
            return False


def main():
    pda = PDA('pda_definition.txt')

    while True:
        input_string = input('Enter an input string (or "exit" to quit): ')
        if input_string.lower() == 'exit':
            break

        result = pda.process_input(input_string)
        if result:
            print('Accepted')
        else:
            print('Rejected')


if __name__ == "__main__":
    main()
