
import re

def check_lines_in_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
    line1 = re.search(r'(?i)this is a new line 1', content)
    line2 = re.search(r'(?i)the sum of 2\s*\+\s*3\s*=', content)
    
    return bool(line1), bool(line2)

file_path = '/home/user/testing-building-new-app/test.md'
line1_present, line2_present = check_lines_in_file(file_path)

print(f"Line 1 ('this is a new line 1') is present: {line1_present}")
print(f"Line 2 ('this is the sum of 2+3 =???') is present: {line2_present}")

if line1_present and line2_present:
    print("Both required lines are already present in the file.")
else:
    print("One or both required lines are missing from the file.")
