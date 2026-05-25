#!/usr/bin/env python3
import subprocess

# This launches the cif manager executable
try:
    # Run the command
    subprocess.Popen(["/usr/local/cif/manager/cif_startup_linux.exe"]) 
    print("The CIF Manager is running")
except FileNotFoundError:
    print(f"Error: The executable '{command[0]}' was not found.")