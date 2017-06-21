from PIL import Image


background = Image.open("output/cropped-inv.jpg")
foreground = Image.open("input/overlay.png")

background = background.convert("RGBA")
foreground = foreground.convert("RGBA")

background.paste(foreground, (0, 0), foreground)

background.save('output/final.jpg')
