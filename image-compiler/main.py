import json, os, numpy as np
import cv2

# bgr constants
BLUE = 0
GREEN = 1
RED = 2

class Image_Compiler:
    color_map = []
    def __init__(self):
        self.load_config()
        self.load_color_map()

    def load_config(self):
        self.cfg = json.load(open('config.json'))
        self.color_grayscale = self.cfg['color-data']['grayscale']
        self.color_bgr = self.cfg['color-data']['bgr']

        self.output_dir = self.cfg['output-dir']
        self.input_dir = self.cfg['input-dir']
    
    def load_color_map(self):
         for depth in range(256):
            for key in self.color_grayscale:
                if depth < self.color_grayscale[key]:
                    self.color_map.append(self.color_bgr[key])
                    break

    def compile_image(self,file_name: str):
        # input data
        input_img = cv2.imread(f"{self.input_dir}/{file_name}")
        h, w, c = input_img.shape
        
        # output img channels
        b,g,r = np.zeros((h,w)), np.zeros((h,w)), np.zeros((h,w))

        for y in range(h):
            for x in range(w):
                depth_val = input_img[y][x][0]
                bgr = self.color_map[depth_val]

                # setting channels
                b[y,x] = bgr[BLUE]
                g[y,x] = bgr[GREEN]
                r[y,x] = bgr[RED]
        
        out_img = cv2.merge([b,g,r])
        cv2.imwrite(f"{self.output_dir}/final.png",out_img)


print("welcome to image-compiler")
comp = Image_Compiler()
comp.compile_image('frame-1721277859.png')