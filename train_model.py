
import numpy as np
from alexnet import alexnet
from game_trainer import _balanced_file_name


WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCH = 8
MODEL_NAME = "pyets2-truck-{}-{}-{}-epochs.model".format(LR, 'alexnetv2', EPOCH)

model = alexnet(WIDTH, HEIGHT, LR)

training_data = np.load(_balanced_file_name)

train = training_data[:-500]
test = training_data[-500:]

X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
test_y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=EPOCH,
          validation_set=({'input': test_x}, {'targets': test_y}),
          snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

# tensorboars --logdir=foo:c:/..../

model.save(MODEL_NAME)
