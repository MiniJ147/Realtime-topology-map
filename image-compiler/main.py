import json, os, numpy as np
import cv2

cfg = json.load(open('config.json',))
# print(cfg)

color_map = []

color_data = cfg['color-data']
color_grayscale = color_data['grayscale']
color_bgr = color_data['bgr']

for depth in range(256):
    for key in color_grayscale:
        if depth <  color_grayscale[key]: 
            color_map.append(color_bgr[key])
            break

print(color_map)

files = os.listdir(cfg['depth-frames-dir'])
image = cv2.imread(f"{cfg['depth-frames-dir']}/{files[-1]}")
h, w, c = image.shape
b, g, r = np.zeros((h,w)), np.zeros((h,w)), np.zeros((h,w))

print(h,w,c)
for y in range(h):
    for x in range(w):
        color = color_map[image[y][x][0]]
        b[y,x] = color[0]
        g[y,x] = color[1]
        r[y,x] = color[2]
        print(color_map[image[y][x][0]],end=" ")
    print("")

final_img = cv2.merge([b,g,r])
cv2.imwrite(f"{cfg['output-dir']}/final.png",final_img)

print("welcome to image-compiler")