import pyaudio
import sys
import _thread
from time import sleep
from array import array
import RPi.GPIO as GPIO

clap = 0
wait = 1
flag = 0
pin = 24#LED所连的GPIO口
exitFlag = False


def Light_on(c):
    GPIO.output(c, True)
    print("Light on")
def Light_off(c):
    GPIO.output(c, False)
    print("Light off")

def waitForClaps(threadName):
    global clap
    global flag
    global wait
    global exitFlag
    global pin
    print("Waiting for more claps")
    sleep(wait)
    if clap == 1:#1次亮
        print("one claps")
        Light_on(pin)
    if clap == 2:#2次灭
        Light_off(pin)
        print("two claps")
    if clap == 3:#3次循环亮灭
        i = 0
        while i < 2:
            Light_on(pin)
            sleep(0.8)
            Light_off(pin)
            sleep(1)
            i+=1
        Light_on(pin)
    if clap > 20:#超过20次退出程序
        exitFlag = True
        print("program termination")
    print("Claping Ended")
    clap = 0
    flag = 0


def main():
    global clap
    global flag
    global pin

    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    threshold = 500#手动调整拍手阈值
    max_value = 0
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    try:
        print("Clap detection initialized")
        while True:
            data = stream.read(chunk)
            as_ints = array('h', data)
            max_value = max(as_ints)
            if max_value > threshold:#检测到声音输入达到标准，记录次数
                clap += 1
                print("Clapped")
            if clap == 1 and flag == 0:
                _thread.start_new_thread(waitForClaps, ("waitThread",))
                flag = 1
            if exitFlag:
                sys.exit(0)#退出整个程序
    except (KeyboardInterrupt, SystemExit):
        print("\rExiting")
        stream.stop_stream()
        stream.close()
        p.terminate()
        GPIO.cleanup()


if __name__ == '__main__':
    main()