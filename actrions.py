from directkey import PressKey, W, ReleaseKey, A, D


def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    #ReleaseKey(A)


def right():
    PressKey(D)
    ReleaseKey(W)
    ReleaseKey(A)
    #ReleaseKey(D)


def slow_down():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)