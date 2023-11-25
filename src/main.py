import re
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
        slices_list = []
        remove_pattern = re.compile(r'\s*(id|style|class)\s*=\s*"[^"]*"\s*')

        i = 0
        while i < len(input_word):
            if input_word[i] == '<':
                end_index = input_word.find('>', i)
                if end_index != -1:
                    current_slice = input_word[i:end_index + 1]
                    modified_slice = remove_pattern.sub('', current_slice)

                    # Check if there is content immediately following the opening tag
                    content_start = end_index + 1
                    content_end = input_word.find('<', content_start)
                    if content_end != -1:
                        content = input_word[content_start:content_end].strip()
                        modified_slice += content

                    slices_list.append(modified_slice)
                    i = end_index + 1
                else:
                    i += 1
            else:
                
                i += 1
        for symbol in slices_list:
            match=re.match(r'<(.*?)>', symbol)
            extracted_content = match.group() if match else None
            match = re.match(r'<([a-zA-Z0-9_]+)(.*?)>', extracted_content)
            tag_name = f'<{match.group(1)}>'
            attributes = match.group(2)
            print(f"{tag_name} and {attributes}")
            current_stack_top = self.stack[-1] if self.stack else None
            transition = self.find_transition(current_state, tag_name, current_stack_top)
            if transition is None:
                print("salah di")
                print(tag_name)
                return False
            next_state, stack_action, stackkaa = transition
            current_state = next_state
            if extracted_content!=symbol and current_state!='stringstate':
                print("salah di")
                print(symbol)
                return False
            if stackkaa != 'e' or stackkaa==current_stack_top:
                self.stack.pop()
            if stack_action != 'e':
                self.stack.append(stack_action)
        return not self.stack
    

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
    except FileNotFoundError:
        print(f"PDA file {pda_file} not found.")
        sys.exit(1)

    try:
        with open(html_file, 'r') as file:
            html_content = file.readlines()
    

    # Remove newlines and spaces
        # html_content_stripped = html_content.replace('\n', '').replace(' ', '')
    except FileNotFoundError:
        print(f"HTML file {html_file} not found.")
        sys.exit(1)
    for z in range(len(html_content)):

        html_content[z]=html_content[z].replace('\n', '')
    pda = PDA(states, input_symbols, stack_symbols, start_state, start_stack, accepting_states, transitions)
    for line in html_content:
        Accept=True
        # print(html_content_stripped)
        if not pda.process_input(line):
            Accept=False
            break
    if (Accept):
        print("Accepted")
    else:
        print("Rejected")