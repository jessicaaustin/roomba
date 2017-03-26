#
# lcd.py
#
import os, sys
import create
import time


ROOMBA_PORT='/dev/ttyAMA0'

robot = create.Create(ROOMBA_PORT, BAUD_RATE=115200)
robot.toSafeMode()


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


def lcd( mode, command ):
    
    output = '|{:.4}| {:.9}\n________________'.format(mode, command)
    print('----------------')
    print(output)
    print('----------------')
    

def main():

    robot.resetPose()
    robot.printSensors()

    print('\ndo nothing')
    fwd_speed = 0
    rot_speed = 0
    robot.go(fwd_speed, rot_speed)

    time.sleep(1)
    senses = robot.sensors([create.OI_MODE])
    mode = modeStr(senses[create.OI_MODE])
    command = commandStr(fwd_speed, rot_speed)
    lcd(mode, command)

    print('\nturn right')
    fwd_speed = 0
    rot_speed = -150
    robot.go(fwd_speed, rot_speed)

    time.sleep(1)
    senses = robot.sensors([create.OI_MODE])
    mode = modeStr(senses[create.OI_MODE])
    command = commandStr(fwd_speed, rot_speed)
    lcd(mode, command)

    print('\ngo straight')
    fwd_speed = 25
    rot_speed = 0
    robot.go(fwd_speed, rot_speed)

    time.sleep(1)
    senses = robot.sensors([create.OI_MODE])
    mode = modeStr(senses[create.OI_MODE])
    command = commandStr(fwd_speed, rot_speed)
    lcd(mode, command)

    print('\nturn left')
    fwd_speed = 10
    rot_speed = 50
    robot.go(fwd_speed, rot_speed)

    time.sleep(1)
    senses = robot.sensors([create.OI_MODE])
    mode = modeStr(senses[create.OI_MODE])
    command = commandStr(fwd_speed, rot_speed)
    lcd(mode, command)



		
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

