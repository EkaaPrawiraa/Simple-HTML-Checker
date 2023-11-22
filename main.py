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
        i = 0
        slices_list=[]
        # print(slices_list)
        while i < len(input_word):
            if input_word[i] == '<':
                # Find the index of the closing '>'
                end_index = input_word.find('>', i)
                
                # Check if a closing '>' was found
                if end_index != -1:
                    # Extract the slice and add it to the list
                    current_slice = input_word[i:end_index + 1]
                    slices_list.append(current_slice)
                    
                    # Move the index to the character after '>'
                    i = end_index + 1
                else:
                    # If no closing '>' was found, move to the next character
                    i += 1
            else:
                # If the current character is not '<', move to the next character
                i += 1
        # Print the slices
        # print(slices_list)
        for symbol in slices_list:
            current_stack_top = self.stack[-1] if self.stack else None
            # print(current_state)
            # print(current_stack_top)
            # print(symbol)
            transition = self.find_transition(current_state, symbol, current_stack_top)
            # print(transition)
            if transition is None:
                return False

            next_state, stack_action, stackkaa = transition
            current_state = next_state
            if stackkaa != 'e':
                self.stack.pop()
            if stack_action != 'e':
                self.stack.append(stack_action)
            # print(self.stack)
        return current_state in self.accepting_states or not self.stack

    def find_transition(self, current_state, input_symbol, stack_top):
        for transition in self.transitions:
            if (
                transition[0] == current_state
                and (transition[1] == input_symbol )
                and (transition[2] == stack_top or (transition[2]=='e'))
            ):
                return transition[3], transition[4], transition[2]
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

            transitions = [line.strip().split() for line in lines[6:]]
            # print(transitions)
    except FileNotFoundError:
        print(f"PDA file {pda_file} not found.")
        sys.exit(1)

    try:
        with open(html_file, 'r') as file:
            html_content = file.read()

    # Remove newlines and spaces
        html_content_stripped = html_content.replace('\n', '').replace(' ', '')
    except FileNotFoundError:
        print(f"HTML file {html_file} not found.")
        sys.exit(1)

    pda = PDA(states, input_symbols, stack_symbols, start_state, start_stack, accepting_states, transitions)

    if pda.process_input(html_content_stripped):
        print("Accepted")
    else:
        print("Not Accepted")