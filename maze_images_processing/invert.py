from PIL import Image
import PIL.ImageOps    

image = Image.open('output/cropped.jpg')

inverted_image = PIL.ImageOps.invert(image)

inverted_image.save('output/cropped-inv.jpg')