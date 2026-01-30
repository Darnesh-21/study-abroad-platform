with open('backend/app/api/counselor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove lines that contain only the box-drawing divider character
lines = content.split('\n')
filtered_lines = []
for line in lines:
    if line.strip() and all(c == '━' for c in line.strip()):
        continue  # Skip this line
    filtered_lines.append(line)

with open('backend/app/api/counselor.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(filtered_lines))

print("Removed divider lines!")
