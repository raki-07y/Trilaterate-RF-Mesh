# -*- coding:utf-8 -*-
import sx126x
import time
import threading
import sys
import SH1106  # Local library
from PIL import Image, ImageDraw, ImageFont

# --- Global Flags ---
running = True
is_sos_active = False  # SOS screen-ah lock panna indha flag use aagum

# --- Initialize OLED (SH1106) ---
disp = SH1106.SH1106()
disp.Init()
disp.clear()

# Load Fonts (Font.ttf file unga folder-la irukanum)
try:
    font_header = ImageFont.truetype('Font.ttf', 14)
    font_msg = ImageFont.truetype('Font.ttf', 12)
except:
    font_header = ImageFont.load_default()
    font_msg = ImageFont.load_default()

# --- Initialize LoRa (SX1262) ---
# Tourist Address = 0
node = sx126x.sx126x(serial_num="/dev/ttyS0", freq=868, addr=0, power=22, rssi=True, air_speed=2400, relay=False)

serial_lock = threading.Lock()

def update_display(line1, line2, mode="NORMAL"):
    """OLED-la text draw panna indha function use aagum"""
    global is_sos_active
    
    # SOS alert active-ah irundha, normal ping messages-ah screen-la kaata koodadhu
    if is_sos_active and mode == "NORMAL":
        return

    # Create blank white image
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    
    # Border draw pannuvom
    draw.rectangle([(0,0),(127,63)], fill = 255, outline = 0)
    
    if mode == "SOS":
        # SOS Mode: Inverted (Black background, White text)
        draw.rectangle([(2,2),(125,61)], fill = 0)
        draw.text((35, 20), "!!! SOS !!!", font=font_header, fill=1)
        draw.text((20, 40), "SENDING SIGNAL", font=font_msg, fill=1)
    else:
        # Normal Mode
        draw.text((30, 5), "TOURIST NODE", font=font_header, fill=0)
        draw.line([(10, 20), (117, 20)], fill=0)
        draw.text((10, 28), line1, font=font_msg, fill=0)
        draw.text((10, 45), line2, font=font_msg, fill=0)

    disp.ShowImage(disp.getbuffer(image))

def get_broadcast_header():
    """Nearby towers (65535) kku anupa header ready pannum"""
    offset_frequence = 868 - (850 if 868 > 850 else 410)
    target_addr = 65535 # Broadcast address
    header = bytes([target_addr >> 8]) + bytes([target_addr & 0xff]) + \
             bytes([offset_frequence]) + bytes([node.addr >> 8]) + \
             bytes([node.addr & 0xff]) + bytes([node.offset_freq])
    return header

def background_receive():
    """Towers kitta irundhu varra badhil-ah listen panna"""
    global running
    while running:
        with serial_lock:
            node.receive()
        time.sleep(0.1)

def background_ping():
    """Ovvoru second-um nearby towers-ku ping anupa"""
    global running, is_sos_active
    header = get_broadcast_header()
    while running:
        # SOS active-ah illadha podhu mattum dhaan Ping pannanum/Display pannanum
        if not is_sos_active:
            packet = header + "PING".encode()
            curr_time = time.strftime("%H:%M:%S")
            
            with serial_lock:
                node.send(packet)
                update_display(f"Ping sent", f"Time: {curr_time}")
                sys.stdout.write(f"\r[STATUS] Last Ping: {curr_time}")
                sys.stdout.flush()
        
        time.sleep(1)

def send_sos():
    """Emergency SOS anupum podhu screen-ah 3 seconds freeze pannanum"""
    global is_sos_active
    
    # Screen-ah lock pandrom
    is_sos_active = True
    
    # SOS Packet ready pannuvom
    header = get_broadcast_header()
    packet = header + "SOS_EMERGENCY".encode()
    
    with serial_lock:
        node.send(packet)
        # SOS screen-ah display-la kaatrom
        update_display("", "", mode="SOS")
        print(f"\n[{time.strftime('%H:%M:%S')}] EMERGENCY SOS SENT VIA KEY1")

    # 3 Seconds wait pannuvom (Indha time-la background ping disturb aagaadhu)
    time.sleep(1.5)
    
    # Lock-ah release pandrom, ippo thirumbavum normal ping screen varum
    is_sos_active = False
    print("Resuming Normal Operations...")

def button_listener():
    """OLED-la ulla KEY1 button-ah monitor panna"""
    global running
    print("Button Monitor Active (KEY1 for SOS)")
    while running:
        # digital_read == 1 na button press aagi irukku nu artham
        if disp.RPI.digital_read(disp.RPI.GPIO_KEY1_PIN) == 1:
            send_sos()
        time.sleep(0.15) # Debounce delay

# --- MAIN EXECUTION ---
try:
    print("\n" + "="*45)
    print(" LORA TOURIST NODE: READY")
    print(" Press KEY1 on OLED for Emergency SOS")
    print("="*45 + "\n")
    
    # Moonu threads-aiyum parallel-ah start pandrom
    t_recv = threading.Thread(target=background_receive, daemon=True)
    t_ping = threading.Thread(target=background_ping, daemon=True)
    t_btn  = threading.Thread(target=button_listener, daemon=True)

    t_recv.start()
    t_ping.start()
    t_btn.start()

    # Program-ah activate-la veika
    while running:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping system...")
finally:
    running = False
    time.sleep(0.5)
    disp.clear()
    disp.reset()
    disp.RPI.module_exit() # Hardware resources-ah clean-ah close panna
    print("OLED Cleared and System Exited.")
