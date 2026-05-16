import sys
import sx126x
import time
import select
import termios
import tty

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())
node = sx126x.sx126x(serial_num = "/dev/ttyS0",freq=868,addr=0,power=22,rssi=True,air_speed=2400,relay=False)
def send_deal():
    get_rec = ""
    print("")
    print("input a string such as \033[1;32m0,868,Hello World\033[0m")
    print("please input and press Enter key:",end='',flush=True)

    while True:
        rec = sys.stdin.read(1)
        if rec != None:
            if rec == '\x0a': break
            get_rec += rec
            sys.stdout.write(rec)
            sys.stdout.flush()

    get_t = get_rec.split(",")

    offset_frequence = int(get_t[1])-(850 if int(get_t[1])>850 else 410)
    data = bytes([int(get_t[0])>>8]) + bytes([int(get_t[0])&0xff]) + bytes([offset_frequence]) + bytes([node.addr>>8]) + bytes([node.addr&0xff]) + bytes([node.offset_freq]) + get_t[2].encode()
    node.send(data)
    
def receive_deal():
    print("Waiting for Message.....")
    print("______________________________________________")
    while True:
            node.receive()
try:
    time.sleep(1)
    print("\n______________________________________________")
    print("Press \033[1;35mS\033[0m   to send message")
    print("Press \033[1;32mR\033[0m   to receive message")
    print("Press \033[1;37mEsc\033[0m to exit")
    print("______________________________________________")
    
    while True:

        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            c = sys.stdin.read(1)

            # dectect key Esc
            if c == '\x1b': break
            # dectect key i
            if c == '\x53':
                send_deal()
            if c == '\x52':
                receive_deal()
            sys.stdout.flush()
            
        
        
except:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
