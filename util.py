import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import win32api, win32con, win32gui
from mss import mss

def random_sleep(sec):
    time.sleep(sec + 0.3*(np.random.rand()-0.5))

def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff

def find_img_pos(screen, img, count=1, dist=None, interval=5, verbose=False):
    H, W = screen.shape[0:2]
    h, w = img.shape[0:2]
    min_commutative_image_diff = 10000*np.ones([count])
    pos = np.zeros([count, 2], dtype=np.int32)
    all_pixel_num = (H-h)*(W-w)
    for i in range(0, H-h, interval):
        for j in range(0, W-w, interval):
            commutative_image_diff = get_image_difference(img, screen[i:i+h,j:j+w])
            idx = np.argmax(min_commutative_image_diff)
            if commutative_image_diff < min_commutative_image_diff[idx]:
                min_commutative_image_diff[idx] = commutative_image_diff
                pos[idx] = np.array([i, j], dtype=np.int32)
                        
            if verbose:
                current_pixel_num = i*(W-w)+j
                sys.stdout.write('\ron scanning... {:.2f}%'.format(current_pixel_num/all_pixel_num*100))
    return pos, min_commutative_image_diff

def get_screen(sct, monitor):
    screen = np.array(sct.grab(monitor))
    return screen

def click(pos):
    x, y = pos[1], pos[0]
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    
def drag(pos1, pos2):
    pos1 = pos1[::-1]
    pos2 = pos2[::-1]
    win32api.SetCursorPos(pos1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos1[0], pos1[1], 0, 0); time.sleep(0.1)
    for i in np.arange(0, 1, 0.05):
        win32api.SetCursorPos(pos1 + ((pos2-pos1)*i).astype('int')); time.sleep(0.03)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos2[0], pos2[1], 0, 0)
    
def get_mouse_pos():
    _, _, pos = win32gui.GetCursorInfo()
    return np.array(pos)[::-1]