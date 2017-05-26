import time

import cv2
import numpy as np
import os.path

from actrions import straight, left, right
from directkey import PressKey, ReleaseKey, W, S
# from PIL import ImageGrab
from draw_lanes import draw_lanes
from grabscreen import grab_screen
# Game window defition
from manual_drive_ai import roi
from getkeys import key_check
from statistics import mean

_screen_box = (0,40,1024,768)
_vertices = np.array([[[10, 760], [10, 700], [455, 350], [555, 350], [1010, 700], [1010, 760]]], dtype=np.int32)
_file_name = "training_data.npy"
_balanced_file_name = "balanced_data.npy"


def keys_to_output(keys):
    # [A,W,D,S]
    output = [0,0,0,0]
    if 'A' in keys:
        output[0] = 1
    if 'W' in keys:
        output[1] = 1
    if 'D' in keys:
        output[2] = 1
    if 'S' in keys:
        output[3] = 1
    return output


def process_image(original_image):
    """Make stuff on image"""
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = roi(processed_img, _vertices)
    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 100, np.array([]), 50, 15)
    m1 = 0
    m2 = 0
    try:
        l1,  l2, m1, m2 = draw_lanes(original_image, lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0, 255, 0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0, 255, 0], 30)
    except Exception as e:
        print(str(e))
        pass
    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 0, 0], 3)
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img,original_image, m1, m2


def manual_ai():
    last_time = time.time()
    while(True):
        #screen = np.array(ImageGrab.grab(bbox=_screen_box))
        screen = grab_screen(_screen_box)
        print('Loop time: {}'.format(time.time()-last_time))
        last_time = time.time()
        new_screen,original_image, m1, m2 = process_image(screen)
        cv2.imshow('window', new_screen)
        cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

        if m1 < 0 and m2 < 0:
            right()
        elif m1 > 0 and m2 > 0:
            left()
        else:
            straight()


        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def main():
    if os.path.isfile(_file_name):
        print("File exists, load training data.")
        traning_data = list(np.load(_file_name))
    else:
        print("Starting new data.")
        traning_data = []
    last_time = time.time()
    loop_time = []
    while(True):
        screen = grab_screen(_screen_box)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = cv2.resize(screen, (80,60))
        output = keys_to_output(key_check())
        traning_data.append([screen,output])

        #print('Loop time: {}'.format(time.time()-last_time))
        loop_time.append(time.time()-last_time)
        last_time = time.time()

        if len(traning_data) % 500 == 0:
            mean_loop_time = mean(loop_time)
            print("Training data at len {}, time {}, fps {}".format(len(traning_data),
                                                                    mean_loop_time,
                                                                    1/mean_loop_time))
            np.save(_file_name, traning_data)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def delay():
    for i in list(range(4))[::1]:
        print(i+1)
        time.sleep(1)

def simple_input():
    print('up')
    PressKey(W)
    time.sleep(3)
    ReleaseKey(W)
    print('down')
    PressKey(S)
    time.sleep(2)
    ReleaseKey(S)

if "__main__" == __name__:
    delay()
    main()
