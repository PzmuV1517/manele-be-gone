#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import sys
from bleak import BleakScanner
from tabulate import tabulate

async def scan_devices():
    print("\nScanning for Bluetooth devices...")
    try:
        devices = await BleakScanner.discover(return_adv=True)
        
        if not devices:
            print("No devices found!")
            return

        devices_list = []
        for device, adv_data in devices.values():
            name = device.name or "Unknown"
            address = device.address
            rssi = device.rssi
            metadata = adv_data.manufacturer_data if hasattr(adv_data, 'manufacturer_data') else {}
            manufacturer = list(metadata.keys())[0] if metadata else "Unknown"
            
            devices_list.append([
                name,
                address,
                rssi,
                manufacturer
            ])
        
        # Sort by RSSI (strongest signal first)
        devices_list.sort(key=lambda x: x[2], reverse=True)
        
        print("\nFound {} devices:".format(len(devices)))
        print(tabulate(devices_list, 
              headers=['Device Name', 'MAC Address', 'RSSI', 'Manufacturer'], 
              tablefmt='grid'))
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your Bluetooth adapter is enabled!")
        sys.exit(1)

async def continuous_scan():
    print("Bluetooth Device Scanner")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            await scan_devices()
            print("\nWaiting 3 seconds before next scan...")
            await asyncio.sleep(3)
    
    except KeyboardInterrupt:
        print("\nScanning stopped by user")
        sys.exit(0)

def main():
    asyncio.run(continuous_scan())

if __name__ == "__main__":
    main()