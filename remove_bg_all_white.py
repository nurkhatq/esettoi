from PIL import Image

input_path = 'd:/toi/i.webp'
output_path = 'd:/toi/esettoi/public/assets/number_6.png'
copy_path = 'd:/toi/esettoi/public/assets/20_5.png'

# Open image and convert to RGBA
img = Image.open(input_path).convert("RGBA")
width, height = img.size

# Extract pixels
pixdata = img.load()

# Define strict tolerance for white
def is_bg(r, g, b, tolerance=15):
    # Anything very bright/near white
    return r > (255 - tolerance) and g > (255 - tolerance) and b > (255 - tolerance)

transparent_count = 0
for y in range(height):
    for x in range(width):
        r, g, b, a = pixdata[x, y]
        if is_bg(r, g, b):
            pixdata[x, y] = (0, 0, 0, 0)
            transparent_count += 1

# Optional: do a slight cleanup to remove semi-transparent white fringes if any
# but purely replacing hard white usually works nicely against white backgrounds.

img.save(output_path, "PNG")

import shutil
shutil.copy(output_path, copy_path)

print(f"Removed {transparent_count} white background pixels (including the inner hole)!")
