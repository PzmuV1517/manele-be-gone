#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import asyncio
import random

STARTUP_MESSAGES = [
    "Initializing the matrix...",
    "The Gibson has been accessed...",
    "Welcome to the Desert of the Real...",
    "Hack the Planet!",
    "Time to crash the system..."
]

EXIT_MESSAGES = [
    "Wake up, Neo...",
    "Remember... All I'm offering is the truth...",
    "Never send a human to do a machine's job.",
    "Hasta la vista, baby.",
    "The cake is a lie."
]

BANNER = """
-------------------------------------------------------------------------------------------------------------------------
|  ███╗   ███╗ █████╗ ███╗   ██╗███████╗██╗     ███████╗     ██████╗ ███████╗     ██████╗  ██████╗ ███╗   ██╗███████╗   |
|  ████╗ ████║██╔══██╗████╗  ██║██╔════╝██║     ██╔════╝     ██╔══██╗██╔════╝    ██╔════╝ ██╔═══██╗████╗  ██║██╔════╝   |
|  ██╔████╔██║███████║██╔██╗ ██║█████╗  ██║     █████╗       ██████╔╝█████╗      ██║  ███╗██║   ██║██╔██╗ ██║█████╗     |
|  ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══╝  ██║     ██╔══╝       ██╔══██╗██╔══╝      ██║   ██║██║   ██║██║╚██╗██║██╔══╝     |
|  ██║ ╚═╝ ██║██║  ██║██║ ╚████║███████╗███████╗███████╗     ██████╔╝███████╗    ╚██████╔╝╚██████╔╝██║ ╚████║███████╗   |
|  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝     ╚═════╝ ╚══════╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝   |
|                                                                                       by Par@DoX Industries           |
-------------------------------------------------------------------------------------------------------------------------"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    clear_screen()
    print(random.choice(STARTUP_MESSAGES))
    print(BANNER)
    print("\n1. Scan for Bluetooth Devices")
    print("2. Launch Attack")
    print("3. Exit")
    return input("\nSelect an option (1-3): ")

def run_program(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except KeyboardInterrupt:
        print("\nReturning to main menu...")
    except subprocess.CalledProcessError:
        print(f"\nError running {script_name}")
        input("Press Enter to continue...")

def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_program('findAddr.py')
        elif choice == '2':
            run_program('maneleBeGone.py')
        elif choice == '3':
            clear_screen()
            print(random.choice(EXIT_MESSAGES))
            sys.exit(0)
        else:
            input("Invalid option. Press Enter to try again...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + random.choice(EXIT_MESSAGES))
        sys.exit(0)