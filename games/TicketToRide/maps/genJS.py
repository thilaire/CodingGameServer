# small script to generate the base64 images in JS (from the png)

import base64
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
	img64 = str(genJS(dir+'/map.jpg'))
	res = f"maps['{dir}'] = "
	res += f"'data:image/jpg;base64,{img64}'"
	src.append(res)

with open('../server/templates/game/maps_images.js', 'w') as f:
	f.write("var maps = [];")
	f.write("\n".join(src))