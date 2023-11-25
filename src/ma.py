import re
import shlex
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
                    if '!--' not in modified_slice:
                        slices_list.append(modified_slice)
                    i = end_index + 1
                else:
                    i += 1
            else:
                i += 1
        # print(slices_list)
        for symbol in slices_list:
            match=re.match(r'<(.*?)>', symbol)
            extracted_content = match.group() if match else None
            match = re.match(r'<(/?[a-zA-Z0-9_]+)(.*?)>', extracted_content)
            tag_name = f'<{match.group(1)}>' if match else None
            attributes = match.group(2) if match else None
            list_att=shlex.split(attributes)
            current_stack_top = self.stack[-1] if self.stack else None
            transition = self.find_transition(current_state, tag_name, current_stack_top)
            # print(tag_name)
            if transition is None:
                # print(f"Salah di : {tag_name}\n")
                return False
            next_state, stack_action, stackkaa = transition
            current_state = next_state
            if extracted_content!=symbol and current_state!='stringstate':
                print(f"Salah di : {symbol}\n")
                return False
            if stackkaa != 'e' and stackkaa==current_stack_top:
                self.stack.pop()
            if stack_action != 'e':
                self.stack.append(stack_action)
            listofwajib=[]
            listofh=['id','style','class']
            type=[]
            for trans in self.transitions:
                if (trans[0]==tag_name):
                    if trans[2]=='w':
                        listofwajib.append(trans[1])
                    elif trans[2]=='h':
                        listofh.append(trans[1])
            if (tag_name=='<form>' ):
                type=['GET','POST']
            elif (tag_name =='<input>'):
                type = ['text','password','email','number','checkbox']
            elif (tag_name == '<button>'):
                type = ['submit','reset','button']
            # print(list_att)
            if (len(listofwajib)!=0):
                
                for elements in list_att:
                    # print(elements)
                    # print(listofwajib)
                    i=0
                    end_index = elements.find('=', i)
                    current_slice = elements[i:end_index]
                    # print(current_slice)
                    if (current_slice not in listofwajib) and (current_slice not in listofh):
                        print(f"Salah di : {current_slice}\n")
                        return False
                    elif current_slice in listofwajib:
                       
                        listofwajib.remove(current_slice)
                    elif current_slice in listofh:
                        listofh.remove(current_slice)
                if len(listofwajib)!=0:
                    print(f"Salah di : {listofwajib}\n")
                    
                    return False
            elif (len(list_att)!=0):
                # print("masuk sini\n")
                for elements in list_att:
                    i=0
                    end_index = elements.find('=', i)
                    current_slice = elements[i:end_index]
                    end_filled = elements.find('"',end_index+2)
                    filled_slice=elements[end_index+2:end_filled]
                    # print(filled_slice)
                    if current_slice not in listofwajib and (current_slice not in listofh):
                        print(f"Salah di : {current_slice}\n")
                        return False
                    elif current_slice in listofwajib:
                        listofwajib.remove(current_slice)
                    elif current_slice in listofh:
                        if current_slice in ['type','method']:
                            if filled_slice not in type:
                                print(f"Salah di : {filled_slice}\n")
                                # print("masuk sini 3\n")
                                return False
                

                
                


                

                
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
            html_content = file.read()

    
        html_content_stripped = html_content.replace('\n', ' ')
    except FileNotFoundError:
        print(f"HTML file {html_file} not found.")
        sys.exit(1)

    pda = PDA(states, input_symbols, stack_symbols, start_state, start_stack, accepting_states, transitions)

    if pda.process_input(html_content_stripped):
        print("Accepted")
    else:
        print("Not Accepted")