import os
import re

def remove_comments(content):
    def replacer(match):
        s = match.group(0)
        if s.startswith('#'):
            return ""
        else:
            return s

    pattern = re.compile(
        r'#.*|"(?:\\.|[^\\"])*"|\'(?:\\.|[^\\\'])*\'',
        re.MULTILINE
    )
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.strip().startswith('#'):
            continue
        
        clean_line = line
        in_string = False
        quote_char = None
        for i, char in enumerate(line):
            if char in ('"', "'"):
                if not in_string:
                    in_string = True
                    quote_char = char
                elif quote_char == char:
                    in_string = False
                    quote_char = None
            elif char == '#' and not in_string:
                clean_line = line[:i].rstrip()
                break
        
        new_lines.append(clean_line)
    
    return '\n'.join(new_lines)

root_dir = r"c:\Users\ashwin\OneDrive\Desktop\TeamTaskManager"
for root, dirs, files in os.walk(root_dir):
    if 'venv' in dirs:
        dirs.remove('venv')
    if '.git' in dirs:
        dirs.remove('.git')
        
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    content = f.read()
                except:
                    continue
            
            cleaned = remove_comments(content)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(cleaned)

print("Done cleaning comments.")
