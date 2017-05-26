import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
from game_trainer import _file_name, _balanced_file_name
import cv2

def main():
    try:
        training_data = np.load(_file_name)
    except Exception as e:
        print("Unable to load data from {}\n{}".format(_file_name, str(e)))
        return
    print(len(training_data))
    df = pd.DataFrame(training_data)
    print(df.head())
    print(Counter(df[1].apply(str)))
    lefts = []
    right = []
    forwards = []
    idle = []
    slow = []
    for_left = []
    for_right = []

    shuffle(training_data)
    # '[0, 1, 0, 0]': 7042,
    # '[0, 0, 0, 0]': 2727,
    # '[0, 1, 1, 0]': 391,
    # '[1, 1, 0, 0]': 337,
    # '[0, 0, 1, 0]': 229,
    # '[0, 0, 0, 1]': 164,
    # '[1, 0, 0, 0]': 110})

    for data in training_data:
        img = data[0]
        choice = data[1]
        # [A,W,D,S]
        if choice == [0, 1, 0, 0]:
            forwards.append(data)
        elif choice == [0, 0, 0, 0]:
            idle.append(data)
        elif choice == [0, 1, 1, 0]:
            for_right.append(data)
        elif choice == [1, 1, 0, 0]:
            for_left.append(data)
        elif choice == [0, 0, 1, 0]:
            right.append(data)
        elif choice == [0, 0, 0, 1]:
            slow.append(data)
        elif choice == [1, 0, 0, 0]:
            lefts.append(data)
        else:
            print('No match!!! {}'.format(choice))

    min_len = min([len(forwards), len(lefts), len(right), len(idle),
                  len(slow), len(for_left), len(for_right)])
    print('min_len: {}'.format(min_len))
    forwards = forwards[:min_len]
    lefts = lefts[:min_len]
    right = right[:min_len]
    idle = idle[:min_len]
    slow = slow[:min_len]
    for_left = for_left[:min_len]
    for_right = for_right[:min_len]
    
    final_data = forwards + lefts + right + idle + slow + for_left + for_right
    print(len(final_data))
    np.save(_balanced_file_name, final_data)

def main_old():
    try:
        train_data = np.load(_file_name)
    except Exception as e:
        print("Unable to load data {}".format(str(e)))
        return
    for data in train_data:
        img = data[0]
        choice = data[1]
        cv2.imshow("test", img)
        print (choice)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destrowAllWindows()
            break

if __name__ == "__main__":
    main()
