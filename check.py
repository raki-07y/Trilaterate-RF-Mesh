#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sx126x
import time
import math

# ================= LORA INIT =================
node = sx126x.sx126x(
    serial_num="/dev/ttyS0",
    freq=868,
    addr=2,          # receiver address
    power=22,
    rssi=True,       # REQUIRED for RSSI
    air_speed=2400,
    relay=False
)



print("LoRa Receiver Started")
print("Listening infinitely...\n")


while True:
    node.receive(node)
