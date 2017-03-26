import sys
import select
import tty
import termios
import time
import os
import atexit

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

init_anykey()
while True:
   key = anykey()
   if key != None:
      if key == 32:  # spacebar
        print("STOP")
      elif key == 119:  # w
        print("faster")
      elif key == 115:  # s
        print("slower")
      elif key == 97:  # a
        print("left")
      elif key == 100:  # d
        print("right")
      else:
        print key
   else:
      print('.')
      time.sleep(0.1)

