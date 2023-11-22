class PDA:
    def __init__(self, states, input_symbols, stack_symbols, start_state, start_stack, accepting_states, transitions):
        self.states = states
        self.input_symbols = input_symbols
        self.stack_symbols = stack_symbols
        self.start_state = start_state
        self.start_stack = start_stack
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.stack = [start_stack]

    def process_input(self, input_word):
        current_state = self.start_state

        for symbol in input_word:
            current_stack_top = self.stack[-1] if self.stack else None
            transition = self.find_transition(current_state, symbol, current_stack_top)

            if transition is None:
                return False

            next_state, stack_action = transition
            current_state = next_state

            if stack_action != 'e':
                if stack_action == 'E':
                    if not self.stack:
                        return False
                    self.stack.pop()
                else:
                    self.stack.extend(stack_action[::-1])

        return current_state in self.accepting_states and not self.stack

    def find_transition(self, current_state, input_symbol, stack_top):
        for transition in self.transitions:
            if (
                transition[0] == current_state
                and (transition[1] == input_symbol or transition[1] == 'e')
                and (transition[2] == stack_top or transition[2] == 'Z')
            ):
                return transition[3], transition[4]
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python main.py <pda_file> <html_file>")
        sys.exit(1)

    pda_file = sys.argv[1]
    html_file = sys.argv[2]

    try:
        with open(pda_file, 'r') as pda_file:
            lines = pda_file.readlines()

            states = set(lines[0].split())
            input_symbols = set(lines[1].split())
            stack_symbols = set(lines[2].split())
            start_state = lines[3].strip()
            start_stack = lines[4].strip()
            accepting_states = set(lines[5].split())

            transitions = [line.strip().split() for line in lines[7:]]
    except FileNotFoundError:
        print(f"PDA file {pda_file} not found.")
        sys.exit(1)

    try:
        with open(html_file, 'r') as html_file:
            html_content = html_file.read()
    except FileNotFoundError:
        print(f"HTML file {html_file} not found.")
        sys.exit(1)

    pda = PDA(states, input_symbols, stack_symbols, start_state, start_stack, accepting_states, transitions)

    if pda.process_input(html_content):
        print("Accepted")
    else:
        print("Not Accepted")