from PIL import Image

input_path = 'd:/toi/i.webp'
output_path = 'd:/toi/esettoi/public/assets/number_6.png'
copy_path = 'd:/toi/esettoi/public/assets/20_5.png'

img = Image.open(input_path).convert("RGBA")
pixdata = img.load()

width, height = img.size

# Get background color from corner (top-left)
bg_color = pixdata[0, 0][:3]
print(f"Background color: {bg_color}, size: {width}x{height}")

# Tolerance for "close to white" or background color
def is_bg(r, g, b, tolerance=30):
    return (
        abs(int(r) - int(bg_color[0])) < tolerance and
        abs(int(g) - int(bg_color[1])) < tolerance and
        abs(int(b) - int(bg_color[2])) < tolerance
    )

# BFS flood fill from all 4 edges to mark true background
from collections import deque

visited = set()
queue = deque()

# Seed from all borders
for x in range(width):
    for y in [0, height-1]:
        r, g, b, a = pixdata[x, y]
        if (x, y) not in visited and is_bg(r, g, b):
            queue.append((x, y))
            visited.add((x, y))

for y in range(height):
    for x in [0, width-1]:
        r, g, b, a = pixdata[x, y]
        if (x, y) not in visited and is_bg(r, g, b):
            queue.append((x, y))
            visited.add((x, y))

print(f"BFS flood fill starting with {len(queue)} seeds...")

while queue:
    cx, cy = queue.popleft()
    for nx, ny in [(cx-1,cy), (cx+1,cy), (cx,cy-1), (cx,cy+1)]:
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
            r, g, b, a = pixdata[nx, ny]
            if is_bg(r, g, b):
                visited.add((nx, ny))
                queue.append((nx, ny))

print(f"Flood fill done. Marking {len(visited)} pixels as transparent...")

# Make background transparent
for (x, y) in visited:
    pixdata[x, y] = (0, 0, 0, 0)

img.save(output_path, "PNG")

import shutil
shutil.copy(output_path, copy_path)

print(f"Saved transparent PNG to: {output_path}")
print("Done!")
