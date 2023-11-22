import re
symbol='<asdfl content="sadfsadfsadfasdf">jlasjflasjf'
match=re.match(r'<(.*?)>', symbol)
extracted_content = match.group() if match else None
match = re.match(r'<([a-zA-Z0-9_]+)(.*?)>', extracted_content)
tag_name = f'<{match.group(1)}>' if match else None
attributes = match.group(2) if match else None
print(f'{tag_name} and {attributes}')