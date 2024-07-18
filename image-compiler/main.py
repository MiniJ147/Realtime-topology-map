import json, os
import cv2

cfg = json.load(open('config.json',))
print(cfg)

files = os.listdir(cfg['depth-frames-folder'])
image = cv2.imread(f"{cfg['depth-frames-folder']}/{files[-1]}")
h, w, c = image.shape
print(h,w,c)
for y in range(h):
    for x in range(w):
        print(image[y][x][0],end=" ")
    print("")


print("welcome to image-compiler")