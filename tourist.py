import sx126x
import time
import threading
import sys

# Node Initialization
node = sx126x.sx126x(serial_num="/dev/ttyS0", freq=868, addr=0, power=22, rssi=True, air_speed=2400, relay=False)

serial_lock = threading.Lock()
running = True

def get_broadcast_header():
    """Generates a header for all nearby towers (65535)."""
    offset_frequence = 868 - (850 if 868 > 850 else 410)
    target_addr = 65535 # Broadcast to all nearby LoRa modules
    
    header = bytes([target_addr >> 8]) + bytes([target_addr & 0xff]) + \
             bytes([offset_frequence]) + bytes([node.addr >> 8]) + \
             bytes([node.addr & 0xff]) + bytes([node.offset_freq])
    return header

def background_receive():
    global running
    while running:
        with serial_lock:
            # Nearby towers badhil anupuna inge receive aagum
            node.receive()
        time.sleep(0.1)

def background_ping():
    global running
    # Broadcast header common for all pings
    header = get_broadcast_header()
    
    while running:
        packet = header + "PING_NEARBY".encode()
        
        with serial_lock:
            node.send(packet)
            current_time = time.strftime("%H:%M:%S")
            # Clear line and update status
            sys.stdout.write(f"\r[STATUS] Last Broadcast Ping sent at {current_time} | Press 'S' for SOS: ")
            sys.stdout.flush()
            
        time.sleep(1) # Send every second

def send_sos():
    header = get_broadcast_header()
    packet = header + "SOS_EMERGENCY_NEARBY".encode()
    
    with serial_lock:
        node.send(packet)
        print("\n" + "!"*57)
        print(f"!!! EMERGENCY SOS BROADCAST TO ALL TOWERS AT {time.strftime('%H:%M:%S')} !!!")
        print("!"*57 + "\n")

# --- MAIN ---
try:
    print("\n" + "="*45)
    print(" LORA TOURIST NODE: BROADCAST MODE ACTIVE")
    print(" Threads: Receive & Ping Initialized...")
    print("="*45 + "\n")

    # Start threads
    threading.Thread(target=background_receive, daemon=True).start()
    threading.Thread(target=background_ping, daemon=True).start()

    while True:
        # Wait for keyboard input ('S' or 'I')
        cmd = input().upper()
        
        if cmd == 'S':
            send_sos()
        elif cmd == 'I':
            running = False
            break

except Exception as e:
    print(f"\nError: {e}")
finally:
    running = False
    print("\nSystem Disarmed. Exiting.")
