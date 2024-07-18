import json, os, numpy as np
import cv2
import threading, time

# bgr constants
BLUE = 0
GREEN = 1
RED = 2

# state managment
AWAITING_START = 0
START = 1
ACTIVE = 2
PAUSE = 3
RELOAD_CONFIG = 4
RESTART = 5
SHUTDOWN_PROGRAM = 6

state_msg_map = {
    AWAITING_START: "awaiting start",
    START: "starting",
    ACTIVE: "active",
    PAUSE: "paused",
    RELOAD_CONFIG: "Reloading Config",
    RESTART: "restarting compiler",
    SHUTDOWN_PROGRAM: "Shuting Down Program"
}

STATE = AWAITING_START

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
        self.thread_sleep_time = self.cfg['timing']['thread-sleep'] 
        self.no_files_sleep = self.cfg['timing']['no-files']

        print(self.cfg)
    
    def load_color_map(self):
         self.color_map = []
         for depth in range(256):
            for key in self.color_grayscale:
                if depth < self.color_grayscale[key]:
                    self.color_map.append(self.color_bgr[key])
                    break

    def compile_image(self,file_name: str):
        # input data
        input_img = cv2.imread(f"{self.input_dir}/{file_name}")
        if not type(input_img) is np.ndarray:
            print("image null returning")
            return
         
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

def thread_runtime():
    global STATE
    compiler = Image_Compiler()

    while(STATE!=SHUTDOWN_PROGRAM):
        if STATE==AWAITING_START or STATE==PAUSE:
            time.sleep(compiler.thread_sleep_time)
            continue
        elif STATE==RELOAD_CONFIG:
            compiler.load_config()
            compiler.load_color_map()
            STATE = ACTIVE
            continue
        elif STATE==RESTART:
            compiler = Image_Compiler()
            STATE = AWAITING_START
            continue
        files = os.listdir(compiler.input_dir)
        while not files and STATE==ACTIVE:
            print('no files...')
            time.sleep(compiler.no_files_sleep)
            files = os.listdir(compiler.input_dir)

        if STATE==ACTIVE and files:
            compiler.compile_image(files[-1])    
            os.remove(f"{compiler.input_dir}/{files[-1]}")
            time.sleep(compiler.thread_sleep_time)

exec_thread = threading.Thread(target=thread_runtime)
exec_thread.start()

choice_map = {1:ACTIVE, 2:PAUSE, 3:RELOAD_CONFIG, 4:RESTART, 5:SHUTDOWN_PROGRAM}
while(STATE != SHUTDOWN_PROGRAM):
    choice = int(input(f"State: {state_msg_map[STATE]}\n1. Start, 2.Pause, 3.Reload Config, 4. Restart Compiler, 5. Shutdown\n>>> "))
    STATE = choice_map[choice]

exec_thread.join()