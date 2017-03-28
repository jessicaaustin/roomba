#
# lcd.py
#
import os, sys
import subprocess
import create
import time
import thread
import select
import tty
import termios
import atexit


ROOMBA_PORT='/dev/ttyAMA0'

robot = create.Create(ROOMBA_PORT, BAUD_RATE=115200)
robot.toSafeMode()

MAX_FORWARD = 50 # in cm per second
MAX_ROTATION = 200 # in cm per second
SPEED_INC = 5 # increment cm/s 
ROT_INC = 20 # increment in cm/s

# non-blocking console input code from http://stackoverflow.com/a/32382950
old_settings=None

def init_anykey():
   global old_settings
   old_settings = termios.tcgetattr(sys.stdin)
   new_settings = termios.tcgetattr(sys.stdin)
   new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON) # lflags
   new_settings[6][termios.VMIN] = 0  # cc
   new_settings[6][termios.VTIME] = 0 # cc
   termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

@atexit.register
def term_anykey():
   global old_settings
   if old_settings:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def anykey():
   ch_set = []
   ch = os.read(sys.stdin.fileno(), 1)
   while ch != None and len(ch) > 0:
      ch_set.append( ord(ch[0]) )
      ch = os.read(sys.stdin.fileno(), 1)
   return ch_set[0] if len(ch_set) > 0 else None


def modeStr( mode ):
    """ prints a string representing the input SCI mode """
    if mode == create.OFF_MODE: return 'OFF '
    if mode == create.PASSIVE_MODE: return 'PASV'
    if mode == create.SAFE_MODE: return 'SAFE'
    if mode == create.FULL_MODE: return 'FULL'
    return 'UNKN'

def commandStr( vel, rot):
    """ vel: (-50 to 50) => (vvv to ^^^) """
    """ rot: (-200 to 200) => (>>> to <<<) """

    speed = vel / 50.0 * 3.0
    if speed > 2.5:
        speedStr = '^^^'
    elif speed >= 1:
        speedStr = '_^^'
    elif speed > 0.01:
        speedStr = '_^_'
    elif speed < -2.5:
        speedStr = 'vvv'
    elif speed <= -1:
        speedStr = '_vv'
    elif speed < -0.01:
        speedStr = '_v_'
    else:
        speedStr = '___'

    turn = rot / 200.0 * 3.0
    if turn > 2.5:
        leftTurn  = '<<<' 
        rightTurn = '___' 
    elif turn >= 1:
        leftTurn  = '<<_' 
        rightTurn = '___' 
    elif turn > 0.01:
        leftTurn  = '<__' 
        rightTurn = '___' 
    elif turn < -2.5:
        leftTurn  = '___' 
        rightTurn = '>>>' 
    elif turn <= -1:
        leftTurn  = '___' 
        rightTurn = '_>>' 
    elif turn < -0.01:
        leftTurn  = '___' 
        rightTurn = '__>' 
    else:
        leftTurn  = '___'
        rightTurn = '___'
 
    return '{:.3}{:.3}{:.3}'.format(leftTurn, speedStr, rightTurn)


def lcd( output ):
    print('----------------')
    print(output)
    print('----------------')
    

def main():

    init_anykey()
    has_pressed_a_key = False

    #robot.resetPose()
    #robot.printSensors()

    robot.playNote(70, 10)
    robot.playNote(74, 20)

    fwd_speed = 0
    rot_speed = 0

    ssid = subprocess.check_output(['iwgetid', '-r']).strip()
    ipaddr = subprocess.check_output(['hostname', '-I']).strip()

    while True:

        key = anykey()
        if key != None:
            has_pressed_a_key = True
            if key == 32:  # spacebar / STOP
                fwd_speed = 0
                rot_speed = 0
            elif key == 119:  # w / increase speed
                fwd_speed += SPEED_INC
                if fwd_speed > MAX_FORWARD:
                    fwd_speed = MAX_FORWARD
            elif key == 115:  # s / decrease speed
                fwd_speed -= SPEED_INC
                if fwd_speed < -1*MAX_FORWARD:
                    fwd_speed = -1*MAX_FORWARD
            elif key == 97:  # a / turn left
                rot_speed += ROT_INC
                if rot_speed > MAX_ROTATION:
                    fwd_speed = MAX_ROTATION
            elif key == 100:  # d / turn right
                rot_speed -= ROT_INC
                if rot_speed < -1*MAX_ROTATION:
                    fwd_speed = -1*MAX_ROTATION
            else:
                pass

        robot.go(fwd_speed, rot_speed)

        senses = robot.sensors([create.OI_MODE])
        mode = modeStr(senses[create.OI_MODE])
        command = commandStr(fwd_speed, rot_speed)

        if has_pressed_a_key:
            output = '|{:.4}| {:.9}\n________________'.format(mode, command)
            lcd(output)
        else:
            lcd('{:.16}\n{:.16}'.format(ssid, ipaddr))

        time.sleep(0.1)

		
if __name__ == '__main__': 
    try:
        main()
    except Exception as err:
        print(err)
    except (KeyboardInterrupt, SystemExit):
        pass # continue to closing connection below
    print('Closing connection')
    robot.go(0,0)
    robot.close()

