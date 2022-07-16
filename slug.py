from sense_emu import SenseHat
from random import randint
import time

sense = SenseHat()
sense.clear()
bule = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
slug = [[2, 4], [3, 4], [4, 4]]
direction = 'right'
blank = (0, 0, 0)
vegetables = []
score = 0
pause = 0.5
dead = False

def move():#slug的功能函数
    global score
    global pause
    global remove
    global dead
    remove = True
    dead = False
    last = slug[-1]
    first = slug[0]
    next = list(last)
    if direction == 'right':
        next[0] = last[0] + 1
    elif direction == 'left':
        next[0] = last[0] - 1
    elif direction == 'up':
        next[1] = last[1] - 1
    elif direction == 'down':
        next[1] = last[1] + 1
    wrap(next)
    if next in slug:
        dead = True
    slug.append(next)
    sense.set_pixel(next[0], next[1], white)
    if next in vegetables:
        vegetables.remove(next)
        score += 1
        if score % 3 == 0:
            remove = False
            pause = pause * 0.9
    if remove == True:
        sense.set_pixel(first[0], first[1], blank)
        slug.remove(first)


def wrap(pix):  # 更改坐标

    if pix[0] > 7:
        pix[0] = 0
    if pix[0] < 0:
        pix[0] = 7
    if pix[1] < 0:
        pix[1] = 7
    if pix[1] > 7:
        pix[1] = 0

    return pix


def joystick_moved(event):  # 控制上下左右的操作
    global direction
    direction = event.direction


def vege():  # 得分点设置，用于增加长度
    new = slug[0]
    while new in slug:
        x = randint(0, 7)
        y = randint(0, 7)
        new = [x, y]
    sense.set_pixel(new[0], new[1], red)
    vegetables.append(new)


while dead is not True:  # 主函数
    move()
    if len(vegetables) < 1:
        vege()
    sense.stick.direction_any = joystick_moved
    time.sleep(pause)
sense.show_message("game over")
