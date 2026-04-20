from rembg import remove
from PIL import Image
import io
import shutil

input_path = 'd:/toi/i.webp'
output_png_path = 'd:/toi/esettoi/public/assets/number_6.png'

print("Opening image...")
with open(input_path, 'rb') as f:
    input_data = f.read()

print("Removing background (this may take a minute)...")
output_data = remove(input_data)

print("Saving transparent PNG...")
img = Image.open(io.BytesIO(output_data)).convert("RGBA")
img.save(output_png_path, "PNG")

# Also overwrite the original slots used in HTML
shutil.copy(output_png_path, 'd:/toi/esettoi/public/assets/20_5.png')

print(f"Done! Saved to {output_png_path}")
print(f"Image size: {img.size}, mode: {img.mode}")
