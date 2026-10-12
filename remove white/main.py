from PIL import Image

input_file = "C:\\Users\\stijn\\Downloads\\Untitled.png"
output_file = "output.png"

img = Image.open(input_file).convert("RGBA")
pixels = img.getdata()

threshold = 230  # 0-255

nieuwe_pixels = []

for pixel in pixels:
    r, g, b, a = pixel

    if r >= threshold and g >= threshold and b >= threshold:
        nieuwe_pixels.append((r, g, b, 0))
    else:
        nieuwe_pixels.append(pixel)

img.putdata(nieuwe_pixels)
img.save(output_file)

print(f"Opgeslagen als {output_file}")