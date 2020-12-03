# small script to generate the base64 images in JS (from the png)

import base64
from PIL import Image
import os

def genJS(filename):
	"""Generate the base64 corresponding to the png
	See https://stackoverflow.com/questions/6375942/how-do-you-base-64-encode-a-png-image-for-use-in-a-data-uri-in-a-css-file"""
	return base64.b64encode(open(filename, "rb").read()).decode('utf-8')
	# return filename


src = []

# convert maps images to base64 data and write it in maps_images.js
for dir in os.listdir("."):
	if (os.path.isfile(dir)):
		continue
	img_path = dir+'/map.jpg'
	img64 = str(genJS(img_path))
	img = Image.open(img_path)
	width, height = img.size
	img.close()
	res = "maps['" + dir + "'] = { \n"
	res += f"  'width' : {width}, 'height' : {height}, \n"
	res += f"  'data' : 'data:image/jpg;base64,{img64}'\n"
	res += "}"
	src.append(res)

with open('../server/templates/game/maps_images.js', 'w') as f:
	f.write("var maps = [];\n")
	f.write("\n".join(src))